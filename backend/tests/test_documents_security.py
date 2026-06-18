"""
Security tests for Document API.
"""

import pytest
from httpx import AsyncClient
from app.config import get_settings

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict, monkeypatch):
    """
    Test that uploading a file exceeding MAX_UPLOAD_SIZE_MB returns 413.
    """
    # Force a very small limit
    monkeypatch.setattr("app.api.documents.settings.MAX_UPLOAD_SIZE_MB", 0) # 0 MB limit

    # Try to upload a small file (which is > 0 MB)
    files = {"file": ("test.txt", b"some content", "text/plain")}
    response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

    # This SHOULD fail with 413 after the fix
    assert response.status_code == 413
    assert response.json()["error"] == "FileTooLargeError"
