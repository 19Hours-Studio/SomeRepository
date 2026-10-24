# NOTES — repair c1 (scripts: model.py, systems.py, systems2.py, energy.py)

## Sources (SRC) used
- DeepSeek-V3/V3.2 config: 61 layers, 256 experts top-8, expert FF 2048, MLA 576-dim latent, V3.2 FP8 cache 656 B/token/layer, indexer 128-dim FP8, top-k 2048.
- HBM4 2.75 TB/s/stack (FACT 15), $550–600 (2026) / $1,300 (2027) per 36 GB stack (FACT 18).
- LPDDR $10/GB, LTAs up to $21/GB (FACT 1/20); LPDDR5X 3.6 pJ/b system (FACT 5, Vera 1.2 TB/s).
- N3E bitcell 31.8 Mib/mm² (FACT 9); AMD V-Cache 64 MB / 36 mm² (FACT 4).
- VR NVL72 ≈ $7.8M (Morgan Stanley via digitalcitizen/guru3d; range $5–9.1M).
- Groq 3 LPX: 256 LP30/rack, 500 MB SRAM, 1.2 PF FP8, 128 GB/rack (The Register, StorageReview, Counterpoint, Mar 2026); attention on Rubin, FFN on LPX (Nvidia dev blog, ABI).
- d-Matrix Corsair 2 GB SRAM + 256 GB LPDDR5(X), 400 GB/s per card (The Register, Chips and Cheese); Raptor 3D-DRAM 32 GB, >100 TB/s (Hot Chips 2026).
- MatX One: SRAM weights + HBM KV (SiliconANGLE Feb 2026).
- N3 wafer ~$19.5k, N2 ~$30k (Silicon Analysts).
- ESS latent offload to CPU memory (FACT 22).

## Main estimates (EST)
BW eff 0.6, FLOP eff 0.45 for all systems; 4-yr amortization, 70% utilization, $0.08/kWh, PUE 1.25; Rubin FP8 dense 17.5 PF; VR rack 190 kW; GPU wide-EP decode floor 2.5 ms/step; LPX rack $3.5M/130 kW; SRAM macro efficiency 55%; LPDDR6 128 GB/s per x96 package, 8 GB min package; die board/system share $1,200.

## Key insight (Idea 1): memory drain-time matching
Required drain time τ = KV footprint / (KV bytes read per token × tok/s/user).
Dense MLA: τ = 1/(tok/s) = 10 ms @100 tok/s → HBM (13 ms) is the matched pool.
DSA 128K: τ = 55 ms @100 tok/s → LPDDR (62 ms) is the matched pool; HBM strands bandwidth or runs out of capacity.

## Consistency table — Idea 1 (Continuum-D)
| limit | value relied on | check | ok? |
|---|---|---|---|
| reticle 858 mm² | die 800 mm²: SRAM 436 + compute ~180 (2.8 TF/mm², B200-class) + LPDDR PHY ~60 + SerDes ~40 + NoC 60 = 776 | ≤800 | ok (tight) |
| SRAM per die 1 GiB | 36 experts × 24.8 MB = 893 MB + MLA layer weights FP4 105 MB = 998 MB | ≤1074 MB | ok (7% headroom) |
| LPDDR capacity 64 GB/die | 128K DSA: 6.3 GB/user; 10.2 users/die capacity vs 5.3 (100 tok/s) / 2.6 (200 tok/s) bandwidth limit | cap ≥ need | ok; binds at ≤50 tok/s |
| LPDDR BW 1 TB/s/die | Vera does 1.2 TB/s per package (SRC) | precedent exists, not on an accelerator die | OPEN |
| compute 510 TF FP8/die | 128K DSA 240 GFLOP/token; flop limit 4.8 users vs bw 2.6 @200 tok/s | flop > bw limit | ok; dense 32K is flop-bound (3.6 < 4.6) |
| C2C bandwidth | MoE dispatch+combine 172 KB/token/layer → 42 GB/s per stage, ~5 GB/s per die at 247k tok/s | ≪ 100 GB/s link | ok |
| latency floor | 61 stages × 6 µs + 0.1 ms ≈ 0.47 ms → ≤2,100 tok/s/user | SLA 1000 | ok (EST hop 1 µs) |
| power density | 111–300 W / 800 mm² = 0.14–0.38 W/mm² | < B200 ~0.6 | ok |
| prefill ingress | 124 req/s × 6.3 GB = 780 GB/s ≈ 1.5 GB/s/die | ≪ LPDDR write BW | ok; prefill is off-system |
| failures | ~2%/yr/die (EST, no HBM; FACT 19 is 9.1% with HBM) × 527 ≈ 10/yr; 1 spare/stage, 1 GB reload ~20 ms | 2-in-stage risk negligible | ok, KV of 1/8 of users per failure re-prefilled |
| LPDDR supply/price | 33.7 TB/system; $21/GB → +18% $/Mtok | still 1.13x vs VR | wounded |

## Consistency table — Idea 2 (stacked SRAM)
| limit | value | check | ok? |
|---|---|---|---|
| capacity | 3-high×144 dies = 790 GB vs K2 experts 568 GB (1.38), V3 368 GB (2.15) | >1.2 | ok (was 0.96) |
| node capacity | 4-high×16 dies = 117 GB vs gpt-oss-120b 63 GB (1.86); Qwen3-235B experts 128 GB → 0.92 | | ok for ≤120B only |
| power delivery | ~900 W/die at 0.75 V ≈ 1,200 A through 3–4 SRAM layers; ~24k power TSVs at 50 mA, ~5 mm² keep-out | IR drop ~mV | plausible, needs PDN sim |
| SRAM leakage | 14.6 GB/GPU at 0.3–1 W/64 MB = 70–230 W/GPU (4–13% of 1.8 kW) | | hazard; power-gate idle banks |
| thermal | compute die on top next to the cold plate (Zen 5 X3D ordering); SRAM ≤105 °C | | needs thermal sim |
| rack gain bar 1.5x | 1.19x (V3) / 1.33x (K2) at 2.5 ms | FAIL | rack scale fails |

## Cost per delivered Mtok (decode), best baselines
Idea 1 @128K DSA, 200 tok/s/user: Continuum-D $0.095 ($0.112 at $21/GB LPDDR); best VR NVL72 (HBM-only or ESS offload) $0.127; LPX+VR $0.276 (LPX price EST). At dense 32K: $0.138 vs $0.135–0.157 (parity). At 1000 tok/s/user: GPUs can't reach it (floor). The LPX+VR rate is $0.276 at this point, though LPX+VR is in principle able to.
Idea 2 node (gpt-oss-120b, 8 GPUs): base $0.024→0.032 @500–800 tok/s (8K) vs stacked $0.017 → 1.39–1.86x; versus spreading the same model over EP72 on an NVL72, the gain is only 1.06x.
