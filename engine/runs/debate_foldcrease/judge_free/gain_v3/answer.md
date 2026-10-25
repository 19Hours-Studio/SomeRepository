=== IDEAS ===

IDEA 1
NAME: A tensioned neutral-plane glass sandwich on a precision-seated hinge, with a servo-held gas cushion (v3)

MECHANISM:

**Display stack, 76 µm.** It is unchanged from v2. From the top:
- an oleophobic layer only, with no polymer film and no AR or AG coating;
- 20 µm UTG (CS 700 MPa, DOL 3 µm, CT 150 MPa);
- 3 µm glassy adhesive (Tg ≥ 120 °C);
- 30 µm polarizer-less OLED panel;
- 3 µm glassy adhesive;
- 20 µm UTG.

The bottom glass face gets two things that are new:
- a 2 µm siloxane hard coat;
- a metal or ITO sense electrode under that coat. The panel emits upward, so this layer is not in the optical path.

**Why little can set.** The OLED sits on the neutral plane. The glass carries 99.2% of D = 2.37e-3 N·m. The polymers that can take a set carry 0.78%. Nothing is bonded under the fold zone.

**Fold geometry (changed).** In v2 the two curvature ramps were 15/15 mm, but the bulb-to-neck ramp carries 4.7× more curvature change than the neck-to-flat ramp. Balancing them gives the new geometry: R = 5.5 mm, ramps 25/9 mm, Rn = 16.7 mm.
- The fold zone stays at 71 mm (70 mm before).
- The bulb width grows from 11.3 to 12.5 mm.
- The peak curvature gradient drops from 15,430 to about 9,800 m⁻² (`ramp_grid.out`, `lever3.out`).

**Tension.** T = 4000 N/m, which is 600 N across the 150 mm display width.
- It comes from a flexure-carriage spring of 800–1200 N/mm with 0.5–0.75 mm of preload.
- The carriage is released by a cam over the last degrees of opening. That takes about 65 mJ of cam work, and the glass stores 33 mJ. This corrects the 30 mJ I gave in v2 and updates the check's 15 mJ to 600 N.
- The open glass carries 94 MPa of membrane stress. Its core then sits at a sustained 244 MPa (CT + membrane), so the edges must be ion-exchanged after cutting.

**Hinge (new): this is where the check's missing budget went.**

1. *Lamination in the seated pose, under load.* The hinge is burned in for about 1000 cycles. It is then seated open with the service 600 N applied by a fixture. The sandwich is bonded to the wing plates through a gap-filling structural adhesive while its face is held on a reference flat. Absolute angle and height errors of the halves are therefore absorbed by the adhesive wedge. Only repeatability after each re-seat remains.

2. *Kinematic open-state seat.*
   - The 600 N compression between the halves is carried through hard contacts: Si₃N₄ on WC, radius ≥ 10 mm, Hertz peak 2.6 GPa (`checks3.out` E).
   - These contacts lie in the glass mid-plane, with eccentricity e ≤ 0.05 mm, so the frame load cannot bow the wings.
   - The open angle is set by a tongue in each frame rail. The tongue reaches 30 mm into the other half and seats on a pad there, so the angular lever is 30 mm rather than a 4 mm detent.

3. *Hinge housing in AlSiC* (α ≈ 8 ppm/K, k ≈ 180 W/m·K) instead of aluminium.
   - Its CTE matches the glass, so tension drifts by only 0.2–0.3% over 35 K, against ±20% in v2.
   - Its α/k is 29× lower than titanium's, which suppresses through-thickness thermal bow.

