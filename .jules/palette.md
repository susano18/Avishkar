## 2026-06-07 - Accessible Visibility for Hover-Only Actions

**Learning:** Interactive elements that are only visible on hover (e.g., using Tailwind's `opacity-0 group-hover:opacity-100`) are inaccessible to keyboard users as they remain hidden even when receiving focus.

**Action:** Always pair hover-triggered visibility with focus-triggered visibility using `focus-visible:opacity-100`. This ensures that keyboard users can identify and interact with these elements when they tab to them.
