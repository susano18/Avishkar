# Palette Journal

## 2025-05-14 - Consistency in Destructive Actions
**Learning:** Destructive actions like document deletion should always have a confirmation step to prevent accidental loss of data, especially when the UI uses hover-only triggers which can be prone to misclicks.
**Action:** Use `AlertDialog` for all delete operations and ensure they are keyboard accessible with `focus-visible` styles.
