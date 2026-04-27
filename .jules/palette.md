# Palette's Journal - Critical UX/Accessibility Learnings

## 2026-04-27 - [Consistency in Destructive Actions]
**Learning:** Destructive actions like deletion should consistently provide a confirmation step and be accessible via keyboard, not just hover. Using Radix UI's AlertDialog ensures a consistent and accessible experience across different parts of the application (e.g., History vs. Library).
**Action:** Always wrap delete buttons in a confirmation dialog and ensure they are visible on focus if they are hidden on hover by default.
