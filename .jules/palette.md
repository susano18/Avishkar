## 2026-06-26 - [Library Deletion Confirmation]
**Learning:** Destructive actions like document deletion should always be guarded by a confirmation dialog to prevent accidental data loss. This also provides an opportunity to display the specific item being deleted, increasing user confidence.
**Action:** Always wrap delete buttons in an `AlertDialog` and include the item name in the description.
