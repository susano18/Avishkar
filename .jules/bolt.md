## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2026-06-10 - Defer large text columns in lists
**Learning:** Fetching large text blobs (extracted text) in paginated list views causes significant database I/O and network payload bloat. Using SQLAlchemy's `defer()` combined with a `column_property` for metadata (like text length) allows the UI to remain functional and informative while being significantly faster.
**Action:** Always defer large text or binary columns in list endpoints. Provide slim schemas for these endpoints to ensure the API doesn't inadvertently load deferred columns.
