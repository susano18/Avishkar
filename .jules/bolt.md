## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2025-05-15 - Optimize list views by omitting large text blobs
**Learning:** Fetching full text content in list views where only metadata (like character count) is displayed creates unnecessary database load and massive network payloads. Calculating length via SQL `func.length()` on the server side is significantly more efficient.
**Action:** For paginated list endpoints, explicitly select only required columns and use database functions for aggregations or property calculations (e.g., string length) instead of transferring raw data and calculating on the client.
