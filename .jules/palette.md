## 2026-05-20 - Accessible hover-only actions
**Learning:** Card-based UI patterns that hide actions until hover (using `opacity-0`) are inaccessible to keyboard and screen reader users unless paired with `focus-visible` visibility and explicit ARIA labels.
**Action:** Always ensure that any action hidden with `opacity-0` includes `focus-visible:opacity-100`, a standard focus ring, and an `aria-label` for icon-only buttons.
