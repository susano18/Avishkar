## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-06-05 - [Insecure File Upload & Information Leakage]
**Vulnerability:** 1) Missing file size validation on the document upload endpoint, allowing for potential disk exhaustion (DoS). 2) Internal server errors during file saving were returned directly to the user, potentially leaking sensitive system information (e.g., local file paths).
**Learning:** FastAPI's `UploadFile` provides a `size` attribute (since v0.100.0) that should be validated early in the request lifecycle. Standard practice should always involve catching generic exceptions in I/O operations and returning sanitized error messages while logging the full context internally.
**Prevention:** 1) Always implement explicit size limits for all file upload endpoints. 2) Use structured logging to capture internal error details and raise `HTTPException` with generic `detail` strings for public-facing responses.