4. *Servo-held gas cushion.* This replaces the v2 vented cavity.
   - A rigid bridge rises at the end of opening. It stops 5 ± 2 µm below the glass and seals the gap at the y-edges with a light lip.
   - The bridge carries a 0.2 mm silicone skin (E ≈ 1 MPa).
   - The trapped air is about 2,800× stiffer than the tensioned glass for mean deflection. Moving the bridge therefore moves the glass's mean height 1:1.
   - Piezo stacks under the bridge (a stroke of about 1 µm is needed) servo the mean gap to a target. The gap is read by a 22 nF capacitor between the bottom-glass electrode and the bridge; 1 nm of gap is 200 ppm of capacitance, or 0.007 Pa.
   - This cancels gravity sag, thermal gas expansion and barometric change together.
   - The cushion re-zeroes at ambient pressure on every fold.

   Why a servo: a passively sealed cushion locks in the sag present at the moment it seals, so it is no better than venting. That gives 0.038 mrad in `budget3.out`.

**Why the crease vanishes.** In tension the residual shape copies the fold's curvature profile, divided by T: slope ≈ Σ(φᵢDᵢ)·max|κ′|/T, with a tension length l = √(D/T) = 0.77 mm. The edges and the loads are now part of the budget, as follows.

**Full slope budget.** Values are taken 1 min after the worst hold, using one script for both v2 and v3 hardware (`budget3.out`).
- Clamp-line feature = seat kink + bow + thermal bow + lamination residual + span slope 3l inside the clamp.
- Interior feature = crease + residual pressure.

| Case | Crease (interior) | Pressure | Seat kink | Bow | Worst feature |
|---|---|---|---|---|---|
| v2 hardware, nominal (my assumed tolerances: 2 µm on a 4 mm detent, Al ±20%, e = 1 mm, vented 1 Pa) | 0.0164 | 0.028 | 0.39 | 0.086 | **0.51 mrad** |
| v2 hardware, pessimistic | 0.029 | 0.13 | 0.98 | 0.34 | **1.45** |
| **v3 nominal** (φ_g = 0, seat σ = 0.1 µm at 3σ, e = 0.05 mm, servo residual 0.05 Pa) | 0.0074 | 0.0005 | 0.0122 | 0.0029 | **0.0197** |
| v3 nominal, φ_g = 1e-3 | 0.0129 | 0.0005 | 0.0122 | 0.0029 | 0.0212 |
| v3 nominal, φ_g = 3e-3 | 0.0238 | 0.0005 | 0.0122 | 0.0029 | 0.0243 (fails) |
| v3, servo off (passive sealed) | 0.0236 | — | 0.0122 | 0.0029 | 0.038 (fails) |
| v3, seat σ = 0.25 µm (QKC after wear-in) | 0.0074 | 0.0005 | 0.030 | 0.0029 | 0.038 (fails) |
| v3, Ti housing instead of AlSiC | 0.0074 | 0.0005 | 0.0122 | 0.0029 (+0.0049 thermal bow) | 0.024 (marginal) |
| **v3 pessimistic** (φ_g = 1e-3, σ = 0.5 µm, e = 0.2 mm, EI = 5, 0.6 Pa) | 0.017 | 0.006 | 0.061 | 0.050 | **0.123** (fails) |
| Option: R = 7 mm, 35/10 mm ramps, 50 mm tongue | 0.0056 | 0.0005 | about 0.009 | 0.0029 | 0.0152 |

**Limits in the nominal hardware** (`phig_limit.out`, `seat_limit.out`):
- Glass set: φ_g ≤ 2.8e-3 for the slope target and ≤ about 2.3e-3 for the depth backstop of ≤ 0.5 µm. Depth is 0.33 µm at 1e-3 and 0.60 µm at 3e-3.
- Seat repeatability: σ ≤ 0.135 µm per contact (3σ ≤ 0.41 µm).
- Load-path eccentricity: ≤ 0.125 mm.
- With R = 7 mm, φ_g ≤ 5e-3.

**Spring failure** (T = 0): a crease of 9–39 µm, or 67–185 µm with glass set. That is a crease of shipping-phone size.

