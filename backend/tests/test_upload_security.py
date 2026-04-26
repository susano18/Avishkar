"""
Security tests for file uploads.

Verifies that file size limits are enforced to prevent Denial of Service (DoS)
attacks via oversized file uploads.
"""

import pytest
from unittest.mock import patch
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file exceeding MAX_UPLOAD_SIZE_MB returns 413.

    We mock settings.max_upload_size_bytes to a small value (1KB) and
    upload a slightly larger file to avoid large memory allocations.
    """
    # Mock settings to 1KB limit
    with patch("app.api.documents.settings") as mock_settings:
        mock_settings.max_upload_size_bytes = 1024
        mock_settings.MAX_UPLOAD_SIZE_MB = 0.001 # 1KB

        # 2KB of dummy data
        content = b"0" * 2048
        files = {"file": ("test.pdf", content, "application/pdf")}

        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

        assert response.status_code == 413
        data = response.json()
        assert "exceeds the maximum upload size" in data["message"]
        assert data["error"] == "FileTooLargeError"
