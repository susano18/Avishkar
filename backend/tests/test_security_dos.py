import pytest
from httpx import AsyncClient
from unittest.mock import patch, MagicMock
from app.config import Settings

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file exceeding the size limit returns 413.
    """
    # Mock settings to have a tiny limit (e.g., 1 byte)
    mock_settings = MagicMock(spec=Settings)
    mock_settings.MAX_UPLOAD_SIZE_MB = 0 # 0 MB
    mock_settings.max_upload_size_bytes = 1 # 1 byte
    mock_settings.UPLOAD_DIR = "./test_uploads"
    mock_settings.upload_path = MagicMock()

    # Create a small file that is still larger than 1 byte
    files = {"file": ("test.txt", b"this is more than one byte", "text/plain")}

    # Import settings from app.api.documents to patch it there
    with patch("app.api.documents.settings", mock_settings):
        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

        assert response.status_code == 413
        assert "exceeds the maximum upload size" in response.json()["message"]
