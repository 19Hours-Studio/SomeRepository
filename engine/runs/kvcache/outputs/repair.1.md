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