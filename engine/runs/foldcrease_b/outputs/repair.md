I repaired both ideas and kept both anchors, but neither has been shown to work in hardware. Idea 1 should work on paper; whether it does depends on two numbers nobody has measured. Idea 2 only works as an add-on to a stack that already creases very little, so it is a niche. Every number below comes from my own estimates in `calc/idea1.py`, `calc/idea2.py` and `calc/idea2_thermal.py`. The round-by-round log is in `LOG.md` and the consistency tables are in `NOTES.md`.
=== IDEAS ===
IDEA 1
NAME: Load-cell-scheduled drumhead hinge
MECHANISM: Anchor kept: in the last few degrees of opening, the hinge pulls the panel edges outward. This puts the panel under in-plane tension, which flattens a residual set elastically, and load cells control that tension in closed loop. Tension cannot reach "invisible" against a narrow or deep crease: a 167 µm crease needs about 2.9 kN/m, and the gate's 3.9 kN/m strains the OCA by about 670%. So the repaired design works only as a finisher on wide, shallow sets. A large-arc waterdrop hinge (R ≈ 3–3.5 mm) spreads the set to σ ≥ 5–8 mm. A graded-modulus bond then spreads the shear over λ ≈ 15 mm, which keeps sustained OCA shear at 50% or less. Under those conditions, 200–290 N/m (30–43 N over the whole hinge) flattens a 48 µm crease with σ = 8 mm, or a 20 µm crease with σ = 4.7 mm, to ≤2 µm, ≤0.3 mrad and ≤0.5 m⁻¹. The tension needs only about 2–7 µm of stretch, while 40 K of temperature swing shifts the panel length by 12 µm. An open-loop cam therefore gets the tension wrong by more than 100%. The fix is a stiff series spring (about 1 kN/mm) whose preload is reset by a micro-actuator from load-cell and temperature readings, scheduled by how long and how hot the phone was last left closed.
VALUE: It turns an existing wide, shallow crease of about 50 µm into a measured, invisible one for about +$5–10 per phone (about 1–1.5% of a ~$670 Fold-class BOM). No baseline (Samsung, Apple matte, Oppo N6) delivers a crease below these thresholds at any cost.

IDEA 2
NAME: Fluid-slip glass-leaf sandwich
MECHANISM: Anchor kept: an index-matched sealed fluid takes the place of the shear-coupling adhesive, so interlayer slip happens as flow with no shape memory. Repairs:
- A Newtonian fluid (phenyl-silicone, n ≈ 1.50) replaces the gel, and it fills the whole optical stack, not just the fold band.
- The layers are pinned only at the fold centreline (outside the active area), and the far edges slide freely inside a soft perimeter seal. This removes the 1.4% membrane mismatch that bonded band-ends force (FACT 11).
- The PET/CPI cover and the back film are removed. The stack is UTG 30 µm (hard-coated) / fluid / 20 µm panel (colour filter on encapsulation, on-cell touch) / fluid / 3–5 fluid-decoupled 30 µm UTG "leaves", at R = 2.5 mm.
Each solid layer bends about its own midplane: UTG at 0.6% strain and 420 MPa, which is below the 500–1000 MPa compressive stress of chemically strengthened glass, and the panel at 0.4%. The fluid locks the layers together in the normal direction: squeeze-flow times run from 69 days under a sustained finger press to over 1,000 years for gravity drainage. The panel, which is the only layer that creeps, is therefore held flat by elastic glass whose bending stiffness adds up leaf by leaf with no added strain. The panel's set is suppressed by D_panel/D_total = 0.009 with 3 leaves and 0.005 with 5. If the free panel keeps 10% or less of its fold curvature as set, the result is 0.3–0.7 µm depth and ≤0.27 mrad slope.
VALUE: The design removes every layer that sets except a 20 µm panel, then overpowers that panel elastically with about 0.5% stiffness ratio. If the panel's set is ≤10%, this gives a crease about 70× flatter in slope than the iPhone Duo at 3000 folds, at an estimated +$20–60 per phone (+3–9% BOM), with glossy optics and no matte layer.

