## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2026-06-13 - Optimize paginated lists by deferring large text columns
**Learning:** Returning large text/blob columns in paginated list endpoints significantly increases network payload and database I/O. Using SQLAlchemy's `defer()` and a computed `column_property` for metadata allows the frontend to show summaries without loading the full content.
**Action:** Always use slim response schemas for listing endpoints and defer large columns when they are not strictly needed for the initial view.
