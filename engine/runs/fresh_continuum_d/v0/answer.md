I ran the round-7 model in `/home/user/SomeRepository/engine/runs/refine_continuum/round7/`. Two things came out of it. First, a fairness fix made my own new lever look worse, and I report it. Second, a design change (Continuum-7) raises the result honestly: about 1.17× Rubin at bulk speeds, 1.6–2.5× at ≥1,000 tok/s/user, and 3–4× tokens per HBM stack. It still loses to Rubin Ultra if Nvidia's 600 kW figure holds. As before, every Continuum number comes from a model; there is no silicon.

# Continuum-7: a weight-stationary 3D-SRAM decode accelerator for frontier MoE, built wide and run slow

## 0. Verdict

### 0.1 What changed this round
All figures are for DeepSeek-V4-Pro at 128K context with draft acceptance p = 0.8. Each cell is output tok/s per provisioned watt, as a ratio to the best Rubin setup at that per-user speed floor.

| Step | ≥200 | ≥500 | ≥1,000 | ≥1,500 | ≥2,000 |
|---|---|---|---|---|---|
| Round-6 headline (Continuum-6), reproduced exactly | 1.04 | 1.08 | 1.27 | 1.51 | 1.90 |
| New lever, first pass: 4 C-dies run at 0.55 V (C7) | 1.21 | 1.29 | 1.52 | 1.82 | 2.51 |
| **Fairness fix A:** one undervolt law and one slot-saving rule for every system (Rubin gets 0.55–0.65 V too) | 1.05 | 1.16 | 1.41 | 1.54 | 2.27 |
| Continuum-6 under the same fix | 0.94 | 1.04 | 1.23 | 1.30 | 1.87 |
| **Design change: trim over-provisioned links and hosts → Continuum-7** | **1.17** | **1.29** | **1.57** | **1.70** | **2.47** |
| Same at 1M context | 1.21 | 1.21 | 1.44 | 2.00 | 3.68 |
| Same with NVFP4 KV cache on every system, 128K | 1.17 | 1.29 | 1.47 | 1.57 | 2.17 |