VALUE: On the same budget code, the worst visible feature falls from 0.51 mrad to 0.020 mrad at nominal tolerances (26×) and from 1.45 to 0.12 mrad at pessimistic ones (12×). The v2 hardware tolerances are my assumptions, and they are kind to v2.
- Nominal v3 meets the 0.024 mrad target with 18% margin.
- Pessimistic v3 does not: it is 5× over.
- On the material-set crease alone, like-for-like: 0.0164 → 0.0074 mrad (2.2×).

IDEA 2
NAME: The same stack and hinge without electronics (vented or passively sealed cavity)

MECHANISM: Everything in Idea 1 except the piezo servo. Gravity sag then stays at q·a/T = 0.023 mrad face-up. A passive seal locks in the sag present when it closes; it only rejects changes after that.

VALUE: 0.038–0.040 mrad nominal (`budget3.out`): about 1.6× over target, but 13× better than v2 hardware. It is the fallback if the servo cannot be justified, and its residual sits at the seams and comes mostly from gravity.

IDEA 3
NAME: Outward fold, the same sandwich

MECHANISM: There are no reverse-curvature necks, and the crease is about 0.8× that of Idea 1. The cost is that the user-facing glass carries 497 MPa while folded. A 1.5 µm scratch then grows slowly and a 2 µm scratch breaks it. It has the same seat and edge budget as Idea 1.

VALUE: The interior crease is slightly lower than Idea 1's. Exposed-glass fracture risk keeps it a fallback. The v1–v2 retrofit (single UTG over OCA) is dropped: its cold-opening panel strain of 1.2% exceeds what TFTs tolerate, and the new levers were not re-run for it.

=== NOTES ===

**Response to the check, point by point**

1. **Gravity sag breaks the headline: accepted.** The v2 worst sum at T = 3000 was 0.0246 mrad, not 0.025 "meeting" the target. Raising T alone is a poor fix, because sag only falls as 1/T. The servo-held cushion cuts the net uniform load to 0.05 Pa, a pressure term of 0.0005 mrad. I also checked a passive seal: it fails (0.038 mrad), because it freezes whatever sag exists at the moment it seals.

2. **Edges of the free span: accepted. This was the largest error in v2, at 0.5–1.5 mrad by my estimate.** I reproduce the check's kink = δ/2 + Δh/2a. The fixes are:
   - lamination in the seated pose under service load, so absolute errors drop out;
   - a kinematic seat with a 30 mm angular lever;
   - an in-plane load path with e ≤ 0.05 mm, so bow = ΔF·e·L/EI;
   - an AlSiC housing, which brings ΔF from ±20% to 0.3% thermal plus 2% spring relaxation.

   I also add a term the check missed: through-thickness thermal bow, κ = α·q″/k. In titanium at 100 W/m² it is 0.0049 mrad, which alone takes the budget to the edge of failure. In AlSiC it is 0.0002 mrad.

   Seat repeatability is now the binding term. The nominal case needs σ ≤ 0.135 µm. Sources:
   - Schouten et al. (1997) report < 0.1 µm at 1.5 kN of preload;
   - Culpepper's quasi-kinematic coupling repeats to 0.25 µm after wear-in;
   - dust, wear and phone-scale preload are untested.

3. **Air pressure: accepted.** The v2 vented cavity needed |ΔP| ≤ 1 Pa. The servo removes the conflict with sealing: the cavity is sealed while open and re-zeroes on each fold. Piezo stroke needed (`checks3.out` D):
   - 0.34 µm for 20 K;
   - 0.18 µm for a 3600 Pa change (a 300 m elevator ride);
   - 0.40 µm for a gravity flip.

   The seal may leak no more than 3 mm³/h (R ≥ 1.7e12 Pa·s/m³), or 8 h of holding uses up 2 µm of stroke.

4. **Unprotected bottom face: accepted.**
   - The face now looks into a sealed, dust-free 5 µm gap over soft silicone, behind a 2 µm hard coat.
   - A particle 5–20 µm proud is pushed by the tensioned glass with 14–56 mN, and it sinks 290–460 µm into a 1 MPa skin. It embeds rather than tenting the glass or flawing it.
   - Hinge wear debris must be kept out of the gap by the seal.
   - The sustained open-state core tension of 244 MPa is a new edge-strength risk that I am now stating. Edges must be ion-exchanged after cutting. A residual risk remains.

