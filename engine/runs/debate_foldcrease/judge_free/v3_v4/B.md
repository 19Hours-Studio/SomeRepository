# Foldable phone with no physical crease: tensioned "floating" display (v4)

The check was right on all six points. Re-budgeted honestly, the bonded-wing design from the last round (v3) sat at 0.047–0.058 mrad, about 2× over its own target, and that target was too loose. I replaced the clamp-line architecture rather than patching it. In the new design the display is bonded to nothing in the active area. It is tensioned only at its two outer edges and hovers over an air gap. Every term the check added is now either zero in the display's shape or only uses up gap clearance. What remains is the crease from material set, against a stricter target.

## Ideas

### Idea 1: Floating tensioned display (v4)

**Display stack, 76 µm, top to bottom.** This is unchanged from v3 except for the bottom face.
- **Oleophobic layer only.** No polymer film, no anti-reflection (AR) or anti-glare (AG) coating.
- **20 µm ultra-thin glass (UTG).** Compressive stress (CS) 700 MPa, depth of layer 3 µm, central tension (CT) 150 MPa. The edges are ion-exchanged after cutting.
- **3 µm glassy adhesive** (Tg ≥ 120 °C).
- **30 µm OLED panel** with no polarizer and an on-cell touch layer. It sits on the neutral plane.
- **3 µm glassy adhesive.**
- **20 µm UTG.**
- **Bottom face:** a metal or ITO electrode under a 2 µm siloxane hard coat. The panel emits upward, so this layer is outside the optical path. The electrode is used only while folded (see below).

**Why the materials barely set.** The glass carries 99.2% of the bending stiffness D = 2.37e-3 N·m. The polymers that can take a set carry 0.78%.

**Support (new).**
- There is **no bond anywhere under the active area.**
- The open display hovers **30 µm above a backing.** The backing is two lapped wing plates plus a bridge in the hinge, which rises at the end of opening.
- The backing has vent grooves at 1 mm pitch.
- The gap vents to the inside of the phone through a porous ePTFE vent with a time constant of about 1 min. On handling time scales the trapped air acts as a stiff cushion (1583× stiffer than the membrane for mean height). On thermal and barometric time scales the gap is vented.
- There is no servo, no piezo and no capacitive gap sensing.

**Tension.** T = 4000 N/m, about 600 N across a 150 mm width.
- It enters only at the two outer side edges, through two-face jaws under the side bezels. Gripping both faces puts the line of action in the mid-plane by symmetry.
- One jaw sits on a flexure carriage: a spring of about 1000 N/mm with about 0.6 mm of preload, engaged by a cam at the end of opening. Tension is force-controlled, so housing CTE no longer matters.
- **The jaws must be Poisson-free.** Each jaw is a comb of flexure fingers that are stiff in x and allow ±22 µm in y. Hindered Poisson contraction (43 µm across 150 mm) would put transverse compression near the clamps, and stretched clamped sheets can wrinkle.
- **Stresses and loads.** The glass carries 94 MPa of membrane stress. The sustained core tension is 244 MPa. The frame carries 600 N in compression. The cam does about 118 mJ of work per opening, much of which can be returned on closing.

**Why backing errors no longer reach the glass.** With no shear and no normal coupling, the open shape is fixed by three things only:
- the straight chord between the two jaws;
- a uniform-pressure parabola (gravity, residual vent pressure), whose curvature radius is 2.7 km at full gravity;
- the material-set crease.

The parabola is the same over the fold and over the reference zone, so it is not a line feature.

The terms the check added therefore drop out of the shape (`float4.out` B):
- the bond moment c·τ;
- seat kink δ/2 + Δh/2a;
- frame bow and thermal bow;
- hinge gravity torque;
- servo bridge reference.

They move the backing, not the glass chord. Each one now only uses up gap (see the gap budget below).

