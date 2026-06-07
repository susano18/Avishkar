"""
Security tests for file uploads.

Verifies that file size limits are enforced and that internal error
details are not leaked to the client.
"""

import pytest
from httpx import AsyncClient
from app.config import get_settings

settings = get_settings()

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file exceeding the maximum size is rejected.
    """
    # Create a dummy file that is "too large" by tricking the system or
    # actually creating a large buffer.
    # Since we want to test Sentinel's fix, we will simulate a large file.

    # We'll use a size slightly larger than MAX_UPLOAD_SIZE_MB
    large_content = b"0" * (settings.max_upload_size_bytes + 1024)
    files = {"file": ("large_file.txt", large_content, "text/plain")}

    response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

    # Currently, this might fail or return 500 because the fix isn't applied yet.
    # We expect 413 after the fix.
    assert response.status_code == 413
    assert "exceeds the maximum upload size" in response.json()["message"]

@pytest.mark.asyncio
async def test_upload_error_leakage(client: AsyncClient, auth_headers: dict, monkeypatch):
    """
    Test that internal processing errors do not leak system details.
    """
    # Mock a service to raise an exception with sensitive info
    def mock_process_uploaded_file(*args, **kwargs):
        raise RuntimeError("Sensitive error: failed to connect to DB at 10.0.0.5:5432")

    monkeypatch.setattr("app.api.documents.process_uploaded_file", mock_process_uploaded_file)

    files = {"file": ("test.txt", b"some content", "text/plain")}
    response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

    # We expect 201 because the document is created even if processing fails
    assert response.status_code == 201
    data = response.json()

    # Ensure the sensitive detail is NOT in the message or document error_message
    assert "10.0.0.5" not in data["message"]
    assert "Sensitive error" not in data["message"]
    assert "10.0.0.5" not in data["document"]["error_message"]
    assert "Sensitive error" not in data["document"]["error_message"]

    # It should be a generic message
    assert "An error occurred during file processing" in data["message"]
    assert "internal error occurred" in data["document"]["error_message"]
