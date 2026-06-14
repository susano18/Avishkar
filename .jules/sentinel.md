## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-06-14 - [Insecure File Upload - Missing Size Limits]
**Vulnerability:** The document upload endpoint lacked server-side file size validation, exposing the application to Denial of Service (DoS) attacks via resource exhaustion (disk/memory).
**Learning:** FastAPI's `UploadFile.seek()` (async) in version 0.136.3 only accepts a single `offset` argument and does not support `whence=2` (SEEK_END). To determine file size without reading the whole file into memory, one must use the underlying synchronous `file.file.seek(0, 2)` and `file.file.tell()`.
**Prevention:** Always enforce strict file size limits at the application layer using `file.file.seek(0, 2)` and `file.file.tell()` before processing or saving large uploads. Use the modern `HTTP_413_CONTENT_TOO_LARGE` status code for these errors.
