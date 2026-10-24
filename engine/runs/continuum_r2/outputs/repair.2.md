=== IDEAS ===
IDEA 1
NAME: Touch-rate-split DSA KV tier
MECHANISM: The anchor is kept. The model's own lightning indexer picks the top-2,048 entries, and a hardware engine gathers exactly those 656-B MLA latents from on-package LPDDR6. The 132-B FP8 indexer keys stay in HBM and are scanned in full every step. The repair drops the bandwidth and energy claim, which was false: against FlashMLA-sparse, HBM bytes per step fall only 1.137→1.055 GB (1.08×), and memory energy is 31.3 vs 31.7 mJ per token, so no gain. The design is restated as a capacity split by touch rate. The indexer needs about 100 reads per second of its own capacity, which nearly matches HBM4's 76 per second, while the latent is touched at only 2,048/L. Each byte class therefore goes to the memory whose bandwidth-to-capacity ratio fits it. The decode die (Continuum-D) has 4 HBM4 stacks, 4 LPDDR6 modules (512 GB, ~0.7 TB/s), a hardware per-layer top-k unit and an LRU hot-buffer tag directory in HBM. At 128K context and 100 tok/s it serves 74 users, or 18.4 per HBM stack, against 5.0 per stack for an all-HBM Rubin. That is 3.9×, and the limit is HBM bandwidth spent on the indexer scan. LPDDR miss traffic (79 GB/s) and gather latency (37 of 164 µs per layer) both have headroom down to a hot-buffer hit rate of about 0.4.
VALUE: Cost per 128K user slot is 1.0× (2026 prices) to 1.0× (2027) that of the best practice, Rubin+Vera with HiSparse offload ($86–100 vs $102 per user slot). The win is 1.9× users per HBM stack when top-k locality is low (hit ≤0.4), and 1.8–3.4× users per chip on accelerators that lack a large coherent host memory, such as Ironwood-class chips (47.7–89.5 vs 26.6 users).

IDEA 2
NAME: SRAM-tiled LPDDR prefill die
MECHANISM: The anchor is kept: a prefill die with no HBM, sharing an ISA with the decode tier and passing it KV (132 B to decode-tier HBM, 656 B to its LPDDR, 1.8 GB/s per die). The original threshold was wrong. The die's ridge is 12,500 FLOP/B (17.5 PF ÷ 1.4 TB/s), not 300. MoE expert-stationary streaming is also capped at about 2·F_expert = 4,096 FLOP/B whatever the batch, so an LPDDR-only die with 256 MB of SRAM reaches only 34% of its compute at 128K. Two changes fix this. First, each package holds a full NVFP4 replica of the model (377 GB in 512 GB LPDDR6), so there is no expert-parallel all-to-all. Second, a hybrid-bonded SRAM token-tile buffer (≥0.75 GB per die at 128K, ≥1.0 GB at 32K; 1.45 GB planned) keeps tiles of 31–65K tokens resident while weights stream past. The package then becomes compute-bound at 76.5k tok/s at 128K, the same as Rubin. A CPX-like part that needs EP3 over a 200 GB/s NIC is network-bound at 30k tok/s. The price is at least 64K tokens per pass, which means about 1–2 s of batching latency.
VALUE: Prefill throughput per FLOP matches Rubin with zero HBM stacks. BOM per ktok/s is 1.0× Rubin at 2026 HBM prices ($115 vs $114) and 1.6× cheaper at 2027 prices ($115 vs $187). Energy per token is the same (23.8 vs 24.2 mJ).

