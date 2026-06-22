"""
Security regression tests for document upload.

Verifies file size limits and secure error handling to prevent
DoS and information leakage.
"""

import pytest
from httpx import AsyncClient
from unittest.mock import patch, PropertyMock
from app.config import Settings

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """Test that files exceeding the size limit are rejected with 413."""
    # Patch the settings instance used in app.api.documents
    with patch("app.api.documents.settings.MAX_UPLOAD_SIZE_MB", 1):
        # Patch the property on the class so it affects all instances including the one in documents.py
        with patch("app.config.Settings.max_upload_size_bytes", new_callable=PropertyMock) as mock_size:
            mock_size.return_value = 1024 * 1024 # 1 MB

            # Create a 2MB dummy file
            content = b"0" * (2 * 1024 * 1024)
            files = {"file": ("large.pdf", content, "application/pdf")}

            response = await client.post(
                "/api/v1/documents/upload",
                headers=auth_headers,
                files=files
            )

            assert response.status_code == 413
            data = response.json()
            assert "message" in data
            assert "exceeds the maximum upload size of 1 MB" in data["message"]

@pytest.mark.asyncio
async def test_upload_save_failure_sanitized(client: AsyncClient, auth_headers: dict):
    """Test that internal file save errors are sanitized in the response."""
    # Mock shutil.copyfileobj to raise an internal error
    with patch("shutil.copyfileobj", side_effect=Exception("Sensitive system path /etc/passwd failed")):
        content = b"small file content"
        files = {"file": ("test.pdf", content, "application/pdf")}

        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

        assert response.status_code == 500
        # FastAPI's HTTPException returns error in 'detail'
        data = response.json()
        assert "detail" in data
        # Check that sensitive info is NOT in the response
        assert "Sensitive system path" not in data["detail"]
        # Check that generic message IS in the response
        assert "Failed to save file to server storage" in data["detail"]
