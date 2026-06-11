"""
Security headers middleware.

Adds essential security headers to all outgoing responses to protect against
common web vulnerabilities such as Clickjacking, MIME-sniffing, and XSS.
"""

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.config import get_settings

settings = get_settings()


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware that attaches security-related headers to every HTTP response.

    Headers included:
    - X-Frame-Options: Prevents clickjacking by disallowing the site to be framed.
    - X-Content-Type-Options: Prevents MIME-sniffing.
    - Content-Security-Policy: Restricts where resources can be loaded from.
    - Strict-Transport-Security: Enforces HTTPS (only in non-debug/production).
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        # 1. Prevent Clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # 2. Prevent MIME-sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # 3. Content Security Policy (CSP)
        # We allow 'unsafe-inline' and 'cdn.jsdelivr.net' to support FastAPI's
        # automatic Swagger and ReDoc documentation.
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' cdn.jsdelivr.net",
            "style-src 'self' 'unsafe-inline' cdn.jsdelivr.net",
            "img-src 'self' data: fastly.picsum.photos picsum.photos",
            "connect-src 'self'",
            "font-src 'self' cdn.jsdelivr.net",
            "object-src 'none'",
            "base-uri 'self'",
            "frame-ancestors 'none'",
        ]
        response.headers["Content-Security-Policy"] = "; ".join(csp_directives)

        # 4. HTTP Strict Transport Security (HSTS)
        # Only applied if NOT in debug mode and the request is HTTPS.
        if not settings.DEBUG and request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )

        return response
