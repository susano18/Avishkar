## 2026-05-07 - Document Deletion Confirmation & Keyboard Visibility
**Learning:** Interactive elements with conditional visibility (e.g., 'opacity-0 group-hover:opacity-100') must include 'focus-visible:opacity-100' and standard focus ring styles to ensure they are accessible to keyboard users. Confirmation dialogs for destructive actions provide a safety net and match established application patterns.
**Action:** Always include 'focus-visible' styles for hover-only buttons and use 'AlertDialog' for delete actions.
