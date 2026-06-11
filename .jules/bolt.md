## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2026-06-11 - Deferred Column Loading for Large Text Fields
**Learning:** Returning large text or BLOB columns in paginated list endpoints can lead to significant network overhead and database I/O, even if the UI only needs a summary (like text length). SQLAlchemy's `defer()` combined with a computed `column_property` allows fetching metadata without the heavy payload.
**Action:** Use `defer()` for large text fields in list views and provide optimized metadata fields (like lengths or snippets) via database-level computations.
