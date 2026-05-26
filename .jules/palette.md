## 2025-05-15 - Accessible Heading-Labels with useId
**Learning:** In React 19, use the `useId` hook to generate unique IDs for linking form controls (like `textarea`) to their labels. When a heading (`<h2>`) also serves as a visible label, nesting the `label` element inside the heading maintains semantic document structure while providing full accessibility for both screen readers and pointer users.
**Action:** Always use `useId` for dynamic form elements and ensure interactive elements have clear `focus-visible` states.
