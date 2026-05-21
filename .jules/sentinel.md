## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-05-22 - [DoS and Information Leakage in File Uploads]
**Vulnerability:** The document upload endpoint lacked file size validation, allowing potential Denial of Service (DoS) attacks via massive file uploads. Additionally, exception handlers were returning raw error details to the user, potentially leaking internal paths or environment info.
**Learning:** FastAPI's `UploadFile.size` (available in 0.115.6+) provides a convenient way to check file size before processing. Structured logging allows capturing full error details for internal debugging while still "failing securely" with generic messages for the client.
**Prevention:** 1) Always validate `file.size` against a configured maximum at the entry point. 2) Catch and sanitize exceptions in API routes, logging the root cause internally but returning generic `HTTPException` details.
