## 2025-05-15 - [Title]
**Learning:** [UX/a11y insight]
**Action:** [How to apply next time]

## 2025-05-15 - Immediate Feedback for Async Actions
**Learning:** For user actions that involve asynchronous or background processes (like copying to clipboard), providing immediate visual confirmation via icon and text toggling significantly improves the perceived reliability of the interface.
**Action:** Always implement a short-duration (e.g., 2s) "success" state for copy operations and other fire-and-forget interactions.

## 2025-05-15 - Accessible Asynchronous UI Updates
**Learning:** Screen readers often miss content updates that happen via skeletons or partial page re-renders unless explicitly informed via ARIA roles like `status` or `log`.
**Action:** Apply `role="status"` and `aria-label="Loading content"` to loading skeleton containers to ensure screen reader users are aware of ongoing background tasks.
