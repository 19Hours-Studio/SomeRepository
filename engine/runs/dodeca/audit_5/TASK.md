# Task: adversarial review - test each explanation against the evidence

QUESTION: What were the Roman dodecahedra? These are small hollow bronze objects with twelve pentagonal faces, a round hole of differing diameter in each face and knobs at the corners, found in the north-western provinces of the Roman Empire and dated to roughly the 2nd-4th centuries AD; no ancient text mentions them. Find the explanation of what they were and how they were used that best accounts for ALL the physical and archaeological evidence, and say how it can be tested.

Below are 6 explanations, mixed and unlabelled. Your job is to be the toughest competent outside specialist. You do
NOT fix or improve the explanations; you test each one against the evidence and rank its defects.

You have tools: WebSearch (WebFetch does not resolve domains here; use search-result excerpts) and Bash with python3.
Work only in `/home/user/SomeRepository/engine/runs/dodeca/audit_5/`: read no other files in the repository, do not modify other files, do not commit.

The evidence ledger (data, check and extend it with your own searches):
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
Corrections and additions from the final researcher (checked with search):
FACT 39 (corrects 8): the Norton Disney alloy figures come from an unpublished pXRF reading (unreliable for lead on a patina); the Deonica piece is brass-like, about 90% Cu and 5% Zn. | SOFT | languagelog.ldc.upenn.edu/nll/?p=73057; jagodina.museum/en/?p=17640
FACT 40 (replaces 21): the wax report comes only from popular sources and the piece cannot be located. | - | (dropped as evidence)
FACT 41 (corrects 24): the horse-and-rider figurine near Norton Disney was a 1989 metal-detector find near the villa, not from the pit. | HARD | the-past.com (Norton Disney feature)
FACT 42 (refines 13): Jublains came from a small cellared, probably commercial building that burned c. AD 200, with a bronze balance among the finds; the Feldberg (c. 150-260) and Zugmantel (c. 90-260) pieces were lost before c. 260. | HARD | Revue archeologique de l'Ouest 25 (2008), journals.openedition.org/rao/680
FACT 43: a 4th-century solid lead dodecahedron coated with silver, found in 1982 under Saint-Pierre cathedral in Geneva, carries the twelve zodiac names in Latin, one per face, and is interpreted as a divination die; it is outside the hollow corpus. | HARD (one object) | ge.ch/actualite/objets-archeologiques-episode1-3-11-2021
FACT 44 (derived from 31): the ten ringed Jublains holes fall into three tight classes (about 11, 16.5 and 21.5 mm) and the five faces around each pole hold the same set (1 small, 2 medium, 2 large); uniform random sizes give this about 0.06% of the time, so matched sizes were set in the wax model, not by a casting accident. One object only. | SOFT | arxiv.org/pdf/1204.6497; repair_final/work/check.py

For each explanation:
1. Go through the hard facts. Which does it CONTRADICT (FATAL), which does it need an extra unsupported assumption
   for (MAJOR), which does it leave unexplained although they are distinctive (MAJOR if the feature is distinctive,
   MINOR otherwise)?
2. Specificity: does it explain the distinctive features themselves, or would it fit any object of that period
   ("ritual", "status", "decoration" without a mechanism for the features is a MAJOR defect)?
3. Is the decisive test it proposes actually able to refute it, is it feasible with existing material, and what
   result would refute it?
Do not pad: a defect needs a fact and a source. If a part survives your check, say so in one line.

Final answer (text only), exactly this format:
=== REVIEW ===
IDEA 1: <name>
DEFECT | <FATAL/MAJOR/MINOR> | <one sentence: what is wrong> | <the fact or source that shows it>
(as many DEFECT lines as needed, most severe first)
FIT | <number of hard facts explained> of <number of hard facts that bear on it> | <one line>
SURVIVES | <what held up, one line>
(same for the other explanations, in the same order as below)

THE 6 EXPLANATIONS:
IDEA 1
NAME: Tallow-candle draught shade
MECHANISM: A home-dipped tallow candle passed up through whichever hole fitted its thickness, its foot on the table between the knobs; the flame burned draught-proof inside, the opposite hole venting smoke. Graded holes suit irregular candles, so no shared scheme was needed; the unringed core openings admitted a light, and rings mark designed holes. North of the olive line Baetican lamp oil dwindled after c. 200, making candles the light until c. 400.
VALUE: It derives hole range, knobs, scarce wax (tallow was normal) and map from lighting economics. Rims and interiors of 10+ pieces lacking both animal-fat lipids (GC-MS) and soot refute it.

IDEA 2
NAME: Touch-coded casting lot
MECHANISM: Tossed onto cloth, it tumbles on its knobs and settles with one face up. That face is read by its hole (size, ringed or not; the large unringed pair a distinct outcome), legible by eye or finger, so no letters were needed, and since each owner knew their own piece, neither a shared scheme nor fairness mattered. A light shell landing on cloth wears little. It belongs to north-western lot-casting (Tacitus describes Germanic lots thrown onto a white cloth), not Mediterranean dice culture, fitting distribution, civil and grave contexts and textual silence.
VALUE: It explains why holes differ within each object yet share no scheme between objects, and why nothing is inscribed. On 10+ pieces, microscope knob tips against protected recesses: repeated tumbling polishes tips, so tips as fresh as recesses refute it.

