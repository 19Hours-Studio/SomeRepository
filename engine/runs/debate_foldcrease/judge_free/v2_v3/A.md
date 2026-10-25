=== IDEAS ===
IDEA 1
NAME: Tensioned neutral-plane glass sandwich with a long-ramp teardrop (v2)

MECHANISM:
- **Display stack, 76 µm.** From the top:
  - oleophobic layer only, with no polymer film and no AR or AG coating;
  - 20 µm UTG (CS ≥ 700 MPa, DOL about 3 µm, so CT is about 150 MPa);
  - 3 µm glassy adhesive (Tg ≥ 120 °C);
  - 30 µm polarizer-less OLED (CPI, TFT, OLED, TFE, colour filter and touch);
  - 3 µm glassy adhesive;
  - 20 µm UTG.
- **Panel thickness.** The panel is now 30 µm, up from 22 µm, per the check. One patent stack gives 15 µm PI, about 4 µm TFT, about 1 µm OLED and 0.4–2.5 µm TFE, before colour filter and touch.
- **Why little can set.** The OLED sits on the neutral plane. At the bulb (R = 5.5 mm) the glass is at 0.69% strain (497 MPa), the panel faces at 0.27% and the adhesive at 0.33%. The glass carries 99.22% of D = 2.37e-3 N·m. The polymers that can take a set carry only 0.78%.
- **Fold zone.** Nothing is bonded under the fold zone.
- **Hinge (new).** The teardrop's curvature changes linearly over 15 mm ramps, bulb to neck and neck to flat, instead of in steps. The geometry was re-solved so the fold still closes to a 0.4 mm gap:
  - bulb radius R = 5.5 mm, bulb width 11.3 mm;
  - peak neck radius 20 mm;
  - fold-zone arc 70 mm, against 39 mm before.
  The user-facing glass at the necks drops from 306 to 137 MPa.
- **Tension (raised).** A preloaded spring pack engages at full open and releases on folding. It sets T = 3000 N/m: 450 N across 150 mm, 71 MPa membrane stress in the glass and 0.10% axial strain in the panel.
  - Spring rate ≤ 1270 N/mm with ≥ 0.36 mm preload holds ±20% over the 35 K aluminium-vs-glass mismatch.
  - Opening work is about 30 mJ.
