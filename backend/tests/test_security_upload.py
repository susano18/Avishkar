"""
Security tests for document uploads.
"""

import pytest
from httpx import AsyncClient
from unittest.mock import patch, PropertyMock

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file exceeding MAX_UPLOAD_SIZE_MB returns 413.
    """
    # Use class-level patch for pydantic-settings
    with patch("app.config.Settings.max_upload_size_bytes", new_callable=PropertyMock) as mock_limit:
        mock_limit.return_value = 10 # 10 bytes limit

        content = b"this is more than 10 bytes"
        files = {"file": ("test.pdf", content, "application/pdf")}

        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

        assert response.status_code == 413
        # CodeLensBaseError uses "message"
        assert "exceeds the maximum upload size" in response.json()["message"]

@pytest.mark.asyncio
async def test_upload_file_save_failure_leaks_no_info(client: AsyncClient, auth_headers: dict):
    """
    Test that internal file saving failures do not leak details in the response.
    """
    # Mock shutil.copyfileobj to raise an exception with sensitive info
    with patch("shutil.copyfileobj", side_effect=Exception("Sensitive OS error: /etc/passwd path failed")):
        content = b"fake pdf content"
        files = {"file": ("test.pdf", content, "application/pdf")}

        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

        assert response.status_code == 500
        data = response.json()
        # HTTPException uses "detail"
        assert data["detail"] == "An error occurred while saving the file to storage."
        # Ensure the sensitive part of the exception is NOT in the response
        assert "Sensitive OS error" not in str(data)
        assert "/etc/passwd" not in str(data)
