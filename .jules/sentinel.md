## 2026-04-25 - [Privilege Escalation via Mass Assignment]
**Vulnerability:** The registration endpoint (`/auth/register`) accepted a `role` field in the request body, allowing users to register themselves with any role, including `admin` or `educator`.
**Learning:** Using a single model for both input validation and database representation without filtering sensitive fields can lead to mass assignment vulnerabilities. Pydantic models used for API requests should only include fields that users are explicitly allowed to provide.
**Prevention:** 1) Use dedicated request schemas that exclude sensitive fields like `role`, `is_active`, or `permissions`. 2) Explicitly set sensitive defaults in the application logic rather than relying on request data. 3) Always verify user-provided data against the principle of least privilege.

## 2026-06-03 - [Mocking Read-Only Settings Properties]
**Vulnerability:** Testing file upload limits required mocking the `max_upload_size_bytes` property on the `Settings` object.
**Learning:** Pydantic settings properties are read-only on the instance. Attempting to patch them at the instance level fails. They must be patched at the class level using `unittest.mock.PropertyMock`.
**Prevention:** Use `with patch("app.config.Settings.max_upload_size_bytes", new_callable=PropertyMock) as mock_prop: mock_prop.return_value = 0` for reliable property mocking in security tests.
