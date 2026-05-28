## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-05-28 - [Unrestricted File Upload Size]
**Vulnerability:** The `/documents/upload` endpoint lacked server-side file size validation, exposing the application to Denial of Service (DoS) attacks via disk or memory exhaustion.
**Learning:** FastAPI version 0.115.6+ introduces a `size` attribute on `UploadFile` objects, enabling immediate validation of the `Content-Length` header without manually reading the file stream.
**Prevention:** Always validate `UploadFile.size` against a configured maximum (e.g., `settings.max_upload_size_bytes`) and raise a `413 Content Too Large` exception using the modern `status.HTTP_413_CONTENT_TOO_LARGE` constant.
