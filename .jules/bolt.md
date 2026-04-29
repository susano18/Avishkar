## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2025-05-15 - Optimize list payload with func.length
**Learning:** Fetching large text blobs in list endpoints significantly increases database I/O and network latency. Using SQLAlchemy's `func.length()` allows the frontend to display character counts without the overhead of transferring the full text.
**Action:** For all list-based API endpoints, explicitly select only the necessary columns and use database-level functions for metadata (like length) to minimize payload size.
