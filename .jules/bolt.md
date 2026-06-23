## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2026-06-23 - Use SQLAlchemy `defer` and `column_property` for large blobs
**Learning:** For models with large text/blob columns, using `defer()` in list queries and providing a pre-calculated `column_property` (e.g., `func.length`) significantly reduces database I/O and network payload size (99.7% reduction in our test case) while still providing necessary metadata to the UI.
**Action:** When designing list endpoints for models with potentially large fields, always default to a slim response schema and defer loading of the heavy columns.
