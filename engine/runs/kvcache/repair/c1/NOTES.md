# NOTES (scripts: calc/idea1.py, calc/idea1b.py, calc/idea1c.py, calc/idea2.py)

## Idea 1: Exact-prefix tiered KV reuse
Anchor: reuse KV only on an exact token-prefix match and keep it in the model's native dtype, so it is lossless by construction.
Sources: Mooncake hit curve (FACT 11, pypi llmtrafficlens; Mooncake 2407.00079); LMCache 2510.09665; llm-d CPU-offload benchmark
(Qwen3-32B, mean TTFT 9.0 -> 6.5 s, i.e. -28%, only when KV > HBM); SplitZip 2605.01708 (lossless BF16 KV, 1.32x, 2.18 TB/s decode);
batch-invariant overhead: SGLang 34% (blog, unverified), LLM-42 2601.17768 56%.
Model: Llama-3.1-8B, 131072 B/token; H100 80GB with 52 GB for KV = 0.40M tokens; DGX-class node with 200 GB DRAM per GPU.
Baselines: (a) no caching; (b) vLLM APC, GPU-only (cheapest, free); (c) FP8 KV in GPU to double APC capacity; (d) vLLM OffloadingConnector or LMCache CPU tier.
Results:
- Chat (Mooncake-conv): GPU APC is 1.09x vs no cache. The node CPU tier is 1.17x vs APC. Adding NVMe gives 1.24x. Cost per 1M requests is $228 -> $196.
- Agentic (S >= 32 sessions x 30-60K context, working set 4-40x HBM): 2.04-2.19x GPU-s per request vs GPU APC. Loading 0.95 x ctx takes
  0.15-0.30 s against a full prefill of 1.4-3.8 s. FP8-KV APC alone gives about 1.2-1.5x on the same workload.
Consistency table:
| limit | value | demand | ok? |
| PCIe4 x16 | 25 GB/s | 2.7-3.3 GB/s average, 11-13% duty | ok |
| node DRAM BW | ~600 GB/s | 8 x 3.3 = 26 GB/s | ok |
| node DRAM capacity | 1.6 TB | S x ctx x 131 KB: S=128 x 60K = 1.0 TB | ok up to S~200; S=512 -> hit 0.38 |
| NVMe endurance | 1 DWPD read-intensive | spill-all 3.2-3.9 DWPD | FAIL -> second-hit admission ~1.0-1.2 DWPD, or 3-DWPD drives |
| load hidden? | needs compute >= load | at hit 0.95 the miss-prefill (0.09-0.28 s) < load | load exposed, but scheduler overlaps other decodes |
| exactness | bitwise needs batch-invariant mode | -34..-56% throughput | replaced by an audit (below) |
Repair: DRAM-first tier pooled across the node; NVMe only with second-hit admission; SHA digests on each block to catch tier corruption;
a 1% sampled shadow-recompute audit that compares top-1 token and logit KL against the server's own run-to-run noise floor, costing ~1.3-1.4%.
Optionally, when the deployment runs FP8 KV, store FP8 blocks in the tier: still exact relative to that deployment, and half the bytes.
Deciding unknown: the reuse-distance CDF of the target workload, i.e. the share of reuses whose distance exceeds HBM capacity but fits in DRAM.
Experiment: replay 1 week of real traffic (or SWE-bench agent traces) through a cache simulator. Needs no GPU; at least 10^5 requests.
The audit itself also needs a real-model run of at least 1000 sampled hits to estimate the divergence rate against the noise floor.
Closest work: vLLM APC + OffloadingConnector, LMCache, Mooncake store, CachedAttention/AttentionStore (multi-turn), SplitZip, Continuum (agent TTL).
The anchor is known practice. The new part is the exactness audit replacing batch-invariant mode, plus regime targeting. Verdict: NICHE that WORKS
in agentic/long multi-turn serving (2x); about 1.2x on chat traces.

## Idea 2: Probe-gated per-layer precision
Anchor: a cheap BF16-vs-FP8 probe, run per model, decides which layers keep BF16. Uses stock FP8 kernels and the stock skip-layers flag only.
Sources: FP8 RULER 10-model study (FACT 7); vLLM FP8 blog 2026-04-22 (FACT 6: 128K NIAH 91% -> 13% from FP32 accumulation, fixed;
--kv-cache-dtype-skip-layers); NVIDIA TensorRT-Edge-LLM FP8KV docs (Qwen2.5-7B-Instruct degrades from very large last-layer KV,
model-specific, seen in other frameworks); KVTuner 2502.04420 (layer sensitivity is consistent across prompts; K more sensitive than V).
Configs: R1-Distill-Qwen-7B 28L/4KV/128d; Gemma-3-1B 26L/1KV/256d with sliding 512 (5:1); Llama-3.1-8B 32L/8KV/128d.
Baselines: (a) FP8 everywhere (cheapest; fails on 2/10 models); (b) BF16 fallback (what TRT-Edge recommends when FP8 fails);
(c) vLLM skip only the sliding layers; (d) KVTuner-style mixed int precision (needs custom kernels and a search).
Numbers at 32K: R1-Distill with 1 gated layer gives 1.93x KV capacity and decode tok/s per request vs the BF16 fallback, 96.5% of FP8-all.
2 layers gives 1.87x; 14 layers gives 1.33x. Gemma-3-1B: FP8-all (sliding skipped) 1.85x; 1 global gated 1.53x; all 4 global 1.00x.
Probe: 100 x 32K x 3 arms = 9 GPU-min, about $0.38.
Consistency table:
| limit | value | check |
| gating pays (>=1.1x) | f <= 0.8 for 2/(1+f) | Qwen f=0.036 ok; Gemma f in global-layer units: 1/4 -> 1.53x, 4/4 fails |
| probe power | N=100 detects layer KL > median + 0.3 sd | ok if outlier is strong (last-layer KV outliers are) |
| decode drift | long CoT (R1) accumulates error | the probe adds 512 teacher-forced decode tokens |
| kernel vs format | FACT 6 bug is kernel accumulation | arm B: fake-quant FP8 with BF16 attention; if A bad and B good -> kernel, do not gate |
| memory-bound | decode memory-bound at B<=54 for 7B (0.8 TFLOP/step vs 21 ms memory) | ok |
Hazards: probe KL may not predict RULER multi-hop; tasks outside the probe set (code, JSON) could fail; per-layer gating cannot fix
per-head/channel outliers in MQA Gemma (1 KV head).
Deciding unknown: whether the R1-Distill-Qwen-7B and Gemma-3-1B FP8 losses are layer-local. Experiment: on 1 GPU, RULER 32K, arms BF16 / FP8-all /
FP8+gated / FP8+random-same-f, 870 paired items per arm (3-point gap, 80% power). The idea is falsified if the gated arm does not beat
random-same-f or does not recover to within 3 points of BF16.
Verdict: WORKS for Qwen-family models with outlier layers (if confirmed); NICHE/FAILS for Gemma-3-style few-global-layer models.
