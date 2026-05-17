"""
Security tests for file uploads.
"""

import pytest
from httpx import AsyncClient
from app.config import get_settings

settings = get_settings()


@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """Test that uploading a file exceeding the size limit returns 413."""
    # Create a dummy large "file" by using a large byte string
    # We exceed MAX_UPLOAD_SIZE_MB (default 50MB)
    large_content = b"0" * (settings.max_upload_size_bytes + 1024)
    files = {"file": ("large_file.pdf", large_content, "application/pdf")}

    response = await client.post(
        "/api/v1/documents/upload",
        headers=auth_headers,
        files=files
    )

    assert response.status_code == 413
    data = response.json()
    assert data["error"] == "FileTooLargeError"
    assert "exceeds the maximum upload size" in data["message"]


@pytest.mark.asyncio
async def test_upload_file_within_limit(
    client: AsyncClient, auth_headers: dict
):
    """
    Test that uploading a file within the size limit proceeds
    (even if it fails later due to missing mock).
    """
    # Small file should pass the size check
    small_content = b"Small PDF content"
    files = {"file": ("small_file.pdf", small_content, "application/pdf")}

    response = await client.post(
        "/api/v1/documents/upload",
        headers=auth_headers,
        files=files
    )

    # It might fail with 500 or 422 if the file is not a real PDF,
    # but it should NOT be 413.
    assert response.status_code != 413
