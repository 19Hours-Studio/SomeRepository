The answer shows no real gain over current practice. Every crease figure it gives comes from a model, the model has never been checked against a real phone, and the "invisible" result depends on a tension spring that has not been tested.

**What holds up**
- I reran `sandwich.py` and `table.py`, and their output matches the files. The physics is consistent within its own assumptions:
  - The panel sits at the neutral plane, strained 0.22% at R = 5 mm.
  - Glass carries 99.5% of the bending stiffness.
  - In-plane tension flattens the residual curvature, because the 39 mm fold zone is much longer than the 1.3 mm length over which tension acts.
- The answer is candid about its weak spots: it admits the earlier calibration was wrong, rejects the soft-gel fix, and says glass anelasticity is assumed to be zero.
- It names a cheap, decisive experiment with a kill criterion: bonded strips wrapped on a mandrel, held 72 h at 60 °C, then profiled with and without a 20 N weight.
- It corrects the brief: the "0.7 mm" figure for the Fold 7 has no source, and the best public measurement is HTX's 48→167 µm on the iPhone Duo. I confirmed the HTX figures, though they come from a single lab.

**Why the headline gains don't count**
- **"≥150× below the aged iPhone Duo"** sets a model of a stack that doesn't exist against a measured product. Each crease value is just an assumed set fraction (5–50%) run through the model.
- **"7–19× better"** compares the design with the author's own previous design, not with current practice.
- **The model type has missed badly before.** The previous round's simplified model predicted 0.3–1.7 µm (I reran it). Once a critic added the adhesive coupling, the same design came out at 4–114 µm.
- **Without tension it fails its own target.** The untensioned range is 3–13 µm and 0.29–1.22 mrad. That shifts a reflection by 2–8 arcmin, above the answer's own 0.2 mrad limit. Only the spring makes the design invisible, and if the spring loses preload the crease comes back.

**Problems the answer misses (`judge_checks.py`)**
- **Gravity sag.** The 39 mm unsupported fold zone sags 0.3–0.6 µm under its own weight even at 500–1000 N/m tension. That is as large as the claimed 0.1–0.4 µm crease, so the result changes with how the phone is held.
- **Every touch hits the hinge plates.** A 1 N finger press deflects the glass about 0.9 mm even under 1000 N/m. The backstop gap is 10–20 µm, so every touch pushes the glass onto the plates. The face that hits them is the back face, which is under 490 MPa tension in the fold. The answer calls this face "protected"; in fact it is in repeated contact with metal, which is exactly how the 1.4–2.8 µm flaws that grow into cracks get made.
- **Prior art.** Symmetric stacks with stiff layers on both sides to put the display at the neutral plane are already patented (US10268238, US10514724, WO2018037311), and Samsung reportedly uses a dual-layer UTG. What is new here is the glassy adhesive, leaving the fold zone unbonded, and the tension spring.

My notes are in `review.md` and the check script is `judge_checks.py`, both in the current folder.

Sources:
- [iThinkDiff – HTX iPhone Duo 3,000-fold test](https://www.ithinkdiff.com/iphone-duo-crease-test-3000-folds/)
- [US10268238 – neutral axis management with thin high-modulus layers](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10268238)
- [US10514724](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10514724)
- [WO2018037311A1](https://patents.google.com/patent/WO2018037311A1/en)
- [TrendForce – Samsung dual-layer UTG](https://www.trendforce.com/news/2026/01/20/news-samsung-reportedly-achieves-20-crease-reduction-with-utg-galaxy-z-fold-8-apple-weigh-adoption)
- [Zerodur room-temperature delayed elasticity (SPIE)](https://electronicimaging.spiedigitallibrary.org/conference-proceedings-of-spie/1533/0000/Delayed-elasticity-in-Zerodur-at-room-temperature/10.1117/12.48857.full)

HONEST GAIN: none demonstrated. The only figure the evidence supports is a modelled, unvalidated 3–13 µm residual depth without tension, against 48 µm measured on a new iPhone Duo (about 4–16× shallower), and that still fails the answer's own 0.2 mrad invisibility limit. The sub-µm "invisible" result rests on an untested tension spring and assumed set values.