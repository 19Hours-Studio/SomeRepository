Continuum is a 3D-SRAM inference accelerator for serving 1.6T-parameter MoE models at long context and high per-user speed. In a fair model it beats Nvidia Rubin by about 1.0–1.6× on tokens per provisioned MW. The win depends on one unmeasured number: exposed per-layer latency τ. It is not shown to be "best in the world". There is no silicon, and every Continuum number is model output.

## Verdict (round 4)

**Changes since round 3**
1. **GPU all-to-all bandwidth is now modelled.** It never binds, but it reaches 54–65% of Rubin's compute time, so imperfect overlap would hurt GPUs slightly.
2. **τ is now set per architecture.**
   - Round 3's uniform 8 µs was 5–12× below every GPU figure derivable from published speeds.
   - GPUs/TPUs now use 20 µs, which is 2–5× better than measured today.
   - Continuum uses 10 µs, inside the measured LPX/Cerebras range.
3. **The GPU model is within 0.6–2× of measured GB300 InferenceX points**, with errors in both directions. Continuum has no such check.

**Continuum's tok/s-per-MW ratio** (DeepSeek-V4-Pro, 128K, each system at its best speculation depth k), by per-user speed floor:

| p | Against | ≥200 | ≥500 | ≥800 | ≥1,000 | ≥1,500 |
|---|---|---|---|---|---|---|
| 0.8 | Rubin 35 PF | 1.17 | 1.40 | 1.54 | 1.70 | 1.91 |
| 0.8 | **Rubin 50 PF** | **1.00** | **1.16** | **1.29** | **1.35** | **1.64** |
| 0.8 | MI455X | 1.44 | 1.85 | 2.05 | 2.15 | 2.6 |
| 0.8 | TPU 8i | 1.66 | 2.07 | 2.33 | 2.60 | 6.0 |
| 0.8 | Rubin + LPX | 3.7 | 3.6 | 3.4 | 3.5 | 3.3 |
| 0.8 | Cerebras CS-4 | 22 | 22 | 19 | 18 | 17 |
| 0.6 | Rubin 50 PF | 1.00 | 1.36 | 1.97 | 3.4 | Rubin can't reach |

**τ sensitivity** (against Rubin50, p = 0.8; cells are ≥200 / ≥1,000 / ≥1,500):

| Continuum τ ↓ / GPU τ → | 8 µs | **20 µs** | 45 µs (≈ today) |
|---|---|---|---|
| 5 µs | 0.95 / 1.14 / 1.22 | 1.09 / 1.64 / 2.17 | 1.34 / 4.4 / — |
| **10 µs** | 0.87 / 0.94 / 0.92 | **1.00 / 1.35 / 1.64** | 1.23 / 3.6 / — |
| 20 µs | 0.75 / 0.64 / 0.56 | 0.86 / 0.92 / 1.01 | 1.06 / 2.5 / — |

**Defensible claim**
- The niche is HBM-constrained serving of 0.5–1.6 TB MoE models at ≥128K context and ≥800 tok/s/user.
- There, Continuum leads the best GPU by **~1.3–1.6× in tok/MW** and **2.2–2.7× in tokens per HBM stack**.
- This holds only if its per-layer latency stays ≥ ~1.5× below Rubin's.
- At ≤500 tok/s/user it ties. If GPU software reaches ~8 µs, it loses by 6–13%.

**Why the lead is bounded**
- At best k, every system is compute-bound.
- Drafting multiplies FLOPs per accepted token by 1.11 / 1.23 / 1.36 / 1.49 for k = 1–4 (p = 0.8).
- At ≥1,000, Continuum uses k = 2 and Rubin k = 4, about a 1.2× compute penalty for Rubin.
- The rest of the lead comes from three things, none of them a 4× effect:
  - latency budget: 62 × 20 µs = 1.24 ms of Rubin's 3.1 ms step;
  - FLOPs per provisioned watt: 13.1 PF/kW against 11.4 (Rubin35) and 16.3 (Rubin50);
  - HBM stacks.

## Workload and metrics

- **Primary workload:** decode of a DeepSeek-V4-Pro-class MoE.
  - 1.6T total / 49B active parameters, 61 layers.
  - 384 routed experts (top-6) plus 1 shared expert.
  - Compressed CSA/HCA attention, FP8 KV cache.
  - Context 128K (also 8K and 1M).
