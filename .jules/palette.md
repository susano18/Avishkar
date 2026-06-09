## 2026-06-09 - Accessible Destructive Actions in Hover-States

**Learning:** Interactive elements hidden via `opacity-0` (common in "hover-to-reveal" patterns) are completely invisible to keyboard users when they receive focus. Additionally, destructive actions without confirmation create high anxiety and potential for data loss in minimalist interfaces.

**Action:** Always pair `group-hover:opacity-100` with `focus-visible:opacity-100` and standard focus rings. Every destructive action (e.g., Delete) must be gated by a confirmation dialog (like `AlertDialog`) that explicitly names the item being deleted.
