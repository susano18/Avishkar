import pytest
from httpx import AsyncClient
from unittest.mock import patch
from app.config import Settings

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file exceeding the MAX_UPLOAD_SIZE_MB limit returns 413.
    We mock the settings to have a small limit for this test.
    """
    # Mock settings to have a 1MB limit
    mock_settings = Settings(MAX_UPLOAD_SIZE_MB=1)

    with patch("app.api.documents.settings", mock_settings):
        # Create a "large" dummy file (2MB)
        large_content = b"0" * (2 * 1024 * 1024)
        files = {"file": ("large.txt", large_content, "text/plain")}

        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

        # Verify that the server rejects the oversized file with a 413 error
        assert response.status_code == 413
        assert "exceeds the maximum upload size" in response.json()["message"]
