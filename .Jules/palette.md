## 2025-04-26 - [Accessibility & Safety for Destructive Actions]
**Learning:** Destructive actions like document deletion should always be protected by a confirmation dialog to prevent accidental data loss. Furthermore, icon-only buttons with conditional visibility (e.g., `opacity-0 group-hover:opacity-100`) must be made focus-visible for keyboard accessibility.
**Action:** Use `AlertDialog` for confirmation of destructive actions and ensure `focus-visible` classes are applied to conditionally visible interactive elements.
