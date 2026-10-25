=== REVIEW ===
IDEA 1: Active thermal crease reset (no coating) (rank 6 of 7)
DEFECT | MAJOR | The heating schedule cannot do what the text claims. A 45 s soak at 45 °C, sped up 13–22×, equals only 10–17 min of recovery at 25 °C, not "hours". Recovering 1 h of set in 1 min needs about 60×, which by the idea's own WLF numbers means 60 °C, not 45 °C. | WLF recomputed: 45 s × 13.5–21.6 = 10–16 min
DEFECT | MAJOR | It breaks the "always invisible" constraint. After every long-closed opening the crease is at full depth until heat-up plus 45 s have passed, which is exactly when the user starts using the screen. | the design itself says it acts "after each long-closed opening"
DEFECT | MAJOR | The share of the crease that can recover is assumed, not measured. HTX's growth from 48 to 167 µm was never split into recoverable and permanent parts, and the idea admits it has no effect on PET/CPI set, metal yield or hinge steps. | HTX/ithinkdiff report depth only, with no recovery-versus-time data
DEFECT | MINOR | The 60 °C case sits at T−Tg = 90–100 K, which is the edge of where the universal WLF constants are valid, so the 60–120× figure is extrapolated. | Tg −30/−40 °C → T−Tg = 90–100 K
DEFECT | MINOR | The 70 J per event is right, but at 50 openings a day it costs 4.2% of the battery per day, not "0.08%". | 70 J ÷ 83.2 kJ (6 Ah × 3.85 V) = 0.084% per event
SURVIVES | The WLF speed-ups (13.5–21.6× at 45 °C, 61–122× at 60 °C) and the 0.084% per event reproduce.
RATIO | 0.99 | Firmware plus heater bus bars cost about $1–2. No reduction in crease visibility is shown, so the ratio per invisible-crease phone is undefined.
KNOWN | no | No shipping phone and no verified proposal found. Heat-assisted recovery of polymer set is textbook viscoelasticity, not a product.

