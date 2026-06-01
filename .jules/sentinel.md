## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-06-01 - [DoS via Large File Upload & Information Leakage]
**Vulnerability:** The `/documents/upload` endpoint lacked server-side file size validation, exposing the server to Denial of Service (DoS) attacks. Additionally, internal exception details (like full file paths and system errors) were returned to the client in `HTTPException` detail strings.
**Learning:** FastAPI's `UploadFile` provides a `size` attribute (in versions 0.115.6+) that allows for immediate validation without reading the entire file into memory or onto disk. Error responses should always be generic, while detailed errors should be captured in internal logs.
**Prevention:** 1) Always validate `file.size` against application-defined limits early in the request lifecycle. 2) Use generic error messages for client-facing exceptions. 3) Ensure `status` and `logger` are correctly imported and utilized for structured logging and standard HTTP responses.
