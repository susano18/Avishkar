"""Security tests for document uploads."""
import pytest
from httpx import AsyncClient
from app.config import get_settings

settings = get_settings()

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """Test that uploading a file exceeding MAX_UPLOAD_SIZE_MB returns 413."""
    limit_bytes = settings.max_upload_size_bytes
    large_content = b"0" * (limit_bytes + 1024)
    files = {"file": ("large_file.pdf", large_content, "application/pdf")}

    response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)
    assert response.status_code == 413
    data = response.json()
    assert data["error"] == "FileTooLargeError"
    assert f"exceeds the maximum upload size" in data["message"]

@pytest.mark.asyncio
async def test_upload_internal_error_sanitization(client: AsyncClient, auth_headers: dict, monkeypatch):
    """Test that internal processing errors do not leak system paths."""
    from app.services.input_handler import process_uploaded_file
    async def mock_process(*args, **kwargs):
        raise RuntimeError("Sensitive info: /etc/passwd or 192.168.1.1")
    monkeypatch.setattr("app.api.documents.process_uploaded_file", mock_process)

    files = {"file": ("test.txt", b"some content", "text/plain")}
    response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)
    assert response.status_code in [201, 500]
    data = response.json()
    message = data.get("message", "") or (data.get("document", {}).get("error_message", "") if "document" in data else "")
    assert "/etc/passwd" not in message
    assert "192.168.1.1" not in message
