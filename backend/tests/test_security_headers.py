import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.config import get_settings

@pytest.mark.asyncio
async def test_security_headers():
    settings = get_settings()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/health")
        assert response.status_code == 200

        headers = response.headers

        # Check for essential security headers
        assert headers["X-Frame-Options"] == "DENY"
        assert headers["X-Content-Type-Options"] == "nosniff"
        assert "Content-Security-Policy" in headers

        # HSTS should NOT be present in debug mode
        if settings.DEBUG:
            assert "Strict-Transport-Security" not in headers
        else:
            assert "Strict-Transport-Security" in headers
            assert headers["Strict-Transport-Security"] == "max-age=31536000; includeSubDomains"
