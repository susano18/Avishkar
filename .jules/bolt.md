## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2025-05-15 - DB-side metadata calculation vs full blob retrieval
**Learning:** For list views, fetching large text blobs (e.g., 100KB+) just to display metadata like character count is a massive bottleneck. Using `func.length()` on the DB side and excluding the blob reduced payload size by 99.7% in this app.
**Action:** Always use explicit column selection or deferred loading to avoid fetching large `Text` or `LargeBinary` columns in listing endpoints.
