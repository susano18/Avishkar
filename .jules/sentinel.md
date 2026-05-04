## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-05-04 - [DoS via Large File Uploads]
**Vulnerability:** The `/documents/upload` endpoint did not validate the size of uploaded files before saving them to disk and processing them, making the application vulnerable to Denial of Service (DoS) attacks via disk space exhaustion or memory OOM.
**Learning:** `UploadFile.size` in FastAPI/Starlette can sometimes be `None` depending on how the request was parsed. A robust size check should include a fallback using `file.file.seek(0, 2)` and `file.file.tell()` to ensure the limit is enforced.
**Prevention:** Always enforce file size limits at the application level (in addition to any reverse proxy limits) and use a reliable method to determine the actual byte count of the `SpooledTemporaryFile`.
