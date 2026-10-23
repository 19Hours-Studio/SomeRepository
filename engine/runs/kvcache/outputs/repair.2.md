=== IDEAS ===
IDEA 1
NAME: Turn-granular reversible KV eviction
MECHANISM: Anchor kept: a query-agnostic score in the style of KVzip decides which ~30% of the FP8 KV stays on the GPU, and the evicted pages stay in CPU memory where they can be recalled, not deleted. The repair moves recall from every decode step to once per user turn. When a new message arrives, its query vectors are scored against page summaries (min/max keys, about 1% of HBM) and the top 10% of offloaded pages are fetched in one ~8 ms burst that overlaps the message's prefill. A per-step Quest-style "valve" is capped at ≤0.36% of the context per step. This cuts PCIe load from 25.8× the step time (the killed design) to 0.08×. At 32K context that is 64 vs 26 active users per H100 and 2.49× decode tokens/s over FP8-full. Turn-start reload from CPU drops from 84 to 34 ms. The binding quantity is the residency-scoring cost: the design only pays if scoring costs ≤0.29× prefill on trace-average turns (7.6K new tokens), or the turns are short follow-ups on a shared context. So the residency score has to be cheap (an observation window or KVzip's static head-level score), not KVzip's full context-reconstruction pass.
VALUE: In multi-turn shared-context chat (≈500 new tokens per turn) it costs 0.49–0.61× the GPU-seconds per request of FP8-full; on document-heavy turns with full KVzip scoring it costs 1.5–2.2× and loses.

IDEA 2
NAME: FLOP-per-byte bounded-tier admission
MECHANISM: Anchor kept: score cached prefixes by (expected reuses × recompute FLOPs) ÷ bytes, with exact reuse only. The repair applies the score only where capacity or writes are actually bounded, since the replay confirmed it gives 0% at ≥25M tokens. The first place is the HBM-only prefix cache, as leaf-only eviction with a 180 s reuse half-life. On replayed Mooncake traces at 0.5–1M tokens it saves 43–75% more prefill FLOPs than LRU for Llama-8B and 156–207% more for DeepSeek-V3 (MLA), and it is never more than 5% worse at any capacity. The second place is SSD admission under an endurance budget. There the score must cover the whole prefix chain, because per-block admission keeps deep blocks whose ancestors are missing and gets about zero value. For DeepSeek-V3 it keeps 37–95% more SSD-hit FLOPs per byte written than random admission at a 10–35% write budget. In $ form the score gives the threshold directly: admit if P(reuse) ≥ $wear/byte ÷ $recompute/byte, which is 0.04 for DSv3 and 0.21 for 8B.
VALUE: For MLA-class models in a capacity-short or write-capped last tier it doubles or triples useful hits per byte. For dense 8B models, or any tier above about 5M tokens, it is worth ≤3% of node cost, because write-all SSD wear costs only $17 per day against $576 per day for the GPU node.

=== NOTES ===

**Idea 1: Turn-granular reversible KV eviction**
- **Anchor kept?** Yes: query-agnostic residency plus recallable CPU backing.
- **Decisive numbers** (all from `idea1_budget.py`):
  - Llama-3.1-8B FP8 is 65,536 B/token by exact config arithmetic. H100 has 3.35 TB/s HBM; PCIe is taken as 25 GB/s (FACT 8). Mean output is 343 tokens per turn, computed from the Mooncake conversation trace.
  - Per-step recall gives a PCIe/HBM ratio of 25.8 (dead). Per-turn recall gives 0.08.
  - At 32K: 64 vs 26 users and 3,074 vs 1,234 tokens/s. At 128K: 16 vs 6 users, 2.54×.
  - KVzip is near-lossless at 30% on Llama-3.1/Qwen2.5/Gemma3, global layers only (FACT 2, arXiv 2505.23416).
- **Best-baseline comparison, in GPU-seconds per request:**
  - Cheapest real alternative is FP8 KV in vLLM plus LMCache/OffloadingConnector for idle sessions: 0.862 s per request ($0.60 per 1k requests at an assumed $2.5/h).
  - This design: 0.695–0.754 s with a cheap score (0.81–0.87×), 1.28–1.86 s with KVzip full scoring (1.5–2.2×), and 0.49–0.61× on follow-up turns.
  - Permanent KVzip at 30% is faster (3.34×) but fails multi-turn (SCBench).
  - ShadowKV claims 3.04× throughput and 6× batch, but only on single long contexts. It needs a per-prompt SVD of K, which is model-specific, and per-step V fetches.
- **Consistency table:** in `NOTES.md`. It binds on scoring overhead and on the valve cap (≤0.36% per step). It stalls if outputs are under 26 tokens per turn. Host DRAM is short at 128K × 512 sessions, which then needs an SSD tier.
- **Hazards:**
  - Paged attention needs eviction that is uniform across heads and done at page level. KVzip's published results are head-wise and token-level, so this granularity is untested.
  - The per-turn query can miss content the generation needs later; the valve only partly covers this.
  - Fails on tasks that need more than ~40% of the context: Text2JSON (FACT 1), whole-document summarisation, and KVzip's failing retrieval variant.
  - Untested on MLA, hybrid SSM and sliding-window layers; these must be left uncompressed.
  - The FP8 kernel accumulation bug (FACT 6) applies.
