## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2024-05-20 - [LLM Parameter Hardening]
**Vulnerability:** Public API endpoints allowed users to override the `model` and `system_prompt` parameters, exposing the application to cost-exhaustion attacks and prompt injection.
**Learning:** Defaulting to permissive schemas for LLM-powered features can lead to "Denial of Wallet" and safety bypasses.
**Prevention:** Strictly define Pydantic schemas for LLM requests, excluding internal parameters like `model` or `system_prompt`. Always enforce these values in the backend logic using a centralized configuration (`Settings`).