5. **The touch test defined away pressing: accepted.**
   - The free travel is now about 5–8 µm. The glass lands on the skin at 0.05–0.09 N, and 1 N adds about 1 µm of skin compression.
   - Added test: indentation compliance from 0.1 to 2 N, fold versus non-fold, within ±20%.
   - Added: a blind press test and a stylus drag test.
   - Whether 5–8 µm of pre-travel is felt is unmeasured.

6. **PolyU EML 71, 102219 (2024): accepted.** It reports macroscopic plastic creasing in ion-exchanged UTG, with recovery inhibited by longer holds *and* by repeated loading. I withdraw "2k = 500k". φ_g may grow with cycle count. The mechanism (mixed-alkali anelasticity in the ion-exchanged layer) is my speculation. The folding radius and stress in that study are unknown to me; I have only the abstract.

7. **700×/1300× was unfair: accepted.** Ranges replace it. Model against measured is not like-for-like.
   - Depth 0.19–0.60 µm (φ_g 0–3e-3) against 167 µm for the aged Duo: 280–880×.
   - Worst slope 0.020–0.12 mrad (nominal to pessimistic) against 21.6 mrad: 180–1100×.

8. **The strip test cannot resolve its signal: accepted.** A horizontal tail of bare UTG sags 1035 µm under its own weight. The signal is 49 µm at φ_g = 6e-4 and 8 µm at 1e-4. The fix: hang the strips vertically, where gravity acts along the length and the tension length (57 mm) is longer than the 30 mm tail. Measure the tip's lateral offset as a before/after difference.

**Points the check said I undersold, now taken:**
- **R as a lever:** at R = 7 mm the worst feature is 0.015 mrad and φ_g ≤ 5e-3, at the cost of a 16.4 mm bulb. It is offered as an option.
- **Opening work:** recomputed above for 600 N.
- **Recovery while open:** still not credited, which is conservative.

**What "invisible" means, and the targets.** These are unchanged except for press feel. Measure 1 min after the worst-case hold, with deflectometry and white-light interferometry per IEC 62715-6-22.
- **Primary:** inside a window over the fold, slope and curvature in the 0.8–20 mm band are no more than 1.2× those of a non-fold zone on the same device. The fold window must now be 90 mm wide, because the clamp lines at ±41.7 mm must fall inside it.
- **Absolute backstops:**
  - depth ≤ 0.5 µm;
  - local slope ≤ 0.024 mrad (10″ reflected) at every line feature, both the interior and each clamp line;
  - luminance change ≤ 1%, Δu′v′ ≤ 0.002.
- **Touch:** swipe topography ≤ 1/5 of Louw's threshold. Press compliance within ±20% of the non-fold zone.
- **Human tests:** a two-choice test with ≥ 30 observers, screen off and on, line-grid and point-source reflections at 0–70°, plus blind swipe and press. Pass means not significantly above chance.
- **Coating rule:** the device must pass with no AR or AG coating.

**Persistence testing**
- **Cycling:** 2k cycles, then checkpoints at 20k, 200k and 500k. At each checkpoint, rescan and also measure seat repeatability with capacitive probes. Seat wear is now a first-order risk.
- **Static holds:** 10 days at 25 °C, 72 h at 60 °C/90% RH, 500 h at 60 °C, and −20 °C opened while still cold.
- **Duty cycle:** 14 days of 8 h folded per day. This tests the PolyU effect of hold time combined with repeated loading.
- **Rescans:** at 1 min, 1 h and 24 h after opening.
- **Servo-off and spring-off runs.**
- **Seal leak rate and drop tests:** before and after cycling. Drop is still unquantified.
- **What breaks it:**
  - φ_g > 2.3e-3;
  - seat σ > 0.135 µm, from wear, fretting or dust;
  - load-path eccentricity > 0.125 mm;
  - spring relaxation;
  - seal leaks;
  - adhesive Tg loss in humid heat;
  - glass flaws > 1.5 µm on the bulb face or > 2.7 µm on the user face at the necks (164 MPa folded).

