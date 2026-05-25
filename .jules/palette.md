# Palette's Journal - CodeLens

## 2025-05-14 - Interactive elements hidden until hover
**Learning:** Interactive elements styled with `opacity-0` (often used in 'hidden until hover' card patterns) must include `focus-visible:opacity-100` and standard focus ring utilities (e.g., `focus-visible:ring-1 focus-visible:ring-ring outline-none`) to ensure keyboard users can discover and interact with them.
**Action:** Always include focus states and visibility on focus for elements that are hidden by default.
