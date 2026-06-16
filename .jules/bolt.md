## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2026-06-16 - Defer large text columns in list endpoints
**Learning:** Returning large text blobs (e.g., `extracted_text`) in paginated list endpoints causes massive JSON payloads and unnecessary database I/O. Using SQLAlchemy's `defer()` alongside a `column_property` for metadata (like `length`) drastically improves performance.
**Action:** Always use `defer()` for large columns in list views and provide slim schemas to minimize network overhead.
