## 2026-05-13 - [Keyboard Visibility for Hover-Only Elements]
**Learning:** Interactive elements that only appear on hover (e.g., 'opacity-0 group-hover:opacity-100') are inaccessible to keyboard users unless they also include 'focus-visible:opacity-100'.
**Action:** Always pair 'group-hover:opacity-100' with 'focus-visible:opacity-100' and ensure standard focus ring styles are applied to ensure visibility during keyboard navigation.

## 2026-05-13 - [Safe Deletion UX]
**Learning:** Destructive actions should always require a secondary confirmation, especially when the action is irreversible. Using an 'AlertDialog' provides a consistent and safe pattern for this.
**Action:** Implement 'AlertDialog' for any irreversible data removal (like document or history deletion) to prevent accidental data loss and maintain UX consistency across the app.
