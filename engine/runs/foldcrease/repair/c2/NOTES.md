# NOTES (repair c2). Scripts: calc/idea1.py, calc/idea1_r3.py, calc/idea2.py

## Sources
- OCA folding shear 250-400% typ. (NAFEMS NWC23 0431; Samsung Display paper, quoted via search); 3M whitepaper >300% (FACT 9)
- OCA 40-50% stress relaxation at 60 C (FACT 1, US11334117)
- CPI: no residual set at R~5 mm, recovery ~log t (FACT 2, koreascience JAKO202102455512209)
- Perceptual: <60 um "good" (FACT 4); IEC 62715-6-22:2026 and deflectometry (FACT 7)
- Oppo N6: 0.05 mm is hinge-surface variance, crease still visible (FACT 8; GSMArena, TechAdvisor reviews)
- Apple: about 1/4 of Fold 7 depth, laser-drilled plate (FACT 6), patent US11644873 (FACT 10)
- Tension hinges: US12641738, EP4738056A1, EP4567555A2
- BOM: Fold5 inner display $122 (TechInsights via Counterpoint); Fold4 BOM ~$670; Fold SE $790 (UBS)
- Material constants used: UTG E=72 GPa (aluminosilicate, textbook); PI 6-8 GPa; PDMS volumetric CTE 9.6e-4/K; phenyl-methyl silicone n 1.49-1.53 (NuSil/Dow datasheets: 1.46-1.52 index-matching gels)

## Consistency tables (each computed rate vs its window)
Idea 1
| quantity | value | window | ok |
|---|---|---|---|
| UTG bend strain R=3 mm | 0.50% (360 MPa) | < today's ~1% at R 1.5 mm | yes |
| panel own-NA strain | 0.50% | CPI no-set threshold ~0.5% (FACT 2) | marginal |
| edge slip | 149 um per edge | PI-loop seal force 1e-4..0.1 N/m < UTG Euler 0.34 N/m | yes |
| fold drag (mu 0.1, 0.5 s) | 0.09-0.19 N/m | dynamic squeeze foundation N_c ~1e5 N/m | yes |
| leveling 9.4 mm | 5-10 s | "invisible when viewed" | transient caveat |
| gravity wedge | <=0.27 mrad | 0.5 mrad target | yes |
| thermal 60 K | 1.2 um dome over 140 mm (0.07 mrad) | 0.5 mrad | yes |
| interface reflectance | <1e-4 (n matched +-0.02) | invisible vs 4% first surface | yes |
| stylus bottom-out | 0.7% UTG strain (2 N) | same as today's soft-OCA stack | equal |
| polymer coat on UTG | 5 um coat -> 10 um crease | must be 0 | design: no film |
Idea 2
| quantity | value | window | ok |
|---|---|---|---|
| T needed R=1.5 mm | 9.6-56 kN/m | glass/frame | no -> radius raised |
| T design R=5 mm | 1000 N/m -> f<=2.5-3.7% | measured f unknown | decides |
| UTG membrane strain | 0.04% | << 0.3% bend strain | yes |
| OCA shear (view area) | 9.4 kPa | 10.5 kPa creep-test | thin margin |
| thermal swing | +-2% Ti / +-8% Al (1 mm spring) | <=10% | yes |
| hinge force/work | 150 N, 0.1 J/cycle | in-plane midframe; over-center toggle | ok |
| spine thickness | ~11.8 mm (R=5), ~9.8 mm (R=4) | Fold 7 8.9 mm | trade-off |
