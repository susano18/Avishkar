# Palette Journal - UX & Accessibility Learnings

## 2025-05-15 - [Initial Entry]
**Learning:** Initializing the UX journal to track critical UX and accessibility improvements.
**Action:** Follow the specified format for all future entries.

## 2026-06-11 - [Accessible Icon Buttons]
**Learning:** When using `opacity-0 group-hover:opacity-100` for secondary actions (like delete buttons) to reduce visual noise, keyboard users cannot see the button when they tab to it.
**Action:** Always include `focus-visible:opacity-100` alongside `opacity-0` so the button becomes visible when focused via keyboard.
