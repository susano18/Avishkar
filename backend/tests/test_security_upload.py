"""
Security tests for file uploads.
"""

import pytest
from httpx import AsyncClient
from unittest.mock import patch, PropertyMock

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file exceeding the size limit returns 413.
    """
    # Mock settings.max_upload_size_bytes property
    with patch("app.api.documents.settings.__class__.max_upload_size_bytes", new_callable=PropertyMock) as mock_size:
        mock_size.return_value = 1  # 1 byte
        files = {"file": ("test.txt", b"too much data", "text/plain")}
        response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

        assert response.status_code == 413
        data = response.json()
        assert "exceeds the maximum upload size" in data["message"]
