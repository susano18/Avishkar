## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-05-07 - [Missing Input Length Limits on File Uploads]
**Vulnerability:** The `/documents/upload` endpoint did not enforce the `MAX_UPLOAD_SIZE_MB` setting, allowing potentially unbounded file uploads.
**Learning:** Even when security settings (like max size) are defined in configuration, they must be explicitly enforced at the API entry points. Relying on default web server limits may not be sufficient if the application logic processes the file before those limits are hit.
**Prevention:** 1) Always validate `file.size` from `UploadFile` against application-defined limits. 2) Use standard HTTP 413 status codes for rejection. 3) Implement automated security tests that mock settings to verify limit enforcement.
