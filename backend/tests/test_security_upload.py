import pytest
from unittest.mock import patch, MagicMock
from httpx import AsyncClient
from app.config import get_settings

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """Test that uploading a file exceeding the size limit returns 413."""
    settings = get_settings()
    # Mocking settings.max_upload_size_bytes to be small for the test
    with patch("app.api.documents.settings") as mock_settings:
        mock_settings.max_upload_size_bytes = 100 # 100 bytes

        content = b"a" * 200
        files = {"file": ("large.txt", content, "text/plain")}

        response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

        assert response.status_code == 413
        assert "exceeds the maximum upload size" in response.json()["message"]

@pytest.mark.asyncio
async def test_upload_file_save_failure_leaks_no_info(client: AsyncClient, auth_headers: dict):
    """Test that file saving failure returns a generic error message."""
    content = b"some content"
    files = {"file": ("test.txt", content, "text/plain")}

    # Mock shutil.copyfileobj to raise an exception with sensitive info
    with patch("app.api.documents.shutil.copyfileobj", side_effect=Exception("Internal path: /secret/path/to/fail")):
        response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

        assert response.status_code == 500
        data = response.json()
        # It should NOT contain the specific error message
        assert "Internal path" not in data["detail"]
        assert "secret" not in data["detail"]
        # It should be a generic message
        assert data["detail"] == "Failed to save file."
