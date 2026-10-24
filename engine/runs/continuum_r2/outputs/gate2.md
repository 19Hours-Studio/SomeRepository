=== GATE ===
IDEA 1: Fusion-enforced LPDDR training die
KILLER | LPDDR price per GB needed for the "1.5–2× cheaper per training FLOP" claim. The claim assumes removing HBM removes its cost, but 256 GB of LPDDR replaces 192 GB of HBM. | required ≤ $3.9/GB for 1.5× (die about $600 + substrate/test about $300 + 256 GB, all over 2 dense FP8 PF; compared with B200 at $6.4k / 4.5 PF = $1.42k/PF) | available about $10/GB, with Q2-2026 contracts at about $19/GB (SemiAnalysis via Wccftech; TrendForce up 78–83% QoQ) | MARGIN 0.39 (0.2 at Q2-26 prices)
CHAIN | B200 (4.5 PF dense FP8, 1 kW, $6.4k BOM per the ledger) in FP8/BF16 3D-parallel training | now $1,420 BOM per dense FP8 PF; 0.22 W/TF | with idea $1,730–3,010 per PF at $10–20/GB; 0.30 W/TF; 2.25× more chips and links per FLOP | RATIO 0.6 (0.47–0.82)
VERDICT | DEAD | In 2026 LPDDR costs about the same per GB as HBM (B200 HBM is about $2,900 / 192 GB ≈ $15/GB), so taking out HBM and CoWoS removes none of the memory cost, and the die is worse per FLOP and per watt than B200, let alone Rubin.
NEW FACT | LPDDR5 contract price is about $10/GB, roughly 3× its Q1-2025 level. TrendForce reported LPDDR5X ASP up 78–83% QoQ in 2Q26, and long-term agreements are reportedly signed with a ceiling of about $21/GB. | https://wccftech.com/mobile-dram-prices-expected-to-increase-by-100-quarter-over-quarter-as-long-term-agreements-now-getting-signed-at-prices-as-high-as-21-gb/amp/

IDEA 2: Line-rate lossless exponent coding
KILLER | Lossless compressed size of FP8 E4M3 tensors with 128×128 block scales | required ≤ 0.85 of original size (savings ≥ 15%) | available 0.81–0.86 measured (whole-byte entropy 0.810 Gaussian, 0.854 heavy-tailed t3), i.e. about 17% savings. I checked the measurement on BF16 first: it gives 0.66–0.67, against DFloat11's real-model about 0.70. The literature agrees: ZipNN-FP8 reaches 83% of original size, ECF8 saves up to 26.9%. (my measurement in fp8_entropy.py; arXiv 2508.19263, 2510.02676) | MARGIN 1.1 on FP8 weights. For NVFP4 tensors it is about 0: I measured 0.99, so nothing to compress.
CHAIN | Decode on HBM GPUs with FP8 weights and FP8/NVFP4 KV, where HBM streaming is about 50% of energy (ledger C) | now 1.00 | with idea 0.5 + 0.5×0.83 = 0.915. This falls toward 1.0 as weights and KV move to NVFP4 on Rubin-class parts, and block-granular random access (for example paged KV) reduces the gain further. | RATIO 1.09
VERDICT | DEAD | The coding works on FP8 weights with almost no headroom, but at system level the gain is only about 9%. It disappears on the FP4 formats that current hardware is moving to, so the 3% of die area does not reach the 1.1 bar.
NEW FACT | E2M1 codes with per-16-element block scales have 0.99 of maximum entropy (my measurement on Gaussian weights), so NVFP4 tensors are essentially incompressible losslessly. ECF8 puts the theoretical FP8 limit at about FP4.67. | fp4_entropy.py (my measurement); https://arxiv.org/html/2510.02676v1

