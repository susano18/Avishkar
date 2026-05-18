import pytest
from httpx import AsyncClient
from unittest.mock import patch, MagicMock
from app.config import get_settings

settings = get_settings()

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """Test that uploading a file exceeding the size limit returns 413."""
    # Create a dummy file that claims to be large
    # FastAPI's UploadFile has a 'size' attribute in newer versions,
    # but we can also just send a large body if the server reads it.
    # However, the server doesn't check it yet.

    files = {"file": ("large_file.txt", b"a" * (settings.max_upload_size_bytes + 1), "text/plain")}

    response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

    # Currently this will likely succeed or fail with something other than 413
    # because there is no check.
    assert response.status_code == 413
    assert "exceeds the maximum upload size" in response.json()["message"]

@pytest.mark.asyncio
async def test_upload_save_failure_does_not_leak_details(client: AsyncClient, auth_headers: dict):
    """Test that file save failure does not leak internal error details."""
    files = {"file": ("test.txt", b"some content", "text/plain")}

    # Mock 'open' to raise an exception with sensitive info
    with patch("app.api.documents.open", side_effect=IOError("Permission denied: /root/secret")):
        response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

    assert response.status_code == 500
    data = response.json()
    # It should not contain the internal error message
    assert "Permission denied" not in data["detail"]
    assert "/root/secret" not in data["detail"]
    assert data["detail"] == "An error occurred while saving the file."
