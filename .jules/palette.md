# Palette's Journal - Critical UX & Accessibility Learnings

This journal documents critical UX and accessibility learnings discovered during development.

## 2025-05-02 - Keyboard Accessibility for Hover-only Actions
**Learning:** Interactive elements with conditional visibility (e.g., `opacity-0 group-hover:opacity-100`) are invisible and inaccessible to keyboard users unless they also include `focus-visible` utility classes.
**Action:** Always include `focus-visible:opacity-100` and appropriate focus ring styles when using hover-triggered visibility for interactive elements.
