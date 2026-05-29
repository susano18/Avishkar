import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, PropertyMock
from app.main import app

@pytest.mark.asyncio
async def test_upload_file_too_large(auth_headers):
    """Test that uploading a file exceeding the limit returns 413."""
    # Patch settings to have a very small limit
    with patch("app.config.Settings.max_upload_size_bytes", new_callable=PropertyMock) as mock_size:
        mock_size.return_value = 10  # 10 bytes limit

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            files = {"file": ("test.pdf", b"this is more than 10 bytes", "application/pdf")}
            response = await ac.post("/api/v1/documents/upload", headers=auth_headers, files=files)

        assert response.status_code == 413
        # FileTooLargeError is a CodeLensBaseError, handled by codelens_error_handler
        # which returns {"error": "...", "message": "...", "status_code": ...}
        assert "exceeds the maximum upload size" in response.json()["message"]

@pytest.mark.asyncio
async def test_upload_save_failure_masks_error(auth_headers):
    """Test that file save failure returns a masked 500 error."""
    # Mock shutil.copyfileobj to raise an exception
    with patch("shutil.copyfileobj", side_effect=Exception("Internal path: /secret/path/failed")):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            files = {"file": ("test.pdf", b"some content", "application/pdf")}
            response = await ac.post("/api/v1/documents/upload", headers=auth_headers, files=files)

        # HTTPException is NOT a CodeLensBaseError, so it uses FastAPI's default handler
        # unless it's caught by Exception handler (but HTTPException is an Exception)
        # Actually, FastAPI has a default handler for HTTPException that returns {"detail": "..."}
        assert response.status_code == 500
        assert response.json()["detail"] == "Failed to save file."

@pytest.mark.asyncio
async def test_upload_extraction_failure_masks_error(auth_headers):
    """Test that extraction failure masks internal error details in the document record."""
    # Mock process_uploaded_file to raise an exception
    with patch("app.api.documents.process_uploaded_file", side_effect=Exception("OCR engine failed at 0xdeadbeef")):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            files = {"file": ("test.pdf", b"some content", "application/pdf")}
            response = await ac.post("/api/v1/documents/upload", headers=auth_headers, files=files)

        assert response.status_code == 201
        assert response.json()["document"]["status"] == "failed"
        assert response.json()["document"]["error_message"] == "Failed to extract text from file."
        assert "0xdeadbeef" not in response.json()["document"]["error_message"]
