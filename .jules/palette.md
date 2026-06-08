## 2025-05-15 - Improving Keyboard Accessibility for Hidden Actions
**Learning:** Actions that are only visible on hover (e.g., `opacity-0 group-hover:opacity-100`) are completely invisible and often unreachable for keyboard-only users unless explicitly handled.
**Action:** Always include `focus-visible:opacity-100` or a similar class when using hover-to-reveal patterns to ensure interactive elements are discoverable during tab navigation.
