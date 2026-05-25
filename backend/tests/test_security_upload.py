"""
Security regression tests for document uploads.

Verifies protection against Denial of Service (large files) and
Information Leakage (sensitive error messages).
"""

import pytest
from httpx import AsyncClient
from unittest.mock import patch, MagicMock
from app.config import get_settings

settings = get_settings()

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file larger than the limit is rejected with 413.
    """
    # Create a small file but mock its size to be over the limit
    files = {"file": ("large.pdf", b"fake content", "application/pdf")}

    # We need to mock the size attribute of the UploadFile object that FastAPI creates.
    # Since we can't easily reach into FastAPI's internals here, we'll implement the check
    # and then verify it with a file that actually exceeds a small threshold if we were to
    # override settings, OR we just verify the 413 response if we can trigger it.

    # For testing, let's assume we implement the check using file.size.
    # In FastAPI TestClient/httpx, we can't easily mock the server-side UploadFile.size
    # without patching the endpoint or the settings.

    with patch("app.api.documents.settings") as mock_settings:
        mock_settings.max_upload_size_bytes = 10 # Very small limit
        mock_settings.MAX_UPLOAD_SIZE_MB = 0

        # This file is 12 bytes, which is > 10 bytes
        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files={"file": ("test.pdf", b"123456789012", "application/pdf")}
        )

        assert response.status_code == 413
        assert "exceeds the maximum upload size" in response.json()["message"]

@pytest.mark.asyncio
async def test_upload_error_sanitization(client: AsyncClient, auth_headers: dict):
    """
    Test that internal error details are not leaked in the response.
    """
    # Mock shutil.copyfileobj to raise an exception with sensitive info
    with patch("shutil.copyfileobj", side_effect=Exception("/etc/passwd access denied or some/internal/path")):
        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files={"file": ("test.pdf", b"some content", "application/pdf")}
        )

        assert response.status_code == 500
        data = response.json()
        # Should not contain the internal path or specific error details
        assert "/etc/passwd" not in data["detail"]
        assert "some/internal/path" not in data["detail"]
        # Should have a generic error message
        assert "Failed to save file" in data["detail"]
