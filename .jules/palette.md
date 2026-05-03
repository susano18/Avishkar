## 2025-05-15 - [Accessible Conditional Visibility]
**Learning:** Components using Tailwind's 'group-hover:opacity-100' for actions (like delete buttons) are invisible to keyboard users unless 'focus-visible:opacity-100' is also applied.
**Action:** Always pair 'group-hover' visibility toggles with 'focus-visible' counterparts and ensure 'outline-none' is managed by 'focus-visible:ring' for consistent focus indicators.
