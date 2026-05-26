"""
Security regression tests for document uploads.

Verifies file size limits and error message sanitization.
"""

import pytest
from httpx import AsyncClient
from unittest.mock import patch


@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """Test that uploading a file exceeding the size limit returns 413."""
    # Create a dummy file
    files = {"file": ("large_file.pdf", b"too much data", "application/pdf")}

    # Patch the settings to a very low value so that any upload triggers the limit.
    # This avoids complex mocking of UploadFile.size.
    with patch("app.api.documents.settings") as mock_settings:
        mock_settings.max_upload_size_bytes = 10 # 10 bytes
        mock_settings.MAX_UPLOAD_SIZE_MB = 0

        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

    assert response.status_code == 413
    assert "exceeds the maximum upload size" in response.json()["message"]


@pytest.mark.asyncio
async def test_upload_error_sanitization_save_failure(client: AsyncClient, auth_headers: dict):
    """Test that file saving failures do not leak detailed exception info."""
    files = {"file": ("test.pdf", b"fake pdf content", "application/pdf")}

    # Mock shutil.copyfileobj to raise an exception with sensitive info
    with patch("shutil.copyfileobj", side_effect=Exception("Sensitive DB/Path info here")):
        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

    assert response.status_code == 500
    data = response.json()
    # Check that the generic message is returned, not the specific exception detail
    assert data["detail"] == "An error occurred while saving the file. Please try again."
    assert "Sensitive" not in data["detail"]


@pytest.mark.asyncio
async def test_upload_error_sanitization_processing_failure(client: AsyncClient, auth_headers: dict):
    """Test that processing failures sanitize error messages in the document record."""
    files = {"file": ("test.pdf", b"fake pdf content", "application/pdf")}

    # Mock process_uploaded_file to raise an exception
    with patch("app.api.documents.process_uploaded_file", side_effect=Exception("Internal processing error details")):
        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

    assert response.status_code == 201
    data = response.json()
    # The document record should have a generic error message
    assert data["document"]["error_message"] == "Failed to extract text from file."
    assert "Internal processing error" not in data["document"]["error_message"]
