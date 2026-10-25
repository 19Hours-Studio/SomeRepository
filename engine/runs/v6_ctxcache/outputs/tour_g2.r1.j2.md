=== TOURNAMENT ===
PAIR 1 | WINNER B | B's margin (0.85) is much nearer 1 than A's (0.46), and its output is exact and it works client-side, while A's 1.39x rests on an unmeasured probe recall.
PAIR 2 | WINNER A | Both are wounded, but A's 1.64x gain is well above B's 1.21x, and A covers reordering, moved tool outputs and insertions, where B only cuts rewrites after expiry.
PAIR 3 | WINNER B | B's whole-chain gain of 1.8x clears 1.5x and covers reordered RAG sets, while A's diff encoding tops out near 1.14x; B's quality margin (0.4) is weaker but the cost difference decides it.
PAIR 4 | WINNER A | A directly handles middle edits and insertions with a sound mechanism (about 1.1–1.45x system-wide), while B's CPU/SSD page fetch fails on PCIe bandwidth and falls back to a gain of about 1.16x on decode only.
PAIR 5 | WINNER B | B's 1.36x gain beats A's 1.16x; B never loses money and beats always-write, while A's single-breakpoint gate does no better than always-write at moderate traffic.