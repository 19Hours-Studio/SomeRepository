# LOG — continuum_r2 repair c1
| round | idea | change | decisive number | result |
|---|---|---|---|---|
| 0 | both | prior-art search | MatX One = SRAM weights + HBM KV; d-Matrix Corsair = 2 GB SRAM + 256 GB LPDDR/card (weights stream from LPDDR at 400 GB/s); Nvidia LPX(256x500 MB SRAM)+VR NVL72 = attention/FFN split | both anchors sit next to known systems; novelty must come from regime and placement |
| 1 | 1 | recompute SRAM area with macro efficiency | 1 GB = 436 mm2 at 55% of N3E bitcell density (claim used raw bitcell: 258 mm2) → 36 experts/die, 8+1 dies per MoE stage, 527 dies (not 340) | capex still $1.44M (<$1.5M bar), die cost $601 |
| 2 | 1 | memory economics | HBM4 $209/TB/s (2026) vs LPDDR $625–1312/TB/s; drain time HBM 13 ms, LPDDR 62 ms | LPDDR is NOT cheaper per bandwidth; it is cheaper per GB → anchor only wins where KV needs capacity more than bandwidth |
| 3 | 1 | dense-MLA 32K vs best VR | $0.138 vs $0.135–0.157/Mtok | parity → dense-attention target FAILS to differentiate |
| 4 | 1 | retarget to sparse-attention (DSA) long context; required drain time 55 ms ≈ LPDDR 62 ms | 128K DSA: $0.095 vs best VR (HBM or ESS offload) $0.127–0.136 → 1.34–1.44x; vs LPX+VR (est price) 2.9x; only option ≥1000 tok/s/user (GPU floor) | WORKS in this regime (NICHE-to-WORKS) |
| 5 | 1 | sensitivity | LPDDR 0.7 TB/s → $0.136 (parity); 1.5 TB/s → $0.063; LP $21/GB → $0.112 | deciding unknown = LPDDR TB/s per organic-packaged die |
| 6 | 1 | energy | 111 W/die bottom-up → 0.34 J/tok vs VR 0.37 J/tok; at 300 W budget 0.92 J/tok | J/token parity at best, loses 2.5x if power budget real |
| 7 | 2 | recompute capacity on 2-die Rubin-class packages, N5 SRAM die 2.29 MB/mm2 | 3-high: 790 GB/rack, margin V3 2.15, K2 1.38 (was 0.96) | capacity repaired |
| 8 | 2 | rack-scale gain = T/(T − W/(N·BW)) | weight read/step 0.40 ms (V3) / 0.62 ms (K2) → 1.19x / 1.33x at 2.5 ms floor | rack scale FAILS 1.5x bar (confirms kill test) |
| 9 | 2 | move to regime where W/N is large: 8-GPU node, ≤120B MoE (gpt-oss-120b), 4-high = 117 GB | gain 1.39x @500, 1.86x @800 tok/s/user; baseline cannot reach 1000 (floor); +$24k on $0.95M node | NICHE: works only where no NVL72-scale domain (vs EP72 gain 1.06x) |
