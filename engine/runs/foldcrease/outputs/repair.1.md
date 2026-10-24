=== IDEAS ===
IDEA 1
NAME: Glass-tendon tensioned clothoid hinge
MECHANISM: The anchor is kept: when the phone opens, the panel is put under in-plane tension that pulls any residual curvature flat. The tension now goes through the 45 µm UTG alone. Titanium rails grip the glass's two outer edges, and a force-controlled flexure spring, latched by a cam in the last few degrees of opening, sets the load at T ≈ 2000 N/m. That is 44 MPa in the glass, 0.063% strain and 300 N in total. A soft silicone optical gel (G ≈ 2 kPa) replaces the acrylic OCA under the glass. Through the acrylic OCA only 30% of the tension reached the fold, at about 48 kPa sustained shear. Through the gel 97% reaches it, at 1.9 kPa. The hinge path changes from a sharp teardrop to a teardrop with R = 3 mm and clothoid curvature ramps of at least 2 mm. Without the ramps, features narrower than √(D/T) ≈ 0.57 mm cannot be pulled flat. In a beam-column model with plate contact, calibrated so that today's creases come out at 60–150 µm, the result is a crease ≤2.1 µm deep with slope ≤0.82 mrad. The targets are ≤5 µm and ≤1 mrad. This holds for any untensioned crease up to about 180 µm.
VALUE: The cost is an estimated $13–50 per phone that meets the spec, about 16–72% of a $70–80 hinge. The reported baselines (Fold 7, Apple/Samsung Display drilled plate, Oppo N6) deliver essentially no phones that meet a ≤5 µm / ≤1 mrad spec, so no meaningful cost ratio exists.

IDEA 2
NAME: Per-layer sub-creep strain budget
MECHANISM: The anchor is kept: every polymer layer in the bend zone stays below its measured no-set strain, so no crease forms in the first place. The budget is now set per layer, not for the whole stack. With soft interlayers, each layer bends about its own mid-plane, so its strain is t_i/2R. The kill test's "60 µm stack at R = 5 mm = 0.6%" therefore does not apply. The thickest polymer layer is capped at 25 µm: the PET protector is removed, the UTG is hard-coated, and the back film is 25 µm CPI. The OCA is a low-relaxation silicone, because OCA slip (πd/2) does not shrink with radius. The locked shear drops from 92 kPa (acrylic) to 6 kPa. The polymers' share of bending stiffness falls from 16.9% to 2.4%. The hinge sets R ≥ 4.2 mm, which gives 0.30% per layer and about a 10.2 mm spine at the hinge.
VALUE: Any crease that remains is elastic and recovers, so flatness can be certified. The estimated cost is $7–33 per phone that meets the spec, about 8–47% of the hinge cost, plus about 1.3 mm more thickness than the 8.9 mm Fold 7.

=== NOTES ===
**Common caveats.**
- All numbers come from my Python model in `calc/`. The residual-set fraction is calibrated so that today's creases come out at 60–150 µm, not measured. The tension-versus-no-tension ratios and the slope-versus-width result hold up better than the absolute depths.
- The radius of today's phones (about 2 mm) is my assumption; Samsung does not publish the Fold 7's.
- The 5 µm / 1 mrad invisibility targets are my margin under the perceptual study's "good" grade of <60 µm. A perception test is needed to confirm them.
- The per-phone cost adders are my estimates; no source gives them.
- The Kumoh paper's full text was blocked, so its film thickness and test temperature are still unconfirmed.

**Idea 1**
- **Anchor kept?** Yes: tension applied on opening flattens the crease.
- **Claims corrected:** "R ≥ 3 mm keeps every layer under 0.3%" is false. At R = 3 mm the UTG is at 0.75% and a 60 µm PET film at 1.0%.
- **Decisive numbers:**
  - T = 2000 N/m gives a crease ≤2.1 µm deep with slope ≤0.82 mrad.
  - With sharp teardrop transitions it fails: slope is 1.4–1.5 mrad.
  - Glass under 44 MPa held for 3 years needs 98–128 MPa short-term edge strength (stress-corrosion exponent n = 20 or 15).
  - With a titanium frame the thermal mismatch is 4 µm, against 95 µm of glass stretch.
  - Folded at R = 3 mm the glass sees 552 MPa, below the about 828 MPa at an assumed shipping R ≈ 2 mm.
- **Baseline:**
  - Apple/Samsung Display: a laser-drilled plate with no tension. The crease is reported at ¼ of the Fold 7's, about 0.15 mm, with an angle under 2.5° (44 mrad).
  - Oppo N6: a liquid-printed hinge surface and glass 50% thicker. TÜV reports up to 82% less long-term crease than the N5, and Engadget still saw the crease.
  - The cheapest option is the plain Fold 7 teardrop.
  - None of these meets the spec, so there is no meaningful cost per qualifying unit to compare.
