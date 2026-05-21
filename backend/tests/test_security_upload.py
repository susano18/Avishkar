import pytest
from httpx import AsyncClient
from app.config import get_settings

settings = get_settings()

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file larger than MAX_UPLOAD_SIZE_MB returns 413.
    """
    # Create a dummy file that exceeds the limit
    # settings.MAX_UPLOAD_SIZE_MB is 50 by default
    oversized_content = b"0" * (settings.max_upload_size_bytes + 1)
    files = {"file": ("large.txt", oversized_content, "text/plain")}

    response = await client.post(
        "/api/v1/documents/upload",
        headers=auth_headers,
        files=files
    )

    assert response.status_code == 413
    assert "exceeds the maximum upload size" in response.json()["message"]

@pytest.mark.asyncio
async def test_upload_error_sanitization(client: AsyncClient, auth_headers: dict, monkeypatch):
    """
    Test that internal error details are not leaked in the response when a save failure occurs.
    """
    # Mock shutil.copyfileobj to raise an exception with sensitive info
    import shutil
    def mock_copyfileobj(*args, **kwargs):
        raise Exception("Sensitive DB connection string: postgres://user:password@localhost:5432/db")

    monkeypatch.setattr(shutil, "copyfileobj", mock_copyfileobj)

    files = {"file": ("test.txt", b"some content", "text/plain")}

    response = await client.post(
        "/api/v1/documents/upload",
        headers=auth_headers,
        files=files
    )

    assert response.status_code == 500
    # Check that the generic message is returned
    assert response.json()["detail"] == "An error occurred while saving the file."
    # Check that sensitive info is NOT in the response
    assert "postgres://" not in response.text
    assert "password" not in response.text
