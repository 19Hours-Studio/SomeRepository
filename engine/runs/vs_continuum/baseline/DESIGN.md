# Continuum: a decode-first LLM inference accelerator (conceptual design)

Files: `roofline.py` (model), `results.txt`, `sensitivity.py` / `sensitivity.txt`.
Labels used below: **[F]** reported fact (source in NOTES), **[A]** design assumption, **[E]** my estimate from the model.

## 1. Scope and what "best" means here
- **Target:** data-center serving of frontier MoE LLMs (DeepSeek-V3-class: 671B total, 37B active, MLA, 61 layers),
  decode-dominated, 8K–128K contexts, for agent and reasoning traffic. **Not** a training chip, and **not** edge.
- **Metrics:** (1) tokens/s per user (interactivity, the SLO), (2) tokens/J and tokens/s per kW **at that SLO**,
  (3) tokens/s per HBM stack (HBM is the supply-limited input in 2026 [F]), (4) tokens/s per cm² of silicon (a cost proxy).
  "Best" means the Pareto frontier of (2–4) against (1). Peak FLOPS is not a metric. Agentic and reasoning output runs to
  thousands of tokens, so the interactivity at a given cost is what users and operators pay for.
- **No single "best" exists.** Continuum is designed to win at ≥200 tok/s/user. Below about 100 tok/s/user it only ties a
  well-run Rubin. It loses at training.

## 2. Architecture (all numbers per package unless stated)
| Block | Spec | Basis |
|---|---|---|
| Compute tiles | 2 × ~800 mm² N2 dies. 30 PF dense FP4, 15 PF FP8, 7.5 PF BF16 | [A] ≈0.6× Rubin's 50 PF NVFP4 on similar area |
| Weight SRAM ("W-stack") | Under each compute die sit 2 N5-class SRAM-only base dies, hybrid-bonded (SoIC) → 4 × ~2.5 GB = **10 GB**, **128 TB/s**, ~0.3 pJ/bit | [F] 38.1 Mb/mm² N2 macro; HD cell is ~0.021 µm² from N5 to N2, so the SRAM uses the cheap node. [E] ~3 MB/mm² usable × 800 mm². Cache-under-logic as in AMD 9800X3D [F] |
| KV memory | 6 × HBM4 12-Hi 36 GB = **216 GB**, **15 TB/s** (2.5 TB/s/stack) | [F] JEDEC 2 TB/s/stack; vendors claim 2.8–3.3 |
| Ridge point | FP8 15 PF / 15 TB/s = **1,000 FLOP/B** | MLA decode attention is **860 FLOP/B** at 4.5-bit KV [E] |
| Scale-up fabric | 1.8 TB/s/dir, 224G copper, 64 packages, single-switch-hop, compiler-scheduled; target ≤1 µs per all-to-all traversal | [A]. The needed bandwidth is only ~0.1 TB/s per package at B=4096 [E]. Latency is what matters |
| Power | 1.8 kW TDP (compute ~0.9 kW, W-stack ≤0.3 kW, HBM ≤0.5 kW at full rate). Rack = 64 pkgs ≈ 144 kW incl. 1.25× overhead | [E] |
| Package | CoWoS-L ~4 reticle; 2 SoIC stacks + 6 HBM4 | [A]. Smaller than Rubin's 8-stack package |

Rack (one model replica): 640 GB SRAM holds 377 GB of 4.5-bit DSv3 weights plus hot-expert duplicates. The rack has
13.8 TB of HBM for KV, 960 TB/s KV bandwidth, 1.9 EF FP4, and 384 HBM stacks (Rubin NVL72: 576).

**Why this split.** Weight bytes are shared by every user and are read on every step. KV bytes are private and grow
with B×L. Putting weights in bonded SRAM takes them off HBM. That frees all 15 TB/s of HBM for KV, and weight reads
stop setting a floor on step time. Small batches can therefore still meet a 1000 tok/s SLO. The capacity problem of
SRAM-only chips is solved because KV lives in HBM. A 128K MLA user needs 2.6 GB of KV, which is about 5 Groq-3 LPUs' worth.

## 3. Numerics
NVFP4 or MXFP4 weights (4.5 b/value incl. scales). NVFP4 KV at 4.5 b [given]. FP8 QK/PV attention, with an FP32
softmax and accumulators. BF16 is used for the router and norms. An FP8 weight fallback halves capacity, so a replica
then needs 128 packages.

