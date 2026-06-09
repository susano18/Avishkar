"""
Security headers middleware.

Adds essential security headers to all outgoing responses to protect against
common web vulnerabilities such as XSS, clickjacking, and content sniffing.
"""

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.config import get_settings

settings = get_settings()


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware that attaches security-related headers to every response.

    Headers included:
    - Content-Security-Policy: Mitigates XSS and data injection.
    - X-Frame-Options: Prevents clickjacking.
    - X-Content-Type-Options: Prevents MIME-type sniffing.
    - Referrer-Policy: Controls how much referrer information is shared.
    - Strict-Transport-Security (HSTS): Enforces HTTPS (only in production).
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        # 1. Content-Security-Policy (CSP)
        # Allows FastAPI's Swagger/ReDoc (unsafe-inline and cdn.jsdelivr.net)
        # and standard self/data origins.
        csp_parts = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' cdn.jsdelivr.net",
            "style-src 'self' 'unsafe-inline' cdn.jsdelivr.net",
            "img-src 'self' data:",
            "connect-src 'self'",
            "frame-ancestors 'none'",
        ]
        response.headers["Content-Security-Policy"] = "; ".join(csp_parts)

        # 2. X-Frame-Options
        # Prevents the site from being embedded in an iframe (Clickjacking protection).
        response.headers["X-Frame-Options"] = "DENY"

        # 3. X-Content-Type-Options
        # Prevents browsers from "sniffing" the content type.
        response.headers["X-Content-Type-Options"] = "nosniff"

        # 4. Referrer-Policy
        # Restricts the amount of referrer information sent with requests.
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # 5. Strict-Transport-Security (HSTS)
        # Forces HTTPS. Only applied when not in debug mode to avoid issues during development.
        if not settings.DEBUG:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )

        return response
