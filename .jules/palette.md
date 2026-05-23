## 2026-05-23 - [Keyboard Discoverability for Hover-Only Actions]
**Learning:** Interactive elements that use `opacity-0` (hidden until hover) are completely invisible to keyboard users even when they have focus, unless specifically handled with `focus-visible:opacity-100`.
**Action:** Always pair `opacity-0` with `focus-visible:opacity-100` and a clear focus ring to ensure all users can discover and interact with the element.