**Failure modes and trade-offs**
- **Thickness:** a 12.5 mm bulb gives a folded spine of about 14–15 mm (estimate). R = 7 mm gives about 18 mm.
- **Hinge space:** the hinge cavity reaches about 25–35 mm into each half.
- **Frame load:** 600 N of compression in the frame.
- **Mass:** about 2.3 g of glass, plus 8–15 g for the spring, bridge, piezos and AlSiC (estimate).
- **Power:** mW-level while open for the piezos and capacitance sensing (estimate).
- **Cost:** glass-panel-glass lamination, a lapped ceramic seat, burn-in, seated lamination, a servo and a seal. Much more than current hinges. There is no cheap peel-off repair.
- **Optics:** no haze, about 4% bare-glass reflection, and possible uniform print-through of the panel (untested).
- **Feel:** glass to the touch, with 5–8 µm of pre-travel in the fold zone.

**Established versus model**
- **Established (sourced):**
  - ε = c/R;
  - HTX 48→167 µm (secondhand);
  - PolyU plastic creasing in UTG (abstract only);
  - Zerodur and ULE delayed elasticity;
  - kinematic-coupling repeatability of 0.1–0.25 µm under lab conditions;
  - display-glass waviness patents;
  - Louw's touch thresholds;
  - the IEC method;
  - vendor statements.
- **Model or assumption:**
  - every φ and φ_g;
  - seat σ in a phone;
  - the EI of a phone half (5–10 N·m²);
  - hinge heat flux (100–300 W/m²);
  - the servo residual;
  - the v2 hardware tolerances;
  - the elastica-in-cavity geometry (needs FEA; the solver has spurious branches, which I filter);
  - all crease numbers.

**Cheapest decisive experiments**
1. **Glass set** (a few hundred dollars). Wrap strips on R = 5.5 mm mandrels for 72 h at 60 °C, for 14 days at 25 °C, and for 2k cycles. Use:
   - ion-exchanged UTG, the same glass without ion exchange, and alkali-free glass;
   - the 20/3/30/3/20 sandwich.

   Hang them vertically and measure the tip offset at 1 min, 1 h and 24 h; eff = κ_res·R. **Kill criterion:** φ_g > 2.3e-3.
2. **Seat bench.** Two AlSiC blocks with Si₃N₄/WC contacts under 600 N, capacitive probes, and 10k re-seats with dust exposure. **Kill criterion:** σ > 0.135 µm.
3. **Tensioned-strip rig.** Vary the wing angle and height with shims and measure by deflectometry. This checks kink = δ/2 + Δh/2a and the kink width l = 0.77 mm.

**Comparison with shipping approaches**
- **Apple iPhone Duo:**
  - reports describe a laser-drilled support plate;
  - a replaceable nano-texture cover layer ($19 with AppleCare+) that reduces the crease's visibility; Apple does not claim the crease is gone;
  - HTX measured 48→167 µm within 3000 folds, which means set builds with use.
- **Samsung Galaxy Z Fold 7:** thicker UTG and a new hinge. The crease deepened by about 105k folds in a live test.
- **Oppo Find N6:** thicker UTG and a 3D-printed titanium hinge whose height variation drops from 0.2 to 0.05 mm. Oppo claims 82% less crease after 600k folds. "Zero-Feel" refers to a visual effect, not physical absence.
- **All three** bond polymer films and a plate across the fold, with no tension and no µm-level open-state seat. Oppo's 50 µm hinge flatness is about 100× coarser than the 0.4 µm (3σ) that this budget needs.
- **The cost:** this design trades their simplicity and thin spine for a precision-instrument hinge.
- **On the brief:** the 0.7 mm Fold 7 depth still has no source.

