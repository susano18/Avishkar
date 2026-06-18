## 2025-05-15 - Interactive Visibility and Keyboard Navigation
**Learning:** Elements hidden with `opacity-0` and revealed via `group-hover:opacity-100` are invisible to keyboard users even when focused.
**Action:** Always pair `group-hover:opacity-100` with `focus-visible:opacity-100` on interactive elements to ensure visibility during tab navigation.
