import pytest
import io
from httpx import AsyncClient
from app.config import get_settings

settings = get_settings()

@pytest.mark.asyncio
async def test_upload_file_too_large_fails(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file exceeding MAX_UPLOAD_SIZE_MB returns 413.
    """
    # Create a dummy file slightly larger than the limit
    # settings.max_upload_size_bytes is 50MB by default
    content_size = settings.max_upload_size_bytes + 1024

    # Using a generator or a large bytes object might be memory intensive in tests,
    # but 51MB should be fine in this environment.
    large_content = b"0" * content_size

    files = {"file": ("large.txt", large_content, "text/plain")}

    response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

    # Before the fix, this will likely return 201 (if it doesn't crash on memory)
    # or it might fail because of other reasons.
    # Sentinel's goal is to ensure it returns 413.
    assert response.status_code == 413
    assert "exceeds the maximum upload size" in response.json()["message"]
