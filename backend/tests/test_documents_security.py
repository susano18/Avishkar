import pytest
from httpx import AsyncClient
import io

@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """Test that uploading a file exceeding MAX_UPLOAD_SIZE_MB returns 413."""
    # Create a large "file" (e.g., 51MB if limit is 50MB)
    content = b"0" * (51 * 1024 * 1024)
    files = {"file": ("large_file.pdf", io.BytesIO(content), "application/pdf")}

    response = await client.post("/api/v1/documents/upload", headers=auth_headers, files=files)

    assert response.status_code == 413
    assert "exceeds the maximum upload size" in response.json()["message"]
