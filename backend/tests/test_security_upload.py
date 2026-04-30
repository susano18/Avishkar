"""
Security tests for file uploads.
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
    # Create a small "large" file for testing
    content = b"a" * 1024  # 1 KB
    files = {"file": ("test.txt", content, "text/plain")}

    # Mock settings to have a 0 MB limit (or very small)
    with patch("app.api.documents.settings") as mock_settings:
        mock_settings.max_upload_size_bytes = 512 # 0.5 KB limit
        mock_settings.MAX_UPLOAD_SIZE_MB = 0 # for the error message

        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

    # Verify that the request is rejected with 413 Content Too Large
    assert response.status_code == 413
    assert "exceeds the maximum upload size" in response.json()["message"]
