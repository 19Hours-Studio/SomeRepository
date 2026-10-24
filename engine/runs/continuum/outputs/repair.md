
=== IDEAS ===
IDEA 1
NAME: Continuum-D: SRAM weights, LPDDR KV
MECHANISM: The anchor is unchanged. Weights of a frontier MoE stay resident in plain 2D SRAM across many standard-packaged dies, with no HBM and no CoWoS, and each user's KV cache lives in LPDDR attached to each die. Repaired sizing:
- At NVFP4's 4.5 bits per weight the model is 377 GB, not 335 GB. That takes 333 N3 dies of 800 mm², each with 1.25 GB of SRAM (428 mm² at 31.8 Mib/mm² and 70% array efficiency), about 1.3 PF of FP8, and 48 GB of LPDDR6 at 1 TB/s (26 x24 channels).
- The dies form 61 layer-groups that broadcast and then reduce, instead of one 333-stage pipeline. That cuts the hop floor from 233 µs to 85 µs per token, so the per-user ceiling is about 11k tok/s.
- Each die keeps a copy of a neighbour's KV slice. Without it, losing one die would erase part of every user's cache.

At 32K context with NVFP4 KV the system serves 414k tok/s and is compute-bound (LPDDR could carry 514k). Bill of materials is $0.81M at 117 kW, or $2.44M priced at a 3× markup. Energy is 0.19–0.20 J/token, about 9% worse than Rubin, so the original "40× less energy" claim is dropped.
VALUE: At 32K context and ≥1000 tok/s/user it serves tokens at $0.077/Mtok. That is 2.8× cheaper than Rubin NVL72 with wide expert parallelism ($0.214), about 5× cheaper than Rubin plus Groq 3 LPX (if an LPX rack costs ~$4M), and 10–19× cheaper than Cerebras. At ≤500 tok/s/user it only reaches parity (1.1×).

IDEA 2
NAME: HBM-halved expert-stationary stack
MECHANISM: The anchor is unchanged: MoE expert weights stay fixed in hybrid-bonded SRAM layers, and HBM serves only the KV cache. The repair changes the job of the stack. It no longer sits on top of a full-HBM GPU, where it bought only 1.00–1.04×: with wide expert parallelism a Rubin package streams just 5.2 GB of weights per step, about 0.24 ms, which is around 1% of energy per token. Instead the stack replaces half the HBM. The repaired package:
- 2 compute dies, each with 2–4 SRAM layers bonded underneath. The compute die sits on top, as in Zen 5 X3D, so heat goes straight to the lid. At the N5 bitcell that is 2.29 MB/mm², 6.9 GB per die with 4 layers, and 987 GB per 72-package rack.
- 4 HBM4 stacks per package instead of 8: 11 TB/s and 144 GB, used only for KV.

DeepSeek-V3 needs 2 SRAM layers per die and Kimi-K2 (1T) needs 3. In every tier tested for DeepSeek-V3, and for Kimi-K2 at a realistic 0.35 MFU, throughput equals the 8-stack Rubin. The stack adds about $4.3k per package; the 4 HBM4 stacks it saves are worth about $10–14k.
VALUE: Throughput per rack is the same, but the rack costs about 0.73–0.83× as much per token and uses 288 fewer HBM4 stacks (half), and HBM supply is the binding limit for 2026–28. It loses (0.61×) only for 1T-class models at high MFU and ≤300 tok/s/user, where HBM bandwidth for KV becomes the limit again.

=== NOTES ===

**Idea 1 (Continuum-D)**
- **Anchor kept?** Yes.
- **Decisive numbers:**
  - N3 wafer $19.5k (range $17–22k), N3E SRAM 31.8 Mib/mm², LPDDR $10/GB (range $7.8–21), LPDDR6 38.4 GB/s per x24 (SK hynix, ISSCC 2026), Vera LPDDR ~3.6 pJ/bit, HBM 3.44 pJ/bit, Rubin 288 GB / 22 TB/s, Vera Rubin NVL72 rack $7.8M (analyst estimate, range $5–9.1M).
  - SRAM capacity margin is 1.10, which is thin.
- **Best-baseline comparison, $ per million delivered tokens** at 32K context, NVFP4 KV, 60% MFU assumed for every design:

