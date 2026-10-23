=== GATE ===
IDEA 1: Bit-plane on-demand attention precision
KILLER | share of attention mass outside the set read at full precision (top 2% of tokens + 4 sinks + 64 recent tokens), at 32k CoT, under the idea's own rule (tail mass × 2-bit value error ≤ 1e-3) | required tail ≤ 0.38%, i.e. ≥ 99.62% of the mass inside a set of about 655 tokens (measured: reading only the top 2 bit-planes of a rotated 4-bit g32 code gives 0.263 relative RMS error; the quantizer was first checked against a known uniform-data result, 0.00424 vs 0.00444 theory) | available: dropping tokens is lossless on AIME24 with R1-Distill only at a ≥ 4k-token budget even with SeerAttention-R's trained gate, and Quest is still not lossless at 8k, so about 655 tokens cannot reach 99.6% coverage (SeerAttention-R arXiv 2506.08889). As a budget proxy: 655 / 4096 | MARGIN 0.16 (this is a proxy; the real number needs R1-Distill-8B attention dumps on AIME traces)
CHAIN | NVFP4 KV (4.5 bits stored and read), archetype B, batch 10 | now 64.1 cost units (FP16 baseline = 100) | with idea 58.1 (2.54 bits read; HBM footprint is 4.5 bits, so no capacity gain over NVFP4) | RATIO 1.10 (1.20 if batch grows to fill freed HBM)
VERDICT | DEAD | The coverage it needs from the top 2% is above what published long-CoT sparsity data supports, and even if that held it saves only about 10–20% over NVFP4 because it stores as many bits.
NEW FACT | KIVI-K2V2 loses 7.35 points on average across reasoning benchmarks on Qwen3-8B, so a 2-bit tail is not harmless for CoT | arXiv 2511.18643 (KITTY)

