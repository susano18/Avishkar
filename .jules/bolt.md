## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2025-05-15 - Optimize document list by deferring large text blobs
**Learning:** Loading large `Text` columns (like `extracted_text`) during paginated list queries significantly increases database I/O and network payload size, especially when the frontend only needs metadata or the content length. Calculating the length in the database using `func.length` is much more efficient.
**Action:** In list endpoints, explicitly select only metadata columns and use database-native functions for aggregations or length checks to minimize payload size and memory usage.
