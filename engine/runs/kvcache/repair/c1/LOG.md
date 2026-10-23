# LOG (one line per round)
| # | idea | change | decisive number | result |
|---|------|--------|-----------------|--------|
| 1 | I1 | baseline check: Mooncake-conv hit curve (FACT 11), per-GPU private CPU tier | hit 0.121 (GPU APC) -> 0.165 (+CPU); 1.03x/request | FAIL in chat regime |
| 2 | I1 | node-shared CPU pool (8 GPUs x 200 GB) / +NVMe | hit 0.315 / 0.374; 1.17x / 1.24x vs GPU APC | WOUNDED (=LMCache practice) |
| 3 | I1 | add lossless exponent coding (SplitZip-style 1.32x) to tier | +0.03 hit, 1.17->1.205x | marginal; known (SplitZip, 2605.01708) -> optional only |
| 4 | I1 | move to agentic regime: S sessions x 30-60K ctx, working set >> HBM, HBM-limited batch | 2.04x (30K) / 2.19x (60K) GPU-s per request vs GPU APC; load 0.15-0.30 s vs prefill 1.4-3.8 s | WORKS in regime |
| 5 | I1 | consistency: NVMe write endurance if spill-all | 3.2-3.9 DWPD > 1 DWPD -> second-hit admission: ~1.0-1.2 DWPD; DRAM-first | fixed by design |
| 6 | I1 | "bit-identical": batch-invariant mode costs 34-56% throughput | breakeven needs >1.52-2.27x gain -> replace with sampled shadow-recompute audit + block digests | ~1.3-1.4% cost at 1% audit |
| 7 | I2 | evidence: TRT-Edge-LLM says Qwen2.5-7B FP8-KV loss is from very large last-layer KV | predicts f=1/28 for Qwen-family (R1-Distill-Qwen-7B is Qwen2.5 arch) | anchor regime found |
| 8 | I2 | compute gated memory: R1-Distill 1 layer BF16 at 32K | 1.93x KV capacity & decode tok/s vs BF16 fallback (FP8-all 2.00x) | WORKS if failure is layer-local |
| 9 | I2 | Gemma-3-1B: only 4 global layers carry KV | gate 1 global layer -> 1.53x; all 4 -> 1.00x | NICHE/weak on few-global hybrids |
| 10 | I2 | add two-arm probe (stock FP8 kernel vs fake-quant BF16 attention) to separate kernel bug (FACT 6) from format/layer error; teacher-forced decode KL for long-CoT | probe 9 GPU-min ($0.38); falsifier n=870 paired RULER items for 3-pt gap | repaired |
