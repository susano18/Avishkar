## 2026-05-27 - [Accessible Feedback & Loading States]
**Learning:** Skeleton loaders should be marked with role="status" to inform assistive technologies of ongoing async updates. Visual feedback for clipboard actions (toggling icons/text) provides immediate confirmation that feels faster and more reliable than a toast alone.
**Action:** Always wrap skeleton components in a container with role="status" and use dual-layer feedback (UI change + toast) for high-value micro-interactions.
