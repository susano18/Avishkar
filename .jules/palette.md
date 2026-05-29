## 2025-05-29 - Form Accessibility and Output Interaction
**Learning:** When a heading element also serves as a visible label for a form control, use the nested pattern `<h2><label htmlFor={id}>{label}</label></h2>` to maintain semantic document structure while satisfying accessibility requirements.
**Action:** Always associate headings used as labels with their respective inputs using `useId` and `htmlFor`.

**Learning:** Apply `role="status"` and `aria-label="Loading content"` to loading skeleton containers (like `SkeletonLines`) to inform screen readers of asynchronous UI updates.
**Action:** Consistently use ARIA status roles for skeleton loaders to provide a comparable experience for screen reader users.
