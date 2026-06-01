## 2025-05-15 - [Copy to Clipboard Feedback Pattern]
**Learning:** For asynchronous or transient operations like "Copy to Clipboard," providing immediate visual feedback by toggling both the icon and text (e.g., from `Copy` to `Check`/`Copied`) for a short duration (2 seconds) significantly improves user confidence in the action's success.

**Action:** Always implement the "toggled feedback" pattern for copy buttons using a transient state and `useEffect` for automatic reset. Use ARIA labels to ensure accessibility during the state change.
