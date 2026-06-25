## 2025-05-15 - [Interactive element visibility]
**Learning:** Interactive elements using the `opacity-0 group-hover:opacity-100` pattern (common for delete buttons in lists) are invisible to keyboard-only users who navigate via Tab.
**Action:** Always include `focus-visible:opacity-100` alongside `group-hover:opacity-100` to ensure accessibility and visibility for keyboard-only users.
