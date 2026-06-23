"""
Security regression tests for document upload.
"""

import pytest
from httpx import AsyncClient
from app.config import get_settings

settings = get_settings()

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file larger than MAX_UPLOAD_SIZE_MB returns 413.
    """
    # Create a dummy content that is slightly larger than the limit
    # To avoid huge memory usage in tests, we can temporarily monkeypatch the settings
    # or just use a smaller limit if we were able to.
    # Since we want to test the actual implementation, let's use a large-ish buffer if we must,
    # but a better way is to mock the settings.

    # However, let's just try to upload something and see it PASSING (incorrectly) first.
    # Actually, I'll just use a 1MB file and pretend the limit is 0.5MB for the sake of the test if I can.

    # For now, let's use a small enough large file, say 1MB, and I'll temporarily
    # set the limit to 0 in the code to verify the check works,
    # OR I can just use a 51MB dummy file.

    limit_mb = settings.MAX_UPLOAD_SIZE_MB
    large_content = b"0" * (limit_mb * 1024 * 1024 + 1024) # limit + 1KB

    files = {"file": ("large_file.pdf", large_content, "application/pdf")}

    response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

    # Currently it should NOT be 413 because the check is missing.
    # It might be 500 because it tries to process a dummy PDF, but it won't be 413.
    assert response.status_code == 413
    assert "exceeds the maximum upload size" in response.json()["message"]
