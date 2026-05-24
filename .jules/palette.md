## 2025-05-15 - Form Accessibility Pattern
**Learning:** Found a pattern where custom InputPanel components and standard login forms lacked proper label-to-input association and visible focus indicators. Heading elements were used visually as labels but not semantically connected to their respective controls.
**Action:** Always use 'useId' for unique identifiers in reusable components and ensure labels are correctly associated with their inputs using 'htmlFor'. Maintain semantic heading hierarchy while adding label functionality by nesting: '<h2><label htmlFor={id}>{label}</label></h2>'.
