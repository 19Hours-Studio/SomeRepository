=== REVIEW ===
IDEA 1: Spectrum-matched drumhead hinge
DEFECT | FATAL | The value claim needs the set to fall from the author's own "today ≈8%" to below 2.1–3.7% just because R grows from 1.5 to 4.5 mm, but no data shows that, and in linear viscoelasticity the set fraction does not depend on strain. | My code, with the implied D = 2.44e-4 N·m, half-wave over the arc πR and w₀ = fπ²R/8: at R = 4.5 mm, f = 8% and T = 1000 N/m the residual is 5.3 µm and 1.2 mrad, which is 5× the ≤1 µm / ≤0.5 mrad target. Moving to R = 4.5 mm also raises the untensioned w₀ from 148 to 444 µm at the same f.
DEFECT | MAJOR | The adhesive creep margin is 1.12 (9.4 kPa against a 10.5 kPa test stress), with no test temperature or hold time given; at 40–60 °C in a pocket the creep rate of acrylic OCA rises by orders of magnitude. | 10.5/9.4 = 1.117.
DEFECT | MAJOR | The tension works only at full flat. At any partial angle (the cam releases "before folding starts"), and at flex-mode angles, the untensioned set is visible: 148 µm at R = 1.5 mm or 444 µm at R = 4.5 mm if f = 8%. | My w₀ calculation.
DEFECT | MAJOR | The thickness cost is understated. A bulb of 2R = 8–10 mm plus two display stacks and two cover walls gives a spine of about 11–12 mm, against the Fold 7's 8.9 mm folded, which is the market's reference point. | 2×4.5 mm + 2×0.3 mm + 2×0.6 mm ≈ 10.8 mm minimum.
DEFECT | MINOR | "Flattening needs 3.9 kN/m" does not reproduce from the author's own kill numbers. | Fitting w/w₀ = 0.165 and slope/amplitude = 697 m⁻¹ gives 2.25 kN/m for 1 µm, 3.2 kN/m for 0.5 mrad, and 4.6 kN/m for 0.5 µm.
DEFECT | MINOR | The ≤1 µm / ≤0.5 mrad target is not tied to any measured visibility threshold, and there is no 2000-cycle test plan with a sample size. | A zero-failure claim at 99% reliability and 95% confidence needs n = ln0.05/ln0.99 = 298 units.
SURVIVES | Glass strain 0.048% (rounded to 0.04%), 150 N total, the 9.6–56 kN/m requirement at R = 1.5 mm (I get 16 kN/m at f = 8%), and the Ti thermal case: a 49 µm mismatch over 60 K against 71 µm of elastic elongation can be absorbed by a constant-force spring.
RATIO | ≈0.99 | $1,999 phone against +$8–20 per phone. Neither side has a verified crease-free unit, so the "undefined" baseline is rhetoric. Against Oppo's claimed result (82% depth reduction, "no visible crease" after 600k folds, a manufacturer claim) it is a cost add for an unproven gain.
KNOWN | yes | Apple EP 4738056 A1 (tension assembly in the flat state) and Huawei-style US 12541230 (tension assembly pushes brackets apart to flatten the display); LG US 20240215189 (magnetic tension). https://www.goveda.com/patent/EP-4738056-A1 , https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12541230
NEW FACT | The iPhone Duo is $1,999 and Apple discloses no fold-cycle rating; reviewers still see the crease off-axis. | https://www.macrumors.com/2026/10/07/iphone-duo-hands-on/ , https://www.notebookcheck.net/iPhone-Duo-does-have-a-visible-crease-despite-Apple-s-clever-nano-texture-surface.1395055.0.html

