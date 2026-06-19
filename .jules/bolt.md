## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2025-05-15 - Optimize large text listings with SQLAlchemy defer and column_property
**Learning:** Fetching and transmitting large text columns (like `extracted_text`) in list views can cause significant performance bottlenecks in database I/O and network latency. Using SQLAlchemy's `defer()` to skip loading the large column, combined with a `column_property` using `func.length()` for metadata, allows the database to provide necessary summaries without the heavy payload.
**Action:** Use slim response schemas and SQLAlchemy `defer` for list endpoints that involve large text or binary data.