**Fold geometry.**
- **Nominal:** water-drop hinge, R = 5.5 mm, ramps 28/12 mm, neck radius Rn = 20.2 mm, fold zone 80 mm, bulb 13.4 mm. The folded spine is about 15.5 mm (estimate).
- **Option:** R = 7 mm with 35/12 mm ramps and a bulb of 16.6 mm (spine about 18.5 mm).
- **Folded state:**
  - Tension is about zero (cam released).
  - The bulb shape is set by back-side hinge plates, as in v3.
  - The flat parts are held on the wings by electroadhesion, energised only while folded: about 100–200 V across a dielectric of about 3–5 µm. The ideal parallel-plate pressure is 17–25 kPa; measured holds on conductive targets range from 1 to 100 kPa at 400 V.
  - The peel force at the wing edge is V = D·κ′ ≈ 10 N/m. At 5–20 kPa the glass lifts off for 1–4 mm. The curvature gradient in that region is at most the ramp's own (V/D), so it adds no new crease term.

**Opening sequence.** Seat open → bridge up → electroadhesion off → tension on → the glass lifts to its chord in about 0.2 s through the grooves. Closing runs in reverse.

**The crease that remains** (`float4.out` A, max slope at 1 min after the worst hold). Polymer set fractions are 0.2 for the panel and 0.1 for the adhesive, as before. φ_g is the glass set fraction (the share of the folded curvature the glass keeps after unfolding).

| Geometry, T | φ_g = 0 | 5e-4 | 1e-3 | 3e-3 | Pessimistic polymers (0.5/0.3) + φ_g 1e-3 | Tolerable φ_g at 5″ / 3″ |
|---|---|---|---|---|---|---|
| R5.5 25/9 (v3 geometry), 4000 | 0.0077 | 0.0106 | 0.0134 | 0.0248 | 0.0256 | — |
| **R5.5 28/12, 4000 (nominal)** | **0.0066** | 0.0090 | 0.0114 | 0.0212 | 0.0218 | 1.1e-3 / 1.5e-4 |
| R5.5 28/12, 5000 | 0.0053 | 0.0072 | 0.0092 | 0.0169 | 0.0175 | 1.8e-3 / 5.2e-4 |
| R7 35/12, 4000 | 0.0043 | 0.0058 | 0.0074 | 0.0137 | 0.0142 | 2.5e-3 / 9.6e-4 |
| R7 35/12, 5000 | 0.0034 | 0.0047 | 0.0059 | 0.0110 | 0.0113 | 3.4e-3 / 1.5e-3 |

- Values are in mrad.
- Depth is 0.18 µm (nominal, φ_g = 0) and 0.57 µm at φ_g = 3e-3.
- If the springs fail (T = 0), the crease reverts to 9–185 µm, the size of a shipping phone's crease.

**Edge tails** (a separate location, not added to the crease). The jaw mouth sits 4 mm outside the active area.
- Jaw shear asymmetry of 5–20% gives 0.0006–0.0025 mrad at the active edge.
- A 0.2 mrad jaw angle error adds 0.0011 mrad (`float4.out` C).
- Worst case is 0.0036 mrad.

**VALUE.**
- **Nominal:** the worst line feature is 0.0066 mrad at φ_g = 0. This passes the stricter 5″ target (0.0121 mrad) with 1.8× margin and the 3″ stretch target (0.0073 mrad) with 1.1×.
- **Glass-set limits:** it fails 5″ above φ_g = 1.1e-3 and fails 3″ above 1.5e-4.
- **Pessimistic:** 0.0218 mrad, which is 1.8× over the 5″ target.
- **Like-for-like with v3:** 0.047–0.058 → 0.0066 mrad, a 7–9× improvement (`float4.out` H).

### Idea 2: Idea 1 at R = 7 mm and T = 5000 (for the 3″ target)

- The crease is 0.0034 mrad at φ_g = 0 and 0.0059 at 1e-3.
- It passes 3″ up to φ_g = 1.5e-3 and 5″ up to 3.4e-3. The pessimistic case (0.0113 mrad) also passes 5″.
- **Cost:**
  - a folded spine of about 18.5 mm;
  - 750 N of frame load;
  - 268 MPa of sustained core tension;
  - about 184 mJ of cam work per opening.

This is the version to build if the vernier threshold proves to be 3″ under real viewing.

### Idea 3 (retired): v3 bonded wings with the check's fixes

The check's own fixes (shape servo, ΔF ≤ 0.5%, joint stiffness 2000–10,000 N·m/rad, R = 7) give 0.020–0.029 mrad. That is still 1.7–2.4× over 5″, and it needs nanometre-level bridge references and µm-level seats.

