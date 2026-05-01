## 2025-05-15 - Interactive Elements with Conditional Visibility
**Learning:** Interactive elements like deletion buttons that use 'opacity-0 group-hover:opacity-100' are inaccessible to keyboard users because they remain invisible even when focused.
**Action:** Always include 'focus-visible:opacity-100' or similar classes to ensure interactive elements are visible when they receive keyboard focus.
