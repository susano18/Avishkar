"""
Security tests for document uploads.
"""

import pytest
from httpx import AsyncClient
from app.config import get_settings

settings = get_settings()

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file exceeding MAX_UPLOAD_SIZE_MB is rejected.
    This ensures protection against DoS via resource exhaustion.
    """
    # Create a dummy file larger than the limit
    # MAX_UPLOAD_SIZE_MB is 50 by default in config.py
    limit_mb = settings.MAX_UPLOAD_SIZE_MB
    large_content = b"0" * (limit_mb * 1024 * 1024 + 1024)

    files = {"file": ("large.pdf", large_content, "application/pdf")}

    response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

    # It should return 413 Request Entity Too Large
    assert response.status_code == 413
    assert "exceeds the maximum upload size" in response.json()["message"]
