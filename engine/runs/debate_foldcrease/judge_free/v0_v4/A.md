=== IDEAS ===
IDEA 1
NAME: Glass-dominated elastic stack, 4 mm teardrop
MECHANISM: A permanent crease needs a layer that takes a permanent set and is stiff enough to pull the rest of the stack out of flat. Glass at room temperature does not creep, and metals kept well inside their elastic range do not either, so the design puts no glassy polymer film anywhere in the fold zone. From top to bottom the stack is: 70 µm chemically strengthened UTG as the outermost surface, with only a nanometre-scale oleophobic layer, no PET, TPU or nano-texture film, and no AR or AG coating. Under it, a 25 µm high-recovery OCA with G ≈ 10⁴–10⁵ Pa and creep recovery ≥ 90%. Then a polarizer-less OLED panel about 25 µm thick (colour filter on the encapsulation, touch on the encapsulation, CPI substrate). At the bottom, a solid 40 µm β-titanium foil, with no lattice openings that could print through. The hinge is a teardrop with a minimum bend radius of 4 mm (the Fold 7's radius is unpublished; my guess is about 2 mm). At 4 mm the strains are: UTG 0.87%, or 630 MPa, which stays below a compressive stress of ≥ 750 MPa, so the glass surface never goes into net tension and stress-corrosion fatigue is suppressed. The panel sees 0.31%, well under the roughly 1% that TFTs tolerate. The Ti foil sees 0.5%, or 500 MPa, about 50% of yield. The glass provides about 80% of the bending stiffness, so it acts as the spring that pulls the stack flat. In my decoupled-layer model with a polymer set fraction φ = 2–10%, residual depth is 0.3–1.7 µm and slope is 0.07–0.35 mrad. A Fold-like stack in the same model (top polymer film, 45 µm UTG, R = 2 mm) gives 13–66 µm and up to 1.6°, which is the same order as HTX's measurement of the iPhone Duo (48 µm new, 167 µm and 1.24° after 3,000 folds). That agreement is what calibrates the model.
VALUE: The model predicts roughly 30–100× less residual depth than the best measured shipping crease (48→167 µm on the iPhone Duo, an unverified ~11 µm on the N6). That would bring it near the target of ≤ 2 µm and ≤ 0.4 mrad, where it can't be seen, without any masking. The cost is a spine about 2–3 mm thicker when folded (teardrop bulb about 8 mm across), and a bare glass surface that scratches and shatters more easily.

IDEA 2
NAME: Tensioned-flat hinge with non-contact backstop
MECHANISM: Over the last ~5° of opening, a cam pulls the panel's two ends apart and holds an in-plane tension T = 500–1000 N/m across the fold. Under tension, any leftover natural curvature κ₀ flattens to a depth of about (D/T)·κ₀ instead of κ₀L²/8, with a characteristic length ℓ = √(D/T) of about 1–2 mm. When the device is flat, the hinge plates sit 10–20 µm below the Ti foil without touching it, so their height variation (Oppo quotes 0.05 mm, which is 25× my depth target) can't print through to the screen at rest. The plates act only as a stop under a finger or stylus; without that stop, a 1 N press would deflect the span by about 0.2–0.7 mm. Computed effect: a Fold-like stack goes from 66 µm to 12 µm at 500 N/m and to 6 µm at 1000 N/m, and the Idea 1 stack goes from 1.7 µm to 0.1–0.2 µm. The added tensile stress in 70 µm glass is only 7–14 MPa. The hinge has to supply 75–150 N across a 150 mm wide panel. US 12487643 already describes a larger outward force on the display when going from folded to flat, so the principle is in the patent literature.
VALUE: Used with Idea 1, it gives a 5–10× safety margin that keeps the screen under the visibility threshold after creep has built up over 200k cycles or long periods folded. Fitted to current stacks, it gives about a 5–10× reduction, which on its own is not enough to make the crease invisible. The costs are hinge mass, a stiffer opening feel, and the risk of creep in the adhesive at the panel ends that carry the constant tension.

IDEA 3
NAME: Active thermal crease reset (no coating)
MECHANISM: Most of the crease that develops over time comes from viscoelastic set that can recover. HTX deliberately left the phones closed before rescanning, and the depth grew in that state. Recovery speeds up steeply with temperature. Using the universal WLF constants, going from 25 to 45 °C speeds recovery about 13–22× for an acrylic OCA or TPU with Tg between −30 and −40 °C, and going to 60 °C speeds it about 60–120×. A transparent heater (an ITO or metal-mesh trace already on the touch layer) warms the 19 × 150 mm fold zone to about 45 °C for about 45 s after each long-closed opening, while the Idea 2 tension is applied. That uses about 70 J, around 0.08% of a 6,000 mAh cell. The heater never runs while the phone is folded, because heat accelerates set in the folded state too.
VALUE: This is a firmware and heater add-on. It could pull a residual polymer crease below threshold within a minute instead of hours. It does nothing for set in glassy polymers like PET or CPI, plastic yield in the metal plate, or steps in the hinge, and it is the most speculative of the four ideas.

IDEA 4
NAME: Outward fold, 5.5 mm spine radius
MECHANISM: If the form factor isn't fixed, folding the screen outward over the full body thickness (about 11 mm folded, R ≈ 5.5 mm) gives 70 µm UTG a strain of 0.64% (460 MPa). Idea 1 needs a dedicated teardrop bulb to reach that radius. The same elastic-only stack and tensioning apply. The difference is that the outer glass surface, the one users touch, is in tension while the phone is closed. Its compressive layer has to stay above 460 MPa even after scratches, and the screen is exposed in the pocket.
VALUE: This gets close to Idea 1's crease physics without a bulb hinge. The price is much worse screen durability and protection, so it is a fallback, not the main recommendation.

=== NOTES ===
**Measuring "invisible" (targets, all relative to a flat control, measured across a 30 mm scan):**
- Depth: ≤ 2 µm peak-to-valley, by white-light interferometry or profilometry.
- Slope: ≤ 0.4 mrad (0.02°). That bends a reflected ray by ≤ 3 arcmin. For comparison, the iPhone Duo after folding measured 1.24°, about 55× this target.
- Reflection optical power: ≤ ~100 mD, by phase-measuring deflectometry.
- Luminance change along the fold: ≤ 1%, colour shift Δu′v′ ≤ 0.002.
- Human tests: a two-choice test (crease sample vs flat control) with ≥ 20 observers, screen on and off, a point light and a line grid, viewing angles 0–70°. A blind finger-swipe test run the same way. Pass means ≤ 55% correct for both.

**The 2,000-cycle assumption is wrong.** Samsung's 200k rating corresponds to about 100 folds a day for 5 years, so 2,000 cycles is about 3 weeks of use. Time spent folded is the bigger driver, since a phone is closed about 20 h a day.

**Test protocol:**
- 2,000 cycles at 25 °C, then continue to 200k and 500k cycles.
- Static folded holds: 72 h at 60 °C/90% RH, 72 h at −20 °C, then 500 h at 60 °C.
- Rescan 1 min, 1 h and 24 h after opening, to separate set that recovers from set that is permanent.

**What could break it:**
- Hot or humid folded storage (polymer and OCA creep).
- Cold opening (OCA stiffens; delamination; the edge "white" peel seen in cyclic cohesive-zone studies).
- Slow crack growth in the glass if a scratch cuts through the compressive layer.
- The Ti foil reaching its fatigue limit at 500k cycles at 50% of yield. This one is a real concern.
- Creep in the adhesive at the panel ends under constant tension.

**Trade-offs:**
- Spine 2–3 mm thicker; about 3–5 g more from glass, foil and cam.
- More expensive: thicker UTG plus a tensioning cam.
- Brighter, clearer image than a matte film (no haze, true blacks).
- The screen feels like glass and is stiff under a stylus.
- Bare glass is more prone to scratches and shattering, and there is no cheap $19 replaceable layer.

**Established vs speculative:**
- Established by data: the HTX measurements (secondhand, one source), Apple's statements, the strain formula ε = t/2R, glass not creeping at room temperature, and OCA property ranges from 3M and patents.
- Model, not data: φ, the 4 mm radius, the Fold 7's radius, perception thresholds, the tension result, and the WLF speed-ups.
- Needs FEA and a prototype: the real teardrop geometry, the coupled OCA response, and Ti fatigue.

**Correction on adhesive shear:** the OCA's shear slip equals layer separation × π, which comes to 170–310 µm (shear strain about 6) at any bend radius. A larger radius does not reduce it. Only a thinner stack, fast-recovering OCA, and tension help.

**Cheapest test of the central claim:** fold 70 µm UTG + OCA + CPI + Ti foil laminate strips around mandrels of R = 2, 3, 4 and 5 mm. Hold them 72 h at 60 °C, then measure depth and slope with a university white-light interferometer or a phone-camera deflectometry rig. Run a control strip with a 60 µm PET top film. Cost is a few hundred dollars. My model predicts ≤ 2 µm for the glass-only strip and tens of µm for the control.

**Comparison with the reported approaches:**
- **Apple:** reports describe Samsung Display's laser-drilled metal plate (Kuo), a crease under 0.15 mm in leaks, and a replaceable nano-texture polymer cover layer that Bergeron says is there to reduce the crease. My reading, which is speculation, is that this polymer layer is a likely cause of the 48→167 µm growth. Reviewers agree the crease can still be felt and is visible at some angles.
- **Samsung (Fold 7):** UTG 50% thicker than the Fold 6 and a third-generation hinge. A YouTuber's manual test found the crease visibly deeper by about 105k folds.
- **Oppo Find N6:** UTG 50% thicker, a 3D-printed titanium hinge with 0.05 mm height variation, and an 11% wider waterdrop. Oppo claims (with TÜV Rheinland) 82% less crease than the N5 and only +22 µm after 600k folds. Those are vendor numbers, and the ~11 µm figure is unverified. The N6 is the closest existing product to Idea 1, but it still has finite depth.

**On the brief itself:** the "about 0.7 mm" crease depth given for the Fold 7 is unsupported. Measured creases are 0.05–0.35 mm.

**Files** (in the working directory): `crease_model.py`, `crease_model.out`, `tension_heat.py`, `tension_heat.out`.

**Sources:**
[HTX via iThinkDiff](https://www.ithinkdiff.com/iphone-duo-crease-test-3000-folds/) · [MacRumors – Apple on crease](https://macrumors.com/2026/09/09/iphone-duo-crease/) · [MacRumors – replaceable layer](https://macrumors.com/2026/10/01/iphone-duo-cover-layer-is-replaceable) · [9to5Mac reviews](https://9to5mac.com/2026/10/22/iphone-duo-reviews-the-absolute-best-foldable-phone-but-not-without-compromise/) · [Trusted Reviews](https://www.trustedreviews.com/news/the-foldable-iphone-duo-still-has-a-crease-despite-what-apple-says) · [Macworld – laser-drilled plate](https://www.macworld.com/article/2848958/report-apples-folding-iphone-wont-have-a-crease-thanks-to-laser-drilled-plates.html) · [GSMArena leak <0.15 mm](https://m.gsmarena.com/iphone_folds_crease_size_detailed_in_new_leak-news-71722.php) · [Oppo newsroom](https://www.oppo.com/en/newsroom/stories/oppo-find-n6-zero-feel-crease-foldable-innovation/) · [Android Authority N6](https://www.androidauthority.com/oppo-find-n6-zero-feel-crease-durability-3648272/) · [NasiLemakTech N6 (22 vs 165 µm)](https://nasilemaktech.com/oppo-find-n6-review/) · [Samsung Fold 7 engineering](https://news.samsung.com/us/?p=79999) · [Fold 7 fold test](https://www.androidauthority.com/samsung-galaxy-z-fold-7-live-fold-test-3583522) · [US 12487643](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12487643) · [3M foldable OCA whitepaper](https://multimedia.3m.com/mws/media/1793258O/optically-clear-adhesives-for-foldable-oled-displays-whitepaper.pdf) · [US 12174665 OCA](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12174665) · [UTG CS patent 12167556](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12167556) · [Schott UTG](https://www.schott.com/en-in/applications/schott-utg-in-foldable-displays) · [Cyclic CZM OLED fatigue](https://www.sciencedirect.com/science/article/abs/pii/S0141938224003135)