"""
Security headers middleware.

Adds essential security headers to every outgoing response to protect against
common web vulnerabilities like clickjacking, MIME-type sniffing, and XSS.
"""

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.config import get_settings

settings = get_settings()


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware that adds security-related headers to all HTTP responses.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        # Prevent the browser from rendering the page in a <frame>, <iframe> or <object>
        # to protect against clickjacking attacks.
        response.headers["X-Frame-Options"] = "DENY"

        # Prevent the browser from "sniffing" the content type, which can lead to
        # security vulnerabilities if the browser misinterprets the content.
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Enforce the use of HTTPS (HSTS) in non-debug environments.
        if not settings.DEBUG:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

        # Content Security Policy (CSP) - restrict where resources can be loaded from.
        # This policy is configured to support FastAPI's automatic documentation
        # (Swagger UI and ReDoc) while maintaining a high security posture.
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net",
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net",
            "img-src 'self' data: https://fastapi.tiangolo.com",
            "object-src 'none'",
            "frame-ancestors 'none'",
        ]
        response.headers["Content-Security-Policy"] = "; ".join(csp_directives)

        return response
