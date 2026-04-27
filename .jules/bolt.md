## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2026-04-27 - Database-level length computation and column exclusion
**Learning:** For listing endpoints where only metadata is needed, computing the length of large text fields (like `extracted_text`) at the database level using `func.length` and excluding the actual content significantly reduces payload size and bandwidth usage. This is more efficient than transferring the full text and computing length in the frontend.
**Action:** Use database-level aggregations and column selection for summary listings. If schema compatibility is required, return `None` for the large field instead of deleting it to avoid breaking changes.
