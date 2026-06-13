## 2025-05-15 - [Consistent Deletion Confirmation & Keyboard Visibility]
**Learning:** Destructive actions (like document deletion) in this application often use a pattern where the action button is hidden until hover (`opacity-0 group-hover:opacity-100`). This creates two issues: accidental deletions due to misclicks and total inaccessibility for keyboard users who cannot "hover".
**Action:** Always wrap destructive actions in an `AlertDialog` confirmation and ensure buttons have `focus-visible:opacity-100` to be discoverable and usable by keyboard-only users.
