import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.config import get_settings

settings = get_settings()

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """Test uploading a file that exceeds the size limit."""
    # Create a dummy "large" file in memory
    large_content = b"a" * (settings.max_upload_size_bytes + 1024)
    files = {"file": ("large.txt", large_content, "text/plain")}

    response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

    # It should fail with 413
    assert response.status_code == 413
    assert "exceeds the maximum upload size" in response.json()["message"]

@pytest.mark.asyncio
async def test_upload_file_error_sanitization(client: AsyncClient, auth_headers: dict, monkeypatch):
    """Test that file save errors are sanitized in the response."""
    # Mock shutil.copyfileobj to raise an exception with sensitive info
    def mock_copyfileobj(*args, **kwargs):
        raise OSError("Secret path /root/top_secret/data failed")

    import shutil
    monkeypatch.setattr(shutil, "copyfileobj", mock_copyfileobj)

    files = {"file": ("test.txt", b"some content", "text/plain")}
    response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

    assert response.status_code == 500
    # Should NOT contain the secret path
    assert "/root/top_secret" not in response.json()["detail"]
    assert "Failed to save" in response.json()["detail"]