=== NOTES ===
**Measurement targets (used for both ideas, open state).**
- Depth ≤2 µm peak-to-valley.
- Max slope ≤0.3 mrad, measured by deflectometry. The iPhone Duo is at 21.6 mrad (1.24°) after 3000 folds (FACT 5).
- Peak curvature ≤0.5 m⁻¹ (500 mdpt). This is speculative: I scaled the ~100 mdpt architectural-glass specs ([AIS](https://aisglass.com/wp-content/uploads/2020/10/AIS-7.pdf), [IIBEC](https://iibec.org/wp-content/uploads/2024/05/Rosen-Final.pdf)) for reflected objects about 10× closer. No psychophysics source was found.
- Touch: below the [Louw 2000](https://link.springer.com/doi/10.1007/s002210000350) haptic threshold (A ∝ w^1.3), which is about 27 µm at 3 mm width and about 128 µm at 10 mm.
- Persistence test: 2000 cycles at 23 °C, at 60 °C/93% RH, and at −20 °C, with 8 h folded holds every 100 cycles. Deflectometry and profilometry are read at 10 s, 1 min and 1 h after opening.

**Idea 1: anchor kept** (closed-loop, set-scheduled tension). Calculations are in `calc/idea1.py` and `calc/idea1b.py`.
- **Decisive numbers:**
  - The required tension scales as T ≈ n·D·k².
  - The fit to HTX data gives σ = 4.7 mm.
  - The adhesive allows T_max ≈ 675 N/m: λ = 15 mm × 50% shear × G′ = 9×10⁴ Pa (FACT 12). A 300% short-term limit (FACT 13) is not a safe sustained limit.
- **Baselines:**
  - Samsung Fold 7: UTG + PET + OCA, the cheapest option. The crease is visible.
  - Apple: matte coating plus a $19 replaceable cover layer. The crease measured 48→167 µm and can be seen and felt.
  - Oppo N6: claims about 50 µm (manufacturer figure).
  - None reaches the targets, so the cost per invisible crease delivered is undefined for all three. Per phone, Idea 1 adds about 1% BOM ([Fold 4 BOM ~$670](https://www.sammobile.com/news/samsung-flagship-foldable-lower-profit-margin-than-huawei/)). The component costs are my estimates.
- **Consistency check:**

| Quantity | Value | Status |
|---|---|---|
| OCA shear at 200 N/m | 15% at 25 °C, ~27% at 60 °C | OK |
| Panel strain from tension | 0.01–0.02% | OK |
| Required stretch | 2–7 µm | Below the thermal swing, so the loop or spring is mandatory |
| Hinge force | 30–43 N | OK |
| Sets of 167 µm | Need 2.9 kN/m | **FAIL** |

- **Hazards:** sustained OCA creep while the phone is open, and tension changing as the phone is dropped or twisted. Tension also does almost nothing against short-wavelength kinks: a 3 mm ridge keeps about 80% of its curvature.
- **Deciding unknown:** whether open-state tension acting as reverse stress stops the cycle-to-cycle set ratchet (48→167 µm in the HTX test).
- **Cheapest experiment:** 2×5 panels in a commercial fold tester, with and without 250 N/m of open tension. Run 2000 cycles with dwells and take profilometry every 250 cycles.
- **Closest prior art:** Apple EP 4738056 (open-loop tension past a threshold angle). This design adds the load-cell plus series-spring schedule that open-loop cams cannot replace (more than 100% thermal error).
- **Verdict: NICHE** (finisher on a wide, shallow set).

**Idea 2: anchor kept** (fluid slip with no shape memory). Calculations are in `calc/idea2.py`.
- **Decisive numbers:**
  - Suppression ratio D_p/D_tot = 0.0054–0.009.
  - UTG stress 420 MPa against 500–1000 MPa compressive stress ([Schott](https://www.schott.com/en-in/applications/schott-utg-in-foldable-displays), general range).
  - Interface reflectance 1×10⁻⁵, against 4% for an air gap.
  - Viscous drag 13 Pa, against about 0.2 MPa for an OCA.
- **Baselines:** the same three as Idea 1; none delivers the targets. Idea 2 costs +3–9% BOM (estimate; I found no UTG price).
- **Consistency check:**

| Quantity | Value | Status |
|---|---|---|
| Slip at each interface / whole stack | 63 µm / 377 µm | Fits under a ≥1 mm bezel; seal shear ~40% over a 1 mm bead |
| Thermal gap change | 0.58 µm, uniform | OK |
| Suction needed | ~kPa, against 100 kPa available | OK |
| Panel strain | 0.4% | Assumed below the thin-film encapsulation's crack onset |
| Glass fatigue | Surface stays in net compression | OK only if compressive stress ≥ ~500 MPa (narrow margin) |

- **Hazards:**
  - Air ingress or bubbles, which would be highly visible.
  - Seal life.
  - Impact and pen-drop resistance without the PET protector, plus shatter containment.
  - Fluid compatibility with the organic layers.
  - Thickness of about 240 µm in total.
  - Yield of a liquid-lamination process.
- **Deciding unknown:** the set fraction f_set of a bare 20 µm panel (no OCA, no back film) after 8 h at R = 2.5 mm and 60 °C/93% RH. The design works if f_set ≤ 0.1 and fails at 0.2.
- **Cheapest experiment:** 10 bare panel or PI/encapsulation coupons per condition, held on a mandrel, then residual angle measured over 24 h. That is about $2–5k, and it gives f_set to about ±0.02.
- **Closest prior art:** [US 11546986](https://patents.justia.com/patent/11546986) (lubricating layer or air gap) and Corning's [US 11752730](https://patents.justia.com/patent/11752730) (bendable glass stacks; I did not check whether it uses a fluid). This design adds the index-matched optical-fluid stack, the centreline pin with free edges, and the leaf-stiffness overpowering of the panel set.
- **Verdict: WORKS conditionally** (it hinges on f_set; NICHE if 0.1 < f_set < 0.2, FAILS if ≥ 0.2).

Data versus speculation: FACT 5/12/13, the Louw threshold law and the compressive-stress range are sourced. The f_set values, visibility thresholds, sustained-shear limit and costs are assumptions. The round-by-round log is in `LOG.md`.

Sources: [Louw 2000](https://link.springer.com/doi/10.1007/s002210000350); [AIS glass spec](https://aisglass.com/wp-content/uploads/2020/10/AIS-7.pdf); [IIBEC roll-wave](https://iibec.org/wp-content/uploads/2024/05/Rosen-Final.pdf); [Schott UTG](https://www.schott.com/en-in/applications/schott-utg-in-foldable-displays); [US 10090480 static fold test](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10090480); [SamMobile Fold 4 BOM](https://www.sammobile.com/news/samsung-flagship-foldable-lower-profit-margin-than-huawei/); [US 11752730](https://patents.justia.com/patent/11752730); [US 11546986](https://patents.justia.com/patent/11546986)

IDEA 3
NAME: Centre-pinned capillary-wrung glass sandwich
MECHANISM: Anchor kept: there is no adhesive anywhere in the active area. The layers are held together by thin films of index-matched phenyl-methyl silicone oil (DC 550, n = 1.49, 3 µm). The repair addresses the kill test. Each layer is pinned only on the fold axis, by tabs in the short-edge bezel. The long edges float in a 0.5 mm oil-filled groove (the reservoir), so the 64–112 µm fold slip and 61 µm of thermal slip happen with zero strain. The original idea was killed because 0.85% of mismatch cannot fit under a 0.0009% buckling limit. The hermetic seal is replaced by an open oil edge, so surface tension clamps the layers together at 2γ/h = 14 kPa. A barrier coating keeps the oil from creeping out, as watchmakers do to stop oil migrating. The stack, from the top:
- 50 µm bare cover glass (UTG) with only an anti-fingerprint coat;
- oil film;
- 25 µm OLED on polyimide (PI), with no polarizer and touch built into the panel;
- oil film;
- a floating 30 µm back glass.

It folds as a waterdrop at R = 3.5 mm. The OLED then bends at only 0.36%, below the ~0.5% at which colourless PI starts to keep a set. The cover glass sees 514 MPa against ≥700 MPa of compressive surface stress. If the OLED does keep a set, the clamp pulls it flat: the lift is 52 nm if 5% of the curvature stays, and 209 nm if 10% stays. Under the bend zone the hinge plates sit 20 µm below the stack and do not touch it at rest, so their tolerance cannot print through. That leaves one source of crease: how flat the two halves sit when open. The hard stops must be factory-trimmed to ≤0.02° and ≤3.5 µm, and they wear only about 1 nm in 2,000 cycles.
VALUE: It gives a glossy screen whose crease is gone by design, not hidden. It is about 150 µm thinner than a bonded stack (111 vs ~260 µm) and costs an estimated +$4–14 per phone (4–12% of a ~$122 inner-display subsystem). Apple's matte approach still measures 48 → 167 µm and charges $19 per replacement top layer.

IDEA 4
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
