=== TRIAGE ===
IDEA 1 | I 7 | P 8 | DECIDES: hit rate × prefix length (load ≪ recompute) | Exact tiered prefix reuse targets D's prefill term (ceiling 2.46×), which is the only archetype with room; it extends what vLLM/LMCache already do. Overlaps 9/12/13.
IDEA 2 | I 3 | P 3 | DECIDES: fraction of pages certifiable at ε=1e-3 | Min/max bounds are loose on 128-dim keys, so few pages certify; capped by A's decode-KV ceiling of 1.29×.
IDEA 3 | I 3 | P 8 | DECIDES: per-model accuracy delta at 128K | A safe 2× capacity gate, but FP8 is already standard and gives only 1.14× in A. Same idea as 5 and 14.
IDEA 4 | I 5 | P 4 | DECIDES: offloaded-page recall per step × PCIe bytes | Fixes eviction's multi-turn failure, but PCIe stalls (Quest/InfiniGen-style) likely eat the capacity win.
IDEA 5 | I 3 | P 7 | DECIDES: correlation of probe KL with RULER loss | The gating is sound, but Attempt 4 shows perplexity-like probes miss failures, and the gain is capped at 2×.
IDEA 6 | I 5 | P 6 | DECIDES: working set ÷ tier capacity | Cheap and exact, and lifts h for 1/(1−0.66h). It only matters when capacity binds; a +15% gain over LRU is plausible on skewed traces.
IDEA 7 | I 4 | P 4 | DECIDES: link time ÷ compute time per token | Essentially Cake. Re-estimation adds little, and it only pays off on 1–4 GB/s links.
IDEA 8 | I 5 | P 4 | DECIDES: RULER/SCBench gap vs FP8 at matched memory | Needs 2-bit KIVI, which is unvalidated on reasoning. Promotion per turn misses pages that shift mid-decode.
IDEA 9 | I 7 | P 8 | DECIDES: h × prefill saved vs slowest-tier load time | Same as 1, with the clearest failure list (low h, reordered chunks, SSD-only tiers).
IDEA 10 | I 3 | P 3 | DECIDES: lossless ratio on FP8 KV bytes | FP8 mantissas are close to random, so the ratio is likely ≤1.2× and likely below the 1.3× kill line.
IDEA 11 | I 3 | P 5 | DECIDES: top-k page recall vs PCIe bytes per token | Quest plus offload (ShadowKV/InfiniGen territory); capped at 1.29× in A.
IDEA 12 | I 7 | P 5 | DECIDES: link BW vs ~1.5 GB/s break-even | Core idea is the same as 1. The falsifier is mis-specified: an NVMe hit cannot beat a GPU-resident hit by 3× in TTFT.
IDEA 13 | I 7 | P 8 | DECIDES: hit rate h (≥0.4 with overlap) | Same as 9, and its falsifier is the best-specified of the group.
IDEA 15 | I 4 | P 4 | DECIDES: mean accepted length per verify (>~3) | Output is exact (TriForce/MagicDec lineage), but acceptance collapses on long reasoning and the verify still reads the full cache.

Recommendation: merge 1/9/13 as the lead (exact tiered prefix reuse for D), add 6 as its eviction policy, and keep 3/5/14 as the safe FP8 default. The rest are tight-ceiling or repeat earlier attempts.