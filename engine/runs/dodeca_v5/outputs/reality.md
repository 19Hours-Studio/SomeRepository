I tested two quantities from published per-face hole measurements. On two objects, opposite holes are matched in size far more often than chance allows. That hurts Ideas 4 and 1 most and gives Idea 2 some support, but only two complete per-face tables could be found.

=== REALITY ===

**OBSERVABLE 1: How opposite holes pair up.** Each object has six axes running through opposite faces. The quantity is the sum of the size differences between the two holes on each axis, compared with every possible way of pairing the same 12 holes (10,395 pairings).
Predictions:
- **Idea 4 (apotropaic display):** sizes are random variation, so opposite pairs should be no more alike than chance.
- **Idea 3 (Platonic receptacle):** the holes are "decorative variation", so it predicts no pattern either.
- **Idea 1 (lot):** all 12 faces must differ, so near-twin opposite pairs are unwelcome.
- **Idea 2 (casting):** holes are openings for supporting or removing the core, so planning by axis fits but isn't required.
- **Rangefinder (FACT 27):** opposite holes must differ by a set ratio.

**OBSERVABLE 2: How many faces can be told apart by eye.** I counted the separable size classes at different discrimination limits (2–10%). Idea 1 needs 12 classes. The other ideas predict nothing.

**VALIDATION** (`holes.py`):
- **Counting test:** a synthetic object with holes spaced 8% apart gave 12 classes at a 5% limit and 1 class at 10%. Twelve identical holes gave 1 class.
- **Pairing test, no-pattern case:** on 300 random objects with random pairing, it flagged 3.7% at a 5% significance cut-off. That is within the expected rate.
- **Pairing test, planned case:** on objects built with one size per axis plus about 1 mm of noise, it detected the pattern 98% of the time.

NEW FACT | **Tongeren** (opposite pairs 10.6/13.0, 13.8/14.0, 25.2/27.0, 23.0/26.3, 15.6/17.8, 20.3/20.5 mm). Opposite pairs differ by 0.2–3.3 mm, 10.1 mm in total, against 40.2 mm for chance pairing. Exact p = 0.0005. | [wingarden.de](http://www.wingarden.de/wing/dodekaeder.html); holes.py

NEW FACT | **Sparavigna's 12-hole table** (10.5–22 mm plus two ovals of about 26×21.5 mm, pairs as she published them). Opposite pairs differ by 13.0 mm in total, against 35.2 mm for chance. Exact p = 0.010, and the result holds whichever oval axis is used. Four of the six pairs differ by 1 mm or less. The two pairs that don't match, 10.5/17 and 15.5/11.5, would also match if two face labels were swapped, so this may be a labelling slip. Combining both objects gives p ≈ 7×10⁻⁵. | [arxiv 1204.6497](https://arxiv.org/pdf/1204.6497), [1206.0946](https://www.arxiv.org/pdf/1206.0946); holes.py

NEW FACT | Where this table comes from is unclear. The same numbers are credited to Jublains (Sparavigna), to a 59 mm, 81 g piece that is possibly from Avenches ([nunc.ch](https://nunc.ch/en/gallo-roman-dodecahedron-twelve-faces-zero-answers/)), and to Krefeld-Gellep. FACT 3's "Newhall" data and FACT 6's Newhall weight (81 g) are probably this same object counted twice. | search excerpts above

NEW FACT | **Faces that can be told apart.** I assumed a 5–10% discrimination limit for holes seen one at a time.
- Sparavigna object: 4–6 classes at 5–10% (3 if the ovals are counted by their mean width), and 9 even at 2%. Two pairs of holes are exactly equal (17/17 and 22/22).
- Tongeren: 6–8 classes at 5–10%, and 10 at 2%.
Neither object gives 12 readable faces. | holes.py

NEW FACT | Two measurements of the same hole on a Carnuntum piece differ by 0.3 mm (16.0 vs 16.3 mm), which gives a sense of measurement error. This is far smaller than the gap between paired holes and random pairing. Greiner's re-measurement found one opposite pair with zero difference, which rules out the rangefinder reading for that pair. | [liberalter.wordpress.com](https://liberalter.wordpress.com/2025/09/02/wozu-diese-romischen-dodecahedra/) (blog, secondary)

NEW FACT | **Overall spread on other objects:**
- Fishguard: apertures 27.67–40.55 mm on a 127.7 mm, 553 g object ([British Museum H_1924-0411-1](https://www.britishmuseum.org/collection/object/H_1924-0411-1)).
- Braunschweig: the largest spread between holes within one object is 26 mm ([Guggenberger, Ferdinandeum](http://wwwhomes.uni-bielefeld.de/tkohers/R%F6mischer%20Dodekaeder/Guggenberger,%20Etwas%20Gewisses%20hievon%20zu%20bestimmen%20waere%20ein%20Gewagtes,%20260%20Jahre%20Dodekaederforschung.pdf)).
- East Riding (PAS YORYM-41CD72): "large, irregularly cut holes" ([finds.org.uk](https://finds.org.uk/database/artefacts/record/id/246648)). That matters for Idea 2's cut-versus-cast-holes test.

**VERDICT**
- **Idea 4 (apotropaic display) is hurt badly.** Hole sizes are not free variation: on both objects the makers sized the holes axis by axis, matching opposite holes.
- **Idea 1 (lot) is hurt badly.** There are only about 4–8 readable sizes, two exactly equal pairs, and near-twin opposite holes. In practice the object has about six readable outcomes, not twelve.
- **Idea 3 (Platonic receptacle) is hurt moderately.** The hole system has a structure that "decorative variation" doesn't predict.
- **Idea 2 (casting) gets modest support.** Openings planned by axis fit a core held or removed through opposite holes, or anything passing straight through the object along an axis. The bone rod that passed through the Gellep piece points the same way. But this doesn't separate the masterpiece reading from a tool used along an axis.
- **The rangefinder is hurt.** Pairs with near-zero difference give no usable ratio.
- **Caveats:** this rests on only two full tables, one of uncertain origin and one from a hobby website. The decisive next step is to run the same pairing test on Guggenberger's 2024 catalogue measurements (*Die römischen Dodekaeder*, nos. 1–134). Matched axes across the whole corpus would confirm "six designed axes". Random pairing would overturn this.

Files are in /home/user/SomeRepository/engine/runs/dodeca_v5/reality:
- holes.py