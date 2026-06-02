## 2026-06-02 - Immediate feedback for copy and accessible skeletons
**Learning:** For async copy operations, provide immediate visual feedback by toggling the button icon and text for a short duration (e.g., 2 seconds) to confirm the action succeeded. Additionally, apply `role="status"` and `aria-label="Loading content"` to loading skeleton containers to inform screen readers of asynchronous UI updates.
**Action:** Always implement temporary visual state changes for copy buttons and ensure loading states are announced to screen readers using appropriate ARIA roles.