| tok/s per user | Continuum-D | Rubin NVL72, wide EP | Rubin + LPX AFD | Cerebras, 12 wafers |
|---|---|---|---|---|
| ≤500 | $0.077 | $0.087 | $0.26 | — |
| 1000 | $0.077 | $0.214 | $0.39 | $1.50 |
| 2000 | $0.077 | cannot reach | cannot reach | $0.75 |

  - At 128K context: $0.28 vs Rubin's $0.34.
  - Per chip, Continuum-D is weak: 1.2k tok/s, against 4.1k for Ironwood and 14.3k for a Rubin package. It wins only on cost and per-user speed, not on per-chip performance or J/token.
- **Consistency:** every limit passes (reticle, SRAM, LPDDR bandwidth and capacity, 0.44 W/mm², hop floor, MTBF of ~1500 h with spares and a 0.1 s weight reload). The die-edge length left for LPDDR and SerDes (~80 of 113 mm) is my own estimate and needs a floorplan.
- **Hazards:**
  - It needs 16 TB of LPDDR per system, and LPDDR prices rose about 90% in one quarter in 1Q26.
  - The whole instance depends on 333 dies.
  - The 3× markup is my assumption.
- **Deciding unknown:** real decode MFU of MLA attention, and the per-layer broadcast/reduce latency across ~5.5 dies.
  - Cheapest experiment: run DeepSeek-V3 decode in LLMCompass or Timeloop on the stated die, plus a 2-FPGA SerDes hop-latency measurement (about 10⁴ samples to get the p99).
  - It is falsified if effective MFU is below 0.35, or if a hop takes more than 3 µs at 1000 tok/s/user.
- **Closest existing work:** d-Matrix Corsair has the same SRAM-plus-LPDDR split, but with about 4× less LPDDR bandwidth per GB of SRAM, aimed at small models. Groq 3 LPX keeps KV on Rubin's HBM. What is new here is LPDDR sized to KV bandwidth and sliced per layer, at frontier-MoE scale.
- **Verdict:** WORKS for the high-interactivity tier; NICHE below 500 tok/s/user.

**Idea 2 (expert-stationary stack)**
- **Anchor kept?** Yes. Its role was changed from adding bandwidth to replacing HBM.
- **Decisive numbers:**
  - Against a competent wide-EP Rubin, the original design gains only 1.00–1.04×, so its claims of 1.4–1.6× better J/token and 1.6× more users fail.
  - Repaired version: equal throughput for 0.73–0.83× the price. The HBM4 stack price comes from memory being 26% of the rack price, which is an upper bound.
  - Stacked SRAM costs about $312/GB.
- **Consistency:**
  - Capacity: margins of 2.6× for DeepSeek-V3 and 1.7× for 1T models.
  - KV capacity: 56 of 144 GB used at 300 tok/s/user.
  - Thermal: SRAM leakage of 0.8–4 W is negligible.
  - Unverified: feeding ~1200 A per die through 2–4 TSV layers, and stack yield of 0.78.
- **Hazards:** SoIC capacity becomes the new bottleneck. The design loses on 1T-class models when MFU is high. It still needs CoWoS for 4 stacks.
- **Deciding unknown:** whether ~1.2 W/mm² can be delivered through stacked SRAM.
  - Cheapest experiment: a thermal and IR-drop simulation (e.g. HotSpot plus a power-delivery-network model), then a 2-layer test vehicle (n≈30 stacks for bond yield).
  - It is falsified if IR drop exceeds 5% or bond yield is below 0.9 per layer.
- **Closest existing work:** AMD V-Cache, and a single unconfirmed report that Nvidia's Feynman will stack LPU-style SRAM on the GPU. What is new here is cutting HBM in half and dedicating it to KV.
- **Verdict:** WORKS, as a cost and supply design, not a performance one.

Files are in the work folder: `LOG.md`, `NOTES.md`, `model.py`, `round3_idea2.py`, `round4_idea2.py` and `round5_idea1.py`.

