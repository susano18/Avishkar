## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-05-02 - [Missing File Size Validation (DoS Risk)]
**Vulnerability:** The document upload endpoint (`/documents/upload`) did not validate the size of uploaded files before saving them to disk or processing them.
**Learning:** Lack of upload size limits can lead to Denial of Service (DoS) attacks by exhausting disk space or memory. Even if a limit is defined in settings, it must be explicitly enforced in the application logic.
**Prevention:** Always validate `file.size` against a configured maximum early in the request lifecycle. Provide a fallback mechanism to determine file size if the framework does not automatically populate it.