- **Speculation:** a one-layer block drafter with geometric acceptance.
  - p = 0.8 for code and tools; this fits reported acceptance lengths of 3.1–3.85 at depth 5.
  - p = 0.6 for prose.
- **Out of scope:** training, edge, and models under 200B (they already fit SRAM-only systems).
- **Main metric:** output tok/s per provisioned MW at a per-user speed floor, with each system at its best k. Sites are power-limited, and dropping the floor or best-k skews the comparison.
- **Also measured:** tokens per HBM stack (HBM4 is sold out; ~$600 per stack in 2026, ~$1,300 forecast for 2027).

## Measured per-layer latency (upper bounds)

| System type | Measured per-layer latency |
|---|---|
| On-silicon / one-hop static pipelines (Cerebras; Groq-3 LPX, the closest analogue) | ~5–15 µs |
| Multi-GPU NVLink (DGX B200 Maverick record; best V4-Pro GPU APIs) | ~45–110 µs |

- I assume the GPU gap is mostly software and dynamic all-to-all synchronisation. Megakernels could cut it 2–5×.
- Continuum adds two package-level collectives per layer to an LPX-class design.
- Neither τ is measured on the actual hardware.

**GPU calibration against GB300**

| tok/s/user | Model vs measured |
|---|---|
| 55 | 0.58× |
| 81 | 0.93× |
| 106 | 1.97× |

The error is about ±2× and not biased against GPUs, so read ratios, not absolute numbers.

## Architecture

**Package**
- **Compute:** 2 N2 C-Dies (288 tiles), 32 PF FP4 dense. Activations stay in place and weights stream past them.
- **W-Tier:** 4 SoIC-bonded N4 SRAM dies, 9.2 GB at 256 TB/s and 0.15 pJ/bit. Power, not bonds, caps the bandwidth.
- **K-Mem:** 4 × HBM4 (144 GB, ~10 TB/s), used for KV cache only. Weights never touch HBM.
- **Links:** 1.8 TB/s per direction. They never bind.
- **Power:** 2.1 kW TDP. **The 2.45 kW provisioned slot is an assumption, and it carries ~1.25× of the result.**
- **Thermal:** density is GPU-class, so there is no thermal advantage.

**Pod:** 192 packages (5 spare), ~470 kW across 3 racks.

**Mapping and the structural argument**
- Each layer is mapped to 3 packages, with every expert split into thirds.
- GPUs at large batch need data-dependent all-to-all across 72 endpoints.
- Continuum's collectives have fixed size, fixed peers and compile-time schedules. That is why its τ should sit near LPX, but this is an argument, not a measurement.

**Numerics:** NVFP4 experts and FP8 elsewhere. V4-Pro already runs at FP4 on GB300, so there is no accuracy cost relative to GPUs.

**SKUs**
- A 1-tier SKU (249 packages) halves SoIC demand and is nearly equal at p = 0.8, but weaker at p = 0.6.
- A 3-HBM-stack variant raises tokens per stack to 19.1k, against 14.3k for the primary.
- All-SRAM designs lose 3.3–22× on 1.6T models.

## Key numbers

**Operating points**

| Tier | Continuum | Rubin |
|---|---|---|
| ≥200 | 470 tok/s/user, 71.3k tok/s per package | Rubin35: 75.9k tok/s per GPU |
| ≥1,000 (Continuum k = 2, Rubin50 k = 4) | 57.3k tok/s per package | 53.0k tok/s per GPU; 40% of the step is exposed latency |

**Central case, M tok/s per MW (p = 0.8)**

| System | ≥200 | ≥1,000 | ≥1,500 |
|---|---|---|---|
| Rubin50 | 29.1 | 17.3 | 11.5 |
| Continuum | 29.1 | 23.4 | 18.8 |

**Max speed:** Continuum 5,261 tok/s/user, CS-4 5,573 (optimistic), Rubin 2,849.

**Activity energy**
- Continuum's advantage is 1.08× at throughput tiers and 1.13–1.32× at ≥1,000.
- FLOPs are 65–75% of activity energy for every design.

**Cost:** cost per token tracks tok/MW within ±30%. 2027 HBM prices would add ~10–15% in Continuum's favour.

