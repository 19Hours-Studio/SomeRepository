I've finished the checks. The author's numbers reproduce, but the claim that the crease is invisible does not hold up, because the slope budget leaves out several terms.

## 1. Re-run and re-derived numbers

All four scripts (`design2`, `design3`, `checks2`, `sag_combo`) re-run and match their stored outputs exactly (`critic2/*.rerun`). My independent checks are in `critic2/check3.py`.

| Claim | My check | Holds? |
|---|---|---|
| D = 2.37e-3 N·m; glass 99.22% of D; strains 0.69 / 0.27 / 0.33%; 497 MPa at the bulb | Same | ✓ |
| 15/15 mm ramps, 20/10% set, T = 3000 N/m: 0.24 µm and 0.016 mrad | The simple formula (depth = ΣφD·Δκ/T, slope = ΣφD·κ′/T) gives 0.246 µm and 0.0164 mrad; the full solver gives 0.240 µm and 0.0164 mrad. The tension length is 0.89 mm, much shorter than the 15 mm ramps, so the simple formula is valid. | ✓ |
| 4× on depth and 20× on slope against round 1; ramps alone give 6.6× at T = 1000 | 4.0×, 20.4×, 6.6× | ✓ |
| The 15 mm geometry is a real solution | 13, 14, 15 and 17 mm ramps give a smooth family (Rn 16.7–23.5 mm). 16 mm jumps to a spurious solution (Rn 2.9 mm), so the solver is fragile but the 15 mm result is valid. | ✓ |
| Spine 13–14 mm; hinge cavity 25–35 mm into each half | Cavity depth is 5.3, 4.7, 2.4 and 0.8 mm at 5, 10, 15 and 20 mm from the spine | ✓ |
| Flaw thresholds 1.48 / 2.04 µm; 119 µm per newton of finger force; spring sizing; Idea 2 at 0.78×; spring-failure crease 9–185 µm | Same | ✓ |
| HTX 48→167 µm, 1.24° (21.6 mrad) | Matches the iThinkDiff write-up. It is secondhand; I couldn't find HTX's own publication. | ✓ (sourced) |

## 2. Unfair or unsupported points

1. **Gravity sag breaks the headline.** With sag included, the realistic case (20/10% set, no glass set) is 0.0246 mrad at T = 3000, already over the 0.024 mrad target. "Meets the target if φ_g ≤ 6e-4" is only true at T = 4000 (0.0239 mrad). The spring has not been sized for 600 N.
2. **The biggest omission: the two edges of the free span.** The model assumes both phone halves are perfectly level with each other when open. Under tension the free span pulls straight, so any misalignment becomes a sharp slope break about 0.9 mm wide at each clamp line. Raising T makes these breaks sharper, not smaller.
   - **Angle:** an open-angle error δ gives a break of δ/2. Meeting 0.024 mrad needs δ ≤ 0.05 mrad (0.003°).
   - **Height:** a height step must be ≤ 1.8 µm across the 76 mm span.
   - **Frame bowing:** the frame carries the 450 N reaction. If that load sits 1–2 mm below the display, each half bows by 0.8–3.2 mrad. The ±20% thermal swing in tension moves that by ±0.16–0.65 mrad, which is 7–27× the target.

   None of these is in the budget. This could change the slope by one to two orders of magnitude.
