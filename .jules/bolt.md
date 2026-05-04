## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2025-05-15 - Optimize list API payloads by deferring heavy columns
**Learning:** Transferring large text blobs in list views creates massive network overhead. Using DB-side length calculations (e.g., `func.length`) and excluding the full text reduced the payload by 99.7% in this application (from ~1.9MB to ~5KB for 20 documents).
**Action:** For list endpoints, only select necessary metadata and use database functions for aggregate data or lengths instead of sending full content.
