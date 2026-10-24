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