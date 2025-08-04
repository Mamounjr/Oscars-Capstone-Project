import os
import io
import json
import uuid
import pytest
from app import app, s3, METADATA_FOLDER
from botocore.stub import Stubber
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

@pytest.fixture
def s3_stub():
    with Stubber(s3) as stubber:
        yield stubber

def test_upload_success(client):
    pdf_data = io.BytesIO(b"%PDF-1.4 test pdf content")
    cover_data = io.BytesIO(b"\x89PNG\r\n\x1a\n test image content")

    # Set fixed UUID for predictability
    fixed_uuid = uuid.UUID("12345678-1234-5678-1234-567812345678")

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

    with patch("app.uuid.uuid4", return_value=fixed_uuid), \
         patch("app.s3.upload_fileobj") as mock_upload, \
         patch("app.s3.generate_presigned_url", return_value="https://fake-url.com/fake.pdf"):

        response = client.post('/upload', data={**data, **files}, content_type='multipart/form-data')

        print("RESPONSE STATUS:", response.status_code)
        print("RESPONSE BODY:", response.data.decode())

        assert response.status_code == 200
        body = response.get_json()
        assert body["message"] == "Upload successful"
        assert "pdf_url" in body["data"]
        assert "cover_url" in body["data"]
        assert mock_upload.call_count == 2

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
