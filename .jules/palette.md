## 2025-05-15 - Improving destructive action safety and keyboard discoverability
**Learning:** Interactive elements hidden until hover (opacity-0) are invisible to keyboard users unless they have explicit focus-visible styles (e.g., focus-visible:opacity-100). Additionally, destructive actions like deletion should use AlertDialogs to prevent accidental data loss and maintain UX consistency.
**Action:** Always include focus-visible styles on hover-revealed elements and wrap destructive triggers in confirmation dialogs.
