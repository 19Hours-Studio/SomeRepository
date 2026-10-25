=== TRIAGE ===
IDEA 1 | I 2 | P 4 | DECIDES: quoted share of answer tokens × anchor-resolution accuracy | Targets output in Archetype B, which has no room for 3x; quotes are rarely ≥35% of answers.
IDEA 2 | I 2 | P 6 | DECIDES: harness-prefix share of all writes | Plausible but small (5–9%), and only the provider can deploy it.
IDEA 3 | I 6 | P 5 | DECIDES: share of requests that become exact hits after canonical ordering | Ordering is cheap and lossless; the remainder inherits CacheBlend's multi-hop and per-model losses (attempt 12).
IDEA 4 | I 6 | P 7 | DECIDES: stale-fact leak rate, journal vs rewrite | Exact, client-only, hits A's write term; ski-rental bound is sound; quality is the open risk.
IDEA 5 | I 4 | P 5 | DECIDES: mean accepted tokens per step at production batch | Covers C's decode term, which 3x needs; speculative gains shrink at high batch.
IDEA 6 | I 6 | P 4 | DECIDES: fallback fire rate on fact-edit tasks | Strong arithmetic, but quality rests on unreplicated 2026 preprints, and scattered recompute fails on fact edits.
IDEA 7 | I 5 | P 7 | DECIDES: erratum uptake without chain-of-thought | Near-duplicate of 4; rebase-on-cold is free; CoT dependence limits it.
IDEA 8 | I 6 | P 5 | DECIDES: shadow-gate KL/F1 pass rate on multi-hop | Its honest fallback beats bare CacheBlend; the savings collapse wherever the gate fails.
IDEA 9 | I 3 | P 6 | DECIDES: share of rewrites caused by eviction rather than expiry | Sound engineering, but it only helps capacity-bound stacks.
IDEA 10 | I 7 | P 5 | DECIDES: accuracy at a 2–4k page budget on RULER/agent replays | Targets the largest residual term (re-reads, needed for A's 3x); needs a provider repricing.
IDEA 11 | I 4 | P 3 | DECIDES: recall of top-deviation tokens at a 3% budget | The lexical proxy for attention dependence is unproven; deviation does not track entity overlap.
IDEA 12 | I 4 | P 8 | DECIDES: share f of writes that are post-expiry rewrites | Cheap and exact; it caps out around 15%.
IDEA 13 | I 3 | P 8 | DECIDES: idle-gap distribution | Subsumed by 12; terms of service need checking.
IDEA 14 | I 4 | P 7 | DECIDES: duplicate share of written tokens | Real win for re-read-heavy agents; diff-application errors are the risk.
IDEA 15 | I 1 | P 5 | DECIDES: cross-tenant public share of writes | Duplicate of 2 at about 3% of the bill.
IDEA 16 | I 3 | P 8 | DECIDES: lookback-miss rate per turn | Pure hygiene; large only if misses are frequent.
IDEA 17 | I 3 | P 4 | DECIDES: per-layer KV L2 deviation vs empty-prefix encoding | An incremental step on APE's shared-prefix trick.
IDEA 18 | I 5 | P 5 | DECIDES: new/context ratio vs 80 round-trip latency | Exact and cuts provider read cost, but latency per layer may dominate.
IDEA 19 | I 2 | P 5 | DECIDES: share of needed chunks covered by the shard | Archetype B ceiling is 3.8x, so the 1.7x is real but bounded.
IDEA 20 | I 4 | P 2 | DECIDES: deviation variance captured by summed pairwise deltas on ≥3 chunks | Deviations are nonlinear; additivity is unlikely to hold.
IDEA 21 | I 5 | P 7 | DECIDES: share of writes driven by invalidation | Duplicate of 4 and 7, with a useful log-based measurement.