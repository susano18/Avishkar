## 2025-05-15 - [Consistency in Destructive Actions]
**Learning:** Destructive actions like deleting documents should always have a confirmation step to prevent accidental data loss. Using established UI patterns like `AlertDialog` provides a familiar and safe experience.
**Action:** When adding delete functionality, always include a confirmation dialog and ensure the trigger is accessible to keyboard users by providing visible focus states.
