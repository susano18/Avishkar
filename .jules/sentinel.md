## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-06-12 - [Defense in Depth: Security Headers Middleware]
**Vulnerability:** Lack of standard security headers (X-Frame-Options, CSP, etc.) making the application vulnerable to Clickjacking and MIME-sniffing.
**Learning:** Implementing a global middleware for security headers provides a consistent layer of defense across all endpoints (including error pages) without requiring individual route configuration.
**Prevention:** Always include a security headers middleware in FastAPI/Starlette applications to enforce secure-by-default behavior for all outgoing responses.
