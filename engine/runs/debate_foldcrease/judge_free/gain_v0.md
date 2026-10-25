The answer supports no gain over the best current practice that has been shown, measured or modelled robustly. Its "30–100× less crease depth" comes from a model that holds up only under its own chosen assumptions. It does offer a reasonable hypothesis and a good cheap experiment to test it.

I read `answer.md` and the supporting code, ran an audit script of my own, and searched for the published measurements. The audit uses the answer's own formulas with varied assumptions (`check_model.py`, `check_model.out`), and the summary is in `review.md`.

**What the answer gets right**
- **Architecture:** it describes a full stack (bare 70 µm UTG, OCA, polarizer-less panel, solid β-Ti foil, 4 mm teardrop hinge) and states each layer's role.
- **Strain arithmetic:** the numbers are correct. My only adjustment is that UTG stress is about 662 MPa rather than 630 MPa once the plate factor (1/(1−ν²)) is included.
- **Measurement and testing:** the targets, test protocol and failure modes are well framed. It reasonably flags that folded hold time matters more than cycle count.
- **Cheapest test:** the proposed experiment is sound and cheap. Fold laminate strips around 2–5 mm mandrels, hold them 72 h at 60 °C, then measure with an interferometer.
- **Facts checked:** the HTX measurement of the iPhone Duo is real but comes from a single secondhand report: 48 µm new with a slope under 0.1°, and 167 µm and 1.24° after 3,000 folds. The 0.7 mm Fold 7 figure is only a press estimate.

**Why the claimed gain doesn't hold up**
1. **Radius has the wrong effect in the model.** Predicted depth grows in proportion to the bend radius, so in the model a larger radius makes the crease worse. That contradicts industry practice, where wider waterdrop hinges reduce the crease. The 4 mm radius therefore contributes nothing to the claimed gain. All of it comes from assuming glass and titanium take zero permanent set and from removing the polymer films.
2. **The "calibration" relies on a free parameter.** To match the Duo, the share of bending strain kept as permanent set has to be 0.07 for a new phone and 0.25 after 3,000 folds. The answer only runs its own stack at 0.02–0.10. At 0.25 it predicts 4.2 µm and 0.89 mrad, which fails its own targets (≤ 2 µm, ≤ 0.4 mrad).
3. **The result is fragile.** A 0.5% permanent set in the titanium foil gives a 12 µm crease, and a 0.1% set in the glass gives 9.6 µm. Either one cancels the advantage. The foil is cycled at about 50% of its yield stress, so a small set there is plausible.
4. **Some crease sources are left out.** The model ignores permanent shear set in the adhesive (shear strain about 7, which the answer itself computes), steps in the hinge and plate, and the reverse-curvature zones of a teardrop.
5. **"Invisible" is asserted, not shown.** On bare glossy glass, a 0.4 mrad slope moves the reflection of an edge 2 m away by about 1.6 mm. The answer cites no perception data showing that can't be seen.
6. **The comparison point is the wrong one.** The answer measures its gain against the iPhone Duo, but the best current practice is the Oppo Find N6. Oppo and TÜV Rheinland claim an 11 µm change after 200,000 folds and 82% less crease than the N5. Those are vendor figures, and they give a change rather than an absolute depth. Against them, even the modelled gain is only about 6–35×. The N6 already uses thicker UTG and a wider waterdrop. The tensioned-flat hinge idea is already in a patent (US 12487643), and the heater idea is speculative.

Sources:
- [iThinkDiff – HTX iPhone Duo crease test](https://www.ithinkdiff.com/iphone-duo-crease-test-3000-folds/)
- [Stuff.tv – N6, 11 µm after 200k folds](https://www.stuff.tv/?p=988012)
- [Oppo newsroom](https://www.oppo.com/en/newsroom/stories/oppo-find-n6-zero-feel-crease-foldable-innovation/)
- [GSMArena – N6](https://www.gsmarena.com/oppo_details_find_n6s_impressive_creasefree_display-news-71887.php)
- [PhoneArena – Fold 7 0.7 mm estimate](https://www.phonearena.com/news/foldable-iphone-crease-against-galaxy-z-fold-7_id178585)
- [SID Digest – deflectometry crease measurement](https://sid.org/Portals/sid/Files/SID-Digest/docs/77-5.pdf)

HONEST GAIN: none