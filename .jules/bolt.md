## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2026-06-26 - Optimize document listing with defer and column_property
**Learning:** Fetching large Text columns in list endpoints significantly bloats JSON payloads and increases database I/O. Using SQLAlchemy's `defer` to skip these columns and `column_property` with `func.length` to pre-calculate metadata at the database level provides a major performance boost without losing essential summary information.
**Action:** For any model with large blob or text fields, always use a "Slim" response schema for list endpoints and defer the large columns. Use database functions via `column_property` for lightweight metadata.