At the same R = 7, Idea 1 gives 0.0043 mrad, 4.7–6.8× lower.

The outward fold is also dropped. The user-facing glass carries 497 MPa while folded, and a flaw of 1.5–2 µm breaks it.

## Notes

### Response to the check, point by point

1. **Off-centre tension entry, 0.82–0.87 mrad: accepted, and removed by design.**
   - I reproduce the mechanism: force offset c = 38 µm gives moment T·c at a bottom-face bond.
   - In v4 no tension passes through a bottom-face bond inside the display. It enters at two-face jaws. Using the check's own finite-difference bond model with 5–20% shear asymmetry, the tail is 0.0006–0.0025 mrad at 4 mm from the jaw mouth.
   - The check's objection to "lamination under load" no longer applies, because nothing is laminated to the wings.

2. **Servo residual had no basis: accepted.** The servo is removed. A bridge height error now only changes the gap: 0 in shape, a few µm of gap.

3. **Hinge gravity torque: accepted. It is no longer a shape term.**
   - A torque of 0.047 N·m at a joint stiffness of 300–1000 N·m/rad rotates the halves 0.05–0.16 mrad. That moves the backing 1.8–5.9 µm under a 30 µm gap.
   - The required joint stiffness falls from ≥ 2000 to about ≥ 300 N·m/rad.
   - The 30 mm tongue stays, but only to keep the angle repeatable to about 0.07 mrad (2.5 µm of gap). Lapped ceramic seats are no longer needed.

4. **The target was not conservative: accepted.** The pass line is now 5″ of vernier offset, which is 0.0121 mrad of surface slope with the source at infinity (0.0139 for a lamp 2 m away with the eye at 0.3 m). 3″ (0.0073 mrad) is the stretch target. I do not take credit for the fact that the crease slope is spread over 12–28 mm ramps, which probably raises the true threshold; that is unmeasured.

5. **26× and 12× were against my own baseline: accepted.** Those numbers are withdrawn. Gains are now stated against the check's re-budget and against the target.

6. **Touch with sealed gas: accepted, and recomputed for the new gap.**
   - The glass lands on the rigid backing at about 0.26 N after 30 µm of travel. There is no foam layer under it.
   - The vent grooves and squeeze film keep the dimple time below 1 ms. The 544 Hz drum mode is overdamped (damping ratio about 16).
   - Because the cushion is sealed on short time scales, a press bulges the rest of the display by a mean of about 4 µm (estimate: dimple volume Fa²/4T ≈ 91 mm³ over 0.0225 m²). That is a uniform parabola while pressing, not a line.
   - The fold zone and non-fold zone now have the same structure. Press compliance is equal by construction, apart from 3 µm seam steps under 76 µm of glass.
   - **Whether 30 µm of pre-travel is felt is unmeasured.** Serina 1997 reports that fingertip pulp is compliant below 1 N, but I have no number in µm.

The check said two things were undersold. Press stiffness is taken up in point 6. The strip-test geometry (57 mm tension length) stands.

### Gap budget, h = 30 µm (`float4.out` D)

**Fixed items, 8.6 µm in total:**
- gravity sag, 1.0 µm;
- flatness, 2 µm;
- seam step, 3 µm;
- angular repeatability, 2.5 µm;
- thermal bow, 0.04 µm.

The housing no longer needs AlSiC; titanium would add about 1 µm.

**Holding cases.** EI is the bending stiffness of the open body; k is the hinge joint's angular stiffness in N·m/rad.

| Case | Load (nominal / pessimistic) | Total gap used | Margin |
|---|---|---|---|
| Held by one half | 1.8 / 5.9 µm | 10.3 / 14.5 µm | 19.7 / 15.5 µm |
| Held by both edges, face-down | 12.0 / 26.2 µm | 20.6 / 34.8 µm | 9.4 / **−4.8 µm** |

Nominal is EI 10 N·m², k 1000 N·m/rad; pessimistic is EI 5 N·m², k 300 N·m/rad.