IDEA 3
NAME: Fumigation cage for aromatics
MECHANISM: Resin or herbs on a small ember went in through the largest hole; then it sat on a smaller-holed face, ember over that hole. Knobs lift it to admit air while upper holes vent smoke, and turning it to another face changes intake and smoulder rate, so holes needed only to differ within a piece; rings are ornament. The thin shell heats fast, knobs give cooler grips, use causes no wear, and the wax specimen is residue. Domestic, bath, theatre and funerary fumigation fits the mixed contexts, a regional form of a common rite, unnamed in texts.
VALUE: It explains knobs as stand-offs, the perforated hollow and the wax specimen together, which symbolic and instrument readings do not. Clean interiors on 10+ pieces, with no soot, charred resin or heat tint and no resin markers by GC-MS, refute it.

IDEA 4
NAME: Knob-footed twelve-face divination lot
MECHANISM: It was a bronze lot for private divination: the person consulting it threw it onto a cloth or table, it came to rest on the five knobs of one face, and the horizontal face opposite was read. Each face is told apart without letters by its hole (size class, ringed or not) and by where it sits relative to the larger unringed pair, which the specialists read as the casting-core axis and which serves as the pole. Because each piece carries its own code, holes differ within every object while no size scheme or module is shared between objects. The twelve outcomes stand for the twelve parts of the heavens: a 4th-century silver-coated lead dodecahedron from Geneva carries the twelve zodiac names in Latin, one per face, and is interpreted as a divination die, and Platonist tradition made the dodecahedron the figure of the whole cosmos (Timaeus 55c). The knobs are feet: only their tips touch the cloth, so the face to read is unambiguous and the ringed rims are spared. Owners were households and individuals across civil and military society, who treated the piece as a valuable; hence rich graves of both sexes, a coin hoard, shrine deposits, and the repair on the Kortessem piece. It was a regional product of the Gaulish, Rhenish and British bronze trade, which soldiers and traders carried to the Danube legionary bases; the Mediterranean cast lots with other devices (the oak lots of Praeneste, the 2nd-century knucklebone oracles of Asia Minor) and already knew both hollow lost-wax casting and the dodecahedron, so the map reflects a regional device, not a missing technique, and the type appears c. 150-200 while its 4th-century end coincides with imperial laws against divination (356-357) and pagan cult (391-392).
VALUE: It is the only explanation that turns four hard facts into one function: holes that vary within each object, no shared scheme, no inscriptions, and the fixed twelve-face template. It also rests on a dated regional parallel (Geneva) instead of the misread Germanic lots. Still unexplained: why only the north-west used this device (shown only by the distribution and the single Geneva die), the start c. 150-200, any role for the knobs beyond feet, and the Arloff icosahedron with holes in only two faces. Decisive test: on 10 or more pieces with surviving original surface, compare all 20 knob tips with their bases, plus the hole rims and interior, by stereo microscope or 3D scan. Throwing predicts rounding on every tip, roughly evenly, with clean rims and interiors; tips as sharp as their bases, or wear limited to one face's five knobs or to particular rims, refute it.

IDEA 5
NAME: Cosmic emblem, sometimes on a staff
MECHANISM: It was a devotional image of the cosmos, Plato's fifth figure that the god used "for the whole" (Timaeus 55c), owned by households and individuals of the north-western provinces rather than by priests. It was kept at home or in shrines, and sometimes carried on a short rod passed through the unringed core-axis pair; at Krefeld-Gellep a bone object, possibly a handle, lay beside the 4th-century piece in a rich woman's grave. It went with the dead, to sanctuaries (Lydney, Pfofeld) and into hoards. The form mattered, not a mechanism: the hollow knobbed icosahedron from Arloff has holes in only two opposite faces, so face holes were optional; rings and knobs are the ordinary decoration of provincial bronze; and hole sizes vary because nothing depended on them. It was rarely handled and never put to work, so it stayed largely unworn, and it needed no letters because the shape carried the meaning. Its region is that of a provincial taste in cult objects and a regional workshop network; the proposed Druid-Pythagorean root is weak, because the Druids were suppressed under Tiberius and Claudius, 150-300 years before the objects, and its end coincides with the closing of pagan cult in 391-392.
VALUE: It accounts for the low wear, the rarity, the valuable and sacred contexts and the two-holed icosahedron better than the lot does, and it drops the reviewed failures of the priest's-sceptre version (priestly regalia, sprig crowns, knobs as anti-roll stops). But it leaves the hard fact of hole variation within each object, and the three preset hole classes at Jublains, as unexplained ornament, and its regional cause is unsupported. On the same test it predicts unworn knob tips, or wear only on the five knobs of one display face, plus abrasion or mineral-preserved wood or bone inside the unringed pair where it was mounted on a staff; evenly rounded tips on all 20 knobs refute it.

IDEA 6
NAME: Native priest's radiate sceptre
MECHANISM: A short rod (as at Gellep) passed through the unringed core openings, so the ten ringed holes formed two radiating five-fold crowns, each holding a sacred-plant sprig; stems differed, hence varied holes and no shared scheme. Never grounded, it stayed unworn; knobs stopped it rolling on altars. Native priesthoods (Gaulish gutuatri; Romano-British priestly crowns and sceptres, known from finds, not images) existed only in the Celtic north-west and ended with the Theodosian bans.
VALUE: It makes the unringed axis, the five-fold form and graded holes necessary and derives art's silence. Ringed rims on 10+ pieces without stem scratches or plant residue refute it.

