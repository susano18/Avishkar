## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-04-30 - [Missing File Size Validation in Upload Endpoint]
**Vulnerability:** The `/documents/upload` endpoint accepted files of any size, despite having a `MAX_UPLOAD_SIZE_MB` setting, creating a Denial of Service (DoS) risk.
**Learning:** Security configurations (like `MAX_UPLOAD_SIZE_MB`) and custom exceptions (like `FileTooLargeError`) do not provide protection unless they are explicitly implemented in the request handling logic.
**Prevention:** Always verify that security limits defined in configuration are enforced at the API entry points. When adding new upload endpoints, include size checks as a standard part of the validation pipeline.
