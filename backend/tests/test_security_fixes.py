"""
Security tests for the CodeLens application.
"""

import pytest
from unittest.mock import patch
from httpx import AsyncClient
from app.config import get_settings

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file larger than MAX_UPLOAD_SIZE_MB returns 413.
    """
    # Mock settings to have a very small limit for testing
    with patch("app.api.documents.settings") as mock_settings:
        mock_settings.max_upload_size_bytes = 100  # 100 bytes
        mock_settings.MAX_UPLOAD_SIZE_MB = 0.000095 # roughly 100 bytes

        # Create a "large" file (150 bytes)
        file_content = b"a" * 150
        files = {"file": ("large.txt", file_content, "text/plain")}

        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

        assert response.status_code == 413
        assert "exceeds the maximum upload size" in response.json()["message"]
