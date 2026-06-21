## 2025-06-21 - Standardizing destructive actions with AlertDialog
**Learning:** Consistent usage of `AlertDialog` for destructive actions (like deleting documents or history) provides a safe and familiar experience for users. Additionally, using `focus-visible` ensures that elements hidden by default (e.g., `opacity-0`) remain accessible to keyboard-only users.
**Action:** Always check for `opacity-0 group-hover:opacity-100` patterns and ensure `focus-visible:opacity-100` is included. Reuse the `AlertDialog` pattern for all permanent deletion tasks.
