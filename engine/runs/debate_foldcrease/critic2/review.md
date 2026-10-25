# Critic round 2 review: tensioned neutral-plane glass sandwich, v2

Re-runs: design2, design3, checks2 and sag_combo all reproduce their stored .out files byte for byte (*.rerun).
Independent checks are in check3.py / check3.out.

## Numbers that hold
- D = 2.372e-3 N m; glass share 99.22%; strains 0.69 / 0.27 / 0.33%; bulb glass stress 497 MPa.
- The quasi-static closed form depth = S*dk/T, slope = S*k'/T matches the solver to within 3% (l = 0.89 mm, much less than the 15 mm ramps).
- 15/15 ramps, 20/10 set, T=3000: 0.24 um / 0.0164 mrad. Against round 1 corrected: 4.0x depth, 20x slope. Ramps alone at T=1000: 6.6x.
- The 15 mm ramp result sits on a continuous solver branch (13, 14, 15 and 17 mm agree). 16 mm and 20 mm jump to a spurious branch.
- Folded geometry: cavity depth per half is 5.3 / 4.7 / 2.4 / 0.8 mm at 5 / 10 / 15 / 20 mm from the spine, so a 13-14 mm spine is consistent.
- Flaw thresholds, finger deflection (119 um/N), spring sizing, Idea 2's 0.78x factor and the T=0 rows are all confirmed.
- Against HTX (48 -> 167 um, 1.24 deg = 21.6 mrad, secondhand via iThinkDiff): the ratios are arithmetically correct.

## Unsupported or unfair
1. Sag is left out of the headline. Including face-up gravity sag, the 20/10, phi_g=0 case is 0.0246 mrad at T=3000, which already fails the 0.024 target. The "phi_g <= 6e-4" condition holds only at T=4000 (0.0239), and the spring was not sized for 4000.
2. Open-state boundary terms are missing from the budget (check3 3a-3d). The model clamps both wings perfectly coplanar. Under tension the span is a straight chord, so any wing misalignment shows up as a slope step at each clamp line, compressed into l = 0.9 mm:
   - an angle mismatch delta gives a kink of delta/2, so meeting 0.024 mrad needs delta <= 0.05 mrad (0.003 deg);
   - a height step dh gives dh/76 mm, so it needs dh <= 1.8 um;
   - 450 N of frame compression at 1-2 mm eccentricity bows each half by 0.8-3.2 mrad, and the +-20% thermal swing in force moves this by +-0.16-0.65 mrad.
   These terms are 7-27x the target, and raising T does not reduce them.
3. Pressure loading is missing. The free span is a 76 mm diaphragm: 1 Pa gives 0.011 mrad, 10 Pa gives 0.11 mrad, and a sealed cavity at +1 K (340 Pa) gives 3.9 mrad and 79 um. The cavity must be vented with tau < 0.3 s, which conflicts with dust and water sealing.
4. The "protected" inner bulb face (497 MPa when folded, slow-growth flaw 1.48 um) is bare glass. It is pressed onto the backstop by every touch above 0.5 N, and it sits in a cavity that must be vented (dust). This is a new contact-damage route on the most highly stressed face.
5. Touch is defined as swipe topography only. A band 76 mm wide that gives 119 um/N and bottoms out at 0.5 N is likely detectable by pressing or with a stylus. The trade-off is listed, but the touch criterion defines it away.
6. phi_g: the 2024 Extreme Mechanics Letters paper (vol. 71, 102219, PolyU) reports permanent macroscopic creases in folded ion-exchanged ultrathin aluminosilicate glass. Recovery there is reduced by longer holds *and repeated loading*. The answer missed this source. It raises the prior on phi_g and contradicts the claim that "set depends on hold time, not on cycle count".
7. The 700x / 1300x ratios compare a best-case model (phi_g=0, 1 min, no boundary terms) with a measured product. With phi_g = 3e-3 the ratio is 217x. With a 0.1 deg open-angle error the slope ratio is about 25x.
8. The strip test as stated: a horizontal 30 mm bare UTG tail sags 1.0 mm under its own weight, and a sandwich strip 63 um, against a 49 um signal. It must be measured edge-on (bending plane horizontal) or as a before/after difference. The test also says nothing about items 2-4.

## Undersold
- Laminate the display with the hinge seated in the open state. Then only *repeatability* of the seat matters, not its absolute accuracy, and the 450 N preload can seat lapped kinematic pads (sub-um repeatability is routine).
- A larger R helps both stress and crease: R = 7 mm gives 391 MPa and 0.0139 mrad, R = 9 mm gives 0.0121 mrad, at the cost of a 14-18 mm bulb. With phi_g = 1e-3, R = 9 mm gives 0.021 mrad, which passes.
- The opening work is about 15 mJ (half of F times the 69 um stretch), not 30 mJ.
- Polymer recovery while open (glass forces the polymer layers flat) is not credited, because everything is measured at 1 min.

## Cheapest decisive experiment (system level)
Run the author's tensioned-strip rig, but add the wing angle and height as controlled variables. Measure with phase-measuring deflectometry (about 0.01 mrad resolution) and record the clamp-line kink against the shim. Run alongside it the edge-on strip test for phi_g on ion-exchanged versus alkali-free glass.
