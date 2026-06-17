"""
Security regression tests for document handling.

Verifies that file size limits are enforced and other document-related
security controls are functioning correctly.
"""

import pytest
from httpx import AsyncClient
from app.config import get_settings

settings = get_settings()

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file exceeding MAX_UPLOAD_SIZE_MB is rejected.

    This is a regression test for the DoS vulnerability via large file uploads.
    """
    # Create a dummy file that is slightly larger than the limit
    # We use a seekable stream mock via bytes in the multipart request
    limit_bytes = settings.max_upload_size_bytes
    large_content = b"0" * (limit_bytes + 1024)

    files = {
        "file": ("large_document.pdf", large_content, "application/pdf")
    }

    response = await client.post(
        "/api/v1/documents/upload",
        headers=auth_headers,
        files=files
    )

    assert response.status_code == 413
    data = response.json()
    assert "exceeds the maximum upload size" in data["message"]
    assert data["error"] == "FileTooLargeError"

@pytest.mark.asyncio
async def test_upload_file_within_limit(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file within the limit is accepted.
    """
    small_content = b"Small PDF content"
    files = {
        "file": ("small_document.pdf", small_content, "application/pdf")
    }

    # We mock process_uploaded_file to avoid actual extraction logic in this security test
    # if necessary, but here we just check if it passes the size check.
    # Since the full app is running, it will try to extract, which might fail
    # but the status code should NOT be 413.

    response = await client.post(
        "/api/v1/documents/upload",
        headers=auth_headers,
        files=files
    )

    assert response.status_code != 413