**Other regimes against Rubin50**

| Regime | ≥200 | ≥1,000 | ≥1,500 |
|---|---|---|---|
| 8K | 0.99 | 1.21 | — |
| 1M | 1.16 | 1.59 | 2.6 |

**Prefill and agentic serving**
- Prefill is a tie: 0.90–1.14×.
- In the agentic blend, Continuum ties Rubin50 within ±15%, so prefill belongs on GPUs.

## Where it loses or ties

1. **Throughput tiers against Rubin50:** a tie.
2. **GPU τ ≈ 8 µs:** loses by 6–13%.
3. **Own τ ≈ 20 µs:** ties or loses unless GPUs stay above ~30 µs.
4. **Small models:** on ≤200B models, LPX or Cerebras likely win.
5. **Deployment unit:** ~470 kW. Small models waste it, and models over 1.6 TB need a second pod.
6. **Training:** not a target.
7. **Software:** starts from zero. GPUs gained ~5× on V4 in 43 days, and every GPU software gain shrinks the latency gap.

## What has to be true (against Rubin50; base 1.00 / 1.35 at ≥200 / ≥1,000)

| Assumption | If wrong |
|---|---|
| **τ gap (decisive)** | GPU-to-Continuum ratio ≤1.2× → ≤1.0 everywhere |
| Tile efficiency η = 0.6 | η = 0.45 → 0.78 / 0.98 |
| Slot power 2.45 kW | 3.06 kW → 0.80 / 1.08 |
| HBM stays scarce; models stay sparse MoE with compressed attention | Dense long-context attention makes decode HBM-bound: Continuum has 10 TB/s, Rubin 22 |

All of these must hold together. If any one fails, Continuum is just another inference chip.

## Risks

- **SoIC capacity:** 1 GW needs 1.5–2.3 months of TSMC's entire reported 2026 SoIC capacity, most of it already committed. The 1-tier SKU halves this.
- **HBM4:** ~1.6M stacks per GW against ~2.6M for Rubin. **This is Continuum's most robust advantage.**
- **Thermal and IR drop:** ~700 A per C-Die through TSV-perforated tiers.
- **Yield:** ~65% for the harvested N2 die.
- **Pipeline fragility:** the spares are mandatory.
- **Better drafters (p ≈ 0.9):** shrink the lead to ~1.0–1.15×.

## Software

- **Compiler path:** PyTorch/JAX → StableHLO → a compiler that emits static schedules.
- **MoE routing:** resolved inside a stage, with no runtime collectives. This is the source of the latency edge.
- **Serving:** a vLLM/SGLang plugin.
- **Existing models:**
  - Standard exported models run unchanged.
  - Custom CUDA/Triton kernels don't port.
  - New attention variants need compiler support.
  - Non-FP4/FP8 checkpoints need quantization.

## Kill tests

| # | Test | Kill if |
|---|---|---|
| 1 | Continuum τ (test chip) | >12 µs |
| 2 | Rubin τ on NVL72 V4-Pro | ≤12 µs → lead below 1.15×; don't tape out |
| 3 | Tile efficiency at M = 4–40 | η < 0.55 |
| 4 | W-Tier bandwidth and energy | <180 TB/s or >0.3 pJ/bit |
| 5 | Thermal and IR drop | Tj >105 °C or IR drop >5% |
| 6 | Production draft acceptance | p ≥ 0.85 |
| 7 | GPU calibration at 100–300 tok/s/user | >2× off |
| 8 | End-to-end sim with V4 routing traces | <70% of the modelled operating point |
| 9 | Bottom-up slot power | >2.8 kW |

None of these could be run here: there is no silicon, and model downloads are blocked.

## Facts vs assumptions

- **Facts:** chip specs, the V4-Pro configuration, acceptance lengths, measured speeds, InferenceX/SGLang throughput, and packaging and memory data.
- **Assumptions:** all τ values, pJ figures, slot powers, η, derates, costs and yields, and whether Rubin's 50 PF is usable.
- **Model outputs:** every throughput number.

**Files** (not committed) are in `/home/user/SomeRepository/engine/runs/refine_continuum/round4/`: `model4.py`, `run4.txt`, `calib4.txt`, `sku4.txt` and `ops4.txt`. Activity energy is carried over from `round3/energy4.txt`.