## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2025-05-14 - Optimize large column loading in lists
**Learning:** Loading large text columns (like `extracted_text`) in paginated list endpoints causes exponential increases in memory usage and network payload size as the library grows.
**Action:** Use SQLAlchemy's `defer()` to skip large columns in lists, and provide metadata (like character counts) via `column_property` calculated at the database level.
