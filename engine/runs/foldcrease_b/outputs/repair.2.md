I repaired both ideas and kept both anchors, but neither has been shown to work in hardware. Idea 1 should work on paper; whether it does depends on two numbers nobody has measured. Idea 2 only works as an add-on to a stack that already creases very little, so it is a niche. Every number below comes from my own estimates in `calc/idea1.py`, `calc/idea2.py` and `calc/idea2_thermal.py`. The round-by-round log is in `LOG.md` and the consistency tables are in `NOTES.md`.

=== IDEAS ===
IDEA 1
NAME: Centre-pinned capillary-wrung glass sandwich
MECHANISM: Anchor kept: there is no adhesive anywhere in the active area. The layers are held together by thin films of index-matched phenyl-methyl silicone oil (DC 550, n = 1.49, 3 µm). The repair addresses the kill test. Each layer is pinned only on the fold axis, by tabs in the short-edge bezel. The long edges float in a 0.5 mm oil-filled groove (the reservoir), so the 64–112 µm fold slip and 61 µm of thermal slip happen with zero strain. The original idea was killed because 0.85% of mismatch cannot fit under a 0.0009% buckling limit. The hermetic seal is replaced by an open oil edge, so surface tension clamps the layers together at 2γ/h = 14 kPa. A barrier coating keeps the oil from creeping out, as watchmakers do to stop oil migrating. The stack, from the top:
- 50 µm bare cover glass (UTG) with only an anti-fingerprint coat;
- oil film;
- 25 µm OLED on polyimide (PI), with no polarizer and touch built into the panel;
- oil film;
- a floating 30 µm back glass.

It folds as a waterdrop at R = 3.5 mm. The OLED then bends at only 0.36%, below the ~0.5% at which colourless PI starts to keep a set. The cover glass sees 514 MPa against ≥700 MPa of compressive surface stress. If the OLED does keep a set, the clamp pulls it flat: the lift is 52 nm if 5% of the curvature stays, and 209 nm if 10% stays. Under the bend zone the hinge plates sit 20 µm below the stack and do not touch it at rest, so their tolerance cannot print through. That leaves one source of crease: how flat the two halves sit when open. The hard stops must be factory-trimmed to ≤0.02° and ≤3.5 µm, and they wear only about 1 nm in 2,000 cycles.
VALUE: It gives a glossy screen whose crease is gone by design, not hidden. It is about 150 µm thinner than a bonded stack (111 vs ~260 µm) and costs an estimated +$4–14 per phone (4–12% of a ~$122 inner-display subsystem). Apple's matte approach still measures 48 → 167 µm and charges $19 per replacement top layer.

IDEA 2
NAME: Glass-carried thermally scheduled tension
MECHANISM: Anchor kept: the hinge puts the display in tension when it is flat. The repair sends the tension only into the cover glass, through structural-epoxy edge clamps (1.0–1.7 MPa shear). The adhesive layers (OCA) therefore no longer carry it, which was the kill test. Tension filters the crease as w0·(kℓ)²/(1+(kℓ)²) with ℓ = √(D/T), where w0 is the crease profile, k its spatial frequency and D the stack's bending stiffness. So it can only finish a small residual dent. Removing a Duo-class 48 µm dent to ≤1 µm and ≤0.02° would need 11,900 N/m in the glass (239 MPa, 1.8 kN): FAIL. A ≤10 µm dent needs only 90–2,100 N/m at 25 °C. Cold is the hard case, because adhesive stiffness rises about 40×. To cover it, an aluminium link in a titanium frame, 56 mm long with a 2:1 lever, raises the glass stretch passively by 1.63 µm/K. That gives 135 µm and 3,482 N/m at −20 °C (70 MPa in the glass, 522 N on the hinge) and drops to 5 µm at 60 °C. An over-centre toggle locks it in the last few degrees of opening, and the reaction force must run within 0.3 mm of the glass plane.
VALUE: It is a +$3–7 add-on (2–6% of the display) that cuts a ≤10 µm residual crease to ≤1 µm at −20 to 60 °C. It cannot remove a crease the size of current Apple, Samsung or Oppo ones.

=== NOTES ===
**Idea 1**
- **Anchor kept?** Yes: an adhesive-free, index-matched fluid laminate.
- **What the repair adds over prior art:**
  - US 11546986 lets metal supports slide on a lubricant. This adds an optical fluid stack pinned only on the fold axis, held by surface tension instead of a seal.
  - It adds a two-glass sandwich that flattens any set in the OLED.
  - It adds a non-contact bend zone with trimmed hard stops.
