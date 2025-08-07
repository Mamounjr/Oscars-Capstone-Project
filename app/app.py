from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import boto3
from werkzeug.utils import secure_filename
import json
import uuid
import os

app = Flask(__name__)
CORS(app)

s3 = boto3.client('s3')
BUCKET_NAME = 'oscars-project'

# Local folders for uploads
UPLOAD_FOLDER = "uploads"
#PDF_FOLDER = os.path.join(UPLOAD_FOLDER, "pdfs")
#COVER_FOLDER = os.path.join(UPLOAD_FOLDER, "covers")
METADATA_FOLDER = os.path.join(UPLOAD_FOLDER, "metadata")

# Create directories if they don't exist
for folder in [ METADATA_FOLDER]:
    os.makedirs(folder, exist_ok=True)

VALID_CATEGORIES = ["art", "sports", "music", "science"]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/resourcespage')
def resourcespage():
    return render_template('resources.html')


@app.route('/uploadpage')
def uploadpage():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    pdf = request.files.get('pdf')
    cover = request.files.get('cover')
    title = request.form.get('title')
    author = request.form.get('author')
    year = request.form.get('year')
    category = request.form.get('category')

    if not all([pdf, cover, title, author, year, category]):
        return jsonify({"message": "Missing required fields"}), 400
    if category not in VALID_CATEGORIES:
        return jsonify({"message": "Invalid category"}), 400

    # Secure and unique filenames
    pdf_filename = f"{uuid.uuid4()}_{secure_filename(pdf.filename)}"
    cover_filename = f"{uuid.uuid4()}_{secure_filename(cover.filename)}"

    # Upload to S3
    try:
        s3.upload_fileobj(pdf, BUCKET_NAME, f"pdfs/{pdf_filename}", ExtraArgs={'ContentType': 'application/pdf'})
        s3.upload_fileobj(cover, BUCKET_NAME, f"covers/{cover_filename}", ExtraArgs={'ContentType': cover.mimetype})
    except Exception as e:
        return jsonify({"message": f"S3 upload failed: {str(e)}"}), 500

    # Pre-signed URLs
    pdf_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET_NAME, 'Key': f"pdfs/{pdf_filename}"},
        ExpiresIn=3600  # valid for 1 hour
    )

    cover_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET_NAME, 'Key': f"covers/{cover_filename}"},
        ExpiresIn=3600  # valid for 1 hour
    )

    metadata = {
        "title": title,
        "author": author,
        "year": year,
        "pdf_url": pdf_url,
        "cover_url": cover_url
    }

    # Save metadata locally
    metadata_path = os.path.join(METADATA_FOLDER, f"{category}_{pdf_filename}.json")
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f)

    return jsonify({
        "message": "Upload successful",
        "data": metadata
    }), 200

@app.route('/resources/<category>', methods=['GET'])
def get_resources(category):
    if category not in VALID_CATEGORIES:
        return jsonify({"message": "Invalid category"}), 400

    resources = []
    for filename in os.listdir(METADATA_FOLDER):
        if filename.startswith(category):
            with open(os.path.join(METADATA_FOLDER, filename), 'r') as f:
                resources.append(json.load(f))
    return jsonify(resources)

# Serve static files
@app.route('/pdfs/<filename>')
def serve_pdf(filename):
    return send_from_directory(PDF_FOLDER, filename)

@app.route('/covers/<filename>')
def serve_cover(filename):
    return send_from_directory(COVER_FOLDER, filename)
'''
@app.route('/')
def index():
    return send_from_directory('.', 'upload.html')'''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
