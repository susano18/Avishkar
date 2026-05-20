"""
Security regression tests for document uploads.

Verifies file size limits and error message sanitization.
"""

import pytest
import shutil
from httpx import AsyncClient
from app.config import get_settings

settings = get_settings()

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file larger than the limit returns 413.
    Matches Sentinel requirement: 4. Always validate input length and file size.
    """
    # Create a dummy file that is "large" by just exceeding the limit
    # We mock the size if possible, or just send a slightly larger buffer if memory permits
    # For testing, we can temporarily lower the limit in settings if needed,
    # but here we'll just try to send a bit more than the default 50MB if it's not too much,
    # or better, monkeypatch the settings.

    content = b"a" * 100
    # Monkeypatch max_upload_size_bytes to be very small for this test
    from app.api import documents
    original_max = documents.settings.MAX_UPLOAD_SIZE_MB
    documents.settings.MAX_UPLOAD_SIZE_MB = 0 # 0 MB limit

    try:
        files = {"file": ("large.pdf", content, "application/pdf")}
        response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

        assert response.status_code == 413
        data = response.json()
        assert "error" in data
        assert "FileTooLargeError" in data["error"]
    finally:
        documents.settings.MAX_UPLOAD_SIZE_MB = original_max

@pytest.mark.asyncio
async def test_upload_error_sanitization(client: AsyncClient, auth_headers: dict, monkeypatch):
    """
    Test that internal error details are not leaked on upload failure.
    Matches Sentinel requirement: Fail securely - errors should not expose sensitive data.
    """

    # Mock shutil.copyfileobj to raise an internal exception with sensitive info
    def mock_copyfileobj(*args, **kwargs):
        raise OSError("Sensitive info: Connection to /var/lib/secret failed")

    monkeypatch.setattr(shutil, "copyfileobj", mock_copyfileobj)

    files = {"file": ("test.pdf", b"some content", "application/pdf")}
    response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

    assert response.status_code == 500
    data = response.json()

    # FastAPI/Starlette default HTTPException response for status_code 500
    # in the way we called it (detail="...") will have "detail" key if not handled by our custom handler
    # but wait, app/main.py has exception_handler(Exception) which returns "message"
    # Actually, HTTPException is NOT handled by exception_handler(Exception), it has its own default handler
    # unless we override it.

    # In app/api/documents.py we raise HTTPException(status_code=500, detail="...")
    # This should be handled by FastAPI's default HTTPException handler, which uses "detail" key.

    msg_key = "detail" if "detail" in data else "message"

    # Should not contain the internal error message
    assert "Sensitive info" not in data[msg_key]
    assert "/var/lib/secret" not in data[msg_key]
    # Should contain a generic message
    assert "An error occurred while saving the file" in data[msg_key]
