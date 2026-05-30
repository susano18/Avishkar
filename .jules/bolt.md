## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2025-05-30 - Optimize large text listings with defer() and column_property
**Learning:** Returning large text blobs (like extracted document content) in listing endpoints causes massive performance degradation in database I/O and network payload. Using SQLAlchemy's `defer()` to skip the large column and `column_property(func.length(...))` to provide metadata instead is highly efficient.
**Action:** Always defer large text or binary columns in list views and use server-side length calculations for UI metadata.
