I could not run a new replay. My simulation script at `/tmp/claude-0/-home-user-SomeRepository-engine/86b61a25-826d-5e99-8ce4-43b0688ac74a/scratchpad/ka.py` returned no readable output in this session. So every number below is derived from the candidates' own figures and the facts listed, and is labelled as an estimate.

**Shared cost model.** I backed out the document share of the bill, w ≈ 0.68, from Pair 1 A's own figures (1.17x per request at 0.40 reuse, 1.35x at 0.546). Pair 2 A's ratios fit a blended-path cost of about 51.2, an exact-path cost of about 84.7, and a prefix-caching baseline of 83.

**Pair 1.** A gated breakpoint placement removes most of the write premium on long-tail documents. Estimated per-request gain over sending documents uncached:

| Zipf | Before | After (if misses are mostly tail) |
|---|---|---|
| 1.05 | 1.17x | 1.33x |
| 1.2 | 1.35x | 1.50x |
| 1.5 | 1.78x | about 1.9x |

The 1.5x threshold moves from Zipf ≈1.4 to ≈1.2, and the method can no longer lose money at low traffic. This partly removes the weak link.

**Pair 2.** Popularity ordering lowers the exact-path cost from 84.7 to about 74, 70 and 62 at Zipf 1.05, 1.2 and 1.5. At m = 0.25 the ratio rises from 1.39x to 1.46x, 1.49x and 1.55x. The largest m that still gives 1.5x rises from 0.12 to 0.18, 0.22 and 0.38. This removes the weak link only at Zipf ≥ 1.2.

**Pair 3.** The combination does not fix A's weak link. FACT 20 caps per-session keep-alive at 1.08–1.11x on input cost. The best improvement is to apply the hazard rule to org-wide shared document prefixes. The upper bound is lifting FACT 21's low-traffic reuse (0.05–0.42) toward the high-traffic band (0.40–0.77). This is unmeasured.

=== IDEAS ===
IDEA 1
NAME: Reuse-gated single-breakpoint document ordering
MECHANISM: The client orders retrieved documents by an online retrieval-frequency counter, with ties broken by ID. From each document's counter rate λ, it estimates P(reuse within TTL) = 1−e^(−5λ). It places one cache breakpoint after the last document with P > 0.217 (the break-even), and sends the rest after the breakpoint uncached at 1.0x instead of a 1.25x write. Exact prefix KV means output equals full recompute for that order; the reorder effect is tested by F1/EM across order permutations on a real model.
VALUE: Estimated 1.33x, 1.50x and about 1.9x per request at Zipf 1.05, 1.2 and 1.5, client-only through third-party APIs, with one breakpoint and no money-losing writes at low traffic; tail documents still miss, so about 100% hit is out of reach.

IDEA 2
NAME: Popularity-ordered probe-routed KV reuse
MECHANISM: On a self-hosted or provider stack, documents are ordered by global retrieval frequency before lookup. CacheBlend's layer-1 recompute measures cross-chunk key deviation; single-source requests are blended from position-independent chunk KV, and requests above the threshold take the exact prefix path. That exact path now hits the popularity-ordered prefix, cutting its cost from about 84.7 to 62–74 units against an 83-unit prefix-caching baseline.
VALUE: At m = 0.25 routed away, the whole bill falls 1.46–1.55x, and 1.5x holds up to m = 0.18–0.38 instead of 0.12; probe recall still needs testing on 2WikiMQA and MuSiQue against full recompute.

IDEA 3
NAME: Shared-prefix hazard keep-alive
MECHANISM: An org-wide counter gives each popularity-ordered document-prefix path an arrival rate, which serves as the hazard. Before each 5-minute expiry, the client sends a 1-token read of every leaf path whose P(hit before next expiry) × 1.25 > 0.1; one ping serves every user sharing that path. Output is unchanged because only exact prefixes are kept warm.
VALUE: Low-traffic organisations could approach the reuse that only ≥1k requests per window give today (from 0.05–0.42 toward 0.40–0.77), with each ping positive in expected value; the net gain needs a trace replay, and per-session gaps remain capped at about 1.1x.