- **Pessimistic edge hold fails.** The fix is h = 35 µm or EI ≥ 7 N·m².
- **Handling time scales.** The slow-vent cushion lets the glass follow uniform bending. Gap use is 4% for a self-weight bow and 25% for a hinge kink. Moment-type hand loads then need roughly 1 N·m beyond a normal hold to cause contact (estimate). Local finger pushes from behind the hinge get there sooner (not computed).
- **What contact does.** It is elastic and transient, and while it lasts the glass can show the backing's seams. This is the main new handling failure mode, and it needs a prototype.

### How "invisible" is measured, and the targets

Measure 1 min after the worst hold, with deflectometry and white-light interferometry per IEC 62715-6-22, across the full display.

**Primary metric.** Slope and curvature in the 0.8–20 mm band over the fold must be ≤ 1.2× those of a non-fold zone on the same device.

**Absolute backstops:**
- depth ≤ 0.5 µm;
- line-feature slope ≤ 0.0121 mrad (5″), with 0.0073 mrad (3″) as the stretch;
- the same slope limit at the side-edge tails;
- luminance change ≤ 1%, Δu′v′ ≤ 0.002.

**Touch:**
- swipe topography ≤ 1/5 of Louw's threshold;
- press compliance at 0.1–2 N within ±20% of the non-fold zone.

**Human tests:**
- a two-choice test with ≥ 30 observers, screen off and on, line-grid and point-source reflections at 0–70°;
- blind swipe, press and stylus-drag tests.

Pass means not significantly above chance.

**Coating rule:** the device must pass with no AR or AG coating.

### Persistence testing

**Cycling.** Run 2k cycles, then checkpoints at 20k, 200k and 500k. At each checkpoint, rescan and measure:
- tension (from carriage position);
- jaw finger health;
- electroadhesive hold pressure.

**Static and duty-cycle holds:**
- 10 days at 25 °C;
- 72 h at 60 °C / 90% RH;
- 500 h at 60 °C;
- −20 °C, opened while still cold;
- 14 days of 8 h folded per day (the PolyU effect of hold time combined with repeated loading).

**Rescans:** 1 min, 1 h and 24 h after opening.

**New tests for v4:**
- folded 72 h with the electroadhesion **unpowered** (power-loss case);
- holding-load sweeps up to contact;
- a dust chamber: particles under about 20 µm cannot bridge the gap, and in the folded hold a 10 µm particle tents the glass to only about 3.5 m⁻¹;
- spring relaxation (crease scales with 1/T);
- drop tests.

**What breaks invisibility:**
- φ_g above 1.1e-3 (nominal geometry, 5″);
- polymer set above the 0.5/0.3 pessimistic level;
- jaw creep or asymmetry above about 20%;
- jaws that bind in y (wrinkling);
- gap contact while viewing;
- electroadhesion failure while folded, which lets the bulb shape drift;
- glass edge or core failure at 244 MPa sustained.

**Wear.** The glass slides about 0.2 mm on the backing per cycle under about 1.5 Pa. By Archard's law that is nanometre-level wear over 500k cycles.

**2k versus 500k cycles.** The design has no wear-limited optical term. The only cycle-dependent term is set (φ_g, polymers), which PolyU shows can grow with repeated loading. 500k is therefore the test of record.

### Failure modes and trade-offs

- **Thickness:** a spine of about 15.5 mm, or about 18.5 mm at R = 7. Side bezels grow to about 6–7 mm (jaws plus the 4 mm tail margin).
- **Mass:** about 2.3 g of glass, plus about 6–10 g for jaws, carriage, spring and bridge (estimate).
- **Power:** a 100–200 V boost converter for electroadhesion, which draws only capacitive leakage while folded.
- **Cost:** below v3 (no servo, no lapped seat), but well above current hinges: glass-panel-glass lamination, flexure jaws, a cam and a carriage. There is no cheap peel-off repair.
- **Optics:** no haze and about 4% bare-glass reflection. Print-through of the panel is untested.
- **Feel:** glass to the touch with 30 µm of pre-travel everywhere, uniform across the display.
- **Glass risks:** sustained 94 MPa membrane stress plus 244 MPa core tension; free y-edges carry 94 MPa parallel to the edge. A stylus at 3 N puts at most about 232 MPa on the bottom face, against 700 MPa of CS.
- **Wrinkling:** if the Poisson-free jaws bind in y, the sheet can wrinkle. This is a finite-element-analysis (FEA) item.

