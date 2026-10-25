# Continuum-8: a weight-stationary 3D-SRAM decode accelerator for frontier MoE, built from two package types: KV-heavy layers get HBM packages, all other layers get SRAM-only packages

Every Continuum number below is model output. There is no silicon and no simulator run. Unless stated otherwise, a ratio is Continuum's output tok/s per provisioned watt divided by the best Rubin configuration at the same per-user speed floor. The workload is DeepSeek-V4-Pro at 128K context with draft acceptance p = 0.8.

## 0. Verdict

### 0.1 How each point of the check was handled

| Check point | Decision | Effect (≥200 / ≥500 / ≥1,000 / ≥1,500 / ≥2,000 tok/s/user) |
|---|---|---|
| **A.** The pipeline runs at its slowest stage | **Accepted.** The model now gives each layer type its own stage: 30 CSA layers, 31 HCA layers and 1 MTP layer, each with its own package count. It reproduces the critic's 46.8 (I get 46.9). | Continuum-7: 1.17/1.29/1.57/1.70/2.47 → 1.05/1.16/1.40/1.67/2.42 |
| **B.** Only Continuum was trimmed | **Accepted, with a computed bound.** Rubin's slot carries 3,056/1.146 − 2,300 = 367 W of non-GPU load at DC. One rule now applies to both systems: one CPU per 8 accelerators (50 W), a 30 W NIC, and each system keeps its own scale-up fabric. That removes about 100–130 W at DC from Rubin, or 115–150 W at the slot. I use 150 W, the top of that range. Trimming 250 W would mean cutting NVSwitch, which Rubin's modelled 1.8 TB/s expert-parallel traffic needs, so it appears only as a sensitivity row. | Every Rubin baseline below is trimmed by 150 W |
| **C.** Perfect four-way overlap | **Kept as base, bracketed.** The schedule is static, so the compiler can double-buffer KV prefetch and weight streaming. The two-phase bound (weight work and attention work run one after the other) is applied to both systems. Continuum-8 is less balanced than Continuum-7, so the penalty is smaller. | Two-phase: 1.06/1.18/1.42/1.88/2.31 |
| **D.** The calibration was mostly prefill | **Accepted.** The V4 0.19 figure is retired. New decode-only anchor: three measured GB200 decode-pool points give **0.29–0.34** of my model (`calib8.txt`). | Break-even, §0.3 |
| **E.** Prefill is left out | **Accepted, and a lever added.** If prefill stays on GPUs, the gain dilutes toward 1.0. If Continuum also does prefill, the site ratio has a floor of **1.23** (about 1.12 on the same node). | §4.6 |
| **F.** Per HBM stack compares 16-high with 12-high | **Accepted.** Figures are now given per GB as well. | Per GB at ≥200: 5.9× |
| **G.** Silicon area understated | **Accepted.** The N4 SRAM tiers are now counted. | All silicon: 3.2× Rubin per token at ≥200, 2.4× at ≥1,000 |
| **H.** The cost range paired like ends | **Accepted.** I now give the centre-to-centre ratio and the full crossed range. | §4.5 |
| Undersell: tile imbalance | **Adopted, with a capacity check.** Imbalance is set to 1.07 only when the stage has room for 12.5% hot-expert replicas, the DeepSeek EPLB ratio of 32 redundant per 256. | About +4% |
| Undersell: Ultra at 600 kW plus undervolt | **Rejected as a bound.** It implies 28.9 PF/kW, which is 1.55× same-node Rubin's best (18.6) and above Continuum's own N2 figure (22.9). The 600 kW at 100 PF case is kept at full clock. A reported 2-die Ultra is added. | §5 |

### 0.2 The design change that raises the honest number (`run8.txt`; Rubin trimmed by 150 W)

| Step | ≥200 | ≥500 | ≥1,000 | ≥1,500 | ≥2,000 |
|---|---|---|---|---|---|
| 1. Continuum-7, per-layer stages | 0.96 | 1.06 | 1.28 | 1.53 | 2.21 |
| 2. + hot-expert replicas (imbalance 1.07 where they fit) | 1.00 | 1.10 | 1.33 | 1.58 | 2.25 |
| 3. + HCA KV in the W-Tier SRAM; HCA packages ship **without HBM** | 1.06 | 1.17 | 1.42 | 1.67 | 2.41 |
| 4. + **CSA indexer keys in the W-Tier SRAM** (new lever) | 1.10 | 1.22 | 1.48 | 1.67 | 2.41 |
| 5. + 2, 3 or 4 HBM stacks per CSA package, chosen by capacity: **Continuum-8** | **1.13** | **1.25** | **1.51** | **1.71** | **2.51** |
| Continuum-8, same process node | 1.02 | 1.12 | 1.36 | 1.54 | 2.25 |
| Continuum-8 at 1M context | 1.17 | 1.17 | 1.40 | 1.97 | 3.80 |
| Continuum-8 against Rubin as shipped (no trim) | 1.23 | 1.36 | 1.65 | 1.87 | 2.75 |

