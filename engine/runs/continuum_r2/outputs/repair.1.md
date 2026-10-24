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