3. **Air pressure is not modelled.** The free span acts like a diaphragm: 1 Pa gives 0.011 mrad and 10 Pa gives 0.11 mrad. A sealed cavity warming by 1 K builds about 340 Pa, giving 3.9 mrad and a 79 µm bulge. The cavity must therefore vent quickly (time constant under about 0.3 s), which conflicts with dust and water sealing.
4. **The "protected" glass face is not protected.** The bottom glass face carries 497 MPa when folded and starts slow crack growth from a 1.48 µm flaw. It is bare glass, every touch above 0.5 N presses it onto the backstop, and it sits in a cavity that must be vented, so dust can get in. This is a new route to fracture that the answer does not consider.
5. **The touch test defines away a detectable feature.** It checks only swipe topography. A 76 mm band that gives 119 µm per newton and then bottoms out on the backstop at 0.5 N is likely detectable by pressing or with a stylus.
6. **Glass set (φ_g): there is a source the answer missed.** Extreme Mechanics Letters vol. 71, 102219 (2024, PolyU) reports permanent creases in folded ion-exchanged ultrathin aluminosilicate glass. I could only read the abstract, not the full text. Recovery there gets worse with longer holds *and with repeated loading*, which contradicts "set depends on time held folded, not fold count". This raises the risk that φ_g ≥ 1e-3.
7. **700× / 1300× compares a best-case model with a measured product.** With φ_g = 3e-3 the depth ratio is about 217×. With a 0.1° open-angle error the slope ratio is about 25×.
8. **The strip test as written won't resolve the signal.** A horizontal 30 mm tail of bare 20 µm glass sags about 1 mm under its own weight; a sandwich strip sags 63 µm. The expected signal is 49 µm. Strips must be measured edge-on or as a before/after difference. The test also says nothing about points 2–4.

**Where the answer undersells itself:**
- **Opening work** is about 15 mJ (½ × 450 N × 69 µm stretch), not 30 mJ.
- **Bulb radius is an unused lever.** R = 7 mm gives 391 MPa in the glass and 0.0139 mrad. R = 9 mm gives 0.0121 mrad, and still passes at φ_g = 1e-3 (0.021 mrad), at the cost of a 14–18 mm bulb.
- **Polymer recovery while open is not credited,** because everything is measured 1 minute after opening.
- **Its comparison with current glass is fair:** its flaw tolerance is comparable to or better than shipping UTG.

## 3. Where a larger honest gain is likely

- **Fix the edges first; that is where the error budget really goes.** Laminate the display with the hinge seated in its open position. Then only the *repeatability* of that seat matters, not its absolute accuracy. Let the 450 N preload seat lapped kinematic pads, which routinely repeat to under 1 µm. Route the frame load in the display's plane, within about 0.15 mm.
- **Protect the bottom glass face** with a compliant polymer backstop and a breathable ePTFE vent membrane.
- **Use a larger R** if a thicker spine is acceptable.
- **Cheapest decisive experiment:** the author's tensioned-strip rig, with the wing angle and height deliberately varied using shims and the result measured by deflectometry. Run it alongside the edge-on glass-set test comparing ion-exchanged and alkali-free glass.

Files are in `critic2/`: `review.md`, `check3.py`, `check3.out`, and the `*.rerun` outputs.

Sources:
- [iThinkDiff – HTX Duo test](https://www.ithinkdiff.com/iphone-duo-crease-test-3000-folds/)
- [Oppo newsroom – Find N6](https://www.oppo.com/en/newsroom/stories/oppo-find-n6-zero-feel-crease-foldable-innovation/)
- [Android Authority – N6 durability](https://www.androidauthority.com/oppo-find-n6-zero-feel-crease-durability-3648272)
- [PolyU – Plastic deformation and recovery in ultrathin aluminosilicate glass](https://research.polyu.edu.hk/en/publications/plastic-deformation-and-recovery-in-ultrathin-aluminosilicate-gla/)
- [On the origin of delayed elasticity in inorganic glasses](https://www.tib-op.org/ojs/index.php/glass-europe/article/view/3253)

HONEST GAIN: the modelled material-set crease falls from 0.97 µm / 0.335 mrad to 0.24 µm / 0.016 mrad (4× depth, 20× slope; reproduced), but invisibility is not shown. Gravity sag alone pushes it to 0.025 mrad at T = 3000, and the missing edge-alignment, pressure and glass-set terms could each exceed the 0.024 mrad target by 5–100×.