## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.
## 2026-05-03 - Optimize list payloads by excluding large text blobs
**Learning:** Returning large text content in list endpoints that the UI only uses for metadata (like character counts) creates a massive network and memory bottleneck. Using database-side functions like `func.length` to fetch only the required metadata can reduce payload sizes by orders of magnitude.
**Action:** Always audit list endpoints for "big blob" fields and move metadata calculations to the database when the full content isn't immediately required by the frontend.
