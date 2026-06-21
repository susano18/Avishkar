## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2025-06-21 - Optimize Large Column Loading in Lists
**Learning:** Fetching large text/blob columns in list endpoints causes significant latency and payload bloat. Using SQLAlchemy's `deferred()` for large columns and `column_property()` to pre-calculate metadata (like text length) on the database side drastically improves performance.
**Action:** Use `deferred()` for large columns in list views. Provide a "Slim" Pydantic schema for lists and a full schema for detail views, using `.options(undefer(...))` in the detail endpoint to load the large content only when specifically requested.
