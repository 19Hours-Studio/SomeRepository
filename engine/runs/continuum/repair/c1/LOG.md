# LOG — repair c1 (one line per round)

| # | idea | change | decisive number | result |
|---|------|--------|-----------------|--------|
| 1 | I1 Continuum-D | Recomputed sizing with NVFP4 4.5 b/w (377 GB, not 335) | 1.0 GB/die needs 416 dies; 1.25 GB/die (428 mm² SRAM at N3E, 70% array eff.) → 333 dies | 333 × 800 mm² closes on area |
| 2 | I1 | BOM at N3 $19.5k/wafer, LPDDR $10/GB, no CoWoS | BOM $0.81M, 117 kW; at 3× markup $2.44M vs Rubin NVL72 $7.8M | under the $1.5M kill line (BOM) |
| 3 | I1 | Energy/token vs Rubin wide-EP | 0.19–0.20 J/tok vs 0.18 (C-D **loses ~9%**; SRAM weight reads not batch-amortised) | drop the "40× less energy" claim |
| 4 | I1 | Topology: serial pipeline → 61 layer-groups (bcast+reduce) | hop floor 233 µs → 85 µs/token; ceiling ~11.7k tok/s/user | anchor strongest at ≥1000 tok/s/user |
| 5 | I1 | $/Mtok vs Rubin, Rubin+LPX AFD, Cerebras at 32K, NVFP4 KV | ≤500 tps/user: $0.077 vs $0.087 (1.1×, parity); 1000: vs $0.214 Rubin (2.8×), $1.50 Cerebras; 2000: only C-D & Cerebras ($0.75, 10×) | WORKS in high-interactivity tier |
| 6 | I1 | KV slice replication (one die loss hits every user) | needs 32.2 GB/die at 50 tps/user → raise LPDDR to 48 GB/die (+$53k BOM) | fixed |
| 7 | I2 Expert-stationary | Recomputed capacity with N5/N3 bitcell, 2 compute dies × 4 layers | 13.7 GB/pkg, 987 GB/rack → DSV3 margin 2.6, Kimi-K2 1T margin 1.7 | capacity wound healed |
| 8 | I2 | Throughput vs competent Rubin wide-EP (weights only 5.2 GB/pkg = 0.24 ms/step) | gain 1.00–1.04× in nearly all regimes; weight energy ~1% of J/tok | original claims (1.4–1.6× J/tok, 1.6× users) FAIL |
| 9 | I2 | Search for strong regime: more weight bytes per HBM GB/s | half-HBM pkg + stack: 1.4–2.5× vs half-HBM pkg without stack at 500–750 tps | anchor value = replacing HBM BW, not adding to it |
| 10 | I2 | Repair: 4 HBM4 stacks (KV only) + SRAM layers (experts) vs Rubin 8 stacks | equal throughput for DSV3 at all tiers; Kimi-1T at realistic MFU 0.35 equal; at MFU 0.6 loses 0.61× at ≤300 tps; price ratio 0.73 (0.83 with lower HBM price) | WORKS as supply/cost play: −288 HBM4 stacks/rack |
| 11 | I1 | Long context + Ironwood comparison | 128K: 114k tok/s, $0.28 vs Rubin $0.34/Mtok; per chip C-D 1.2k vs Ironwood 4.1k vs Rubin 14.3k tok/s at 32K | C-D is many small chips; wins on $ only |
