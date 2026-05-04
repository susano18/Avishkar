## 2025-03-24 - [Accessible Destructive Actions]
**Learning:** Destructive actions (like deletion) hidden behind hover states (opacity-0) are inaccessible to keyboard users unless explicitly handled with focus-visible states. Confirmation dialogs (AlertDialog) are essential for safety but must be correctly triggered via `asChild` to maintain valid DOM structure.
**Action:** Always pair `group-hover:opacity-100` with `focus-visible:opacity-100` and use standard `AlertDialog` patterns for all destructive actions in this codebase.
