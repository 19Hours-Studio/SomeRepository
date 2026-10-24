# NOTES — repair c1

Code: `model.py` (I1 + I2 rounds 1–2), `round3_idea2.py`, `round4_idea2.py`, `round5_idea1.py`. [S] = sourced, [E] = own estimate.

## Shared workload / metrics
DeepSeek-V3-class MLA MoE: 671B total / 37B active, 61 layers, 128 heads, KV = 576 elements/token/layer [S, public config].
NVFP4 weights at 4.5 b/w → 377 GB. KV at 32K: 1.15 GB FP8, 0.65 GB NVFP4. Metrics: tok/s per system at a given tok/s/user, $/Mtok (4 yr, 70% util, $0.10/kWh, PUE 1.3), J/token.

## Sources used
- N3 wafer price ~$19.5k (range $17–22k): siliconanalysts.com/guide/tsmc-3nm-cost; N2 ~$30k: tech-insider.org
- N3E SRAM 31.8 Mib/mm² (FACT 9); V-Cache 64 MB/36 mm² (FACT 4)
- LPDDR $10/GB, range $7.8–21 (FACT 1); Vera 1.2 TB/s LPDDR5X at ~3.6 pJ/b (FACT 5); LPDDR6 38.4 GB/s per x24 at 14.4 Gb/s (SK hynix ISSCC 2026, via guru3d / 36kr)
- HBM3e 3.44 pJ/b (FACT 6; 5.74 alternative)
- Rubin: 288 GB, 22 TB/s (The Register 2026-03-19, FACT 15); VR NVL72 rack $7.8M, memory 26% (Morgan Stanley via digitalcitizen.life); range $5–9.1M
- Groq 3 LPX: 500 MB SRAM/LPU, 150 TB/s, 256 LPU/rack, attention stays on Rubin GPUs (The Register, storagereview, SemiAnalysis)
- d-Matrix Corsair: 2 GB SRAM + 256 GB LPDDR5 per card, 8 chiplets × 2 × 32-bit LPDDR5-6400 (~410 GB/s) (ascii.jp, aiwiki); Raptor 3D DRAM 0.37 pJ/b (hwbusters)
- Cerebras WSE-3 44 GB, CS-3 ~23 kW [S]; price $2.5M/system [E]
- Ironwood 192 GB, 7.37 TB/s, 4.6 PF FP8 [S Google]
- Feynman "LPU stacked on GPU" report: naddod.com (single secondary source, unconfirmed)
- Not verified: LPX rack price ($4M assumed), FP8 dense of Rubin (16 PF assumed), a2a latency (2–5 µs swept; DeepEP figures could not be retrieved)

## Idea 1 — consistency table (333 dies, 1.25 GB SRAM + 48 GB LPDDR6 @ 1 TB/s each)
| limit | value relied on | computed | ok? |
|---|---|---|---|
| reticle ~858 mm² | 800 mm² die | 428 SRAM + 262 logic + 110 PHY/SerDes | ✓ |
| SRAM capacity | 377 GB + 10% | 416 GB → margin 1.10 | ✓ (thin) |
| LPDDR BW/die | 1 TB/s = 26 LPDDR6 x24 ch | KV-bound 514k vs compute-bound 414k tok/s at 32K | ✓ compute binds |
| shoreline | 113 mm perimeter | ~42 mm LPDDR + ~38 mm SerDes [E] | ✓ (needs a floorplan) |
| LPDDR capacity | 48 GB | 32.2 GB with KV replication at 50 tps/user | ✓ |
| power | 350 W/die budget | ~236 W dynamic at 414k tok/s | ✓ 0.44 W/mm² |
| latency | 1 ms/token at 1000 tps | hop floor 85 µs (122 hops × 0.7 µs) | ✓ |
| MTBF | 2000 FIT/node [E] | 1500 h/instance; reload 0.1 s; N+k spares | ✓ with replication |
| supply | 0 HBM, 0 CoWoS | 16 TB LPDDR/system (LPDDR is tight, FACT 10) | ⚠ |

## Idea 2 — consistency table (repaired: 2 compute dies, 2–4 SRAM layers/die under compute, 4 HBM4 stacks)
| limit | value | computed | ok? |
|---|---|---|---|
| capacity | 6.9 GB/die at 4 layers | DSV3 needs 2.6 GB/die (2 layers); Kimi-K2 1T needs 4.05 GB/die (3 layers) | ✓ |
| HBM capacity for KV | 144 GB | 1T at 300 tps: 87 users × 0.65 GB = 56 GB | ✓ |
| HBM BW | 11 TB/s, KV only | equal to Rubin 8-stack at realistic MFU 0.35 | ✓; loses 0.61× at MFU 0.6, 1T, ≤300 tps |
| thermal | compute on top (Zen 5 X3D orientation) | SRAM leakage 0.8–4 W, reads ~1.6 W | ✓ |
| power delivery | ~1.2 W/mm², ~1200 A/die through 2–4 TSV layers | unmodelled | ⚠ needs silicon |
| stacked yield | 0.97 per bond × 8 | 0.78; included in $4.3k/pkg | ⚠ |
| supply | SoIC capacity | adds SoIC, removes 288 HBM4 stacks/rack | ⚠ swaps one bottleneck for a smaller one |
