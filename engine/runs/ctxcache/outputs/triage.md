=== TRIAGE ===
IDEA 1 | I 6 | P 5 | DECIDES: recompute fraction needed to hold first-token KL under budget (needs ≤10%) | Closed-loop audit beats CacheBlend's open-loop 15%, but it is own-stack only and the "B 2.3×" claim mislabels a hosted archetype.
IDEA 2 | I 4 | P 7 | DECIDES: accuracy loss of patched vs clean text | Sound and client-only, but it only covers edit-heavy C sessions (1.3–1.7×), not reordering.
IDEA 3 | I 4 | P 6 | DECIDES: patch-application accuracy as patch count grows | Same as 2 without cost numbers; merge into 2/5.
IDEA 4 | I 5 | P 4 | DECIDES: in-cluster recall of needed chunks | It is CAG scaled by routing, but the longer context adds distraction risk and recall misses fall back to uncached input; ~1.6× at most.
IDEA 5 | I 4 | P 7 | DECIDES: answer agreement between patched and inline prompts, including multi-hop | Best-specified version of the patch idea, with honest scope (no reordering). Keep this one as the canonical patch candidate.
IDEA 6 | I 7 | P 4 | DECIDES: token fraction capturing ~95% of query attention mass on multi-hop tasks | It targets D's largest term, but query attention at layer l depends on stale earlier layers and decode tokens attend elsewhere, so 3% is optimistic.
IDEA 7 | I 3 | P 5 | DECIDES: retrieval popularity skew | Exact reuse, but hits are capped by set overlap; duplicate of 9/10/14.
IDEA 8 | I 4 | P 6 | DECIDES: patch-application accuracy vs rewritten doc | Duplicate of 5; line-diff patches are harder for the model to apply than prose patches.
IDEA 9 | I 3 | P 6 | DECIDES: chunk-set overlap between queries | Honest 30–60% hits with exact outputs. The quality risk is relevance order lost to sorting. Keep as the canonical ordering variant.
IDEA 10 | I 4 | P 5 | DECIDES: Zipf skew of retrieval frequency | Hysteresis is a useful addition, but the 60–80% hit estimate is a guess and the long tail stays uncached.
IDEA 11 | I 6 | P 3 | DECIDES: fraction of layers skippable at <1% loss | Residual coupling likely spreads boundary effects to all layers, so the multiplicative saving probably collapses.
IDEA 12 | I 5 | P 5 | DECIDES: task-success drop at 2–3× fewer turns | It attacks A's dominant cache-read term directly; a ~2× read cut gives about 1.4–1.5× overall.
IDEA 13 | I 5 | P 5 | DECIDES: share of post-edit tokens above drift threshold (needs ≤5%) | Audited and own-stack. The risk is that drift in early layers may underpredict drift in later layers.
IDEA 14 | I 4 | P 5 | DECIDES: Zipf skew of retrieval | Duplicate of 10, but it correctly states the long-tail limit.
IDEA 15 | I 6 | P 6 | DECIDES: tool-output share of history, plus re-fetch rate | It cuts read volume in A rather than raising hit rate, so it is lossy but measurable on SWE-bench, for ~1.5×.

Overall: the patch ideas (2, 3, 5, 8) and the ordering ideas (7, 9, 10, 14) should each be merged into one candidate. On hosted APIs, B cannot reach 3× (ceiling 3.6×). Only own-stack approximate reuse (1, 6, 13) can approach ~100% reuse, and only at a measured, non-zero quality cost. Exact ~100% hits for reordering and middle edits are not achievable under these constraints.