IDEA 2: Floating glass on fluid
DEFECT | FATAL | A free fluid film under 30 µm glass has no long-wavelength restoring force. With the phone upright the fluid drains to the bottom, the top region goes dry and atmospheric pressure presses the glass onto the panel, so the panel's crease prints through: the same failure as the dropped vacuum version. | Hydrostatic Δp over 150 mm = 1.6 kPa, against glass stiffness Dk⁴ = 32 Pa/m at λ = 300 mm, so the glass is not rigid and the "0.27 mrad tilt" (= 40 µm/150 mm, a rigid-plate full-drain wedge) is a lower bound. Drain time over 75 mm is 2.9 h at 0.05 Pa·s and 5.8 h at 0.1 Pa·s, i.e. overnight on a vertical stand.
DEFECT | MAJOR | After every opening the crease is visible until the fluid levels, and the levelling time grows with viscosity and feature width. This breaks "invisible" at the moment of use. | Thin-film plate model τ = 12μ/(h³Dk⁶): λ = 10 mm gives 7–15 s at 0.05–0.1 Pa·s, 59 s at 0.4 Pa·s (cold; the viscosity factor is assumed), and 470–940 s for a 20 mm-wide set.
DEFECT | MAJOR | The 20 µm gap is smaller than any plausible panel set at R = 3 mm. Where the set is a ridge, the glass rides on it; only valleys can be filled. | w₀ = fπ²R/8 = 74 µm at f = 2% and 296 µm at f = 8%, against a 20 µm gap.
DEFECT | MAJOR | Finger or stylus holds squeeze the film within about a second and leave a dimple that recovers slowly; "stylus within limits" has no number. | Rigid-disk Stefan bound: a 1 N press over 10 mm halves the gap in 0.55 s at 0.05 Pa·s.
DEFECT | MINOR | Bare 30 µm UTG with no top film, over a liquid, is a shatter and leak hazard. Samsung and Apple both keep a top layer, and the Fold 7 / N6 glass is reportedly thicker. | About 0.46 mL of oil in 20 µm × 145 × 160 mm; Oppo glass "50% thicker than UTG".
DEFECT | MINOR | The pinned meniscus has to survive 149 µm of contact-line travel per fold without ingesting air. That is about 0.6 m of cumulative travel over 2000 cycles with nothing validating it, and the "2.5% bonded stack" baseline is a strawman, since real stacks already decouple with soft OCA. | 149 µm × 2 × 2000.
DEFECT | MINOR | The cost baseline (+$5–15) is the author's own unsourced estimate. | —
SURVIVES | 0.34 N/m buckling (L ≈ 69 mm pinned), slip πd = 149 µm with d ≈ 47 µm, interface reflectance 4.3e-5 at Δn = 0.02, glass bending strain 0.50% (350 MPa), and the thermal dome (1.1 µm of fluid expansion over 60 K).
RATIO | ≈1.0 nominal (+$2–6 on $1,999), but effectively <1 | Drain and print-through mean it does not deliver crease-free units, so cost per spec-meeting phone is undefined for the idea too.
KNOWN | partly | Index-matched fill polymers in UFG recesses (TDCommons disclosure) and Apple's liquid-deposited polymer in a glass groove. I found no free-liquid full-area layer. https://www.tdcommons.org/dpubs_series/8090 , https://m.gsmarena.com/apple_patents_a_foldable_display_with_no_creases_for_iphone_and_ipad-amp-61917.php
NEW FACT | Samsung Display reportedly gets about 20% crease reduction for the Fold 8 from UTG changes, which means the competent baseline keeps moving. | https://www.trendforce.com/news/2026/01/20/news-samsung-reportedly-achieves-20-crease-reduction-with-utg-galaxy-z-fold-8-apple-weigh-adoption

IDEA 3: Per-layer sub-creep strain budget
DEFECT | FATAL | The "measured no-set strain" is cited but never sourced, and below yield the set curvature fraction does not fall with strain, so a 0.30% strain cap does not make the residual curvature zero. The stack's residual curvature is roughly the polymer stiffness share times the polymer set fraction. | 2.4% × (30–50% set, assumed) = 0.7–1.2% of 1/R, which gives 37–62 µm free-standing depth at R = 4.2 mm. That is roughly the 60 µm level a 17-prototype study graded only "good", not invisible.
DEFECT | MAJOR | "Elastic and recovers" leaves out the recovery time. Viscoelastic recovery runs in log time and is comparable to the hold time, so after an overnight fold the crease is present at opening. | Supporting NEW fact, not relied on: Choi et al. (2021) report residual strain in CPI decaying ∝ log t, with a critical radius ≈5 mm.
DEFECT | MINOR | The 25 µm cap is silent on the circular polarizer and panel sub-layers, so it implicitly needs a polarizer-free colour-filter panel, and removing the PET protector removes shatter retention. | —
DEFECT | MINOR | The cost basis is internally inconsistent. | 7/0.08 implies a $87.5 hinge; 33/0.47 implies $70.
DEFECT | MINOR | A 10.2 mm spine with a 2R = 8.4 mm bulb leaves ≤0.9 mm per side for display stack plus wall. | 10.2 − 8.4 = 1.8 mm.
SURVIVES | 25 µm/(2×4.2 mm) = 0.298%; per-layer bending about each layer's own mid-plane is valid with soft interlayers; a polymer share of 2.4% is plausible (25 µm CPI alone ≈ 4.7% of a 30 µm UTG pair).
RATIO | ≈0.99 | +$7–33 on $1,999, with no evidence of spec-meeting yield.
KNOWN | partly | Low-strain CPI and large-R waterdrop hinges are standard practice; the "R above the critical residual-strain radius" idea is in Choi et al. 2021. https://koreascience.or.kr/article/JAKO202102455512209.pdf
NEW FACT | Oppo's N6 hinge cuts height variance from 0.2 to 0.05 mm by laser-scanning parts and 3D-printing liquid polymer fill; this is a support-flatness lever the idea ignores. | https://www.androidauthority.com/oppo-find-n6-zero-feel-crease-durability-3648272

