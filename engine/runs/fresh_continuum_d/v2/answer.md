I reproduced the check's "worst untested pair" of 1.10 for Continuum-8: W-Tier at 0.30 pJ/bit combined with doubled leakage. Writing the final answer now.

# Continuum-9: a weight-stationary 3D-SRAM decode accelerator for frontier MoE, with expert-parallel pipeline stages

Every Continuum number below is model output. There is no silicon and no simulator run. Unless stated otherwise, a ratio is Continuum's output tok/s per provisioned watt divided by that of the best Rubin configuration at the same per-user speed floor. Rubin is trimmed by 150 W under the shared host rule. The workload is DeepSeek-V4-Pro at 128K context with draft acceptance p = 0.8. Tiers are written ≥200 / ≥500 / ≥1,000 / ≥1,500 / ≥2,000 tok/s/user.

## 0. Verdict

### 0.1 How each point of the check was handled

| Check point | Decision | Number |
|---|---|---|
| **Count spares** (the check's ~1.45 implies about 3–4% charged on power) | **Partly refuted, and a cost the check missed is added.** Spares are capital, not provisioned watts. Spares can be cold: a spare loads its 1.5 GB of weights from the host in about 25 ms and is otherwise power-gated (5% idle power assumed). The real cost of a failure is lost KV. Failure rate: 419 unexpected interruptions in 54 days on 16,384 GPUs (Llama 3) = 0.17 per accelerator-year. That is about 120 failures a year for a 710-package instance. Without protection, each failure forces 6.8k users × 128K tokens to be prefilled again, about 1.9 h of the pod each time: **2.7% of capacity.** Fix: mirror each step's new KV to host DRAM. That is 1.4 GB/s per package against a 100 GB/s NIC, and about 1.2 TB of DRAM per 8 packages, which a Vera-class CPU supports. Restore takes about 1.5 s. I charge **10 W per slot** for that DRAM. | Cold spares + KV mirror: **−0.6%** (1.63 → 1.62 at ≥1,000). Hot-spare bound (3% at full power) shown in every table: 1.59. Spares stay in silicon and cost: −3%. |
| **Worst untested pair = 1.10** | **Accepted for Continuum-8; I reproduce 1.10** (W-Tier at 0.30 pJ/bit + leakage ×2, `c8pairs.txt`). All **90 pairs** of 14 adverse assumptions are now tested on the new design. | Continuum-9's worst pair at ≥1,000: **1.19** (η = 0.5 + leakage ×2). The pair that gave 1.10 now gives 1.25. |
| **About 1.14× against same-date bottom-up Ultra** | **Accepted as the right comparator.** Ultra ships in H2 2027; Continuum ships no earlier than 2028. Feynman (2028) has no public specification, so I cannot compare against it. | Continuum-9 against 4-die bottom-up Ultra: **1.11 / 1.11 / 1.23 / 1.27 / 1.34**. Against the 600 kW, 100 PF Ultra: 1.00 at ≥200 (Continuum-8 lost there at 0.92). |
| **The bulk tier is a tie (about 1.0–1.1)** | **Accepted, narrowed.** The base is now 1.22×. It falls to 1.03–1.14 under any one adverse assumption and to 0.89 under the worst pair. | Still not a defensible win. |
| Other points (numbers byte-identical, NVFP4-KV rows) | Confirmed by the check; no change. | — |

### 0.2 The change that raises the honest number: expert-parallel stages (`sweep9*.txt`, `all9.txt`)

**What bound Continuum-8.** Inside each layer's stage, Continuum-8 split every expert's intermediate dimension across g packages. Every package therefore had to receive and reduce every position, about 2.9 × hidden bytes per position per package. That traffic is independent of g. The link was 85–93% used, so the microbatch could not grow, and the fixed per-layer latency τ stayed exposed.

**What Continuum-9 does.**
1. **Expert-parallel split.** Each package owns 384/g whole experts plus the attention for b/g users. A token is sent only to the packages that own its 6 experts. The number of distinct packages hit is D(g) = g(1 − (1 − 1/g)^6), which is 4.96 at g = 13. Bytes received per package per position:
   - EP: hid × (1 + 3·D·(g − 1)/g)/g = **1.15 × hid** at g = 13;
   - the old split: 2.92 × hid.
   
   The link stops binding, so stages can be wider (g up to 14) and microbatches larger (b = 713 against 354).
2. **The W-Tier SRAM gets its own clock domain**, provisioned per deployment at ω × 512 TB/s. This is chosen like a voltage point, and every system picks its own voltage. At g = 13 each package reads only 1.1 GB of expert weights per microbatch, so ω = 0.7 suffices. Provisioned W-Tier power = 100 W static (new, charged explicitly) + 514 W × ω × clock.

| Step (128K, Rubin trimmed 150 W) | ≥200 | ≥500 | ≥1,000 | ≥1,500 | ≥2,000 |
|---|---|---|---|---|---|
| Continuum-8 (round 1, reproduced at 55.2 tok/s/W) | 1.13 | 1.25 | 1.51 | 1.71 | 2.51 |
| + EP stages, W-Tier at ω = 1, 100 W SRAM static charged | 1.20 | 1.33 | 1.60 | 1.91 | 2.82 |
| + W-Tier at ω = 0.7, g ≤ 14: **Continuum-9** (59.8 tok/s/W) | **1.22** | **1.35** | **1.63** | **1.81** | **2.67** |
| Continuum-9 with KV mirror (+10 W/slot) and cold spares | 1.21 | 1.34 | **1.62** | 1.80 | 2.66 |
| Same, but with g ≤ 20 (927 packages per instance) | 1.25 | 1.38 | 1.67 | 1.96 | 2.92 |
| Same, but with g ≤ 10 (525 packages) | 1.18 | 1.31 | 1.58 | 1.79 | 2.55 |

**Levers that failed:**
- Fewer link lanes: 48 lanes → 1.54; 40 lanes → 1.51.
- More lanes: 80 → 1.65; 96 → 1.62.
- ω below 0.7: at ω = 0.4 the result is 1.60 at g ≤ 14.

**At 1M context the change does not help.** With the W-Tier clock at ω = 1 the result is 15.4 tok/s/W against Continuum-8's 15.7. The 2% loss is the newly charged SRAM static power. At 1M the binding resource is SRAM KV bandwidth, not the link.

### 0.3 Defensible claims

| Claim | Number | Holds only if |
|---|---|---|
| Decode tok/s/W against Rubin, 128K | **1.62× at ≥1,000** (1.21× at ≥200, 2.66× at ≥2,000); same node 1.47× | Continuum realises ≥ 62% of the decode fraction GPUs realise, i.e. ≥ 0.18–0.21 of its own model (GPUs realise 0.29–0.34, `calib8.txt`) |
| Worst single adverse assumption, ≥1,000 | 1.38 (leakage ×2) | — |
| Worst of 90 pairs, ≥1,000 | **1.19** (η = 0.5 + leakage ×2); median pair 1.41 | — |
| Against 4-die bottom-up Ultra (same date) | **1.23× at ≥1,000**; 1.11 at ≥200; 1.34 at ≥2,000 | The 4-die Ultra ships; reports say it is cancelled |
| Against the reported 2-die Ultra | 1.30 / 1.74 / 2.84 | The reports hold |
| Bulk tier (≥200) | **Not a win.** 1.22 base; 1.03–1.19 under one adverse assumption; 0.89 under the worst pair | — |
| Site level, Continuum also doing prefill | 1.48× at ≥1,000 with r = 1; floor 1.27 (about 1.15 on the same node) | Equal prefill η and imbalance on both systems |
| Site level, prefill left on GPUs | 1.33 (r = 1) → 1.04 (r = 16) | — |
| 1M context | 1.15 / 1.38 / 3.74 against Rubin; **0.90 / 1.09 / 1.41 against 4-die Ultra** | — |
| Tokens per HBM GB | 6.4× (≥200), 8.6× (≥1,000) | SoIC and N4 SRAM capacity are less scarce than HBM |

**Bottom line.**
- Continuum-9 is a credible design for the **best decode tokens per MW and per HBM GB at 1,000–2,000 tok/s/user**, on frontier sparse MoE with compressed attention, at 128K context. That is **about 1.6× Rubin and 1.2× a same-date 4-die Ultra**, and it stays at or above 1.19× under every adverse pair tested.
- It is **not** shown to be the best in the world overall:
  - at bulk speeds it is within the noise of Rubin;
  - at 1M bulk it loses to Ultra (0.90×);
  - it does not train;
  - every Continuum number is model output.

---

## 1. Target workloads and metrics

**Workload: decode of DeepSeek-V4-Pro.**
- 1.6T total / 49B active parameters, 61 layers plus an MTP drafter.
- 384 experts, top-6, plus a shared expert; expert FFN size 3072.
- 30 CSA layers: an FP4 indexer scores L/4 compressed keys, then top-1024 attention plus a 128-token window.
- 31 HCA layers: 128× compressed attention.
- FP8 KV cache.
- Conditions: 128K and 1M context; p = 0.8 (code and tools) or 0.6 (prose).

**Out of scope:**
- training;
- edge;
- models under ~200B, where SRAM-only systems win;
- the 6.2T stress case, which has not been re-run.

| Metric | Why it defines "best" |
|---|---|
| Output tok/s per provisioned MW at a per-user floor (200…2,000 tok/s/user) | Sites are power-limited, and the floor stops gaming at low speeds. Each system picks its own draft depth k (0–6), microbatch count m (1–4), layout and voltage (0.55–0.75 V on one V/f law for all systems). Continuum also picks the W-Tier clock ω. |
| The same at site level, including prefill, with r fresh prompt tokens per output token | The decode-pod metric alone overstates the gain. |
| Tok/s per HBM GB; total silicon per token | HBM is supply-limited; silicon is what Continuum spends instead. |
| Max tok/s/user; cost per token | Speed tier; cost is rough only. |

**Gate.** A gain counts only if it holds with:
- the same V/f law, slot-saving rule (1.146), latency model τ = 7 + 3/f µs and host rule for every system;
- Rubin in its best layout;
- all 90 adverse pairs reported.

## 2. Reference points (vendor, press or analyst; conflicts noted)

| Design | Compute | Memory | Provisioned power per slot |
|---|---|---|---|
| Rubin VR200 NVL72 | 35 PF FP4 dense ("50" with adaptive compression); N3P | 288 GB HBM4, 22 TB/s | Rack 190–230 kW, one originator ([Spheron](https://www.spheron.network/blog/nvidia-vera-rubin-nvl72-guide/)). I use 220 kW = 3.06 kW per slot, trimmed by 150 W. |
| Rubin Ultra, 4-die (as announced) | 100 PF FP4 | ~1 TB HBM4E, ~32 TB/s | Nvidia: 600 kW per 144 packages ([DCD](https://www.datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027/)). Bottom-up: 5.69 kW. |
| Rubin Ultra, 2-die (reported) | About half of the 4-die plan | 8 HBM4E stacks | [Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidia-reportedly-cancels-quad-die-rubin-ultra-gpu-in-favor-of-dual-gpu-design-report-claims-complex-design-purportedly-scrapped-over-manufacturing-execution-concerns), [igorsLAB](https://www.igorslab.de/en/nvidia-rubin-ultra-four-die-design-dropped/); unconfirmed by Nvidia |
| MI455X | 40 PF MXFP4 | 432 GB, 19.6 TB/s | 3.2 kW (estimate) |
| TPU 8i / Ironwood | 10.1 PF FP4 / 4.6 PF FP8 | 288 GB at 8.6 TB/s / 192 GB at 7.37 TB/s | 1.3 / 1.2 kW (guesses) |
| Groq LP30 / LPX | 1.2 PF, FP8 only | 500 MB SRAM | ~625 W |
| Cerebras CS-4 | ~25 PF per wafer | 44 GB SRAM | ~43 kW per wafer (estimate) |

- **Decode-only GPU measurements** (GB200, R1, 2K-token inputs): [LMSYS Part II](https://lmsys.org/blog/2025-09-25-gb200-part-2) 13,386 tok/s per GPU; [Part I](https://www.lmsys.org/blog/2025-06-16-gb200-part-1) 7,583; [vLLM WideEP](https://vllm.ai/blog/2026-02-03-dsr1-gb200-part1) 10.1k. These are **0.34 / 0.29 / 0.31 of my model.**
- **Process:** I assume N2 compute energy is 0.8× N3P's. TSMC claims N2P is 36% lower power than N3E ([TSMC](https://www.tsmc.com/english/dedicatedFoundry/technology/platform_HPC_tech_advancedTech)). Same-node rows are shown throughout.
- **Reliability:** 419 unexpected interruptions in 54 days on 16,384 H100s, about half GPU or HBM ([DCD](https://datacenterdynamics.com/en/news/meta-report-details-hundreds-of-gpu-and-hbm3-related-interruptions-to-llama-3-training-run), [SDxCentral](https://www.sdxcentral.com/news/meta-report-details-hundreds-of-gpu-and-hbm3-related-interruptions-to-llama-3-training-run/)).
- **Supply:** SoIC ~10–15k wafers/month; CoWoS ~130k wafers/month by late 2026; HBM4 ~$600 per stack in 2026, forecast ~$1,300 in 2027.

## 3. Architecture

### 3.1 Blocks (silicon unchanged from Continuum-8 except the W-Tier clock domain)

**C-Die (compute)**
- 4 per package on N2, ~750 mm² each, 144 tiles each.
- Each tile: ~111 TF FP4 tensor engine plus an FP32 vector/softmax unit.
- 64 PF FP4 / 32 PF FP8 dense at 0.75 V; **40.6 / 20.3 PF at 0.55 V**.
- Zero-skip ×1.43, assumed equal to Rubin's on both systems.

**W-Tier (SRAM)**
- 8 N4 SRAM tiers hybrid-bonded under the C-Dies: 18.4 GB, 0.15 pJ/bit.
- Own rail (≥0.65 V) and **own clock**: up to 512 TB/s; run at ω = 0.7 at 128K and ω = 1 at 1M.
- Holds:
  - the package's whole experts;
  - replicated attention and shared weights (0.43 GB);
  - hot-expert replicas;
  - indexer keys (CSA packages) or the whole KV (HCA and MTP packages).

**Package SKUs**

| SKU | HBM | Role | Slot power at 0.55 V, ω = 0.7 |
|---|---|---|---|
| **K-pkg** | 3 × HBM4 16-high (144 GB, 7.5 TB/s); 2 or 4 optional | CSA layers | 2,380 W |
| **S-pkg** | None | HCA and MTP layers | 2,105 W |

**Link:** 64 × 224G lanes per direction (1.53 TB/s usable), 144 W.

**Host:** one CPU per 8 packages (50 W per slot) plus **10 W for KV-mirror DRAM**, a 30 W NIC and a 30 W switch plane. Rubin gets the same CPU and NIC rule.

**K-pkg chip power at 0.55 V**

| Component | Power |
|---|---|
| Compute | 902 W |
| Leakage | 367 W |
| W-Tier dynamic (514 × 0.7 × 0.635) | 228 W |
| SRAM static | 100 W |
| HBM | 240 W |
| Links | 144 W |
| **Chip total** | **1,981 W** |

Slot = 1,981 W × 1.146 + 110 W = 2,380 W. The S-pkg has no HBM: 1,741 W chip, 2,105 W slot.

**Thermal and packaging:**
- ~0.4 W/mm² compute power density.
- K-pkg ~5 reticles of CoWoS-L; S-pkg ~3.5 reticles.

### 3.2 Mapping (128K, the ≥200–≥1,000 operating point)

| Stage | Packages | Configuration |
|---|---|---|
| CSA | g = 13 × 30 layers = 390 K-pkgs | Indexer keys in SRAM |
| HCA | g = 10 × 31 layers = 310 S-pkgs | KV in SRAM |
| MTP | 9 S-pkgs | — |
| Head | 1 | — |
| **Total** | **710 packages, 1,174 HBM stacks** | **1.6 MW, 88,412 users per instance** |

- **Within a stage:** experts are split expert-parallel with EPLB-style hot replicas; attention is data-parallel.
- **Schedule:** k = 1, m = 2, b = 713.
- **The compiler** picks per stage type g, stack count and KV/indexer placement, and picks ω, V, k and m per deployment, all capacity-checked.

### 3.3 Numerics (unchanged)

| Data | Format |
|---|---|
| Expert weights | NVFP4, zero-compressed |
| Attention, shared expert, drafter | FP8 |
| Indexer | FP4 |
| KV cache | FP8 |
| Accumulation, softmax | FP32 |
| Combine partial sums | BF16 (counted at 2 B per element in the link bytes) |

V4-Pro already runs FP4 on GB300.

## 4. Sanity arithmetic

### 4.1 Hand check at ≥1,000 (128K, 0.55 V, ω = 0.7; 1,426 positions per microbatch)

**Compute per position (full package)**

| Part | Time per position |
|---|---|
| Linear | 2.85e-8 s |
| Attention (FP8) | 1.49e-8 s |
| CSA indexer (FP4) | 1.32e-8 s |

**CSA stage (g = 13)**
- Compute: 5.66e-8 × 1,426 × 1.07 ÷ 0.6 ÷ 13 = **11.07 µs**.
- Link (EP): 1,426/13 × 7,168 × (1 + 3 × 4.96 × 12/13) × 1.07 = 12.4 MB ÷ 1.53 TB/s = **8.1 µs** ✓. The old split would need 29.9 MB, i.e. 19.5 µs, and would bind.
- Capacity:
  - SRAM: 1.10 GB experts + 0.43 GB dense + 14.3 GB indexer keys = 15.8 of 16.6 GB, with 0.75 GB of replica room against 0.14 GB needed ✓;
  - HBM: 88,412 × 18.95 MB ÷ 13 = 128.9 of 129.6 GB. **99.4% full: admission control is mandatory.**

**HCA stage (g = 10)**
- Compute: 4.34e-8 × 1,426 × 1.07 ÷ 0.6 ÷ 10 = **11.04 µs**.
- SRAM traffic: 1.43 GB × 1.07 + 0.43 GB + 47 MB KV = 2.0 GB ÷ 228 TB/s = 8.8 µs ✓.

**Throughput**
- τ = 11.7 µs, so T = max(2 × 11.07, 11.07 + 11.7) = **22.8 µs**.
- Speed: 1.8 ÷ (62 × 22.8 µs) = **1,273 tok/s/user**.
- Efficiency: 0.85 × 2 × 713 × 1.8 ÷ 22.8 µs ÷ (710 × 2,257 W) = **59.7 tok/s/W** ✓ (model 59.8).

**Rubin at the same tier:** 36.6 tok/s/W, so the ratio is **1.63**.

### 4.2 Operating points (`all9.txt`)

| Tier | Continuum-9 | tok/s/W | Rubin |
|---|---|---|---|
| ≥200 to ≥1,000 | Above | 59.8 | 49.0 / 44.2 / 36.6 |
| ≥1,500 | k = 2, b = 539, 710 packages | 55.6 | 30.7 |
| ≥2,000 | k = 3, b = 407, 772 packages, CSA on 2 stacks | 51.2 | 19.2 |
| 1M (ω = 1) | k = 4, m = 3, b = 50, 651 packages, 2,985 tok/s/user | 15.4 | 13.3 / 13.3 / 11.2 / 7.9 / 4.1 |

### 4.3 Sensitivity (`sens9.txt`)

**Single adverse assumptions**

| Change | 128K | 1M (ω = 0.7, conservative) |
|---|---|---|
| Base | 1.22 / 1.35 / 1.63 / 1.81 / 2.67 | 1.08 / 1.08 / 1.29 / 1.81 / 3.50 |
| Same node | 1.10 / 1.21 / 1.47 / 1.63 / 2.39 | 0.97 / … / 1.16 |
| η = 0.5 (Continuum only) | 1.05 / 1.16 / 1.41 / 1.55 / 2.22 | 0.98 / … / 1.17 |
| W-Tier at 0.30 pJ/bit | 1.09 / 1.21 / 1.46 / 1.62 / 2.38 | 0.97 / … / 1.16 |
| Leakage ×2 | **1.03** / 1.14 / **1.38** / 1.53 / 2.24 | 0.91 / … / 1.09 |
| SRAM static 200 W | 1.19 / 1.31 / 1.59 / 1.76 / 2.59 | 1.05 / … / 1.25 |
| No replicas (imbalance 1.12) | 1.19 / 1.32 / 1.60 / 1.75 / 2.54 | 1.05 / … / 1.26 |
| Imbalance 1.25 | 1.08 / 1.19 / 1.44 / 1.59 / 2.25 | 0.99 / … / 1.19 |
| EP package imbalance ≥ 1.15 | 1.17 / 1.29 / 1.57 / 1.72 / 2.50 | 1.04 / … / 1.24 |
| Collectives 12 µs | 1.14 / 1.26 / 1.53 / 1.72 / 2.45 | 1.04 / … / 1.23 |
| Usable SRAM 80% | 1.17 / 1.30 / 1.57 / 1.81 / 2.67 | 1.04 / … / 1.24 |
| Vmin 0.60 V for both | 1.13 / 1.25 / 1.52 / 1.81 / 2.59 | 1.08 / … / 1.36 |
| Two-phase (no overlap), both | 1.14 / 1.26 / 1.52 / 1.95 / 2.50 | 0.97 / 1.03 / 1.39 |
| Rubin trimmed 250 W | 1.14 / 1.26 / 1.53 / 1.70 / 2.49 | 1.01 / … / 1.21 |
| Hot spares 3% at full power | 1.19 / 1.31 / 1.59 / 1.76 / 2.59 | 1.05 / … / 1.25 |

**Worst pairs (90 tested, 128K)**

| Pair | Ratios |
|---|---|
| η = 0.5 + leakage ×2 | 0.89 / 0.98 / **1.19** / 1.30 / 1.87 |
| η = 0.5 + imbalance 1.25 | 0.90 / 1.00 / 1.20 / 1.31 / 1.91 |
| Leakage ×2 + imbalance 1.25 | 0.91 / 1.00 / 1.21 / 1.33 / 1.89 |
| W-Tier 0.30 + leakage ×2 (Continuum-8: 1.10) | 0.94 / 1.04 / 1.25 / 1.39 / 2.04 |
| Median pair at ≥1,000 | 1.41 |

**Why the pair that broke Continuum-8 hurts less now.** At ω = 0.7 the W-Tier draws 228 W rather than 390 W, so doubling its pJ/bit costs less.

### 4.4 Supply and cost per unit of output (`all9.txt`, 128K)

| | ≥200 | ≥1,000 | ≥2,000 |
|---|---|---|---|
| Tokens per HBM GB against Rubin | 6.4× | 8.6× | 20.7× |
| All silicon (N2 + N4) per token against Rubin | 3.1× | 2.3× | 1.45× |
| N2 only, per token | 1.03× | 0.77× | 0.48× |
| Tok/s per BOM dollar, centre (crossed range); with 3% spares | 1.78× (1.18–2.52); 1.73× | 2.38× (1.58–3.38); 2.31× | 4.1× |

- **Per GW:** 443k packages, 0.73M HBM stacks (Rubin: 5.1M), and **77k SoIC wafer passes, i.e. 5–8 months of 2026 SoIC capacity. SoIC is the binding supply line.**

### 4.5 Site level, including prefill
Energy per prompt token at 128K: Rubin 15.8 mJ, Continuum-9 12.5 mJ, a ratio of 1.27 (about 1.15 on the same node).

| r (fresh prompt tokens per output token) | Prefill on GPUs, decode on Continuum: ≥200 / ≥1,000 / ≥2,000 | All Continuum |
|---|---|---|
| 0.25 | 1.18 / 1.51 / 2.39 | 1.23 / 1.58 / 2.47 |
| 1 | 1.11 / 1.33 / 1.92 | 1.24 / 1.48 / 2.12 |
| 4 | 1.05 / 1.13 / 1.39 | 1.25 / 1.36 / 1.66 |
| 64 | 1.00 / 1.01 / 1.03 | 1.26 / 1.27 / 1.30 |

The decode-pod gain reaches the site only if the site is decode-dominated (r ≲ 1) or Continuum also runs prefill.

## 5. All-system comparison (Continuum-9 ÷ X)

| Against | 128K (ω = 0.7) | 1M (ω = 1) |
|---|---|---|
| Rubin, trimmed | 1.22 / 1.35 / 1.63 / 1.81 / 2.67 | 1.15 / 1.15 / 1.38 / 1.94 / 3.74 |
| Rubin as shipped | 1.33 / 1.47 / 1.79 / 1.99 / 2.92 | 1.26 / … / 1.51 |
| Ultra 4-die, bottom-up, trimmed | 1.11 / 1.11 / **1.23** / 1.27 / 1.34 | **0.90** / 0.90 / 1.09 / 1.24 / 1.41 |
| Ultra 4-die, 600 kW, 100 PF, trimmed | 1.00 / 1.10 / 1.22 / 1.24 / 1.29 | 0.93 / 0.93 / 1.08 / 1.35 / 1.81 |
| Ultra 2-die (reported) | 1.30 / 1.44 / 1.74 / 1.93 / 2.84 | 1.05 / 1.16 / 1.47 / 2.05 / 3.95 |
| MI455X | 2.19 / 2.42 / 2.74 / 3.27 / 4.70 | 1.56 / 1.71 / 2.17 / 3.2 / 6.4 |
| TPU 8i | 2.41 / 2.91 / 3.85 / 4.88 / 13.5 | 1.69 / 2.14 / 3.02 / 6.2 / 26 |
| Rubin + LPX (FP8 weights) | 8.8–13 | ~14–21 |
| CS-4 | 27–31 | ~26 |

**Variants**
- **NVFP4 KV on every system:** 128K 1.25 / 1.38 / 1.57 / 1.70 / 2.35.
- **p = 0.6:** 1.20 / 1.49 / 2.81 / …. Ratios above ~3× reflect Rubin's speed ceiling, so I don't claim them.
- **Max tok/s/user:** about 5,600 for Continuum using the Continuum-8 tensor-split mapping, which is software-selectable. The EP mapping at g ≤ 14 tops out at 4,858.

**The Ultra 600 kW plus undervolt bound stays rejected.** It implies 28.9 PF/kW, which is 1.55× same-node Rubin's best (`ultra8.txt`).

## 6. Software stack and programming model
**Front end:** PyTorch (`torch.export`) and JAX (StableHLO) → MLIR → spatial schedule. Per deployment it places:
- layer types on K-pkgs or S-pkgs;
- experts and hot replicas on packages, from a routing profile;
- KV and indexer keys.

It also sets ω, V, k and m. All of this is capacity-checked offline; recompiling takes hours.

**What is no longer static:** the EP dispatch and combine inside a stage depend on routing. Packets vary in size, and the link has 1.07× headroom built in. Compute and stage hand-offs stay static. This dynamic part is why the 12 µs collectives case (1.53) matters.

**Kernels:** a tile DSL (block-matmul, softmax, gather) for CSA, HCA, the FP4 indexer and MLA.

**Serving:** a vLLM/SGLang backend with:
- continuous batching at stage boundaries;
- paged KV across HBM and SRAM;
- **asynchronous KV mirroring to host DRAM**;
- cold-spare failover in about 1.5 s;
- chunked prefill in the pipeline, or GPU prefill with KV shipped over the NIC.

**Existing models:** they convert by NVFP4 post-training quantization. The K:S package ratio is model-specific (V4: 391 K-pkgs to 319 S-pkgs). Dense-attention models need mostly K-pkgs and lose the SRAM-KV gains.

**Training and dynamic control flow** stay on GPUs.

**Maturity risk:** GPU V4 software improved 2.1–2.6× in about two months. Continuum starts from zero.

## 7. Where Continuum loses or ties
1. **Bulk tier:** 1.22× base, but 0.89–1.19 under adverse pairs. Not a defensible win.
2. **1M context at bulk against 4-die Ultra:** 0.90–0.93×. The expert-parallel change adds nothing at 1M.
3. **Site level with GPU prefill and r ≥ 4:** 1.01–1.13×.
4. **Silicon:** 2.3–3.1× Rubin's silicon per token; 77k SoIC passes per GW.
5. **Deployment unit:** 710 packages, 1.6 MW and 88k concurrent users per instance. At g ≤ 10 it is 525 packages at 1.58×. Each instance fails about every 3 days, which the KV mirror covers.
6. **Model lock-in, no training, 2028 calendar** against Feynman, which is unspecified.

## 8. What has to be true

| Assumption (base) | If wrong | ≥1,000 ratio |
|---|---|---|
| Continuum realises ≥ 62% of the GPU decode fraction | Lower | Scales directly |
| Leakage as modelled (367 W at 0.55 V) | ×2 | 1.38 |
| η = 0.6 on 22-token expert tiles | 0.5 | 1.41 |
| EP package imbalance ≤ 1.07 with 12.5% replicas | 1.15 | 1.57 |
| N2 compute energy 0.8× N3P | Same node | 1.47 |
| W-Tier at 0.15 pJ/bit | 0.30 | 1.46 |
| Per-layer collectives at 7 µs, with dynamic dispatch | 12 µs | 1.53 |
| CSA HBM at 99% fill is workable | Cap at 90% | Needs g = 14–15, about −3% (estimate) |
| The frontier stays sparse MoE with compressed attention | Dense attention | About 1.3× (KV-bound) |

## 9. Risks and physical, process and supply limits
- **SoIC:** 5–8 months of 2026 capacity per GW.
- **CoWoS-L:** ~5 reticles for the K-pkg, ~3.5 for the S-pkg.
- **HBM:** 0.73M 16-high stacks per GW; 16-high volume is unconfirmed.
- **Capacity margins:** CSA SRAM is 95% full and HBM 99% full. These are context × users bound, so admission control is mandatory.
- **Low voltage:** adaptive clocking at 0.55 V.
- **Yield:** a 750 mm² N2 die is ~47% raw, ~65% with harvesting; bonds are 98–99% each; known-good-die testing is mandatory.
- **Failure handling:** 0.17 failures per package-year. Without the KV mirror, a 710-package instance loses 2.7% of capacity to re-prefill.

## 10. Tests that could prove the design wrong

| # | Test | Tool | Kill criterion |
|---|---|---|---|
| 1 | Decode realisation against GPU decode-pool runs | LLMCompass-class event simulator with V4 traces | < 62% of the GPU decode fraction at ≥1,000 |
| 2 | **EP dispatch imbalance and link tail** at g = 13, b = 713, using real V4 routing | Trace replay + SerDes/switch simulator | Package imbalance > 1.15 or collectives > 12 µs |
| 3 | Tile η at M ≈ 22, N = 3072, NVFP4 | Timeloop/Accelergy + one-tile RTL | η < 0.5 |
| 4 | N2 V/f, leakage and energy at 0.55 V | PDK SPICE | Leakage > 1.5× model, or f < 0.55 f0 |
| 5 | W-Tier pJ/bit and static power with mixed traffic | CACTI/DESTINY + bank-conflict simulation | > 0.25 pJ/bit or > 200 W static |
| 6 | CSA SRAM/HBM fit under real context distributions | Trace replay | < 80% usable at the target user count |
| 7 | KV-mirror failover | Fault-injection simulation | Restore > 10 s or mirror > 3 GB/s per package |
| 8 | Rubin's best decode efficiency at ≥1,000 | Measurement | > 41 tok/s/W cuts the ratio below 1.45 |
| 9 | Thermal and IR drop | HotSpot/3D-ICE, PDN solver | Tj > 105 °C or IR drop > 5% |

None of these could be run here. Tests 1, 2 and 4 matter most.

## 11. Facts vs assumptions
**Facts (sourced, many secondary):**
- the chip specifications and rack figures in §2;
- the reported 2-die Ultra;
- GB200 decode measurements;
- the Llama 3 interruption counts;
- TSMC's N2P claim;
- the V4 configuration;
- packaging capacity.

**Derived by me:**
- the 0.29–0.34 GPU decode fraction;
- Rubin's 150 W trim;
- the EP link formula and D(g);
- the KV-mirror bandwidth and failure-cost arithmetic;
- the capacity figures;
- supply per GW.

**My assumptions:**
- the V/f law, τ(f), the 1.146 rule and the host rule;
- every pJ figure;
- 100 W of SRAM static power;
- 10 W per slot for mirror DRAM;
- leakage;
- η = 0.6, the 0.85 derate, imbalance 1.07/1.12;
- 5% idle power for cold spares;
- costs and yields.

**Model outputs:** every throughput, ratio and energy figure.

**Files** (in `/home/user/SomeRepository/engine/runs/refine_continuum_d/round2/`; not committed):

| File | Contents |
|---|---|
| `model9.py` | EP split, W-Tier clock ω, lanes, SRAM static, spares; imports `model8.py`, copied unchanged |
| `t1.py` | Reproduces Continuum-8's 55.2 tok/s/W |
| `sweep9.py`, `sweep9b.py` → `.txt` | ω × lanes × gmax sweep |
| `om1m.py` → `om1m.txt` | ω per deployment at 128K and 1M |
| `sens9.py` → `sens9.txt` | 14 singles × 2 contexts, 90 pairs |
| `c8pairs.py` → `c8pairs.txt` | Reproduces the check's 1.10 for Continuum-8 |
| `all9.py` → `all9.txt` | All systems, site level, supply and BOM, NVFP4 KV, p = 0.6 |
| `calib8.txt`, `ultra8.txt` | From round 1, still valid |

---

**Sources**
- [DCD: Meta Llama 3 training interruptions](https://datacenterdynamics.com/en/news/meta-report-details-hundreds-of-gpu-and-hbm3-related-interruptions-to-llama-3-training-run)
- [SDxCentral: same report](https://www.sdxcentral.com/news/meta-report-details-hundreds-of-gpu-and-hbm3-related-interruptions-to-llama-3-training-run/)
- [LMSYS GB200 Part II](https://lmsys.org/blog/2025-09-25-gb200-part-2)
- [LMSYS GB200 Part I](https://www.lmsys.org/blog/2025-06-16-gb200-part-1)
- [vLLM WideEP on GB200](https://vllm.ai/blog/2026-02-03-dsr1-gb200-part1)
- [Tom's Hardware: 2-die Rubin Ultra](https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidia-reportedly-cancels-quad-die-rubin-ultra-gpu-in-favor-of-dual-gpu-design-report-claims-complex-design-purportedly-scrapped-over-manufacturing-execution-concerns)
- [igorsLAB](https://www.igorslab.de/en/nvidia-rubin-ultra-four-die-design-dropped/)
- [hwbusters](https://hwbusters.com/news/nvidia-reportedly-cancels-quad-die-rubin-ultra-gpu-over-packaging-issues/)
- [Spheron: Vera Rubin NVL72](https://www.spheron.network/blog/nvidia-vera-rubin-nvl72-guide/)
- [DCD: Rubin Ultra at 600 kW](https://www.datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027/)
- [SemiAnalysis: Vera Rubin](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution)
- [PyTorch/SGLang: V4 on GB300](https://pytorch.org/blog/serving-deepseek-v4-on-gb300-with-sglang-5x-higher-throughput-at-the-same-interactivity-since-day-0/)
- [TSMC N2/N3](https://www.tsmc.com/english/dedicatedFoundry/technology/platform_HPC_tech_advancedTech)
- [SemiAnalysis: LP30](https://newsletter.semianalysis.com/p/nvidia-the-inference-kingdom-expands)
- [More Than Moore: LPX](https://morethanmoore.substack.com/p/nvidia-introduces-groq-lp30-and-lpx)
- [CUDO Vera Rubin](https://www.cudocompute.com/products/nvidia-vera-rubin)
- [StorageReview MI455X](https://www.storagereview.com/news/amd-mi455x-and-helios-432gb-hbm4-72-gpu-racks-and-a-real-answer-to-vera-rubin)
- [Google TPU 8](https://cloud.google.com/blog/products/compute/tpu-8t-and-tpu-8i-technical-deep-dive)
- [StorageReview CS-4](https://www.storagereview.com/news/cerebras-cs-4-three-wse-3-turbo-wafers-750-pflops-and-a-claimed-30x-over-gpu-racks)
- [arXiv DeepSeek-V4](https://arxiv.org/pdf/2606.19348)
- [Silicon Analysts HBM4 price](https://siliconanalysts.com/market/trendforce-lifts-2027-hbm-asp-forecast-to-121-hbm4-stack-seen-doubling-to-1-300-2026-10-01)
- [TrendForce SoIC](https://www.trendforce.com/news/?p=54678)
- [TSMC CoWoS 130k](https://www.financialcontent.com/article/tokenring-2026-2-5-tsmc-to-quadruple-advanced-packaging-capacity-reaching-130000-cowos-wafers-monthly-by-late-2026)