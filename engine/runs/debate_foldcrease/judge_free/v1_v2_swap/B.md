=== IDEAS ===
IDEA 1
NAME: Tensioned neutral-plane glass sandwich, 5 mm teardrop
MECHANISM: The check found the decisive flaw in the old Idea 1. A soft OCA running at a shear strain of 4.5–6 takes a set, and that set locks the glass to a bonded Ti foil sitting 104 µm away. I accept this. With the check's own model the old design gives 4–114 µm. The fix is to remove the slipping layer entirely, not to soften it. The display becomes one symmetric plate, bonded throughout: 20 µm UTG / 3 µm glassy adhesive (Tg ≥ 120 °C) / 22 µm polarizer-less OLED (CPI, TFT, TFE, colour filter and touch) / 3 µm glassy adhesive / 20 µm UTG. The total is 68 µm. The top surface carries only an oleophobic layer, with no polymer film, AR or AG treatment. The OLED sits on the plate's neutral plane. Its strain is ≤ 0.22% and the adhesive's is ≤ 0.28% at R = 5 mm, against 450–600% shear in an OCA. The adhesive shear-lag length is 61 µm, so the layers act as one plate. Adhesive shear in the fold-zone transitions is about 1 MPa (0.08% strain). In the fold zone nothing is bonded underneath: no Ti, SUS or PET. The hinge has a teardrop with bulb R = 5 mm and reverse-curvature necks Rn = 8 mm, giving a 39 mm fold zone. Its plates rest 10–20 µm below the glass as a backstop for finger and stylus loads that never touches the glass. A preloaded spring (rate ≤ 210 N/mm, 0.36 mm preload) holds T = 500–1000 N/m across the fold when open. A spring is used instead of a cam because the frame-to-glass thermal mismatch is 20–71 µm, against a 6–13 µm tension stroke. Only the glass is stiff (99.5% of D = 1.76e-3 N·m), and glass is taken to be elastic. The polymers that can take a set carry only 0.46% of the bending stiffness. Modelled residual depth and slope: 3–13 µm and 0.3–1.2 mrad untensioned, falling to 0.10–0.42 µm and 0.04–0.16 mrad at 1000 N/m. That is for panel set φ of 5–20% and adhesive set of 2–10%. A deliberately pessimistic 50%/30% case gives 1.1 µm and 0.43 mrad (`sandwich.out`, `table.out`).
VALUE: Using the same coupled-beam logic and the same tension, this design comes out about 7–19× below the old Idea 1+2 (0.7–21 µm). It is about 150–1600× shallower than the aged iPhone Duo measured by HTX (167 µm, 21.6 mrad), and its slope is 4–40× below a new Duo (< 1.75 mrad). The price is a spine about 3 mm thicker (10 mm bulb), a new lamination process, and bare-glass impact risk that has not been measured.

IDEA 2
NAME: Same sandwich, outward fold
MECHANISM: The plate is symmetric, so it folds just as well outward around a body about 10 mm thick (R ≈ 5 mm) and needs no teardrop bulb. The crease physics and tension spring are unchanged, so the result is the same 0.1–0.4 µm with tension. The difference is that the 490 MPa tensile face is now the surface the user touches, and it stays loaded while the phone is folded. With CS 450–800 MPa and DOL 4–6 µm, a flaw 1.4–2.8 µm deep reaches the slow-crack-growth threshold, and one 2.6–3.4 µm deep breaks the glass (`glass_flaw.out`). Pocket scratches are that deep.
VALUE: The crease result is as good as Idea 1 and the spine is about 3 mm thinner. Scratch fracture and an exposed screen make it a fallback, not the main recommendation.

IDEA 3
NAME: Retrofit: single UTG, no metal under fold
MECHANISM: This keeps today's single-UTG panel architecture: 70 µm UTG over an OCA with a flat modulus versus temperature (G ≈ 10⁴ Pa), over the panel. The changes are that the support foil is unbonded in the fold zone and the Idea 1 spring and backstop are added. In the check's coupled model, run without the bonded foil, this gives 3.9–8.5 µm untensioned and 0.5–1.1 µm at 1000 N/m for φ 5–10% (`retrofit.out`, coarse grid). Two things limit it. The OCA still shears by 1.4–2.9. The panel takes 0.5–0.9% extra axial strain, rising to 1.2% if the OCA stiffens in the cold, which is above the roughly 1% that TFTs tolerate.
VALUE: Its depth is near Idea 1's and it needs less new process. However, cold opening threatens both the panel and the set, so it is second choice.

