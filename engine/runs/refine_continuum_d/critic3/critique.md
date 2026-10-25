# Critic 3 on Continuum-10 (round3)

Metric: Continuum tok/s per provisioned W divided by best Rubin (trimmed 150 W); 128K unless stated; tiers >=200/500/1000/1500/2000.

## 1. Re-runs
- hand10, all10, feyn10, sweep10, tau10: byte-identical (re_*.txt). Sens10: the first 9 lines match; worst pair (eta 0.5 + leak x2 -> 1.17 / Ultra 0.88) and 1M eta 0.5 (1.17/1.40, Ultra 0.92/1.11) re-run and match (worst.txt).
- hand_indep.py (no model imports) reproduces: SRAM 11.74/16.56 GB, HBM 85.0/86.4 GB, CSA 6.70/8.99/13.66/8.72 us, ho 4.83, c_pair 24.13, T 48.3, 1,165 tok/s/user, 60.0 tok/s/W -> 1.64.
- round3/t10.txt is stale; a re-run gives the answer's own table (64 lanes 1.23/1.37/1.65/1.80/2.69). The prose is correct; the file is not.
- "Rubin needs about 4.5M stacks per GW-equivalent" is inconsistent. At the model's own Rubin operating slot (1,562 W, 57.1k tok/s/GPU), it is ~1.05M GPUs = ~8.4M stacks. 4.5M uses 2.9 kW per slot. The 7.5x per-GB ratio is right.

## 2. What drives 1.64 (decomp.txt, rubin_pts.txt)
Both systems are compute-bound at 0.55 V. 1.64 is roughly 1.19 (assumed N2 vs N3P compute energy) x 1.34 (Rubin needs k=4 drafts, i.e. 1.49 positions per token, to reach 1,000 tok/s/user; Continuum needs k=1, i.e. 1.11) x ~1.03. At >=2000 Rubin is also per-layer-latency-bound (m=1, T/c = 1.6).

## 3. Points that change numbers (>=1000 unless stated)
| Point | Direction | Effect |
|---|---|---|
| Zero-skip x1.43 assumed for Continuum; Rubin's 50 PF is "adaptive compression", not zero-skip | oversell risk, untested | Continuum-only s=1: 1.64 -> 1.34 (Ultra 1.24 -> 1.01; >=200 1.07). Both s=1: 1.57 |
| 30 W "switch plane" vs switch-side SerDes ~ package SerDes (162 W) | oversell | +130 W/slot: 1.55 (1M 1.57; Ultra 1.17) |
| Continuum leakage 0.167 W/mm2 (N2) vs Rubin 0.091 W/mm2 (N3P), same compute density | undersell | at parity: 1.78 (Ultra 1.35) |
| HBM4 80 W/stack | undersell (moderate) | 50 W: 1.69 |
| omega is a runtime clock, so it can be picked per tier | undersell | omega 0.5 at >=1000: 1.70 |
| Same-date framing: §7 says Continuum is 2028, yet Ultra (2H27) is called "same-date" | oversell of headline | 2028 peer = Feynman proxy: 1.13 (A16 both), 1.02 with cHBM |
| Rubin given unpublished 0.55 V points (slot 1,562 W) | conservative | Rubin limited to vendor points: 1.82; floor 0.65 V: 1.74 |
| Geometric p=0.8 to k=6 favours GPUs (Rubin uses k=4-6) | conservative | k<=2 both: 2.05; p=0.7: 1.94 |
| SRAM 18.4 GB in 8 tiers ~ 24.5 Mb/mm2 on N4, ~1.5x V-cache density scaled | risk | 13.5 GB: 128K 1.64 unchanged (>=200 1.23); 1M 1.66 -> 1.54, Ultra 1.31 -> 1.22 |
| Layer order | supported | secondary source: Pro layers 0-1 HCA, then CSA/HCA interleaved; HCA->CSA pairs give 30 pairs + 1 HCA, as modelled |

Adjusted base (switch +130 W, leakage parity, HBM 50 W, best omega per tier; adj.txt):
128K 1.37/1.52/1.79/2.03/3.02 (Ultra 1.26/1.26/1.35/1.42/1.51); 1M 1.52/1.52/1.81/2.55/4.88.
The same with zero-skip lost: 128K 1.19/1.31/1.45/1.69/2.51 (Ultra 1.08/1.08/1.09/1.18/1.26).

## 4. Larger honest gain
- Regime: >=1500-2000 tok/s/user and 1M context, where Rubin is latency- and draft-bound (Ultra 1.34-1.45 at 128K, 1.49-1.69 at 1M; worst pair against Ultra at >=2000 is still 1.04).
- Design: the CSA layer is compute-bound, and about half of its compute is attention plus the FP4 indexer (604 + 537 of 2,298 MFLOP-eq per position). Possible fixes: a dedicated low-precision indexer/attention datapath, or activity-proportional W-tier power (x0.62 gives 1.86 adjusted).
- The zero-skip question has to be settled (test: NVFP4 V4-Pro weight zero fraction plus tile RTL) before any of this counts.