- **Deciding unknown:** accuracy of 16-token, head-uniform residency at 30% plus 10% per-turn recall on SCBench multi-turn tasks.
  - Experiment: Llama-3.1-8B at 32K, using kvpress plus a recall hook.
  - Kill line: the idea is dead if it scores more than 2 points below FP8-full, or not at least 5 points above permanent KVzip-30%.
  - Sample size: McNemar with ~10% discordant pairs to detect a 2-point gap needs about 2,000 queries. SCBench's ~4.8k multi-turn queries are enough.
  - Also measure the scoring overhead s; it must be under 0.29 on trace-like turns.
- **Closest existing work:** ArkVale (NeurIPS'24: recallable page eviction, but recall every step), RocketKV-MT (keeps all tokens, selects every step), Quest and InfLLM. Turn-granular recall on top of a query-agnostic resident set did not turn up in my searches.
- **Verdict: NICHE → WORKS** for multi-turn shared-context chat with a cheap residency score. FAILS on document-heavy turns if full KVzip scoring is used.

**Idea 2: FLOP-per-byte bounded-tier admission**
- **Anchor kept?** Yes: the value-density score, exact reuse only.
- **Decisive numbers** (replay `sim_evict.py` / `sim_chain.py` on Mooncake FAST25 traces; DSv3 costs from config: 70,272 B/token, 37B active, absorbed-MLA attention):
  - HBM-tier eviction gains are listed in the mechanism above (half-life 180 s). With 600 s or GDSF aging it loses up to 25% at 5–10M tokens.
  - SSD chain admission vs random at equal writes, DSv3: +37% at 35% writes and +65–95% at about 10% writes. Llama-8B: +11% on conversation, −18% on toolagent.
  - Learned reuse probability alone (no FLOP term) is no better than random. The gain therefore comes from the FLOP/byte term, which is large only when attention FLOPs dominate early: about 4.4K tokens for MLA vs 30K for 8B GQA.
- **Best-baseline comparison:**
  - Real alternatives are LRU plus a CPU DRAM tier (vLLM OffloadingConnector, LMCache; cheapest), write-all SSD spill (LMCache/Mooncake), second-hit admission, and AsymCache/Marconi-style cost-aware eviction.
  - Cost per delivered hit: wear is $0.088 per TB written (PM9A3-class drive at ~$160/TB, 1 DWPD over 5 years).
  - Using DeepSeek's 73.7k input tokens/s per node (Day 6) and a 56.3% hit rate (CloudMatrix paper), write-all costs:
    - DSv3: 196 TB/day, about $17/day, 3% of node cost.
    - Llama-70B BF16: 912 TB/day, about $80/day, and the endurance of 119 drives, which is a hard cap.
- **Consistency table:** in `NOTES.md`.
- **Hazards:**
  - Half-life tuning can make it worse than LRU.
  - Reuse is hard to predict at write time; the buckets are weak.
  - Sparse-attention models (e.g. DeepSeek V3.2's DSA) would flatten the FLOP/byte gradient and remove the gain.
  - Exactness still needs batch-invariant kernels (FACT 12).
- **Deciding unknown:** how well reuse can be predicted per chain at write time, on production traces with session IDs. Experiment: replay ≥1 day of traces (≥10⁵ chains) and compare FLOPs per byte written against random admission at equal writes. Kill line: below a 15% gain at a 25% write budget.
- **Closest existing work:** AsymCache (2026, position-aware recompute cost), Marconi (FLOP-aware eviction for hybrid models), GDSF from web caching, ScaleFlux's FDP placement for KV on SSD. I found no published endurance-budgeted admission policy for KV-cache SSD tiers.
- **Verdict: NICHE.** It works for MLA-class models in an HBM-only cache or a write-capped SSD tier. It fails for dense models and for tiers at or above ~5M tokens.

Files are in `/home/user/SomeRepository/engine/runs/kvcache/repair/c2/`: `LOG.md`, `NOTES.md`, the scripts and their output files. Nothing was committed.

Sources: [KVzip](https://arxiv.org/pdf/2505.23416) · [ArkVale (NeurIPS)](https://aitopics.org/tag/efficient%20generative%20llm%20inference) · [RocketKV](https://arxiv.org/html/2502.14051v3) · [AsymCache](https://arxiv.org/pdf/2606.02964) · [KVCache in the Wild](https://arxiv.org/pdf/2506.02634) · [Mooncake traces](https://github.com/kvcache-ai/Mooncake) · [ScaleFlux KV SSD DWPD](https://storagereview.com/news/scaleflux-kv-cache-ssd-platform-claims-7-10-dwpd-and-200-fdp-streams) · [Tutti](https://arxiv.org/pdf/2605.03375) · [SSD prices](https://datacenterdisk.com/nvme-u2/7-68tb/samsung) · [DeepSeek Day 6](https://wbgsv0a.gigazine.net/gsc_news/en/20250303-deepseek-ai-cost-profit) · [CloudMatrix384](https://arxiv.org/pdf/2506.12708) · [SCBench review](https://liner.com/review/scbench-kv-cachecentric-analysis-longcontext-methods) · [llm-d tiered cache](https://llm-d.ai/docs/guides/tiered-prefix-cache)