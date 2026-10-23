
=== IDEAS ===
IDEA 1
NAME: Audited exact-prefix agentic KV tier
MECHANISM: The anchor stays: KV is reused only on an exact token-prefix match and kept in the deployment's own KV dtype, so the result is lossless by construction. In the repaired design, the CPU DRAM of all 8 GPUs in a node is pooled into one cache (about 1.6 TB). NVMe is written only for blocks that have already been hit twice. Each block gets a hash, and a 1% sample of cache hits is recomputed from scratch. That sample is checked against the server's own run-to-run noise. This replaces the claim that outputs are bit-identical, which would need batch-invariant kernels that cost 34–56% of throughput. The design is aimed at agentic or long multi-turn sessions whose working set is 4–40× larger than GPU memory. For a 30–60K-token context on Llama-3.1-8B, loading a 95% hit takes 0.15–0.30 s, against 1.4–3.8 s of prefill. That gives 2.04–2.19× less GPU time per request than prefix caching on the GPU alone. PCIe is busy 11–13% of the time and the audit adds about 1.4%.
VALUE: In agentic or multi-turn serving where the working set is larger than GPU memory, it needs about 2.0–2.2× less GPU time per request than vLLM prefix caching on the GPU alone. On chat traces like Mooncake the gain is only about 1.17–1.24×: $228 → $196 per 1M requests.

