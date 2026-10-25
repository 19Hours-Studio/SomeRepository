# Critique of Continuum-8 (refine_continuum_d/round1)

Ratio = Continuum-8 output tok/s per provisioned W ÷ best Rubin (trimmed 150 W) at the same tok/s/user floor; 128K, p = 0.8 unless noted.

## 1. Re-runs
- run8, calib8, site8, supply8, ultra8, fp4kv8 (128K, 1M), t0: byte-identical (`rerun/`). sens8: all 64 lines of the author's file byte-identical; my complete run adds the two NVFP4-KV rows the author's run was cut off before, and they match fp4kv8_*.txt.
- §4.1 hand check re-derived with no model imports (`scripts/hand.py`): c = 10.94 / 10.20 µs, T = 22.66 µs, 1,281 tok/s/user, slots 2,450 / 2,175 W, average 2,332 W, 55.2 tok/s/W, 13.15 GB indexer keys, 118.8 / 129.6 GB HBM. All hold.
- Link model checked: (g−1)/g·hid + 2·hid equals all-gather (FP8) + BF16 reduce-scatter + forward per package, (3g−1)/g·hid. Consistent.

## 2. Unfair / unsupported
| # | Point | Number changed |
|---|---|---|
| U1 | "Worst tested pair 1.21": the two worst singles were never paired | W-Tier 0.30 + leakage ×2: 1.51 → **1.10** (1M: 1.02); W-Tier 0.30 + η 0.5: 1.13; W-Tier 0.30 + same node: 1.16; triple: 1.03 (1M 0.98). At ≥200 pairs give 0.82–0.87 |
| U2 | Calibration at 34–70 tok/s/user, then applied at ≥200–≥1,000 | Measured GB300 falls 0.038 → 0.013 of model (V4, 93 → 133 tok/s/user) and 0.18 → 0.006 (R1, 88 → 235); the model is flat. Model GB300 max 3.4–4.1k tok/s/user against ~235–250 measured. Break-even thresholds 0.19–0.30 are unanchored; Rubin's 1,110 tok/s/user point is 4–5× past any measured GPU on this model class (`shape.txt`) |
| U3 | Headline against a 2026 N3P part for a 2028 N2 chip | Same date, bottom-up Ultra 4-die: 1.14 at ≥1,000; same node vs Rubin: 1.36; Feynman unmodelled |
| U4 | Spares (~3%) excluded | 1.51 → 1.46; 1.13 → 1.10 |
| U5 | W-Tier 25 Mb/mm² averaged over a 750 mm² die = 79% of N5/N3E HD macro density (31.8) | At 16 Mb/mm² (11.8 GB): 1.42 at 128K, 1.21 at 1M; the indexer-in-SRAM lever is lost (CSA back to 4 stacks) |

## 3. Undersold
| # | Point | Number |
|---|---|---|
| S1 | "All silicon 3.2× / 2.4×" leaves out the HBM DRAM and base dies | Including them (~1.2 cm² per die): **0.52× / 0.39× / 0.22×** of Rubin per token |
| S2 | Intermediate-dim split balances load across packages | Imbalance 1.00: 1.13 → 1.16, 1.51 → 1.56 |
| S3 | 2-die Ultra reported at 192 GB, not 512 | 128K 1.33 / 1.61; 1M 1.51 / 1.66 (vs 1.07 / 1.49) |
| S4 | If measured GPU high-interactivity collapse is structural, the ≥66% realisation bar is far too demanding | Unquantified; needs measurement |

## 4. Where a larger honest gain lies
The regime, not a design change: ≥1,000 tok/s/user decode on frontier MoE with r ≲ 0.25. No GPU has been measured there, and SRAM dataflow machines have demonstrated it. The decisive experiment is a measured GPU tok/s/W at ≥500 tok/s/user on V4-Pro, run with a decode-realisation simulation of the Continuum pipeline at the same speed.
