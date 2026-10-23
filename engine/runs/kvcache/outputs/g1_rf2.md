# Answer: for shared prefixes, exact reuse beats any lossy cache, so the real question is load vs recompute

**Criteria.** The figure of merit is GPU-seconds per request at zero quality change. The baseline is stock vLLM prefix caching with an FP8 KV cache, not FP16. For workload D, reuse is the only lever that is bit-exact on any decoder-only model.

**Crossover (my roofline estimate; nothing measured).** These use the ledger's H100 assumption of about 500 TFLOPs effective.

- **Llama-3.1-8B KV size.** 32 layers × 8 KV heads × 128 dims × 2 (K and V) = 128 KB per token in BF16, or 64 KB in FP8.
- **Recompute cost per prefix token.** About 16 GFLOP for the linear layers, plus about 5 GFLOP of attention at an average position of 10K. That is about 42 µs per token.
- **Break-even bandwidth.** Loading wins when the link is faster than 128 KB / 42 µs ≈ 3 GB/s (BF16), or about 1.5 GB/s (FP8).
  - PCIe Gen5 and local NVMe (7 GB/s or more) win clearly.
  - 25 GbE (about 3 GB/s) is roughly break-even for BF16.
- **Effect of prefix length.** Attention cost grows with position, so break-even bandwidth falls as prefixes get longer. Below about 2K tokens it rises to about 4 GB/s.
- **Effect of model size.** For 70B (327 KB per token against about 280 µs per token), break-even drops to about 1.2 GB/s.

**Ceiling.** In D, at hit rate h, cost ≈ 1 − 0.66·h. At h = 0.9 that is about 2.5×. Reaching 3× needs h above 1, so prefill reuse alone cannot get there.

**Where it stops working.**
- Misses: only the lookup is wasted.
- Hybrid or sliding-window models: Mamba state cannot be split mid-block, so they need per-architecture state snapshots.
- Non-prefix reuse cannot be done exactly.
- The tier capacity has to hold the working set. One 20K FP8 prefix is 1.3 GB, so 1 TB of DRAM holds about 770 of them.

**For the original question.**
- A and B: FP8 KV is the only lossless plug-in. Tests show it degrades on DeepSeek-R1-Distill-Qwen-7B and Gemma-3-1B.
- Eviction and sub-4-bit methods fail in multi-turn and long-reasoning workloads. See the SCBench and vLLM TurboQuant results cited in the brief.

=== IDEAS ===
IDEA 1
NAME: FP8 tiered exact-prefix store
MECHANISM: Store the FP8 KV blocks the model already produces, hash-keyed by prefix, in GPU, then DRAM, then NVMe, and load them layer by layer, overlapped with compute. The closest earlier attempt is CacheGen; it needed a codec and won only at low bandwidth, whereas this keeps the native FP8 bytes, so a hit gives exactly what recompute would give with no decoder kernel. The deciding quantity is link bandwidth against about 1.5 GB/s for 8B (64 KB/token ÷ about 42 µs/token). It is falsified if TTFT on hits over NVMe is not at least 3× lower than vLLM's GPU-only prefix cache at a matched hit rate.
VALUE: Gives a bit-identical, any-dense-model cut of up to about 2.5× in GPU-seconds for RAG and multi-turn at hit rates near 0.9.

IDEA 2
NAME: Bandwidth-balanced split load/recompute
MECHANISM: For each hit, choose a split point p: load KV for tokens [0,p) over the link while the GPU recomputes [p,n) from that KV as it arrives, picking p so both finish together using measured link and FLOP rates. The closest earlier attempt is Cake (2024); it is the same idea, without validation on GQA models or SSD tiers, and this design adds per-request re-estimation under batch load. The deciding quantity is the ratio of link time to compute time per token. It is falsified if TTFT is not at least 1.3× better than the better of pure-load or pure-recompute when the link is between 1 and 4 GB/s.
VALUE: Makes reuse pay off over slow network or remote storage links where pure loading only breaks even.

IDEA 3
NAME: Recompute-cost-per-byte store eviction
MECHANISM: Score each stored prefix by (expected reuses × FLOPs saved) ÷ bytes held. Long prefixes score higher because attention cost is superlinear, and expected reuses decay with time since last hit. Evict the lowest scores first, instead of LRU. The closest earlier attempt is CacheBlend, which raised effective hits through approximate non-prefix reuse; this design stays exact by raising the exact hit rate. The deciding quantity is the working set against tier capacity. It is falsified if, on a replayed RAG or chat trace, the hit-weighted FLOPs saved are not at least 15% above LRU at equal capacity.
VALUE: Raises the exact-reuse hit rate h, which sets the 1/(1−0.66h) gain, without changing any model output.