Both ideas keep their anchors. Idea 1 holds up, but only for one class of workload: decode for MoE models with sparse attention at long context. Idea 2 fails at rack scale and survives only as a niche. All figures come from roofline and cost models written in Python. They are not simulated or measured, and many inputs are my own estimates (marked "est.").
=== IDEAS ===
IDEA 1
NAME: Continuum-D: SRAM experts, LPDDR sparse-KV
MECHANISM: The anchor survives: a 671B MoE (DeepSeek-V3.2 class) sits fully resident in SRAM across standard-packaged dies with no HBM and no CoWoS, and the KV cache goes to commodity LPDDR. The repair changes three things. First, SRAM area is recomputed at a realistic 55% of N3E bitcell density, so 1 GB takes 436 mm² rather than 258 mm². That gives 36 experts per die and one 8+1-die stage per MoE layer, so all-to-all traffic stays inside a stage. The system grows to 527 dies costing $1.44M, under the $1.5M kill line. Second, the target changes from dense-MLA attention to sparse-attention (DSA) MoE models at 32K–128K context. The binding quantity is "drain time": how long a memory takes to be read end to end. Sparse KV at 128K needs about 55 ms at 100 tok/s per user, and LPDDR drains in about 62 ms. HBM4 drains in 13 ms, so it strands bandwidth or runs out of capacity. Dense MLA needs 10 ms, and there the design only ties GPUs ($0.138 vs $0.135–0.157 per million tokens). Third, the system is decode-only: prefill runs on separate GPUs and arrives as about 1.5 GB/s per die of KV writes.
VALUE: At 128K context, sparse attention and 200–400 tok/s per user, it costs about $0.095 per million tokens. The best Vera Rubin NVL72 setup (HBM only, or with CPU-memory KV offload) costs $0.127–0.136, so Continuum-D is 1.34–1.44× cheaper. Against LPX+Rubin it is about 2.9× cheaper, but that figure depends on an estimated LPX price. It is one of the few options above 1,000 tok/s per user.

IDEA 2
NAME: Node-scale expert-stationary SRAM stacks
MECHANISM: The anchor survives: hybrid-bonded multi-layer SRAM stacked under each compute die holds all expert weights, so HBM carries only KV. Capacity is repaired by putting the stacks on 2-die Rubin-class packages using N5 SRAM dies (est. 2.29 MB/mm²). Three layers give 790 GB per rack, a margin of 1.38 on Kimi K2 and 2.15 on V3; the original design had 0.96. But removing weight reads can save at most W/(N·BW) per step, which is 0.40–0.62 ms on an EP72 rack. Rack-scale gain is therefore only 1.19–1.33×, which fails the 1.5× bar. The repair moves the design to where that term is large: an 8-GPU node, without a 72-GPU NVLink rack (NVL72), serving MoE models of 120B parameters or less (gpt-oss-120b). Four layers give 117 GB per node, a 1.86 capacity margin. Gain is 1.39× at 500 tok/s per user and 1.86× at 800, and above 1,000 tok/s per user the stacked node keeps working where the baseline node cannot reach that speed. The SRAM adds about $24k to a ~$0.95M node.
VALUE: At 500–800 tok/s per user on 8-GPU nodes, cost falls from $0.024–0.032 to $0.017 per million tokens (1.4–1.9× cheaper). Against the same model spread across a full NVL72 rack, the gain is only about 1.06×.

=== NOTES ===
**Idea 1: Continuum-D**
- **Anchor kept?** Yes: all SRAM-resident weights, zero HBM, LPDDR for KV. What changed is the target workload (sparse-attention, long context), the die count (527) and the expert placement (layer-local).
- **Decisive numbers:**
  - HBM4 is $209 per TB/s (2026) against $625–1,312 per TB/s for LPDDR. So LPDDR is *more* expensive per unit of bandwidth and cheaper only per GB ($10 vs $16–36 per GB; sources: FACT 1/18/20).
  - At 128K, sparse attention reads 1.14 GB of KV per token, against 5.24 GB for dense attention.
  - Die cost is $601 (N3 wafer ~$19.5k, 65 dies per wafer, 0.77 yield est.).
