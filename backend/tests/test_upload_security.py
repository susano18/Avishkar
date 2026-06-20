"""
Security tests for file uploads.

Verifies that file size limits are enforced and that the server
does not leak sensitive information in error messages.
"""

import pytest
from httpx import AsyncClient

from app.config import get_settings


@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict, monkeypatch):
    """
    Test that uploading a file exceeding MAX_UPLOAD_SIZE_MB returns 413.
    """
    settings = get_settings()
    # Set a small limit for testing
    monkeypatch.setattr(settings, "MAX_UPLOAD_SIZE_MB", 1)

    # Create a 2MB dummy file
    content = b"0" * (2 * 1024 * 1024)
    files = {"file": ("too_large.pdf", content, "application/pdf")}

    response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

    # Should be 413 Request Entity Too Large (or Content Too Large)
    assert response.status_code == 413
    assert "exceeds the maximum upload size" in response.json()["message"]


@pytest.mark.asyncio
async def test_upload_error_does_not_leak_details(client: AsyncClient, auth_headers: dict, monkeypatch):
    """
    Test that internal server errors during upload do not leak stack traces or system info.
    """
    # Mock a failure during file processing or saving
    from app.api.documents import ensure_upload_dir
    def mock_ensure_upload_dir():
        raise RuntimeError("Sensitive system info: /etc/passwd or database_url secret")

    monkeypatch.setattr("app.api.documents.ensure_upload_dir", mock_ensure_upload_dir)

    files = {"file": ("test.pdf", b"fake pdf content", "application/pdf")}
    response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

    assert response.status_code == 500
    data = response.json()
    # We want a generic error message, not the "Sensitive system info" one
    assert "Sensitive system info" not in data["detail"]
    assert data["detail"] == "An unexpected error occurred while processing the file."
