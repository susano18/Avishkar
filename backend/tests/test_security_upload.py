"""
Security-focused tests for document uploads.

Verifies file size limits (DoS protection) and error message sanitization
(Information Leakage prevention).
"""

import pytest
from unittest.mock import patch
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """Test that files exceeding the size limit are rejected with 413."""
    # We don't actually want to send 60MB in a test if we can avoid it,
    # so we'll mock the settings to a very small value.
    with patch("app.api.documents.settings") as mock_settings:
        mock_settings.MAX_UPLOAD_SIZE_MB = 1
        mock_settings.max_upload_size_bytes = 1024

        # 1KB limit
        content = b"0" * 2048 # 2KB
        files = {"file": ("too_large.pdf", content, "application/pdf")}
        response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

        assert response.status_code == 413
        assert "exceeds the maximum upload size" in response.json()["message"]

@pytest.mark.asyncio
async def test_upload_error_sanitization_save_failure(
    client: AsyncClient, auth_headers: dict, db_session: AsyncSession
):
    """Test that file save failures don't leak internal error details."""
    files = {"file": ("test.pdf", b"fake pdf content", "application/pdf")}

    # Mock shutil.copyfileobj to raise an exception with sensitive info
    with patch("shutil.copyfileobj", side_effect=Exception("Sensitive path: /etc/passwd failed")):
        response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

        assert response.status_code == 500
        data = response.json()
        # Generic message from global_exception_handler
        # print(f"DEBUG: {data}")
        assert data["detail"] == "An error occurred while saving the file."
        # Ensure sensitive info is NOT in the response
        assert "etc/passwd" not in data["detail"]
        assert "Sensitive path" not in data["detail"]

@pytest.mark.asyncio
async def test_upload_error_sanitization_extraction_failure(
    client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_user: User
):
    """Test that extraction failures don't leak internal error details."""
    files = {"file": ("test.pdf", b"fake pdf content", "application/pdf")}

    # Mock process_uploaded_file to raise an exception
    with patch("app.api.documents.process_uploaded_file", side_effect=Exception("Internal extraction logic error at line 42")):
        # We need to mock ensure_upload_dir to avoid real IO
        from pathlib import Path
        with patch("app.api.documents.ensure_upload_dir") as mock_dir:
            # We must use a valid directory that exist in the sandbox for the file open to work
            # or mock the open() call. Let's mock the open() call too.
            mock_dir.return_value = Path("/tmp")
            with patch("app.api.documents.open", create=True) as mock_open:
                response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

            # The endpoint returns 201 even if extraction fails (it just updates the status to FAILED)
            # wait, looking at the code:
            # except Exception as e:
            #     doc.status = ProcessingStatus.FAILED
            #     doc.error_message = "Text extraction failed."
            #     logger.error("document_processing_failed", doc_id=doc.id, error=str(e))
            # It continues to return DocumentUploadResponse.

            assert response.status_code == 201
            data = response.json()
            assert data["document"]["status"] == "failed"
            assert data["document"]["error_message"] == "Text extraction failed."
            # Ensure internal detail is NOT in the response
            assert "line 42" not in data["document"]["error_message"]
