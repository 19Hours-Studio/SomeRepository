=== IDEAS ===
IDEA 1
NAME: Floating glass on fluid
MECHANISM: Anchor kept: an index-matched liquid film, not an adhesive, couples the ultra-thin glass (UTG) to the panel where it bends. Because a liquid has no shape memory, the visible surface sits on a layer that cannot take a set. The repair fixes the flaw the kill test found: wherever the liquid strip met bonded adhesive, the layers had to slip 157 µm past each other, a shear strain of 6.3 against the 2.5–4 that folding adhesives are designed for. So the fluid (20 µm of phenyl-silicone, refractive index 1.51 ±0.02, viscosity 0.05–0.1 Pa·s) now covers the whole display, and the 149 µm of slip at each edge runs out at the perimeter. There it is taken by a pinned meniscus plus a 5 µm polyimide loop seal, which pushes back with at most 0.1 N/m; the glass would buckle at 0.34 N/m. The rest of the stack: 30 µm UTG with no polymer film on top (a bonded 5 µm hardcoat would print a 10 µm crease); a polarizer-free colour-filter OLED panel with touch built in; adhesive plus a 30 µm laser-patterned titanium plate; and a waterdrop hinge with a 3 mm minimum radius, so the glass and panel strain is 0.50% instead of 2.5% for a bonded stack. With the glass free to slip, any set in the layers below is levelled out by fluid flow in 5–10 s. Gravity, heat and stylus effects all stay inside their limits (a gravity tilt of at most 0.27 mrad, a 1.2 µm dome over 140 mm across 60 K, interface reflectance below 10⁻⁴). An earlier round with spacer pillars and a slight vacuum failed: the glass could then sag 360 µm into any dip and the crease printed straight through, so that version was dropped.
VALUE: It removes the layer that creeps from under the viewed surface for an estimated +$2–6 per phone, against roughly +$5–15 (my estimate) for the Apple/Samsung patterned plate or Oppo's ~20-pass printed hinge. On paper it is the only one of these aimed at zero crease rather than a smaller one, so cost per crease-free phone delivered is finite against undefined for the baselines.

IDEA 2
NAME: Spectrum-matched drumhead hinge
MECHANISM: Anchor kept: on opening, a hinge cam puts in-plane tension on the display and pulls any set flat over a flat plate. That tension works as a long-wavelength filter: the residual is w = w₀·k²/(k² + T/D), so it beats wide sets and loses to narrow ones. I reproduced the kill result (a 20 µm × 3 mm set leaves 3.3 µm and 2.3 mrad at 600 N/m; flattening it needs 3.9 kN/m). At today's 1.5 mm radius, 9.6–56 kN/m would be needed, which no phone can take. So the repair moves the design to where the anchor is strong. A thick hinge spine with a 4–5 mm bend radius spreads the set over a ~9 mm width. At the design tension of 1000 N/m (150 N total), the residual is ≤1 µm and ≤0.5 mrad as long as the set stays below 2.1–3.7% of the fold curvature. Clamping every layer together at the panel ends means the tension never passes through the adhesive as shear: shear in the viewing area drops from the kill's 25 kPa to 9.4 kPa, against a 10.5 kPa creep-test stress. A titanium frame and a 1 mm-stroke constant-force spring keep the tension within ±2% from −20 to +40 °C (±8% with aluminium). Glass strain from the tension is only 0.04%, and the cam releases the tension before folding starts.
VALUE: It turns any set below about 2.5% of the fold curvature into an invisible one, adding about +$8–20 per phone (cam, springs, titanium frame) and about 3 mm of spine thickness. Today's phones sit near 8% by my rough estimate, and the best current alternatives reduce the crease rather than remove it.

=== NOTES ===