### Established versus model

**Established (sourced):**
- ε = c/R;
- HTX iPhone Duo measurements: 48 µm and below 0.1° new; 167 µm and 1.24° after 3000 folds (secondhand);
- PolyU plastic creasing in UTG (abstract only);
- vernier acuity of 2–5″;
- electroadhesion pressures of 1–100 kPa on conductive targets at 400 V;
- stretch-induced wrinkling of clamped sheets;
- fingertip pulp compliant below 1 N;
- tension-applying display hinges exist in patents (US 10209746), as do floating support plates with a safety gap (CN 115929771 B).

**Model or assumption:**
- every φ value;
- the membrane decoupling: exact in linear theory, but not prototyped;
- EI, k_θ, flatness and seam values;
- jaw asymmetry;
- hold pressure in a phone;
- the folded bulb shape without a bond (needs a prototype);
- wrinkling (needs FEA);
- all crease numbers.

### Cheapest decisive experiments

1. **Glass-set strips (a few hundred dollars).**
   - Wrap strips on 5.5 and 7 mm mandrels: 72 h at 60 °C, 14 days at 25 °C, and 2k cycles.
   - Materials: ion-exchanged UTG, the same glass without ion exchange, alkali-free glass, and the 20/3/30/3/20 sandwich.
   - Hang the strips vertically and read the tip offset at 1 min, 1 h and 24 h.
   - **Kill:** φ_g above 1.1e-3 (R = 5.5, T = 4000), or above 2.5e-3 for Idea 2 at R = 7.
2. **Decoupling rig (low thousands of dollars).**
   - Clamp a 150 × 150 mm, 50–76 µm glass sheet in two-face jaws at T = 4000 N/m over a split lapped plate. Shim in steps up to 5 µm and kinks up to 0.2 mrad.
   - Run deflectometry at T = 0 and T = 4000.
   - This tests the central claim (no transfer while the gap is open), the edge-tail decay length (0.77 mm) and wrinkling, all in one rig.

### Comparison with shipping approaches

- **Apple iPhone Duo:**
  - reports describe a laser-drilled support plate;
  - a replaceable nano-texture cover layer ($19 with AppleCare+) that reduces visibility; Apple does not claim the crease is gone;
  - HTX measured 48 → 167 µm and below 0.1° → 1.24° (21.6 mrad) within 3000 folds;
  - reviews call it less intrusive than rivals but visible in some light and felt under a finger.
- **Samsung Galaxy Z Fold 7:** thicker UTG and a new hinge. The crease deepened in a live fold test to about 105k folds. The 0.7 mm figure in the brief still has no source.
- **Oppo Find N6:** a 3D-printed titanium hinge whose height variation drops from 0.2 to 0.05 mm. Oppo claims 82% less crease and TÜV certifies 600k folds. Engadget says it is "still visible".
- **What they share:** all three bond polymer films and a plate across the fold, with no tension.
- **What v4 does differently:** it decouples the glass from the hinge entirely. That trades their thin spine and simplicity for tension hardware, wide side bezels and a hover gap.
- **Predicted versus measured:**
  - 0.0066–0.022 mrad against 21.6 mrad for the aged Duo is about 1000–3300×;
  - against the new Duo (below 1.75 mrad) it is about 80–260×.
  - These are model numbers against measurements, not like-for-like.

**Files:** all in `round4/`: `float4.py`, `float4.out`, `README.md`, plus unchanged copies of `sandwich.py`, `design2.py`, `design3.py` and `lever3.py`.

**HONEST GAIN.**
- **Like-for-like with v3:** same crease model and set assumptions. The worst visible feature falls from 0.047–0.058 mrad (v3 as re-budgeted by the check) to 0.0066 mrad nominal, 7–9×. At the v3 geometry alone it is 6–7.5×. Against the check's improved v3 at R = 7 (0.020–0.029), v4 at R = 7 gives 0.0043, 4.7–6.8×.
- **Where it comes from:** removing every clamp line inside the display. Five terms go to zero in shape:
  - bond moment, 0.02–0.87 mrad;
  - seat kink;
  - bow;
  - hinge torque;
  - servo reference.
