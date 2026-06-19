import pytest
from httpx import AsyncClient
from app.config import get_settings

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict, monkeypatch):
    """
    Test that uploading a file exceeding the size limit returns 413 Content Too Large.
    """
    # Get the actual settings instance
    settings = get_settings()

    # Temporarily reduce the limit to 1MB for the test
    monkeypatch.setattr(settings, "MAX_UPLOAD_SIZE_MB", 1)

    # Create a file content larger than 1MB (1MB + 1KB)
    large_content = b"0" * (1 * 1024 * 1024 + 1024)
    files = {"file": ("large_test.pdf", large_content, "application/pdf")}

    response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

    # Verify that the server returns 413 Content Too Large (or Request Entity Too Large currently)
    # Once we update it, it should be 413.
    assert response.status_code == 413
    data = response.json()
    assert "exceeds the maximum upload size" in data["message"]
    assert data["error"] == "FileTooLargeError"
