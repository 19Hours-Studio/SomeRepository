# Critic 2 on Continuum-9 (round2)

Reproduced: all9, sens9, c8pairs, om1m, sweep9b re-run from copies in src/ -> byte-identical (out/).
90 pairs confirmed: worst at >=1000 = 1.19 (eta 0.5 + leakage x2), median 1.41, worst at >=200 = 0.89.
Hand check (out/handcheck.txt): D(13)=4.96, CSA link 8.1 us, T=22.8 us, 1,274 tok/s/user, 59.7 tok/s/W: all hold.

## Corrections
1. mHC residual hand-off omitted (V4 config hc_mult=4). Stage boundary carries 4 x hid, BF16 = 8x the modelled 1 B x hid.
   Rubin unaffected (residual local). out/handoff.txt, out/handoff2.txt:
   64 lanes: 1.63 -> 1.46 at >=1000. Re-optimised 88 lanes: 1.19/1.31/1.59/1.76/2.59 vs Rubin; 1.08/1.08/1.20/1.23/1.30 vs 4-die Ultra.
   Worst pair (96 lanes) 1.15 at >=1000, 0.86 at >=200; vs Ultra the worst pair is 0.87 at >=1000.
   1M (omega 1, 96 lanes): 1.33 at >=1000 vs Rubin (answer 1.38), 0.87 vs Ultra at bulk (answer 0.90).
2. Failure cost is 1000x overstated: re-prefill of 6.8k users x 128K = 8.9e8 tok x 12.5 mJ = 11 MJ = 6.9 s of pod, not 1.9 h;
   0.0027%/yr, not 2.7%. The KV mirror (10 W = 0.44%) is not needed; drop it (+0.4%).
3. "1.62x holds only if Continuum realises >= 62% of GPU fraction" is wrong: 62% gives parity (1/1.63 = 0.61). 1.6x needs the same fraction.
4. Undersell: HBM "99.4% full" is 99.4% of a 90% cap (89.5% physical); SRAM "95%" is 86% physical. The section-8 "cap at 90% -> -3%" row double-counts.
5. Minor: section 3.1 lists 120 W host but the model and slot formula use 110 W; "1.15 x hid" is 1.21 x hid with the 1.07 imbalance (link time 8.1 us is right).
6. Feynman is not "unspecified": GTC 2026 reports 3D-stacked logic + custom HBM (2028), i.e. Continuum's own lever; same-date margin is at risk.

## Lever
Fixed per-layer collective latency 7 -> 4 us (static point-to-point fabric): 1.59 -> 1.64 at >=1000, 1.76 -> 1.95 and 2.59 -> 2.88 at >=1500/2000 (out/tau.txt). Saturates below 4 us. Unproven; it belongs in test 2.

Supported headline: ~1.6x Rubin (1.59), ~1.2x 4-die Ultra at >=1000 tok/s/user, 128K, decode tok/s per provisioned W, model output only.
