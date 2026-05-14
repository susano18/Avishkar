## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-05-14 - [Information Leakage in Error Responses]
**Vulnerability:** The `upload_document` endpoint was returning detailed system error messages (including file paths and OS errors) directly to the client when file saving failed.
**Learning:** Exposing internal system details in API responses can assist an attacker in mapping the server's file system or identifying specific library/OS versions.
**Prevention:** Always catch low-level exceptions and return a generic, non-informative error message to the client, while logging the full details internally for debugging purposes.
