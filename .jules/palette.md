## 2025-05-14 - Accessible Hover Actions
**Learning:** Interactive elements that use Tailwind's `opacity-0 group-hover:opacity-100` pattern (like delete buttons) are invisible to keyboard users even when focused.
**Action:** Always include `focus-visible:opacity-100` alongside `group-hover:opacity-100` to ensure visibility and accessibility for keyboard navigation.
