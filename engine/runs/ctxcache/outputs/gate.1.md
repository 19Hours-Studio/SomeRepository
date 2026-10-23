=== GATE ===
IDEA 1: Edits shipped as appended patches
KILLER | Whether answers from the patched prompt match answers from the inline-edited prompt, including multi-hop questions that touch superseded text. It must hold before the client rebuilds at 5% patches | required ≥0.98 agreement | available: not measured on documents. PI-LLM shows near-perfect retrieval of the latest value while sequential updates stay below a model-specific threshold, then a fast drop to near zero. Telling the model to ignore earlier input has "limited success" (arXiv 2506.08184) | MARGIN ≈1, provisional: needs a paired evaluation on a real model
CHAIN | Archetype C: document first with a cache breakpoint, and a mid-document edit forces a 1.25× rewrite of the 25k-token tail | now $0.514 per 10-question session with one edit ($0.42 + $0.094) | with idea $0.423 ($0.42 + $0.0034 for the patch write and its reads) | RATIO 1.21 (only 1.02–1.06 if 10–30% of sessions have an edit)
VERDICT | WOUNDED | It is cheap and runs client-only, but cache writes and reads still dominate, and the gain is capped at about 1.2× even when every session has an edit.
NEW FACT | Interference from superseded values cuts retrieval accuracy roughly log-linearly toward zero, and errors return overwritten values even when the correct one sits just before the query | https://arxiv.org/abs/2506.08184
NEW FACT | Anthropic's own docs give 1-hour cache writes at 2× the base input price and reads at 0.1×, which confirms the ledger's multipliers | https://docs.claude.com/en/docs/build-with-claude/prompt-caching

IDEA 2: Query-gated selective KV recompute
KILLER | Share of tokens that must be recomputed under query-driven selection to keep about full accuracy | required ≤3% | available 20%: ProphetKV, which already does query-driven selective recompute, needs a 20% ratio for 96–101% of full-prefill accuracy (arXiv 2602.02579, ICML 2026) | MARGIN 0.15
CHAIN | Archetype D with CacheBlend in LMCache (about 15% recompute) | now 0.533 of baseline cost | with idea 0.483 at the claimed 3% plus about 3% probe overhead. At ProphetKV's 20% it would be 0.577, i.e. worse | RATIO 1.10 as claimed, 0.92 at the measured recompute ratio
VERDICT | DEAD | The query-driven approach is prior art (ProphetKV, QCFuse), and the best of it still needs about 7× more recompute than the idea assumes.
NEW FACT | ProphetKV names a "crowding-out" effect in CacheBlend's selection (globally salient but query-irrelevant tokens fill the budget) and fixes it with query-relevance ranking. It still needs 20% recompute | https://arxiv.org/html/2602.02579v3
NEW FACT | QCFuse (arXiv 2606.05875) also does query-aware cache fusion, recomputing only selected KV entries under the current request order | https://arxiv.org/pdf/2606.05875

IDEA 3: Read-cost-gated turn collapsing
KILLER | Cut in turns per task without losing task success | required 2× fewer turns | available ≤1.43×: CodeAct reports "up to 30% fewer actions" on M3ToolEval (82 tasks), with gains mostly in long or parallel chains (arXiv 2402.01030) | MARGIN 0.71
CHAIN | Archetype A: append-only agent with cache breakpoints, where cache reads are 54% of cost | now 1.00 | with idea 0.73 at 2× fewer turns, or 0.84 at CodeAct's 30%. Writes of new tool output (23%) and output tokens (23%) stay the same | RATIO 1.37 as claimed (1.19 at the measured 30%)
VERDICT | WOUNDED | It attacks the right term, but halving the reads is worth only 1.37×, and the measured turn reduction is short of 2×.
NEW FACT | The CodeAct advantage grows with chain length: an 18.8-point absolute gap at chains of 12 or more steps, and none at short chains | https://www.alphaxiv.org/abs/2608.06370

IDEA 4: Drift-gated partial recompute
KILLER | Share of post-edit tokens that need full recompute to keep quality | required ≤5% | available 5–18%, with about 15% "typically" needed for the same quality: CacheBlend on Yi-34B, F1 drop of 0.01–0.03 (arXiv 2405.16444). ProphetKV needs 20% | MARGIN 0.33
CHAIN | Archetype D: own stack with CacheBlend-style selective recompute in LMCache (15%) | now 0.533 | with idea 0.505 (5% recompute plus 4 of 80 early layers over post-edit tokens). At the 15% seen in practice it is 0.56 | RATIO 1.05 (0.95 at 15%; 1.98 only against plain prefix recompute)
VERDICT | DEAD | Against the selective-recompute practice already in LMCache, the gain is about 1.05×. What it adds is mainly the audited quality bound, not lower cost.
NEW FACT | Exact check: a Llama-70B-class model's KV is 80×8×128×2×2 B = 320 KiB per token at FP16, which matches the idea. Keeping full per-layer hidden states to measure drift would cost 1,280 KiB per token, so only a few early layers can be stored | computed in `gate_calc.py`
NEW FACT | With full KV reuse and no recompute, Musique F1 falls from 0.35 to 0.15 | https://arxiv.org/pdf/2405.16444

Caveat: I could not measure quality on a real model here because Hugging Face is blocked. Idea 1's MARGIN and the recompute shares for Ideas 2 and 4 come from published papers. A real-model run would need paired patched-vs-inline evaluations for Idea 1 and the share of post-edit tokens above the drift threshold for Idea 4. The arithmetic is in `/home/user/SomeRepository/engine/runs/ctxcache/gate/c1/gate_calc.py`. Nothing was committed.

Sources: [CacheBlend](https://arxiv.org/pdf/2405.16444) · [LMCache CacheBlend blog](https://blog.lmcache.ai/2025-03-31-eurosys) · [PI-LLM](https://arxiv.org/abs/2506.08184) · [ProphetKV](https://arxiv.org/html/2602.02579v3) · [QCFuse](https://arxiv.org/pdf/2606.05875) · [CodeAct](https://arxiv.org/html/2402.01030v1) · [Bitter Lesson of Tool Calling](https://www.alphaxiv.org/abs/2608.06370) · [Anthropic prompt caching docs](https://docs.claude.com/en/docs/build-with-claude/prompt-caching) · [Helicone caching pricing](https://docs.helicone.ai/gateway/concepts/prompt-caching)