=== NOTES ===
**Response to the check, point by point**
- **(a) OCA set lock-in: accepted.** The old Idea 1 is replaced, not patched. The proposed fix, a G ≈ 100 Pa gel, is rejected. The softest datasheet value I found is Wacker LUMISIL 201 FLEX at G′ = 1–3 kPa. Optical gels list 35–40% elongation (Momentive OP1221, Dow VE-8001), while the required shear is about 6.5, so the gel would tear or cavitate. Bonding the panel stiffly at the neutral plane removes the slip altogether.
- **(b) Ti yield: accepted for the old stack.** It is moot now because no metal is bonded in the fold zone. Cold stiffening no longer matters either, since the adhesive is glassy and stiff at every temperature.
- **(c) Calibration: accepted.** φ was fitted to a point from a different device, and peak-to-valley values from different scan windows were mixed. I drop "calibrates the model". Comparisons now use slope as well as depth, and the new-Duo margin (4–40×) is stated separately from the aged-Duo margin.
- **(d) Thermal stroke: accepted.** A preloaded spring with rate ≤ 210–760 N/mm holds tension within ±20% over 35 K. The ends are anchored by a stiff epoxy clamp bar, which sees about 0.2 MPa of shear, instead of by an OCA.
- **(e) Threshold: accepted.** 0.4 mrad bends a reflected ray by 2.75 arcmin, which is above vernier acuity, so I no longer call it invisible. The new definition is in the next section.
- **(f) Standard, impact, necks:**
  - IEC 62715-6-22 is adopted for the measurement protocol; its 2nd edition was published 2026-06-03.
  - The necks are now modelled (Rn = 8 mm). There they put 306 MPa of tension on the user-facing surface. The fracture threshold is a flaw 3.5–4.7 µm deep.
  - Pen-drop and ball-drop performance is still unquantified and needs a test.
- **Where the check said I undersold the design:** tension is now part of the core design. It is worth about 16–30× here, because the 39 mm fold zone is much longer than the tension length √(D/T) = 1.3 mm. Ti fatigue is no longer an issue.

**What "invisible" means and the targets.** All measurements are taken at 1 min after opening, following the worst-case hold.
- **Primary, "physically absent":** inside a 40 mm window over the fold, RMS slope and RMS curvature are no more than 1.2× those of a non-fold reference zone on the same device. This uses phase-measuring deflectometry and white-light interferometry, per IEC 62715-6-22.
- **Absolute backstops:**
  - Depth ≤ 1 µm.
  - Slope ≤ 0.2 mrad (0.011°).
  - Luminance change ≤ 1%, Δu′v′ ≤ 0.002.
- **Touch:** detection thresholds for Gaussian bumps rise from about 1 µm at 0.15 mm width to 8 mm at 240 mm width, with exponent 1.3 (Louw et al. 2000). Interpolated, that is about 6 µm at 1 mm width and about 130 µm at 10 mm. The target is ≤ 1/5 of the threshold at the measured width.
- **Context:** Park et al. (AHFE 2023) found that creases under 60 µm were rated "good", but "good" is not "invisible".
- **Human tests:** a two-choice test with ≥ 30 observers, about 200 trials per condition. Conditions: screen off (mirror) and on, a line grid and a point source, 0–70°, and a blind finger swipe. Pass means the result is not significantly above chance at a power able to detect 60% correct.
- **Coating rule:** the device must pass with no AR or AG coating.

