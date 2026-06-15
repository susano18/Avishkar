"""
Security tests for document uploads.
"""

import pytest
from httpx import AsyncClient
from unittest.mock import patch
from app.config import Settings

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file exceeding MAX_UPLOAD_SIZE_MB is rejected with 413.
    """
    # Override settings to use a small limit for testing
    test_settings = Settings(MAX_UPLOAD_SIZE_MB=1)

    with patch("app.api.documents.settings", test_settings):
        # Create 1.1 MB of dummy data
        file_content = b"0" * (1 * 1024 * 1024 + 1024)
        files = {"file": ("large_file.pdf", file_content, "application/pdf")}

        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

        # Currently this is expected to FAIL (return 201) because the check is missing
        assert response.status_code == 413
        assert "exceeds the maximum upload size" in response.json()["message"]

@pytest.mark.asyncio
async def test_upload_info_leakage_on_failure(client: AsyncClient, auth_headers: dict):
    """
    Test that internal error details are not leaked when file saving fails.
    """
    with patch("app.api.documents.open", side_effect=Exception("Sensitive system error: /etc/passwd not found")):
        files = {"file": ("test.txt", b"some content", "text/plain")}

        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

        assert response.status_code == 500
        data = response.json()
        # The message should be generic, not containing "Sensitive system error"
        # Check in both 'message' and 'detail' (FastAPI default)
        error_msg = data.get("message") or data.get("detail", "")
        assert "Sensitive system error" not in error_msg
        assert "An error occurred while saving the file" in error_msg
