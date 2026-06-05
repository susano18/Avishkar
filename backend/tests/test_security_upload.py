"""
Security tests for document upload.

Tests file size limits and secure error handling (info leakage prevention).
"""

from unittest.mock import patch, MagicMock, AsyncMock

import pytest
from httpx import AsyncClient
from app.config import get_settings

settings = get_settings()

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """Test that files exceeding the size limit are rejected with 413."""

    # Mock settings to have a very small limit for this test
    # We patch it where it is imported in app.api.documents
    with patch("app.api.documents.get_settings") as mock_settings_getter:
        mock_settings = MagicMock()
        mock_settings.max_upload_size_bytes = 5  # 5 bytes limit
        mock_settings.MAX_UPLOAD_SIZE_MB = 0
        mock_settings_getter.return_value = mock_settings

        from app.api.documents import upload_document
        from app.models.user import User

        mock_db = MagicMock()
        mock_db.flush = AsyncMock()
        mock_user = MagicMock(spec=User)
        mock_user.id = "test-user-id"

        mock_file = MagicMock()
        mock_file.filename = "large.pdf"
        mock_file.size = 10  # > 5

        # We need to ensure 'settings' in documents.py is our mock_settings
        with patch("app.api.documents.settings", mock_settings):
            # This should raise FileTooLargeError
            from app.utils.exceptions import FileTooLargeError
            with pytest.raises(FileTooLargeError):
                await upload_document(file=mock_file, db=mock_db, current_user=mock_user)

@pytest.mark.asyncio
async def test_upload_file_save_failure_masking(client: AsyncClient, auth_headers: dict):
    """Test that internal file save errors do not leak system details."""
    content = b"test content"
    files = {"file": ("test.pdf", content, "application/pdf")}

    # Mock 'open' or 'shutil.copyfileobj' to raise an exception with sensitive info
    with patch("app.api.documents.open", side_effect=Exception("Sensitive path: /etc/passwd error")):
        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

        assert response.status_code == 500
        data = response.json()
        assert data["detail"] == "An error occurred while saving the uploaded file."
        assert "/etc/passwd" not in data["detail"]
