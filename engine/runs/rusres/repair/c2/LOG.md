# LOG — repair c2 (scripts in calc/)

| round | idea | change | decisive number | result |
|---|---|---|---|---|
| 1 | I1 thermosyphon triage | Reproduced the kill test: whole-chain cost per t Ni-eq | Programme $3–17M/yr = 0.04–0.20% of $8.1bn full cost ($9,124/t Ni-eq) | Kill test confirmed on measure (a) |
| 2 | I1 | Made the freezing-index cutoff a number: cooling margin M = winter extraction / annual heat load per unit (idea1.py) | M in 2050 (+2.5 K winter): Norilsk 1.53, Udachny 2.10, Pevek 1.57, Salekhard 1.05, Nadym 0.88, Fairbanks 0.90, Beiluhe 0.41 | Cutoff M≥1.5 keeps Norilsk, Yakutia diamonds and Pevek and drops Yamal South, TAPS and the Qinghai–Tibet line, which matches the observed fade (F320–321) |
| 3 | I1 | Sensitivity to R (0.08–0.2 K/W) and lateral heat gain (5–30 W) (idea1b.py) | Norilsk 2050 M ranges 0.68–3.01; at R≥0.2 the Norilsk margin is lost | Deciding unknown is R in saline Norilsk loam, measured in the pilot |
| 4 | I1 | Moved the value from measure (a) to (c) plus tail risk. Added the cheapest baseline as triage step 0: fix crawlspace ventilation and utility leaks | Triaged $64M vs blanket $198M vs underpinning $196–392M. Expected thaw-share loss $26–86M/yr vs programme $6–10M/yr | NICHE: B/C ~3–9, cost per t moves by <0.2% |
| 5 | I2 XRT shaft-bottom | Reproduced the kill test with fines bypass (65% sortable) (idea2.py) | Unconstrained case: break-even metal loss at 15% rejection is 0.08–0.42%, against a measured ~2% | Kill test confirmed when the concentrator is not the bottleneck |
| 6 | I2 | Changed the regime to deep mines where the shaft is the bottleneck (Skalisty-type, 2.1 km shafts) | Metal per year from a fixed shaft rises ×1.095 (Selebi) to ×1.36 (stringer). Metal NPV ×1.085–1.31 after counting the lost tail metal | Works only where the hoist binds |
| 7 | I2 | Baseline is a new deep shaft for the same extra metal (idea2c.py) | Marginal $/t Ni-eq: sorting $5.0–8.3k vs new shaft $6.7–12.6k, ratio 1.21–1.81. Mine-level average cost ratio is only 1.003–1.06 | NICHE/WORKS in the hoist-bound regime; FAILS on disseminated ore (RAV4W: 23% rejection with 16% loss) |
| 8 | I2 | Consistency checks: backfill void balance and sorter count | Rejects ≤0.41 t/t ROM vs fill capacity 0.44–0.67 t/t. Needs 2–3 × 150 t/h units | Passes. At massive ore (density 4.5) the margin is thin (0.41 vs 0.44) |