**Why step 4 matters.** After fix A, the binding stage was the CSA layer. At 128K each user reads 2.1 MB of indexer keys there (32K compressed keys × 64 B) from HBM. That is 4.2× more than the 0.66 MB of attention KV the same layer reads. In the operating point, 43,896 users × 2.1 MB ÷ 7 packages = 13.2 GB per package. That fits in the 16.6 GB usable W-Tier next to 2.5 GB of weights, so the read moves off HBM. Once that read is gone, the CSA stage is compute-bound and needs only 3 HBM stacks for capacity.

### 0.3 Defensible claims

| Claim | Number | Holds only if |
|---|---|---|
| Decode-pod tok/s/W against Rubin, 128K | **1.13 / 1.51 / 2.51×** at ≥200 / ≥1,000 / ≥2,000 (same node: 1.02 / 1.36 / 2.25) | Continuum realises at least 89% / 66% / 40% of the fraction of its model that GPUs realise (below) |
| Worst single adverse assumption at ≥1,000 | 1.27 (W-Tier at 0.30 pJ/bit); worst tested pair 1.21 (same node with η = 0.5) | — |
| Bulk tier (≥200) | **A tie.** It falls to 0.95–1.02 under any one of: same node, η = 0.5, W-Tier at 0.30 pJ/bit, leakage ×2 | — |
| Site level, Continuum doing its own prefill | 1.39× at ≥1,000 with 1 fresh prompt token per output token; floor 1.23× (about 1.12× on the same node) | Prefill η and imbalance equal on both |
| Site level, prefill left on GPUs | 1.27× (r = 1) → 1.03× (r = 16) at ≥1,000 | — |
| Tokens per HBM GB against Rubin | 5.9× (≥200), 7.9× (≥1,000) | SRAM tiers and SoIC are less scarce than HBM |
| Against 4-die Rubin Ultra, built bottom-up and trimmed | 1.03 / 1.14 / 1.26×; at 1M 0.92 / 1.11 / 1.43× | Ultra ships as originally specified, which is now reported cancelled |
| Against the reported 2-die Ultra | 1.20 / 1.61 / 2.67× | The reports hold (unconfirmed by Nvidia) |

**Calibration and break-even.** GB200 decode-pool measurements for DeepSeek-R1 (all with 2K-token inputs) against my model:

| Measurement | Measured (tok/s per decode GPU) | Model | Measured ÷ model |
|---|---|---|---|
| LMSYS Part II, NVFP4 MoE | 13,386 | 39,069 | 0.34 |
| vLLM WideEP, 2K in / 2K out | 10.1k | 32,206 | 0.31 |
| LMSYS Part I, FP8 MoE | 7,583 | 25,997 | 0.29 |

So GPUs realise **0.29–0.34** of the model in decode. To keep its ratio, Continuum must realise at least 1/ratio of that fraction: ≥0.19–0.23 of its own model at ≥1,000 tok/s/user, and ≥0.26–0.30 at ≥200. This is unmeasured and remains the largest unknown.

**Bottom line.**
- Continuum-8 is a credible "best decode tokens per MW and per HBM GB above ~1,000 tok/s/user" design for frontier sparse MoE with compressed attention: **about 1.5× Rubin (1.36× on the same node)**.
- It is **not** shown to be the best in the world:
  - at bulk speeds it ties;
  - against a 4-die Ultra it gains only 1.03–1.26×;
  - Ultra at 600 kW and 100 PF beats it slightly at ≥200 (0.92×);
  - every Continuum number is model output.

---

## 1. Target workloads and metrics

**Workload: decode of DeepSeek-V4-Pro.**
- 1.6T total / 49B active parameters, 61 layers plus an MTP drafter.
- 384 experts, top-6, plus 1 shared expert; expert FFN size 3072.
- 30 CSA layers: an FP4 indexer scores L/4 compressed keys, then top-1024 attention plus a 128-token window.
- 31 HCA layers: 128× compressed attention.
- FP8 KV cache.
- Conditions: 128K and 1M context; p = 0.8 (code and tools) or 0.6 (prose).

**Out of scope:**
- training;
- edge;
- models under ~200B, where SRAM-only systems win;
- the 6.2T stress case, which was not re-run under the stage model (the round-7 Continuum-7 figures of 1.22 / 1.48 / 2.01× are superseded and unverified).

| Metric | Why it defines "best" |
|---|---|
| Output tok/s per provisioned MW at a per-user speed floor (200…2,000 tok/s/user) | Sites are power-limited, and the floor prevents gaming at low speeds. Each system picks its own draft depth k (0–7), microbatch count m (1–4), layout and voltage (0.55–0.75 V on one V/f law for all systems). |
| The same metric at site level, including prefill, with r fresh prompt tokens per output token | The check showed that the decode-pod metric alone overstates the gain. |
| Tok/s per HBM GB; total silicon per token | HBM is supply-limited; silicon is the price of avoiding HBM. |
| Max tok/s/user; cost per token | Speed tier for agents; cost is rough only. |

**Gate.** A gain counts only if it holds with:
- the same V/f law, slot-saving rule (1.146), latency model (τ = 7 + 3/f µs) and host-allowance rule for every system;
- Rubin in its best layout.

