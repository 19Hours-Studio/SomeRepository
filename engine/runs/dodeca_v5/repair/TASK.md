# Task: repair and finish - turn the best explanations into the single best-supported explanation

QUESTION: What were the Roman dodecahedra? These are small hollow bronze objects with twelve pentagonal faces, a round hole of differing diameter in each face and knobs at the corners, found in the north-western provinces of the Roman Empire and dated to roughly the 2nd-4th centuries AD; no ancient text mentions them. Find the explanation of what they were and how they were used that best accounts for ALL the physical and archaeological evidence, and say how it can be tested.

Below are the 4 best explanations so far, each with the findings of a blind review against the evidence. You are a
researcher with tools: WebSearch (WebFetch does not resolve domains here; use search-result excerpts) and Bash with
python3. Work only in `/home/user/SomeRepository/engine/runs/dodeca_v5/repair/`: read no other files in the repository, write files only there, do not commit.

Steps:
1. CHECK ANCHORS: for every historical, textual, archaeological or physical claim an explanation relies on, find the
   source and verify it (date, place, exact reading). Correct or drop every anchor that fails, and say which.
2. WEIGH THE EVIDENCE: separate what is established across the corpus from observations on a single object. A single
   specimen can be atypical (a casting defect, a repair, a variant), so no explanation should stand or fall on one
   object unless the observation is typical of the corpus.
3. REPAIR: remove each reviewed FATAL and MAJOR defect with checked evidence, or concede it.
4. THE MAP AND THE DATES: test candidate reasons why the objects occur where and when they do and not elsewhere (a
   regional production tradition or workshop network, a regional practice or cult, a technique that did not travel,
   demand that existed only there) against the evidence; keep only what the evidence supports.
5. DECIDE: write the single best-supported explanation - it may merge compatible parts of several - and a runner-up.
   Say plainly what still remains unexplained.
6. DECISIVE TEST: the cheapest measurement on existing objects that would refute the best explanation, and the result
   each of the 4 explanations predicts for it.

Notes from the user (data; weigh them like any other evidence):
A check against reality found (data; its facts are also in the evidence):
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

