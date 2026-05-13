"""
Security tests for Sentinel's fixes.
"""

import pytest
from httpx import AsyncClient
from app.config import get_settings

settings = get_settings()

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file exceeding the size limit returns 413.
    """
    # Create a dummy file that is "too large" by mocking the size
    # We'll use a small actual payload but mock the size property in the endpoint
    # Actually, we can just send a payload that is larger than the limit if we want to be realistic,
    # but for a unit test, we want to be fast.

    # Let's try sending a file and see if we can trigger the 413 by mocking the limit
    # Actually, the code checks file.size which is set by FastAPI/Starlette

    # We'll send a 100 byte file but set the limit to 50 bytes for this test
    # But settings is a singleton. I should patch it.

    # For now, let's just verify it works with the default limit if we can't easily patch
    # The default limit is 50MB.

    files = {"file": ("large.pdf", b"x" * (settings.max_upload_size_bytes + 1), "application/pdf")}

    response = await client.post(
        "/api/v1/documents/upload",
        headers=auth_headers,
        files=files
    )

    assert response.status_code == 413
    assert "exceeds the maximum upload size" in response.json()["message"]

@pytest.mark.asyncio
async def test_upload_file_within_limit(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file within the size limit is accepted (fails later on processing if mocked).
    """
    files = {"file": ("small.pdf", b"x" * 100, "application/pdf")}

    # This might still fail with 500 or 422 because it's not a real PDF,
    # but it shouldn't be a 413.
    response = await client.post(
        "/api/v1/documents/upload",
        headers=auth_headers,
        files=files
    )

    assert response.status_code != 413
