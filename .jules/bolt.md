## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2026-06-04 - Defer loading of large text blobs in listings
**Learning:** Fetching large  or  columns in paginated listings causes significant memory and network overhead. Using SQLAlchemy's `defer()` combined with a `column_property` for length calculation allows for lightweight listings while still providing useful metadata.
**Action:** Always use slim schemas and `defer()` for large columns in list endpoints.

## 2026-06-04 - Defer loading of large text blobs in listings
**Learning:** Fetching large Text or Blob columns in paginated listings causes significant memory and network overhead. Using SQLAlchemy's `defer()` combined with a `column_property` for length calculation allows for lightweight listings while still providing useful metadata.
**Action:** Always use slim schemas and `defer()` for large columns in list endpoints.
