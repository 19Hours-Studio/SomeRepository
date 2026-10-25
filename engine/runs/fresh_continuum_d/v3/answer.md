# Continuum-10: a weight-stationary 3D-SRAM decode accelerator for frontier MoE, with layer-pair expert-parallel groups

Every Continuum number below comes from my model. There is no silicon and no simulator run. Unless stated otherwise, a ratio means Continuum's output tok/s per provisioned watt divided by that of the best Rubin configuration at the same per-user speed floor. Rubin is trimmed by 150 W under the shared host rule. The workload is decode of DeepSeek-V4-Pro at 128K context, with draft acceptance p = 0.8. Tiers are ≥200 / ≥500 / ≥1,000 / ≥1,500 / ≥2,000 tok/s/user. Scripts and outputs are in `/home/user/SomeRepository/engine/runs/refine_continuum_d/round3/`.

## 0. Verdict

### 0.1 How each point of the check was handled

| Check point | Decision | Number |
|---|---|---|
| **The mHC residual hand-off is missing** (hc_mult = 4: 4 streams × hid in BF16 = 8 × hid per position, against the 1 × hid charged) | **Accepted. I reproduce the result:** 1.46 at 64 lanes and 1.59 at 88 lanes (`t10.txt`). mHC is in V4-Pro ([SemiAnalysis](https://inferencex.semianalysis.com/model/deepseek-v4)), and the residual cannot be shrunk before it crosses a package. All numbers now use HO = 8. An FP32 residual (HO = 16) is a sensitivity case. | Before the design change in §0.2: 1.19 / 1.31 / **1.59** / 1.76 / 2.59 |
| **The calibration condition was misstated** | **Accepted.** The ratio scales with ρ_C/ρ_G, where ρ is the fraction of the model's ideal decode rate that a system actually reaches. Continuum breaks even with Rubin at ρ_C/ρ_G = 1/1.64 = 0.61. The headline needs ρ_C = ρ_G, which is 0.29–0.34 for GPUs (`calib8.txt`). | Ratio = 1.64 × ρ_C/ρ_G |
| **The Feynman risk was understated** | **Accepted, and now quantified.** GTC 2026 reports describe stacked GPU dies, custom HBM, A16 and an LP40 LPU ([heise](https://heise.de/-11214678), [Jon Peddie](https://www.jonpeddie.com/news/nvidia-gtc-2026-keynote/), [Wccftech](https://wccftech.com/nvidia-feynman-gpu-gets-3d-die-stacking-custom-hbm-next-gen-rosa-cpu/amp/)). My proxy is the Ultra architecture with compute energy × 0.66 (N3P → A16), with and without +50% HBM bandwidth (`feyn10.txt`). | At ≥1,000: 1.04 (N2 Continuum against the proxy). On the same node (A16 both): 1.13, or **1.02 if the proxy also gets +50% HBM bandwidth**. That is a tie. |
| **Host power: 120 W listed, 110 W modelled** | **Fixed.** The KV-mirror DRAM is dropped, so the host is 110 W per slot everywhere. | — |
| **Failure cost overstated 1,000×** | **Accepted.** For Continuum-10 (497 packages, G = 16), one failure loses KV for 4,336 users. Re-prefilling 4,336 × 128K tokens × 12.7 mJ = 7.2 MJ, which is **6.3 s of pod time**. At 85 failures a year that is 0.0017% of capacity. Cold spares cost 0.00–0.01. | Mirror removed: +0.4% |
| **Memory margins double-counted** | **Accepted.** "Full" means full against a 90% fill cap. The "cap at 90% → −3%" row is deleted. | — |
| **Link bytes are 1.21 × hid, not 1.15** | Accepted. The imbalance had been left out of the formula but not out of the time. | — |
| **Collective latency 7 → 4 µs** (the check's lever) | **Tested symmetrically.** The check applied it to Continuum only. Rubin's per-layer collectives are the same kind of cost, so the gate requires applying it to both. | Both systems: 1.64 → 1.67 at ≥1,000, and 2.90 → **2.52** at ≥2,000 (Rubin gains more there). Continuum only: 1.67 / 2.94. **Not adopted as base.** |

### 0.2 The change that raises the honest number: layer-pair groups (`model10.py`, `sweep10.txt`, `hand10.txt`)

**What bound the corrected Continuum-9.**
- Every layer was its own pipeline stage on its own packages, so the 8 × hid mHC residual crossed a link at all 61 layer boundaries.
- The CSA and HCA stages were sized separately:
  - CSA stages were sized by HBM capacity;
  - HCA stages had no HBM at all.
  
  So capacity-driven packages were idle for part of the cycle. At 1M context this was the dominant waste.

**What Continuum-10 does.**
- Each CSA layer and the following HCA layer share one group of G packages.
- Each package owns 384/G whole experts of **both** layers.
- Attention is **user-stationary**: user u's attention for both layers runs on the same package. The residual therefore stays on-package inside the pair, and the hand-off happens once per pair.
- Every pair package carries 1–4 HBM stacks. The compiler picks the count; the HBM holds the CSA KV, and the HCA KV goes to HBM or SRAM.
- The extra HCA layer and the MTP drafter stay single-layer stages on no-HBM packages.
- Silicon is unchanged except for **72 link lanes** instead of 64 (+18 W). This is a mapping and SKU-mix change.

**Pipeline accounting (corrected inside this round).**
- There are 32 stages: 30 pairs, 1 HCA stage and MTP.
- Cycle: Tp = max(m·c_pair, c_pair + 2τ), where c_pair = c_CSA + c_HCA run back to back. Each pair stage still pays two per-layer collective latencies.
- Users in flight = m·b·32.

My first version of the script counted 61 stages' worth of users on 32 stages. That bug produced a spurious 2.8×. The fixed version is the one reported here.

**Costs the change takes on.**
- Spreading a layer's experts over more packages raises the number of distinct packages a token's 6 experts hit: D(16) = 5.14, against D(13) = 4.96.
- There are 30 more HBM-bearing packages' worth of HBM power.
- Both are charged.

| Step | ≥200 | ≥500 | ≥1,000 | ≥1,500 | ≥2,000 |
|---|---|---|---|---|---|
| Continuum-9 as answered (HO = 1) | 1.22 | 1.35 | 1.63 | 1.81 | 2.67 |
| Continuum-9 corrected, HO = 8, 88 lanes (the check) | 1.19 | 1.31 | 1.59 | 1.76 | 2.59 |
| Pair groups, HO = 8, 64 lanes | 1.23 | 1.37 | 1.65 | 1.80 | 2.69 |
| **Pair groups, 72 lanes: Continuum-10** | **1.27** | **1.40** | **1.64** | **1.92** | **2.90** |
| Same with ω = 0.6 (a per-deployment W-Tier clock) | 1.27 | 1.40 | 1.67 | 1.89 | 2.84 |

**At 1M context the pair layout gives the largest honest gain** (ω = 0.7, `all10.txt`):

| | ≥200 | ≥1,000 | ≥2,000 |
|---|---|---|---|
| Against Rubin, corrected Continuum-9 | 1.05 | 1.25 | 3.40 |
| **Against Rubin, Continuum-10** | **1.39** | **1.66** | 4.49 |
| Against 4-die Ultra, corrected Continuum-9 | 0.84 | 1.01 | 1.31 |
| **Against 4-die Ultra, Continuum-10** | **1.08** | **1.31** | 1.69 |

The reason: the CSA-KV capacity forces about 27 packages per pair. Those packages now also do HCA work instead of a separate set of HCA packages doing it.

**Levers that failed:**
- 56 lanes: 1.57.
- 80 or 88 lanes: 1.62–1.63.
- ω = 1: 1.58.
- g/G ≤ 10/20: 1.64. This is the same efficiency at a smaller instance.

### 0.3 Defensible claims

| Claim | Number | Holds only if |
|---|---|---|
| Decode tok/s/W against Rubin, 128K | **1.64× at ≥1,000** (1.27× at ≥200, 2.90× at ≥2,000); same node 1.48× | ρ_C = ρ_G (break-even at 0.61 ρ_G) |
| Worst single adverse assumption, ≥1,000 | 1.39 (η = 0.5, or leakage ×2) | — |
| Worst of 90 pairs, ≥1,000 | **1.17** (η = 0.5 + leakage ×2); median pair 1.43 | — |
| Against 4-die bottom-up Ultra (same date), 128K | **1.24× at ≥1,000**; 1.16 at ≥200; 1.45 at ≥2,000. **Worst pair 0.88 at ≥1,000** (median pair 1.08) | The 4-die Ultra ships (reports say it is cancelled) |
| Against a Feynman proxy (2028) | ~1.0–1.15 when both are on the same node | Proxy assumptions in §5 |
| 1M context | 1.39 / 1.66 / 4.49 against Rubin; **1.08 / 1.31 / 1.69 against Ultra** | — |
| Bulk tier (≥200), 128K | **Not a win.** 1.27 base; 1.08–1.23 under one adverse assumption; **0.95 under the worst pair** (0.86 against Ultra) | — |
| Site level, Continuum also doing prefill, r = 1 | 1.47× at ≥1,000; floor about 1.24 (about 1.13 on the same node) | Equal prefill η on both systems |
| Tokens per HBM GB | 3.1× (≥200), 7.5× (≥1,000), 25× (≥2,000) | SoIC and N4 SRAM are less scarce than HBM |

**Bottom line.**
- Continuum-10 is a credible design for **the best decode tokens per MW and per HBM GB at 1,000–2,000 tok/s/user** on frontier sparse MoE with compressed attention. At 128K it is about 1.6× Rubin and 1.2× a same-date 4-die Ultra; at 1M it is 1.66× Rubin and 1.31× Ultra.
- Against Rubin it stays ≥ 1.17× under every adverse pair tested.
- It is **not** shown to be the best in the world overall:
  - against Ultra, the worst pairs lose (0.88);
  - at bulk speeds it is within noise of Rubin;
  - a 2028 Feynman on the same node is a tie in my proxy;
  - it does not train;
  - every Continuum number is model output.

---

## 1. Target workloads and metrics

**Workload: decode of DeepSeek-V4-Pro.**
- 1.6T total / 49B active parameters.
- 61 layers plus an MTP drafter.
- 384 experts, top-6, plus a shared expert; expert FFN size 3072; hid = 7,168.
- 30 CSA layers: an FP4 indexer over L/4 compressed keys, then top-1024 attention plus a 128-token window.
- 31 HCA layers: 128× compressed attention.
- mHC residual with 4 streams.
- FP8 KV cache.
- Conditions: 128K and 1M context; p = 0.8 (code and tools) or 0.6 (prose).

**Layer order (assumption).** The pair layout assumes CSA and HCA layers alternate. That alternation is reported for V4-Flash ([AMD ROCm](https://rocm.blogs.amd.com/software-tools-optimization/primus-deepseek-v4/README.html)); for Pro it is my assumption. If Pro groups same-type layers together, pairs become CSA+CSA or HCA+HCA, which I have not modelled.

**Out of scope:** training, edge, models under ~200B (where SRAM-only systems win), and the 6.2T stress case.

| Metric | Why it defines "best" |
|---|---|
| Output tok/s per provisioned MW at a per-user floor | Sites are power-limited, and the floor stops gaming at low speeds. Every system picks its own draft depth k (0–6), microbatch count m (1–4), layout and voltage (0.55–0.75 V on one V/f law). Continuum also picks the W-Tier clock ω. |
| The same at site level, with r fresh prompt tokens per output token | The decode-pod metric alone overstates the gain. |
| Tok/s per HBM GB; silicon per token | HBM is supply-limited; silicon is what Continuum spends instead. |
| Max tok/s/user; cost per token | Speed tier; cost is rough only. |

**Gate.** A gain counts only if it holds with:
- the same V/f law, slot rule (1.146 × chip + host), τ = 7 + 3/f µs and host rule for every system;
- Rubin in its best layout;
- all 90 adverse pairs reported;
- any latency improvement applied to both systems.

## 2. Reference points (vendor, press or analyst; conflicts noted)

| Design | Compute | Memory | Provisioned power per slot |
|---|---|---|---|
| Rubin VR200 NVL72 | 35 PF FP4 dense; N3P | 288 GB HBM4, 22 TB/s | Rack 190–230 kW ([Spheron](https://www.spheron.network/blog/nvidia-vera-rubin-nvl72-guide/)). I use 220 kW, i.e. 3.06 kW per slot, trimmed by 150 W. |
| Rubin Ultra, 4-die (as announced) | 100 PF FP4 | ~1 TB HBM4E, ~32 TB/s | Nvidia: 600 kW per 144 packages ([DCD](https://www.datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027/)). Bottom-up: 5.69 kW. |
| Rubin Ultra, 2-die (reported) | About half of the 4-die plan | 8 HBM4E stacks | [Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidia-reportedly-cancels-quad-die-rubin-ultra-gpu-in-favor-of-dual-gpu-design-report-claims-complex-design-purportedly-scrapped-over-manufacturing-execution-concerns); unconfirmed |
| Feynman (2028) | No spec. Reported: stacked GPU dies, custom HBM, A16, LP40 | — | heise reports possibly >2 kW per accelerator |
| MI455X | 40 PF MXFP4 | 432 GB, 19.6 TB/s | 3.2 kW (estimate) |
| TPU 8i | 10.1 PF FP4 | 288 GB at 8.6 TB/s | ~1.3 kW (guess) |
| Groq LP30 / LPX | 1.2 PF, FP8 only | 500 MB SRAM | ~625 W |
| Cerebras CS-4 | ~25 PF per wafer | 44 GB SRAM | ~43 kW (estimate) |

- **GPU decode measurements** (GB200, R1): [LMSYS](https://lmsys.org/blog/2025-09-25-gb200-part-2) 13,386 and 7,583 tok/s per GPU; [vLLM WideEP](https://vllm.ai/blog/2026-02-03-dsr1-gb200-part1) 10.1k. These are **0.34 / 0.29 / 0.31 of my model**, i.e. ρ_G.
- **Process:** I assume N2 compute energy is 0.8× N3P's. TSMC claims N2P is 36% lower power than N3E, and A16 is a further 15–20% lower than N2P ([TSMC](https://www.tsmc.com/english/dedicatedFoundry/technology/platform_HPC_tech_advancedTech)).
- **Reliability:** 419 unexpected interruptions in 54 days on 16,384 H100s, i.e. 0.17 per accelerator-year ([DCD](https://datacenterdynamics.com/en/news/meta-report-details-hundreds-of-gpu-and-hbm3-related-interruptions-to-llama-3-training-run)).
- **Supply:** SoIC ~10–15k wafers/month; CoWoS ~130k wafers/month by late 2026; HBM4 ~$600 per stack in 2026, forecast ~$1,300 in 2027.

## 3. Architecture

### 3.1 Blocks

**C-Die (compute)**
- 4 per package on N2, ~750 mm² each, 144 tiles each.
- Each tile: ~111 TF FP4 tensor engine plus an FP32 vector/softmax unit.
- 64 PF FP4 / 32 PF FP8 dense at 0.75 V; 40.6 / 20.3 PF at 0.55 V.
- Zero-skip ×1.43, assumed equal on both systems.

**W-Tier (SRAM)**
- 8 N4 SRAM tiers hybrid-bonded under the C-Dies: 18.4 GB at 0.15 pJ/bit.
- Own rail and own clock: up to 512 TB/s, run at ω = 0.7 (228 TB/s).
- Holds:
  - the package's experts of both layers in its pair;
  - replicated attention and shared weights;
  - hot-expert replicas;
  - the CSA indexer keys;
  - optionally the HCA KV.

**Package SKUs** (one silicon design; the HBM count varies)

| SKU | HBM | Role | Slot power at 0.55 V, ω = 0.7 |
|---|---|---|---|
| **P-pkg** | 1–4 × HBM4 16-high (48 GB, 2.5 TB/s each); 2 at ≥1,000 | CSA+HCA pairs | 2,309 W with 2 stacks |
| **S-pkg** | None | The extra HCA layer, MTP | 2,126 W |

**Link:** 72 × 224G lanes per direction (1.72 TB/s usable), 162 W.

**Host:** one CPU per 8 packages (50 W per slot), a 30 W NIC and a 30 W switch plane, for 110 W per slot. Rubin gets the same CPU and NIC rule.

**P-pkg chip power at 0.55 V, 2 stacks**

| Component | Power |
|---|---|
| Compute | 902 W |
| Leakage | 367 W |
| W-Tier dynamic (514 × 0.7 × 0.635) | 228 W |
| SRAM static | 100 W |
| HBM | 160 W |
| Links | 162 W |
| **Chip total** | **1,919 W** |

Slot = 1,919 × 1.146 + 110 = 2,309 W.

**Thermal and packaging:**
- ~0.4 W/mm² compute power density.
- P-pkg ~4.5 reticles of CoWoS-L; S-pkg ~3.5.

### 3.2 Mapping at the ≥1,000 point, 128K (`all10.txt`)

| Stage | Packages | Configuration |
|---|---|---|
| 30 CSA+HCA pairs | G = 16 × 30 = 480 P-pkgs | 2 stacks each; indexer keys in SRAM; CSA and HCA KV in HBM |
| Extra HCA layer | 8 S-pkgs | KV in SRAM |
| MTP | 8 S-pkgs | — |
| Head | 1 | — |
| **Total** | **497 packages, 964 stacks** | **1.14 MW, 69,376 users** (previously 710 packages and 1.6 MW) |

- **Schedule:** k = 1, m = 2, b = 1,084.
- **Other tiers:**
  - ≥200: k = 0, m = 3, G = 20 with 4 stacks, 612 packages;
  - ≥2,000: k = 2, m = 3, G = 20 with 1 stack and HCA KV in SRAM, 623 packages.

### 3.3 Numerics

| Data | Format |
|---|---|
| Expert weights | NVFP4, zero-compressed |
| Attention, shared expert, drafter | FP8 |
| Indexer | FP4 |
| KV cache | FP8 |
| Accumulation, softmax | FP32 |
| **mHC residual hand-off** | **BF16, 4 streams** |
| Combine partial sums | BF16 |

## 4. Sanity arithmetic

### 4.1 Hand check at ≥1,000, 128K (`hand10.txt`)

The operating point is G = 16, h = 2, b = 1,084, k = 1 (2 positions per user), so there are 135.5 positions per package.

**Capacity**
- SRAM: 2 × 0.89 GB experts + 2 × 0.43 GB dense + 9.09 GB indexer keys = 11.7 of 16.6 GB usable. Replica room is ample.
- HBM: 4,336 users × (18.95 MB CSA KV + 0.66 MB HCA KV) = 85.0 of 86.4 GB usable (the 90% cap).

**Time per layer**

| Layer | SRAM | HBM | Compute | Dispatch + combine |
|---|---|---|---|---|
| CSA | 6.7 µs | 9.0 µs | **13.66 µs** | 8.7 µs |
| HCA | 6.1 µs | 9.0 µs | **10.47 µs** | 8.7 µs |

- **Dispatch + combine:** 1.07 × 135.5 × 7,168 × 3 × 5.14 × 15/16 = 15.0 MB ÷ 1.72 TB/s = 8.7 µs.
- **Hand-off:** 1.07 × 8 × 135.5 × 7,168 = 8.3 MB, i.e. 4.8 µs, charged on the CSA link.
  - CSA link total = 13.55 µs against 13.66 µs of compute: **the link is 99% used**, which is why 72 lanes are needed.
  - Without pairing, the hand-off would be paid at both layers.

**Throughput**
- c_pair = 24.1 µs; τ = 11.7 µs.
- Tp = max(2 × 24.1, 24.1 + 23.4) = **48.3 µs**.
- Speed: 1.8 ÷ (32 × 48.3 µs) = **1,165 tok/s/user**.
- Efficiency: 0.85 × 2 × 1,084 × 1.8 ÷ 48.3 µs ÷ (497 × 2,303 W) = **60.0 tok/s/W**.
- Rubin at this tier: 36.6 tok/s/W, so the ratio is **1.64**.

### 4.2 Hand check at 1M
The operating point is G = 27, h = 3, b = 233, k = 2, m = 3.

**Capacity**
- SRAM: 15.8 of 16.6 GB (13.9 GB of it indexer keys).
- HBM: 129.1 of 129.6 GB.

**Time and throughput**
- c_pair = 13.15 µs, compute-bound (6.9 + 6.3 µs).
- Tp = max(3 × 13.15, 13.15 + 23.4) = 39.4 µs.
- Speed: **1,933 tok/s/user**.
- Efficiency: **18.5 tok/s/W** on 830 packages, against Rubin's 13.3 / 11.2 at ≥200 / ≥1,000.
- **At 1M every tier uses this single point**, because capacity binds. Continuum cannot trade speed for efficiency there.

### 4.3 Sensitivity (`sens10.txt`, 128K; ratios against Rubin, with Ultra at ≥1,000 in brackets)

| Change | ≥200 / ≥500 / ≥1,000 / ≥1,500 / ≥2,000 |
|---|---|
| Base | 1.27 / 1.40 / 1.64 / 1.92 / 2.90 [1.24] |
| Same node | 1.15 / 1.27 / 1.48 / 1.73 / 2.59 [1.11] |
| η = 0.5 (Continuum only) | 1.11 / 1.23 / 1.39 / 1.64 / 2.46 [1.05] |
| W-Tier at 0.30 pJ/bit | 1.15 / 1.27 / 1.47 / 1.73 / 2.59 [1.11] |
| Leakage ×2 | **1.08** / 1.20 / **1.39** / 1.63 / 2.44 [**1.05**] |
| SRAM static 200 W | 1.23 / 1.37 / 1.60 / 1.87 / 2.82 [1.21] |
| No replicas (imbalance 1.12) | 1.22 / 1.35 / 1.57 / 1.83 / 2.76 [1.19] |
| Imbalance 1.25 | 1.13 / 1.25 / 1.41 / 1.63 / 2.45 [1.06] |
| EP package imbalance ≥ 1.15 | 1.20 / 1.33 / 1.53 / 1.78 / 2.68 [1.15] |
| Collectives 12 µs (Continuum only) | 1.21 / 1.34 / 1.62 / 1.77 / 2.59 [1.22] |
| Usable SRAM 80% | 1.24 / 1.37 / 1.64 / 1.92 / 2.90 |
| Vmin 0.60 V for all | 1.15 / 1.27 / 1.54 / 1.77 / 2.55 [1.19] |
| Two-phase (no overlap), all | 1.18 / 1.31 / 1.58 / 2.03 / 2.56 [1.21] |
| Rubin trimmed 250 W | 1.19 / 1.31 / 1.54 / 1.80 / 2.71 |
| Hot spares 3% at full power | 1.23 / 1.36 / 1.59 / 1.87 / 2.81 [1.20] |
| FP32 residual hand-off (HO = 16) | 1.08 / 1.20 / 1.45 / 1.53 / 2.28 [1.09] |
| No pairing (corrected Continuum-9 mapping) | 1.13 / 1.25 / 1.51 / 1.69 / 2.51 |

**At 1M**, the worst single case is η = 0.5: 1.17 / 1.40 against Rubin and **0.92** / 1.11 against Ultra.

**Worst of 90 pairs, against Rubin and Ultra**

| Pair | Against Rubin | Against Ultra |
|---|---|---|
| η = 0.5 + leakage ×2 | 0.95 / 1.05 / **1.17** / 1.38 / 2.07 | 0.86 / 0.86 / **0.88** / 0.97 / 1.04 |
| Leakage ×2 + imbalance 1.25 | 0.96 / 1.07 / 1.19 / 1.38 / 2.06 | 0.88 / 0.88 / 0.90 / 0.96 / 1.04 |
| η = 0.5 + imbalance 1.25 | 0.99 / 1.09 / 1.20 / 1.43 / 2.11 | 0.90 / … / 0.91 |
| **Median pair** | 1.10 / 1.22 / **1.43** / 1.65 / 2.41 | 1.01 / 1.02 / **1.08** / 1.17 / 1.23 |

### 4.4 Supply and cost per unit of output (128K)

| | ≥200 | ≥1,000 | ≥2,000 |
|---|---|---|---|
| Tokens per HBM GB against Rubin | 3.1× | 7.5× | 25× |
| All silicon (N2 + N4) per token against Rubin | 2.7× | 2.25× | 1.33× |
| N2 only, per token | 0.90× | 0.75× | 0.44× |
| Tok/s per BOM dollar, centre (crossed range) | 1.54× (0.97–2.35) | 2.35× (1.55–3.37) | 4.6× |

- **Per GW at ≥1,000:**
  - 434k packages and 0.84M HBM stacks; Rubin needs about 4.5M stacks for the same tokens;
  - **76k SoIC wafer passes, 5–8 months of 2026 SoIC capacity. SoIC is the binding supply line.**

### 4.5 Site level, including prefill
Energy per prompt token at 128K: Rubin 15.8 mJ, Continuum 12.7 mJ, a ratio of 1.24 (about 1.13 on the same node).

| r (fresh prompt tokens per output token) | Prefill on GPUs: ≥200 / ≥1,000 / ≥2,000 | All Continuum |
|---|---|---|
| 0.25 | 1.21 / 1.52 / 2.56 | 1.26 / 1.58 / 2.65 |
| 1 | 1.13 / 1.33 / 2.01 | 1.25 / 1.47 / 2.21 |
| 4 | 1.05 / 1.13 / 1.42 | 1.25 / 1.34 / 1.67 |
| 64 | 1.00 / 1.01 / 1.03 | 1.24 / 1.25 / 1.28 |

## 5. All-system comparison (Continuum-10 ÷ X; `all10.txt`, `feyn10.txt`)

| Against | 128K | 1M |
|---|---|---|
| Rubin, trimmed | 1.27 / 1.40 / 1.64 / 1.92 / 2.90 | 1.39 / 1.39 / 1.66 / 2.33 / 4.49 |
| Rubin as shipped | 1.38 / 1.53 / 1.80 / 2.11 / 3.18 | 1.52 / … / 1.81 |
| Ultra 4-die, bottom-up | 1.16 / 1.16 / **1.24** / 1.34 / 1.45 | **1.08** / 1.08 / 1.31 / 1.49 / 1.69 |
| Ultra 4-die, 600 kW, 100 PF | 1.03 / 1.14 / 1.22 / 1.32 / 1.41 | 1.12 / 1.12 / 1.31 / 1.62 / 2.18 |
| Ultra 2-die (reported) | 1.35 / 1.49 / 1.75 / 2.05 / 3.08 | 1.26 / 1.39 / 1.76 / 2.46 / 4.78 |
| **Feynman proxy** (Ultra architecture, compute energy × 0.66) | 0.96 / 0.97 / 1.04 / 1.13 / 1.22 | 0.91 / … / 1.09 |
| **Feynman proxy, Continuum also on A16** | 1.04 / 1.05 / **1.13** / 1.23 / 1.33 | 0.99 / … / 1.18 |
| Feynman proxy + custom HBM at 1.5× bandwidth, Continuum on A16 | 0.93 / 1.04 / **1.02** / 1.10 / 1.15 | 0.89 / … / 0.98 |
| MI455X | 2.27 / 2.51 / 2.75 / 3.47 / 5.11 | 1.87 / … / 2.61 |
| TPU 8i | 2.50 / 3.02 / 3.86 / 5.18 / 14.7 | 2.03 / … / 3.60 |
| Rubin + LPX (FP8 weights) | 9.2–14 | 16–26 |
| CS-4 | 29–32 | ~29 |

**Variants**
- **NVFP4 KV on every system:** 128K 1.31 / 1.45 / 1.58 / 1.84 / 2.55.
- **p = 0.6:** above ~3× the ratios reflect Rubin's speed ceiling, so I don't claim them.
- **Max tok/s/user:** Continuum about 4,860, Rubin 4,950, Ultra 5,560. **Continuum does not win peak speed.** The earlier ~5,600 came from a tensor-split mapping that the HO = 8 hand-off breaks.

## 6. Software stack and programming model
**Front end:** PyTorch (`torch.export`) and JAX (StableHLO) → MLIR → spatial schedule. Per deployment it:
- **pairs consecutive layers** onto G-package groups;
- picks G, the stack count and the KV placement for each pair;
- places experts and hot replicas from a routing profile;
- **pins each user's attention for both layers of a pair to one package** (user-stationary);
- sets ω, V, k and m.

All of this is capacity-checked offline; recompiling takes hours.

**Dynamic parts:**
- EP dispatch and combine within a group: variable-size packets, 1.07× headroom.
- The hand-off between pairs is a static neighbour transfer.
- Compute stays statically scheduled.

**Kernels:** a tile DSL (block-matmul, softmax, gather) for CSA, HCA, the FP4 indexer, MLA and the mHC mixing.

**Serving:** a vLLM/SGLang backend with:
- continuous batching at pair boundaries;
- paged KV in HBM and SRAM;
- cold-spare failover (weights reload in about 25 ms; lost KV is re-prefilled in about 6 s of pod time);
- chunked prefill in the pipeline, or GPU prefill with KV shipped over the NIC.

**Existing models:** they convert by NVFP4 post-training quantization. Models without alternating compressed attention (dense GQA or MLA) still map: all packages become P-pkgs. They lose most of the SRAM-KV gain, and I estimate about 1.3× at 128K (not re-run).

**Training and dynamic control flow** stay on GPUs. GPU V4 software improved 2.1–2.6× in about two months; Continuum starts from zero.

## 7. Where Continuum loses or ties
1. **Against Ultra under adverse pairs:** 0.86–0.90 at ≤1,000 tok/s/user, and the median pair is 1.01–1.08. The same-date win depends on the base assumptions.
2. **Against a Feynman-class part on the same node:** about 1.0–1.13 at ≥1,000, and 0.89–0.99 at 1M bulk. The 2028 margin is not established.
3. **Bulk 128K:** 1.27× Rubin base, 0.95 under the worst pair.
4. **Site level with GPU prefill and r ≥ 4:** 1.01–1.13×.
5. **Silicon:** 2.25–2.7× Rubin's silicon per token; 76k SoIC passes per GW.
6. **Peak per-user speed:** about 4,860 against Ultra's 5,560.
7. **Model lock-in**, no training, a 2028 calendar.

## 8. What has to be true

| Assumption (base) | If wrong | ≥1,000 ratio |
|---|---|---|
| ρ_C = ρ_G (≈ 0.3) | ρ_C = 0.8 ρ_G | 1.31 (parity at 0.61) |
| Leakage as modelled (367 W at 0.55 V) | ×2 | 1.39 |
| η = 0.6 on ~34-token expert tiles | 0.5 | 1.39 |
| EP imbalance ≤ 1.07 with 12.5% replicas | 1.15 | 1.53 |
| N2 compute energy 0.8× N3P | Same node | 1.48 |
| W-Tier at 0.15 pJ/bit | 0.30 | 1.47 |
| Residual hand-off in BF16 | FP32 | 1.45 |
| Link reaches 85% of raw bandwidth (CSA link at 99% of budget) | 75% | about 1.55 (estimate: the next-best point is 64-lane-like) |
| CSA and HCA alternate in V4-Pro | Same-type runs | Pairing gain unmodelled; fallback 1.51 |
| The frontier stays sparse MoE with compressed attention | Dense attention | About 1.3× |

## 9. Risks and physical, process and supply limits
- **SoIC:** 5–8 months of 2026 capacity per GW.
- **CoWoS-L:** ~4.5 reticles (P-pkg).
- **HBM:** 0.84M 16-high stacks per GW; 16-high volume is unconfirmed.
- **Capacity:** HBM is at 98% of its 90% cap at both contexts, so admission control is mandatory.
- **Link margin:** the CSA link is at 99% of its budget at the base point.
- **Low voltage:** 0.55 V with adaptive clocking.
- **Yield:** a 750 mm² N2 die is ~47% raw, ~65% with harvesting; bonds are 98–99% each; known-good-die testing is mandatory.
- **Failures:** 85 per year per instance at about 6 s each, which is negligible. A mirror is not needed.

## 10. Tests that could prove the design wrong

| # | Test | Tool | Kill criterion |
|---|---|---|---|
| 1 | Decode realisation against GPU decode-pool runs | LLMCompass-class event simulator, V4 traces | ρ_C < 0.61 ρ_G |
| 2 | EP dispatch imbalance and link tail at G = 16, b = 1,084, with real routing and pair hand-offs | Trace replay + SerDes/switch simulator | Imbalance > 1.15, collectives > 12 µs, or link efficiency < 80% |
| 3 | Tile η at M ≈ 34, N = 3072, NVFP4 | Timeloop/Accelergy + one-tile RTL | η < 0.5 |
| 4 | N2 V/f, leakage and energy at 0.55 V | PDK SPICE | Leakage > 1.5× model |
| 5 | W-Tier pJ/bit and static power | CACTI/DESTINY | > 0.25 pJ/bit or > 200 W |
| 6 | V4-Pro layer order and mHC hand-off precision | Config and quantization study | Layers not alternating, or BF16 hand-off loses accuracy |
| 7 | Rubin's best decode efficiency at ≥1,000 | Measurement | > 41 tok/s/W cuts the ratio below 1.45 |
| 8 | A Feynman specification | Vendor disclosure | Same-node proxy ratio < 1.1 at ≥1,000 |
| 9 | Thermal and IR drop | HotSpot/3D-ICE | Tj > 105 °C or IR drop > 5% |

None of these could be run here. Tests 1, 2 and 4 matter most.

## 11. Facts vs assumptions
**Facts (sourced, many secondary):**
- the chip specifications and rack figures in §2;
- the reported 2-die Ultra and the reported Feynman features;
- GB200 decode measurements;
- the Llama 3 interruption counts;
- TSMC's process claims;
- V4 using mHC;
- V4-Flash alternating CSA and HCA layers;
- packaging capacity.

**Derived by me:**
- ρ_G;
- Rubin's 150 W trim;
- the EP and hand-off link formulas;
- the pair pipeline accounting;
- the failure cost;
- capacity and supply per GW.

**My assumptions:**
- hc_mult = 4 (from the check's config citation);
- Pro's layer order;
- the V/f law, τ(f), the 1.146 rule and the 110 W host;
- every pJ figure;
- 100 W of SRAM static power;
- leakage;
- η = 0.6, the 0.85 derate and the imbalances;
- the Feynman proxy (× 0.66 compute energy, optional +50% HBM bandwidth);
- costs and yields.

**Model outputs:** every throughput, ratio and energy figure.

**Files** (in `/home/user/SomeRepository/engine/runs/refine_continuum_d/round3/`):

| File | Contents |
|---|---|
| `model10.py` | HO = 8 hand-off, pair layout, two-phase option; imports `model9.py` and `model8.py`, unchanged |
| `t10.py` → `t10.txt` | Reproduces Continuum-9 (59.8) and the check's 1.46 / 1.59; lane checks |
| `sweep10.py` → `sweep10.txt` | Lanes × ω, 128K and 1M |
| `hand10.py` → `hand10.txt` | Hand checks in §4.1–4.2 |
| `sens10.py` → `sens10.txt` | 14 singles + 4 extra × 2 contexts, 90 pairs, against Rubin and Ultra |
| `all10.py` → `all10.txt` | All systems, site level, supply, NVFP4 KV, p = 0.6 |
| `tau10.py` → `tau10.txt` | Collective-latency lever, Continuum only and both systems |
| `feyn10.py` → `feyn10.txt` | Feynman proxy |

---

**Sources**
- [SemiAnalysis InferenceX: DeepSeek-V4 (mHC, CSA/HCA)](https://inferencex.semianalysis.com/model/deepseek-v4)
- [AMD ROCm: DeepSeek-V4-Flash on MI355X (layer alternation)](https://rocm.blogs.amd.com/software-tools-optimization/primus-deepseek-v4/README.html)
- [NVIDIA NeMo DeepSeek-V4 config](https://docs.nvidia.com/nemo/automodel/nemo-automodel/nemo_automodel/components/models/deepseek_v4/config)
- [Hugging Face Transformers: DeepSeek-V4](https://huggingface.co/docs/transformers/main/model_doc/deepseek_v4)
- [arXiv DeepSeek-V4](https://arxiv.org/pdf/2606.19348)
- [heise: Feynman stacked dies and custom HBM](https://heise.de/-11214678)
- [Jon Peddie: GTC 2026 keynote](https://www.jonpeddie.com/news/nvidia-gtc-2026-keynote/)
- [Wccftech: Feynman 3D stacking, cHBM, Rosa](https://wccftech.com/nvidia-feynman-gpu-gets-3d-die-stacking-custom-hbm-next-gen-rosa-cpu/amp/)
- [igorsLAB: Feynman logic stacking](https://www.igorslab.de/en/starting-in-2028-nvidia-will-apparently-stack-true-logic-dies-in-feynman-for-the-first-time-turning-25d-into-a-thermal-tightrope-walk/)
- [DCD: Meta Llama 3 interruptions](https://datacenterdynamics.com/en/news/meta-report-details-hundreds-of-gpu-and-hbm3-related-interruptions-to-llama-3-training-run)
- [LMSYS GB200 Part II](https://lmsys.org/blog/2025-09-25-gb200-part-2)
- [LMSYS GB200 Part I](https://www.lmsys.org/blog/2025-06-16-gb200-part-1)
- [vLLM WideEP on GB200](https://vllm.ai/blog/2026-02-03-dsr1-gb200-part1)
- [Tom's Hardware: 2-die Rubin Ultra](https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidia-reportedly-cancels-quad-die-rubin-ultra-gpu-in-favor-of-dual-gpu-design-report-claims-complex-design-purportedly-scrapped-over-manufacturing-execution-concerns)
- [Spheron: Vera Rubin NVL72](https://www.spheron.network/blog/nvidia-vera-rubin-nvl72-guide/)
- [DCD: Rubin Ultra at 600 kW](https://www.datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027/)
- [PyTorch/SGLang: V4 on GB300](https://pytorch.org/blog/serving-deepseek-v4-on-gb300-with-sglang-5x-higher-throughput-at-the-same-interactivity-since-day-0/)
- [TSMC process technology](https://www.tsmc.com/english/dedicatedFoundry/technology/platform_HPC_tech_advancedTech)
- [SemiAnalysis: LP30](https://newsletter.semianalysis.com/p/nvidia-the-inference-kingdom-expands)
- [StorageReview MI455X](https://www.storagereview.com/news/amd-mi455x-and-helios-432gb-hbm4-72-gpu-racks-and-a-real-answer-to-vera-rubin)
- [Google TPU 8](https://cloud.google.com/blog/products/compute/tpu-8t-and-tpu-8i-technical-deep-dive)
- [StorageReview CS-4](https://www.storagereview.com/news/cerebras-cs-4-three-wse-3-turbo-wafers-750-pflops-and-a-claimed-30x-over-gpu-racks)
- [Silicon Analysts: HBM4 price](https://siliconanalysts.com/market/trendforce-lifts-2027-hbm-asp-forecast-to-121-hbm4-stack-seen-doubling-to-1-300-2026-10-01)
- [TrendForce SoIC](https://www.trendforce.com/news/?p=54678)
- [TSMC CoWoS 130k](https://www.financialcontent.com/article/tokenring-2026-2-5-tsmc-to-quadruple-advanced-packaging-capacity-reaching-130000-cowos-wafers-monthly-by-late-2026)