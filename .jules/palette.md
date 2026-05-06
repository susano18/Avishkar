# Palette Journal

## 2025-05-14 - [Initial Entry]
**Learning:** Initializing palette journal to track UX and accessibility improvements.
**Action:** Always check for destructive actions without confirmation and hidden interactive elements that lack focus-visible states.

## 2025-05-14 - [Hidden Interactive Elements]
**Learning:** Interactive elements with conditional visibility (e.g., 'opacity-0 group-hover:opacity-100') must include 'focus-visible:opacity-100' and standard focus ring styles to ensure they are visible and accessible to keyboard users.
**Action:** Always pair hover-based visibility with focus-visible visibility and focus indicators.
