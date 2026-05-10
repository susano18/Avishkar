## 2025-05-15 - [Keyboard visibility for hover-only actions]
**Learning:** Interactive elements that only appear on hover (e.g., using `group-hover:opacity-100`) are inaccessible to keyboard users unless they also have `focus-visible:opacity-100`.
**Action:** Always pair `group-hover:opacity-100` with `focus-visible:opacity-100` and standard focus ring styles to ensure accessibility.
