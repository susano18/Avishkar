## 2025-05-05 - Interactive elements with conditional visibility
**Learning:** Interactive elements that are only visible on hover (e.g., 'opacity-0 group-hover:opacity-100') are inaccessible to keyboard users unless they also include 'focus-visible' visibility classes.
**Action:** Always include 'focus-visible:opacity-100' along with standard focus ring styles for buttons that use hover-based visibility patterns.

## 2025-05-05 - Consistency in destructive actions
**Learning:** Destructive actions like document deletion should always have a confirmation step to prevent accidental data loss, especially when the action is triggered by a small, easily-clickable icon.
**Action:** Use Radix 'AlertDialog' for confirmation dialogs to maintain a consistent UX pattern across the application (e.g., matching the history deletion flow).
