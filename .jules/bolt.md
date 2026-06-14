## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2026-06-14 - Optimize large text fields in list endpoints
**Learning:** Loading large text/blob columns in paginated list endpoints significantly increases database I/O, backend memory usage, and network payload size. Using SQLAlchemy's `defer()` for large columns and providing a computed `column_property` (e.g., `extracted_text_length`) allows the frontend to display metadata without the overhead of transferring full text content.
**Action:** Use `defer()` for large text fields in all list/paginated endpoints and provide lightweight metadata via computed properties when needed.