IDEA 2: Tensioned-flat hinge with non-contact backstop (rank 2 of 7)
DEFECT | MAJOR | The non-contact gap is smaller than the tolerance it is meant to avoid. The 10–20 µm plate gap is less than the 50 µm plate height variance the idea itself quotes, so some plates will touch the foil at rest. A real clearance needs ≥60 µm, which lets a finger press travel 3–6× further. | OPPO: hinge height variance 0.05 mm ([OPPO](https://www.oppo.com/en/newsroom/press/oppo-launches-find-n6/))
DEFECT | MAJOR | The tension is set by a displacement of only 15–30 µm over 150 mm. That is smaller than the differential thermal expansion of an Al frame against glass, so the panel goes slack (and buckles) or runs at 3–5× design tension across normal temperatures. | T/(E·h)·L = 14.9–29.8 µm, against (23−8.5) ppm/K × 30 K × 150 mm = 65 µm
DEFECT | MAJOR | Even taking its own numbers, a Fold-type stack only drops to 6–12 µm, which is 3–6× above a ≤2 µm invisibility target. Alone it does not remove the crease. | the idea's own figures, 66 → 12/6 µm
DEFECT | MINOR | "Stiffer opening feel" is overstated: the elastic energy stored is about 2 mJ. The real cost is a sustained 150 N reaction through the hinge and frame. | 0.5 × 150 N × 30 µm = 2.2 mJ
DEFECT | MINOR | The precedent patent US 12487643 could not be found in my search, and "the Idea 1 stack" (1.7 µm) is really Idea 7's stack. | USPTO search returned other numbers
SURVIVES | For 70 µm glass, ℓ = 1.47–2.08 mm, 7.1–14.3 MPa, 75–150 N and the 0.37–0.73 mm unsupported press deflection all reproduce.
RATIO | 0.97 | Cam, toggle and a stiffer frame add about $5–10 per hinge. Crease reduction is 5–10× but not to invisibility.
KNOWN | partly | Hinges that manage display stretch and pull the screen flat when open are in the patent literature (US 12032416, US 12591272). No shipping phone holds 500–1000 N/m.

IDEA 3: Outward fold, 5.5 mm spine radius (rank 7 of 7)
DEFECT | FATAL | While the phone is closed, the user-facing glass is held in tension at 458 MPa for hours. With CS 750 MPa and DOL 10 µm, any flaw deeper than about 2.5 µm reaches net tension (+51 MPa at 3 µm, +165 MPa at 5 µm). Pocket quartz grit (Mohs 7, harder than glass) makes such scratches, so this is static fatigue under a sustained load, and drops land right on the pre-strained spine. | python: bending stress 458×(1−2z/70) minus a linear CS profile
DEFECT | MAJOR | Its central claim (fold over the body thickness, get no crease) has already shipped. Huawei's Mate Xs 2 folds outward at 11.1 mm, and reviewers still describe its crease as "not fully invisible". | [GSMArena](https://fo.gsmarena.com/huawei_mate_xs_2-review-2459p2.php), [Stuff](https://www.stuff.tv/?p=848428)
DEFECT | MINOR | It points to "Idea 1's bulb" and an "elastic-only stack" that are not part of this idea set (they belong to Idea 7), so the stack is undefined. | text cross-reference
SURVIVES | 0.64% strain and 458 MPa reproduce.
RATIO | 0.9 | It saves the cover display, but replacing exposed glass and the warranty cost dominate. It is no better than the Mate Xs 2 at removing the crease.
KNOWN | yes | Huawei Mate X / Xs / Xs 2 and the Royole FlexPai.

IDEA 4: Glass-carried thermally scheduled tension (rank 5 of 7)
DEFECT | MAJOR | "The OCA no longer carries the tension" is false. The shear-lag length (4.7–30 mm) is shorter than the 70 mm half-span, so the tension flows into the panel and any bonded Ti backing. The glass then keeps only about 45% of the tension, and the OCA carries a sustained 0.05–0.73 MPa of peak shear, which is near OCA strength at −20 °C. | λ = √(E·h·t/G); glass 3.6 MN/m vs Ti 4.2 MN/m
DEFECT | MAJOR | At 60 °C the design stretch is 5 µm, but 50 µm glass over 140 mm starts to buckle at 0.06 µm of compression. Any assembly or creep error of a few µm therefore turns tension into a visible wrinkle. | Euler (clamped) strain 4.2e-7 × 140 mm = 0.06 µm
DEFECT | MAJOR | It has no standalone value. It needs another design to deliver a residual crease of ≤10 µm, while measured shipping creases are 48–167 µm. | its own FAIL at 11,900 N/m
DEFECT | MINOR | The 239 MPa figure assumes 50 µm glass; with 70 µm glass it is 170 MPa. The thickness is never stated. | 11,900/50e-6 vs /70e-6
SURVIVES | 1.62 µm/K, a 130 µm swing, 3,482 N/m → 70 MPa and 522 N, about 1,590 N/m at 25 °C, and the filter formula w0(kℓ)²/(1+(kℓ)²) all reproduce.
RATIO | 0.96 | +$3–7 plus per-unit trimming of the tension. It helps only if paired with another idea.
KNOWN | partly | Bimetal and lever thermal compensation is standard in precision mechanics. Tension-when-flat appears in hinge patents. No shipping device uses it.

IDEA 5: Fluid-slip glass-leaf sandwich (rank 3 of 7)
DEFECT | MAJOR | The headline result does not reproduce. At the stated set of φ = 10% over the R = 2.5 mm arc (L = 7.85 mm), the crease is 1.7–2.5 µm deep with a 0.86–1.28 mrad slope. The claim is 0.3–0.7 µm and ≤0.27 mrad, so the slope is 2–3× over a 0.4 mrad target. The claimed values fit only φ ≈ 2%. | python: κs·(D_p/D_tot)·L²/8 and ·L/2
DEFECT | MAJOR | The top layer is bare 30 µm UTG with no polymer film. It has no anti-splinter layer, its pen-drop resistance is unknown, a crack would leak the optical fluid, and the minimum-CS margin is 80 MPa (500 against 420–432 MPa). | strain 0.6% × 72 GPa = 432 MPa
DEFECT | MAJOR | It needs a sealed fluid volume across the whole panel, with the FPC passing through a soft seal that sees 0.1–0.6 mm of edge sliding. Its drop and bubble reliability is undemonstrated, and silicone fluids dissolve large amounts of air, so bubbles can form under transient suction (I have not quantified this). | the design's own free-edge slip
DEFECT | MINOR | "70× flatter than the Duo" becomes 17–25× after the correction, and it is measured against the Duo instead of the flatter N6. | 21.7 mrad ÷ 0.86–1.28
SURVIVES | Strains of 0.6% and 0.4%, 432 MPa, and stiffness ratios of 0.008 (3 leaves) and 0.0055 (5 leaves) reproduce.
RATIO | 0.94 | +$20–60, about 3–9% of BOM. It is not yet invisible after the correction.
KNOWN | partly | Liquid optical bonding and fluid-lubricated layered stacks exist in the patent literature. No shipping foldable uses them.

IDEA 6: Centre-pinned capillary-wrung glass sandwich (rank 4 of 7)
DEFECT | MAJOR | The capillary clamp is miscalculated. In a connected oil body, the film pressure equals the pressure at the largest meniscus, which is in the 0.5 mm reservoir: 84 Pa, not 14 kPa (167× less). Scaling the idea's lift figures by that factor gives 8.7–35 µm. | 2γ/h: 0.042/3e-6 = 14 kPa vs 0.042/5e-4 = 84 Pa
DEFECT | MAJOR | An open oil edge rules out an IP rating. Dust of ≥3 µm in a 3 µm film shows as bumps, and epilame barriers stop static drops from spreading, not a film that folding pumps in and out. | 3 µm film thickness
DEFECT | MAJOR | The hard-stop tolerance of 0.02° (0.35 mrad) uses 87% of the 0.4 mrad visibility budget on its own. Frame flex and drop set have no margin left. | radians(0.02°) = 0.349 mrad
DEFECT | MINOR | The fold slip for 180° recomputes to 96–127 µm (claimed 64–112). The OLED substrate is yellow PI, not colourless PI, so the 0.5% set threshold is for the wrong material. | π × midplane spacing
SURVIVES | 0.36%, 514 MPa, a 111 µm stack, and 14 kPa (for the 3 µm film alone) reproduce. Hard-stop wear of about 1 nm is plausible by Archard's law.
RATIO | 0.97 | +$4–14, but an IP-rated version would need a seal the idea removes.
KNOWN | no | No product or proposal with an open-oil foldable stack was found.

IDEA 7: Glass-dominated elastic stack, 4 mm teardrop (rank 1 of 7)
DEFECT | MAJOR | The "calibration" fails. The Fold-type model tops out at 66 µm, but the measured aged Duo crease is 167 µm, so the model underpredicts by 2.5×. Applying that factor puts Idea 7 at up to 4.3 µm, over the 2 µm target, and φ is a free parameter spanning 5×. | [HTX via ithinkdiff](https://www.ithinkdiff.com/iphone-duo-crease-test-3000-folds/)
DEFECT | MAJOR | The baseline is the wrong one. The best shipping crease is the N6's (OPPO says it grows only 22 µm after 600k folds, against 165 µm for the Z Fold 7; unverified). Measured against the N6, the gain is 6.5–37×, not 30–100×. | [OPPO](https://www.oppo.com/en/newsroom/stories/oppo-find-n6-zero-feel-crease-foldable-innovation/); 11 ÷ 1.7–0.3
DEFECT | MAJOR | "Never in net tension" is true only at the surface itself. With CS 750 MPa and DOL 10 µm, the bending tension exceeds CS below about 2.5 µm depth (+51 MPa at 3 µm, +165 MPa at 5 µm). Add the bare 70 µm glass with no anti-splinter film, and fatigue and shatter risk are both understated. | python profile
DEFECT | MAJOR | The decoupled-layer model ignores the OCA held in shear. The shear-lag length is 35–112 mm and each half slips about 114 µm, so 25 µm of OCA sits at up to 460% shear while closed. At 90% recovery that leaves about 46% residual shear, a source of set the model does not include. | π/2 × 72.5 µm ÷ 25 µm
DEFECT | MINOR | A CPI panel substrate cannot survive LTPS processing (real panels use yellow PI). The ≤0.4 mrad threshold has no source. For comparison, HTX's new Duo slope of 0.097° is 1.69 mrad. | HTX
SURVIVES | 0.875% and 630 MPa for the UTG, 0.5% for the Ti, and the glass's roughly 77–80% share of bending stiffness reproduce.
RATIO | 0.97 | Similar BOM, a spine 2–3 mm thicker, and thicker UTG. This is the most credible route, but invisibility is not shown.
KNOWN | partly | Waterdrop hinges with flatness tuning are already shipping in the OPPO Find N6 (3D-printed Ti hinge, photopolymer levelling). Notebookcheck still saw a faint crease in some lighting ([Notebookcheck](https://www.notebookcheck.net/Oppo-Find-N6-review-finally-crease-free.1318522.0.html)).
NEW FACT | HTX: the new Duo's centre slope was 0.097°, rising to 1.245° after 3,000 folds | [ithinkdiff](https://www.ithinkdiff.com/iphone-duo-crease-test-3000-folds/)
NEW FACT | OPPO says the N6 crease grew 22 µm after 600k folds, against 165 µm for the Z Fold 7 (a manufacturer claim) | [OPPO](https://www.oppo.com/en/newsroom/stories/oppo-find-n6-zero-feel-crease-foldable-innovation/)
NEW FACT | The Mate Xs 2 is an outward fold at 11.1 mm whose crease reviewers still describe as visible | [Stuff](https://www.stuff.tv/?p=848428)

The Python checks are in /tmp/claude-0/-home-user-SomeRepository-engine-runs-vs-foldcrease-b-compare-r2/86b61a25-826d-5e99-8ce4-43b0688ac74a/scratchpad/chk.py. They use assumed material values (glass 72 GPa; PI 8 GPa; β-Ti 105 GPa; CS 750 MPa with a linear profile and DOL 10 µm; γ = 21 mN/m). The RATIO costs are rough estimates, not sourced figures.

Sources:
- [ithinkdiff – iPhone Duo crease test](https://www.ithinkdiff.com/iphone-duo-crease-test-3000-folds/)
- [OPPO Find N6 launch](https://www.oppo.com/en/newsroom/press/oppo-launches-find-n6/)
- [OPPO Engineering the Invisible](https://www.oppo.com/en/newsroom/stories/oppo-find-n6-zero-feel-crease-foldable-innovation/)
- [Notebookcheck Find N6 review](https://www.notebookcheck.net/Oppo-Find-N6-review-finally-crease-free.1318522.0.html)
- [GSMArena Mate Xs 2 review](https://fo.gsmarena.com/huawei_mate_xs_2-review-2459p2.php)
- [Stuff Mate Xs 2 review](https://www.stuff.tv/?p=848428)
- [US 12032416](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12032416)
- [US 12591272](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12591272)