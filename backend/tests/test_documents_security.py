import pytest
from httpx import AsyncClient
from app.config import get_settings

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict, monkeypatch):
    """Test that uploading a file larger than MAX_UPLOAD_SIZE_MB fails."""
    settings = get_settings()

    # Set a small limit for testing
    monkeypatch.setattr(settings, "MAX_UPLOAD_SIZE_MB", 1)

    # Create a dummy file content larger than 1MB
    # 1.1 MB of data
    large_content = b"0" * (1024 * 1024 + 100 * 1024)

    files = {"file": ("large_test.txt", large_content, "text/plain")}

    response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

    # Should fail with 413
    assert response.status_code == 413
    assert "exceeds the maximum upload size" in response.json()["message"]
