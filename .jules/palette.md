## 2025-05-14 - Interactive elements hidden by default

**Learning:** When using Tailwind's `opacity-0 group-hover:opacity-100` to hide interactive elements until hover, they remain invisible and difficult to find for keyboard-only users.
**Action:** Always pair `group-hover:opacity-100` with `focus-visible:opacity-100` on the element itself (or its parent if appropriate) to ensure it appears when focused via Tab.
