## 2023-10-27 - [Pattern] Accessible conditional visibility
**Learning:** Interactive elements that only appear on hover (like 'group-hover:opacity-100') are inaccessible to keyboard users unless they also include 'focus-visible' visibility states.
**Action:** Always pair 'group-hover:opacity-100' with 'focus-visible:opacity-100' and ensure standard focus rings are applied to these elements.

## 2023-10-27 - [UX] Confirmation for destructive actions
**Learning:** Providing confirmation dialogs for destructive actions like document deletion improves user confidence and prevents accidental data loss. Consistency across routes (Library vs History) is key for a predictable UX.
**Action:** Use AlertDialog components for all destructive actions. Ensure the description explicitly names the item being deleted for clarity.
