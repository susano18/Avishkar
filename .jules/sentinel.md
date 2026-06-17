## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-05-22 - [Denial of Service via Resource Exhaustion]
**Vulnerability:** The document upload endpoint (`/documents/upload`) lacked file size validation, allowing users to upload arbitrarily large files. This could lead to disk space exhaustion or CPU/memory exhaustion during PDF/Audio processing.
**Learning:** FastAPI's `UploadFile` does not automatically enforce size limits. Validating size using `file.file.seek(0, 2)` and `file.file.tell()` is necessary before performing any I/O or processing. Resetting the pointer with `seek(0)` is critical to avoid "empty file" errors downstream.
**Prevention:** Always implement explicit file size checks early in the request lifecycle for any endpoint that accepts file uploads. Use structured logging to monitor and alert on rejected large uploads.
