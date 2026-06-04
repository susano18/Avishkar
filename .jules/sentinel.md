## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-06-04 - [Information Leakage and DoS via File Uploads]
**Vulnerability:** The `/documents/upload` endpoint was vulnerable to potential DoS due to missing file size enforcement and information leakage by returning raw exception details (including local file paths) to clients on failure.
**Learning:** FastAPI's `UploadFile` provides a `size` attribute that should be checked against application limits before processing to prevent resource exhaustion. Generic error messages must be returned to clients in security-sensitive paths, while full context is logged internally.
**Prevention:** 1) Implement explicit `file.size` checks early in the request lifecycle. 2) Wrap I/O and external service calls in `try-except` blocks that catch generic `Exception`. 3) Log specific errors with identifiers (like `doc_id`) internally and return a generic `HTTPException` detail to the user.
