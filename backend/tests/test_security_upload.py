"""
Security tests for file uploads.
"""

import pytest
from httpx import AsyncClient
from app.config import get_settings

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict, monkeypatch):
    """
    Test that uploading a file exceeding the maximum size limit
    is rejected with a 413 Content Too Large (Request Entity Too Large).
    """
    settings = get_settings()

    # Mock settings to have a very small limit (1KB)
    monkeypatch.setattr(settings, "MAX_UPLOAD_SIZE_MB", 0.001)
    # 0.001 MB = 1048.576 bytes

    # Create a "large" file (2KB)
    large_content = b"a" * 2048
    files = {"file": ("large.pdf", large_content, "application/pdf")}

    response = await client.post(
        "/api/v1/documents/upload",
        headers=auth_headers,
        files=files
    )

    assert response.status_code == 413
    assert "exceeds the maximum upload size" in response.json()["message"]

@pytest.mark.asyncio
async def test_security_headers_present(client: AsyncClient):
    """
    Test that security headers are present in responses.
    """
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
