**Short answer:** No KV design is best everywhere. Only exact prefix reuse keeps outputs bit-identical. FP8 KV is the safe default on dense GQA models only. Every lower-bit or eviction method trades away quality on some workload. "Any model" is not supported: nothing in the sources was tested on hybrid or state-space models, and FP8 already degrades DeepSeek-R1-Distill-Qwen-7B and Gemma-3-1B (vLLM FP8 blog).

**Criteria and where each one matters**

| Workload | Metric | Room (ledger) | KV verdict |
|---|---|---|---|
| D: RAG / shared prefix | GPU-s per request | 2.46× from a 10× prefill cut | Exact reuse is the biggest lever |
| A: 128K single request | GPU-s per request | 1.29× from decode KV read | Low-bit plus re-promotion |
| B: short-context serving | tok/s per GPU | KV is ~12% | KV design barely matters; weights dominate |
| C: hosted API | $/turn | 30% margin, ceiling 3.3× | No engineering room |

**Deciding number for reuse (D).**
- Loading KV over PCIe: 128 KB per token at ~50 GB/s (my assumption) ≈ 2.6 µs per token.
- Recomputing it: ~16 GFLOP per token at the ledger's assumed 500 TFLOPs ≈ 32 µs per token.
- So loading is about 12× cheaper than recompute, and reuse pays whenever the hit rate is above about 10%.
- Supporting evidence: Oracle/LMCache reported ~2× throughput and ≥50% TTFT cut, a vendor figure for one setup.

**Where things fail**
- **Reuse:**
  - Unique prompts, or a low hit rate.
  - Edited prefixes; CacheBlend handles these, but it is lossy and was shown on only 3 models.
  - Recurrent-state models, whose state cannot be split at arbitrary token boundaries.
- **2-bit KV (KIVI):** shown only on Llama-2, Falcon and Mistral. 3-bit variants dropped accuracy on reasoning and long context (vLLM TurboQuant study).
- **Eviction:** degrades even at 10% eviction on later queries (KVzip paper). SnapKV scores 0 F1 on long outputs (RefreshKV).

**Required tests**
- Benchmarks: RULER at 128K, SCBench multi-turn, a long-reasoning set, and multi-query reuse.
- Compare at matched memory against FP8, not against BF16.
- Models: Llama-3.1-8B, Qwen2.5, Gemma-3, R1-Distill, and one hybrid model.

I ran no experiments. The A/B/D cost splits come from a roofline estimate, not a profile.

=== IDEAS ===
IDEA 1
NAME: Exact tiered prefix store
MECHANISM: Hash fixed-size token blocks of each prompt and keep their FP8 key/value tensors in GPU, CPU and SSD tiers. On a later request with a matching block chain, stream those blocks back instead of recomputing them, overlapping the transfer with prefill of the unmatched suffix. Unlike CacheGen or CacheBlend, nothing is lossily encoded or approximately stitched, so outputs match the uncached run. The deciding quantity is hit rate × prefix length × (recompute time − load time), roughly 32 µs versus 2.6 µs per token for an 8B model.
VALUE: Up to about 2.5× fewer GPU-seconds on shared-prefix RAG and chat, with outputs identical to the uncached run. The hypothesis is falsified if, measured against the same stack with prefix caching off, end-to-end throughput gains less than 1.5× at a 50% hit rate.

IDEA 2
NAME: Query-refreshed two-precision cache
MECHANISM: Keep every token in HBM at 2 bits (keys per-channel, values per-token), with an exact FP8 copy held in CPU memory. At each new query or turn, score pages by their min/max key bounds against the query, and promote the top ~10% back to FP8 in HBM in about 0.2 s. Unlike SnapKV or H2O, no token is dropped, so later turns can recover pages that the first query ignored. The deciding quantity is the RULER/SCBench gap at matched memory versus all-FP8.
VALUE: About 3× smaller decode KV at 128K context while staying safe for multi-turn use. The hypothesis is falsified if the loss exceeds 1 point versus FP8, or if it fails on long reasoning outputs where the relevant pages shift during decode.

IDEA 3
NAME: Probe-gated per-layer precision
MECHANISM: Run about 100 long prompts once with BF16 KV and once with FP8 KV, and measure per-layer attention-output error and final-logit KL divergence. Layers above a threshold stay in BF16; all others use stock FP8 kernels, so no custom datatypes are needed, unlike KVQuant. The deciding quantity is whether probe KL predicts the RULER loss.
VALUE: Turns "FP8 everywhere" into a model-checked default, with no weight changes. The hypothesis is falsified if the gated layers fail to restore RULER accuracy on Gemma-3-1B or R1-Distill.