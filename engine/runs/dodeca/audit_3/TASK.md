# Task: adversarial review - test each explanation against the evidence

QUESTION: What were the Roman dodecahedra? These are small hollow bronze objects with twelve pentagonal faces, a round hole of differing diameter in each face and knobs at the corners, found in the north-western provinces of the Roman Empire and dated to roughly the 2nd-4th centuries AD; no ancient text mentions them. Find the explanation of what they were and how they were used that best accounts for ALL the physical and archaeological evidence, and say how it can be tested.

Below are 6 explanations, mixed and unlabelled. Your job is to be the toughest competent outside specialist. You do
NOT fix or improve the explanations; you test each one against the evidence and rank its defects.

You have tools: WebSearch (WebFetch does not resolve domains here; use search-result excerpts) and Bash with python3.
Work only in `/home/user/SomeRepository/engine/runs/dodeca/audit_3/`: read no other files in the repository, do not modify other files, do not commit.

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
NAME: Festival ember carrier
MECHANISM: Yearly, in the Celtic custom (recorded later in Ireland) of quenching hearths and rekindling them from a sanctuary fire, each household carried a live coal home in it. The coal entered an unringed core opening; turning the shell set a larger or smaller ringed vent (rings mark designed vents) windward to keep it glowing, knobs giving cooler grips. Coligny's Samonios month attests this festival calendar in 2nd-century Gaul; Christianisation ended it.
VALUE: It derives household contexts, annual (hence unworn) use and the Celtic-calendar map from one rite. Interiors of 10+ pieces without heat tint, soot or ash refute it.

IDEA 2
NAME: Staff finial on tapering shaft
MECHANISM: A light insignia head was slid onto a staff through the larger unringed opposite pair and wedged where the taper met that pair's smaller hole, so opposite pairs may differ widely. Ringed holes faced outward as decorated windows; knobs were ornamental terminals shielding the head when grounded. Each head fitted its own staff, so no size scheme was needed. Carried occasionally, it stayed unworn, followed its holder into graves (the Gellep rod), hoards or rivers, and as an unofficial regional badge escaped texts and art.
VALUE: It makes the unringed axis and unequal opposite pairs necessary, which symbolic and instrument readings leave unexplained. Under CT and microscopy, type-2a unringed pairs showing no more rim abrasion, organic traces or staining than ringed holes, or admitting no single tapering rod, refute it.

IDEA 3
NAME: Coursing hunter's personal whistle
MECHANISM: Blown across an unringed oval, all other holes open, it gives one note fixed by cavity volume and total hole area, so no hole is stopped by hand. Varying bodies and holes give each piece its own note for its owner's hounds to learn; a shared scheme would defeat that. Arrian (Cynegeticus, 2nd century) calls coursing with hounds a Celtic sport, unlike Mediterranean net-hunting, hence north-western villas and forts until c. 400.
VALUE: It makes continuous size spread and no shared hole scheme necessary. Unringed rims on 10+ pieces as blunt as ringed ones, with no sharp blowing edge, refute it.

IDEA 4
NAME: Sanctuary-theatre chorus pitch-giver
MECHANISM: At festivals in Gaul's and Britain's sanctuary theatres, a chorus leader gave the opening note by blowing across an unringed oval, other holes open. After casting, the maker reamed ringed holes wider until the piece gave its owner's note, so holes differ within every piece and follow no shared scheme; rings were layout lines. Choristers kept them at home, hence settlement finds; the temple closures of 391-392 ended them.
VALUE: It explains within-piece differences and the missing scheme as tuning, tied to a regional building type. Ringed-hole walls on 10+ pieces without post-casting reaming marks refute it.

IDEA 5
NAME: Touch-coded casting lot
MECHANISM: Tossed onto cloth, it tumbles on its knobs and settles with one face up. That face is read by its hole (size, ringed or not; the large unringed pair a distinct outcome), legible by eye or finger, so no letters were needed, and since each owner knew their own piece, neither a shared scheme nor fairness mattered. A light shell landing on cloth wears little. It belongs to north-western lot-casting (Tacitus describes Germanic lots thrown onto a white cloth), not Mediterranean dice culture, fitting distribution, civil and grave contexts and textual silence.
VALUE: It explains why holes differ within each object yet share no scheme between objects, and why nothing is inscribed. On 10+ pieces, microscope knob tips against protected recesses: repeated tumbling polishes tips, so tips as fresh as recesses refute it.

IDEA 6
NAME: Bright-or-dark day-luck lot
MECHANISM: Thrown on pale cloth, it rests on knobs, one opposite pair vertical; the reader looks down through the top hole. A larger lower hole shows only bright cloth, "good"; a smaller one, a dark interior ring, "not good"; near-equal pairs void the throw, so no shared scheme is needed. It extended to single decisions the good/not-good (MAT/ANM) day-marking of Gaul's 2nd-century Coligny calendar, used only in Celtic-calendar lands until Christian reckoning.
VALUE: It makes variable opposite pairs and missing letters requirements, and ties the map to Gaulish time-reckoning. Measured opposite pairs (Jublains, Guggenberger's list) mostly equal within 1 mm refute it.

