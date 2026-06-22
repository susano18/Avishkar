## 2025-05-15 - [Improving Deletion Experience and Accessibility]
**Learning:** Using `opacity-0 group-hover:opacity-100` for actions is a common UX pattern but hides actions from keyboard-only users unless `focus-visible:opacity-100` is also applied. Destructive actions should always have a confirmation step to prevent accidental data loss.
**Action:** Always pair `group-hover:opacity-100` with `focus-visible:opacity-100` for interactive elements and implement `AlertDialog` or similar confirmation patterns for destructive actions.
