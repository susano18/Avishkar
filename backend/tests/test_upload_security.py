"""
Security tests for file uploads.
"""

import pytest
from httpx import AsyncClient
from app.config import get_settings

settings = get_settings()

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file exceeding MAX_UPLOAD_SIZE_MB is rejected.
    """
    # Create a dummy large file (limit + 1 byte)
    max_size_bytes = settings.max_upload_size_bytes
    large_content = b"0" * (max_size_bytes + 1)

    files = {"file": ("large_file.pdf", large_content, "application/pdf")}

    response = await client.post(
        "/api/v1/documents/upload",
        headers=auth_headers,
        files=files
    )

    # Before the fix, it might be 201 or 500 depending on environment/implementation
    # After the fix, it should be 413
    assert response.status_code == 413
    assert "exceeds the maximum upload size" in response.json()["message"]
