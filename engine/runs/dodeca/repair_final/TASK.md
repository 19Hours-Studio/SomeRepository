# Task: repair and finish - turn the best explanations into the single best-supported explanation

QUESTION: What were the Roman dodecahedra? These are small hollow bronze objects with twelve pentagonal faces, a round hole of differing diameter in each face and knobs at the corners, found in the north-western provinces of the Roman Empire and dated to roughly the 2nd-4th centuries AD; no ancient text mentions them. Find the explanation of what they were and how they were used that best accounts for ALL the physical and archaeological evidence, and say how it can be tested.

Below are the 4 best explanations so far, each with the findings of a blind review against the evidence. You are a
researcher with tools: WebSearch (WebFetch does not resolve domains here; use search-result excerpts) and Bash with
python3. Work only in `/home/user/SomeRepository/engine/runs/dodeca/repair_final/`: read no other files in the repository, write files only there, do not commit.

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
The single specimen with repeated hole sizes (Jublains) may be a casting defect or an atypical piece, so do not let one object decide. Why none were found around the Mediterranean is unclear to me - perhaps the technique never reached there - but look for the explanation the evidence supports best.

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
Found by the blind reviewers of round 1 (added to the ledger):
FACT 31: Jublains dodecahedron, the only published per-hole table: ten ringed holes 10.5-22 mm with repeated sizes (17/17, 22/22, 21/21.5 mm); two oval unringed holes 26x21.5 and 25.5x21.5 mm; the five ringed holes around one pole average 17.5 mm, around the other 17.4 mm. | HARD (one object) | Sparavigna 2012, arXiv 1204.6497
FACT 32: The Arloff icosahedron (Bonn) is hollow-cast with corner knobs, like the dodecahedra, but has holes in only two opposite faces. | SOFT (one object) | en.wikipedia.org/wiki/Roman_dodecahedron
FACT 33: The larger unringed pair is less round and is read by the corpus specialists as a production feature. | SOFT (interpretation) | Guggenberger & Leach 2025, Antiquaries Journal 105
FACT 34: Resting on its knobs, every dodecahedron has its opposite-hole axes at 26.565 or 90 degrees to the horizontal (dihedral angle 116.57 degrees). | HARD (geometry) | geometry
FACT 35: The north-western provinces had full Roman dice culture, including a 4th-c. dice tower (Vettweiss-Froitzheim, Bonn). | HARD | LVR-LandesMuseum Bonn
FACT 36: Germanic lots (Tacitus, Germania 10) were wooden slips marked with signs and thrown onto a white cloth; dodecahedra are almost absent from free Germania. | HARD | Tacitus, Germania 10; FACT 12
FACT 37: Insignia staffs are shown on north-western provincial monuments (beneficiarius lance on the Friedberg altar). | SOFT | mithraeum.eu/monument/1480
FACT 38: The Druids were suppressed under Tiberius and Claudius (Pliny NH 30.13; Suetonius, Claudius 25), 150-300 years before the objects. | HARD | Pliny NH 30.13; Suetonius, Claudius 25

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
NAME: Touch-coded casting lot
MECHANISM: Tossed onto cloth, it tumbles on its knobs and settles with one face up. That face is read by its hole (size, ringed or not; the large unringed pair a distinct outcome), legible by eye or finger, so no letters were needed, and since each owner knew their own piece, neither a shared scheme nor fairness mattered. A light shell landing on cloth wears little. It belongs to north-western lot-casting (Tacitus describes Germanic lots thrown onto a white cloth), not Mediterranean dice culture, fitting distribution, civil and grave contexts and textual silence.
VALUE: It explains why holes differ within each object yet share no scheme between objects, and why nothing is inscribed. On 10+ pieces, microscope knob tips against protected recesses: repeated tumbling polishes tips, so tips as fresh as recesses refute it.
BLIND REVIEW:
- MAJOR: Its cultural anchor misfires: Tacitus' lots are marked slips scattered on the cloth, of which three are then picked up and read by their signs, not by how they land, and dodecahedra are almost absent from free Germania, where that practice was. (Tacitus, Germania 10 ("ter singulos tollit"); FACT 36; FACT 12)
- MAJOR: "Not Mediterranean dice culture" is wrong and leaves the map unexplained: the north-west had full Roman dice culture, and Italy had lot oracles (the Praeneste sortes) yet no finds. (FACT 35; FACT 11; Cicero, De Divinatione 2.85-86)
- MAJOR: The test contradicts the mechanism: if landing on cloth "wears little", fresh knob tips are what the idea itself predicts, so they cannot refute it, and corrosion masks polish anyway. (FACT 20; idea text)
- SURVIVES: The knobs (resting geometry, FACT 34), the hole variation within each piece, the missing shared scheme, the absence of inscriptions, the low wear and the civil and grave contexts all follow from one mechanism.