- **Backstop.** It sits 60–100 µm below the glass (the check's point), so it never touches the glass at rest.

**Why the crease vanishes.** In tension the residual shape copies the fold's curvature profile, scaled by the tension length l² = D/T:
- depth = Σ(φᵢDᵢ)·Δκ/T;
- slope = Σ(φᵢDᵢ)·max|κ′|/T.

Long ramps cut max|κ′| by about 10×. Higher T cuts both depth and slope.

Modelled results, 1 min after the worst hold (`design3.out`, 15/15 mm ramps, T = 2000 → 3000 N/m):

| Polymer set (panel/adhesive) | Glass set φ_g | Depth (µm) | Slope (mrad) |
|---|---|---|---|
| 5% / 2% | 0 | 0.09 → 0.06 | 0.006 → 0.004 |
| 20% / 10% | 0 | 0.36 → 0.24 | 0.025 → 0.016 |
| 20% / 10% | 1e-3 | 0.62 → 0.42 | 0.043 → 0.029 |
| 20% / 10% | 3e-3 | 1.15 → 0.77 | 0.079 → 0.053 |
| 50% / 30% (pessimistic) | 0 | 0.92 → 0.62 | 0.063 → 0.042 |

- **Face-up gravity sag.** It adds ≤ 0.017 mrad at T = 3000. The worst-case sum for the 20/10 row is 0.025 mrad at T = 3000 and 0.019 mrad at T = 4000 (`sag_combo.out`).
- **Spring failure.** With the spring broken (T = 0) the crease is 9–39 µm, and 67–185 µm with glass set. That is a visible crease of shipping-phone size.

VALUE: Like-for-like against round 1 corrected to a 30 µm panel (critic: 0.89–0.97 µm and 0.30–0.335 mrad at T = 1000):
- depth is 4× lower and slope 20× lower;
- at equal T = 1000, the ramps alone give 6.6× on slope.

Against the aged iPhone Duo measured by HTX (167 µm, 21.6 mrad) this is about 700× shallower and about 1300× lower in slope. Against a new Duo (48 µm) it is about 200× shallower.

It meets the absolute 0.024 mrad backstop for the crease alone only if glass delayed elasticity is φ_g ≤ 6e-4 (realistic polymer set) or ≤ 1.7e-3 (low polymer set). That number is unknown, and it is now the central risk.

IDEA 2
NAME: Same sandwich, outward fold

MECHANISM: The plate is symmetric, so it can wrap outward around an 11 mm body with the same 15 mm ramps. There are no reverse-curvature necks, so Δκ = 1/R. Max κ′ is 12,100 m⁻² instead of 15,440 m⁻², so the crease is about 0.8× that of Idea 1, and the bulb disappears. The cost is that the user-facing glass is under 497 MPa while folded. A flaw 1.4–1.5 µm deep then grows slowly, and one 1.8–2.0 µm deep breaks the glass (`checks2.out` B). Pocket scratches are that deep.

VALUE: Best crease of the three and a thinner spine. Exposed-glass fracture risk makes it a fallback.

IDEA 3
NAME: Retrofit: single UTG over OCA, no metal under the fold

MECHANISM: Today's 70 µm UTG / OCA / panel stack, with the support foil unbonded in the fold zone, plus the tension spring and backstop. The check re-ran it and confirmed:
- 3.9–8.5 µm untensioned;
- 0.5–1.1 µm at 1000 N/m;
- panel axial strain 0.46–0.93%, rising to 1.21% if the OCA stiffens in the cold.

The ramp and T = 3000 levers have not been re-run for this stack.

VALUE: Needs the least new process. A 1.2% cold-opening strain is above the roughly 1% that TFTs tolerate, so it stays second choice.

=== NOTES ===
**Response to the check, point by point**
1. **Panel thickness of 22 µm was optimistic: accepted.** The baseline is now 30 µm, with R raised to 5.5 mm to keep the glass at about 500 MPa. All headline numbers use 30 µm. A 40 µm panel roughly doubles depth and slope (`design2.out`).
2. **Slope target was inconsistent with my own vernier argument: accepted.** The absolute slope backstop is now ≤ 0.024 mrad, which is 10″ of reflected deviation for a line target in the worst orientation. The old 0.2 mrad target is withdrawn.
   - I also report the stricter line-curvature literature: sagitta thresholds of 2–4″, which is 0.006–0.011 mrad. Only the low-set row meets that.
   - Context: patent limits for display glass are WCA ≤ 0.10–0.15 µm in the 0.8–8 mm band. That allows local slopes of 0.12–0.37 mrad, and even WCA 0.03 µm gives 0.04–0.07 mrad (`checks2.out` F). Ordinary flat glass screens therefore do not meet the hyperacuity bound either. That is why the primary criterion is relative to the non-fold area, as defined below.
3. **Glass anelasticity was assumed zero: accepted, and it is now the main risk.**
   - Zerodur shows delayed elasticity at room temperature of up to about 1% of the applied deformation, fully reversible over weeks, and attributed to its alkali content. Corning reports none measurable for alkali-free ULE.
   - Ion-exchanged UTG is rich in alkali. φ_g of 1e-3 to 1e-2 is therefore plausible. This is not measured.
   - At φ_g = 1e-2 the design gives about 2 µm and 0.13 mrad: far below shipping phones, but not invisible.
   - The strip test below now measures φ_g directly.
4. **Central tension was ignored: accepted and recomputed.**
   - With CS 700 / DOL 3 µm, CT is 150 MPa. The worst net tension anywhere in the bottom sheet (what an edge flaw sees) is 608 MPa. A shipping-like 30 µm UTG sees 519–663 MPa at R = 1.5–2 mm.
   - The surface flaw that starts slow growth is 1.48 µm deep on the sandwich's inner face, against 0.80–1.45 µm for the shipping-like UTG.
   - So the sandwich is comparable to current glass. CS 450 / DOL 6 µm is excluded because it reaches 756 MPa.
5. **Backstop gap: accepted.** The gap is now 60–100 µm. A 1 N finger deflects the tensioned span by about 120 µm, so the glass lands on the backstop at 0.5–0.8 N. Lighter touches float on a span of about 8 N/mm.
6. **Pessimistic and untensioned cases fail: stated.** The pessimistic and untensioned cases are in the Idea 1 numbers, and spring loss brings back a visible crease.

On the summary's 0.024 mrad point: Idea 1 now reaches 0.016 mrad at T = 3000 when φ_g = 0, and 0.019 mrad including sag at T = 4000.

The "1.75 mrad new Duo" figure had no source and is dropped. I took the check's undersold points:
- smooth ramps;
- 7–50× like-for-like against round 0;
- HTX's 48→167 µm growth happening within 3000 folds, which supports the claim that set depends on time held folded rather than on cycle count;
- higher T;
- polymer recovery while the phone is open.

**What "invisible" means and the targets.** All measurements are taken 1 min after opening, following the worst-case hold, using deflectometry and white-light interferometry per IEC 62715-6-22 (2nd edition, 2026).
- **Primary, "physically absent":** inside a 70–80 mm window over the fold, slope and curvature filtered to the 0.8–20 mm band are no more than 1.2× those of a non-fold zone on the same device.
- **Absolute backstops:**
  - depth ≤ 0.5 µm;
  - local slope ≤ 0.024 mrad;
  - luminance change ≤ 1%, Δu′v′ ≤ 0.002.
- **Touch:** ≤ 1/5 of Louw's threshold at the measured width. At about 15 mm width the threshold is ≥ 100 µm, so 0.3 µm is far below it.
- **Human tests:** a two-choice test with ≥ 30 observers, screen off and on, line-grid and point-source reflections at 0–70°, plus a blind finger swipe. Pass means not significantly above chance, with power to detect 60% correct.
- **Coating rule:** the device must pass with no AR or AG coating.

**Persistence testing**
- **Cycling:** 2,000 cycles, then checkpoints at 20k, 200k and 500k.
- **Static folded holds:** 10 days at 25 °C, 72 h at 60 °C/90% RH, 500 h at 60 °C, and 72 h at −20 °C, opened while still cold.
- **Duty cycle:** 14 days of 8 h folded per day. Glass delayed elasticity with time constants of weeks would build up under this pattern.
- **Rescans** at 1 min, 1 h and 24 h after opening. **Tension** logged from −20 to 60 °C.
- **Drop tests:** pen drop and ball drop before and after cycling. These are still unquantified.
- **2k versus 500k cycles:** set depends on time held folded, not on fold count. Glass cycles 0↔497 MPa at the bulb and 0↔137 MPa at the necks, so it is cycle-insensitive while flaws stay below about 1.4 µm. The adhesive at 0.33% strain sits well below typical epoxy fatigue strains. I predict the same result at 2k and 500k; neither has been tested.
- **What breaks it:** glass delayed elasticity, humid-heat lowering of the adhesive's Tg, spring stress relaxation (residual depth scales with 1/T), and flaws on the glass faces.

**Failure modes and trade-offs**
- **Thickness:** a bulb 11.3 mm wide gives a folded spine of about 13–14 mm (estimate).
- **Hinge space:** the 70 mm fold zone means the hinge cavity reaches about 25–35 mm into each half, which takes battery space.
- **Frame load:** the frame must carry 450–600 N in compression.
- **Mass:** about 2.3 g of glass; the spring and frame add 5–10 g (estimate).
- **Optics:** no haze. Bare glass reflects about 4%. A thin bonded glass may print through panel topography uniformly across the whole screen; that is not a crease, but it is untested.
- **Touch:** a glass feel, with a slightly "trampoline" response below about 0.5 N.
- **Cost and repair:** a new glass-panel-glass lamination step and no peel-off layer.

**Established versus model**
- **Established data:**
  - ε = c/R;
  - HTX 48→167 µm (secondhand);
  - Zerodur and ULE delayed elasticity;
  - UTG CS patent;
  - display-glass WCA patents;
  - Louw's touch thresholds;
  - line-curvature thresholds;
  - vendor statements.
- **Model only:**
  - every φ value and φ_g;
  - the ramped-teardrop shape (an elastica in a cavity, which needs FEA);
  - clamp flatness;
  - the membrane estimate for finger load;
  - all crease numbers.

**Cheapest decisive experiment (a few hundred dollars plus glass).** Wrap strips on R = 5.5 mm mandrels for 72 h at 60 °C and for 14 days at 25 °C:
- bare ion-exchanged UTG, the same glass without ion exchange, and alkali-free glass;
- the sandwich (20/3/30/3/20);
- the old UTG + OCA + Ti stack.

Release the strips and measure end deflection at 1 min, 1 h and 24 h. eff = κ_res·R. φ_g = 6e-4 gives about 50 µm of tail deflection, so it is easy to resolve. Then clamp the sandwich strips flat under 20–60 N of hanging load and profile them.
- **Kill criterion:** if the sandwich's eff > 2.0e-3, or if φ_g > 1.7e-3, the 0.024 mrad target cannot be met at T ≤ 3000 N/m.

**Comparison with shipping approaches**
- **Apple iPhone Duo:**
  - Reports describe a laser-drilled support plate.
  - A replaceable nano-texture cover layer ($19 with AppleCare+) is presented as reducing the crease. Apple does not claim the crease is gone.
  - HTX measured 48→167 µm within 3000 folds.
- **Samsung Galaxy Z Fold 7:** thicker UTG and a new hinge. In a live fold test the crease was deeper by about 105k folds.
- **Oppo Find N6:**
  - Thicker UTG and a 3D-printed titanium hinge whose height variation drops from 0.2 to 0.05 mm.
  - Oppo claims 82% less crease after 600k folds. Its "Zero-Feel" refers to a visual effect, not physical absence.
- **All three** still bond polymer films and a plate across the fold, with step-like curvature and no tension. Those are the three levers Idea 1 changes.
- **On the brief:** the "0.7 mm" depth for the Fold 7 has no source.

**Files:** in `round2/`: `design2.py`/`.out`, `design3.py`/`.out`, `checks2.py`/`.out`, `sag_combo.py`/`.out`, and `README.md`.

Sources:
- [HTX via iThinkDiff](https://www.ithinkdiff.com/iphone-duo-crease-test-3000-folds/)
- [MacRumors – replaceable layer](https://macrumors.com/2026/10/01/iphone-duo-cover-layer-is-replaceable)
- [Tom's Guide – Duo layer](https://www.tomsguide.com/phones/iphones/apple-reveals-iphone-duo-has-a-replaceable-display-layer-what-it-means-for-you)
- [9to5Mac reviews](https://9to5mac.com/2026/10/22/iphone-duo-reviews-the-absolute-best-foldable-phone-but-not-without-compromise/)
- [Macworld – laser-drilled plates](https://www.macworld.com/article/2848958/report-apples-folding-iphone-wont-have-a-crease-thanks-to-laser-drilled-plates.html)
- [Oppo newsroom](https://www.oppo.com/en/newsroom/stories/oppo-find-n6-zero-feel-crease-foldable-innovation/)
- [Android Authority N6](https://www.androidauthority.com/oppo-find-n6-zero-feel-crease-durability-3648272)
- [Fold 7 fold test](https://www.androidauthority.com/samsung-galaxy-z-fold-7-live-fold-test-3583522)
- [IEC 62715-6-22](https://ccn-scc.ca/standardsdb/standards/2058735)
- [Louw et al. 2000](https://link.springer.com/doi/10.1007/s002210000350)
- [Zerodur delayed elasticity (SPIE 1533)](https://electronicimaging.spiedigitallibrary.org/conference-proceedings-of-spie/1533/0000/Delayed-elasticity-in-Zerodur-at-room-temperature/10.1117/12.48857.full)
- [Zerodur modelling (SPIE 8450)](https://nanolithography.spiedigitallibrary.org/conference-proceedings-of-spie/8450/84504P/ZERODUR-for-stressed-mirror-polishing-II--improved-modeling-of/10.1117/12.924989.full)
- [Line-curvature threshold study (SWOV)](https://swov.nl/nl/publicatie/perception-curvature)
- [Display-glass waviness, US 8835335](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8835335)
- [Display-glass waviness, US 8049860](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8049860)
- [Panel layer thicknesses, US 10490758](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10490758)
- [UTG CS/DOL, US 12167556](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12167556)
- [US 12487643](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12487643)
- [GANA FB18-08 (optical distortion in heat-treated glass)](https://glass.org/sites/default/files/2023-06/FB18-08_2023_Methods_Measuring_Optical_Distortion_Heat-Treated_Flat_Glass.pdf)

**HONEST GAIN:** For a realistic 30 µm panel with 20/10% polymer set, the modelled crease falls from 0.97 µm and 0.335 mrad (round 1 corrected, T = 1000) to 0.24 µm and 0.016 mrad. That is 4× on depth and 20× on slope, about 700× shallower than the aged iPhone Duo. The gain comes from the 15 mm curvature ramps (6.6× on slope at equal T) and from T = 3000 N/m. It meets the 0.024 mrad criterion only if the glass's delayed set is φ_g ≤ 6e-4. That is unmeasured, and the strip test decides it.