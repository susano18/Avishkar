"""
Tests for file size validation and hardened error handling.
"""

import pytest
from httpx import AsyncClient
from app.config import get_settings

settings = get_settings()

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """Test that uploading a file larger than the limit returns 413."""
    # Create a dummy file that exceeds the limit
    large_content = b"x" * (settings.max_upload_size_bytes + 1024)
    files = {"file": ("large.pdf", large_content, "application/pdf")}

    response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

    assert response.status_code == 413
    data = response.json()
    assert "exceeds the maximum upload size" in data["message"]
    assert data["error"] == "FileTooLargeError"

@pytest.mark.asyncio
async def test_upload_file_valid_size(client: AsyncClient, auth_headers: dict):
    """Test that a small file passes the size check."""
    small_content = b"x" * 1024
    files = {"file": ("small.txt", small_content, "text/plain")}

    response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

    # It might fail later due to missing LLM key or something, but 413 means it failed size check
    assert response.status_code != 413
