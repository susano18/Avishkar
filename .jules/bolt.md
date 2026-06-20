## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2025-05-15 - Defer large text blobs in list views
**Learning:** Fetching full text blobs (like `extracted_text`) in list endpoints (like `/documents`) creates significant overhead in database I/O, server memory, and network bandwidth. Using SQLAlchemy's `column_property` with `func.length` allows for metadata display (like character count) without loading the full blob, and `defer()` ensures the blob is only fetched when explicitly needed.
**Action:** Always use `defer()` and `column_property` for large columns in list endpoints to optimize performance and reduce payload size.
