# Review of answer.md: what gain it actually supports

Claimed: a residual crease of 0.3–1.7 µm and 0.07–0.35 mrad, "30–100× less than the best measured shipping crease".

Checks (`check_model.py` → `check_model.out`):
1. **Model radius dependence is backwards.** In the model, depth scales with R (κ∝1/R, L∝R). A larger radius therefore makes the crease *worse*, which contradicts industry practice (e.g. Oppo's wider waterdrop). The 4 mm radius contributes nothing to the claimed gain. The whole gain comes from setting the set fraction to 0 for glass and Ti, and from deleting the polymer films.
2. **The "calibration" uses a free parameter.** To match the iPhone Duo with the current-like stack needs φ=0.07 for a new phone (48 µm) and φ=0.25 after 3,000 folds (167 µm). The answer runs the proposed stack only at φ=0.02–0.10. At φ=0.25 it gives 4.2 µm and 0.89 mrad, which fails the answer's own target of ≤2 µm and ≤0.4 mrad.
3. **The result is fragile to set in the "elastic" layers.** A 0.5% set in the Ti foil, which is cycled at 500 MPa (about 50% of yield), gives 12 µm. A 0.1% set in the glass gives 9.6 µm. Either is comparable to Oppo's claimed figure.
4. **Not modelled:** OCA shear set (shear strain about 7, which the answer itself computes), steps at the hinge and plate, and the reverse-curvature zones of a teardrop.
5. **UTG margin is thin.** The bending stress is 662 MPa once the plate factor is included. About 470 MPa of net tension sits below a 10 µm DOL.
6. **The visibility target is not shown to mean "invisible".** A slope of 0.4 mrad on bare gloss glass shifts a reflected edge 2 m away by about 1.6 mm. That is not shown to be below detection, and no perception data is cited.
7. **The baseline is cherry-picked.** The answer compares against the iPhone Duo (48→167 µm, HTX, a single secondhand report). Best current practice is the Oppo Find N6: vendor/TÜV claim of an 11 µm change after 200k folds and 82% less than the N5. Against the N6, even the modelled gain is only about 6–35×.

**Verdict:** a testable hypothesis plus a good cheap experiment (mandrel strips, 72 h at 60 °C, interferometry). There is no measured or robustly modelled gain over the N6.
