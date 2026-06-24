## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-06-24 - [Information Leakage and DoS via Large Uploads]
**Vulnerability:** The document upload endpoint lacked file size validation and returned raw exception messages (including file paths) to the client on storage failures.
**Learning:** FastAPI's `UploadFile` size attribute can be inconsistent; using `seek(0, 2)` and `tell()` on the underlying file object provides a reliable measurement. Verbose error messages in `try...except` blocks can leak internal system architecture.
**Prevention:** 1) Always validate file size before processing or saving to disk. 2) Sanitize `HTTPException` detail messages to return generic errors while logging specific details internally. 3) Use `status.HTTP_413_CONTENT_TOO_LARGE` for size limit rejections.
