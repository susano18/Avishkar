## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2025-05-31 - Payload reduction via column deferral and server-side calculation
**Learning:** For listing endpoints, transferring large text columns that aren't displayed in the list view is a massive waste of bandwidth and I/O. Using SQLAlchemy's `defer()` on the column and calculating derived data (like string length) on the database side using `column_property` and `func.length()` significantly reduces API latency and payload size.
**Action:** Always use `defer()` for large text/binary columns in listing endpoints and prefer database-side calculations for metadata about those columns.
