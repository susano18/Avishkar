"""
Security tests for document upload.

Tests file size limits (DoS protection) and error message sanitization.
"""

import pytest
from httpx import AsyncClient
from unittest.mock import patch, MagicMock
from app.models.user import User

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """Test that uploading a file exceeding the size limit returns 413."""
    # Create a large dummy file content
    content = b"a" * (51 * 1024 * 1024)  # 51 MB, limit is 50 MB
    files = {"file": ("large.pdf", content, "application/pdf")}

    response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

    assert response.status_code == 413
    assert "exceeds the maximum upload size" in response.json()["message"]

@pytest.mark.asyncio
async def test_upload_file_save_failure_sanitization(
    client: AsyncClient, auth_headers: dict, test_user: User
):
    """Test that file saving failures return a generic error message (no leakage)."""
    content = b"test content"
    files = {"file": ("test.pdf", content, "application/pdf")}

    # Mock shutil.copyfileobj to raise an exception with sensitive info
    with patch("shutil.copyfileobj", side_effect=Exception("Sensitive path: /secret/path/to/fail")):
        response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

    assert response.status_code == 500
    data = response.json()
    # HTTPException with detail="..." returns {"detail": "..."} by default
    # unless handled by a custom exception handler.
    # In this app, global_exception_handler handles general Exception,
    # but HTTPException is handled by FastAPI's default handler.
    assert data["detail"] == "Failed to save file."
    assert "Sensitive path" not in data["detail"]
    assert "/secret/path" not in data["detail"]
