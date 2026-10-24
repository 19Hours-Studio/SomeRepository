# NOTES — repair c2

Scripts: idea1_tiered_kv.py, idea1_round2.py, idea1_hitsweep.py, idea2_prefill.py, idea2_round2.py (all python3, no deps).

## Idea 1 — consistency table (128K ctx, 100 tok/s/user, DeepSeek-V3.2 NVFP4, 72-way weight shard)
| limit relied on | value used | demand computed | ok? |
|---|---|---|---|
| HBM4 capacity, usable 90% of 4x36 GB | 129.6 GB | 74 users x (1.055 idx + 0.16 hot buffer) + 5.2 wts = 95 GB | yes |
| HBM4 BW at 80% eff (4 x 2.75 TB/s) | 8.8 TB/s | 74 x 106 GB/s idx + hot hits + 0.52 TB/s wts = 8.8 TB/s | binding |
| LPDDR6 capacity | 512 GB | 388 GB | yes |
| LPDDR6 gather BW (0.7 TB/s peak x 0.5 eff) | 0.35 TB/s | 74 x 8.2 GB/s x 0.13 miss = 79 GB/s | yes; holds down to hit ~0.4 |
| per-layer latency budget (10 ms / 61) | 164 us | miss gather 36.8 us/layer (needs 2-batch overlap) | yes |
| compute | ~1/4 Rubin | 1.78 PF needed | yes |
| LPDDR6 bank parallelism for 656 B | 16 banks | 1.8 in flight to hide tRC (60 ns assumed) | yes (on paper) |

## Idea 2 — consistency table (2-die package, 35 PF dense FP4, 16 LPDDR6 modules 2.8 TB/s, 2 x 1.45 GB SoIC SRAM)
| limit | value | demand | ok? |
|---|---|---|---|
| ridge | 12,500 FLOP/B per die | MoE act stream fixed ~4,096 -> must keep token tile on-die | design response |
| SRAM token tile | >=0.75 GB/die (128K), >=1.0 GB (32K) | 1.45 GB | yes |
| tokens per pass | >=64K | pass latency 0.95-1.9 s | only throughput tier |
| LPDDR capacity | 512 GB | 377 GB weights + 1.9 GB spill | yes |
| LPDDR BW | 2.8 TB/s | 10 MB/token x 76.5k tok/s = 0.77 TB/s | yes |
| network | none for MoE (full replica) | KV handoff 1.8 GB/s/die | yes |
| power | ~1.8 kW liquid (assumed = Rubin compute share) | — | not air-coolable |
| LPDDR beachfront | 16 SOCAMM-class modules (2x Vera's 8) | — | tight, unverified |

Sources: see final answer.
