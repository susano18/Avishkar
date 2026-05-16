## 2025-05-16 - Prevent accidental data loss with AlertDialog
**Learning:** Destructive actions (like document deletion) should use an 'AlertDialog' for confirmation to prevent accidental data loss and ensure UX consistency across routes (e.g., library and history).
**Action:** Always wrap delete buttons in an `AlertDialog` and use `e.stopPropagation()` on the trigger and content if nested within other interactive elements.

## 2025-05-16 - Ensure visibility of conditional elements for keyboard users
**Learning:** Interactive elements with conditional visibility (e.g., 'opacity-0 group-hover:opacity-100') must include 'focus-visible:opacity-100' and standard focus ring styles to ensure they are visible and accessible to keyboard users.
**Action:** Apply 'focus-visible:opacity-100 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring' to any elements that use group-hover for visibility.
