## 2025-05-14 - Confirmation for Destructive Actions in Library
**Learning:** Destructive actions like document deletion should always have a confirmation step to prevent accidental data loss, especially when the delete button is only visible on hover, making it prone to misclicks. Aligning this with other routes (like history) provides a more cohesive UX.
**Action:** Always use `AlertDialog` for deletion or other destructive operations. Ensure icon-only buttons have `aria-label` and are visible on focus (`focus-visible:opacity-100`) for keyboard accessibility.
