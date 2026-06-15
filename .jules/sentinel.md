## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-06-15 - [Resource Exhaustion and Information Leakage in File Upload]
**Vulnerability:** The document upload endpoint lacked a file size limit check before saving to disk, creating a Denial of Service (DoS) risk through storage exhaustion. Additionally, it leaked internal system error details (e.g., file system paths) to clients when file operations failed.
**Learning:** 1) In FastAPI, the `UploadFile.size` attribute might be missing in some versions; using `seek(0, 2)` and `tell()` on the underlying file stream is a more reliable way to determine size before processing. 2) Catching generic `Exception` and returning its string representation to clients can expose internal system architecture and paths.
**Prevention:** 1) Always validate input size before performing disk or memory-intensive operations. 2) Log detailed error information internally and return sanitized, generic messages to the end user.