- **Against the stricter 5″ target:** nominal passes with 1.8× margin; pessimistic fails by 1.8×. Idea 2 passes 5″ even when pessimistic, and passes 3″ up to φ_g = 1.5e-3.
- **Still unproven:**
  - glass and polymer set (strip test);
  - decoupling and wrinkling (rig);
  - gap contact under hard grips;
  - folded-state retention without a bond.

## Sources
- [HTX via iThinkDiff](https://www.ithinkdiff.com/iphone-duo-crease-test-3000-folds/)
- [TechEBlog – HTX Duo test](https://www.techeblog.com/htx-studio-iphone-duo-inner-display-crease-test/)
- [Notebookcheck – Duo reviews](https://www.notebookcheck.net/Apple-iPhone-Duo-reviews-are-in-Plenty-of-criticism-but-positive-hinge-stress-test.1430224.0.html)
- [9to5Mac reviews](https://9to5mac.com/2026/10/22/iphone-duo-reviews-the-absolute-best-foldable-phone-but-not-without-compromise/)
- [MacRumors – replaceable layer](https://macrumors.com/2026/10/01/iphone-duo-cover-layer-is-replaceable)
- [Tom's Guide – Duo layer](https://www.tomsguide.com/phones/iphones/apple-reveals-iphone-duo-has-a-replaceable-display-layer-what-it-means-for-you)
- [Macworld – laser-drilled plates](https://www.macworld.com/article/2848958/report-apples-folding-iphone-wont-have-a-crease-thanks-to-laser-drilled-plates.html)
- [Oppo newsroom](https://www.oppo.com/en/newsroom/stories/oppo-find-n6-zero-feel-crease-foldable-innovation/)
- [Android Authority N6](https://www.androidauthority.com/oppo-find-n6-zero-feel-crease-durability-3648272)
- [Engadget – Find N6](https://engadget.com/mobile/smartphones/oppos-find-n6-might-be-the-foldable-of-your-dreams-131036055.html)
- [Mobile World Live – Find N6](https://www.mobileworldlive.com/oppo/oppo-irons-out-foldable-crease-with-find-n6/)
- [Fold 7 fold test](https://www.androidauthority.com/samsung-galaxy-z-fold-7-live-fold-test-3583522)
- [PolyU – plastic deformation and recovery in UTG](https://research.polyu.edu.hk/en/publications/plastic-deformation-and-recovery-in-ultrathin-aluminosilicate-gla/)
- [Vernier acuity (Wolfe essay)](https://learninglink.oup.com/public/files/cdn/wolfe4e/essay03.01.html)
- [Mukamel KITP lecture](https://online.itp.ucsb.edu/online/neuro10/mukamel/pdf/Mukamel_Neuroscience_KITP.pdf)
- [Electroadhesion pressure before/after contact (PMC)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10359345/)
- [Low-voltage electroadhesive pad, parylene](https://wanglab.mee.sustech.edu.cn/assets/pdf/Low-voltage_Electroadhesive_Pad_with_Thin_Insulation_Layer_Fabricated_by_Parylene_Deposition.pdf)
- [Stretch-induced wrinkling, Nayyar thesis](https://repositories.lib.utexas.edu/handle/2152/ETD-UT-2010-08-1814)
- [Disappearance of stretch-induced wrinkles (arXiv 1602.08607)](https://arxiv.org/pdf/1602.08607)
- [Fingertip pulp force response (Serina)](https://www.coeh.berkeley.edu/publications/force-response-fingertip-pulp-repeated-compression-effects-loading-rate-loading-angle)
- [US 10209746 – tensioned foldable display](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10209746)
- [US 9661719 – air gap with movable supporter](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9661719)
- [CN 115929771 B – floating plate with safety gap](https://www.goveda.com/patent/CN-115929771-B)
- [US 12487643](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12487643)
- [IEC 62715-6-22](https://ccn-scc.ca/standardsdb/standards/2058735)
- [Louw et al. 2000](https://link.springer.com/doi/10.1007/s002210000350)
- [UTG CS/DOL, US 12167556](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12167556)