I screened all four ideas. Ideas 1, 2 and 4 come out DEAD and idea 3 comes out WOUNDED. The arithmetic is in `gate_calc.py`, with output in `gate_calc_out.txt` and notes in `notes.md`, all in the c2 directory. Nothing was committed. Two results were checked against known values before use: the 30 µm UTG bending stiffness came out at 1.68×10⁻⁴ N·m (idea 4 says 1.6×10⁻⁴), and the bonded-stack strain came out at 4.0% (idea 2 says about 4%).

The best current reference is a lab measurement the ledger did not have: an iPhone Duo crease measured 48 µm new and 167 µm after 3000 folds. I used 167 µm as "now" in every CHAIN line.

=== GATE ===
IDEA 1: Unbonded sliding bend-zone laminate
KILLER | Length mismatch between the unbonded layers. The layers are bonded at both ends of the zone and the fluid carries no shear, so a 20 µm PI layer over a 15 mm free span buckles once the mismatch exceeds the clamped Euler strain π²t²/3L². | required: hold a thermal mismatch of 4×10⁻⁵ to 1.4×10⁻⁴ (ΔCTE 1–3.5 ppm/K over 40 K) | available: 5.9×10⁻⁶ Euler strain (exact arithmetic; PI CTE 5.2 ppm/K from RSC Polym. Chem. 2021; my UTG CTE of ~8.7 ppm/K is unsourced) | MARGIN 0.04 (0.15 at best)
CHAIN | iPhone Duo-style bonded stack | now 167 µm crease after 3000 folds (HTX Studio) | with idea: a 15 mm-wide band of wrinkles, gap-limited to ±2.5 µm but with about 24 mrad slope and a period of about 0.66 mm | RATIO ~2 by slope (estimated, assuming the Duo crease is about 10 mm wide)
VERDICT | DEAD | Bonding the layers at the zone ends means they cannot slide, so a few tens of ppm of thermal or creep mismatch buckles the free PI into a ripple that shows in reflection; the defect moves rather than disappears.
NEW FACT | When folded, bonding at the zone ends forces a membrane mismatch of πd/L = 0.63% into the PI, on top of its 0.5% bending strain. That is sustained tension in a polymer layer, which is exactly what drives creep. | gate_calc.py
NEW FACT | iPhone Duo peak-to-valley crease height: 48 µm new, 167 µm after 3000 folds (HTX Studio) | https://www.ithinkdiff.com/iphone-duo-crease-test-3000-folds/

IDEA 2: Liquid-coupled slip stack
KILLER | The same constraint on the thinnest unbonded layer (20 µm PI over a 10 mm strip). Folding also adds mismatch, so the claimed 0.75% strain does not hold. | required: hold 4×10⁻⁵ to 1.4×10⁻⁴ thermal mismatch, plus 1.41% fold mismatch at each fluid interface | available: 1.3×10⁻⁵ Euler strain (exact arithmetic; CTE sources as for idea 1) | MARGIN 0.09 (0.33 at best)
CHAIN | iPhone Duo-style bonded stack | now 167 µm after 3000 folds | with idea: gap-limited ripple of about 24 mrad slope across the strip, and up to about 2.8% cumulative tension in the OLED-on-PI layer when folded | RATIO ~2 by slope (estimated)
VERDICT | DEAD | Because the strip ends are bonded, the layers cannot slip, so the strain relief the idea claims does not happen and the free films buckle under ordinary thermal mismatch.
NEW FACT | With fluid films in place of OCA, the mismatch at each interface is πd/L ≈ 1.4% (d ≈ 45 µm, L = 10 mm). That is about double the 0.75% the idea claims. | gate_calc.py

IDEA 3: Tensioned drumhead hinge
KILLER | Peak OCA shear at the edges, held for as long as the phone is open, at the tension needed to flatten a 20 µm, 3 mm-wide set to 2 µm. That needs T ≈ 3.9 kN/m, or about 580 N over a 151 mm fold, given a stack bending stiffness D ≥ 3.9×10⁻⁴ N·m. | required: γ ≈ 1.8 at 25 °C and ≈ 2.3 at 80 °C, rising to about 2.5–3.2 with creep over months held open (shear-lag model; the creep growth is my estimate) | available: OCA designed for >300% shear and full recovery after up to 10 days folded (3M whitepaper), with G′ ≈ 90 kPa at 25 °C (US 11334117) and about 41% lower at 80 °C (Cao 2024) | MARGIN ≈ 0.9 (1.3–1.7 before creep)
CHAIN | iPhone Duo | now 167 µm after 3000 folds | with idea: about 16 µm residual at 3.9 kN/m (residual ratio Dk²/(Dk²+T) = 0.10) | RATIO ~10
VERDICT | WOUNDED | Closed-loop tension can mechanically flatten the crease by about 10x, but it holds about 580 N in the hinge and the OCA in near-limit shear for as long as the phone is open, well past the 10-day hold the adhesive is designed for.
NEW FACT | Foldable OCA storage modulus G′ is about 1.4×10⁵ Pa at −20 °C and about 9×10⁴ Pa at 25 °C | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11334117
NEW FACT | Foldable OCA must take more than 300% shear and recover fully after a static fold of up to 10 days | https://multimedia.3m.com/mws/media/1793258O/optically-clear-adhesives-for-foldable-oled-displays-whitepaper.pdf

IDEA 4: Drumhead tension hinge
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