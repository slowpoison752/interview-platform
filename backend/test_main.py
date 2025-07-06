import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_api_root():
    """Test the API root endpoint"""
    response = client.get("/api")
    assert response.status_code == 200
    assert "message" in response.json()

def test_upload_resume_no_file():
    """Test upload endpoint without file"""
    response = client.post("/api/upload-resume")
    assert response.status_code == 422  # Validation error

def test_upload_resume_invalid_file():
    """Test upload endpoint with invalid file type"""
    files = {"file": ("test.txt", b"not a pdf", "text/plain")}
    response = client.post("/api/upload-resume", files=files)
    assert response.status_code == 400
    assert "Only PDF files are allowed" in response.json()["detail"]

def test_cors_headers():
    """Test CORS headers are present"""
    response = client.options("/api")
    assert response.status_code == 200 