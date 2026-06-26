import pytest
from httpx import AsyncClient
from app.config import get_settings

settings = get_settings()

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file exceeding MAX_UPLOAD_SIZE_MB is rejected.
    """
    # Use a size slightly larger than the limit
    # The default limit is 50MB.
    # We'll use 50MB + 1 byte.
    large_size = settings.max_upload_size_bytes + 1
    content = b"a" * large_size

    files = {"file": ("large_file.txt", content, "text/plain")}

    response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

    # Assert that we get a 413 Content Too Large (formerly Request Entity Too Large)
    # The exception handler in main.py converts CodeLensBaseError to JSON
    assert response.status_code == 413
    data = response.json()
    assert data["error"] == "FileTooLargeError"
    assert f"exceeds the maximum upload size of {settings.MAX_UPLOAD_SIZE_MB} MB" in data["message"]
