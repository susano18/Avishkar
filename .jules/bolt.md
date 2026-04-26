## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2025-05-15 - Use composite indexes for paginated list queries
**Learning:** Queries that filter by one column (e.g., `user_id`) and sort by another (e.g., `created_at`) benefit significantly from composite indexes. Without them, the database may perform a full scan of the filtered results and then an in-memory sort, which slows down as data grows.
**Action:** When implementing paginated lists with filtering and sorting, always consider adding a composite index covering both the filter and sort columns to ensure O(log N) retrieval.
