## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-06-16 - [Resource Exhaustion via Large File Uploads]
**Vulnerability:** The document upload endpoint lacked file size validation, allowing users to upload arbitrarily large files. This could lead to Denial of Service (DoS) by exhausting disk space or memory during processing.
**Learning:** FastAPI/Starlette's `UploadFile` may not always have a reliable `.size` attribute depending on the version. Manually determining size using the underlying file object's `seek` and `tell` is a more robust approach for enforcement.
**Prevention:** Always validate file sizes at the application level before performing any costly I/O or database operations. Use `file.file.seek(0, 2)` and `file.file.tell()` to find the size, and ensure `file.file.seek(0)` is called afterward to reset the pointer for processing.
