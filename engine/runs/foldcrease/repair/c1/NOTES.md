# NOTES — repair c1

Scripts: calc/strain.py (strain in each layer), calc/crease.py + calc/study1.py + calc/contact_check.py (beam-column crease model with tension, finite differences, support-plate contact, refined until the result stopped changing), calc/budget.py (shear lag, glass fatigue, thermal, thickness, OCA locked shear), calc/study2.py (idea-2 stack), calc/cost.py.

## How the model works and how much to trust it
- The crease is treated as residual intrinsic curvature: k_r(x) = c·k_fold(x), along a teardrop path (tip radius R, necks at 3R / 35°).
- The bend zone is clamped at its edges and rests on the plate (w ≥ 0). We minimise the integral of D/2(w''−k_r)² + T/2·w'².
- The residual-set fraction phi is **calibrated**, not measured. The calibration sets an untensioned crease of 60 or 150 µm at R = 2 mm. FACT4 is the anchor for this ("good" means below 60 µm, and reviewers still see creases).
- Per layer, residual = phi·max(0, eps − eps_c). eps_c is the no-set strain. Kumoh (FACT2) gives R ≈ 5 mm, but the film thickness and temperature are unverified.
- The results that hold up are the **ratios** with and without tension, and the slope-vs-width argument. Absolute depths depend on the calibration.

## Invisibility targets (proposed)
- Depth ≤ 5 µm and maximum slope ≤ 1 mrad (0.057°), both measured to IEC 62715-6-22 / deflectometry (FACT7).
- Reflected-line distortion in the crease zone no worse than in the flat zone of the same panel.
- Off-axis luminance change ≤ 2% at 0–60°.
- Not detectable by finger: below 5 µm over a width of at least 4 mm.
- Data behind these: FACT4 only grades below 60 µm as "good". The 5 µm / 1 mrad values are my margin, and a perception study is needed to confirm them. For comparison, the leaked iPhone Fold figure is a crease angle under 2.5° (44 mrad).

## Consistency table
| limit | value used | computed over life | ok? |
|---|---|---|---|
| UTG bending stress folded, R=3 | 552 MPa | shipping UTG runs at R≈2 → 828 MPa (R assumed; Fold 7 radius is not public) | yes |
| UTG sustained tension when open | 44 MPa | needs 98–128 MPa 10 s edge strength (n = 20/15, 3 years open) | probably; edge strength unmeasured |
| gel shear when open | 1.9 kPa | gel G about 2 kPa → about 93% strain, sustained; creep allowed because the rails fix the glass position | unknown cohesion |
| tension reaching the fold | 97% (gel) / 30% (acrylic OCA) | — | gel only |
| thermal, 40 K | Ti frame 4 µm vs 95 µm stretch | ±4% T | yes (Al needs a 0.9 mm spring stroke) |
| slope target | 1 mrad | 0.82 mrad at T = 2000 N/m, 150 µm base, 2 mm clothoid | yes; fails with sharp transitions (1.4) |
| allowed untensioned-equivalent crease | ≤ about 180 µm | today's 60–150 µm class | yes; not if the 0.7 mm Fold 7 figure is real |
| idea-2 per-layer strain | ≤ eps_c(60 °C) | 25 µm at R = 4.2 → 0.30% | only if eps_c ≥ 0.30% |
| idea-2 OCA locked shear | — | acrylic 92 kPa; silicone 6 kPa; gel 0.4 kPa | needs silicone |
| spine thickness | Fold 7 8.9 mm | R = 3 → 7.8 mm (crude), R = 4.2 → 10.2 mm | idea 1 fits; idea 2 is +1.3 mm |

## Prior art for tension on opening (this weakens idea 1's novelty)
Apple EP4738056 A1 (2026, "tension assembly 44" in the flat state), US12641738, US12541230 and EP4567555. Idea 1 differs from these in three ways, none of which I found in the claims I could see:
- The UTG alone is the tendon, gripped at its outer edges.
- A gel interlayer replaces the OCA so the tension is not lost to shear.
- A clothoid ramp of at least 4·sqrt(D/T) in the hinge path.
I only saw the abstracts.