- **Consistency summary:** It passes on glass bending stress, thermal behaviour, tension reaching the fold and slope. It is unknown on gel cohesion under sustained shear and on UTG edge strength.
- **Hazards:**
  - A soft gel under the glass weakens pen-drop resistance.
  - The gel may delaminate in the teardrop.
  - In half-open "tent" postures the tension is off, so the crease is visible.
  - Drop shock goes into the rails.
  - The stored strain energy is small (about 0.014 J).
- **Deciding unknown and experiment:** Whether residual curvature from 8 h folded at 60 °C has a width of at least 2 mm under tension.
  - Make UTG/CPI/PET dummy strips with two interlayers (acrylic OCA vs silicone gel), 5 strips each.
  - Fold them 8 h at 60 °C at R = 3 mm on a teardrop jig with a clothoid ramp.
  - Profile them at T = 0, 1000 and 2000 N/m (2000 N/m is 40 N on a 20 mm strip), at 10 s, 1 min and 1 h.
  - Repeat after 2000 cycles.
- **Durability:** It meets the 2000-cycle minimum. At 200,000 folds, glass fatigue is lower than in today's phones, but gel fatigue is untested.
- **Closest work:** Apple EP4738056 A1 (2026 tension assembly), US12641738, US12541230, EP4567555. Tension on opening is already patented. The glass-only tendon, the gel decoupling layer and the clothoid ramp rule did not appear in any of these, but I only saw their abstracts.
- **Verdict:** WORKS on paper, but novelty is moderate.

**Idea 2**
- **Anchor kept?** Yes: stay below the creep onset.
- **Decisive numbers:**
  - Minimum radius is t/(2ε_c): 4.2 mm if the no-set strain at 60 °C is 0.30%, 5.0 mm at 0.25%, 2.5 mm at 0.50%.
  - If no threshold exists (ε_c = 0), a crease of 11–42 µm remains, and the idea fails.
  - OCA locked shear is 92 kPa for acrylic, 6 kPa for silicone OCA and 0.4 kPa for gel.
- **Baseline:** As for idea 1. Its advantage is no moving parts. The cost is about +1.3 mm of thickness and no PET protector, which brings scratch and impact risk.
- **Consistency summary:** It passes on glass stress (394 MPa). It is unknown on the no-set strain at 60 °C. Recovery right after opening is anelastic, so the spec must allow "invisible within 60 s".
- **Deciding unknown and experiment:** The no-set strain of 20–25 µm CPI at 60 °C.
  - Run a Kumoh-style mandrel test at 0.20, 0.25, 0.30, 0.40 and 0.50% strain.
  - Hold for 8 h and 24 h, with 5 films per condition, 50 films in total.
  - Read residual curvature down to 4 m⁻¹ (residual strain of 0.005%) at 10 s, 60 s and 1 h.
- **Durability:** If the threshold holds, both 2000 and 200,000 cycles are fine. Ratcheting needs the cyclic version of the test.
- **Closest work:** The Kumoh critical-radius result, and the multi-neutral-plane stacks already used in foldables. The per-layer threshold-certified budget with a silicone interlayer appears to be new.
- **Verdict:** NICHE/WORKS. It depends entirely on a 60 °C no-set threshold, and the cost is a thicker hinge.

Files are in `/home/user/SomeRepository/engine/runs/foldcrease/repair/c1/`:
- `LOG.md`
- `NOTES.md`
- `calc/`

Sources:
- [Kumoh CPI residual strain (koreascience)](https://koreascience.or.kr/article/JAKO202102455512209.pdf)
- [Apple EP4738056 A1](https://www.goveda.com/patent/EP-4738056-A1)
- [US12641738](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12641738)
- [US12541230](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12541230)
- [EP4567555](https://data.epo.org/publication-server/rest/v1.2/patents/EP4567555NWA2/document.html)
- [US11644873](https://patents.google.com/patent/US11644873)
- [MacRumors iPhone Fold crease](https://www.macrumors.com/2026/02/25/iphone-fold-crease-measured-production/)
- [AppleInsider ¼ crease](https://appleinsider.com/articles/26/02/25/iphone-fold-hinge-crease-will-be-about-14-the-depth-of-the-galaxy-fold-7)
- [AppleInsider hinge cost (Kuo)](https://appleinsider.com/articles/25/10/12/apples-expensive-iphone-fold-hinge-could-be-cheaper-than-expected)
- [Samsung Fold thickness](https://news.samsung.com/uk/from-17-1-mm-to-8-9-mm-the-galaxy-z-folds-journey-to-becoming-48-thinner)
- [TD Commons crease quantification](https://www.tdcommons.org/cgi/viewcontent.cgi?article=6896&context=dpubs_series)
- [AGC flexible glass](https://oled-info.com/agc-developed-ultra-thin-flexible-cover-glass-suitable-foldable-devices)
- The facts ledger (`evidence.md`)