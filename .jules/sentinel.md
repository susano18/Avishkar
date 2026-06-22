## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-06-22 - [DoS via Disk Exhaustion & Information Leakage]
**Vulnerability:** Document upload endpoint lacked file size limits, allowing potential Denial of Service (DoS) through disk space exhaustion. Error handling also leaked internal file system paths during save failures.
**Learning:** Reliable file size validation in FastAPI requires accessing the underlying file object with synchronous `seek()` and `tell()` to ensure compatibility across versions. Information leakage in error responses can reveal sensitive system paths if exceptions are passed directly to the client.
**Prevention:** 1) Always validate file size before processing or saving to disk. 2) Sanitize error messages in `try...except` blocks before returning them to the API client, while logging full details internally. 3) Use modern, specific HTTP status codes like `413 Content Too Large` for resource limit violations.
