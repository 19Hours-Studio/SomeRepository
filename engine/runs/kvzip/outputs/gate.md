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
IDEA 5: Per-request online KLT bit-allocation
KILLER | Decode time per token per head. Keys are stored in the KLT basis and RoPE is applied after dequantization, so the 128×128 basis cannot be folded into the query. Each cached key has to be rebuilt with a 128×128 matmul: 32,768 FLOP for 40 B read, or 819 FLOP/byte. The H100 ridge point is 295 FLOP/byte, so this part is compute-bound | required ≤43 ps per token-head (the NVFP4 K+V read time) | available 33 ps at 100% of bf16 tensor peak, 66 ps at a realistic 50% (exact arithmetic: 989 TFLOP/s, 3.35 TB/s; script gate_calc.py) | MARGIN 0.65
CHAIN | NVFP4 KV, 4.5 b/value, Archetype B (ledger shares 50/36/14) | now 0.78 (relative to FP8 KV = 1.00) | with idea 0.72 at peak compute. If KV memory caps the batch and the larger batch spreads weight reads: 0.62 now vs 0.56 with idea | RATIO 1.1
VERDICT | WOUNDED | The 2.5-bit memory saving is mostly lost to the key-rebuild compute that comes from applying RoPE after dequantization, so at realistic tensor-core use decode attention gets slower than NVFP4 (values are fine, since their basis folds into the output). The AM/GM gain on real pre-RoPE keys is still unmeasured and needs a real-model KV dump.
NEW FACT | I checked the AM/GM gain formula on a known case: eigenvalues [4,1] give 0.161 bits. In Archetype B the basis would be estimated only from the short prompt, not from the 32k CoT tokens it later encodes | gate_calc.py (measurement)
IDEA 6: Calibration-free trellis-coded KV
KILLER | Attention-logit MSE at 2 bits relative to 4-bit scalar codes. Logit error equals |q|² × per-dimension key MSE after rotation, so the ratio is the same as the key-MSE ratio | required ≤1.2 × 0.0095 = 0.0114 (Lloyd-Max 4-bit on a Gaussian, measured: 0.009496, matching the textbook value 0.009497) | available ≥0.0625. That is the Shannon D(R)=2^-2R limit at 2 bits, which no code can beat, and QTIP-class trellises sit at about 0.069 (exact; [QTIP](https://arxiv.org/pdf/2406.11235)) | MARGIN 0.17
CHAIN | NVFP4 KV, Archetype B | now 0.78 | with idea about 0.93. This is the memory gain (0.65) plus online Viterbi encoding. At 2^L=65,536 states, 4 branches and 256 steps, that is about 2.6e5 ops per value, or 1.9e10 per token for an 8B model. At batch 10 that adds about 3.2 ms to an 11.3 ms step even at 60 TOPS peak | RATIO 0.84
VERDICT | DEAD | The idea's own criterion fails by 6× even at the rate-distortion limit, and per-token Viterbi encoding costs more than the bandwidth it saves.
NEW FACT | For a 128k-token prefill on a 70B-class model, Viterbi encoding would take about 5.6e15 ops, roughly 94 GPU-s on CUDA cores. That about doubles Archetype A prefill | exact arithmetic from the QTIP Viterbi complexity O(2^L·T), [QTIP](https://arxiv.org/pdf/2406.11235)
IDEA 7: Asymmetric dithered key-value codes
KILLER | Effective number of attended tokens (N_eff) in retrieval heads | required ≥4 by the idea's own text. Matching 4-bit value quality would actually need N_eff about 48: measured 2-bit, group-128, absmax value MSE is 0.30 against 0.0063 for 4-bit group-16 | available about 1. Retrieval heads are defined by their single highest-attention token being copied into the output ([Wu et al.](https://arxiv.org/html/2404.15574v1)), and masking 20 of them drops NIAH from 94.7 to 63.6. A real attention-entropy measurement on a model is still needed | MARGIN 0.25
CHAIN | NVFP4 KV, Archetype B | now 0.78 (0.62 if KV caps the batch) | with idea 0.67 (0.43) | RATIO 1.17 (1.47 if KV caps the batch)
VERDICT | DEAD | Subtractive dither removes bias (measured mean error −9e-5 vs −9e-4) but leaves MSE the same (0.302 vs 0.304), and retrieval heads do not average enough tokens to hide a 6 dB value SNR.
NEW FACT | KIVI K2V2 loses about 13 points on AIME24/25 at 32k generation. Kitty's 2-bit method still loses 3–4 points. MixKVQ shows KIVI-2bit dropping 61.7→50.0 on R1-Distill-Qwen-14B, and KVQuant-2bit falling to 0 | [Kitty](https://arxiv.org/pdf/2511.18643), [MixKVQ](https://arxiv.org/pdf/2512.19206)
IDEA 8: Hadamard-E8 lattice KV
KILLER | AIME24 accuracy change at 32k with 2-bit values | required ≤2 points vs FP16 | available about 3–4 points: the best published 2-bit-class KV result on long CoT (Kitty), with KIVI-2 at 10–15. Also, 2-bit value MSE cannot go below 0.0625 (Shannon), which is about 10× the 4-bit level of 0.0063 (measured) | MARGIN 0.57
CHAIN | NVFP4 KV, Archetype B | now 0.78 (0.62 if KV caps the batch) | with idea 0.66 (0.42). The 256-entry E8P table is shared-memory sized, so it should fit a fused kernel, but the decode overhead has not been measured | RATIO 1.18 (1.49 if KV caps the batch)
VERDICT | WOUNDED | The bit accounting holds (3.06 b keys + 2.06 b values + FP8 sinks and window ≈ 2.6 b, 6.1×) and the rotation is sound, but the 2-bit values are the very component that published long-CoT results penalize. The proposed 2-GPU-hour AIME test on R1-Distill-Qwen-7B is the right deciding experiment and needs a real model.
NEW FACT | E8P is a 2^16-entry, 8-dimensional codebook decoded through a 2^8-entry table, with the other 8 bits used for signs and shifts. That supports the "256-entry table in shared memory" claim | [QuIP#](https://arxiv.org/pdf/2402.04396)

Caveats: I could not reach Hugging Face, so no real KV tensors or benchmarks were run. Every error figure is measured on Gaussian data (`/home/user/SomeRepository/engine/runs/kvzip/gate/c2/gate_calc.py`, checked against the known Lloyd-Max values). Every latency figure is roofline arithmetic. The chain ratios use the ledger's Archetype B shares (KV 50%, weights 36%, other 14%) and ignore kernel overhead except where stated. Two numbers need a real-model run: the eigenvalue AM/GM ratio on real keys (Idea 1) and N_eff in retrieval heads (Idea 3).

Sources: [Kitty](https://arxiv.org/pdf/2511.18643) · [MixKVQ](https://arxiv.org/pdf/2512.19206) · [PatternKV](https://arxiv.org/pdf/2510.05176) · [QTIP](https://arxiv.org/pdf/2406.11235) · [QuIP#](https://arxiv.org/pdf/2402.04396) · [Retrieval Head (Wu et al.)](https://arxiv.org/html/2404.15574v1) · [QRHead](https://arxiv.org/html/2506.09944v1)
