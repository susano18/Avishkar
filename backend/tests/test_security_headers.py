"""
Security headers verification tests.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_security_headers_present(client: AsyncClient):
    """Test that essential security headers are present in responses."""
    response = await client.get("/health")
    assert response.status_code == 200

    # 1. Clickjacking protection
    assert response.headers["X-Frame-Options"] == "DENY"

    # 2. MIME-sniffing protection
    assert response.headers["X-Content-Type-Options"] == "nosniff"

    # 3. XSS protection
    assert response.headers["X-XSS-Protection"] == "1; mode=block"

    # 4. Referrer Policy
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"

    # 5. Content Security Policy
    assert "Content-Security-Policy" in response.headers
    csp = response.headers["Content-Security-Policy"]
    assert "default-src 'self'" in csp
    assert "frame-ancestors 'none'" in csp


@pytest.mark.asyncio
async def test_hsts_header_not_in_debug(client: AsyncClient):
    """Test HSTS is NOT present when DEBUG=True (default in tests)."""
    response = await client.get("/health")
    assert "Strict-Transport-Security" not in response.headers
