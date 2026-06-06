## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-06-06 - [Information Leakage via Unmasked Internal Exceptions]
**Vulnerability:** API endpoints were returning raw exception strings to users during file upload failures, potentially exposing internal system paths, library versions, or environment details.
**Learning:** Returning raw exceptions in API responses can leak sensitive infrastructure details that assist attackers in reconnaissance. Even "obvious" failures should be caught and replaced with generic, safe messages for the end user.
**Prevention:** Always wrap security-critical or system-interacting logic in try-except blocks. Log the full detailed error internally for debugging, but return a sanitized, generic `HTTPException` to the client.
