import pytest
from httpx import AsyncClient
from unittest.mock import patch, MagicMock
from fastapi import status

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """Test that files exceeding the size limit are rejected with 413."""
    file_content = b"fake content"
    files = {"file": ("large.pdf", file_content, "application/pdf")}

    with patch("app.api.documents.settings") as mock_settings:
        # Set limit to 1 byte
        mock_settings.max_upload_size_bytes = 1
        mock_settings.MAX_UPLOAD_SIZE_MB = 0.000001

        response = await client.post("/api/v1/documents/upload", files=files, headers=auth_headers)

    assert response.status_code == status.HTTP_413_CONTENT_TOO_LARGE
    # The error response structure for CodeLensBaseError has 'message' field
    assert "exceeds the maximum upload size" in response.json()["message"]

@pytest.mark.asyncio
async def test_upload_file_save_failure_no_leak(client: AsyncClient, auth_headers: dict):
    """Test that internal storage errors do not leak details in the API response."""
    file_content = b"fake content"
    files = {"file": ("test.pdf", file_content, "application/pdf")}

    # Mock open() to raise an exception with sensitive info
    # Note: open is used in app.api.documents
    with patch("app.api.documents.open", side_effect=Exception("Sensitive system path /etc/passwd error")):
        response = await client.post("/api/v1/documents/upload", files=files, headers=auth_headers)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["detail"] == "Failed to save file. Internal storage error."
    assert "Sensitive" not in response.json()["detail"]
    assert "/etc/passwd" not in response.json()["detail"]
