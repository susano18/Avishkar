## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2026-06-05 - Use SQLAlchemy defer() and column_property for metadata
**Learning:** For entities with large blob/text columns (like extracted document text), loading them during list operations creates significant database memory pressure and network overhead. Using SQLAlchemy's `defer()` to skip these columns in list queries, combined with a `column_property` to calculate metadata (like length) at the DB level, optimizes both I/O and payload size.
**Action:** Always defer large columns in paginated list endpoints and provide pre-computed metadata properties for UI needs.
