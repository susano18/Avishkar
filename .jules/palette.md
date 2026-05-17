## 2025-05-14 - Interactive focus visibility for 'hidden' actions
**Learning:** Interactive elements with conditional visibility (like 'opacity-0 group-hover:opacity-100') are invisible to keyboard users unless they also have 'focus-visible:opacity-100'. Without this, a user tabbing through the page might land on an invisible button.
**Action:** Always include 'focus-visible:opacity-100' and standard focus ring utilities when using hover-triggered visibility for buttons.
