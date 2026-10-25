# Notes (scripts in calc/: idea1.py, idea2.py, idea2_thermal.py)
## Consistency table - Idea 1
| limit | value used | computed | ok |
|---|---|---|---|
| UTG surface CS (Corning US9321679: >=700 MPa, R 3-10 mm) | 700 MPa | 514 MPa bend (50 um, R 3.5) | yes, 1.36x |
| CPI zero-residual strain (Korean CPI study: R_crit ~5 mm; film thickness unverified) | ~0.5% | OLED 0.36% | assumed |
| reservoir groove width | 500 um | slip 112 um + thermal 61 um = 173 um | yes, 2.9x |
| capillary clamp vs set lift <=0.3 um | 14 kPa | f<=10% gives 0.21 um | if f<=10% |
| wing coplanarity | 0.02 deg / 3.5 um | stop wear 1 nm | requires trim |
| plate clearance vs plate tolerance | 20 um | Oppo plates 50 um (too loose) -> needs <=+-10 um | tighten |
| fold drag vs sandwich constraint | 3 um gap | 1.2-6 N/m, 4 s buckle time | test cold |
| gravity sag | <1 um | 0.32 um | yes |
| Fresnel at fluid/UTG | <0.01% | 0.004% | yes; dewet air 4.1% = failure mode |
## Consistency table - Idea 2
| limit | value | computed | ok |
| glass sustained tension | <=~70 MPa (net compressive with 700 MPa CS) | 32 MPa at 25C, 70 MPa at -20C | yes |
| edge clamp epoxy shear | <~5 MPa | 1.0-1.7 MPa | yes |
| frame thermal mismatch | Ti 0.6 um vs Al 81 um over 140 mm/40 K | Ti required | yes |
| reaction-plane offset | wing bow <3 um | 0.3 mm gives 3 um; 2 mm gives 17 um | design constraint |
| hinge force | ~<=500 N | 522 N peak at -20C | marginal |