Sources:
- [siliconanalysts TSMC 3nm cost](https://siliconanalysts.com/guide/tsmc-3nm-cost)
- [tech-insider N2 price](https://tech-insider.org/tsmc-2nm-wafer-price-2026/)
- [The Register LPX deep dive](https://www.theregister.com/2026/03/19/nvidia_lpx_deep_dive/)
- [StorageReview Groq 3 LPX](https://www.storagereview.com/news/nvidia-groq-3-lpx-everything-we-know)
- [SemiAnalysis inference kingdom](https://newsletter.semianalysis.com/p/nvidia-the-inference-kingdom-expands)
- [Vera Rubin $7.8M rack](https://www.digitalcitizen.life/nvidias-vera-rubin-ai-rack-may-cost-7-8-million-as-memory-prices-surge/)
- [SK hynix LPDDR6](https://www.guru3d.com/story/sk-hynix-previews-144-gb-s-lpddr6-samsung-targets-128/)
- [d-Matrix Corsair (ASCII)](https://ascii.jp/elem/000/004/350/4350373/)
- [aiwiki Corsair](https://aiwiki.ai/wiki/d_matrix_corsair)
- [d-Matrix Raptor](https://hwbusters.com/news/d-matrix-raptor-drops-the-memory-phy-32gb-at-100-tb-s-against-hbm4s-192gb-at-18/)
- [naddod Feynman](https://www.naddod.com/ai-insights/nvidia-feynman-architecture-introduction-next-gen-gpus-with-tsmc-a16-process)
- [InferenceX wide EP](https://inferencex.semianalysis.com/blog/gb200-nvl72-kimi-k2-5-vllm-wide-ep-3x-vs-b200)

IDEA 3
NAME: Layer-pipelined LPDDR prefill dies
MECHANISM: The anchor is kept: a dense FP4/FP8 compute die with no HBM runs the compute-bound prefill phase, sends the KV to the decode tier over a plain NIC, and uses the same ISA and compiler as that tier. The kill test was right that one die holding a whole MoE model is memory-bound: on DeepSeek-V3 at 8K tokens per pass, each expert sees only 256 tokens, which gives 910 FLOP/B. The repair splits the model's layers across 8 dies. Each die (20 PF dense FP4, 800 mm², ~1.18 kW) keeps 47 GB of the 376 GB of NVFP4 weights in 64 GB of 1024-bit LPDDR5X (1.37 TB/s) and pushes a large batch of tokens through one layer before moving to the next (layer-major mega-batch). That makes a die compute-bound from about 45K tokens per pass. Only activations cross between dies (15–45 GB/s, against the 0.65 TB/s per die that expert-parallel all-to-all would need), so no NVLink-class scale-up fabric is required. KV egress is 2.4–5 GB/s per die, TTFT is 0.69 s at 8K prompts, and the design uses 0 GB of HBM and no CoWoS.
VALUE: All-in cost per prefill token comes out 1.27× cheaper than Rubin, 1.20× cheaper than the revived HBM4 Rubin CPX and 2.7× cheaper than B200, rising to about 1.45× vs Rubin if HBM4 reaches $32/GB. It also removes the ~1.26 GB of HBM Rubin needs per 1K prefill tok/s.

IDEA 4
NAME: Detached attention-stack memory nodes
MECHANISM: The anchor is kept: the custom HBM4 logic base die runs GQA decode attention (QKᵀ, softmax, AV at FP8) on KV read through the TSVs, and only partial outputs leave the stack. The repair takes the stack off the GPU interposer. It uses a JEDEC SPHBM4-style organic-substrate mount (standard published July 2026), with a narrow link in place of the 2048-bit host bus. Each 48 GB, 2.5 TB/s stack becomes a separate KV node with a 13–19 W attention base die. It serves 2 users at 128K context (FP8 KV) at 49 tok/s each and needs only 0.2 GB/s of decode link, because KV bytes read outnumber link bytes about 8,000 to 1 (plus ~2 GB/s to load KV after prefill). The claimed 2× energy saving does not hold: counting the GPU-side NoC, L2 and shared-memory path, it is 33% (5.34 → 3.58 pJ/bit). The real gain is that KV capacity and bandwidth grow without CoWoS or GPU silicon: one Rubin handles weights and FFN for about 1,200–1,500 users while 400–760 stacks hold their KV.
VALUE: Long-context (128K) GQA decode costs about 1.7× less per million tokens than the best baseline (Rubin-only: $0.177 vs $0.304 at cost of goods; 2.6× at market prices), and 1.5× less at 16K context.

=== NOTES ===

**Idea 1: Layer-pipelined LPDDR prefill dies**
- **Anchor kept?** Yes. It is still an HBM-free prefill die that shares its ISA with the decode tier. What changed is how the model is split across dies (by layer, not by expert) and how tokens are scheduled (layer-major mega-batches).
- **Decisive numbers:**
  - DeepSeek-V3 public config: 669B parameters, 35.6B active per token, 92 GFLOP per token at 8K context.
  - NVFP4 at 4.5 bits per value (user note, FACT 3).
  - LPDDR5X at 9.6–10.7 Gb/s; a SOCAMM2 module gives 154 GB/s (Cadence). Vera reaches 1.2 TB/s on LPDDR, so the bandwidth is reachable (FACT 5).
  - Rubin CPX has reportedly been redesigned around 168 GB of HBM4 (Kuo, via TechNews, Sept 2026). The GDDR7 CPX that the kill test called prior art is no longer the shipping plan.
  - Rubin is about $55K per GPU, and the VR200 rack about $7.8M (Morgan Stanley via Wccftech).
  - HBM4 is $10–16/GB, with Samsung asking ~$32/GB; LPDDR is $7.8–21/GB (FACT 1).
- **Best-baseline comparison** (per million prefill tokens delivered, all-in: cost of goods + 35% system + power + $10/W facility):

  | Design | $/M prefill tokens |
  |---|---|
  | Continuum-P | 0.00077 |
  | Rubin | 0.00098 |
  | CPX-HBM4 | 0.00092 |
  | B200 | 0.0021 |
  | H100 (cheapest, cost of goods) | 0.0042 |
  | B200 rented at $4.5/h | 0.021 |

  At cost of goods the win is modest. HBM and CoWoS independence is the main value.
- **Consistency table** (in LOG.md): all checks pass.
  - LPDDR bandwidth ≤0.9 used.
  - Capacity: 50 of 64 GB used.
  - Links: 45 of 112 GB/s used.
  - TTFT at 8K: 0.69 s.
  - Power density sits at the limit (1.48 W/mm², about the same as Rubin), so liquid cooling is required.
  - It loses on single long-prompt latency: 1.02 s vs 0.37 s for 8 Rubins at 128K.
- **Hazards:**
  - The prefill benefit depends on NVFP4 weights × activations being accurate enough. The NVFP4 evidence is from training, not from KV quality.
  - Hot experts cause imbalance across pipeline stages.
  - LPDDR prices are rising (FACT 10).
  - The die is 30% smaller than Rubin, and there is little room left to cool it harder.
- **Deciding unknown:** sustained FP4 utilization of layer-major MoE prefill when weights stream from LPDDR (I assumed 0.6).
- **Cheapest experiment:** on a GB200 node, keep weights in Grace LPDDR and stream them over NVLink-C2C. This emulates the memory-light die. Sweep tokens per pass from 4K to 128K (8 points × 3 prompt lengths × 5 runs = 120 runs). Measure the knee and FLOP utilization. The design fails if the knee sits above ~150K tokens or utilization is below 0.4.
- **Closest work:** Rubin CPX (now HBM4), Intel Crescent Island (160 GB LPDDR5X, general inference), Qualcomm AI200 (not verified in my searches). None of them pairs a pipelined, prefill-only design with LPDDR-resident layer slices.
- **Verdict:** WORKS. The cost win is modest (1.2–1.45×); the supply win (no HBM, no CoWoS) is large.

**Idea 2: Detached attention-stack memory nodes**
- **Anchor kept?** Yes: attention runs in the HBM4 base die on KV read through the TSVs, and only partial outputs leave. What changed is that the stack is detached on organic substrate and its value is cost, not energy.
- **Decisive numbers:**
  - HBM energy is 3.44 pJ/bit, of which 0.25 is I/O (FACT 6/7).
  - The GPU-side path is my own estimate: ~80 fJ/bit/mm over 15 mm, plus three SRAM passes at 0.15 pJ/bit each.
  - GQA with groups of 8 at FP8 needs 16 FLOP/B. That works out to 32–40 TFLOPS and 13–19 W per stack.
  - MLA needs 484 FLOP/B (≈387 W) and the DSA indexer 128 FLOP/B (≈102 W), so both are excluded.
  - SPHBM4 (512 data pins with 4:1 serialization, on organic substrate) is the enabler.
- **Best-baseline comparison** (Llama-70B-class model, 128K context, $/M decode tokens at cost of goods):

  | Option | $/M decode tokens | Ratio |
  |---|---|---|
  | Attention stacks | 0.177 | — |
  | Rubin-only | 0.304 | 1.71× |
  | Lamina-style attention on H200s | 0.466 | 2.6× |
  | Stacks, FP4 KV | 0.101 | — |
  | Rubin-only, FP4 KV | 0.171 | 1.69× |

  Duplex (GPU-attached) only gets the ~33% energy saving on the KV share. Rubin-only also gives faster service per user (74 vs 49 tok/s), so the ratio compares slightly different service levels.
- **Consistency table** (in LOG.md):
  - Link, KV ingress and per-layer latency are fine.
  - GPU NIC aggregate is tight at 80%, so batch should be capped at about 1,200 users.
  - The base-die thermal budget is UNKNOWN. A 1-D estimate gives a 20–40 K rise above the lid; this is acceptable only if bond-layer k is at least 3 W/mK and the lid stays at or below ~50 °C.
  - FP4 KV at full bandwidth needs 23–34 W, which is too hot. Store KV in FP4 but run the stack at reduced bandwidth.
- **Hazards:**
  - DRAM retention failures if the base die heats the stack.
  - The niche is shrinking as models move to MLA, DSA sparse attention, and linear-attention hybrids.
  - HBM4 price could reach $32/GB. The win still holds there: 0.26 vs 0.37.
  - It depends on vendors supplying custom SPHBM4 base dies.
- **Deciding unknown:** junction-to-lid thermal resistance of a 16-high stack with 15–20 W in the base die.
- **Cheapest experiment:** a thermal test vehicle. Take an HBM4/SPHBM4 daisy-chain stack, or a 16-die dummy stack with the same bond layers, put a heater in the base die, and sweep 0–25 W with the DRAM layers at 51 W. Use n ≥ 5 stacks × 2 bond types, then run a retention-at-temperature test at 85/95 °C. The design fails if a 16 W base die pushes DRAM above 85 °C with a 45 °C lid.
- **Closest work:** Duplex (base-die Logic-PIM attached to the GPU), NOVA (2026), StreamDQ (dequantization in a custom HBM base die), Lamina (attention on cheap GPUs), CENT (CXL GDDR6-PIM). I found no detached, organic-mounted HBM4 attention-stack node.
- **Verdict:** NICHE. It works for GQA long-context decode (≥16K). It fails for MLA and DSA models, and it depends on a thermal result.

Scripts and the full log are in `/home/user/SomeRepository/engine/runs/continuum/repair/c2/` (`LOG.md` plus 5 Python files).

Sources:
- [Duplex (arXiv 2409.01141)](https://arxiv.org/pdf/2409.01141)
- [NOVA (arXiv 2608.22613)](https://arxiv.org/pdf/2608.22613)
- [StreamDQ (arXiv 2607.08993)](https://arxiv.org/pdf/2607.08993)
- [Lamina (arXiv 2405.01814)](https://arxiv.org/abs/2405.01814)
- [JEDEC SPHBM4 (Blocks & Files)](https://blocksandfiles.com/2025/12/17/jedec-sphbm4/)
- [SPHBM4 on organic substrates (01net)](https://www.01net.it/new-jedec-sphbm4-standard-enables-hbm4-class-bandwidth-on-organic-substrates/)
- [HBM prices (Capital & Compute)](https://capitalandcompute.net/memory-prices/hbm/)
- [HBM pricing (Silicon Analysts)](https://siliconanalysts.com/data/hbm-pricing)
- [Samsung HBM4 pricing ask (Sammyfans)](https://www.sammyfans.com/2026/10/02/samsung-seeks-more-than-3x-hbm3e-pricing-for-hbm4/)
- [Rubin CPX moves to HBM4 (TechNews)](https://technews.tw/2026/09/02/nvidia-rubin-cpx-reenters-roadmap-hbm4-ai-prefill/)
- [VR200 rack cost (Wccftech)](https://wccftech.com/nvidia-vera-rubin-rack-hit-with-memory-price-surge-pushing-hbm4-lpddr5x-bill-to-2m-of-7-8m-total/amp/)
- [GPU pricing guide (IntuitionLabs)](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide)
- [Intel Crescent Island](https://newsroom.intel.com/artificial-intelligence/intel-to-expand-ai-accelerator-portfolio-with-new-gpu)
- [SOCAMM2 bandwidth (Cadence)](https://community.cadence.com/cadence_blogs_8/b/ip/posts/socamm-modernizing-datacenter-memory-with-lpddr6-5x)
- [Samsung HBM base die at Hot Chips 2026 (ServeTheHome)](https://www.servethehome.com/samsung-evolving-hbm-base-die-at-hot-chips-2026/)
