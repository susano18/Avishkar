## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-06-19 - [Denial of Service via Large File Uploads]
**Vulnerability:** The document upload endpoint lacked file size validation, allowing attackers to upload massive files that could exhaust server disk space, memory, and CPU resources during processing.
**Learning:** FastAPI's `UploadFile` provides a `.size` attribute that may be missing or inconsistent depending on the version. Manual validation using the underlying file object's `seek(0, 2)` and `tell()` methods is a reliable way to enforce limits before saving or processing data.
**Prevention:** Always implement application-layer file size limits. Check the size immediately upon receipt and reject oversized files with a 413 Content Too Large status code to prevent resource exhaustion.
