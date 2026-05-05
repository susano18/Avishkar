"""
Security tests for document upload.

Verifies that file size limits are enforced to prevent Denial of Service (DoS)
attacks by filling up server storage.
"""

import pytest
from httpx import AsyncClient
from unittest.mock import patch

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file exceeding MAX_UPLOAD_SIZE_MB is rejected.
    """
    # Mock settings to have a very small limit (1 KB)
    with patch("app.api.documents.settings") as mock_settings:
        mock_settings.MAX_UPLOAD_SIZE_MB = 0.001  # ~1 KB
        mock_settings.max_upload_size_bytes = 1024

        # Create a "large" file in memory (2 KB)
        large_content = b"a" * 2048
        files = {"file": ("large.txt", large_content, "text/plain")}

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
    # Mock settings to have a small limit (10 KB)
    with patch("app.api.documents.settings") as mock_settings:
        mock_settings.MAX_UPLOAD_SIZE_MB = 0.01
        mock_settings.max_upload_size_bytes = 10240

        # Create a small file (1 KB)
        small_content = b"a" * 1024
        files = {"file": ("small.txt", small_content, "text/plain")}

        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

        # It shouldn't be 413
        assert response.status_code != 413