- **Baselines (per million tokens):**
  - Vera Rubin NVL72 (~$7.8M, Morgan Stanley), HBM-only or with CPU-memory KV offload in the style of Baidu's ESS: $0.127–0.157.
  - LPX + Vera Rubin: $0.276, with an estimated LPX price of $3.5M per rack.
  - Continuum-D: $0.095, or $0.112 if LPDDR reaches $21/GB.
- **Where it loses:**
  - Dense attention: it only ties.
  - Energy: 0.34 J/token on a bottom-up 111 W per die, against 0.37 for Rubin. If dies really draw 300 W, it is 0.92 J/token, a 2.5× loss.
  - It cannot do prefill or training.
- **Consistency checks:**
  - Die area is 776 of 800 mm² (tight).
  - SRAM is 998 MB of 1,074 MB.
  - LPDDR capacity binds only at 50 tok/s per user or below.
  - Chip-to-chip traffic is about 5 GB/s per die, far below link capacity.
  - Latency floor is about 0.47 ms per token.
  - Power density is 0.14–0.38 W/mm².
  - At an estimated 2% failure rate per die per year, about 10 dies fail a year; one spare per stage covers this.
- **Hazards:**
  - 1 TB/s of LPDDR per die has a precedent only in a CPU (Vera's 1.2 TB/s).
  - The LPDDR price spike: 33.7 TB per system.
  - It is tied to sparse attention becoming the standard.
  - When a die fails, the KV for one-eighth of that stage's users has to be prefilled again.
- **Deciding unknown:** the LPDDR bandwidth one organic-packaged die can sustain. At 0.7 TB/s the cost advantage disappears; at 1.5 TB/s it becomes 2.0×. Cheapest experiment: a shoreline and signal-integrity study of a 1,024-bit LPDDR6 interface on an FC-BGA package. Running DSA traces through a DRAM simulator (Ramulator) across 3 contexts × 3 concurrency levels would also measure real top-k reuse.
- **Closest existing work:**
  - d-Matrix Corsair: SRAM plus 256 GB LPDDR, but weights stream from LPDDR at 400 GB/s.
  - MatX One: SRAM weights, but KV in HBM.
  - LPX + Rubin: KV on HBM GPUs.
  - Not found in public material: a zero-HBM design whose LPDDR is sized to sparse-attention drain time.
- **Verdict:** WORKS within the sparse-attention long-context decode regime; NICHE outside it.

**Idea 2: Expert-stationary SRAM stacks**
- **Anchor kept?** Yes. The deployment scale changed: rack, then node.
- **Decisive numbers:**
  - Saving per step is at most SRAM capacity ÷ HBM bandwidth: 0.40 ms (V3) or 0.62 ms (K2) on a rack.
  - Capacity rises from 527 to 1,053 GB per rack across 2 to 4 layers.
  - The node SRAM costs about $24k, roughly 2.5% of the node.
- **Baselines:** the same node without SRAM ($0.024–0.032 per million tokens); the model spread over an NVL72 rack (gain only 1.06×); Cerebras and Groq for 1,000+ tok/s per user, for which only public prices are known, not costs.
- **Consistency checks:**
  - Capacity: OK.
  - Power through the stack: about 1,200 A per die through about 24k TSVs; looks plausible but needs a power-delivery simulation.
  - SRAM leakage: 70–230 W per GPU (est.), which is a hazard.
  - Thermal: compute die on top, as in Zen 5 X3D; needs a thermal simulation.
  - The 1.5× bar: fails at rack scale.
- **Hazards:** limited TSMC SoIC hybrid-bonding capacity; yield of the stacked assembly; leakage; only models of 120B parameters or less fit on a node (Qwen3-235B's margin is 0.92).
- **Deciding unknown:** the true per-step decode floor on an 8-GPU node once weight reads are gone. Measuring it with Nsight on a B200 HGX running gpt-oss-120b at batch sizes 1–64 would settle it; about 20 runs.
- **Closest existing work:** MatX One (SRAM weights in the same plane, not stacked); d-Matrix Raptor (stacked DRAM, not SRAM); AMD MI300 Infinity Cache (256 MB, stacked).
- **Verdict:** NICHE (8-GPU nodes at high per-user speed). FAILS at rack scale.

Everything is in `/home/user/SomeRepository/engine/runs/continuum_r2/repair/c1/`: the scripts `model.py`, `systems.py`, `systems2.py` and `energy.py`, plus `NOTES.md` (full check tables) and `LOG.md`. Nothing was committed.

Sources: [The Register LPX](https://www.theregister.com/2026/03/16/nvidia_lpx_groq_3/), [StorageReview LPX](https://www.storagereview.com/news/nvidia-groq-3-lpx-everything-we-know), [Counterpoint](https://counterpointresearch.com/jp/insights/nvidia-gtc-2026-groq-tokenomics-cmx), [ABI AFD](https://www.abiresearch.com/market-research/insight/7787784-inference-is-disaggregating-to-balance-per), [Chips and Cheese Corsair](https://chipsandcheese.com/p/d-matrix-corsair-256gb-of-lpddr-for), [The Register Corsair](https://theregister.com/2025/09/08/dmatrix_jetstream_nic), [hwbusters Raptor](https://hwbusters.com/news/d-matrix-raptor-drops-the-memory-phy-32gb-at-100-tb-s-against-hbm4s-192gb-at-18/), [SiliconANGLE MatX](https://siliconangle.com/2026/02/24/chip-startup-matx-raises-500m-speed-large-language-models/), [VR NVL72 price](https://www.digitalcitizen.life/nvidias-vera-rubin-ai-rack-may-cost-7-8-million-as-memory-prices-surge/), [Guru3D](https://guru3d.com/story/nvidia-vera-rubin-ai-rack-cost-reportedly-hits-million/), [Silicon Analysts wafer pricing](https://siliconanalysts.com/data/wafer-pricing), plus the evidence ledger (FACT 1, 4, 5, 9, 15, 18, 19, 20, 22).

IDEA 3
NAME: Touch-rate-split DSA KV tier
MECHANISM: The anchor is kept. The model's own lightning indexer picks the top-2,048 entries, and a hardware engine gathers exactly those 656-B MLA latents from on-package LPDDR6. The 132-B FP8 indexer keys stay in HBM and are scanned in full every step. The repair drops the bandwidth and energy claim, which was false: against FlashMLA-sparse, HBM bytes per step fall only 1.137→1.055 GB (1.08×), and memory energy is 31.3 vs 31.7 mJ per token, so no gain. The design is restated as a capacity split by touch rate. The indexer needs about 100 reads per second of its own capacity, which nearly matches HBM4's 76 per second, while the latent is touched at only 2,048/L. Each byte class therefore goes to the memory whose bandwidth-to-capacity ratio fits it. The decode die (Continuum-D) has 4 HBM4 stacks, 4 LPDDR6 modules (512 GB, ~0.7 TB/s), a hardware per-layer top-k unit and an LRU hot-buffer tag directory in HBM. At 128K context and 100 tok/s it serves 74 users, or 18.4 per HBM stack, against 5.0 per stack for an all-HBM Rubin. That is 3.9×, and the limit is HBM bandwidth spent on the indexer scan. LPDDR miss traffic (79 GB/s) and gather latency (37 of 164 µs per layer) both have headroom down to a hot-buffer hit rate of about 0.4.
VALUE: Cost per 128K user slot is 1.0× (2026 prices) to 1.0× (2027) that of the best practice, Rubin+Vera with HiSparse offload ($86–100 vs $102 per user slot). The win is 1.9× users per HBM stack when top-k locality is low (hit ≤0.4), and 1.8–3.4× users per chip on accelerators that lack a large coherent host memory, such as Ironwood-class chips (47.7–89.5 vs 26.6 users).

IDEA 4
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
