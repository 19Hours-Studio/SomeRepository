=== TOURNAMENT ===
PAIR 1 | WINNER A | A is exact-output and client-only with margin 0.85 and gain 1.22; B's margin is 0.46 (m near 25% vs the 12% needed), and it only works self-hosted.
PAIR 2 | WINNER B | B has the larger whole-chain gain (1.64 vs 1.21) and a stable margin 0.53 vs A's unstable 0.9, and its compute headroom on reordered content is real, with an exact fallback.
PAIR 3 | WINNER A | A has gain 1.8 and clears 1.5x, with canonical ordering turning most reorders into exact hits; B's gain is 1.14 and its margin is unstable (0.38–0.9).
PAIR 4 | WINNER B | B covers middle edits with an exact RoPE shift and a fallback, giving a plausible 1.1–1.45x overall; A fails on PCIe bandwidth by 5–10x and falls back to about 1.16x.
PAIR 5 | WINNER A | A's gain is 1.36 vs 1.16 and it never loses money; B's single breakpoint misses shallow shared prefixes and does no better than plain always-write at ≥100 requests per 5 minutes.