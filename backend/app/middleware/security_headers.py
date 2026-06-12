"""
Security headers middleware.

Adds essential security headers to every outgoing response to protect against
common web vulnerabilities like Clickjacking, MIME-sniffing, and XSS.
"""

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.config import get_settings

settings = get_settings()


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware that adds security-related HTTP headers to all responses.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        # 1. Prevent Clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # 2. Prevent MIME-sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # 3. Enable XSS protection in older browsers
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # 4. Content Security Policy (CSP)
        # Optimized for FastAPI's Swagger/ReDoc documentation
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' cdn.jsdelivr.net",
            "style-src 'self' 'unsafe-inline' cdn.jsdelivr.net",
            "img-src 'self' data: fastly.picsum.photos picsum.photos",
            "connect-src 'self'",
            "font-src 'self' cdn.jsdelivr.net",
            "object-src 'none'",
            "base-uri 'self'",
            "form-action 'self'",
            "frame-ancestors 'none'",
        ]
        response.headers["Content-Security-Policy"] = "; ".join(csp_directives)

        # 5. Strict-Transport-Security (HSTS)
        # Only applied in production-like environments over HTTPS
        if not settings.DEBUG and request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )

        return response
