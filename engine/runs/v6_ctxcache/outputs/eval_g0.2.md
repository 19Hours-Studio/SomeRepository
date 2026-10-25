=== GATE ===
IDEA 1: Erratum-append discipline with rebase-on-cold
KILLER | share of the best-practice agent bill caused by in-place middle edits, which is the only thing errata can remove | required ≥33% of the bill avoidable, to reach 1.5x | available ≈1–8% (ledger Archetype A: fresh uncached input is 1% and total misses are 8%; the 47% write term is new suffix tokens, which every turn must pay anyway) | MARGIN ≈0.03–0.24 (call it 0.1)
CHAIN | append-only context with deterministic serialization, which is already Manus and Claude Code practice at a 92% hit rate | now $0.58/MTok input | with idea ≈$0.56–0.58/MTok (≤$0.30/MTok only in the unrealistic case where all 8% of misses were avoidable edits, giving a 1.9x upper bound) | RATIO ≈1.02
VERDICT | DEAD | My exact recomputation supports the arithmetic: in-place edit 6.1x vs erratum 1.02x per edit, close to the idea's 6.78x and 1.03x. But the 1.85x is measured against in-place editing, which best practice already avoids, so the gain over a competent append-only agent is about 1x.
NEW FACT | In an exact recomputation (100k context, 1k new suffix, Anthropic multipliers), a uniform-position edit costs 6.11x a fully cached turn and a 200-token erratum costs 1.022x | gate.py in this working directory

