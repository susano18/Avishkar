"""
Security tests for document uploads.

Tests file size limits and other security-related upload constraints.
"""

import pytest
from unittest.mock import patch, PropertyMock
from httpx import AsyncClient

from app.config import Settings
from app.models.user import User


@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file exceeding the maximum size limit
    returns a 413 Request Entity Too Large error.
    """
    # Patch the max_upload_size_bytes property at the class level
    # to a very small value for testing.
    with patch.object(Settings, "max_upload_size_bytes", new_callable=PropertyMock) as mock_limit:
        mock_limit.return_value = 100  # 100 bytes limit

        # Create a small file that exceeds the 100 bytes limit
        content = b"x" * 200
        files = {"file": ("large_file.pdf", content, "application/pdf")}

        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files,
        )

        assert response.status_code == 413
        data = response.json()
        assert data["error"] == "FileTooLargeError"
        assert "exceeds the maximum upload size" in data["message"]
