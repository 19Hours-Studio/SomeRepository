# improve_g2 answers (scripts: i1_admission.py, i2_fallback.py, i3_regime.py; outputs *.out)

IDEA 1 — popularity-first order + second-sighting admission + per-regime TTL
- Never-loses: 1.01–1.24x (Zipf 1.05), 1.19–1.44x (1.2), 1.46–1.83x (1.5) over W=10..1000 req/5min.
- The old always-write rule lost money (0.88–0.97x) at low traffic; 1.5x now reached at Zipf 1.5 from W~100 (1.66x).

IDEA 2 — probe-routed blending with popularity-ordered exact fallback
- At m=0.25: 1.46/1.50/1.55x vs plain APC (old 1.39x); max m for 1.5x 0.19/0.24/0.46 (old 0.12).
- Against APC + popularity order, blending adds only 1.25/1.19/1.08x.

IDEA 3 — per-session TTL switch from return hazard
- Choose 1h TTL when s > s* = 0.75n/(1.15P), otherwise 5m with hazard-gated pings.
- Gain over the best static choice is 1.0–1.5x; on the Mooncake traces the ceiling is 1.07–1.10x.
