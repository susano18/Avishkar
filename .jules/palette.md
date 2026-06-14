# Palette Journal

## 2025-05-15 - Improving keyboard accessibility for hover-only actions
**Learning:** Using `opacity-0 group-hover:opacity-100` for action buttons (like delete) makes them invisible to keyboard users even when they have focus. This creates a confusing "hidden focus" state.
**Action:** Always pair `group-hover:opacity-100` with `focus-visible:opacity-100` (or similar focus states) to ensure interactive elements become visible when navigated via keyboard.
