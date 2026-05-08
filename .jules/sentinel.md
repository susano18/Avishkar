## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-05-08 - [LLM Prompt Injection via API Overrides]
**Vulnerability:** The `/process-text` endpoint allowed users to provide their own `system_prompt` and `model`, which could be used to bypass intended application constraints or abuse expensive LLM resources.
**Learning:** Externalizing LLM configuration parameters to client-side requests without strict validation or hardcoded bounds creates a significant surface for prompt injection and resource abuse.
**Prevention:** Hardcode sensitive LLM parameters (like system prompts and allowed models) on the backend or use strict server-side allow-lists. Remove these fields from public-facing request schemas.
