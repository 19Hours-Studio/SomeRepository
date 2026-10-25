=== REVIEW ===
IDEA 1: Canonical ordering plus position-independent chunks
DEFECT | MAJOR | The "5–10× less prefill than prefix caching" claim goes beyond the cited evidence, and the baseline is wrong: the fair competitor is canonical/popularity ordering plus ordinary prefix caching, which is lossless and also works through APIs. | CacheBlend measured 2.2–3.3× TTFT against full prefill. Recomputing 15% of tokens plus each chunk's first tokens plus the question leaves ≥18–20% of compute, so the ceiling is about 0.80/0.20 = 4× against system-prompt-only prefix caching. Against ordered prefix caching (doc reuse 0.34–0.70 at 1k req/5 min) the ceiling is about 2.5–3× on prefill.
DEFECT | MAJOR | "Canonical ordering turns most reorders into exact hits" is only true when the retrieved set is identical. When the set varies, the prefix breaks at the first differing document. | My replay, popularity order, 1k req/5 min: exact doc reuse is 0.337, 0.476 and 0.697 at Zipf 1.05, 1.2 and 1.5. That leaves 30–66% of doc tokens to blending, not a small remainder. At the measured skew (Zipf ≈ 0.8, see Idea 2) reuse is 0.15, so about 85% goes to blending.
DEFECT | MAJOR | APE is misattributed. APE's 93–98% needs a shared prefix plus an adaptive attention temperature plus a scaling factor, all hyperparameter-sensitive, not the shared prefix alone. A 93% retention is also a 7% loss, above the claimed 1–3%. | [APE arXiv 2502.05431](https://arxiv.org/pdf/2502.05431): "98% and 93% … on RAG and ICL"; three components; "sensitive to hyperparameter selection".
DEFECT | MINOR | The proposed order-and-blend test has no sample size. A 1-point EM difference needs about 7,840 paired questions (80% power, α = 0.05, 10% discordance); 2 points needs about 1,960. | Computed: (1.96 + 0.84)² · 0.1 / 0.01².
DEFECT | MINOR | "About 6× less with ~3-bit" does not reproduce. | 16/3 = 5.33× at most; about 4× once per-group FP16 scale and zero-point are stored (group size 32).
DEFECT | MINOR | Per-tenant isolation, needed because of HijackKV, removes cross-tenant chunk sharing. That shrinks the reuse population, which the 85–90% hit figure ignores. | [HijackKV arXiv 2607.19957](https://arxiv.org/pdf/2607.19957) is a single preprint with no independent replication.
SURVIVES | 30.5 GiB per 100k tokens is correct for a 70B model with GQA (327,680 B/token). The Berkeley figures (3.4×, 32%; [MLSys 2025](https://proceedings.mlsys.org/paper_files/paper/2025/hash/b5dc49f44db2fadc5c4d717c57f4a424-Abstract-Conference.html)) and EPIC's 8×/7× ([arXiv 2410.15332](https://arxiv.org/abs/2410.15332v3)) are quoted correctly.
RATIO | ~2 | Own stack only. Prefill gain of about 3× over ordered prefix caching (measured TTFT ≤ 3.3×), diluted by decode cost; not usable via third-party APIs.
KNOWN | yes | CacheBlend + EPIC + Liu et al. reordering ([MLSys 2025](https://mlsys.org/virtual/2025/3359)); LMCache ships CacheBlend.

IDEA 2: Popularity-first exact-prefix document ordering
DEFECT | MAJOR | The tested Zipf exponents are all more skewed than measured RAG traces. At the measured skew the gain disappears. | [Cache-Craft](https://arxiv.org/pdf/2502.15734) reports that the top 5% of chunks serve 40–60% of requests. That matches Zipf ≈ 0.75–0.85; Zipf 1.05 gives 80.5% and Zipf 1.5 gives 99.2%. At Zipf 0.8 my replay gives reuse of 0.089–0.205 (below the 0.217 break-even) and a bill ratio of 0.97–1.06×.
DEFECT | MAJOR | The headline reuse (0.400/0.546/0.768) only reproduces at about 10,000 requests per 5-minute TTL (about 33 req/s), which is never stated. | My replay: 0.405/0.551/0.776 at 10k per window, 0.253/0.379/0.590 at 100, and 0.155/0.259/0.452 at 10. Zipf 1.05 at 10 req/5 min is below the 0.217 break-even.
DEFECT | MAJOR | Four breakpoints cannot cover the system prompt plus five documents. Either the system prompt or documents 4–5 go uncached, and the 1.78× does not survive against a baseline that caches the system prompt. | Breakpoints at system, docs 1, 2, 3: 1.27/1.44/1.57× at 10k req/5 min and 1.11/1.24/1.46× at 100. Caching only the system prompt is itself worth about 1.25× in my cost model, so the baseline matters.
DEFECT | MAJOR | "Counter matches trie-greedy" is an artefact of the independent-draw Zipf workload, under which popularity order is near-optimal by construction. Real retrieval is query-correlated (documents are retrieved together). The counter is also not stateless: it holds counts for 100k IDs. | No real trace was used; [CacheWeaver](https://arxiv.org/pdf/2606.19667) was evaluated on real QA with vLLM, a 20–33% TTFT gain.
DEFECT | MAJOR | Popularity order pushes the most relevant document out of position 1. The quality cost is real and not bounded, and the proposed test has no sample size. | [Stable-RAG](https://arxiv.org/pdf/2601.02993) finds answers change with order even under 1k tokens. Detecting a 1-point EM change needs about 7,840 paired questions.
SURVIVES | The break-even reuse of 0.217 is exact ((1.25 − 1)/(1.25 − 0.1)). The stated ratios are consistent with fixed costs of about 0.445× the document cost. Hits are exact.
RATIO | ~1.1 | Baseline caches the system prompt. Breakpoints at system, docs 1–3. Zipf 0.8–1.2 at 100–1,000 req/5 min gives 0.97–1.35×.
KNOWN | yes | [CacheWeaver](https://arxiv.org/pdf/2606.19667) and [Liu et al. MLSys 2025](https://proceedings.mlsys.org/paper_files/paper/2025/hash/b5dc49f44db2fadc5c4d717c57f4a424-Abstract-Conference.html) already reorder for prefix sharing.
NEW FACT | Real RAG popularity skew is 5% of chunks → 40–60% of requests (≈ Zipf 0.8), and 3.1–31.4% of corpus → 50% of queries | [Cache-Craft 2502.15734](https://arxiv.org/pdf/2502.15734); [Shared Disk KV 2504.11765](https://arxiv.org/pdf/2504.11765)

IDEA 3: Popularity order with second-sighting cache writes
DEFECT | FATAL | "Never loses in any tested regime" is false against a competent baseline. With breakpoints at depths 2–5 there is no system-prompt breakpoint, so every depth-2 miss pays for the system prompt again. | Baseline with system prompt cached, Zipf 1.05: 0.81× (10 req/5 min) and 0.90× (100) at 5-minute TTL; 0.88× and 1.00× at 1-hour TTL. Zipf 1.2 at 10 req: 0.90×. The claimed 1.06–1.24× only reproduces against an uncached-system-prompt baseline (my run: 1.01–1.40×).
DEFECT | MAJOR | At the measured skew (Zipf ≈ 0.8) it loses money at every traffic level. | My replay: 0.80–0.83× at 100–10k req/5 min with either TTL.
DEFECT | MAJOR | The second-sighting list must be shared across every client process and host in the organisation. Per-process lists split the sightings and delay writes further; this coordination cost is not mentioned. | At 1,000 req/5 min spread over N workers, each worker sees 1/N of the sightings.
DEFECT | MINOR | Over Idea 2 the added gain is small except at low traffic. | Zipf 1.5 at 10k req/5 min: 1.85× against 1.79× for always-write at the same depths.
DEFECT | MINOR | Concurrent identical prefixes miss, because a cache entry exists only after the first response starts. This is not modelled. | 3.3 req/s at 1k req/5 min against multi-second prefill for 3.6k-token prompts.
SURVIVES | Zipf 1.5 at 100–1,000 req/5 min reproduces 1.64–1.82× with the 1-hour TTL. The 1-hour TTL with second sighting is sound: a write needs ≥ 1.11 reads/hour to pay off.
RATIO | ~1.0 | Baseline caches the system prompt. Zipf 0.8–1.2 at 100–1,000 req/5 min: 0.80–1.38×.
KNOWN | partly | TinyLFU / CDN "cache on second hit" is standard. Applying it to breakpoint placement is not found in the literature, but it is a small step.

IDEA 4: Content-addressed position-independent KV with gated repair
DEFECT | MAJOR | The "quality gate with exact fallback" is a population monitor, not a per-request fallback. The 99% of requests not shadowed are served approximated with no check, and KL on 32 output tokens is not task F1. | At 1k req/5 min, 1% shadowing gives 2,880 samples/day across all chunk types. Detecting a 1-point F1 shift needs about 7,840 paired samples, so ≥ 3 days per chunk type before r can be tuned.
DEFECT | MAJOR | The baseline is wrong for the case modelled. "Same 8 chunks in a new order" is solved losslessly by canonical sort plus prefix caching. | Ordered prefix caching: about 1–2% recompute (question only). Idea 4: 8.4–27.9%, i.e. 5–20× worse on that case. The 3–10× gain applies only when the set or the offsets really vary.
DEFECT | MAJOR | Compute fraction is used as the cost: it ignores I/O, selection overhead and measured repair limits. | NVMe load of 77 ms is about 50% of the 152 ms full prefill. CacheBlend measured only 2.2–3.3× TTFT. [KVShareArena](https://arxiv.org/pdf/2609.10266) (preprint) finds repair recovers only ½–⅔ of the gap on multi-source questions.
DEFECT | MINOR | Storing keys before RoPE adds nothing over exact re-rotation (RoPE rotations compose: R(p+d) = R(d)R(p)), and it needs a custom kernel in place of standard paged/Flash kernels, which take rotated keys. | RoPE algebra.
DEFECT | MINOR | Tokenisation can differ at span edges when text is re-embedded in a new context, so token-ID hashes miss the first and last tokens. The 16-token splice window is arbitrary and not sourced. | Byte-pair-encoding merges across span boundaries.
SURVIVES | 128 KiB/token (8B), 320 KiB and 328 GB per 1M tokens (70B), 10.7 ms over PCIe at 50 GB/s, and 77 ms from NVMe at 7 GB/s all reproduce. The prefill estimate (90 TFLOP, about 152–166 ms on an H100) holds, and the compute fractions roughly reproduce (my linear count: 6–32%).
RATIO | ~1.5 | Own stack. Against ordered prefix caching on varying-set or agent traffic: about 2× prefill, diluted by decode and shadow cost; about 1× on pure reorders.
KNOWN | yes | LMCache CacheBlend for agents, [Cache-Craft](https://arxiv.org/pdf/2502.15734), KVShare, EPIC. Content-defined chunking is standard in deduplication (LBFS).
NEW FACT | Anthropic: up to 4 breakpoints, with about 20-block lookback for hits at earlier boundaries | [Anthropic prompt caching docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)

Sources:
- [HijackKV](https://arxiv.org/pdf/2607.19957)
- [KVShareArena](https://arxiv.org/pdf/2609.10266)
- [CacheWeaver](https://arxiv.org/pdf/2606.19667)
- [Anthropic prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Liu et al. MLSys 2025](https://proceedings.mlsys.org/paper_files/paper/2025/hash/b5dc49f44db2fadc5c4d717c57f4a424-Abstract-Conference.html)
- [APE](https://arxiv.org/pdf/2502.05431)
- [EPIC](https://arxiv.org/abs/2410.15332v3)
- [Stable-RAG](https://arxiv.org/pdf/2601.02993)
- [Cache-Craft](https://arxiv.org/pdf/2502.15734)
- [Shared Disk KV](https://arxiv.org/pdf/2504.11765)