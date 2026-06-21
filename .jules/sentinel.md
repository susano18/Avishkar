## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-06-21 - [Resource Exhaustion via Large File Uploads]
**Vulnerability:** The document upload endpoint (`/documents/upload`) did not enforce the `MAX_UPLOAD_SIZE_MB` limit, allowing for potential DoS attacks.
**Learning:** FastAPI's `UploadFile.size` can be unreliable or missing depending on the version and underlying engine. Using `file.file.seek(0, 2)` and `file.file.tell()` provides a robust way to determine size across environments.
**Prevention:** Always validate file size early in the request lifecycle, before any significant processing or database operations occur. Use the synchronous underlying file object for reliable size measurement.
