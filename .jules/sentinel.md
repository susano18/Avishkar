## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-05-15 - [Denial of Service (DoS) via Large File Uploads]
**Vulnerability:** The `/documents/upload` endpoint did not validate the size of uploaded files before processing them, potentially allowing an attacker to exhaust server disk space or memory by uploading extremely large files.
**Learning:** Even if the underlying web framework (like Starlette/FastAPI) has some default limits, explicit application-level validation against configurable thresholds is necessary to protect resources and provide clear error feedback.
**Prevention:** Always check the `size` attribute of uploaded file objects against a defined maximum threshold before proceeding with resource-intensive operations like saving to disk or text extraction. Use `413 Content Too Large` to inform the client of the limit.
