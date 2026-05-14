## 2025-05-15 - Accessible conditional visibility for interactive elements
**Learning:** Interactive elements that use `opacity-0 group-hover:opacity-100` for "reveal on hover" patterns are invisible and thus unusable for keyboard users.
**Action:** Always include `focus-visible:opacity-100` alongside `group-hover:opacity-100` and ensure standard focus ring styles are present to maintain accessibility for keyboard navigation.

## 2025-05-15 - Consistency in destructive actions
**Learning:** Inconsistent patterns for destructive actions (e.g., immediate delete vs. confirmation dialog) across different routes (Library vs. History) creates user uncertainty and increases risk of data loss.
**Action:** Use `AlertDialog` for all destructive actions to ensure safety and maintain UX consistency across the application.
