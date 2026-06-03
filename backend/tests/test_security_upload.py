import pytest
from httpx import AsyncClient
from unittest.mock import patch, PropertyMock
from fastapi import UploadFile

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers):
    # Mock settings.max_upload_size_bytes to be 0
    # We need to patch the class property because it's a @property on the instance
    with patch("app.config.Settings.max_upload_size_bytes", new_callable=PropertyMock) as mock_size:
        mock_size.return_value = 0
        files = {"file": ("test.txt", b"some content", "text/plain")}
        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

        assert response.status_code == 413
        # Custom exceptions return "message", standard Fast API ones return "detail"
        # Since FileTooLargeError is a CodeLensBaseError, it uses codelens_error_handler
        # which returns "message".
        assert "exceeds the maximum upload size" in response.json()["message"]

@pytest.mark.asyncio
async def test_upload_internal_error_masking(client: AsyncClient, auth_headers):
    # Mock shutil.copyfileobj to raise an exception
    with patch("shutil.copyfileobj", side_effect=Exception("Secret internal database error")):
        files = {"file": ("test.txt", b"some content", "text/plain")}
        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

        assert response.status_code == 500
        # The message should NOT contain "Secret internal database error"
        # Standard HTTPException uses "detail"
        assert "Secret internal database error" not in response.json()["detail"]
        assert "An error occurred while saving the file" in response.json()["detail"]
