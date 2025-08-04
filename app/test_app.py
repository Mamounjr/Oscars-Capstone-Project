import os
import io
import json
import uuid
import pytest
from app import app, s3, BUCKET_NAME, METADATA_FOLDER
from botocore.stub import Stubber

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

@pytest.fixture
def s3_stub():
    with Stubber(s3) as stubber:
        yield stubber

def test_upload_success(client, s3_stub):
    pdf_data = io.BytesIO(b"%PDF-1.4 test pdf content")
    cover_data = io.BytesIO(b"\x89PNG\r\n\x1a\n test image content")
    
    pdf_filename = f"{uuid.uuid4()}_test.pdf"
    cover_filename = f"{uuid.uuid4()}_cover.png"

    # Mock S3 upload and presigned URL generation
    s3_stub.add_response("put_object", {}, {
        "Bucket": BUCKET_NAME,
        "Key": f"pdfs/{pdf_filename}",
        "Body": pdf_data,
        "ContentType": "application/pdf"
    })

    s3_stub.add_response("put_object", {}, {
        "Bucket": BUCKET_NAME,
        "Key": f"covers/{cover_filename}",
        "Body": cover_data,
        "ContentType": "image/png"
    })

    # Mock presigned URLs
    s3_stub.add_response("get_object", {}, {
        "Bucket": BUCKET_NAME,
        "Key": f"pdfs/{pdf_filename}"
    })

    s3_stub.add_response("get_object", {}, {
        "Bucket": BUCKET_NAME,
        "Key": f"covers/{cover_filename}"
    })

    data = {
        "title": "Test Title",
        "author": "Test Author",
        "year": "2025",
        "category": "music"
    }
    files = {
        "pdf": (pdf_data, "test.pdf"),
        "cover": (cover_data, "cover.png")
    }

    response = client.post('/upload', data={**data, **files}, content_type='multipart/form-data')
    assert response.status_code == 200
    body = response.get_json()
    assert body["message"] == "Upload successful"
    assert "pdf_url" in body["data"]
    assert "cover_url" in body["data"]

def test_upload_missing_fields(client):
    response = client.post('/upload', data={}, content_type='multipart/form-data')
    assert response.status_code == 400
    assert "Missing required fields" in response.get_json()["message"]

def test_upload_invalid_category(client):
    data = {
        "title": "Test",
        "author": "Author",
        "year": "2025",
        "category": "invalid"
    }
    files = {
        "pdf": (io.BytesIO(b"PDF"), "test.pdf"),
        "cover": (io.BytesIO(b"IMG"), "test.png")
    }
    response = client.post('/upload', data={**data, **files}, content_type='multipart/form-data')
    assert response.status_code == 400
    assert "Invalid category" in response.get_json()["message"]

def test_get_resources_valid(client):
    # Ensure at least one dummy file exists
    os.makedirs(METADATA_FOLDER, exist_ok=True)
    test_path = os.path.join(METADATA_FOLDER, "music_dummy.json")
    with open(test_path, "w") as f:
        json.dump({
            "title": "Sample",
            "author": "Someone",
            "year": "2025",
            "pdf_url": "http://example.com/pdf",
            "cover_url": "http://example.com/cover"
        }, f)

    response = client.get("/resources/music")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_resources_invalid(client):
    response = client.get("/resources/invalidcategory")
    assert response.status_code == 400
    assert "Invalid category" in response.get_json()["message"]
