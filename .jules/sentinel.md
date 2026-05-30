## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-05-30 - [DoS via Large File Uploads]
**Vulnerability:** The document upload endpoint lacked server-side file size validation, allowing potentially unlimited disk/memory exhaustion. Detailed internal error messages were also exposed to the client.
**Learning:** FastAPI's `UploadFile` (0.115.6+) provides a `size` attribute for easy validation. When mocking Pydantic settings in tests, `unittest.mock.PropertyMock` at the class level is required because instance-level properties are read-only.
**Prevention:** 1) Always validate `file.size` before processing uploads. 2) Mask internal exception details in production responses using generic messages while logging the actual error for observability. 3) Configure global size limits at the proxy/gateway level as defense-in-depth.
