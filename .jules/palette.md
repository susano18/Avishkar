## 2025-05-15 - [Delete Confirmation for Documents]
**Learning:** Destructive actions like document deletion should always be protected by a confirmation dialog to prevent accidental data loss. Using 'focus-visible' and 'aria-label' ensures these actions are accessible to keyboard and screen reader users.
**Action:** Always implement Radix 'AlertDialog' or similar for destructive UI actions, and ensure conditional visibility elements are focusable.
