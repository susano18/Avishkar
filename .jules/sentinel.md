## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-05-19 - [DoS and Information Leakage in File Uploads]
**Vulnerability:** The document upload endpoint lacked file size validation, making it vulnerable to Denial of Service (DoS) attacks. Additionally, failure to catch exceptions during file saving resulted in detailed error messages (including internal paths) being returned to the user.
**Learning:** FastAPI's `UploadFile` provides a `.size` attribute that can be used for immediate validation before processing. Standardizing error responses to use generic messages while logging details internally is critical to prevent information leakage.
**Prevention:** 1) Always validate `file.size` against a defined limit early in the request lifecycle. 2) Wrap I/O operations in try-except blocks and return generic `HTTPException` details to the user. 3) Use structured logging to capture the full error for internal debugging without exposing it to the client.
