"""
Security tests for file uploads.

Verifies that file size limits are enforced to prevent DoS attacks.
"""

import io
from unittest.mock import patch

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_upload_file_too_large(client: AsyncClient, auth_headers: dict):
    """
    Test that uploading a file exceeding the size limit returns 413.
    """
    # Create a small "large" file for testing
    content = b"x" * 1024  # 1 KB
    file_name = "test.pdf"
    files = {"file": (file_name, io.BytesIO(content), "application/pdf")}

    # We need to ensure max_upload_size_bytes is small enough
    with patch("app.api.documents.settings") as mocked_settings:
        mocked_settings.max_upload_size_bytes = 512
        mocked_settings.MAX_UPLOAD_SIZE_MB = 0

        response = await client.post(
            "/api/v1/documents/upload",
            headers=auth_headers,
            files=files
        )

    assert response.status_code == 413
    assert "exceeds the maximum upload size" in response.json()["message"]


@pytest.mark.asyncio
async def test_upload_file_within_limit(
    client: AsyncClient,
    auth_headers: dict
):
    """
    Test that uploading a file within the size limit is accepted.
    """
    content = b"x" * 100
    file_name = "test.txt"
    files = {"file": (file_name, io.BytesIO(content), "text/plain")}

    # Mock settings to have a 1 KB limit
    with patch("app.api.documents.settings") as mocked_settings:
        mocked_settings.max_upload_size_bytes = 1024
        mocked_settings.MAX_UPLOAD_SIZE_MB = 1

        # Also need to mock process_uploaded_file to avoid real extraction
        with patch("app.api.documents.process_uploaded_file") as mocked_proc:
            mocked_proc.return_value = "Extracted text"

            response = await client.post(
                "/api/v1/documents/upload",
                headers=auth_headers,
                files=files
            )

    assert response.status_code == 201
    assert response.json()["document"]["filename"] == "test.txt"