- **Fairness fix A was the big correction.** My first pass credited Continuum's undervolt savings at 1.146 W of slot power per W of chip power, but Rubin's at 0.83. With one rule for both, Rubin's best rises 18% at ≥200 (37.9 → 44.9 tok/s/W), because Rubin can undervolt too. So most of the first-pass gain at low speeds was an accounting artefact, and I removed it.
- **Other fixes:**
  - Fixed per-layer latency now scales with clock for every system: τ = 7 µs + 3 µs/f.
  - Groq LP30 has no FP4 ([SemiAnalysis](https://newsletter.semianalysis.com/p/nvidia-the-inference-kingdom-expands), [More Than Moore](https://morethanmoore.substack.com/p/nvidia-introduces-groq-lp30-and-lpx)), so the Rubin+LPX baseline now holds expert weights in FP8.
  - Rubin Ultra is re-derived bottom-up (§2).
- **What survives at the bulk tier (1.17×) and why:** a slot-level FLOPs-per-watt edge of 22.8 vs 18.6 PF/kW (×1.23), minus worse tile imbalance (1.12 vs 1.07). On the same process node it is **1.06×**, i.e. a tie. At bulk speeds no memory hierarchy beats a same-node GPU by much, because both are bound by MAC energy.
- **Where the large gain is real:** ≥1,000 tok/s/user. Continuum-7 stays at its bulk efficiency (52.4 tok/s/W) up to 1,158 tok/s/user. Rubin falls to 33.4, because it must speculate deeper (k = 4) and becomes HBM-bound. On the same node this is still 1.42×.

### 0.2 Defensible claims

| Claim | Number | Holds only if |
|---|---|---|
| Tok/MW against Rubin, 1.6T MoE at 128K, ≥200 / ≥1,000 / ≥2,000 tok/s/user | **1.17 / 1.57 / 2.47×** (same node: 1.06 / 1.42 / 2.25) | Tile efficiency η ≥ 0.5 (η = 0.5 gives 0.97 / 1.31 / 2.06); logic runs at 0.55 V (floor at 0.60 V gives 1.08 / 1.45 / 2.47) |
| Tokens per HBM stack against Rubin | **3.0× (≥200), 4.0× (≥1,000), 9.3× (≥2,000)**; 3.6–4.3× at 1M | HBM is scarcer than SoIC for the buyer |
| Against Rubin Ultra built bottom-up (5.69 kW per slot, matching the 820 kW report) | 1.03 / 1.14 / 1.19× at 128K; 0.90 / 1.09 / 1.33× at 1M | Ultra power as derived in §2 |
| **Against Rubin Ultra at Nvidia's 600 kW and full 100 PF** | **0.91 / 1.11 / 1.13×**; with Ultra also undervolted: **0.75 / 0.83 / 0.87×** | Implies 47% better FLOP/W than Rubin on the same N3P node (§2) |
| Against MI455X / TPU 8i / Rubin+LPX / CS-4 at 128K, ≥200–2,000 | 1.9–4.0× / 2.1–11× / 7.8–11× / 22–27× | Power for TPU and LP30 is guessed; CS-4 is outside its design envelope at 1.6T |

**Bottom line.** Continuum-7 is a credible "best tokens per MW and per HBM stack above ~1,000 tok/s/user" design for frontier sparse MoE against what ships in 2026. It is **not** shown to be the best in the world:
- at bulk speeds it is a same-node tie;
- it loses to Rubin Ultra if Nvidia's 600 kW rack delivers the full 100 PF;
- every Continuum number is model output.

### 0.3 Calibration warning (now V4-native; decisive)
- **InferenceX, GB300, V4-Pro FP4, 8K in / 1K out, MTP:** ~11.2–12k tok/s per GPU at ~50 tok/s/user ([PyTorch/SGLang](https://pytorch.org/blog/serving-deepseek-v4-on-gb300-with-sglang-5x-higher-throughput-at-the-same-interactivity-since-day-0/), [LMSYS](https://x.com/lmsysorg/status/2065513735213773021)).
- **My model, with prefill GPUs charged** (`calib7.txt`): 63k total tok/s per GPU. If InferenceX counts input plus output tokens (my reading of its [glossary](https://inferencex.semianalysis.com/glossary/throughput); not stated), **GPUs realise ~0.19 of the model**. MLPerf R1 gave 0.09–0.33 (`round5/calib5.txt`).
- **Break-even:** Continuum must realise at least 85% (≥200), 64% (≥1,000) or 40% (≥2,000) of the fraction GPUs realise. This is unmeasured and is the main unknown.

---

## 1. Target workloads and metrics
- **Workload:** decode of DeepSeek-V4-Pro:
  - 1.6T total / 49B active parameters, 61 layers;
  - 384 experts, top-6, plus 1 shared; expert FFN size 3072;
  - compressed sparse attention on 30 layers, 128× compressed attention on 31 layers;
  - FP8 KV cache.
- **Conditions:** 128K and 1M context; p = 0.8 (code and tools) or 0.6 (prose).
- **Stress case:** a 6.2T model with the same active parameters.
- **Out of scope:**
  - training;
  - edge;
  - models under ~200B, where SRAM-only systems win;
  - prefill, which stays on GPUs (compute-bound, so a tie).

| Metric | Why it defines "best" |
|---|---|
| Output tok/s per provisioned MW at a per-user speed floor (200…2,000 tok/s/user) | Sites are power-limited, and the floor prevents gaming at low speeds. Each system chooses its own draft depth k (0–7), microbatch count m (1–4), parallel layout and **voltage (0.55–0.75 V plus vendor Max-Q)**. |
| Tok/s per HBM stack | HBM is supply-limited through 2027. |
| Max tok/s/user | The speed tier for agents and reasoning. |
| Cost per token | Rough only (§4.5). |

**Gate.** A gain counts only if it holds with:
- the same V/f law, slot-saving rule and latency model for every system;
- Rubin given its best layout (NVL72 or multi-rack; multi-rack never wins, `round6/run6c.txt`).

## 2. Reference points (vendor, press or analyst; conflicts noted)

| Design | Compute | Memory | Provisioned power per slot |
|---|---|---|---|
| Rubin VR200 | 35 PF FP4 dense; "50" with adaptive compression; N3P | 288 GB HBM4, 22 TB/s | Max-P 3.06 kW (220 kW rack); Max-Q 2.64 kW at compute ×0.92 (generous). Law points 0.55–0.65 V: 1.71–2.29 kW. |
| Rubin Ultra (2H 2027) | 100 PF FP4 per 4-die package (70 dense); N3P | 768 GB–1 TB HBM4E, ~32 TB/s | Nvidia: 600 kW per 144 packages = 4.17 kW ([DCD](https://www.datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027/); no update found in 2026). **Bottom-up from Rubin's per-die power** (4 × 935 W + 2 × 430 W HBM/IO + ~1 kW rack overhead) gives **5.6–5.7 kW**, matching the 820 kW reports. At 600 kW with full clocks, each die would need 1.04 kW all-in against Rubin's 1.53 kW on the same node. |
| MI455X | 40 PF MXFP4 (70% treated as dense) | 432 GB, 19.6 TB/s | 3.2 kW (estimate) |
| TPU 8i / Ironwood | 10.1 PF FP4 / 4.6 PF FP8 | 288 GB at 8.6 TB/s / 192 GB at 7.37 TB/s | 1.3 / 1.2 kW (guesses) |
| Groq LP30 / LPX | 1.2 PF **FP8 only**; 500 MB SRAM at 150 TB/s | — | ~600–625 W (unconfirmed analyst figure) |
| Cerebras CS-4 | ~25 PF per wafer; 44 GB SRAM | — | ~43 kW per wafer (estimate) |

- **Process:** TSMC gives N2P −36% power at iso-speed against N3E ([TSMC](https://www.tsmc.com/english/dedicatedFoundry/technology/platform_HPC_tech_advancedTech)). I use −20% for N2 against N3P, so C-die compute is 0.041 pJ/FLOP against 0.049 for Rubin; the same-node case is in §4.3. For A16 I use −18% (assumed).
- **Measured Rubin efficiency:** 59.4M total tok/s/MW at 100 tok/s/user on pre-release software, against 28.5M for GB300 ([AI Weekly summary of SemiAnalysis](https://aiweekly.co/alerts/semianalysis-benchmarks-vera-rubin-nvl72-at-7x-blackwells-tokens-per-mw-on)). The workload mix (AgentX with cached input) prevents an output-only calibration.
- **Packaging and supply:** carried over. SoIC is ~10–15k wafers/month; CoWoS ~130k wafers/month by late 2026; HBM4 ~$600 per stack in 2026, forecast ~$1,300 in 2027.

## 3. Architecture

### 3.1 Package blocks (Continuum-7)

**C-Die (compute)**
- 4 per package on N2, ~750 mm² each, 144 tiles each.
- Each tile: a ~111 TF FP4 tensor engine at f0 plus an FP32 vector/softmax unit.
- **64 PF FP4 / 32 PF FP8 dense at 0.75 V; 40.6 / 20.3 PF at 0.55 V** (f = 0.635 f0 from the alpha-power law: Vt 0.30 V, α 1.3).
- Zero-skip front end assumed equal to Rubin's (×1.43). With zero-skip off on both: 1.17 / 1.48 / 2.01×.
- **Why wide and slow:** at 0.55 V dynamic energy per operation is ×0.54. Four dies at 0.635 f give 1.27× the throughput of C6's two dies at Max-P, for 0.91× the slot power.

**W-Tier (weight SRAM)**
- 8 N4-class SRAM tiers, hybrid-bonded under the C-Dies: 18.4 GB.
- 512 TB/s at f0, clocked with the compute (325 TB/s at 0.55 V), at 0.15 pJ/bit.

**K-Mem (KV cache only)**
- 4 × HBM4 16-high: 192 GB at 10 TB/s.

**Link (trimmed)**
- 64 × 224G lanes per direction: 1.8 TB/s, 85% usable, 144 W (C7 untrimmed had 128 lanes).
- At the operating points it takes 10.8 µs of a 12.5 µs microbatch, so it never binds.

**Host and NIC (trimmed)**
- One CPU per 8 packages: 50 W per slot.
- One 800G NIC per package (30 W) for KV ingress from GPU prefill. That traffic is ~0.4 Tb/s per package at the ≥200 point: 29k requests/s × 0.65 GB × 1/373.
- Switch plane: 30 W.

**Slot power** (`run7c.txt`, then trimmed in `run7d.txt`)

| | 0.75 V | **0.55 V (operating point)** |
|---|---|---|
| Compute | 2,640 W | 902 W |
| Leakage | 500 W | 367 W |
| W-Tier | 614 W | 390 W |
| HBM | 320 W | 320 W |
| Links | 144 W | 144 W |
| Conversion and cooling | ×1.146 | ×1.146 |
| Host, NIC, switch | 110 W | 110 W |
| **Slot** | **4.9 kW** | **2.54 kW** |

**Thermal and packaging**
- Compute power density ≈ 0.4 W/mm² at 0.55 V, about a third of a GPU's. This makes SRAM-under-logic stacking easier.
- ~580 A per C-Die.
- 4 SoIC stacks plus 4 HBM sites on a ~5-reticle CoWoS-L interposer, the same class as Rubin Ultra.

### 3.2 Mapping
**Layer groups (g packages per layer)**
- Each expert's intermediate dimension is split g ways, then over tiles.
- The compiler picks g and V per deployment:
  - ≤500 tok/s/user: g = 3, a **187-package pod**, with the same ratio (1.17 / 1.29);
  - ≥1,000 tok/s/user: g = 6 (373 + 11 spares).
- At g = 3 the SRAM is 27% full; the free space holds hot-expert replicas.
- Attention is data-parallel: each package re-reads the 0.43 GB of attention and shared weights every microbatch.

**Microbatching**
- m = 2–3; cycle T = max(m·c, c + τ).

### 3.3 Numerics

| Data | Format |
|---|---|
| Expert weights | NVFP4, zero-compressed |
| Attention, shared expert, drafter | FP8 |
| Indexer | FP4 |
| Accumulation, softmax | FP32 |
| Partial sums on links | BF16 |
| KV cache | FP8 (NVFP4 optional, applied to all systems in §0.1) |

V4-Pro is already served in FP4 on GB300, so the weight format adds no new accuracy risk.

### 3.4 Variants

| SKU | Change | Result at 128K (≥200 / ≥1,000 / ≥2,000) |
|---|---|---|
| **Continuum-7** (primary) | As above | 1.17 / 1.57 / 2.47× Rubin |
| Continuum-7-A16 | C-dies on A16 | 1.26 / 1.69 / 2.68× Rubin; 1.11–1.29× bottom-up Ultra; 0.98–1.23× Ultra at 600 kW |
| Continuum-6 (round 6) | 2 C-dies, Max-Q | 0.94 / 1.23 / 1.87× under fair accounting. Superseded. |
| Continuum-G | GDDR7 for KV, no HBM (round 6) | Carried over; for HBM-starved buyers |

## 4. Sanity arithmetic

### 4.1 Operating points (`run7d.txt`, 128K)

| Tier | System | Setting | tok/s/user | tok/s/W | Binding resource (µs per microbatch) |
|---|---|---|---|---|---|
| ≥200 – ≥1,000 | C7 | 0.55 V, k = 1, b = 407, m = 2, g = 6, slot 2,542 W | 1,158 | **52.4** | compute 12.5 (KV 11.3, link 10.8, SRAM 8.6); T 25.1 |
| ≥200 | Rubin | 0.60 V, k = 1, B = 23,324, slot 1,981 W | 323 | 44.9 | compute ≈ HBM |
| ≥1,000 | Rubin | 0.60 V, **k = 4**, B = 5,014, tensor-parallel 2 | 1,119 | 33.4 | HBM ≈ compute |
| ≥1,500 | C7 / Rubin | 0.55 V, k = 1, m = 3 / 0.55 V, k = 6, tensor-parallel 4 | 1,548 / 1,630 | 47.6 / 28.0 | — |
| ≥2,000 | C7 / Rubin | 0.60 V, k = 2 / 0.55 V, k = 6 | 2,153 / 2,038 | 43.2 / 17.5 | — |

### 4.2 Hand check, C7 at ≥200
- Positions per microbatch: 407 × 2 = 814.
- Time per position per layer, summed: **4.95e-8 s**:
  - linear: 1.655 GFLOP ÷ (64 PF × 0.635 × 1.43);
  - attention: 0.297 GFLOP ÷ (32 PF × 0.635);
  - indexer: 0.26 GFLOP ÷ (64 PF × 0.635).
- 814 × 4.95e-8 ÷ 6 packages × 1.12 imbalance ÷ 0.6 efficiency = **12.5 µs** ✓
- Speed: 1.8 accepted tokens ÷ (62 × 25.1 µs) = **1,157 tok/s/user** ✓
- Efficiency: 0.85 × 50,468 users × 1,158 tok/s ÷ (373 × 2,542 W) = **52.4 tok/s/W** ✓
- **Where 1.17× comes from:**
  - C7: 40.6 × 1.43 ÷ 2.542 kW = 22.8 PF/kW;
  - Rubin: 25.8 × 1.43 ÷ 1.981 kW = 18.6 PF/kW;
  - ratio 1.23, times the imbalance penalty 1.07/1.12 = **1.17** ✓
- **Where 1.57× at ≥1,000 comes from:** C7 is unchanged, while Rubin pays deeper speculation (k = 4 wastes 1.49 FLOPs per accepted token against 1.11 at k = 1) and HBM-bound weight reads (expert-weight floor 9 µs per layer per microbatch).

### 4.3 Sensitivity (ratio to best Rubin; 128K, ≥200 / ≥1,000 / ≥2,000)

| Change | Ratio |
|---|---|
| Base | 1.17 / 1.57 / 2.47 |
| Same node (C-die energy ×1.25) | 1.06 / 1.42 / 2.25 |
| η = 0.5 (Continuum only) | **0.97** / 1.31 / 2.06 |
| W-Tier at 0.30 pJ/bit | 0.99 / 1.33 / 2.03 |
| Leakage ×2 | 1.00 / 1.35 / 2.16 |
| Tile imbalance 1.25 | 1.05 / 1.40 / 2.21 |
| Vmin floor 0.60 V for all | 1.08 / 1.45 / 2.47 |
| Vendor profiles only, for all | 1.08 / 1.32 / 2.33 |
| Collectives 12 µs | 1.17 / 1.57 / 2.24 |
| V/f law with Vt 0.35 or α 1.6 | ~0.95× of base (from `run7b.txt`) |

- **At ≥200 the gain is gone under any one adverse assumption** (η, W-Tier energy or leakage).
- **At ≥1,000 it survives every single adverse assumption tested, and pairs of them.**

### 4.4 Supply, per GW at ≥200 (`run7e.txt`)

| | HBM stacks | Leading-edge logic | SoIC passes |
|---|---|---|---|
| Rubin | 4.04M | 8.3M cm² (N3P) | — |
| C7 | **1.57M** | 11.8M cm² (N2) | 68k (4.6–6.8 months of 2026 capacity) |
| C6 | 1.23M | 6.1M cm² | 36k |

- Wide-and-slow spends logic area and SoIC capacity to save power: about 1.2× Rubin's logic area per token, but 3× fewer HBM stacks per token.
- SoIC becomes the binding supply line.

### 4.5 Cost (assumptions)

| | Package BOM | tok/s per package at ≥200 |
|---|---|---|
| C7 | ~$11–15k (4 N2 dies ~$2.6k; 8 tiers ~$2.5k; 4 × 16-high HBM $3.6–7.8k; CoWoS-L/SoIC/test ~$2.5k) | 133k |
| Rubin | ~$7.6–13k | 89k at 0.60 V |

- Tokens per BOM dollar: C7 ~1.1–1.4× at ≥200 and ~1.5–1.9× at ≥1,000. Rough.
- A 187-package bulk pod is ~$2.4M BOM and ~0.48 MW.

## 5. All-system comparison (`run7d.txt`; same law and τ(f) for every system)

**Continuum-7 ratio, 128K / 1M, per-user speed tiers ≥200 / ≥500 / ≥1,000 / ≥1,500 / ≥2,000**

| Against | 128K | 1M |
|---|---|---|
| Rubin | 1.17 / 1.29 / 1.57 / 1.70 / 2.47 | 1.21 / 1.21 / 1.44 / 2.00 / 3.68 |
| Ultra, bottom-up | 1.03 / 1.03 / 1.14 / 1.14 / 1.19 | 0.90 / 0.90 / 1.09 / 1.25 / 1.33 |
| Ultra, 600 kW at 100 PF | 0.91 / 1.00 / 1.11 / 1.10 / 1.13 | 0.92 / 0.92 / 1.07 / 1.34 / 1.69 |
| Ultra, 600 kW plus undervolt | 0.75 / 0.75 / 0.83 / 0.83 / 0.87 | 0.66 / 0.66 / 0.80 / 0.91 / 0.98 |
| MI455X | 1.92 / 2.12 / 2.40 / 2.80 / 3.97 | 1.48 / 1.63 / 2.07 / 3.02 / 5.88 |
| TPU 8i | 2.12 / 2.55 / 3.37 / 4.17 / 11.4 | 1.61 / 2.05 / 2.85 / 5.91 / 22 |
| Rubin + LPX (FP8 weights) | 7.8 / 7.8 / 8.1 / 9.5 / 11.2 | 12.9–19.5 |
| CS-4 | 22–27 | 21–23 |

- **Max tok/s/user (modelled):** C7 5,894; CS-4 5,737; Ultra 5,557; Rubin 4,949.
- **Other regimes:** ratios above ~3× (p = 0.6 at ≥1,500, the 6.2T model at ≥1,000) mean Rubin is near its speed ceiling, not that Continuum is more efficient; I don't claim them.
- **6.2T model, 128K:** 1.22 / 1.48 / 2.01× at ≥200 / ≥500 / ≥1,000.

## 6. Software stack and programming model
- **Front end:** PyTorch (`torch.export`) and JAX (StableHLO) → MLIR compiler → **static spatial schedule**. The schedule covers:
  - layer-to-group placement (g);
  - expert slicing over tiles;
  - hot-expert replication from a routing profile;
  - m, k;
  - **a voltage/frequency point per deployment** (new: the tier choice sets V, g and m together);
  - fixed-size collectives.
  
  Recompiling a model is an offline step of hours.
- **Kernels:** a tile-level DSL (block-matmul, softmax, gather) for compressed sparse attention, the FP4 indexer and MLA. No warp/thread model.
- **Serving:** a vLLM/SGLang backend plugin with continuous batching at stage boundaries, paged KV in K-Mem and a built-in block drafter. Prefill runs on GPUs, with KV shipped over the per-package 800G NIC.
- **Existing models:** MoE and dense checkpoints convert by NVFP4 post-training quantization; V4-Pro and gpt-oss need no new quantization. Models of 200B or less waste a pod. Training and dynamic control flow stay on GPUs.
- **Maturity risk:** GPU software for V4 improved 2.1–2.6× at matched interactivity in about two months. Continuum starts from zero, and §0.3 depends on this stack.

## 7. Where Continuum loses or ties
1. **Bulk tier (≤500 tok/s/user):** 1.17–1.29×, but 1.06× on the same node and 0.97× at η = 0.5. Physically it is a tie.
2. **Rubin Ultra at Nvidia's 600 kW:** loses 9% at ≥200, wins ~1.1× at ≥1,000. If Ultra also undervolts, it loses by 13–25%.
3. **Ultra at 1M context, ≤500 tok/s/user:** 0.90×. Ultra's 32 TB/s of HBM per package wins on long-context KV.
4. **Logic and SoIC per token:** ~1.2× Rubin's leading-edge area per token and 68k SoIC passes per GW.
5. **Deployment unit:** 187 packages (bulk) or 373 (speed tier) per 1.6T instance.
6. **Training:** not supported.
7. **Calendar:** 2028 at the earliest. Nvidia's 2028 Feynman generation has unknown specs and may remove the node advantage.

## 8. What has to be true

| Assumption (base) | If wrong | Effect at ≥1,000 tok/s/user |
|---|---|---|
| Continuum realises the same fraction of its model as GPUs (~0.19) | Lower | Scales directly; break-even at 64% of the GPU fraction |
| η = 0.6 on narrow expert slices | 0.5 | 1.31 |
| 0.55 V logic operation on N2 | 0.60 V floor | 1.45 |
| W-Tier at 0.15 pJ/bit | 0.30 | 1.33 |
| N2 compute energy 0.8× N3P | Same node | 1.42 |
| Rubin Ultra ≥ 5.7 kW per slot | 4.17 kW at 100 PF | 1.11 (0.83 if also undervolted) |
| Sparse MoE with compressed attention stays the frontier | Dense long-context attention | KV-bound; Continuum loses |
| p ≈ 0.8 | p ≥ 0.9 | Rubin's speculation waste falls; gain shrinks toward ~1.3 |

## 9. Risks and physical, process and supply limits
- **SoIC:** 4.6–6.8 months of 2026 capacity per GW. New capacity is reported at ~$7B per 10k wafers/month.
- **CoWoS-L:** ~5 reticles, the same class as Rubin Ultra.
- **HBM:** 1.57M 16-high stacks per GW; 16-high volume is unconfirmed (fallback 12-high, ≤5% loss).
- **Low-voltage operation:** timing variation at 0.55 V needs adaptive clocking. SRAM sits on a separate rail at ≥0.65 V.
- **Yield:** a 750 mm² N2 die is ~47% raw and ~65% with harvesting. Bond interfaces are 98–99% each, so known-good-die testing is mandatory.
- **Pipeline fragility:** 11 spares per pod (×0.97, not included in the ratios).
- **Workload drift:** fewer, larger experts or dense attention erode the design.

## 10. Tests that could prove the design wrong

| # | Test | Tool | Kill criterion |
|---|---|---|---|
| 1 | **Realisation:** V4 traces through an event-level Continuum simulator, against the GPU model's 0.19 fraction on InferenceX | LLMCompass-class simulator | Continuum below 64% of the GPU fraction at ≥1,000 |
| 2 | Tile η at M = 4–40, N = 32–64, NVFP4 with zero-skip | Timeloop/Accelergy + one-tile RTL | η < 0.5 |
| 3 | **N2 V/f and energy at 0.55 V** | Foundry PDK SPICE on the MAC array | f < 0.55 f0 or energy > 0.6× nominal |
| 4 | W-Tier energy and bandwidth through the bond | CACTI/DESTINY | > 0.25 pJ/bit or < 300 TB/s |
| 5 | Collectives across 6 packages | SerDes/switch simulation | > 12 µs |
| 6 | Rubin at its best undervolt at ≥1,000 | Own runs | > 40 tok/s/W voids 1.57× → ≤1.3× |
| 7 | Rubin Ultra rack power at 100 PF | Vendor data or measurement | ≤ 4.5 kW per slot → loses the calendar comparison |
| 8 | Thermal and IR drop | HotSpot/3D-ICE, PDN solver | Tj > 105 °C or IR drop > 5% |

None of these could be run here. Tests 1, 3 and 2 matter most.

## 11. Facts vs assumptions
**Facts (sourced, many secondary):**
- chip specifications in §2; Rubin Ultra's 600 kW (Nvidia) against 820 kW (reports);
- LP30 has no FP4;
- TSMC's N2P −36% iso-speed claim against N3E;
- InferenceX V4-Pro throughput points;
- V4 configuration;
- packaging capacity.

**Derived by me:**
- bottom-up Rubin Ultra power;
- GPU realisation fraction 0.19 (assumes InferenceX counts total tokens);
- KV ingress bandwidth per package;
- supply per GW.

**My assumptions:**
- V/f law (V0 0.75 V, Vt 0.30 V, α 1.3), τ(f), and the 1.146 slot-saving rule for all;
- every pJ figure;
- leakage splits;
- η = 0.6 and the 0.85 derate;
- slot powers other than vendor rack figures;
- costs and yields.

**Model outputs:** every throughput, ratio and energy figure for every system.

**Files** (in `/home/user/SomeRepository/engine/runs/refine_continuum/round7/`; not committed):

| File | Contents |
|---|---|
| `model7.py` | V/f law, symmetric profiles, C7/C7T, Ultra, FP8-weight LPX; imports `round6/model5.py` |
| `check7.py` → `check7.txt` | Round-6 reproduction; profile table |
| `run7.py`, `run7b.py`, `run7c.py` → `.txt` | Untrimmed C7, sensitivities, operating points |
| **`run7d.py` → `run7d.txt`** | **Final tables** |
| `run7e.py` → `run7e.txt` | Extreme Ultra bound; supply per GW |
| `calib7.py` → `calib7.txt` | V4-Pro calibration against InferenceX |

`run7.txt` and `run7b.txt` are from the rerun after fairness fix A; the before-fix C7 figures appear in the first-pass row of §0.1. `run7c.txt` was not rerun, so it still shows untrimmed slot powers under the old accounting.

---

**Sources** (new this round first; round-6 sources still apply)
- [DCD: Rubin Ultra NVL576 at 600 kW, 2H 2027](https://www.datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027/)
- [rdp.in: Rubin Ultra / Kyber planning](https://rdp.in/gpu-mart/knowledge-base/rubin-ultra-kyber-nvl576-planning-2027-flagship-rack/)
- [VRLA Tech roadmap](https://vrlatech.com/nvidia-gpu-roadmap-2026-2030/)
- [Barrack AI: Rubin at GTC 2026](https://blog.barrack.ai/nvidia-rubin-specs-architecture-2026/)
- [More Than Moore: LP30/LPX](https://morethanmoore.substack.com/p/nvidia-introduces-groq-lp30-and-lpx)
- [SemiAnalysis: Inference Kingdom (LP30, LP35)](https://newsletter.semianalysis.com/p/nvidia-the-inference-kingdom-expands)
- [StorageReview LPX](https://www.storagereview.com/news/nvidia-groq-3-lpx-everything-we-know)
- [The Register: LPX deep dive](https://www.theregister.com/2026/03/19/nvidia_lpx_deep_dive/)
- [TSMC N2/N3 HPC technology](https://www.tsmc.com/english/dedicatedFoundry/technology/platform_HPC_tech_advancedTech)
- [PyTorch/SGLang: V4 on GB300](https://pytorch.org/blog/serving-deepseek-v4-on-gb300-with-sglang-5x-higher-throughput-at-the-same-interactivity-since-day-0/)
- [LMSYS: >12K tok/s/GPU V4-Pro](https://x.com/lmsysorg/status/2065513735213773021)
- [InferenceX throughput glossary](https://inferencex.semianalysis.com/glossary/throughput)
- [InferenceX V4-Pro rankings](https://inferencex.semianalysis.com/rankings/fastest-gpu-for-deepseek-v4)
- [InferenceX GB300 vs MI355X V4](https://inferencex.semianalysis.com/compare/deepseek-v4-gb300-vs-mi355x)
- [SemiAnalysis V4 day 0 → 43](https://newsletter.semianalysis.com/p/deepseekv4-16t-day-0-to-day-43-performance)
- [SemiAnalysis tok/s/MW definition](https://x.com/SemiAnalysis_/status/2091208991271420076)
- [AI Weekly: Vera Rubin 59.4M tok/s/MW](https://aiweekly.co/alerts/semianalysis-benchmarks-vera-rubin-nvl72-at-7x-blackwells-tokens-per-mw-on)
- [Artificial Analysis: Vera Rubin AgentPerf](https://artificialanalysis.ai/articles/vera-rubin-nvl72-agentperf)
- [SimpleTechTrend: OCP 2026 InferenceX tokens/MW](https://www.simpletechtrend.com/en/post/semianalysis-ocp-2026-inferencex-agentx-tokens-per-mw-en)
- Carried from round 6:
  - [SemiAnalysis Rubin](https://newsletter.semianalysis.com/i/188150420/rubin)
  - [CUDO Vera Rubin](https://www.cudocompute.com/products/nvidia-vera-rubin)
  - [StorageReview MI455X](https://www.storagereview.com/news/amd-mi455x-and-helios-432gb-hbm4-72-gpu-racks-and-a-real-answer-to-vera-rubin)
  - [Google TPU 8](https://cloud.google.com/blog/products/compute/tpu-8t-and-tpu-8i-technical-deep-dive)
  - [StorageReview CS-4](https://www.storagereview.com/news/cerebras-cs-4-three-wse-3-turbo-wafers-750-pflops-and-a-claimed-30x-over-gpu-racks)
  - [arXiv DeepSeek-V4](https://arxiv.org/pdf/2606.19348)
  - [Silicon Analysts HBM4 price](https://siliconanalysts.com/market/trendforce-lifts-2027-hbm-asp-forecast-to-121-hbm4-stack-seen-doubling-to-1-300-2026-10-01)
  - [TrendForce SoIC](https://www.trendforce.com/news/?p=54678)
  - [TSMC CoWoS 130k](https://www.financialcontent.com/article/tokenring-2026-2-5-tsmc-to-quadruple-advanced-packaging-capacity-reaching-130000-cowos-wafers-monthly-by-late-2026)
  - [LaPedus N2 SRAM](https://marklapedus.substack.com/p/intel-tsmc-tout-sram-breakthroughs)