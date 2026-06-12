## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2024-06-12 - Defer large columns and use column_property for metadata
**Learning:** Fetching large text fields (like `extracted_text`) in paginated list endpoints causes massive network overhead and slow database I/O. SQLAlchemy's `defer()` allows skipping these columns in queries. Additionally, using `column_property` with `func.length` computes metadata at the database level, which is significantly faster and more efficient than calculating it in the application layer after fetching the full data.
**Action:** In list endpoints, always defer large text/blob columns and use database-level computed properties for any required metadata to minimize payload size and processing time.
