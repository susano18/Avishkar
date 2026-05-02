## 2025-05-14 - Cache OpenAI client for connection pooling
**Learning:** Reusing the `OpenAI` client instance (and thus its underlying `httpx` client) enables HTTP connection pooling. This significantly reduces latency for subsequent API calls by avoiding redundant TCP and TLS handshakes.
**Action:** Always use a singleton or cached client instance when working with the OpenAI SDK or other HTTP-based service clients to maintain connection efficiency.

## 2025-05-24 - Database-side length calculation for large fields
**Learning:** Calculating field lengths on the database side (e.g., `func.length(Document.extracted_text)`) and selecting specific columns instead of full ORM objects prevents transferring large text blobs over the network. This drastically reduces API payload size and improves response times for list endpoints.
**Action:** Use specific column selection and DB-side aggregations for summary/list views where large content fields are not immediately required by the UI.