=== NOTES ===
**Idea 1: Touch-rate-split DSA KV tier**
- **Anchor kept?** Yes: exact gather of the indexer-selected entries from an LPDDR capacity tier.
- **Decisive numbers:**
  - KV layout of 656 B per token ([FlashMLA](https://gittrend.io/repo/deepseek-ai/FlashMLA), [vLLM DSA blog](https://vllm.ai/blog/deepseek-v3-2)).
  - Indexer key of 132 B and top-k of 2,048 ([DeepSeek-V3.2](https://arxiv.org/pdf/2512.02556), [aiwiki/Tensor Economics](https://aiwiki.ai/wiki/deepseek_v3_2_exp)). The 132 B is a secondary figure.
  - Rubin: 288 GB, 8×HBM4, 22 TB/s ([Guru3D](https://www.guru3d.com/story/nvidia-details-rubin-gpu-architecture-with-hbm4-nvlink-6-and-336-billion-transistors/)).
  - Vera: 1.5 TB at 1.2 TB/s, C2C 1.8 TB/s ([Tom's Hardware](https://tomshardware.com/pc-components/gpus/nvidias-vera-rubin-platform-in-depth-inside-nvidias-most-complex-ai-and-hpc-platform-to-date)).
  - HiSparse LRU at 2× top-k gives an 87% hit rate ([arXiv 2608.07009](https://arxiv.org/html/2608.07009)). Raw step-to-step overlap is 35–50% ([GVR](https://arxiv.org/html/2604.22312v1)).
  - LPDDR6 is 38.4 GB/s per x24 chip ([Power Systems Design](https://www.powersystemsdesign.com/articles/lpddr6-bandwidth-math-what-you-gain-what-you-pay-what-you-measure/22/23664)).
  - Prices: HBM4 at $600 (2026) and $1,300 (2027) per stack, LPDDR at $10/GB (ledger facts 18 and 20).
- **Best-baseline comparison per served 128K user slot:**
  - Rubin with all KV in HBM: 5.0 users per stack, $119–258 per user.
  - Rubin+Vera with HiSparse/ESS: 17.9 per stack, $86–125.
  - Continuum-D: 18.4 per stack, $102–140.
  - Ironwood with all KV in HBM: 3.3 per stack.
- **Consistency table:** in NOTES.md. HBM bandwidth is the binding limit. LPDDR capacity (388 of 512 GB), LPDDR bandwidth (79 of 350 GB/s), latency (37 of 164 µs) and compute (1.8 PF) all pass. The design loses at short context: at 8K it gets 0.34× per stack unless the latent is placed in HBM adaptively.
- **Hazards:**
  - It only applies to DSA-style models.
  - The gather sits on the critical path, so two-batch overlap is mandatory.
  - LPDDR prices are rising (+80–90% QoQ).
  - Because the indexer scan sets the HBM floor, users per stack keep dropping as 1/L.
- **Deciding unknown:** the top-k hot-buffer hit rate on production traces. Measure the per-layer LRU(2×k) hit rate across all 61 layers on ≥200 long-context sessions (≥10K decode steps each) of agentic, coding and RAG work. If the hit rate is ≥0.7, Vera+software already matches this design. The second unknown is LPDDR6 efficiency on random 656-B gathers, which needs a DRAMsim3/Ramulator2 run.
- **Closest existing work:** ESS, HiSparse (SGLang), [AVSG](https://arxiv.org/pdf/2609.37538), [SAC/CXL](https://arxiv.org/html/2606.19746), LongSight. All of these are software or CXL designs. None is an on-package tier sized by touch rate with a hardware tag directory.
- **Verdict: NICHE.** It roughly equals the best practice on Nvidia systems and wins on TPU/ASIC decode chips and in low-locality regimes.

**Idea 2: SRAM-tiled LPDDR prefill die**
- **Anchor kept?** Yes: memory-light prefill without HBM, a shared ISA, and KV handoff to the decode tier.
- **Decisive numbers:**
  - Ridge of 12,500 FLOP/B, against the idea's 300.
  - MoE activation intensity is fixed at about 4,096 FLOP/B.
  - At least 0.75–1.0 GB of SRAM per die is needed. V-Cache density is 64 MB per 36 mm² (ledger fact 4).
  - Per-token cost at 128K is 174 GFLOP: 74 dense, 65 indexer, 35 attention.
  - Rubin CPX was 30 PF with 128 GB GDDR7 and was pulled at GTC 2026 (ledger facts 2 and 16). Qualcomm AI200 carries 768 GB of LPDDR per card ([DCD](https://www.datacenterdynamics.com/en/news/qualcomm-launches-ai200-and-ai250-chip-offering-targeting-inferencing-workloads-at-rack-scale/.)). Huawei 950PR uses HiBL at 128 GB and 1.6 TB/s ([HuaweiCentral](https://www.huaweicentral.com/huawei-announces-self-made-hbm-memory-to-boost-ai-chips-potential/amp/)). Ironwood is 4.6 PF FP8 with 192 GB and 7.3 TB/s ([TechRadar](https://www.techradar.com/pro/googles-most-powerful-supercomputer-ever-has-a-combined-memory-of-1-77pb-apparently-a-new-world-record-for-shared-memory-multi-cpu-setups)).
- **Best-baseline comparison per delivered prefill throughput at 128K:**

  | design | throughput | BOM per ktok/s | HBM stacks |
  |---|---|---|---|
  | Rubin, EP2 over NVLink | 76.5k tok/s | $114–187 | 8 |
  | Continuum-P2 | 76.5k tok/s | $115 | 0 |
  | CPX-like | 30k tok/s (network-bound) | — | — |
  | Ironwood | 15.8k tok/s at FP8 | — | — |

  These are BOM figures, not prices. Die, SoIC and CoWoS costs are my assumptions.
- **Consistency table:** in NOTES.md. It passes on SRAM, LPDDR capacity and bandwidth (0.77 of 2.8 TB/s) and KV handoff. It fails for short-prompt latency, because a pass needs at least 64K tokens (about 1 s). It cannot be air-cooled (about 1.8 kW).
- **Hazards:**
  - Reticle-scale hybrid-bonded SRAM yield, and SoIC capacity, which is scarcer than CoWoS.
  - 16 LPDDR modules is twice Vera's beachfront.
  - LPDDR at $10/GB wipes out the BOM gain at 2026 HBM prices.
  - It is single-purpose, so it carries a utilization risk.
  - The market already walked away from CPX.
- **Deciding unknown:** whether ≥0.75 GB of hybrid-bonded SRAM per die gives the claimed ~100% compute utilization at 64K-token passes. Test it with a Timeloop/LLMCompass schedule of one DeepSeek-V3.2 MoE layer plus DSA at 32K and 128K, sweeping SRAM over 0.25–2 GB (6 points × 2 contexts). Then run an FPGA/GPU emulation that caps HBM bandwidth to 1.4 TB/s with an L2-sized tile.
- **Closest existing work:** Rubin CPX, Huawei 950PR, Qualcomm AI200, Splitwise. None of them combines a full LPDDR replica with a stacked-SRAM token tile.
- **Verdict: NICHE.** It is a long-context, throughput-tier prefill part that pays off only when HBM is the supply bottleneck or HBM4 reaches about $1,300 per stack.

Files are in `/home/user/SomeRepository/engine/runs/continuum_r2/repair/c2/`: LOG.md, NOTES.md and the five scripts.