**Files:** all in `round3/`:
- `lever3`, `ramp_grid`, `budget3`, `phig_limit`, `seat_limit`, `checks3` (`.py` and `.out`);
- `README.md`.

Sources:
- [HTX via iThinkDiff](https://www.ithinkdiff.com/iphone-duo-crease-test-3000-folds/)
- [MacRumors – replaceable layer](https://macrumors.com/2026/10/01/iphone-duo-cover-layer-is-replaceable)
- [Tom's Guide – Duo layer](https://www.tomsguide.com/phones/iphones/apple-reveals-iphone-duo-has-a-replaceable-display-layer-what-it-means-for-you)
- [9to5Mac reviews](https://9to5mac.com/2026/10/22/iphone-duo-reviews-the-absolute-best-foldable-phone-but-not-without-compromise/)
- [Macworld – laser-drilled plates](https://www.macworld.com/article/2848958/report-apples-folding-iphone-wont-have-a-crease-thanks-to-laser-drilled-plates.html)
- [Oppo newsroom](https://www.oppo.com/en/newsroom/stories/oppo-find-n6-zero-feel-crease-foldable-innovation/)
- [Android Authority N6](https://www.androidauthority.com/oppo-find-n6-zero-feel-crease-durability-3648272)
- [Fold 7 fold test](https://www.androidauthority.com/samsung-galaxy-z-fold-7-live-fold-test-3583522)
- [PolyU – plastic deformation and recovery in UTG (EML 2024)](https://research.polyu.edu.hk/en/publications/plastic-deformation-and-recovery-in-ultrathin-aluminosilicate-gla/)
- [Delayed elasticity origin (Glass Europe)](https://www.tib-op.org/ojs/index.php/glass-europe/article/view/3253)
- [Zerodur delayed elasticity (SPIE 1533)](https://electronicimaging.spiedigitallibrary.org/conference-proceedings-of-spie/1533/0000/Delayed-elasticity-in-Zerodur-at-room-temperature/10.1117/12.48857.full)
- [Schouten 1997 kinematic coupling](https://wp.optics.arizona.edu/optomech/wp-content/uploads/sites/53/2016/10/Schouten-1997.pdf)
- [Willistein report (Culpepper QKC, Slocum)](https://wp.optics.arizona.edu/optomech/wp-content/uploads/sites/53/2016/10/WillisteinReport1.pdf)
- [Quasi-kinematic coupling patent US 6193430](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6193430)
- [IEC 62715-6-22](https://ccn-scc.ca/standardsdb/standards/2058735)
- [Louw et al. 2000](https://link.springer.com/doi/10.1007/s002210000350)
- [Line-curvature threshold (SWOV)](https://swov.nl/nl/publicatie/perception-curvature)
- [Display-glass waviness, US 8835335](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8835335)
- [UTG CS/DOL, US 12167556](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12167556)
- [Panel layers, US 10490758](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10490758)
- [US 12487643](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12487643)

**HONEST GAIN:** Counting every term the check raised, plus thermal bow, with one script for both designs, the worst visible feature drops from 0.51 to 0.020 mrad at nominal tolerances (26×) and from 1.45 to 0.12 mrad at pessimistic ones (12×). Nominal v3 meets the 0.024 mrad target; pessimistic misses by 5×.
- **Where the gain comes from:**
  - a seated, kinematic, in-plane hinge seat (edge kink 0.39 → 0.012 mrad);
  - an AlSiC housing;
  - a servo-held gas cushion (sag and pressure 0.028 → 0.0005 mrad);
  - balanced 25/9 mm ramps with T = 4000 (crease 0.0164 → 0.0074 mrad).
- **Tolerable glass set:** up to 2.3e-3, against 6e-4 before.
- **Still unproven:** invisibility rests on two unmeasured numbers, φ_g ≤ 2.3e-3 and seat σ ≤ 0.135 µm in a phone. The two cheap bench tests above settle both.