## 2. Reference points (vendor, press or analyst; conflicts noted)

| Design | Compute | Memory | Provisioned power per slot |
|---|---|---|---|
| Rubin VR200 NVL72 | 35 PF FP4 dense ("50" with adaptive compression); N3P | 288 GB HBM4 (8 × 12-high), 22 TB/s | Rack 190 kW (Max-Q) to 230 kW (Max-P); one originator ([Spheron](https://www.spheron.network/blog/nvidia-vera-rubin-nvl72-guide/)). I use 220 kW = 3.06 kW per slot. The 2.3 kW TDP is unconfirmed. **Trimmed by 150 W (§0.1 B).** |
| Rubin Ultra, 4-die (as announced) | 100 PF FP4 per package | ~1 TB HBM4E, ~32 TB/s | Nvidia: 600 kW per 144 packages ([DCD](https://www.datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027/)). Bottom-up from Rubin dies: 5.69 kW. |
| Rubin Ultra, 2-die (reported) | About half of the 4-die plan | 8 HBM4E stacks | SemiAnalysis via [Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidia-reportedly-cancels-quad-die-rubin-ultra-gpu-in-favor-of-dual-gpu-design-report-claims-complex-design-purportedly-scrapped-over-manufacturing-execution-concerns), [igorsLAB](https://www.igorslab.de/en/nvidia-rubin-ultra-four-die-design-dropped/) and [hwbusters](https://hwbusters.com/news/nvidia-reportedly-cancels-quad-die-rubin-ultra-gpu-over-packaging-issues/); not confirmed by Nvidia. Modelled as Rubin with 512 GB, +100 W. |
| MI455X | 40 PF MXFP4 | 432 GB, 19.6 TB/s | 3.2 kW (estimate) |
| TPU 8i / Ironwood | 10.1 PF FP4 / 4.6 PF FP8 | 288 GB at 8.6 TB/s / 192 GB at 7.37 TB/s | 1.3 / 1.2 kW (guesses) |
| Groq LP30 / LPX | 1.2 PF, FP8 only | 500 MB SRAM | ~625 W (unconfirmed) |
| Cerebras CS-4 | ~25 PF per wafer | 44 GB SRAM | ~43 kW per wafer (estimate) |

- **Decode-only GPU measurements:** [LMSYS Part II](https://lmsys.org/blog/2025-09-25-gb200-part-2) 13,386 output tok/s per GPU (GB200, R1, 2K-token inputs, NVFP4 MoE); [LMSYS Part I](https://www.lmsys.org/blog/2025-06-16-gb200-part-1) 7,583; [vLLM WideEP](https://vllm.ai/blog/2026-02-03-dsr1-gb200-part1) 10.1k.
- **Process:** I assume N2 compute energy is 0.8× N3P's. TSMC claims N2P is 36% lower power than N3E at the same speed ([TSMC](https://www.tsmc.com/english/dedicatedFoundry/technology/platform_HPC_tech_advancedTech)). Same-node cases are shown throughout.
- **Supply:** carried over. SoIC is ~10–15k wafers/month; CoWoS ~130k wafers/month by late 2026; HBM4 ~$600 per stack in 2026, forecast ~$1,300 in 2027.

## 3. Architecture

### 3.1 Blocks
One C-Die/W-Tier stack is used everywhere. There are two package SKUs.

**C-Die (compute)**
- 4 per package on N2, ~750 mm² each, 144 tiles each.
- Each tile: a ~111 TF FP4 tensor engine plus an FP32 vector/softmax unit.
- 64 PF FP4 / 32 PF FP8 dense at 0.75 V; **40.6 / 20.3 PF at the 0.55 V operating point** (f = 0.635 f0).
- Zero-skip assumed equal to Rubin's ×1.43 on both systems. With zero-skip off on both, the round-7 result was 1.48 at ≥1,000 against 1.57 with it.

**W-Tier (SRAM)**
- 8 N4 SRAM tiers hybrid-bonded under the C-Dies: 18.4 GB, 512 TB/s at f0 (325 TB/s at 0.55 V), 0.15 pJ/bit.
- In Continuum-8 it holds:
  - the layer's expert slice;
  - replicated attention and shared weights (0.43 GB);
  - hot-expert replicas;
  - **plus indexer keys (CSA packages) or the whole KV cache (HCA and MTP packages)**.

**Package SKUs**

| SKU | HBM | Role | Slot power at 0.55 V |
|---|---|---|---|
| **K-pkg** | 3 × HBM4 16-high (144 GB, 7.5 TB/s); 2 or 4 stacks optional | CSA layers | 2,450 W |
| **S-pkg** | None | HCA and MTP layers | 2,175 W |

**Link:** 64 × 224G lanes per direction, 1.8 TB/s (85% usable), 144 W.

**Host and NIC:** one CPU per 8 packages (50 W per slot), a 30 W 800G NIC, 30 W switch plane. Rubin gets the same CPU and NIC rule (§0.1 B).

**Slot power at 0.55 V** (chip × 1.146 + 110 W)

| Component | K-pkg | S-pkg |
|---|---|---|
| Compute | 902 W | 902 W |
| Leakage | 367 W | 367 W |
| W-Tier | 390 W | 390 W |
| HBM | 240 W | 0 |
| Links | 144 W | 144 W |
| **Slot** | **2,450 W** | **2,175 W** |

**Thermal and packaging:**
- ~0.4 W/mm² compute power density; ~580 A per C-Die.
- The K-pkg is ~5 reticles of CoWoS-L. The S-pkg, with no HBM sites, is ~3.5 reticles (my estimate).

### 3.2 Mapping (V4-Pro, 128K, the ≥200–≥1,000 operating point)
- **CSA stages:** 7 K-pkgs per layer × 30 layers = 210 packages; indexer keys in SRAM.
- **HCA stages:** 5 S-pkgs per layer × 31 layers = 155; **MTP:** 5 S-pkgs; **head:** 1.
- **Total:** **371 packages, 634 HBM stacks** (1.71 per package against Continuum-7's 4).
- **Within a layer group:** expert intermediate dimensions are split g ways; attention is data-parallel.
- **Schedule:** microbatches m = 2; T = max(m·c, c + τ).
- **The compiler** picks the per-type g, the stack count, where the KV and indexer keys live, V, k and m, all checked against capacity.

### 3.3 Numerics

| Data | Format |
|---|---|
| Expert weights | NVFP4, zero-compressed |
| Attention, shared expert, drafter | FP8 |
| Indexer | FP4 |
| KV cache | FP8 (NVFP4 optional, applied to all systems in §5) |
| Accumulation, softmax | FP32 |
| Link partial sums | BF16 |

V4-Pro is already served in FP4 on GB300, so the weight format adds no new accuracy risk. KV in SRAM is bit-identical to KV in HBM.

## 4. Sanity arithmetic

### 4.1 Hand check at ≥1,000 (128K)
Setting: 0.55 V, k = 1, b = 354, m = 2, so 708 positions per microbatch.

**Compute per position**

| Part | Work | Rate | Time per position |
|---|---|---|---|
| Linear | 1.655 GFLOP | 40.65 PF × 1.43 | 2.85e-8 s |
| Attention (1,152 entries × 262k FLOP = 302 MFLOP) | FP8 | 20.3 PF | 1.49e-8 s |
| CSA indexer (32,768 × 16,384 = 537 MFLOP) | FP4 | 40.65 PF | 1.32e-8 s |

**Stage times**

| Stage | Compute | Other resources | Result |
|---|---|---|---|
| HCA | (2.85 + 1.49)e-8 × 708 × 1.07 ÷ 0.6 ÷ 5 = **10.96 µs** | SRAM: 2.85 + 0.43 GB weights + 47 MB KV = 3.33 GB ÷ 325 TB/s = 10.2 µs | Binding stage |
| CSA | (2.85 + 1.49 + 1.32)e-8 × 708 × 1.07 ÷ 0.6 ÷ 7 = **10.2 µs** | HBM: 50.6 users × 0.66 MB ÷ 7.5 TB/s = 4.5 µs; SRAM: 2.57 GB ÷ 325 TB/s = 7.9 µs | Not binding |
| Link | 708 × 20.1 kB ÷ 1.53 TB/s = 9.3 µs | — | Not binding |

**Throughput**
- τ = 7 + 3/0.635 = 11.7 µs, so T = max(21.9, 22.7) = **22.7 µs**.
- Speed: 1.8 ÷ (62 × 22.7 µs) = **1,279 tok/s/user** ✓.
- Users: 2 × 354 × 62 = 43,896.
- Efficiency: 0.85 × 708 × 1.8 ÷ 22.7 µs ÷ (371 × 2,332 W) = **55.2 tok/s/W** ✓.

**Capacity check (90% usable SRAM)**
- CSA SRAM: 2.47 GB weights + 13.15 GB indexer keys = 15.6 of 16.6 GB, leaving 0.94 GB free against 0.26 GB needed for replicas ✓.
- CSA HBM: 43,896 × 18.95 MB ÷ 7 = 118.8 of 129.6 GB ✓.
- HCA SRAM: 9.1 of 16.6 GB ✓.

**Rubin at the same tier:** 36.6 tok/s/W after trimming (0.55 V, k = 4). Ratio **1.51**. Rubin pays for deep speculation and for HBM-bound weight and KV reads.

### 4.2 Operating points (`run8.txt`)

| Tier | Continuum-8 | tok/s/W | Rubin (trimmed) |
|---|---|---|---|
| ≥200 – ≥1,000 | Above, 1,281 tok/s/user | 55.2 | 49.0 / 44.2 / 36.6 |
| ≥1,500 | k = 2, b = 203, 279 packages, 454 stacks | 52.4 | 30.7 |
| ≥2,000 | k = 3, b = 176, CSA on 2 stacks, 341 packages | 48.2 | 19.2 |
| 1M, all tiers | k = 4, m = 3, b = 50, 651 packages, 2,985 tok/s/user | 15.7 | 13.3 / 13.3 / 11.2 / 7.9 / 4.1 |

### 4.3 Sensitivity (`sens8.txt`; against Rubin trimmed by 150 W; ≥200 / ≥500 / ≥1,000 / ≥1,500 / ≥2,000)

| Change | 128K | 1M |
|---|---|---|
| Base | 1.13 / 1.25 / 1.51 / 1.71 / 2.51 | 1.17 / 1.17 / 1.40 / 1.97 / 3.80 |
| Same node | 1.02 / 1.12 / 1.36 / 1.54 / 2.25 | 1.06 / … / 1.26 / 1.78 / 3.42 |
| η = 0.5 (Continuum only) | 1.01 / 1.11 / 1.35 / 1.48 / 2.13 | 1.07 / … / 1.27 |
| W-Tier at 0.30 pJ/bit | **0.95** / 1.05 / 1.27 / 1.43 / 2.10 | 0.98 / … / 1.17 |
| Leakage ×2 | 0.96 / 1.06 / 1.28 / 1.44 / 2.12 | 0.99 / … / 1.19 |
| No replicas (imbalance 1.12) | 1.11 / 1.23 / 1.49 / 1.66 / 2.43 | 1.13 / … / 1.35 |
| Imbalance 1.25 | 1.03 / 1.14 / 1.38 / 1.52 / 2.18 | 1.08 / … / 1.29 |
| Collectives 12 µs | 1.06 / 1.17 / 1.42 / 1.56 / 2.24 | 1.05 / … / 1.25 |
| Usable SRAM 80% | 1.07 / 1.18 / 1.43 / 1.71 / 2.51 | 1.14 / … / 1.36 |
| Vmin floor 0.60 V for both | 1.04 / 1.15 / 1.39 / 1.71 / 2.42 | 1.14 / … / 1.43 |
| Two-phase, both systems | 1.06 / 1.18 / 1.42 / 1.88 / 2.31 | 1.15 / 1.22 / 1.65 / 2.26 / 3.96 |
| Pair: same node + η = 0.5 | 0.91 / 1.00 / **1.21** / 1.33 / 1.93 | 0.96 / … / 1.15 |
| Pair: two-phase + no replicas | 1.05 / 1.16 / 1.40 / 1.85 / 2.19 | 1.13 / … / 1.63 |
| Rubin trimmed 250 W | 1.06 / 1.17 / 1.41 / 1.60 / 2.35 | 1.10 / … / 1.31 |

- **At ≥200:** a tie under any one adverse assumption.
- **At ≥1,000:** every single and paired case tested stays at 1.21 or above.

### 4.4 Supply per unit of output (`supply8.txt`, 128K)

| | ≥200 | ≥1,000 | ≥2,000 |
|---|---|---|---|
| Tokens per HBM stack against Rubin | 7.9× | 10.6× | 27× |
| Tokens per HBM GB against Rubin | **5.9×** | **7.9×** | 20× |
| Leading-edge logic (N2 against N3P) per token | 1.08× | 0.81× | 0.50× |
| **All silicon (N2 + N4 tiers) per token** | **3.2×** | **2.4×** | 1.5× |

- **Per GW of Continuum at ≥200:** 429k packages, 733k HBM stacks (Rubin: 5.1M per GW), 3.4M N4 tier dies.
- **SoIC:** ~75k wafer passes per GW, i.e. 5–7.5 months of 2026 SoIC capacity. **SoIC is the binding supply line.**
- **The trade:** Continuum-8 buys HBM independence with N4 SRAM and bonding capacity.

### 4.5 Cost (BOM assumptions; excludes rack, host and vendor margin)

| | Package BOM | tok/s per package at ≥200 |
|---|---|---|
| Continuum-8 | $9.1–11.4k (4 N2 dies $2.6–3.1k; 8 N4 tiers $2.5k; 1.71 stacks × $0.9–1.95k; packaging and test $2.5k) | 128.8k |
| Rubin | $7.6–13k | 76.5k |

| Tier | Tokens per BOM dollar, centre to centre | Crossed range |
|---|---|---|
| ≥200 | 1.69× | 1.12–2.40× |
| ≥1,000 | 2.26× | 1.50–3.21× |

Rough.

### 4.6 Site level, including prefill (`site8.txt`)
Prefill is compute-bound on both systems. Energy per prompt token at 128K: Rubin 15.8 mJ, Continuum-8 12.9 mJ, a ratio of 1.23. That is roughly 1.12 on the same node: an approximation that applies the ×1.25 to the compute share only.

| r (fresh prompt tokens per output token) | Prefill on Rubin, decode on Continuum: ≥200 / ≥1,000 / ≥2,000 | All Continuum: ≥200 / ≥1,000 / ≥2,000 |
|---|---|---|
| 0.25 (reasoning chat) | 1.11 / 1.42 / 2.27 | 1.14 / 1.47 / 2.34 |
| 1 | 1.07 / 1.27 / 1.86 | 1.17 / 1.39 / 2.02 |
| 4 (agent turns with fresh tool output) | 1.03 / 1.11 / 1.37 | 1.20 / 1.30 / 1.59 |
| 64 (full 128K prompt per 2K output) | 1.00 / 1.01 / 1.03 | 1.22 / 1.23 / 1.26 |

- **Prefill on Continuum:** chunked into the same pipeline, so the KV lands where decode needs it with no network transfer.
- **Cost of that:** the pod must be sized for both workloads.
- **The decode-pod gain is real only for buyers whose site is decode-dominated** (r ≲ 1: reasoning, long outputs, high prefix-cache reuse).

## 5. All-system comparison (`sens8.txt`, `ultra8.txt`; Continuum-8 ÷ X)

**Tiers ≥200 / ≥500 / ≥1,000 / ≥1,500 / ≥2,000**

| Against | 128K | 1M |
|---|---|---|
| Rubin, trimmed | 1.13 / 1.25 / 1.51 / 1.71 / 2.51 | 1.17 / 1.17 / 1.40 / 1.97 / 3.80 |
| Ultra 4-die, bottom-up, trimmed | 1.03 / 1.03 / 1.14 / 1.19 / 1.26 | 0.92 / 0.92 / 1.11 / 1.26 / 1.43 |
| Ultra 4-die, 600 kW, 100 PF, trimmed | **0.92** / 1.02 / 1.12 / 1.17 / 1.22 | 0.95 / 0.95 / 1.11 / 1.38 / 1.84 |
| Ultra 2-die (reported) | 1.20 / 1.33 / 1.61 / 1.81 / 2.67 | 1.07 / 1.18 / 1.49 / 2.08 / 4.05 |
| MI455X | 2.02 / 2.24 / 2.53 / 3.08 / 4.42 | 1.58 / 1.74 / 2.21 / 3.23 / 6.66 |
| TPU 8i | 2.23 / 2.69 / 3.55 / 4.59 / 12.7 | 1.72 / 2.19 / 3.05 / 6.3 / 25 |
| Rubin + LPX (FP8 weights) | 8.2 / 8.2 / 8.5 / 10.5 / 12.5 | 13.8–22 |
| CS-4 | 25–28 | 24 |

**Variants and limits**
- **NVFP4 KV on every system:** 128K 1.15 / 1.28 / 1.45 / 1.60 / 2.21; 1M 1.05 / 1.13 / 1.39 / 1.97 / 3.42 (`fp4kv8_*.txt`).
- **p = 0.6:** 1.11 / 1.38 / 2.60 / 9.1 / 98. Ratios above about 3× mean Rubin is at its speed ceiling, not that Continuum is more efficient, so I don't claim them.
- **Max tok/s/user (modelled):** CS-4 5,737; Continuum-8 5,642; Ultra 5,557; Rubin 4,949.

**Ultra at 600 kW plus undervolt: rejected.** At 600 kW and 100 PF, Ultra already reaches 24.0 PF/kW. That is 1.47× Rubin Max-P on the same N3P node. Adding the undervolt law on top gives 28.9 PF/kW: 1.55× same-node Rubin's best, and above Continuum's own N2 figure (22.9). I treat that as double-counting, not a bound.

## 6. Software stack and programming model
**Front end:** PyTorch (`torch.export`) and JAX (StableHLO) → MLIR compiler → static spatial schedule. The schedule now places each layer type on a package type and sets:
- g;
- stack count;
- KV and indexer-key placement;
- hot-expert replicas from a routing profile;
- m, k and V per deployment.

All of this is capacity-checked offline; recompiling takes hours.

**Kernels:** a tile DSL (block-matmul, softmax, gather) for CSA, HCA, the FP4 indexer and MLA. No warp/thread model.

**Serving:** a vLLM/SGLang backend with:
- continuous batching at stage boundaries;
- paged KV split across HBM (K-pkgs) and SRAM (S-pkgs);
- a built-in drafter;
- chunked prefill in the pipeline, or GPU prefill with KV shipped over the NIC.

**Existing models:** they convert by NVFP4 post-training quantization; V4-Pro and gpt-oss need no new quantization. **The K:S package ratio is model-specific** (V4: 210:161). A K-pkg can serve any layer; an S-pkg can serve only layers whose KV fits in SRAM. Dense-attention models need mostly K-pkgs and lose the step 3–5 gains.

**Training and dynamic control flow** stay on GPUs.

**Maturity risk:** GPU V4 software improved 2.1–2.6× in about two months. Continuum starts from zero.

## 7. Where Continuum loses or ties
1. **Bulk tier:** 1.13× falls to 1.02× on the same node and 0.95× with W-Tier at 0.30 pJ/bit. It is a tie.
2. **Rubin Ultra 4-die at 600 kW and full 100 PF:** loses by 8% at ≥200 and wins 1.12× at ≥1,000.
3. **1M context against the 4-die Ultra at bulk:** 0.92×. Ultra's 32 TB/s of HBM wins on long-context KV.
4. **Site level with GPU prefill and large r:** the gain disappears (1.01× at r = 64).
5. **Silicon:** 2.4–3.2× Rubin's total silicon per token; ~75k SoIC passes per GW.
6. **Deployment unit and model lock-in:** 279–651 packages per instance, with a model-specific package mix.
7. **Training:** not supported.
8. **Calendar:** 2028 at the earliest, against Nvidia's Feynman generation.

## 8. What has to be true

| Assumption (base) | If wrong | Ratio at ≥1,000 tok/s/user |
|---|---|---|
| Continuum realises ≥66% of the GPU decode fraction (0.29–0.34) | Lower | Scales directly |
| η = 0.6 on narrow expert slices | 0.5 | 1.35 |
| 0.55 V operation on N2 | 0.60 V floor | 1.39 |
| W-Tier at 0.15 pJ/bit | 0.30 pJ/bit | 1.27 |
| N2 compute energy is 0.8× N3P's | Same node | 1.36 |
| 90% of SRAM usable (CSA packages are 94% full) | 80% | 1.43 |
| Rubin's symmetric trim is ≤150 W | 250 W | 1.41 |
| The frontier stays sparse MoE with compressed attention, with indexer keys ≤ ~2 MB per user per layer at 128K | Dense attention or a bigger indexer | KV-bound; steps 3–5 are lost (about 1.3×) |
| p ≈ 0.8 | p ≥ 0.9 | Rubin's speculation waste falls; the gain shrinks |

## 9. Risks and physical, process and supply limits
- **SoIC:** 5–7.5 months of 2026 capacity per GW; new capacity costs ~$7B per 10k wafers/month.
- **CoWoS-L:** ~5 reticles for the K-pkg (the same class as Ultra), ~3.5 for the S-pkg.
- **HBM:** 0.73M 16-high stacks per GW. Volume for 16-high is unconfirmed; with 12-high stacks the CSA packages need g = 8 or 4 stacks (not modelled).
- **SRAM capacity margin:** CSA packages run at 94% of usable SRAM. The indexer-key footprint grows with context × users, so admission control is mandatory.
- **Low-voltage operation:** adaptive clocking at 0.55 V; SRAM on its own ≥0.65 V rail.
- **Yield:** a 750 mm² N2 die is ~47% raw and ~65% with harvesting; bond interfaces are 98–99% each, so known-good-die testing is mandatory.
- **Pipeline fragility:** spares at ~3% (not included in the ratios).

## 10. Tests that could prove the design wrong

| # | Test | Tool | Kill criterion |
|---|---|---|---|
| 1 | **Decode realisation:** V4 traces through an event-level simulator, against GPU decode-pool runs | LLMCompass-class simulator, plus a measured V4 decode-only GPU point | Continuum below 66% of the GPU decode fraction at ≥1,000 |
| 2 | Tile η at M = 4–40, N = 32–64, NVFP4 with zero-skip | Timeloop/Accelergy + one-tile RTL | η < 0.5 |
| 3 | N2 V/f and energy at 0.55 V | Foundry PDK SPICE | f < 0.55 f0 or energy > 0.6× nominal |
| 4 | W-Tier energy and bandwidth with KV and indexer traffic mixed in | CACTI/DESTINY + bank-conflict simulation | > 0.25 pJ/bit or < 300 TB/s effective |
| 5 | CSA SRAM fit under real routing and context-length distributions | Trace replay | Usable fraction < 80% at target users |
| 6 | Collectives across 7 packages | SerDes/switch simulation | > 12 µs |
| 7 | Rubin's best decode efficiency at ≥1,000 | Measurement | > 41 tok/s/W voids 1.51× → < 1.35× |
| 8 | Rubin Ultra configuration and rack power | Vendor data | 4-die at ≤ 4.2 kW per slot and 100 PF → the bulk-tier loss stands |
| 9 | Thermal and IR drop | HotSpot/3D-ICE, PDN solver | Tj > 105 °C or IR drop > 5% |

None of these could be run here. Tests 1, 3 and 5 matter most.

## 11. Facts vs assumptions
**Facts (sourced, many secondary):**
- chip specifications in §2 and the conflicting rack figures;
- the reported cancellation of the 4-die Ultra (unconfirmed);
- GB200 decode-pool measurements;
- LP30 has no FP4;
- TSMC's N2P claim;
- the V4 configuration;
- packaging capacity.

**Derived by me:**
- Rubin's 367 W of non-GPU load per slot and the 115–150 W symmetric trim;
- bottom-up Ultra power;
- the 0.29–0.34 decode realisation;
- the per-layer KV, indexer and capacity figures;
- supply per GW.

**My assumptions:**
- the V/f law (V0 0.75 V, Vt 0.30 V, α 1.3), τ(f), the 1.146 slot rule and the host rule;
- every pJ figure, and the 80 W per HBM stack;
- leakage;
- η = 0.6, the 0.85 derate, imbalance 1.07/1.12 and the 12.5% replica space;
- the component split of Vera, CX-9 and NVSwitch power;
- costs, yields, and the S-pkg interposer size.

**Model outputs:** every throughput, ratio and energy figure for every system.

**Files** (in `/home/user/SomeRepository/engine/runs/refine_continuum_d/round1/`; not committed; imports `round7/model7.py` and `round6/model5.py` unchanged):

| File | Contents |
|---|---|
| `model8.py` | Per-layer-type stage model; K/S packages; SRAM-resident KV and indexer keys; replica rule; two-phase option; Rubin trim; Ultra variants |
| `t0.py` | Reproduces the critic's 46.8 (46.9) |
| `run8.py` → `run8.txt` | Lever ladder and operating points |
| `sens8.py` → `sens8.txt` | Sensitivities and all-system tables. The run hit the 10-minute background limit after the p = 0.6 rows, so the NVFP4 rows are in `fp4kv8.py` → `fp4kv8_128k.txt`, `fp4kv8_1m.txt` |
| `calib8.py` → `calib8.txt` | Decode-only calibration |
| `site8.py` → `site8.txt` | Site-level ratios with prefill |
| `supply8.py` → `supply8.txt` | HBM per GB, silicon, SoIC, BOM |
| `ultra8.py` → `ultra8.txt` | Ultra 600 kW bounds and implied PF/kW |
| `run7_shim.py` | Imports the round-7 Ultra and other-system profiles |

---

**Sources** (new this round first; round-7 sources still apply)
- [LMSYS: GB200 NVL72 Part II, 13,386 decode tok/s per GPU](https://lmsys.org/blog/2025-09-25-gb200-part-2)
- [LMSYS: GB200 NVL72 Part I, 7,583 decode tok/s per GPU](https://www.lmsys.org/blog/2025-06-16-gb200-part-1)
- [vLLM: WideEP on GB200, 10.1k decode TPGS](https://vllm.ai/blog/2026-02-03-dsr1-gb200-part1)
- [Tom's Hardware: Rubin Ultra reportedly moves to 2 dies](https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidia-reportedly-cancels-quad-die-rubin-ultra-gpu-in-favor-of-dual-gpu-design-report-claims-complex-design-purportedly-scrapped-over-manufacturing-execution-concerns)
- [igorsLAB: four-die Rubin Ultra dropped](https://www.igorslab.de/en/nvidia-rubin-ultra-four-die-design-dropped/)
- [hwbusters: quad-die Rubin Ultra cancelled](https://hwbusters.com/news/nvidia-reportedly-cancels-quad-die-rubin-ultra-gpu-over-packaging-issues/)
- [Spheron: Vera Rubin NVL72 power figures and their single origin](https://www.spheron.network/blog/nvidia-vera-rubin-nvl72-guide/)
- [HashrateIndex: Vera Rubin NVL72 specs](https://hashrateindex.com/blog/nvidia-vera-rubin-nvl72-specs-breakdown/)
- [Ingrasys: Vera Rubin NVL72 tray layout](https://www.ingrasys.com/solutions/NVIDIA/nvidia_verarubin_nvl72_/)
- [SemiAnalysis: Vera Rubin co-design](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution)
- [InferenceX: GB200 NVL72 vs B200 disaggregated](https://inferencex.semianalysis.com/blog/gb200-nvl72-vs-b200-disagg-deepseek-r1-fp4-dynamo-trt)
- [LMSYS: GB300 long-context](https://www.lmsys.org/blog/2026-02-19-gb300-longctx/)
- [DCD: Rubin Ultra NVL576 at 600 kW](https://www.datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027/)
- [PyTorch/SGLang: V4 on GB300](https://pytorch.org/blog/serving-deepseek-v4-on-gb300-with-sglang-5x-higher-throughput-at-the-same-interactivity-since-day-0/)
- [TSMC N2/N3 HPC technology](https://www.tsmc.com/english/dedicatedFoundry/technology/platform_HPC_tech_advancedTech)
- [SemiAnalysis: Inference Kingdom (LP30)](https://newsletter.semianalysis.com/p/nvidia-the-inference-kingdom-expands)
- [More Than Moore: LP30/LPX](https://morethanmoore.substack.com/p/nvidia-introduces-groq-lp30-and-lpx)
- Carried from earlier rounds:
  - [CUDO Vera Rubin](https://www.cudocompute.com/products/nvidia-vera-rubin)
  - [StorageReview MI455X](https://www.storagereview.com/news/amd-mi455x-and-helios-432gb-hbm4-72-gpu-racks-and-a-real-answer-to-vera-rubin)
  - [Google TPU 8](https://cloud.google.com/blog/products/compute/tpu-8t-and-tpu-8i-technical-deep-dive)
  - [StorageReview CS-4](https://www.storagereview.com/news/cerebras-cs-4-three-wse-3-turbo-wafers-750-pflops-and-a-claimed-30x-over-gpu-racks)
  - [arXiv DeepSeek-V4](https://arxiv.org/pdf/2606.19348)
  - [Silicon Analysts HBM4 price](https://siliconanalysts.com/market/trendforce-lifts-2027-hbm-asp-forecast-to-121-hbm4-stack-seen-doubling-to-1-300-2026-10-01)
  - [TrendForce SoIC](https://www.trendforce.com/news/?p=54678)
  - [TSMC CoWoS 130k](https://www.financialcontent.com/article/tokenring-2026-2-5-tsmc-to-quadruple-advanced-packaging-capacity-reaching-130000-cowos-wafers-monthly-by-late-2026)