**Persistence testing**
- **Cycling:** 2,000 cycles at 25 °C, then checkpoints at 20k, 200k and 500k.
- **Static folded holds:** 10 days at 25 °C (3M's static-fold criterion), 72 h at 60 °C/90% RH, 500 h at 60 °C, and 72 h at −20 °C, opened while still cold.
- **Rescans:** at 1 min, 1 h and 24 h after opening.
- **Spring tension:** logged from −20 to 60 °C.
- **Impact:** drop tests before and after cycling.
- **What breaks it:**
  - Humid heat lowering the adhesive's Tg.
  - Anelastic relaxation in the glass, which is assumed to be zero. Even 10⁻⁴ would equal the whole panel contribution.
  - Spring loss. Without tension the crease reverts to 3–13 µm.
  - Flaws deeper than about 2 µm on the inner faces of the glass.
- **2k versus 500k cycles:** the glass sees 0↔490 MPa per fold. If no flaw reaches K_th, cracks don't grow and cycle count doesn't matter. Viscoelastic set scales with time held folded, not with cycles. I therefore predict the same result at 2k and 500k, but that is not tested. 2,000 cycles is only about 3 weeks of use at 100 folds a day.

**Failure modes and trade-offs**
- **Glass flaw tolerance:** at the bulb of the R = 5 mm sandwich, the slow-growth flaw size is 1.4–2.8 µm. For a shipping-like 30 µm UTG at R = 1.5 mm it is 0.3–1.7 µm. The Fold radius is unpublished, so this is an assumption. The sandwich is therefore no worse than current glass, and its tensile face is on the protected inside.
- **Glass stress:** 490 MPa applied. With the 450 MPa CS that a patent sets as the minimum for 30 µm UTG, that leaves net tension at the surface. Specify CS ≥ 600 MPa, or use R = 6 mm (408 MPa).
- **Thickness:** spine about 12–13 mm against a body of about 9 mm (estimate). The R = 4/6 mm variant gives about 10 mm and 0.12–0.52 µm, at the cost of less flaw tolerance.
- **Mass:** the 40 µm of glass weighs about 2 g, the same as a single 50 µm UTG. Dropping the cover film saves 2–3 g. The hinge and spring add about 3–6 g (estimate).
- **Optics:** brighter and clearer than matte, with no haze. Bare glass reflects about 4%.
- **Touch and stylus:** the screen feels like glass. Its stiffness is about that of 66 µm of glass, and the backstop gives a firm stylus feel.
- **Cost and repair:** a new glass-panel-glass lamination step. There is no $19 peel-off layer.

**Established versus model**
- **Established data:** ε = c/R, HTX's 48→167 µm and 1.24° (single secondhand source), the gel datasheets, the UTG CS patent, Louw's thresholds, and Apple's and Oppo's own statements.
- **Model only:** the φ values, the zero anelasticity of glass, the teardrop's own shape (an elastica in a cavity, which needs FEA), clamped-end flatness, and every crease number above.

**Cheapest decisive experiment.** Bond strips of 20–30 µm UTG / 3 µm epoxy / 25 µm CPI / 3 µm epoxy / UTG. Run three controls alongside: a bare UTG strip to bound glass anelasticity, the old 70 µm UTG + OCA + CPI + Ti strip, and a strip with a PET top film. Wrap them on R = 4 and 5 mm mandrels and hold 72 h at 60 °C. Then clamp them flat, with and without a 20 N hanging weight (1000 N/m on 20 mm), and profile them at 1 min, 1 h and 24 h. The cost is a few hundred dollars plus glass samples.
- **Predicted:** sandwich 3–13 µm untensioned and ≤ 0.4 µm tensioned; old strip 4–114 µm.
- **Kill criterion:** if the untensioned sandwich exceeds 13 µm, the central claim fails.

**Comparison with shipping approaches**
- **Apple:**
  - Reports describe a laser-drilled metal support plate (Kuo).
  - Leaks put the crease under 0.15 mm.
  - A replaceable nano-texture polymer cover layer ($19 with AppleCare+) is presented as reducing the crease, which matches the asker's account.
  - HTX measured 48 µm new and 167 µm after folding. Reviewers say the crease can still be felt and seen at some angles.
  - My unverified hypothesis is that the polymer cover takes a set and drives the growth.
- **Samsung Fold 7:** UTG 50% thicker and a new hinge. In a manual fold test the crease was visibly deeper by about 105k folds.
- **Oppo Find N6:**
  - UTG 50% thicker and a 3D-printed titanium hinge whose height variation drops from 0.2 to 0.05 mm.
  - Oppo and TÜV Rheinland claim up to 82% less crease than the N5 after 600k folds.
  - Oppo says "Zero-Feel Crease" describes a visual effect, not physical absence.
  - One review reports 22 vs 165 µm; I could not re-verify it.
  - All three still bond polymer layers and a plate across the fold, which is the mechanism Idea 1 removes.

**On the brief:** the "about 0.7 mm" depth for the Fold 7 has no source. The best public measurement is HTX's 48–167 µm on the iPhone Duo.

**Files:** all scripts and outputs are in `/home/user/SomeRepository/engine/runs/debate_foldcrease/round1/`: `sandwich.py`/`.out`, `table.py`/`.out`, `glass_flaw.py`/`.out`, `retrofit.py`/`.out`, `haptic.out` and `README.md`.

Sources:
- [HTX via iThinkDiff](https://www.ithinkdiff.com/iphone-duo-crease-test-3000-folds/)
- [MacRumors – replaceable layer](https://macrumors.com/2026/10/01/iphone-duo-cover-layer-is-replaceable)
- [Tom's Guide – Duo layer](https://www.tomsguide.com/phones/iphones/apple-reveals-iphone-duo-has-a-replaceable-display-layer-what-it-means-for-you)
- [9to5Mac reviews](https://9to5mac.com/2026/10/22/iphone-duo-reviews-the-absolute-best-foldable-phone-but-not-without-compromise/)
- [Macworld – laser-drilled plate](https://www.macworld.com/article/2848958/report-apples-folding-iphone-wont-have-a-crease-thanks-to-laser-drilled-plates.html)
- [GSMArena leak](https://m.gsmarena.com/iphone_folds_crease_size_detailed_in_new_leak-news-71722.php)
- [Oppo newsroom](https://www.oppo.com/en/newsroom/stories/oppo-find-n6-zero-feel-crease-foldable-innovation/)
- [Android Authority N6](https://www.androidauthority.com/oppo-find-n6-zero-feel-crease-durability-3648272)
- [Tom's Guide N6](https://www.tomsguide.com/phones/android-phones/i-have-been-testing-oppo-find-n6-crease-free-foldable-phone)
- [Fold 7 fold test](https://www.androidauthority.com/samsung-galaxy-z-fold-7-live-fold-test-3583522)
- [IEC 62715-6-22:2026](https://ccn-scc.ca/standardsdb/standards/2058735)
- [Park et al., AHFE 2023](https://openaccess.cms-conferences.org/publications/book/978-1-958651-47-6/article/978-1-958651-47-6_25)
- [Louw et al. 2000](https://link.springer.com/doi/10.1007/s002210000350)
- [Corning SID crease metric](https://sid.org/Portals/sid/Files/SID-Digest/docs/77-5.pdf)
- [UTG CS/DOL patent 12167556](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12167556)
- [Wacker LUMISIL 201 FLEX](https://wacker.com/h/en-us/medias/LUMISIL-201-FLEX-UV-AB-en-2024.07.31.pdf)
- [Momentive OP1221](https://www.momentive.com/docs/default-source/tds/invisisil/invisisil-op1221-uv-curable-silicone-gel.pdf)
- [Dow VE-8001](https://www.designworldonline.com/dow-launches-new-silicone-adhesive-for-flexible-foldable-displays/)
- [3M foldable OCA whitepaper](https://multimedia.3m.com/mws/media/1793258O/optically-clear-adhesives-for-foldable-oled-displays-whitepaper.pdf)
- [US 12174665](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12174665)
- [US 12487643](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12487643)

**HONEST GAIN:** For Ideas 1+2 the modelled crease is 0.10–0.42 µm and 0.04–0.16 mrad at 1000 N/m for realistic set, and 1.1 µm in the pessimistic case. That is 7–19× below the corrected old design and ≥ 150× below the aged iPhone Duo. It comes from removing the slipping adhesive and the bonded metal, not from softer parameters. It is still a model; the strip test decides it.