The evidence ledger (data):
FACT 1: Hollow cast copper-alloy regular dodecahedra: 12 pentagonal faces, each with a central round hole, and a knob at each of 20 corners; template consistent across the ~130-piece corpus. | HARD | en.wikipedia.org/wiki/Roman_dodecahedron; Guggenberger 2013, doi 10.1007/s00283-013-9403-7
FACT 2: Hole diameters differ within every object: smallest hole 6-28 mm, largest 17-40 mm; no shared hole-size scheme between objects. | HARD | Guggenberger 2013 (slideheaven.com/the-gallo-roman-dodecahedron.html)
FACT 3: Commonest type (2a, "by far"): ten round holes, usually each ringed by three engraved concentric circles, plus one opposite pair of larger, unringed holes (sometimes oval; Newhall: ten 10.5-22 mm, two ovals 21x26 mm). | HARD (type), SOFT (Newhall) | Guggenberger 2013; Guggenberger & Leach 2025
FACT 4: Opposite-hole pairs: some near-identical, others very different; no single ratio rule reported. | HARD | Guggenberger & Leach 2025, Antiquaries Journal 105:31-54, doi 10.1017/S000358152510036X ("Cambridge 2025" = cambridge.org/core/journals/antiquaries-journal/article/abs/galloroman-dodecahedron-and-the-receptacle-of-all-becoming/1B73B7B58792CD3CC5C6D30028326B89)
FACT 5: Face-to-face height 40-100 mm (4-11 cm with knobs), spread continuously; no standard module. | HARD | Guggenberger 2013; Wikipedia
FACT 6: Weight 35-580 g plus one outlier over 1,000 g; Norton Disney 8 cm, 245-254 g; Newhall 59 mm, 81 g. | HARD (range), SOFT (outlier) | Guggenberger 2013; aru.ac.uk/news/roman-dodecahedra-still-remain-a-mystery
FACT 7: DERIVED (my calc.py): those masses equal a bronze shell of only ~0.6 mm (40 mm/35 g) to ~1.6 mm (100 mm/580 g); Norton Disney ~1.0 mm; thin-walled, wall scaling with size. | SOFT | calc.py in this folder; wall thickness unpublished
FACT 8: Made by lost-wax casting, hollow. Only published alloy: Norton Disney pXRF ~75% Cu, 7% Sn, 18% Pb (another report ~63% Cu, 27% Pb); no corpus-wide composition data. | SOFT | bostonglobe.com/2024/04/30/world/12-sided-roman-relic-baffles-archaeologists-spawns-countless-theories; nottingham.ac.uk/news/norton-disney-dodecahedron
FACT 9: Count: 116 known by 2013; Guggenberger list now numbered 1-134 (129 hollow); popular sources 120-135. First find recorded 1739. | HARD (~130) | Cambridge 2025; nunc.ch/en/gallo-roman-dodecahedron-twelve-faces-zero-answers
FACT 10: About 70% from modern France and Germany, about 20% from Britain (33 known; 33/134 = 25% by my count); about 90% inside the Gallic Empire area (260-274 AD). | HARD | Cambridge 2025; nunc.ch above
FACT 11: Countries: Austria, Belgium, France, Germany, Hungary, Luxembourg, Netherlands, Switzerland, UK; none in Italy, Spain, Africa or elsewhere around the Mediterranean. | HARD | livescience.com/archaeology/romans/roman-dodecahedron-a-mysterious-12-sided-object-that-has-baffled-archaeologists-for-centuries; english-heritage.org.uk/visit/places/corbridge-roman-town-hadrians-wall/dodecahedron-exhibition
FACT 12: Eastern limit: Brigetio (Hungary), then a 2021-published fragment from Deonica, Serbia (SE-most); fragments from Hurbanovo and Chotin, Slovakia (Wikipedia: two objects; Dragonidesova: three fragments), lie outside the empire in Germanic settlements. | HARD | Wikipedia; Dragonidesova 2025, sav.sk/journals/uploads/0128234503_Dragonidesova.pdf
FACT 13: Dating is by context only (2nd-4th c. AD; bronze cannot be radiocarbon-dated): Jublains c. 200 AD (pottery, coins); Krefeld-Gellep grave 3040 and Saint-Parize-le-Chatel coin hoard 4th c.; Norton Disney provisionally late 3rd-early 4th c. | HARD | Cambridge 2025; nunc.ch above; nottingham.ac.uk/news/norton-disney-dodecahedron
FACT 14: Of finds with known findspot, over half are civil (urban or rural settlement), under a fifth military, about 8.5% plausibly sacred, about 4% hoards. | HARD | nunc.ch above (Guggenberger survey); Cambridge 2025
FACT 15: Contexts named: forts (Feldberg, Zugmantel, Carnuntum), bathhouse (Arles), by a theatre (Besancon), rich graves of both sexes (Krefeld-Gellep, Bachem), well fill, rivers (Nijmegen, Trier, Zurich), refuse pits. | SOFT | nunc.ch above (single translated list)
FACT 16: Few come from excavations and fewer from stratified deposits; most are antiquarian or market finds with unknown context. | HARD | Cambridge 2025; Dragonidesova 2025
FACT 17: Gellep grave 3040 (woman, 4th c.): object lay beside a rod-shaped bone piece, read as a possible sceptre shaft. | SOFT | Wikipedia; livescience (above)
FACT 18: No ancient text mentions them; no relief, mosaic or painting depicts one. | HARD | aru.ac.uk (above); Wikipedia
FACT 19: No inscribed letters or numbers on any piece. | HARD | Wikipedia
FACT 20: Rarely show wear; Norton Disney is complete and unworn. No published microscopic use-wear survey of knobs, hole rims or interiors found. | HARD (reported), untested | Wikipedia; theconversation.com/beautifully-crafted-roman-dodecahedron-discovered-in-lincoln-but-what-were-they-for-229131
FACT 21: Wax residue reported in one German piece, unlocated; sceptics: casting residue. | SOFT | bigthink.com/strange-maps/roman-dodecahedrons
FACT 22: No textile fibre or yarn residue reported; knitting claims rest on form alone. | SOFT | thedebrief.org/mysterious-roman-dodecahedrons-have-baffled-researchers-for-centuries-these-theories-could-help-solve-the-mystery; Wikipedia
FACT 23: Kortessem (Flanders), announced 10 Jan 2023: fragment of a 5-6 cm piece with ancient repair; broken edges read as deliberate. | HARD (find), SOFT (deliberate) | vrt.be/vrtnws/en/2023/01/10/second-mysterious-dodecahedron-found-in-flanders
FACT 24: Norton Disney (Lincolnshire, 2023): complete, upper fill of a Roman quarry or rubbish pit with pottery and demolition rubble, near a villa and the Fosse Way and a horse-and-rider god figurine; first Midlands find, 33rd British. | HARD (context), SOFT (ritual link) | the-past.com/feature/a-multi-sided-story-examining-the-norton-disney-dodecahedron-in-its-wider-context
FACT 25: Some South Shields (Arbeia) hole rims carry incised triple rings; one of its holes is unringed. | SOFT | romanarmytalk.com/rat/showthread.php?tid=7529
FACT 26: Catalogued by Nouwen 1993 (77 pieces, Tongeren); over 50 theories, most judged refuted or improbable. | HARD | Live Science (above); bitcoin.com/these-12-sided-roman-bronze-objects
FACT 27: Rangefinder idea (opposite holes as similar-triangle sights) is worked example only, never tested for accuracy; size variation argues against a shared measure. | SOFT | arxiv.org/pdf/1204.6497; arxiv.org/pdf/1206.0946
FACT 28: Wax-forming trial with a 65 mm 3D-printed PLA replica gave repeatable bosses; authors claim plausibility, not proof; gaming use discarded. | SOFT | exarc.net/issue-2026-2/rev/functional-reassessment-roman-dodecahedra-tools-forming
FACT 29: Guggenberger & Leach 2025 read them as symbolic (Plato's receptacle, Pythagorean and Druidic ideas); the argument rests on texts and distribution, not on object evidence. | SOFT | Cambridge 2025; wasteflake.com/tiki-read_article.php?articleId=45
FACT 30: Newcastle PhD (Hitchens, BAA award 2025) is running pXRF on Bonn (LVR) dodecahedra; no results seen. | SOFT | thebaa.org/award/hitchens-2025
GAPS:
- Use-wear, residue and lipid, wax or fibre analysis (SEM, microscopy) of knobs, hole rims and interiors would separate tool, vessel and symbol; LVR-LandesMuseum Bonn, Gallo-Romeins Museum Tongeren and Jublains hold the pieces.
- Per-object tables (all 12 hole diameters, wall thickness, mass, alloy, CT scans of cores) would test whether hole sizes encode a system; Guggenberger's list nos. 1-134 and Nouwen 1993 hold the raw data.
- No casting workshop, mould or core debris is known; production site and date are unresolved, so the Gallic-Empire link is untested.
- Grave and hoard associations (Gellep 3040 at Krefeld, Bachem, Saint-Parize) need full inventories to show which objects travel with them.
- Reason for Mediterranean absence and Slovak imports remains unexplained; Hitchens pXRF data could show regional alloy groups.
FACT 31: A 4th-c. silvered-lead dodecahedron from Saint-Pierre Cathedral, Geneva (excavated 1982), carries the Latin zodiac names on its 12 faces, so FACT 19 holds only for the hollow bronze type | NEW from audit_a, check before relying on it | ge.ch/actualite/objets-archeologiques-episode1-3-11-2021
FACT 32: A Roman icosahedron from Arloff, long misclassified as a dodecahedron, is in the LVR-LandesMuseum Bonn; the polyhedral family is wider than the dodecahedron | NEW from audit_a, check before relying on it | en.wikipedia.org/wiki/Roman_dodecahedron
FACT 33: The Gellep bone rod (~15 cm × 3 cm) was too decayed to recover, so the sceptre link cannot be re-examined | NEW from audit_a, check before relying on it | livescience (above)
FACT 34: A knobbed regular dodecahedron always rests on 5 knobs around one face, never on 3 (convex-hull check) | NEW from audit_a, check before relying on it | own python calculation
FACT 35: calc.py, cited as the source of FACT 7, is not in the audit folder; recomputing gives a wall of 0.60-1.58 mm before subtracting the holes, which confirms the range | NEW from audit_a, check before relying on it | own recalculation
FACT 36: **Tongeren** (opposite pairs 10.6/13.0, 13.8/14.0, 25.2/27.0, 23.0/26.3, 15.6/17.8, 20.3/20.5 mm). Opposite pairs differ by 0.2–3.3 mm, 10.1 mm in total, against 40.2 mm for chance pairing. Exact p = 0.0005. | NEW from reality, check before relying on it | [wingarden.de](http://www.wingarden.de/wing/dodekaeder.html); holes.py
FACT 37: **Sparavigna's 12-hole table** (10.5–22 mm plus two ovals of about 26×21.5 mm, pairs as she published them). Opposite pairs differ by 13.0 mm in total, against 35.2 mm for chance. Exact p = 0.010, and the result holds whichever oval axis is used. Four of the six pairs differ by 1 mm or less. The two pairs that don't match, 10.5/17 and 15.5/11.5, would also match if two face labels were swapped, so this may be a labelling slip. Combining both objects gives p ≈ 7×10⁻⁵. | NEW from reality, check before relying on it | [arxiv 1204.6497](https://arxiv.org/pdf/1204.6497), [1206.0946](https://www.arxiv.org/pdf/1206.0946); holes.py
FACT 38: Where this table comes from is unclear. The same numbers are credited to Jublains (Sparavigna), to a 59 mm, 81 g piece that is possibly from Avenches ([nunc.ch](https://nunc.ch/en/gallo-roman-dodecahedron-twelve-faces-zero-answers/)), and to Krefeld-Gellep. FACT 3's "Newhall" data and FACT 6's Newhall weight (81 g) are probably this same object counted twice. | NEW from reality, check before relying on it | search excerpts above
FACT 39: Two measurements of the same hole on a Carnuntum piece differ by 0.3 mm (16.0 vs 16.3 mm), which gives a sense of measurement error. This is far smaller than the gap between paired holes and random pairing. Greiner's re-measurement found one opposite pair with zero difference, which rules out the rangefinder reading for that pair. | NEW from reality, check before relying on it | [liberalter.wordpress.com](https://liberalter.wordpress.com/2025/09/02/wozu-diese-romischen-dodecahedra/) (blog, secondary)

Final answer (text only), in this order:
=== IDEAS ===
IDEA 1
NAME: (max 6 words)
MECHANISM: (4-7 sentences: what the thing was, who used it and how, what each distinctive feature did, and why it occurs only in that region and period)
VALUE: (2-3 sentences: which hard facts it explains that the others do not, what remains unexplained, and the decisive test with its refuting result)
IDEA 2
(the runner-up, same format)
=== NOTES ===
Anchors checked (kept / corrected / dropped, with sources); the single-object weighing; the map-and-dates finding; a
table of the decisive test with each explanation's predicted result.

THE 4 EXPLANATIONS, WITH THEIR BLIND REVIEWS:
IDEA 1
NAME: Unwritten twelve-face lot
MECHANISM: The object was a lot for drawing omens, cast by hand onto soft ground or cloth. Each face was identified by its hole size instead of by numbers. Because the holes had to differ, variation within each object is required, and the lack of any shared scheme between objects follows from each maker setting their own sizes. The two large unringed holes marked the "special" outcomes, and the knobs made the object come to rest on a face. Occasional private use explains the lack of wear and the silence of the texts.
VALUE: Unlike other divination ideas, it makes the absence of inscriptions and the varied holes necessary rather than awkward. Test: check knob tips under a microscope for even, all-round micro-flattening and compare it with the unused Norton Disney piece. If the corpus shows no such wear, the idea is refuted.
BLIND REVIEW:
- MAJOR: Its central claim that the faces had to be uninscribed is undercut by a related 4th-c. object: the silvered lead dodecahedron from Saint-Pierre, Geneva, carries the Latin zodiac names on its 12 faces. When a 12-face prediction object was wanted, people inscribed it. (ge.ch "Objets archéologiques - Episode#1" (NEW FACT))
- MAJOR: Identification by hole size fails where opposite holes are near-identical, and in type 2a the ten ringed holes span only about 10-22 mm, about 1.2 mm per step. That is hard to read reliably by eye. (FACT 3, FACT 4 (Newhall))
- MAJOR: The test contradicts itself: the idea says occasional use on soft ground leaves no wear, yet makes "no knob flattening" the refuting result. That result is already the reported state of the corpus. (FACT 20)
- FIT: 9 of 17 | It fits the differing holes within each object, the lack of a scheme between objects, the absence of inscriptions, the silence of texts and resting on a face, though resting on a face holds for any knobbed dodecahedron.
- SURVIVES: The knobbed dodecahedron does come to rest on one face (5-knob support, my check), so "lands on a face" is mechanically correct.
- KNOWN: yes | Dice and divination are long listed; criticised on the inscription and knob grounds (mentalfloss; Wikipedia); "gaming use discarded" (exarc 2026)

IDEA 2
NAME: Thin-wall casting masterpiece
MECHANISM: The object was a provincial bronzesmith's proof of mastery: a hollow geometric shell with a wall of about 0.6–1.6 mm, cast around a clay core. Each face hole held a support for the core and later let the core be broken out. That is why every face has a hole, why hole sizes are freehand and unstandardised, and why the interiors are rough. The knobs are vents or feeders at the corners, which are the last points to fill, later shaped into a decorative finish. The engraved rings and lack of wear show display rather than use. Its value as a valued keepsake explains its presence in graves, hoards and rich houses.
VALUE: It explains the holes in all twelve faces, the varying diameters, the rough interiors, the thin walls that scale with size, and the absence of wear, without needing any user function. Refutation test: CT-scan pieces in Bonn or Tongeren. If the holes were cut through an originally closed shell (tool marks on the hole walls) and there are no core residues or chapter-pin traces, the idea fails.
BLIND REVIEW:
- MAJOR: Core supports don't require holes that differ systematically from 6 to 40 mm within one object, a recurring large oval opposite pair, or engraved triple rings. Those are deliberate finishing choices that a casting rationale doesn't explain. (FACT 2, FACT 3)
- MAJOR: A guild "masterpiece" system is a medieval institution with no Roman evidence. Bronzesmiths worked throughout the empire, so the idea leaves the absence from Italy and the Mediterranean unexplained. (FACT 11; Wikipedia (Schwarz's own caveat))
- MAJOR: Twenty corner vents or feeders is not credible foundry practice for a ~1 mm shell, and the knobs are finished balls. No vent stubs are reported. (FACT 1; FACT 7 (my recalculation 0.60/1.58/1.07/0.64 mm before subtracting the holes; calc.py is not actually in the folder))
- MAJOR: The refutation needs two conditions at once (cut holes AND no core or chaplet traces), which makes it hard to trigger. Core-hole casting would also be true of any hollow function, so a positive result doesn't separate masterpiece from tool or symbol. (GAPS; FACT 8)
- FIT: 10 of 17 | It fits the hollow form, a hole in every face, the lack of a scheme, the size range, the lack of wear, the silence of texts, Kortessem's repair and the deposit types.
- SURVIVES: Holes as core prints or core-removal openings is the best mechanical account of why every face is pierced, and CT on Bonn or Tongeren pieces is feasible.
- KNOWN: yes | Rüdiger Schwarz (Saalburg), masterpiece and test-piece reading (Wikipedia; mentalfloss); "production holes" wording in Guggenberger & Leach 2025

IDEA 3
NAME: Platonic cosmic receptacle
MECHANISM: The dodecahedron, the Platonic solid tied to the cosmos, was made in Gaul and Britain as a material "receptacle" in Pythagorean-Platonic spirit, a philosophy Druids were said to admire. The twelve pentagonal faces embody the universe; holes and knobs are decorative or ritual variation, hence no standard sizes. A rod-shaped bone object beside the Gellep grave specimen suggests staff mounting, like a scepter of spiritual authority. Absence from Italy follows from its Celtic provincial origin.
VALUE: It explains the geography, lack of wear, lack of standardisation and silence of texts. Proponents propose better-contexted finds and evidence of mounting.
BLIND REVIEW:
- MAJOR: It explains the 12 faces through the Platonic solid but calls the holes and knobs "decorative or ritual variation", which leaves the most distinctive patterned features without a mechanism: why ten ringed holes plus one opposite pair of larger, unringed holes. (FACT 2, FACT 3 (Guggenberger 2013))
- MAJOR: The Druid-Pythagorean link needs a working Druidic intellectual class in the 2nd-4th c., but Druidism was banned under Tiberius and Claudius in the 1st c. AD, and the dated contexts run c. 200 to the 4th c. (FACT 13; Suetonius, Claudius 25; Pliny, NH 30.13)
- MAJOR: The sceptre-mount claim rests on one bone rod that was too decayed to recover, and the bone had passed through the "production holes". A staff mount would also predict socket wear on one hole pair, which is not reported. (FACT 17, FACT 20; livescience (above); Cambridge 2025 core reader)
- MAJOR: The evidence is texts plus distribution, not the objects themselves, and the "test" (better-contexted finds, evidence of mounting) names no result that would refute it. Mounting evidence would fit insignia readings just as well. (FACT 29, FACT 16)
- FIT: 9 of 17 | It fits the geography, the silence of texts and art, the absence of inscriptions, the lack of wear and the varied contexts, but only by setting the hole system aside.
- SURVIVES: The 12-face form does match the Platonic cosmic solid, and the north-western distribution is described correctly.
- KNOWN: yes | Guggenberger & Leach 2025, Antiquaries Journal 105:31-54; Guggenberger's sceptre reading of Gellep (Wikipedia; Tongeren museum essay)

IDEA 4
NAME: Apotropaic household display object
MECHANISM: The piece stood on three knobs in a household or bath shrine. Its triple-ringed holes worked as "eyes" averting harm, and its twelve faces stood for the cosmos. Light passing through the holes mattered more than their exact sizes, so hole sizes are free variation set by the wax modeller. When a house or person ended, the object was retired, sometimes broken or repaired, into wells, rivers, pits, graves and hoards.
VALUE: It explains the random hole sizes, the absence of wear and the mixed deposition, which tool readings cannot. Refutation: per-object tables of the 12 diameters (Guggenberger 1-134) show a consistent ratio scheme, or wear facets concentrate on three-knob triads rather than being absent.
BLIND REVIEW:
- MAJOR: It is geometrically wrong: with a knob at each of the 20 corners, the support planes are the 12 face planes, so the object always rests on five knobs around a face and never on three. A convex-hull check gave 5 knob tips on every support plane. That also makes the proposed "three-knob triad wear" test impossible. (FACT 1; my python convex-hull check)
- MAJOR: "Free variation set by the modeller" contradicts the repeated, structured type 2a: one opposite pair of larger, unringed, sometimes oval holes recurs across the corpus, which is not random. (FACT 3 (Guggenberger 2013, "by far" commonest))
- MAJOR: "Shrine" and "eyes averting harm" are not supported by findspots: only about 8.5% are plausibly sacred, over half are civil, and no shrine or lararium assemblage is reported. (FACT 14)
- MAJOR: Its first refutation test is already decided: the corpus is known to lack a shared hole scheme, so the "ratio scheme" outcome cannot occur, and the test cannot refute anything. (FACT 2, FACT 4)
- FIT: 9 of 17 | It fits the lack of wear, the mixed deposition, Kortessem, the uninscribed faces and the silence of texts, but not the patterned type 2a or the geometry.
- SURVIVES: Reading the triple rings as "eye" motifs is a reasonable iconographic suggestion; ring-and-dot motifs are common on Roman small finds.
- KNOWN: partly | General religious, candle-holder and decorative readings are widely listed (Wikipedia; mentalfloss); the specific apotropaic "eye" reading has no named proponent that I found.

