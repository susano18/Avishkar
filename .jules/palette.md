## 2024-05-22 - [Keyboard Discovery for Hidden Actions]
**Learning:** Interactive elements styled with `opacity-0` (common in "hidden until hover" patterns) are invisible to keyboard users even when focused.
**Action:** Always pair `group-hover:opacity-100` with `focus-visible:opacity-100` and provide a clear focus ring to ensure keyboard discoverability.

## 2024-05-22 - [Form Accessibility Gaps]
**Learning:** Labels in login and input forms were missing `htmlFor` association, preventing screen readers from correctly identifying input purpose.
**Action:** Ensure all form labels have `htmlFor` matching the input `id`, even in minimal design systems.
