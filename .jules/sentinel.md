## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-06-23 - [Insecure File Upload size validation]
**Vulnerability:** The application lacked file size validation on the upload endpoint, making it vulnerable to Denial of Service (DoS) via resource exhaustion (disk and memory).
**Learning:** FastAPI's 'UploadFile.size' attribute is not always present or reliable across different versions/transports. Furthermore, its async 'seek' method may not support the 'whence' parameter in all versions.
**Prevention:** Always use the underlying 'file.file.seek(0, 2)' (synchronous) and 'file.file.tell()' to determine the actual file size before processing or saving to disk, followed by 'file.file.seek(0)' to reset the pointer.
