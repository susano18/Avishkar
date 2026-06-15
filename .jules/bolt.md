## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2025-06-15 - Defer large text columns in listing endpoints
**Learning:** Fetching large text fields (like `extracted_text`) in paginated list views creates massive JSON payloads and unnecessary database I/O. Using SQLAlchemy's `defer()` combined with a `column_property` for metadata (like `extracted_text_length`) allows the UI to show necessary info without the performance penalty of loading the full content.
**Action:** Always use `defer()` for large columns in list endpoints and provide lightweight metadata properties for the frontend.
