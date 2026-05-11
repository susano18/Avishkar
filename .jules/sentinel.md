## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-05-11 - [Missing Enforcement of Configured Upload Limits]
**Vulnerability:** The `/documents/upload` endpoint did not enforce the `MAX_UPLOAD_SIZE_MB` limit, despite `FileTooLargeError` being defined in the utility layer. This exposed the server to resource exhaustion (DoS) during file processing.
**Learning:** Security debt can exist in the form of "half-implemented" features where the error types are defined but the validation logic is missing from the API handlers.
**Prevention:** Ensure that all resource-intensive operations (uploads, LLM calls) have explicit, enforced limits at the entry point of the request.
