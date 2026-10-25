=== REVIEW ===
IDEA 1: Detached attention-stack memory nodes
DEFECT | MAJOR | The 49 tok/s per user depends on the stack delivering 84% of its peak HBM bandwidth nonstop, while it sits next to a 13–19 W logic die under 16 DRAM layers. Hot DRAM needs more refresh, which takes bandwidth away. | Llama-3-70B-class GQA at 128K FP8 KV is 21.47 GB per user. 2 users × 49 tok/s × 21.47 GB = 2.10 TB/s, which is 84% of 2.5 TB/s. At a realistic 75% it is 43.7 tok/s per user. Stack power is about 34–50 W of DRAM (2.1 TB/s at 2–3 pJ/bit) plus 13–19 W of base die.
DEFECT | MAJOR | The "1,200–1,500 users per Rubin" means 600–750 separate stacks, each with its own substrate, link port, power and cold plate. The 400 lower bound does not match the user count. Per-node overhead such as switch ports and boards does not appear in a cost of goods dominated by HBM. | 1,200 users ÷ 2 per stack = 600 stacks, not 400. One NVL72-equivalent would need 72 × 750 = 54,000 network endpoints.
DEFECT | MINOR | SPHBM4 (JESD330-4) defines a 512-bit, 22.4–46 GT/s substrate interface to a nearby host, using a JEDEC PHY/buffer base die. It is not a network link, and a custom attention base die with a NIC/SerDes is not SPHBM4-compliant. | [JEDEC SPHBM4, Tom's Hardware](https://www.tomshardware.com/pc-components/dram/jedec-releases-new-sphbm4-standard-to-slash-ai-memory-costs-narrow-512-bit-interface-enables-dropping-expensive-interposers-for-organic-substrates)
DEFECT | MINOR | The baseline is plain Rubin with FP8 KV. A competent operator at 128K would also use FP4 KV, or an MLA or sparse-attention model, and either one removes most of the KV-bandwidth problem this idea solves. | DeepSeek V3.2 DSA attends to 2,048 tokens per query, which is 64× fewer than 128K ([arXiv 2512.02556](https://arxiv.org/pdf/2512.02556))
SURVIVES | These reproduce: the 8,192:1 KV-to-link byte ratio, the 0.26 GB/s link, the 33% energy saving (5.34 → 3.58 pJ/bit), the 33.7 TFLOP/s FP8 per stack (fits 13–19 W), and Rubin-only being capacity-bound at about 7–10 users per GPU.
RATIO | ~1.45 | Their 1.7× derated for 75% instead of 84% sustained bandwidth on the stack portion, which is about 90% of the cost.
KNOWN | yes | AttAcc, ASPLOS'24: PIM attention plus an xPU running the FC layers, 2.81× performance and 2.67× energy ([UIUC](https://experts.illinois.edu/en/publications/unleashing-the-potential-of-pim-accelerating-large-batched-infere/)). NeuPIMs and Lamina-style attention offloading are close relatives.
NEW FACT | HBM4 12-high 36 GB stack is about $600 in 2026, forecast about $1,300 in 2027 (secondhand TrendForce figure). | [Silicon Analysts](https://siliconanalysts.com/market/trendforce-lifts-2027-hbm-asp-forecast-to-121-hbm4-stack-seen-doubling-to-1-300-2026-10-01)

IDEA 2: SRAM-stacked weights, HBM4 only for KV
DEFECT | MAJOR | 10 GB of SRAM per package does not fit under two 800 mm² compute dies. If the base dies only cover the compute-die footprint, the 64-package rack holds 299 GB, which is less than the 377 GB of weights. | At 31.8 Mib/mm² and 70% array efficiency, 800 mm² gives 2.33 GB per compute die and 4.67 GB per package. 10 GB needs four base dies of about 857 mm² each, which is the reticle limit, with no area left for the TSV power path feeding a ~1 kW die. Fitting the weights takes at least 81 packages, or about 486 HBM stacks, which wipes out most of the per-stack lead over Rubin's 576.
DEFECT | MAJOR | "Rubin with today's measured software cannot reach ≥200 tok/s/user" ignores speculative decoding and MTP, which DeepSeek-V3 ships natively. | 8×B200 already exceeded 250 tok/s/user on DeepSeek-R1 at concurrency 1 ([NVIDIA](https://developer.nvidia.com/blog/nvidia-blackwell-delivers-world-record-deepseek-r1-inference-performance)).
DEFECT | MINOR | tok/J × 1000 should equal tok/s per kW, but the figures use different power boundaries, and the boundary for each chip is different. | 7.75 tok/J implies 115 kW against the 144 kW rack (80%). Rubin's 6.5 tok/J implies 135 kW against 207 kW (65%). On one consistent wall-power basis the lead is 1.47×, not 1.2×.
DEFECT | MINOR | "The dense SRAM cell stayed at 0.021 µm² from N5 to N2" is wrong. | N2 HD bitcell is about 0.0175 µm² (−17%), 38.1 Mb/mm² ([semiwiki](https://semiwiki.com/forum/threads/sram-scaling-isnt-dead-after-all-%E2%80%94-tsmcs-2nm-process-tech-claims-major-improvements.21363/latest)). N5 is still cheaper per bit.
DEFECT | MINOR | The 5,300 users at 128K is a capacity figure only. Bandwidth limits them to about 70 tok/s each. | 15 TB/s ÷ (82.8 users × 2.59 GB) = 69.9 tok/s, which needs 12.9 PF of FP8 per package.
SURVIVES | These reproduce: 377 GB of weights, 19.76 KB per token MLA KV at 4.5 bits, 2.59 GB per user, 13.8 TB of HBM, 384 vs 576 stacks, and the throughput behind both rack figures (892.8k vs 875k tok/s).
RATIO | ~1.1 | After resizing to about 81–100 packages, or near-reticle base dies, so the weights fit.
KNOWN | partly | AMD MI300X puts N5 compute dies hybrid-bonded on top of N6 base dies with 256 MB Infinity Cache. Groq 3 LPU has 500 MB SRAM per chip ([StorageReview](https://www.storagereview.com/news/nvidia-groq-3-lpx-everything-we-know)).

IDEA 3: Continuum-D: SRAM weights, LPDDR KV
DEFECT | MAJOR | The stated energy does not follow from the stated power and throughput. | 117 kW ÷ 414k tok/s = 0.283 J/token, not 0.19–0.20. That is about 57% worse than Rubin, not 9%.
DEFECT | MAJOR | The headline 2.8× is against Rubin NVL72 at ≥1000 tok/s/user, a configuration that Idea 6 of the same design says "no Rubin setup reaches". | Idea 3 prices Rubin at $0.214 at this speed. Idea 6 says Rubin is infeasible above about 639 tok/s/kW at 10 µs per layer.
DEFECT | MINOR | The 1 TB/s of LPDDR6 needs 12.8 Gbps on all 26 x24 channels. Launch-speed parts give 0.83 TB/s, which cuts the bandwidth ceiling to about 427k tok/s, a 3% margin. | 26 × 24 × 10.667 Gbps / 8 = 0.832 TB/s
DEFECT | MINOR | The weights are not replicated across the 333 dies, so any single die or board failure takes down the whole model instance. | At the 0.04–0.11 failures per die-year seen on GPU fleets, 333 dies give about 13–37 full-system interruptions a year.
SURVIVES | These reproduce: 428 mm² of SRAM, 416 GB total, 631 GFLOP per token at 32K (60% MFU at 414k), 514k tok/s from LPDDR, and capex plus power of about $0.057/Mtok, so $0.077 is plausible.
RATIO | ~2.6 | Against a Rubin price for a speed Rubin may not reach. With the energy corrected, cost is about $0.081/Mtok.
KNOWN | partly | Groq and Cerebras keep weights in SRAM. Combining SRAM weights with LPDDR KV on standard-packaged dies is not a shipping product.
NEW FACT | Rubin CPX was dropped from NVIDIA's roadmap at GTC 2026. An HBM4 revival (168 GB) has been reported but is unconfirmed. | [TheElec](https://www.thelec.net/news/articleView.html?idxno=10763), [TechPowerUp](https://www.techpowerup.com/352213/nvidias-rubin-cpx-gpu-reborn-with-hbm4-memory-no-more-gddr7)

IDEA 4: Layer-pipelined LPDDR prefill dies
DEFECT | MAJOR | The 1.20× lead over the "revived HBM4 Rubin CPX" is measured against a product whose existence, spec and price are an analyst rumour. | Removed at GTC 2026; HBM4 redesign reported via Ming-Chi Kuo only (sources above).
DEFECT | MINOR | The 45K-token compute-bound threshold holds only if absorbed-MLA attention FLOPs are counted. DeepSeek's prefill uses the non-absorbed form. | Linear layers alone cross over at 131K tokens. Counting absorbed attention it is 38K; counting non-absorbed attention it is 58K. At 45K non-absorbed: 26.6 ms of compute against 34.3 ms of weight reads.
DEFECT | MINOR | A 1,024-bit LPDDR5X at 10.7 Gbps is twice the width and twice the speed of Grace's 512-bit LPDDR5X. LPDDR contract prices also rose in 2026, which squeezes the cost lead. | 1024 × 10.7 / 8 = 1.37 TB/s
SURVIVES | These reproduce: 910 FLOP/B at 8K tokens, 47 GB per die, 2.4 GB/s of KV egress, a TTFT of about 0.65–0.69 s at 50% MFU, and small inter-die activation traffic (about 8 GB/s in BF16).
RATIO | ~1.15 | Their 1.27× against Rubin, minus LPDDR price inflation and the uncertainty in die cost.
KNOWN | yes | Rubin CPX was a prefill-only part with no HBM; Splitwise and DistServe do prefill/decode disaggregation; FlexGen uses a layer-major schedule.

IDEA 5: Same die, separate training/prefill SKU
DEFECT | MAJOR | A compute die built to be hybrid-bonded face-down onto SRAM base dies, with power and I/O through those dies, cannot simply drop them. It needs a passive base die or a different top-metal and bump tapeout. So "same die" is not physically the same die. | Same mechanism as MI300's XCD, which only works on its IOD.
DEFECT | MINOR | Each Continuum-T package uses 8 HBM4 stacks at 0.6–0.85× Rubin. That makes it worse per HBM stack, which is the scarce resource the design itself chose as a metric. | 8 stacks, the same as Rubin, for 0.6–0.85× the output
SURVIVES | These hold up: there is no training lead and that is honestly stated. Weight-only NVFP4 PTQ of DeepSeek-class checkpoints is shipped by NVIDIA with small accuracy loss. FP4 KV is not similarly proven.
RATIO | ~0.7 | Their own 0.6–0.85× training estimate
KNOWN | yes | TPU and Trainium families split training and inference SKUs on a shared toolchain. The PyTorch/StableHLO path is used by XLA and others.

IDEA 6: Deterministic, compiler-scheduled low-latency scale-up fabric
DEFECT | MAJOR | The GPU per-layer floor is taken from DeepEP over InfiniBand across nodes, not NVLink within a rack. All GPU and Cerebras baselines also ignore speculative decoding. | DGX B200 measured 1,038 tok/s/user on Llama 4 Maverick (400B MoE) with EAGLE-3 ([NVIDIA](https://developer.nvidia.com/blog/blackwell-breaks-the-1000-tps-user-barrier-with-metas-llama-4-maverick)). Cerebras's 2,100 tok/s uses speculative decoding ([changelog](https://inference-docs.cerebras.ai/change-log)). Correcting for about 2.5 accepted tokens per step, its implied cost is about 21 µs per layer forward, not 10.
DEFECT | MAJOR | The ≤6 µs per layer target is assumed, not demonstrated. At 1000 tok/s/user the whole layer budget, compute included, is 16.4 µs. | 1 ms ÷ 61 layers = 16.4 µs
DEFECT | MINOR | "Batch 4096 needs only 0.1 TB/s" is wrong by about 6.7×. At 4096 the per-layer serialization alone uses the full 6 µs. 0.1 TB/s corresponds to batch about 573. | At batch 4096: 64 tokens/package, 0.67 TB/s average, 6.1 µs per layer at 1.8 TB/s. At batch 573: 0.094 TB/s and 0.86 µs.
DEFECT | MINOR | Fixed all-to-all slots must be sized for the hottest package or tokens get dropped. Poisson load alone needs +35% headroom, and real expert skew needs more. DeepSeek-V3 does not drop tokens. | Mean 71.6 assignments per package, expected max about 97
SURVIVES | These reproduce: DeepEP's 77–194 µs dispatch and 114–369 µs combine figures as quoted, and the 12 µs and 20 µs feasibility arithmetic. tok/J and tok/s/kW again use different boundaries (6,350 vs 3,978).
RATIO | ~2 | Against Groq LPX at ≥1000 tok/s/user. Low confidence, because LPX per-chip power is guessed and the speculative-decoding baselines are unaccounted for.
KNOWN | yes | Groq's statically scheduled chip-to-chip links, TPU ICI, and NVLink-switched domains.
NEW FACT | Groq 3 LPU: 500 MB SRAM and 150 TB/s per chip. LPX rack: 256 chips, 128 GB. | [StorageReview](https://www.storagereview.com/news/nvidia-groq-3-lpx-everything-we-know)

IDEA 7: Ridge point matched to MLA decode
DEFECT | MAJOR | The ~1,000 FLOP/B balance is tuned to dense MLA, but the current DeepSeek model (V3.2 DSA) shifts long-context attention to a memory-bound indexer, so the compute ridge sits idle. | Indexer (64 heads × 128 dims, FP8): 1.0 MFLOP per context token for 7.8 KB, which is 128 FLOP/B. Dense MLA is 17 MFLOP. That is 17× less compute ([arXiv 2512.02556](https://arxiv.org/pdf/2512.02556)).
DEFECT | MINOR | The 0.1 pJ per FP8 FLOP is assumed and decides the result. Any chip doing the same math pays the same energy, so the 1.08× lead at 128K is within the uncertainty of that assumption. | 557 GFLOP × 0.1 pJ = 55.7 mJ. 21 mJ for KV implies 4.05 pJ/bit.
SURVIVES | These reproduce: 16.99 MFLOP and 19,764 B per context token (860 FLOP/B), and ridge points of 1,000, about 795 (Rubin) and 626 (Ironwood).
RATIO | ~1.0 | 1.08× on dense MLA, about 1.0 or lower on DSA-class models.
KNOWN | partly | Choosing the compute-to-bandwidth balance per workload is standard roofline co-design (TPU and Ironwood generations).

Method notes:
- I recomputed all of these numbers in a Python script in the scratchpad (`/tmp/claude-0/-home-user-SomeRepository-engine-runs-vs-continuum-compare-r2/86b61a25-826d-5e99-8ce4-43b0688ac74a/scratchpad/chk.py`). I wrote nothing into the repository.
- Idea 1 gives no model, so I assumed a Llama-3-70B-like GQA layout to recompute it.
- Two things I did not verify against a primary source: the HBM4 price, which is a secondhand TrendForce figure, and the Rubin CPX HBM4 revival, which is an analyst report.
- The fleet failure rate in Idea 3 is my estimate from GPU fleet data (Meta's Llama 3 training report), not something I sourced in this check.