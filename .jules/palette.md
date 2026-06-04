## 2025-05-14 - Consistency in Destructive Actions
**Learning:** In a dashboard with multiple list-like interfaces (Library and History), inconsistent patterns for destructive actions (like deletion) can lead to user confusion and accidental data loss. One page having a confirmation while another deletes immediately is a jarring experience.
**Action:** When implementing destructive actions, ensure a consistent confirmation pattern (like `AlertDialog`) across all related views.
