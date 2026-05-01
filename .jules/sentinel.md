## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2025-05-15 - [Denial of Service (DoS) via Large File Uploads]
**Vulnerability:** The `/documents/upload` endpoint did not validate the size of uploaded files before saving them to disk and processing them, allowing an attacker to exhaust server disk space and memory.
**Learning:** Relying on configuration settings without active enforcement in the application code can leave endpoints vulnerable to resource exhaustion. FastAPI's `UploadFile` provides a `size` attribute (in recent versions) and access to the underlying file object for manual size checks.
**Prevention:** 1) Always validate file sizes at the start of upload handlers. 2) Use `status.HTTP_413_CONTENT_TOO_LARGE` for rejection. 3) Implement fallback size checks if the framework doesn't automatically provide the size.