- **Decisive numbers:**
  - Layer strain 0.36% against a PI set threshold of about 0.5% (Korean study, R_crit ≈ 5 mm; the film thickness behind it is not verified).
  - Glass 514 MPa against ≥700 MPa compressive stress (Corning US 9321679).
  - Clamp 14 kPa.
  - Gravity sag 0.32 µm.
  - Edge reflectance 0.004%; if the oil pulls away and leaves an air gap, it jumps to 4.1%, which is a visible failure.
- **Invisibility targets:**
  - Depth ≤1 µm peak-to-valley and slope ≤0.02°, measured by deflectometry and white-light interferometry. The result must not differ from a rigid glossy phone tested as a control.
  - Nothing detectable by a finger sliding across, at ≤2 µm. This tactile threshold is not sourced.
  - No published human threshold exists. The AHFE 2023 study only rated <60 µm as "good".
- **Test for persistence:**
  - 2,000 cycles at 25 °C, then 24 h folded at 60 °C / 93% RH, 24 h at 85 °C, and folding at −20 °C. Measure profile and slope after each step.
  - Watch for air bubbles, oil migration, and the oil swelling the OLED's thin-film encapsulation.
- **Baseline:**
  - Duo: HTX measured 48 → 167 µm and 1.24°, with a $19 replaceable matte layer that dulls colour and blacks.
  - Oppo N6: about 50 µm (manufacturer claim).
  - Fold 7: the cheapest route, a PET screen protector over the glass that you replace.
  - None of these delivers an invisible crease, so per invisible-crease phone delivered, idea 1 is the only option, at +$4–14.
  - All cost figures are my estimates. The $122 display-subsystem figure is TechInsights, reported second-hand.
- **Hazards:**
  - The bare cover glass loses the shatter-retaining polymer film. A 25 µm replaceable glossy film held on by oil would add only 0.04 µm of lift.
  - Pen-drop resistance is untested.
  - Folding drag reaches 6 N/m at −20 °C.
  - The hard stops need ≤1.75 µm face tolerance.
- **Deciding unknowns and cheapest experiment:**
  - How much curvature the OLED-on-PI keeps (f) at 0.36% strain and 85 °C.
  - Whether the oil films survive 2,000 folds without air getting in.
  - Experiment: 10 sandwich coupons in a lab folder plus 5 bonded controls, measured by deflectometry.

**Verdict:** WORKS on paper. It is unproven until f ≤ 10% and no bubbles appear.

**Idea 2**
- **Anchor kept?** Yes: tension in the open state.
- **Prior art:** tension the flexible display when flat (Apple EP 4738056, US 12541230); heat the display to recover set (Motorola US 10409335). I found no passive thermal scheduling of the tension, and no tension carried only in the glass.
- **Baseline:** it is only worth adding to a stack that is already at ≤10 µm. Duo, Oppo and Samsung crease levels would need 1.8–6 kN, which is impossible.
- **Hazards:**
  - A 522 N frame load.
  - The wing bows 17 µm if the reaction force sits 2 mm off the glass plane.
  - The glass edges carry sustained tension.
  - An aluminium frame causes 81 µm of thermal mismatch, so the design needs titanium.
- **Deciding unknown:** how the stack's bending stiffness changes with temperature, i.e. the real 40× figure.
- **Cheapest experiment:** tension 6 coupons that have been folded and creased, at −20, 25 and 60 °C, measured by deflectometry.

**Verdict:** NICHE, as a finisher for a crease that is already ≤10 µm. The core mechanism is otherwise KNOWN.

Sources:
- [AHFE 2023 crease visibility study](https://openaccess.cms-conferences.org/publications/book/978-1-958651-47-6/article/978-1-958651-47-6_25)
- [Korean CPI residual-strain study](https://koreascience.or.kr/article/JAKO202102455512209.pdf)
- [Corning US 9321679](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9321679)
- [International Finance, Fold BOM](https://internationalfinance.com/technology/samsung-vs-apple-foldable-rivalry-why-these-smartphones-cost-so-much/)
- [Motorola US 10409335](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10409335)
- [Schott UTG](https://www.schott.com/en-in/applications/schott-utg-in-foldable-displays)