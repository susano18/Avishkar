## 2026-06-06 - [Delete Confirmation UI Pattern]
**Learning:** Destructive actions like document deletion should always be wrapped in a confirmation dialog to prevent accidental data loss. Using Radix UI's `AlertDialog` ensures that focus is trapped correctly and the interaction is keyboard-accessible.
**Action:** Always implement `AlertDialog` for delete operations. Ensure trigger buttons have descriptive `aria-label` attributes and the dialog content explicitly names the object being deleted for clarity.

## 2026-06-06 - [Type Safety in Paginated Lists]
**Learning:** Using `any` in component state for API data (like `docs`) bypasses TypeScript's benefits and can lead to runtime errors during UI rendering. Defining a shared `DocumentMetadata` interface improves developer experience and prevents common bugs like accessing undefined properties on document objects.
**Action:** Define interfaces for all API response objects instead of using `any`.
