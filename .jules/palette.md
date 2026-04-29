## 2025-05-15 - [Keyboard Visibility for Hover-Only Actions]
**Learning:** Interactive elements that are hidden by default and only revealed on hover (e.g., using `group-hover:opacity-100`) are inaccessible to keyboard users unless they also have `focus-visible` classes to reveal them when focused.
**Action:** Always pair `group-hover:opacity-100` with `focus-visible:opacity-100` and ensure a clear focus ring is present.