**Idea 1: Floating glass on fluid**
- **Anchor kept?** Yes. The fluid coupling stays; only its extent (whole display, not a strip) and the seal changed.
- **Decisive numbers:**
  - Slip is π·d: 157 µm in the original, 149 µm per edge in the repair. Folding adhesives are designed for 250–400% shear (NAFEMS; 3M whitepaper).
  - Own-layer strain at R = 3 mm is 0.50%. The Kumoh CPI study puts the no-set limit near 5 mm radius, about 0.5% strain, so the panel is right at the edge.
  - Levelling time is τ = 12μ/(h³Dk⁶): 0.7 s at 6 mm, 5–10 s at 9.4 mm.
  - Silicone volumetric expansion is 9.6×10⁻⁴/K.
  - Calculations are in `calc/idea1.py` and `calc/idea1_r3.py`.
- **Baselines, per phone delivered:**
  - Galaxy Z Fold 7 (cheapest): +$0, crease visible.
  - Apple/Samsung Display laser-drilled plate: crease reported at about ¼ of the Fold 7's, so smaller but presumably still there.
  - Oppo N6: about 20 laser-scan and print passes per hinge plus 50% thicker glass. Reviewers (GSMArena, Tech Advisor, Engadget) could still see the crease.
  - Context: BOM is $670–790 and the inner display about $122.
  - All the $ increments are my estimates, not sourced.
- **Consistency:** all checks pass (table in `NOTES.md`) except two. The panel strain sits exactly at the CPI no-set limit (marginal), and levelling takes 5–10 s after opening.
- **Hazards:**
  - Bubbles from dissolved gas: needs degassed fluid and a gas-tight, ALD-coated seal.
  - Glass shards are not held together without a top film.
  - The floating glass may slowly drift sideways (ratchet) over many cycles.
  - At −20 °C the fluid thickens 3–5×, so levelling slows.
  - Stylus loads give 0.7% glass strain, the same as today.
  - The panel's own set stays visible in the weak reflection from inside the panel (target: slope ≤3 mrad; speculative).
- **Deciding unknown:** the visible surface profile 10 s and 60 s after opening, following 2000 folds at R = 3 mm plus 24 h folded at 60 °C.
- **Cheapest experiment:** float 30 µm UTG strips on 20 µm phenyl-silicone over a dummy lower stack (PI/adhesive/Ti), with bonded strips as controls. Run 5 strips per arm and measure by deflectometry to IEC 62715-6-22. Five per arm is enough to resolve 1 µm at σ ≈ 0.5 µm.
- **Targets for "invisible":**
  - Depth ≤1 µm and slope ≤0.5 mrad at the top surface.
  - Off-axis: no visible line distortion from 20° to 70°.
  - Touch: participants cannot tell the fold zone apart above chance in a forced-choice test (n = 25).
- **Durability:** 2000 cycles look comfortable. For 200k cycles, wear on the sliding parts is about 0.05 µm, so the open question is seal fatigue at 149 µm of travel per cycle.
- **Closest existing work:** the LCD cell, a liquid between glass plates filled by one-drop fill (my analogy, not a source I checked). A quick patent search found no liquid layer under the cover of a foldable.
- **Verdict:** WORKS on paper. It needs the strip test.

**Idea 2: Spectrum-matched drumhead hinge**
- **Anchor kept?** Yes. Hinge tension on opening stays; the bend radius, the end clamp and the frame changed.
- **Decisive numbers:**
  - The required tension rises steeply as the set gets narrower: 9.6–56 kN/m at R = 1.5 mm, 0.44–2.6 kN/m at R = 5 mm with a 2% set.
  - Adhesive relaxes 40–50% at 60 °C (US11334117), which is what makes the set grow.
  - Calculations are in `calc/idea2.py`.
- **Baselines:** the same three as Idea 1. Here tension complements the patterned plate rather than replacing it.
- **Consistency:**
  - Adhesive shear is 9.4 kPa against the 10.5 kPa limit: a thin margin.
  - The tolerable set (2.1–3.7%) has not been measured.
  - Thickness is the main trade-off: the spine is about 11.8 mm at R = 5 mm or 9.8 mm at R = 4 mm, against 8.9 mm for the Fold 7.