IDEA 3: Indexer-gathered tiered KV decode
KILLER | Sustained LPDDR6 efficiency on random 656-B gathers | required ≥ 50% of peak | available about 75% (analytic, not simulated). One gather takes 41 ns on a 12-bit, 10.667 Gb/s subchannel (16 GB/s). The activate limit (4 ACT per tFAW of about 20 ns) allows about 131 GB/s, far above the bus rate, so the gathers are bus-bound. Burst alignment wastes little (97.6% at 32-B bursts), leaving refresh and turnaround as the main losses. This number needs confirming in a DRAM simulator such as Ramulator2 or DRAMsim3. (JEDEC LPDDR6 subchannel width and rate; idea_math.py) | MARGIN 1.5
CHAIN | GB200/B200 serving DeepSeek-V3.2 with sparse FlashMLA, which already reads only the top-2048 entries from HBM; or the ESS-style software offload of latent cache to CPU memory | HBM-only: about 25 users per GPU at 128K, capacity-bound. ESS: 2.23× throughput at 128K, from simulation. | with idea about 69 users per GPU at 100 tok/s/user (bandwidth-bound: the indexer scan is 1.02 GB per token, against 0.08 GB per token for the gather), so about 2.8× over HBM-only. That is about 1.25× over ESS, before paying for about 350 GB of LPDDR per chip at $10–19/GB. | RATIO 1.25
VERDICT | WOUNDED | The mechanism works and is exact. But against today's sparse-attention kernels, HBM bytes per token fall only 1.08×, not 4.6×, because the full indexer scan dominates. So the claimed "3× cut of the HBM energy term" is wrong. What remains is a capacity gain that software offload on Grace/CPU memory already captures for the most part, and it only applies to DSA-style models.
NEW FACT | ESS (Baidu, Dec 2025) offloads DeepSeek-V3.2 latent cache to CPU memory and keeps the indexer on GPU. In simulation it gains 69.4% throughput at 32K and 123% at 128K. A vLLM RFC proposes top-k onload from CPU. | https://arxiv.org/abs/2512.10576 ; https://github.com/vllm-project/vllm/issues/33980

IDEA 4: Peer-mirrored state for goodput
KILLER | Mirroring traffic per step compared with spare link bandwidth | required about 16 B/param of shard per step: about 16 GB per chip per step for 1T parameters over a 1,024-way shard group, or about 1.6 GB/s at a 10-s step | available about 50 GB/s of spare scale-up link, an assumed half of a 100 GB/s class link | MARGIN about 30
CHAIN | The Llama 3 405B run on 16K H100s, which already had over 90% effective training time with 419 unexpected interruptions in 54 days (MTTF about 2.7 h), plus published in-memory checkpointing and fast-recovery runtimes (TrainMover, GoCkpt) | now goodput ≥ 0.90 | with idea 0.98. That is applied only to the time-proportional share of run cost (hardware 44 + network 13 + energy 4 = 61%), because staff cost does not scale with goodput. | RATIO 1.05 (≤ 1.03 against in-memory checkpointing)
VERDICT | DEAD | The traffic fits easily. But even the idea's own 90→98% goodput claim moves whole-run cost by only about 5%, and software checkpointing already captures part of that.
NEW FACT | Llama 3 pretraining saw 466 interruptions in 54 days (47 planned), and 58.7% of the unexpected ones were GPU issues, including HBM3. | https://arxiv.org/pdf/2407.21783

The scripts are fp8_entropy.py, fp4_entropy.py and idea_math.py in /home/user/SomeRepository/engine/runs/continuum_r2/gate2/; nothing was committed.

Sources:
- [ECF8, arXiv 2510.02676](https://arxiv.org/html/2510.02676v1)
- [ZipNN low-precision, arXiv 2508.19263](https://arxiv.org/html/2508.19263v1)
- [ESS, arXiv 2512.10576](https://arxiv.org/abs/2512.10576)
- [vLLM issue 33980](https://github.com/vllm-project/vllm/issues/33980)
- [TensorRT-LLM DeepSeek-V3.2 on Blackwell](https://nvidia.github.io/TensorRT-LLM/1.3.0rc13/blogs/tech_blog/blog15_Optimizing_DeepSeek_V32_on_NVIDIA_Blackwell_GPUs.html)
- [Wccftech LPDDR pricing](https://wccftech.com/mobile-dram-prices-expected-to-increase-by-100-quarter-over-quarter-as-long-term-agreements-now-getting-signed-at-prices-as-high-as-21-gb/amp/)
- [TrendForce via Hartware](https://www.hartware.de/?p=362715)
- [Llama 3 Herd of Models](https://arxiv.org/pdf/2407.21783)
- [TrainMover](https://arxiv.org/html/2412.12636v2)
- [GoCkpt](https://arxiv.org/html/2511.07035v1)