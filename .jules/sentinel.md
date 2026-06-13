## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-06-13 - [Reliable File Size Validation in FastAPI]
**Vulnerability:** Document upload endpoint lacked file size limits, allowing potential Denial of Service (DoS) through resource exhaustion (disk space/memory).
**Learning:** In certain FastAPI/Starlette versions, `UploadFile.size` is unavailable or unreliable. Additionally, `UploadFile.seek()` may be a coroutine that only accepts one argument (`offset`). Reliable size detection for security checks requires accessing the underlying `file.file` object to use `seek(0, 2)` (with `whence`) and `tell()`.
**Prevention:** Implement early file size validation in all upload endpoints. Use the underlying file object for multi-parameter `seek` operations and always reset the cursor to `0` before continuing processing.
