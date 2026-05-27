"""
Security regression tests for file uploads.

Tests file size limits and error message sanitization to prevent
information disclosure.
"""

from unittest.mock import PropertyMock, patch

import pytest
from httpx import AsyncClient

from app.config import get_settings

settings = get_settings()


@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file exceeding the size limit returns 413.
    """
    # Patch settings to a very small size for testing without high memory usage.
    # We patch the property on the class since it's a read-only property on the instance.
    with patch("app.config.Settings.max_upload_size_bytes", new_callable=PropertyMock) as mock_size:
        mock_size.return_value = 1024
        # Create a dummy file that is "large" (relative to our patched limit)
        content = b"a" * 2048
        files = {"file": ("large_file.pdf", content, "application/pdf")}

        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files,
        )

        assert response.status_code == 413
        data = response.json()
        assert "exceeds the maximum upload size" in data["message"]
        assert "FileTooLargeError" == data["error"]


@pytest.mark.asyncio
async def test_upload_error_sanitization_save_failure(client: AsyncClient, auth_headers: dict):
    """
    Test that internal file saving errors are sanitized and don't leak details.
    """
    files = {"file": ("test.pdf", b"pdf content", "application/pdf")}

    # Mock shutil.copyfileobj to raise an internal exception with sensitive info
    with patch("shutil.copyfileobj", side_effect=Exception("/etc/shadow access denied")):
        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files,
        )

    assert response.status_code == 500
    data = response.json()
    # Should show generic message, not the internal path or error
    assert "An error occurred while saving the file" in data["detail"]
    assert "/etc/shadow" not in data["detail"]


@pytest.mark.asyncio
async def test_upload_error_sanitization_processing_failure(client: AsyncClient, auth_headers: dict):
    """
    Test that internal processing errors are sanitized in the document record.
    """
    files = {"file": ("test.pdf", b"pdf content", "application/pdf")}

    # Mock process_uploaded_file to raise an internal exception
    with patch(
        "app.api.documents.process_uploaded_file",
        side_effect=Exception("Database connection timeout at 192.168.1.50")
    ):
        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files,
        )

    assert response.status_code == 201
    data = response.json()
    doc = data["document"]
    assert doc["status"] == "failed"
    # The error message in the response should be sanitized
    assert "Error during text extraction and processing" in doc["error_message"]
    assert "192.168.1.50" not in doc["error_message"]
