"""
Security tests for file uploads.
Verifies that file size limits are enforced.
"""

import pytest
from httpx import AsyncClient
from unittest.mock import patch
from app.config import Settings

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file larger than MAX_UPLOAD_SIZE_MB returns 413.
    """
    # Mock settings to have a very small limit (1KB)
    mock_settings = Settings()
    mock_settings.MAX_UPLOAD_SIZE_MB = 0.001 # approx 1KB

    # Patch settings in BOTH modules because it's imported in documents.py
    with patch("app.api.documents.settings", mock_settings):
        # Create a "large" payload (2KB)
        content = b"a" * 2048
        files = {"file": ("large.txt", content, "text/plain")}

        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

        assert response.status_code == 413
        assert "exceeds the maximum upload size" in response.json()["message"]

@pytest.mark.asyncio
async def test_upload_file_within_limit(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file within the limit still works.
    """
    # Mock settings to have a 1MB limit
    mock_settings = Settings()
    mock_settings.MAX_UPLOAD_SIZE_MB = 1

    with patch("app.api.documents.settings", mock_settings):
        # Small content
        content = b"Hello, world!"
        files = {"file": ("small.txt", content, "text/plain")}

        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

        # Should NOT be 413. It might fail for other reasons (like no LLM API key),
        # but here we just want to see it passed the size check.
        assert response.status_code != 413
