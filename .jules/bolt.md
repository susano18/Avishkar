## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2026-06-02 - Optimize list payloads with defer and column_property
**Learning:** For entities with large text fields (like extracted document content), using SQLAlchemy's `defer()` in list queries significantly reduces database I/O and network payload size. Combining this with `column_property` and `func.length()` allows the frontend to show metadata (like character count) without downloading the full content.
**Action:** Always use `defer()` for large columns in listing endpoints and provide server-side calculated metadata via `column_property` when needed for UI summaries.
