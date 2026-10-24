# LOG — repair c1 (foldcrease)

| round | idea | change | decisive number | result |
|---|---|---|---|---|
| 0 | 1 | check claim "R>=3 mm keeps every layer <0.3%" (calc/strain.py) | UTG 45 µm at R=3: 0.75%; 60 µm PET film 1.0%; back PET 0.63% | claim FALSE; anchor (tension) must do the work, not radius |
| 1 | 1 | tension via wing plates -> PSA -> stack (as proposed) | shear-lag of 45 µm UTG over acrylic OCA (G=50 kPa): l=40 mm, only 30% of edge tension reaches the fold, sustained shear 48 kPa (~100% strain) at 60 °C | FAILS (matches kill-test 89 kPa) |
| 2 | 1 | UTG made the tendon: grip the UTG's outer edges in rails; silicone optical gel (G~2 kPa) replaces OCA under UTG | l=281 mm, 97% of tension reaches the fold, gel shear 1.9 kPa; glass 44 MPa at T=2000 N/m | load path works |
| 3 | 1 | beam-column FD model with plate contact (calc/crease.py, contact_check.py), calibrated to today's 60–150 µm creases | sharp teardrop transitions: T=2000 -> depth 1.5 µm but slope 1.4–1.5 mrad (FAILS the 1 mrad target) | features narrower than sqrt(D/T)=0.57 mm can't be pulled flat |
| 4 | 1 | clothoid (curvature-ramped) hinge path, ramp >=2 mm | T=2000 N/m, base 150 µm: depth <=2.1 µm, slope <=0.82 mrad; holds for untensioned-equivalent crease <=~180 µm | WORKS on paper (model) |
| 5 | 1 | consistency: glass static fatigue, thermal, frame | 44 MPa needs >=98–128 MPa 10 s edge strength (n=20/15); Ti frame mismatch 4 µm vs 95 µm stretch; Al needs 0.9 mm spring stroke | pass with Ti frame or a force-controlled spring |
| 0 | 2 | check "60 µm stack at R=5 = 0.3–0.5%" | bonded t/2R=0.6% (kill-test right), but with soft interlayers each layer bends about its own mid-plane -> strain = t_i/2R | rule must be per layer, not per stack |
| 1 | 2 | per-layer budget: thickest polymer layer <=25 µm (drop PET protector and PET back film -> hard-coated UTG, CPI back film) | R_min = t/(2 eps_c): 4.2 mm @0.30%, 5.0 mm @0.25%, 2.5 mm @0.50% | R=4.2 mm -> spine ~10.2 mm |
| 2 | 2 | OCA is a crease source that does NOT scale with R (slip = pi*d/2) | acrylic locked shear 92 kPa; silicone OCA 6 kPa; gel 0.4 kPa | add a low-relaxation silicone interlayer to the budget |
| 3 | 2 | model idea-2 stack, untensioned, 2 mm clothoid (calc/study2.py) | polymer share of stack stiffness 16.9% -> 2.4%; if no threshold exists (eps_c=0): 11–42 µm crease (FAILS); eps_c(60 °C)>=0.30%: 0 µm at R=4.2 | WORKS only if a no-set threshold exists at 60 °C — deciding unknown |
| 4 | both | cost per spec-passing unit (calc/cost.py; adders are my estimates) | idea1 $13–50, idea2 $7–33 vs hinge $70–80 (Kuo); baselines deliver ~0 units that meet spec | — |
