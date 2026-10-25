# Gain review of answer.md

Reproduction: sandwich.py and table.py rerun; their numbers match sandwich.out and table.out.

Independent checks (judge_checks.py):
- Self-weight sag over the 39 mm unsupported fold zone: 5.4 um with no tension, 0.3-0.6 um at 500-1000 N/m. That is the same size as the claimed 0.1-0.4 um crease, so it depends on orientation.
- A 1 N finger press deflects the fold zone by about 0.9 mm even at 1000 N/m, far more than the 10-20 um backstop gap. Every touch therefore presses the glass onto the hinge plates. The face that hits the plates is the bottom face, which carries 490 MPa tension in the bulb; the answer calls it "protected".
- At the answer's own 0.2 mrad limit, the untensioned case (0.29-1.22 mrad, a 2-8 arcmin reflection shift) fails. Invisibility depends entirely on the tension spring.

Evidence status:
- No measured data exist for the proposed stack. Every crease figure comes from assumed set fractions (phi) plus an assumed zero anelasticity of glass.
- The model has not been calibrated against any device.
- The round-0 simplified model predicted 0.3-1.7 um. Once the critic added coupling, that design gave 4-114 um. This class of model has missed by 10-100x before.
- "150-1600x below the aged Duo" compares model output for a hypothetical stack with a measurement of a product (HTX: 48 um new, 167 um after 3000 folds; a single lab).
- "7-19x" compares the design with the author's own earlier design, not with current practice.
- Prior art: symmetric neutral-plane stacks with high-modulus layers on both sides (US10268238, US10514724, WO2018037311), and Samsung's reported dual-layer UTG. What is new here is the glassy adhesive, having no bonded plate in the fold zone, and the tension spring.