IDEA 2
NAME: Fumigation cage for aromatics
MECHANISM: Resin or herbs on a small ember went in through the largest hole; then it sat on a smaller-holed face, ember over that hole. Knobs lift it to admit air while upper holes vent smoke, and turning it to another face changes intake and smoulder rate, so holes needed only to differ within a piece; rings are ornament. The thin shell heats fast, knobs give cooler grips, use causes no wear, and the wax specimen is residue. Domestic, bath, theatre and funerary fumigation fits the mixed contexts, a regional form of a common rite, unnamed in texts.
VALUE: It explains knobs as stand-offs, the perforated hollow and the wax specimen together, which symbolic and instrument readings do not. Clean interiors on 10+ pieces, with no soot, charred resin or heat tint and no resin markers by GC-MS, refute it.
BLIND REVIEW:
- MAJOR: It calls this a regional form of a rite that was common everywhere, yet the Mediterranean had turibula/thymiateria and the north-west itself had ceramic and bronze incense cups (Räucherkelche, tazze), so nothing explains why this cage occurs only in the north-west and never in Italy, Spain or Africa. (FACTS 10, 11; bronze Räucherkelch from Trier (journals.ub.uni-heidelberg.de/index.php/tz/article/view/54937); Walheim incense cup (bawue.museum-digital.de object 418))
- MAJOR: It waves away the most distinctive feature of the corpus, the type-2a pattern (ten triple-ringed holes plus one larger unringed opposite pair), as "ornament", since changing the draught by turning the piece needs only holes of different sizes. (FACTS 3, 31)
- MAJOR: Domestic, bath and funerary fumigation was an everyday practice, yet only ~130 pieces exist from three centuries and none is depicted, although incense burners appear widely in Roman art; this needs the unsupported assumption of a rare luxury variant. (FACTS 9, 18)
- MAJOR: Nothing in the mechanism yields the 2nd-4th-century window or the ~90% concentration in the Gallic-Empire area. (FACTS 10, 13)
- SURVIVES: No hard fact contradicts it, and its test (soot, heat alteration, diterpenoid resin markers by GC-MS in interiors) can refute it and is feasible on the Bonn, Tongeren, Jublains and Norton Disney pieces.

IDEA 3
NAME: Tallow-candle draught shade
MECHANISM: A home-dipped tallow candle passed up through whichever hole fitted its thickness, its foot on the table between the knobs; the flame burned draught-proof inside, the opposite hole venting smoke. Graded holes suit irregular candles, so no shared scheme was needed; the unringed core openings admitted a light, and rings mark designed holes. North of the olive line Baetican lamp oil dwindled after c. 200, making candles the light until c. 400.
VALUE: It derives hole range, knobs, scarce wax (tallow was normal) and map from lighting economics. Rims and interiors of 10+ pieces lacking both animal-fat lipids (GC-MS) and soot refute it.
BLIND REVIEW:
- MAJOR: The dating mechanism is misdated: in Britain oil lamps were already rare after the 1st century and confined mainly to forts and large towns, so tallow candles were the normal light about a century before the earliest dated pieces (c. 200 AD), and an oil decline after 200 cannot explain the start date. (FACT 13; Eckardt, Illuminating Roman Britain (2002); Colchester collections record (cim-web.adlibhosting.com/ais6/Details/collect/181098))
- MAJOR: A household lighting device used across a tallow-burning region for two centuries should survive in thousands, like lamps and candlesticks, not ~130, and lighting gear (candelabrum, laterna) is named and depicted while this object never is. (FACTS 9, 18)
- MAJOR: The rings and the larger unringed opposite pair get only labels; a candle uses one bottom hole and one vent, so the other ten holes are idle leaks that defeat "draught-proof". (FACTS 1, 3)
- SURVIVES: The geometry works (the candle hole and the vent hole lie on one vertical axis when it rests on its knobs, FACT 34), and the GC-MS lipid plus soot test is feasible and can refute it.

IDEA 4
NAME: Native priest's radiate sceptre
MECHANISM: A short rod (as at Gellep) passed through the unringed core openings, so the ten ringed holes formed two radiating five-fold crowns, each holding a sacred-plant sprig; stems differed, hence varied holes and no shared scheme. Never grounded, it stayed unworn; knobs stopped it rolling on altars. Native priesthoods (Gaulish gutuatri; Romano-British priestly crowns and sceptres, known from finds, not images) existed only in the Celtic north-west and ended with the Theodosian bans.
VALUE: It makes the unringed axis, the five-fold form and graded holes necessary and derives art's silence. Ringed rims on 10+ pieces without stem scratches or plant residue refute it.
BLIND REVIEW:
- MAJOR: A priestly insignia should come mostly from shrines, graves and hoards, but over half of finds with a known findspot are civil settlements, under a fifth are military (forts at Feldberg, Zugmantel and Carnuntum), only ~8.5% are plausibly sacred, and Norton Disney lay in a rubbish/quarry pit; it needs unsupported loss or discard assumptions. (FACTS 14, 15, 24)
- MAJOR: The excavated Romano-British regalia it invokes have a different form (Wanborough: 17 sceptre handles with wooden shafts and bronze bindings, 4 chain head-dresses; Farley Heath: sceptre cap), no dodecahedron is reported among them, and the Wanborough group (mid-1st to mid-2nd c.) is older than most dodecahedra. (surreyarchaeology.org.uk (Green Lane, Wanborough); Esposito, traj.openlibhums.org/article/3978)
- MAJOR: Graded holes are not "necessary": a sprig or bundle sits in a hole of any size, so "stems differed" is an ad hoc reason for the hole variation inside every object, including repeated sizes. (FACTS 2, 31)
- MAJOR: The 20 knobs get no real function: a polyhedron on a rod cannot roll, and one lying on a face is already stable. (FACTS 1, 34)
- MAJOR: The test cannot refute it: soft plant stems do not scratch bronze, the theory itself predicts an unworn object, and plant residue seldom survives burial and conservation, so "no scratches, no residue" is also the result the theory expects. (FACTS 16, 20)
- SURVIVES: The rod through the unringed pair matches the specialists' own handle suggestion for Gellep, the crown geometry is correct, and gutuatri are attested in inscriptions (two Autun altars, EDH HD032385/HD032388).

