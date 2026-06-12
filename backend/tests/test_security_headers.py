"""
Security headers tests.

Verifies that essential security headers are present in API responses.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_security_headers_present(client: AsyncClient):
    """
    Test that security headers are included in a standard API response.
    """
    response = await client.get("/health")
    assert response.status_code == 200

    # Verify standard security headers
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-XSS-Protection"] == "1; mode=block"

    # Verify Content-Security-Policy
    csp = response.headers["Content-Security-Policy"]
    assert "default-src 'self'" in csp
    assert "script-src 'self' 'unsafe-inline' cdn.jsdelivr.net" in csp
    assert "frame-ancestors 'none'" in csp


@pytest.mark.asyncio
async def test_security_headers_on_error(client: AsyncClient):
    """
    Test that security headers are also present on error responses.
    """
    # Trigger a 404 by requesting a non-existent endpoint
    response = await client.get("/api/v1/nonexistent-endpoint")
    assert response.status_code == 404

    # Verify security headers are still there
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert "Content-Security-Policy" in response.headers
