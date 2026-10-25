=== GATE ===
IDEA 1: Tensioned membrane open state
KILLER | Peak shear the OCA must hold for as long as the phone stays open, at 60 °C, to carry the tension that pulls the crease down to ≤1 µm | required ≈63 kPa. My model treats the stack as separate layers held together by a soft adhesive (UTG 30 µm, two PET films of 50 µm, panel 30 µm, bending stiffness D = 2.8e-4 N·m). It is checked against a known case: with no tension it returns the input crease unchanged. The starting crease is the HTX-measured 167 µm (Gaussian width σ = 4.7 mm, from HTX's 167 µm depth and 1.24° slope). Flattening that to 1 µm needs T ≈ 3.0 kN/m, or 0.11 % strain. The tension passes into the panel through the OCA over a shear-lag length of about 48 mm, giving the 63 kPa peak. | available ≈10.5 kPa. That is the stress a foldable-OCA patent tests at 60 °C/93 % RH, where the adhesive already creeps 10–30 % in 10 minutes, with a modulus of 0.02–0.045 MPa (USPTO 11348487 family). At 63 kPa the shear strain is about 200 % and keeps creeping, so the tension relaxes or the bond slips. | MARGIN 0.17
CHAIN | iPhone Duo-class stack (best measured shipping result) | now 167 µm after 3000 folds (HTX) | with idea about 6 µm, if the tension relaxes to the ~500 N/m the OCA can hold; this is a model only and needs a prototype | RATIO ~28 (model)
VERDICT | DEAD | As written (≤1 µm), the bond has to hold about 6x the shear at which foldable OCAs already creep. The same model says ~120 N/m (0.004 % strain, 2.5 kPa peak shear) would reach the 20 µm target with about 4x margin, so the cheapest test is to tension a coupon of the stack after folding. Note that if the layers bond tightly (cold, about −20 °C) the stiffness rises about 40x and the margin goes away.
NEW FACT | The HTX lab measured the iPhone Duo crease at about 48 µm peak-to-valley new and about 167 µm after 3,000 folds, with a 1.24° slope. An older phone in the same test showed 350 µm, and one unnamed rival did better than the Duo. Hands-on reports still see a crease under some lighting. | ithinkdiff (HTX test), Notebookcheck
IDEA 2: Gel-slip decoupled glass stack
KILLER | Bending strain in the solid polymer layers that still bend at the phone's small radius (cover PET or CPI, back film); the gel does not change this | required ≤0.5 %, the creep-safe limit at 60 °C. This value is assumed (Idea 3 uses the same figure), not sourced. | available 1.67 % for a 50 µm film bent at R = 1.5 mm about its own midplane (ε = t/2R = 50/3000). Films set badly on their own: crosslinked polyurethane protective films kept a 50–70° residual angle after 24 h folded at 5 mm radius, 60 °C/93 % RH (USPTO 9780318). | MARGIN 0.30
CHAIN | Fold7/Duo stack, which already has no polarizer (Samsung Eco² colour-filter-on-encapsulation since the Fold3) | now 167 µm | with idea about 142 µm. Only the OCA term (15 %) is removed, and the thinner-polarizer gain is already shipped. | RATIO 1.18
VERDICT | WOUNDED | Even if the gel stores no shear set, the polymer films still bend at about 3x their creep-safe strain, and the polarizer saving is already in Samsung's design, so the gain is at most ~1.2x.
NEW FACT | Samsung's Eco² OLED (Galaxy Z Fold3, 2021) already removes the polarizer by putting a colour filter on the encapsulation, saving about 50–100 µm of thickness. | thelec.net; oled-info.com
IDEA 3: Sub-creep strain budget fold
KILLER | Fraction of the 180° bend that does not recover after 8 h folded at 60 °C. The depth of a free crease is about πR·θ/8, which I checked on an exact circle. | required ≤0.32 % unrecovered (≥99.7 % recovery) for ≤20 µm at R = 5 mm. The idea's own limit of 0.05 % residual strain at 0.5 % strain means 10 % unrecovered, an 18° residual angle and about 620 µm free sag. | available about 4–5 % unrecovered for the best foldable OCA (95–96 % recovery at 60 °C/93 % RH, USPTO 11348487 family). Polyurethane films at R = 5 mm kept 28–39 % (USPTO 9780318). Also, 60 µm bonded at R = 5 mm gives 0.6 % strain, not ≤0.5 %. | MARGIN 0.08
CHAIN | iPhone Duo-class stack | now 167 µm after 3000 folds | with idea about 250 µm free-state estimate at 4 % unrecovered and R = 5 mm, because a larger radius spreads the same set fraction over a longer arc. A supported panel would come out lower, which needs a prototype. | RATIO ~0.7–1
VERDICT | DEAD | A larger radius lowers strain, but the same unrecovered fraction spread over a 15.7 mm arc makes a deeper crease. It would need about 99.7 % recovery, and the measured OCA and film recoveries are 10–100x short. The 5 mm radius also pushes the folded phone past 12 mm, versus 8.9 mm for the Fold7.
NEW FACT | A standard static-fold test (5 mm radius, 24 h at 60 °C/93 % RH, then 24 h hanging) left crosslinked PU films at 50–70° and thermoplastic PU at 180°, meaning it did not unfold at all. | USPTO 9780318 / 10090480
IDEA 4: Large-radius tensioning teardrop hinge
KILLER | Peak shear the OCA must hold for as long as the phone stays open, at 60 °C, to carry the specified 0.1 % panel tension (T = 0.001 × EA = 2.74 kN/m, shear-lag length about 48 mm) | required ≈57 kPa | available ≈10.5 kPa, the same creep test level as Idea 1 (USPTO 11348487 family). Separately, the claim that every layer stays below 0.3 % at R = 3 mm fails: 30 µm UTG is at 0.5 % and 50 µm PET at 0.83 %. A layer would have to be ≤18 µm. | MARGIN 0.18
CHAIN | iPhone Duo-class stack | now 167 µm | with idea about 1 µm if the full tension holds, or about 6 µm after the tension relaxes to what the OCA can hold. Model only. | RATIO ~28 (model)
VERDICT | DEAD | The specified 0.1 % tension loads the edge bonds about 5x above the level where certified OCAs already creep. The model says about 25x less tension would be enough, but that is a re-spec, not the idea as written.
NEW FACT | Oppo's own figure for the Find N6 is about 0.05 mm (50 µm) surface variation. It is a manufacturer claim, not an independent measurement. | tomsguide.com

All four ideas share a problem: the crease is not a simple elastic dent, it is a set that grows with folds and time, as HTX's 48 → 167 µm over 3,000 folds shows. Everything above that I marked "model" is a beam calculation I wrote, not measured data. The single cheapest experiment is a coupon of the stack folded 2000 times, with 24 h held folded at 60 °C/90 % RH after every 500 folds. Then measure the depth with a profilometer, flat with no tension and again with about 120 N/m and 3 kN/m of in-plane tension.

Files are in /home/user/SomeRepository/engine/runs/foldcrease_b/gate/c1/:
- gate_calc.py
- coupled.py

Sources:
- [ithinkdiff – HTX 3,000-fold test](https://www.ithinkdiff.com/iphone-duo-crease-test-3000-folds/)
- [Notebookcheck – iPhone Duo crease](https://www.notebookcheck.net/iPhone-Duo-does-have-a-visible-crease-despite-Apple-s-clever-nano-texture-surface.1395055.0.html)
- [USPTO 11348487 (OCA modulus/creep at 60 °C)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11348487)
- [USPTO 9780318 (static fold recovery test)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9780318)
- [3M foldable OCA whitepaper](https://multimedia.3m.com/mws/media/1793258O/optically-clear-adhesives-for-foldable-oled-displays-whitepaper.pdf)
- [TheElec – Eco² COE](https://thelec.net/news/articleView.html?idxno=3239)
- [oled-info – Eco² OLED](https://www.oled-info.com/samsung-display-announces-polarizer-free-eco2oled-tech)
- [Tom's Guide – Oppo Find N6 0.05 mm](https://www.tomsguide.com/phones/android-phones/i-have-been-testing-oppo-find-n6-crease-free-foldable-phone)
IDEA 5: Unbonded sliding bend-zone laminate
KILLER | Length mismatch between the unbonded layers. The layers are bonded at both ends of the zone and the fluid carries no shear, so a 20 µm PI layer over a 15 mm free span buckles once the mismatch exceeds the clamped Euler strain π²t²/3L². | required: hold a thermal mismatch of 4×10⁻⁵ to 1.4×10⁻⁴ (ΔCTE 1–3.5 ppm/K over 40 K) | available: 5.9×10⁻⁶ Euler strain (exact arithmetic; PI CTE 5.2 ppm/K from RSC Polym. Chem. 2021; my UTG CTE of ~8.7 ppm/K is unsourced) | MARGIN 0.04 (0.15 at best)
CHAIN | iPhone Duo-style bonded stack | now 167 µm crease after 3000 folds (HTX Studio) | with idea: a 15 mm-wide band of wrinkles, gap-limited to ±2.5 µm but with about 24 mrad slope and a period of about 0.66 mm | RATIO ~2 by slope (estimated, assuming the Duo crease is about 10 mm wide)
VERDICT | DEAD | Bonding the layers at the zone ends means they cannot slide, so a few tens of ppm of thermal or creep mismatch buckles the free PI into a ripple that shows in reflection; the defect moves rather than disappears.
NEW FACT | When folded, bonding at the zone ends forces a membrane mismatch of πd/L = 0.63% into the PI, on top of its 0.5% bending strain. That is sustained tension in a polymer layer, which is exactly what drives creep. | gate_calc.py
NEW FACT | iPhone Duo peak-to-valley crease height: 48 µm new, 167 µm after 3000 folds (HTX Studio) | https://www.ithinkdiff.com/iphone-duo-crease-test-3000-folds/
IDEA 6: Liquid-coupled slip stack
KILLER | The same constraint on the thinnest unbonded layer (20 µm PI over a 10 mm strip). Folding also adds mismatch, so the claimed 0.75% strain does not hold. | required: hold 4×10⁻⁵ to 1.4×10⁻⁴ thermal mismatch, plus 1.41% fold mismatch at each fluid interface | available: 1.3×10⁻⁵ Euler strain (exact arithmetic; CTE sources as for idea 1) | MARGIN 0.09 (0.33 at best)
CHAIN | iPhone Duo-style bonded stack | now 167 µm after 3000 folds | with idea: gap-limited ripple of about 24 mrad slope across the strip, and up to about 2.8% cumulative tension in the OLED-on-PI layer when folded | RATIO ~2 by slope (estimated)
VERDICT | DEAD | Because the strip ends are bonded, the layers cannot slip, so the strain relief the idea claims does not happen and the free films buckle under ordinary thermal mismatch.
NEW FACT | With fluid films in place of OCA, the mismatch at each interface is πd/L ≈ 1.4% (d ≈ 45 µm, L = 10 mm). That is about double the 0.75% the idea claims. | gate_calc.py
IDEA 7: Tensioned drumhead hinge
KILLER | Peak OCA shear at the edges, held for as long as the phone is open, at the tension needed to flatten a 20 µm, 3 mm-wide set to 2 µm. That needs T ≈ 3.9 kN/m, or about 580 N over a 151 mm fold, given a stack bending stiffness D ≥ 3.9×10⁻⁴ N·m. | required: γ ≈ 1.8 at 25 °C and ≈ 2.3 at 80 °C, rising to about 2.5–3.2 with creep over months held open (shear-lag model; the creep growth is my estimate) | available: OCA designed for >300% shear and full recovery after up to 10 days folded (3M whitepaper), with G′ ≈ 90 kPa at 25 °C (US 11334117) and about 41% lower at 80 °C (Cao 2024) | MARGIN ≈ 0.9 (1.3–1.7 before creep)
CHAIN | iPhone Duo | now 167 µm after 3000 folds | with idea: about 16 µm residual at 3.9 kN/m (residual ratio Dk²/(Dk²+T) = 0.10) | RATIO ~10
VERDICT | WOUNDED | Closed-loop tension can mechanically flatten the crease by about 10x, but it holds about 580 N in the hinge and the OCA in near-limit shear for as long as the phone is open, well past the 10-day hold the adhesive is designed for.
NEW FACT | Foldable OCA storage modulus G′ is about 1.4×10⁵ Pa at −20 °C and about 9×10⁴ Pa at 25 °C | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11334117
NEW FACT | Foldable OCA must take more than 300% shear and recover fully after a static fold of up to 10 days | https://multimedia.3m.com/mws/media/1793258O/optically-clear-adhesives-for-foldable-oled-displays-whitepaper.pdf
IDEA 8: Drumhead tension hinge
KILLER | Tension accuracy of a cam that sets displacement rather than force. 600 N/m on a stack with Et ≈ 2.6×10⁶ N/m over a 136 mm span is a stroke of only 31 µm. | required: stroke error within ±9 µm to keep T within ±30% | available: ±30 µm best published assembly tolerance (Oppo N6, 0.03 mm), plus about 78 µm thermal drift between an aluminium frame and the UTG over 40 K | MARGIN 0.09 (0.31 with a titanium frame)
CHAIN | iPhone Duo | now 167 µm after 3000 folds | with idea: about 70 µm even at the nominal 600 N/m, because the full stack D (≥3.9×10⁻⁴ N·m, not UTG alone) gives a residual ratio of 0.42 | RATIO 2.4
VERDICT | DEAD | The tolerance and thermal drift swamp the 31 µm stroke, so the tension swings from slack to several times nominal; even at nominal tension, a 20 µm set only drops to about 8 µm, which is not invisible.
NEW FACT | Oppo N6: the hinge surface height variance went from 0.2 mm to 0.05 mm, and the crease is 82% shallower than the N5 per TÜV, but no µm value is published | https://www.gsmarena.com/oppo_details_find_n6s_impressive_creasefree_display-news-71887.php
NEW FACT | iPhone Duo reviews say the nano-texture hides the crease in daily use, but it can still be felt and seen at some angles. This supports the asker's description of Apple's approach. | https://www.iphoneincanada.ca/2026/10/21/iphone-duo-reviews-roundup/

**Judgement calls that drive the numbers:**
- **What counts as "invisible":** I set it at 2 µm residual for a 20 µm set. No published invisibility threshold exists, and this target sets the tension idea 3 needs.
- **Stack stiffness:** D = 3.9×10⁻⁴ N·m is a lower bound with the layers treated as uncoupled. Real coupling makes it higher, which makes ideas 3 and 4 harder.
- **Creep in idea 3:** the growth from about 1.8 to 3.2 shear while held open is my estimate, not a measured value.
- **UTG thermal expansion:** the ~8.7 ppm/K figure is from memory; I could not find a source. Even a 1 ppm/K mismatch keeps ideas 1 and 2 below 0.3.

Sources:
- [ithinkdiff – iPhone Duo crease after 3,000 folds](https://www.ithinkdiff.com/iphone-duo-crease-test-3000-folds/)
- [iPhone in Canada – iPhone Duo reviews roundup](https://www.iphoneincanada.ca/2026/10/21/iphone-duo-reviews-roundup/)
- [Notebookcheck – iPhone Duo visible crease](https://www.notebookcheck.net/iPhone-Duo-does-have-a-visible-crease-despite-Apple-s-clever-nano-texture-surface.1395055.0.html)
- [GSMArena – Find N6 crease-free display](https://www.gsmarena.com/oppo_details_find_n6s_impressive_creasefree_display-news-71887.php)
- [Android Authority – Find N6 durability](https://www.androidauthority.com/oppo-find-n6-zero-feel-crease-durability-3648272)
- [3M – OCAs for foldable OLED whitepaper](https://multimedia.3m.com/mws/media/1793258O/optically-clear-adhesives-for-foldable-oled-displays-whitepaper.pdf)
- [US 11334117 – Foldable display device](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11334117)
- [Cao 2024 – OCA modulus vs temperature](https://yuan.mae.sustech.edu.cn/pdf/2024Cao-polymer-science.pdf)
- [RSC Polym. Chem. 2021 – low-CTE colourless PI](https://pubs.rsc.org/en/content/articlehtml/2021/py/d1py00762a)
