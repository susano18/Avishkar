## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2025-05-15 - Optimize Large Text Lists with Defer and Slim Schemas
**Learning:** Loading and transferring large text fields in "list" endpoints creates a massive performance bottleneck in both database I/O and network transfer. Using SQLAlchemy's `defer()` to skip loading these columns and a `column_property` with `func.length()` allows fetching only the necessary metadata while keeping the payload small.
**Action:** Implement slim response schemas and deferred loading for any entity listing that involves large content fields (e.g., extracted text, logs, or blobs).
