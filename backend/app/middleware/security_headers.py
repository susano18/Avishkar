"""
Security headers middleware.

Enforces essential security headers to protect against common web
vulnerabilities like clickjacking, MIME-sniffing, and XSS.
"""

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.config import get_settings

settings = get_settings()


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware that adds security-related headers to all responses.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        # 1. Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # 2. Prevent MIME-sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # 3. Enable browser XSS filtering
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # 4. Control referrer information
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # 5. Content Security Policy (CSP)
        # Allows self, FastAPI docs assets from cdn.jsdelivr.net, and unsafe-inline for Swagger/Redoc
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' cdn.jsdelivr.net; "
            "img-src 'self' data:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        response.headers["Content-Security-Policy"] = csp

        # 6. Strict-Transport-Security (HSTS) - only in production
        if not settings.DEBUG and request.url.scheme == "https":
            # 1 year in seconds
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response
