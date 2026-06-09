"""
Security headers tests.

Verifies that the SecurityHeadersMiddleware correctly attaches the expected
security headers (CSP, X-Frame-Options, HSTS, etc.) to all API responses.
"""

import pytest
from httpx import AsyncClient

from app.config import get_settings

settings = get_settings()


@pytest.mark.asyncio
async def test_security_headers_present(client: AsyncClient):
    """
    Test that essential security headers are present in the response.
    """
    response = await client.get("/health")
    assert response.status_code == 200

    # 1. Content-Security-Policy
    assert "Content-Security-Policy" in response.headers
    csp = response.headers["Content-Security-Policy"]
    assert "default-src 'self'" in csp
    assert "script-src 'self' 'unsafe-inline' cdn.jsdelivr.net" in csp

    # 2. X-Frame-Options
    assert response.headers.get("X-Frame-Options") == "DENY"

    # 3. X-Content-Type-Options
    assert response.headers.get("X-Content-Type-Options") == "nosniff"

    # 4. Referrer-Policy
    assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"


@pytest.mark.asyncio
async def test_hsts_header_in_production(client: AsyncClient, monkeypatch):
    """
    Test that Strict-Transport-Security is present when DEBUG is False.
    """
    # Force DEBUG to False for this test
    monkeypatch.setattr(settings, "DEBUG", False)

    # We need to re-import or re-initialize if the middleware captures settings at import time
    # but since it accesses settings from app.config which is lru_cached,
    # we might need to clear the cache if it was already called.
    from app.config import get_settings
    get_settings.cache_clear()

    response = await client.get("/health")
    assert response.status_code == 200
    assert "Strict-Transport-Security" in response.headers
    assert "max-age=31536000" in response.headers["Strict-Transport-Security"]


@pytest.mark.asyncio
async def test_hsts_header_absent_in_debug(client: AsyncClient, monkeypatch):
    """
    Test that Strict-Transport-Security is absent when DEBUG is True.
    """
    # Force DEBUG to True for this test
    monkeypatch.setattr(settings, "DEBUG", True)

    from app.config import get_settings
    get_settings.cache_clear()

    response = await client.get("/health")
    assert response.status_code == 200
    assert "Strict-Transport-Security" not in response.headers
