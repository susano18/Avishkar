import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_security_headers_present():
    """
    Test that security headers are correctly added to responses by the middleware.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")

    assert response.status_code == 200

    # Check for presence of security headers
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert "Content-Security-Policy" in response.headers

    csp = response.headers["Content-Security-Policy"]
    assert "default-src 'self'" in csp
    assert "script-src 'self' 'unsafe-inline' cdn.jsdelivr.net" in csp

@pytest.mark.asyncio
async def test_hsts_header_not_present_in_http():
    """
    Test that HSTS header is not present when using HTTP or in debug mode.
    (Tests are typically run with DEBUG=False but using http:// scheme)
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")

    assert response.status_code == 200
    assert "Strict-Transport-Security" not in response.headers