IDEA 2
NAME: Two-arm probe-gated FP8 layers
MECHANISM: The anchor stays: a cheap per-model probe compares BF16 KV with FP8 KV and picks which layers keep BF16. Everything else uses the stock vLLM FP8 kernels and the `--kv-cache-dtype-skip-layers` flag. The repaired probe runs three arms over 100 prompts of 32K tokens each, plus 512 decode tokens per prompt: BF16, the stock FP8 kernel, and a simulated FP8 rounding with BF16 attention. If the stock kernel fails but the simulated rounding does not, the problem is the kernel (as in vLLM's 128K NIAH drop from 91% to 13%). The answer is then to fix the kernel, not to gate layers. Gating is used only when the error sits in a few layers. NVIDIA's docs trace Qwen2.5-7B's FP8 loss to very large values in its last layer, and R1-Distill-Qwen-7B uses the same architecture. With 1 of 28 layers in BF16, R1-Distill gets 1.93× the KV capacity and decode tokens/s of BF16 at 32K. That is 96.5% of what FP8 everywhere would give. The probe costs about 9 GPU-minutes (about $0.38).
VALUE: On models where FP8 fails, it gives about 1.9× the throughput per request of the usual BF16 fallback, for $0.38 of probing. On models where FP8 already works, it changes nothing and only certifies FP8. On Gemma-3-1B it drops to 1.0–1.5×.

=== NOTES ===
No real model was run, because Hugging Face is blocked. Every number below comes from exact memory arithmetic or from published measurements.

**Idea 1**
- **Anchor kept?** Yes: exact-prefix reuse in the native dtype.
- **Decisive numbers:**
  - Llama-3.1-8B uses 131,072 bytes of KV per token. An H100 leaves about 0.40M tokens of room for cached KV.
  - On the Mooncake conversation trace (FACT 11), the hit rate is 0.121 with the GPU cache alone. It rises to 0.315 with the pooled CPU tier and 0.374 with NVMe added.
  - On the agentic workload: 2.04× at 30K tokens of context and 2.19× at 60K.
  - Lossless exponent coding (SplitZip, 1.32× smaller) adds only 1.17 → 1.205×. It is already published, so it stays optional.
- **Baselines, cost per request served:**
  - No caching.
  - vLLM prefix caching on the GPU only. This is the cheapest option and is 1.09× better than no caching.
  - FP8 KV on the GPU, which gives about 1.2–1.5× on the agentic workload.
  - The vLLM OffloadingConnector or LMCache CPU tier. llm-d measured about −28% mean time-to-first-token on Qwen3-32B, but only when the KV cache is larger than GPU memory.
- **Consistency table:**

| Limit | Demand | Result |
|---|---|---|
| PCIe 25 GB/s | 2.7–3.3 GB/s average | OK |
| Node DRAM bandwidth, about 600 GB/s | about 26 GB/s | OK |
| DRAM capacity 1.6 TB | up to about 200 sessions × 60K tokens | OK; at 512 sessions the hit rate falls to 0.38 |
| NVMe endurance, 1 drive write per day | 3.2–3.9 per day if every evicted block is written | Fails; writing only twice-hit blocks gives about 1.0–1.2 |
| Load hidden behind compute | at a 95% hit, the load is longer than the remaining prefill | Load is exposed; the scheduler must overlap other requests' decodes |

- **Hazards:**
  - Silent corruption in the tier. Per-block hashes catch this.
  - Hit rates that depend on the workload.
  - Reordered retrieval chunks, which never hit an exact prefix.
  - "Same outputs" holds only up to the server's existing nondeterminism, not bit for bit.
- **Deciding unknown and experiment:** The deciding unknown is the share of reuse distances that exceed GPU memory but fit in DRAM. To measure it, replay at least 10⁵ requests of the real trace (or SWE-agent traces) through a cache simulator; this needs no GPU. Then estimate the audit's divergence rate on at least 1,000 sampled hits on a real model.
- **Closest existing work:** vLLM prefix caching plus the OffloadingConnector, LMCache, the Mooncake store, CachedAttention, SplitZip and Continuum. The anchor itself is known; what is new is the audit in place of batch-invariant kernels and the choice of workload.
- **Verdict:** NICHE. It works in the agentic regime (about 2×) and gives about 1.2× on chat traffic.

**Idea 2**
- **Anchor kept?** Yes: a probe-driven per-layer BF16/FP8 gate built on stock flags.
- **Decisive numbers at 32K:**

| Model | Layers kept in BF16 | KV capacity vs BF16 |
|---|---|---|
| R1-Distill-Qwen-7B | 1 | 1.93× |
| R1-Distill-Qwen-7B | 2 | 1.87× |
| R1-Distill-Qwen-7B | 14 | 1.33× |
| Gemma-3-1B (4 global layers) | 0 / 1 / 4 global | 1.85× / 1.53× / 1.00× |

- **Supporting sources:** the 10-model FP8 RULER study (FACT 7), the NVIDIA TensorRT-Edge-LLM finding on Qwen2.5's last layer, and KVTuner, which found layer sensitivity is consistent across prompts.
- **Baselines, cost per request served:**
  - FP8 everywhere: cheapest, but lossy on 2 of the 10 models.
  - BF16 fallback: the idea is 1.93× better on R1-Distill.
  - Skipping only the sliding-window layers.
  - KVTuner: needs custom kernels and a search.
- **Consistency checks:**
  - Gating pays (≥1.1×) as long as at most 80% of layers stay in BF16.
  - With N=100 prompts, the probe can spot an outlier layer whose error is more than 0.3 SD above the median.
  - Decode stays memory-bound up to a batch of 54.
  - The kernel-versus-format arm deals with the FACT 6 kernel bug.
- **Hazards:**
  - Probe KL may not predict multi-hop RULER scores.
  - The probe only covers the task types in its prompt set.
  - Per-layer gating cannot fix per-channel outliers in Gemma's single KV head (multi-query attention).
- **Deciding unknown and experiment:** Is the FP8 loss confined to a few layers in R1-Distill and Gemma-3-1B? Run RULER at 32K with four arms: BF16, FP8 everywhere, FP8 with the gated layers, and FP8 with the same number of random layers in BF16. That needs 870 paired items per arm to detect a 3-point gap at 80% power. The idea is shown wrong if the gated arm does not beat the random arm, or does not come within 3 points of BF16.
- **Closest existing work:** KVTuner, NVIDIA ModelOpt per-layer KV scales and vLLM's skip-layers flag. This idea is an incremental deployment tool on top of them.
- **Verdict:** WORKS for Qwen-family models with outlier layers, pending the experiment above. NICHE or FAILS for Gemma-3-style models with few global layers.

Files are in /home/user/SomeRepository/engine/runs/kvcache/repair/c1/:
- LOG.md
- NOTES.md
- calc/idea1.py
- calc/idea1b.py
- calc/idea1c.py
- calc/idea2.py

Sources:
- [SplitZip](https://arxiv.org/pdf/2605.01708)
- [KVTuner](https://arxiv.org/pdf/2502.04420)
- [TensorRT-Edge-LLM FP8 KV](https://nvidia.github.io/TensorRT-Edge-LLM/latest/user_guide/features/FP8KV.html)
- [LLM-42](https://arxiv.org/pdf/2601.17768)
- [vLLM batch-invariance issue](https://goodfirstissue.org/vllm-project/vllm/issues/27433)
- [llm-d CPU offload](https://llm-d.ai/docs/guide/Installation/tiered-prefix-cache/cpu)
- [LMCache](https://arxiv.org/pdf/2510.09665)
- [FP8 RULER study (mirror)](https://www.plushcap.com/content/huggingface/blog/huggingface-fp8-kv-cache-on-intel-arctm-pro-b70-2-capacity-with-strong-long-context-throughput-gains)
- [Lossless compression of K/V caches](https://arxiv.org/html/2508.19263v1)

IDEA 3
NAME: Turn-granular reversible KV eviction
MECHANISM: Anchor kept: a query-agnostic score in the style of KVzip decides which ~30% of the FP8 KV stays on the GPU, and the evicted pages stay in CPU memory where they can be recalled, not deleted. The repair moves recall from every decode step to once per user turn. When a new message arrives, its query vectors are scored against page summaries (min/max keys, about 1% of HBM) and the top 10% of offloaded pages are fetched in one ~8 ms burst that overlaps the message's prefill. A per-step Quest-style "valve" is capped at ≤0.36% of the context per step. This cuts PCIe load from 25.8× the step time (the killed design) to 0.08×. At 32K context that is 64 vs 26 active users per H100 and 2.49× decode tokens/s over FP8-full. Turn-start reload from CPU drops from 84 to 34 ms. The binding quantity is the residency-scoring cost: the design only pays if scoring costs ≤0.29× prefill on trace-average turns (7.6K new tokens), or the turns are short follow-ups on a shared context. So the residency score has to be cheap (an observation window or KVzip's static head-level score), not KVzip's full context-reconstruction pass.
VALUE: In multi-turn shared-context chat (≈500 new tokens per turn) it costs 0.49–0.61× the GPU-seconds per request of FP8-full; on document-heavy turns with full KVzip scoring it costs 1.5–2.2× and loses.

IDEA 4
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
