"""
Security test for file upload size limits.
"""

import pytest
from httpx import AsyncClient
from unittest.mock import patch

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file larger than the configured limit returns 413.
    """
    # Create a small "large" file (e.g., 10 bytes)
    content = b"a" * 10
    files = {"file": ("test.txt", content, "text/plain")}

    # Mock the settings object itself
    with patch("app.api.documents.settings") as mock_settings:
        mock_settings.max_upload_size_bytes = 5
        mock_settings.MAX_UPLOAD_SIZE_MB = 1

        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

    # This should fail with 413 if validation is implemented.
    assert response.status_code == 413
    assert "exceeds the maximum upload size" in response.json()["message"]
