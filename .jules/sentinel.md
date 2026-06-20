## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-06-20 - [Resource Exhaustion & Information Leakage in File Uploads]
**Vulnerability:** 1) The `/documents/upload` endpoint lacked file size validation, exposing the server to Denial of Service (DoS) via extremely large uploads. 2) Unhandled exceptions during file processing were returned directly to the client, potentially leaking system paths or internal logic.
**Learning:** 1) FastAPI's `UploadFile` does not automatically enforce size limits; manual validation using `file.file.seek(0, 2)` and `file.file.tell()` is necessary before processing. 2) Generic `except Exception` blocks in API endpoints must sanitize error messages returned to the client while logging full details internally.
**Prevention:** 1) Always validate `UploadFile` size before saving or processing. 2) Implement a clear distinction between "user-safe" exceptions (4xx) and "internal" exceptions (500), ensuring the latter never leak raw exception strings.