## 4. Results (DSv3-671B, 32K context; `results.txt`)
| ≥ tok/s/user | System | tok/J | tok/s/kW | tok/s per HBM stack | chips |
|---|---|---|---|---|---|
| 50 | Rubin NVL72, opt. SW (25 µs/layer) | 7.4 | 5,593 | 2,010 | 72 |
| 50 | Continuum ×64 | 7.9 | 6,594 | 2,473 | 64 |
| 200 | Rubin NVL72, today's SW (100 µs/layer) | infeasible | – | – | 72 |
| 200 | Rubin NVL72, opt. SW | 6.5 | 4,227 | 1,519 | 72 |
| 200 | Ironwood ×64 | 3.3 | 1,482 | 232 | 64 |
| 200 | Continuum ×64 | 7.75 | 6,200 | 2,325 | 64 |
| 1000 | Groq-3 LPU (600 W assumed) | 2.15 | 747 | n/a | 2,313 |
| 1000 | Cerebras WSE-3 | 0.50 | 155 | n/a | 11 wafers |
| 1000 | Continuum ×64 | 6.35 | 3,978 | 1,492 | 64 |

**Where it loses:**
- Tokens/s per cm² of silicon at ≤100 tok/s/user: ~0.5× Rubin (515 vs 1005). The SRAM area costs money.
- KV capacity per rack: 13.8 TB vs 20.7 TB.
- 128K MLA contexts: attention compute dominates on every system, so the lead shrinks to ~1.08× tok/J (2.07 vs 1.92).
- Training: a Continuum-T SKU would be at best ~0.6–0.85× Rubin.

**Sensitivity (`sensitivity.txt`):**
- If Continuum's per-layer floor is 12 µs, it still meets 1000 tok/s/u, at 1,785 tok/s/kW. At 20 µs, 1000 tok/s/u is infeasible.
- If Rubin's software reaches 10 µs/layer, its lead at 200 tok/s/u shrinks to 1.18× (6,200 vs 5,253). At 1000 tok/s/u Rubin still reaches only 639 tok/s/kW.
- SRAM at 0.6 pJ/bit instead of 0.3 changes almost nothing.
- Halving compute halves the lead. Compute density and the latency floor decide the result. SRAM energy does not.

## 5. Software
PyTorch/JAX → torch.export/StableHLO → Continuum compiler, which does three things:
1. Weight-stationary placement of experts in W-stack banks.
2. Static, deterministic fabric schedules, Groq/TPU-style, with slot-based MoE all-to-all and a capacity factor.
3. Paged KV in HBM.

The serving plugin targets vLLM/SGLang (prefill/decode disaggregation; prefill runs on Continuum-T or on GPUs).
Existing checkpoints run without retraining after PTQ to NVFP4. Custom CUDA kernels do not port. Dynamic shapes are
padded into fixed buckets. The Groq and TPU compilers show this works but takes years of engineering.

## 6. Limits and risks
- **HBM supply:** sold out for 2026 [F]. Continuum needs 33% fewer stacks per rack.
- **CoWoS:** fully booked [F]. SoIC adds a second constrained step.
- **Thermal:** the compute die sits on top, next to the cold plate, so heat does not cross the SRAM. Power, however, must
  cross 2 base dies through TSVs, so IR drop is a risk.
- **Yield:** the compound yield of KGD SRAM stacking. SRAM can be repaired; the 800 mm² N2 compute dies are the yield risk.
- **Workload drift:** models above ~1.1T params at 4.5 b exceed 640 GB → 2 racks per replica, and the floor doubles.
- **Sparse attention:** DSA-style attention shifts the bottleneck to indexer KV reads (~1 GB/user at 128K [E]).

## 7. Falsification plan (cheapest first)
1. **Fabric latency (decisive).** Run a cycle-level simulation (BookSim2 / ASTRA-sim) of dispatch+combine for 128–512 tokens × 7168 FP8 across 64 packages.
   Kill criterion: >3 µs per traversal, or a per-layer floor >12 µs.
2. **Decode simulator.** Calibrate LLMCompass or this model against the InferenceMAX GB200 curve and the Cerebras/Groq tok/s/user figures.
   Kill criterion: the model misses measured points by >30%.
3. **W-stack energy and thermal.** Run CACTI/Accelergy for the 0.3 pJ/bit figure, and HotSpot for 1.1 W/mm² over 2 bonded dies.
   Kill criterion: Tj > 105 °C or IR drop > 5%.
4. **Numerics.** Evaluate NVFP4 weights and KV on long-context evals. This needs model weights, which were unavailable here.
   Kill criterion: more than a 1-point drop.
5. **Silicon.** Build a 2-package test vehicle and measure pJ/bit and hop latency.