IDEA 2: Coarse-HBM, refined-host residual
KILLER | PCIe time per decode step to fetch the top-256 residuals, against the HBM read time saved compared with NVFP4 (archetype B, 8B, batch 10, 32k). Each layer's top-k depends on that layer's query, so the fetch cannot be prefetched | required ≥ 1.25 ms/step of saving to pay for 41.9 MB/step over PCIe5 (4.2 MB per request, which matches the idea's 10.5 MB for 70B; assumed about 45 GB/s effective for 64-B gathers, plus 32 dependent per-layer hops at about 10 µs) | available 0.90 ms/step saved (NVFP4 1.8 ms vs 2.25-bit 0.9 ms HBM KV read; 21.5 GB average FP16 KV at 3.35 TB/s) | MARGIN 0.72
CHAIN | NVFP4 KV, archetype B | now 64.1 units | with idea 66.8 (PCIe adds 9.8 units; it does halve the HBM footprint) | RATIO 0.96 (0.98 with batch growth)
VERDICT | DEAD | The PCIe residual fetch costs more decode time than the 2-bit HBM reads save over NVFP4, and the quality gain comes from only 256 of 131k tokens (0.2%).
NEW FACT | The closest competitor is KITTY, which gets about 8× lower KV memory (2-bit plus dynamic high-precision key channels) with near-zero loss on Qwen3 and LLaMA3 and 2.1–4.1× throughput, all in HBM with no host fetch | arXiv 2511.18643 / MLSys 2026

IDEA 3: Progressive bit-plane attention
KILLER | attention mass covered by the top 2% of pages on long CoT (the idea's own threshold) | required ≥ 99% at a 2% budget | available: drop-safe budgets on R1-Distill AIME24 are ≥ 4k of 32k tokens (≥ 12.5%), and Quest is not lossless at 8k (SeerAttention-R arXiv 2506.08889; LessIsMore arXiv 2508.07101 needs 2K for Qwen3-8B) | MARGIN 0.16 (budget proxy; non-selected pages still get 2-bit reads, so a real-model mass measurement would decide it)
CHAIN | NVFP4 KV, archetype B | now 64.1 units | with idea 57.7 (2.2 bits read × 1.125 two-pass overhead; 4.3 bits stored, so no capacity gain unless planes are offloaded) | RATIO 1.11 (1.23 with batch growth)
VERDICT | DEAD | Its 99%-coverage-at-2% condition fails by about 6× on published long-CoT budgets, and the best-case gain over NVFP4 is about 11–23%.
NEW FACT | Under Hadamard rotation, NVFP4's relative RMS error is 0.097 (measured, synthetic Gaussian with 4 outlier channels), against 0.32–0.38 for 2-bit, so the base plane is about 3.5× noisier than the NVFP4 bar | gate.py measurement

IDEA 4: Entropy-measured per-head bit allocation
KILLER | share of KV heads that can be K4V4 within a 2.1-bit average (group-128 FP16 scale/zero, 0.25 bit/value, a favourable assumption) | required ≈ 50% of heads at full fidelity for GQA Llama-3-8B to match full attention on NIAH (DuoAttention README) | available 14% (exact arithmetic: K2V1 = 1.75, K4V4 = 4.25 bits; a 50/50 split costs 3.0 bits) | MARGIN 0.28
CHAIN | NVFP4 KV, archetype B | now 64.1 units | with idea 56.6 (2.1 bits stored and read) | RATIO 1.13 (1.37 with batch growth)
VERDICT | DEAD | The 2.1-bit budget leaves room for only 14% retrieval-grade heads where GQA models need about 50%, and 1-bit min-max values give 1.31 relative RMS error (measured), worse than zeroing the value.
NEW FACT | DuoAttention itself saves only 1.65× memory on GQA; CateKV reports its accuracy drops sharply below a 0.3 retrieval-head ratio; KVTuner finds 3.25 bits (Llama-3.1-8B) and 4.0 bits (Qwen2.5-7B) is the near-lossless floor for layer-wise mixed precision | arXiv 2410.10819; arXiv 2608.30295; arXiv 2502.04420

All four ideas fail the gate. Three cautions about how solid that is:
- **Real-model data needed for ideas 1 and 3:** both margins are a proxy. They rest on token budgets at which dropping tokens is lossless; these ideas read the remaining tokens at 2 bits rather than drop them. Dumping R1-Distill-8B attention on AIME traces and measuring the mass in the top 2% would settle it, and that cannot be run here.
- **Assumptions in idea 2's margin:** the 45 GB/s PCIe figure and the 10 µs per-layer hop are my estimates, not measurements.
- **Synthetic inputs:** all quantizer errors were measured on rotated Gaussian data, not real KV tensors.

Files are in `/home/user/SomeRepository/engine/runs/kvzip/gate/c1/`:
- gate.py
- gate_out.txt

Sources:
- [KITTY arXiv 2511.18643](https://arxiv.org/abs/2511.18643v1) / [MLSys 2026](https://proceedings.mlsys.org/paper_files/paper/2026/file/e4d8d1b5120be349d3fff8878650cf45-Paper-Conference.pdf)
- [SeerAttention-R](https://arxiv.org/pdf/2506.08889)
- [LessIsMore](https://arxiv.org/pdf/2508.07101)
- [Quest](https://arxiv.org/html/2406.10774v2)
- [DuoAttention](https://arxiv.org/pdf/2410.10819), [README](https://raw.githubusercontent.com/mit-han-lab/duo-attention/main/README.md)
- [CateKV](https://arxiv.org/pdf/2608.30295)
- [KVTuner](https://arxiv.org/pdf/2502.04420)
- [ZipCache](https://arxiv.org/pdf/2405.14256)
- [Twilight](https://arxiv.org/html/2502.02770)
- [NVIDIA NVFP4 KV blog](https://developer.nvidia.com/blog/optimizing-inference-for-long-context-and-large-batch-sizes-with-nvfp4-kv-cache/)