- **Hazards:**
  - 150 N of sustained load on the frame.
  - About 0.1 J of extra work per cycle, which needs an over-centre toggle so the user doesn't feel it.
  - Narrow features such as plate-edge steps (~1 mm wide) are not flattened, so the plate transitions must be smooth.
  - The set grows with time held folded, roughly as log(t). The 1.5× tension margin is meant to cover growth from 2k to 200k cycles; this is not verified.
- **Deciding unknown:** the set fraction f at R = 4–5 mm after 2000 folds plus 24 h at 60 °C. It must be ≤2.5%.
- **Cheapest experiment:** cycle real stack strips on 4 and 5 mm mandrels (5 per radius), profile them, then tension them from 0 to 1500 N/m on a tensile stage over a lapped plate.
- **Closest existing work:** US12641738, EP4738056 and EP4567555 already tension the display when it is flat. The new parts here are the long-wavelength design rule (set width ≫ √(D/T)), the all-layer end clamp and the constant-force titanium frame.
- **Verdict:** NICHE. It only works in a thicker-spine phone, and only if f ≤ ~2.5%.

**Comparison with Apple and Oppo:** both reduce the crease by mechanical means. Apple uses a patterned plate and leaves room for the bent display; its patent names pulling on the display as a cause of damage, the opposite of Idea 2. Oppo levels the hinge surface and uses thicker glass. Neither has published an absolute crease depth, and Oppo's 0.05 mm is the hinge-surface variation, not a measured crease. Idea 1 differs by removing the creeping layer from under the viewed surface; Idea 2 by actively flattening whatever set accumulates. Both are speculative until the tests above are run.

Files are in the working folder: `LOG.md`, `NOTES.md`, `calc/idea1.py`, `calc/idea1_r3.py`, `calc/idea2.py`. Nothing was committed.

Sources:
- [3M OCA foldable whitepaper](https://multimedia.3m.com/mws/media/1793258O/optically-clear-adhesives-for-foldable-oled-displays-whitepaper.pdf)
- [NAFEMS NWC23 0431](https://www.nafems.org/publications/resource_center/nwc23/0431-presentation/)
- [Kumoh CPI residual strain](https://koreascience.or.kr/article/JAKO202102455512209.pdf)
- [US11334117 (OCA relaxation)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11334117)
- [Crease perception study](https://openaccess.cms-conferences.org/publications/book/978-1-958651-47-6/article/978-1-958651-47-6_25)
- [IEC 62715-6-22:2026](https://www.evs.ee/et/iec-62715-6-22-2026)
- [US12641738](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12641738)
- [EP4738056](https://www.goveda.com/patent/EP-4738056-A1)
- [EP4567555](https://data.epo.org/publication-server/rest/v1.2/patents/EP4567555NWA2/document.html)
- [US11644873](https://patents.google.com/patent/US11644873)
- [AppleInsider on the iPhone Fold crease](https://appleinsider.com/articles/26/02/25/iphone-fold-hinge-crease-will-be-about-14-the-depth-of-the-galaxy-fold-7)
- [GSMArena Find N6 review](https://fo.gsmarena.com/oppo_find_n6-review-2947p2.php)
- [Tech Advisor Find N6](https://www.techadvisor.com/article/3083746/oppo-find-n6-review-hands-on.html)
- [Engadget Find N6](https://engadget.com/mobile/smartphones/oppos-find-n6-might-be-the-foldable-of-your-dreams-131036055.html)
- [Oppo N6 newsroom](https://www.oppo.com/en/newsroom/stories/oppo-find-n6-zero-feel-crease-foldable-innovation/)
- [International Finance on foldable BOM](https://internationalfinance.com/technology/samsung-vs-apple-foldable-rivalry-why-these-smartphones-cost-so-much/)
- [Android Authority on UBS BOM](https://www.androidauthority.com/iphone-fold-cheaper-than-galaxy-z-fold-7-8-3577492)
- [NuSil index-matching gels](https://av.cmd.avantorsciences.com/rq/iddl/using_optical_index_matching_silicone_gels_to_improve_outdoor)