## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2025-05-15 - Defer large text columns in list views
**Learning:** Loading large `Text` columns (like `extracted_text`) in paginated list views significantly increases database I/O and API payload size.
**Action:** Use SQLAlchemy's `defer()` for heavy columns in list endpoints and provide a server-side `column_property` (e.g., `func.length()`) if the metadata is needed for the UI.