IDEA 2: Content-addressed position-independent KV with gated repair
KILLER | fraction of the quality gap (no cache vs full recomputation) recovered by partial-recompute repair on multi-source queries; "≈100% hit at full quality" needs about 0.95 or more | required ≥0.95 gap recovered | available 0.5–0.67 for multi-source queries (KVShareArena, arXiv 2609.10266; unrepaired caches can do worse than no cache). Single-source queries are near-full. | MARGIN ≈0.6
CHAIN | Archetype C: vLLM/SGLang automatic prefix caching plus routing plus LMCache. Prefill is 55% of cost, and only the system prompt hits (83% of full prefill compute) | now 1.00 (relative GPU cost per request) | with idea 0.61 (23.2% + 1% shadow out of 83%, so prefill × 0.29); 0.64 at r=30% for multi-hop | RATIO 1.64 (1.56 for multi-hop)
VERDICT | WOUNDED | It has real compute headroom on reordered or re-placed content and the memory and transfer numbers check out (128 KiB/token at 8B; 512 MiB is about 10.7 ms over PCIe5). But published repairs recover only half to two-thirds of the multi-source quality gap. The gate would fall back to exact recompute on exactly the hardest cases, and it does nothing for third-party API users (Archetype B).
NEW FACT | KVShareArena: training-free repair methods are barely affected when a different checkpoint wrote the cache, while trained adapters lose quality | https://arxiv.org/pdf/2609.10266
NEW FACT | KV-Repurpose, a vLLM testbed: naive segment reuse holds up on single-document tasks but fails on cross-document reasoning | arXiv 2610.13060 (https://www.opentrain.ai/papers/kv-repurpose-a-testbed-for-evaluating-non-prefix-kv-cache-reuse--arxiv-2610.13060/)
NEW FACT | PatchKV (arXiv 2609.26219) is direct prior art for KV recovery under dynamic context edits | https://arxiv.org/pdf/2609.26219

IDEA 3: Diff-encoded repeated tool outputs
KILLER | share of written plus re-read tokens that duplicate content already in context | required ≥37% (to remove 33% of the bill from the 89% write+read share) | available ≈14%. Estimate: 26% of file reads are repeats (CORVUS, SWE-PolyBench with Sonnet 4, 834/3,207) × an assumed ~60% file-read share of written tokens × ~90% removed after diffs. CORVUS's measured input cut for a similar mechanism is 9–50%. | MARGIN ≈0.38
CHAIN | Archetype A, a Claude Code-style agent with existing file-unchanged notices | now $0.58/MTok-equivalent bill | with idea ≈$0.51 (range $0.32–0.53 across CORVUS's 9–50%) | RATIO ≈1.14 (range 1.09–1.8)
VERDICT | WOUNDED | It does reach the right terms (writes, and every later re-read of them), but measured repeat rates put the typical gain near 1.1–1.3x. The 50% case is model-specific, and the 60% file-read share needs a trace measurement.
NEW FACT | CORVUS (synced file registry with only current contents injected) cut input tokens per task by 9–50% across four LLMs with comparable pass rates; 26% of file-read actions were repeats | https://arxiv.org/pdf/2607.22711
NEW FACT | AgentDiet reports 21–36% total cost and 40–60% input-token reductions from trajectory pruning, in a different setup | https://pypi.org/project/clew-custos/

IDEA 4: Cut the re-read bill, not misses
KILLER | CPU-to-GPU PCIe bandwidth needed to fetch top-K pages per decode step from CPU/SSD as written (Llama-3-8B, 128 KiB/token, 2–4k token budget = 0.27–0.54 GB per step per sequence, 30 ms per-token latency) | required ≈17.9 GB/s per sequence (4k budget) → 573 GB/s at batch 32 | available ≈50 GB/s effective PCIe5 x16, so the maximum batch is 2.8–5.6 (ShadowKV and NOSA also report offloaded decode is communication-bound) | MARGIN ≈0.09–0.18
CHAIN | Archetype C with dense KV kept in HBM. Decode is 25% of cost, and Quest's 2.23x latency gain applies only there | now 1.00 | with idea ≈0.86 (0.75 + 0.25/2.23), and this assumes KV stays on the GPU, unlike the idea | RATIO ≈1.16
VERDICT | DEAD | Fetching pages per query from CPU/SSD fails on PCIe bandwidth by 5–10x at serving batch sizes. If KV stays in HBM (plain Quest), the gain is limited to the decode share (~1.16x). The "0.1x read" is a provider price, not a GPU cost this idea removes, so on an API it changes nothing.
NEW FACT | In my recomputation, the idea's own 50-turn model gives cached reads at 63.3% of the bill, writes 22.9% and output 13.8% (the idea says 60.5%, 26.3% and 13.2%); the conclusion is the same | gate.py in this working directory
NEW FACT | ShadowKV keeps low-rank keys on the GPU and offloads values, with up to 6x batch and 3.04x throughput on A100 (assuming 31.5 GB/s PCIe); NOSA states that offloaded decoding is communication-bound and that training-free sparse offload degrades long-generation quality | https://arxiv.org/pdf/2410.21465 ; https://arxiv.org/pdf/2510.13602v2

Notes: The quality claims for ideas 2–4 (KL/F1 against full recompute, SWE-bench pass rates, RULER) need a run on a real model, which can't be done here because Hugging Face is blocked. The 60% file-read share in idea 3 and the 25% decode share in idea 4 are assumptions, not measurements. The arithmetic is in `/home/user/SomeRepository/engine/runs/v6_ctxcache/eval_g0/c2/gate.py`.

Sources:
- [KVShareArena (arXiv 2609.10266)](https://arxiv.org/pdf/2609.10266)
- [PatchKV (arXiv 2609.26219)](https://arxiv.org/pdf/2609.26219)
- [KV-Repurpose (arXiv 2610.13060)](https://www.opentrain.ai/papers/kv-repurpose-a-testbed-for-evaluating-non-prefix-kv-cache-reuse--arxiv-2610.13060/)
- [CORVUS (arXiv 2607.22711)](https://arxiv.org/pdf/2607.22711)
- [clew-custos on PyPI](https://pypi.org/project/clew-custos/)
- [ShadowKV (arXiv 2410.21465)](https://arxiv.org/pdf/2410.21465)
- [NOSA (arXiv 2510.13602)](https://arxiv.org/pdf/2510.13602v2)