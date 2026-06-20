## 2026-06-20 - Keyboard Visibility for Hover-Triggered Actions

**Learning:** Interactive elements (like delete buttons) that use Tailwind's `opacity-0 group-hover:opacity-100` pattern for a "clean" UI are completely inaccessible to keyboard users because they remain invisible even when focused.

**Action:** Always include `focus-visible:opacity-100` alongside `group-hover:opacity-100` for any interactive element that is hidden by default. This ensures the element becomes visible to sighted keyboard users when they tab to it.