IDEA 4: Glass-tendon tensioned clothoid hinge
DEFECT | MAJOR | √(D/T) = 0.57 mm uses a D close to UTG alone, but the set sits in the panel, back film and support plate, whose stiffness adds through the gel. Tripling D breaks the target. | Implied D = 6.5e-4 against 5.6e-4 for 45 µm UTG. Over a 13.4 mm arc+ramp, 180 µm leaves 3.2 µm / 0.74 mrad at D = 6.5e-4, but 9.1 µm / 2.1 mrad at 3D.
DEFECT | MAJOR | The model is calibrated to 60–150 µm creases and then extrapolated 70× down. The ≤180 µm envelope is below the only Fold 7 figure in circulation, and the gel thickness that must take the depth difference is not stated. | The task's ~0.7 mm figure (unconfirmed) is 3.9× the envelope. A 25–50 µm gel would need a 3.6–7.2× thickness change.
DEFECT | MAJOR | The tension acts only at full flat, so partial-angle use shows the raw crease. | —
DEFECT | MINOR | Sustained 44 MPa membrane tension, fed through cut glass edges in Ti rails, adds to the central tension of strengthened UTG, and the static fatigue of the grip edge is untested. | Assuming CS = 700 MPa and DOL = 5 µm: CT rises from 100 to 144 MPa.
DEFECT | MINOR | The ≤5 µm / ≤1 mrad target is not tied to a visibility threshold, and there is no sample size. | n = 298 for 99%/95% zero-failure.
SURVIVES | 44.4 MPa, 0.063%, 300 N, $13–50 = 16–71% of a $70–80 hinge, folded bending stress 525 MPa at R = 3 mm (in line with current practice), and gel cavitation (~5 kPa) is well above the ~0.25 kPa needed to hold the panel flat.
RATIO | ≈0.98 | +$13–50 on $1,999. The "no meaningful ratio" claim fails because Oppo claims "no visible crease" after 600k folds (TÜV-tested, depth −82% vs N5), which is unverified but not zero.
KNOWN | yes | Apple EP 4738056 A1 and Huawei-style US 20240069604 (more outward force when flat to speed crease recovery). https://patents.justia.com/patent/20240069604
NEW FACT | A 2026 IEC 62715-6-22 edition defines crease and waviness measurement, and a SID paper uses phase-measuring deflectometry (<30 s per scan), which would be the cheapest way to test all four ideas. | https://www.technickenormy.cz/publicdoc/iec_previews/4247157.pdf , https://sid.org/Portals/sid/Files/SID-Digest/docs/77-5.pdf

Ranking, least to most damaged: Idea 4, then Idea 1, then Idea 3, then Idea 2. The checks are in `calc.py` in the audit folder; nothing else was touched.

Sources:
- [Android Authority – Oppo Find N6](https://www.androidauthority.com/oppo-find-n6-zero-feel-crease-durability-3648272)
- [Mobile World Live – Oppo Find N6](https://www.mobileworldlive.com/oppo/oppo-irons-out-foldable-crease-with-find-n6/)
- [MacRumors – iPhone Duo hands-on](https://www.macrumors.com/2026/10/07/iphone-duo-hands-on/)
- [Notebookcheck – iPhone Duo crease](https://www.notebookcheck.net/iPhone-Duo-does-have-a-visible-crease-despite-Apple-s-clever-nano-texture-surface.1395055.0.html)
- [PhoneArena – Fold 7 crease](https://www.phonearena.com/news/foldable-iphone-crease-against-galaxy-z-fold-7_id178585)
- [CMS/AHFE crease visibility study](https://openaccess.cms-conferences.org/publications/book/978-1-958651-47-6/article/978-1-958651-47-6_25)
- [SID Digest deflectometry](https://sid.org/Portals/sid/Files/SID-Digest/docs/77-5.pdf)
- [IEC 62715-6-22 preview](https://www.technickenormy.cz/publicdoc/iec_previews/4247157.pdf)
- [EP 4738056 A1](https://www.goveda.com/patent/EP-4738056-A1)
- [US 12541230](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12541230)
- [US 20240069604](https://patents.justia.com/patent/20240069604)
- [LG US 20240215189](https://patents.justia.com/patent/20240215189)
- [TDCommons index-matched fill](https://www.tdcommons.org/dpubs_series/8090)
- [GSMArena Apple groove patent](https://m.gsmarena.com/apple_patents_a_foldable_display_with_no_creases_for_iphone_and_ipad-amp-61917.php)
- [TrendForce Fold 8 UTG](https://www.trendforce.com/news/2026/01/20/news-samsung-reportedly-achieves-20-crease-reduction-with-utg-galaxy-z-fold-8-apple-weigh-adoption)
- [Choi et al. 2021 CPI residual strain](https://koreascience.or.kr/article/JAKO202102455512209.pdf)