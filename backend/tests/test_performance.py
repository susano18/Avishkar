"""
Performance verification tests for Document API.
Ensures optimized listing does not return full text and correctly computes length.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document, FileType, ProcessingStatus
from app.models.user import User

@pytest.mark.asyncio
async def test_list_documents_performance_optimization(
    client: AsyncClient, auth_headers: dict,
    db_session: AsyncSession, test_user: User,
):
    """Verify that document listing does not include extracted_text and includes length."""
    text_content = "This is a test document with some text content."
    doc = Document(
        user_id=test_user.id,
        filename="perf_test.pdf",
        file_type=FileType.PDF,
        extracted_text=text_content,
        status=ProcessingStatus.COMPLETED,
    )
    db_session.add(doc)
    await db_session.commit()

    response = await client.get("/api/v1/documents", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()

    assert len(data["documents"]) == 1
    doc_resp = data["documents"][0]

    # Core optimization check: extracted_text should be None in the response to save bandwidth
    assert doc_resp["extracted_text"] is None
    # New field should be present and correct
    assert "extracted_text_length" in doc_resp
    assert doc_resp["extracted_text_length"] == len(text_content)

    # Detailed view should still have the full text
    response = await client.get(f"/api/v1/documents/{doc.id}", headers=auth_headers)
    assert response.status_code == 200
    detail_data = response.json()
    assert detail_data["extracted_text"] == text_content
