## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2025-05-15 - Optimize large text blobs in list APIs
**Learning:** Returning large text fields (like `extracted_text`) in a paginated list endpoint creates massive network payloads and database overhead. Offloading the character count calculation to the database using `func.length()` and explicitly omitting the text content in the list view significantly reduces latency and bandwidth.
**Action:** Use projected queries (SQLAlchemy `.select()`) for list endpoints to fetch only metadata, and use database functions for aggregate or metadata-only calculations on large columns.
