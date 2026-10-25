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