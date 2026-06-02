## 2026-06-02 - [Information Leakage via Internal Exceptions]
**Vulnerability:** The `upload_document` endpoint was returning raw exception messages to the client when file saving failed. This could expose internal server details like file paths, OS errors, or storage architecture.
**Learning:** Catching broad exceptions and returning them directly in an `HTTPException` detail field is a common source of information leakage. While helpful for debugging, these details should only be logged internally.
**Prevention:** Always catch exceptions in sensitive operations and return a generic, non-descriptive error message to the client. Use a structured logger to record the full error context internally for troubleshooting.
