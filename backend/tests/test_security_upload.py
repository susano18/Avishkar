"""
Security tests for document uploads.

Verifies file size limits and ensures no sensitive information leakage
in error responses.
"""

import pytest
from unittest.mock import patch, MagicMock, PropertyMock
from httpx import AsyncClient
from app.config import Settings


@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """Test that uploading a file exceeding the size limit returns 413."""
    # Mock settings to have a very small limit (1 byte)
    # Using PropertyMock on the class because Pydantic settings properties are read-only on instances
    with patch("app.config.Settings.max_upload_size_bytes", new_callable=PropertyMock) as mock_size:
        mock_size.return_value = 1

        files = {"file": ("test.pdf", b"too much data", "application/pdf")}
        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

        assert response.status_code == 413
        assert "exceeds the maximum upload size" in response.json()["message"]


@pytest.mark.asyncio
async def test_upload_error_no_leakage(client: AsyncClient, auth_headers: dict):
    """Test that internal save errors do not leak path or exception details."""
    # Mock shutil.copyfileobj to raise an exception
    with patch("shutil.copyfileobj", side_effect=Exception("Sensitive path: /etc/passwd or DB error")):
        files = {"file": ("test.pdf", b"some data", "application/pdf")}
        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

        assert response.status_code == 500
        # Should NOT contain the specific error message or sensitive paths
        data = response.json()
        assert "Sensitive path" not in data["detail"]
        assert "/etc/passwd" not in data["detail"]
        assert "Internal server error" in data["detail"]
