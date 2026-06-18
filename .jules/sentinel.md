## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-06-18 - [Missing Upload File Size Validation]
**Vulnerability:** The `/documents/upload` endpoint did not validate the size of uploaded files before processing them, creating a risk of Denial of Service (DoS) through resource exhaustion.
**Learning:** FastAPI's `UploadFile` object does not automatically enforce file size limits. While some deployment environments (like Nginx) can be configured with `client_max_body_size`, the application should provide its own guardrails as part of defense-in-depth.
**Prevention:** Explicitly check the file size using `file.file.seek(0, 2)` and `file.file.tell()` (and resetting with `file.file.seek(0)`) at the entry point of the upload handler before any processing or disk I/O occurs.
