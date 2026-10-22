# Task: adversarial review - test each explanation against the evidence

QUESTION: What were the Roman dodecahedra? These are small hollow bronze objects with twelve pentagonal faces, a round hole of differing diameter in each face and knobs at the corners, found in the north-western provinces of the Roman Empire and dated to roughly the 2nd-4th centuries AD; no ancient text mentions them. Find the explanation of what they were and how they were used that best accounts for ALL the physical and archaeological evidence, and say how it can be tested.

Below are 7 explanations, mixed and unlabelled. Your job is to be the toughest competent outside specialist. You do
NOT fix or improve the explanations; you test each one against the evidence and rank its defects.

You have tools: WebSearch (WebFetch does not resolve domains here; use search-result excerpts) and Bash with python3.
Work only in `/home/user/SomeRepository/engine/runs/dodeca/audit_1/`: read no other files in the repository, do not modify other files, do not commit.

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

THE 7 EXPLANATIONS:
IDEA 1
NAME: Platonic cosmic receptacle
MECHANISM: The dodecahedron, the Platonic solid tied to the cosmos, was made in Gaul and Britain as a material "receptacle" in Pythagorean-Platonic spirit, a philosophy Druids were said to admire. The twelve pentagonal faces embody the universe; holes and knobs are decorative or ritual variation, hence no standard sizes. A rod-shaped bone object beside the Gellep grave specimen suggests staff mounting, like a scepter of spiritual authority. Absence from Italy follows from its Celtic provincial origin.
VALUE: It explains the geography, lack of wear, lack of standardisation and silence of texts. Proponents propose better-contexted finds and evidence of mounting.

IDEA 2
NAME: Hand-tuned bronze vessel whistle
MECHANISM: Each piece was a Gallo-British edge-blown vessel flute: the player blew across one larger unringed hole, its opposite twin was a thumb vent, and the ring-marked holes were finger or wax stops. Pitch depends on open hole area against cavity volume, so graded holes give a fuller scale, and continuously varying bodies forced individual tuning, which rules out any shared hole standard. Knobs let it be held and set down without blocking holes. Wax, used to join and tune ancient pan-pipes, explains the German residue; lips and fingers leave bronze unworn; and the Kortessem repair restores airtightness.
VALUE: It turns differing holes, continuous sizes, the unringed pair and the wax trace into requirements. Sound the intact Norton Disney piece with an artificial-mouth air jet across an unringed rim, other holes film-sealed: if no stable tone results, it is refuted.

IDEA 3
NAME: Founder's hollow-casting masterpiece
MECHANISM: Casting a closed polyhedron hollow with millimetre walls is among the hardest lost-wax tasks; the dodecahedron was a provincial founder's proof piece, kept or given to patrons. Every face is holed because the clay core must be pinned and raked out: the larger, unringed, sometimes oval opposite pair is the main core-pin axis, filed open, while the other ten got finishing rings. Corner knobs are feeders filling thin junctions; each founder set his own core and wax, so sizes vary. Display means no wear or lettering; graves, hoards and the Kortessem repair show value; the range maps a north-western casting tradition.
VALUE: It explains why every face is holed, why one pair is larger and unringed, the knobs and the thin walls, all arbitrary in use-based readings. Test: radiograph existing pieces; if core-pin, filing and porosity traces do not concentrate on the larger unringed axis, it is refuted.

IDEA 4
NAME: Travelling founders' trade sample
MECHANISM: Itinerant founders, casting on site for towns, villas and forts, carried a dodecahedron as proof they could cast closed, thin-walled hollows. Its form records casting: holes pin and empty the core, the larger unringed pair marks the main core axis, ringed holes display finishing, knobs fed thin corners; each team cast its own, so sizes vary. Seldom handled, samples show little wear and needed no words; they were lost at work sites, rivers, wells and pits, sold on into graves and hoards, and taken beyond the frontier by hired teams. Fixed Mediterranean workshops needed none.
VALUE: It explains the civil majority, military minority, river and pit losses and Slovak finds as one trade's itinerary, not a cult or army. Test: pXRF and core-clay analysis should show a few alloy-clay groups each spread over hundreds of kilometres; local matches at each findspot refute it.

IDEA 5
NAME: Gallo-Roman divination and magic
MECHANISM: A private, non-official object of sorcery or fortune-telling, absent from literature and art because unofficial. Twelve faces echo zodiac or twelve-oracle systems like the Sortes Sangallenses and the zodiac-named Geneva die. In the Spindle-of-Necessity version, thread was wound across knobs and through holes to cast or read fate. Breakage and repair of finds such as Kortessem may mark ritual destruction.
VALUE: It explains absence from texts, lack of wear and the Celtic-area distribution. Its test is thread or fibre traces on knobs and holes, and deposition patterns showing deliberate burial or breakage.

IDEA 6
NAME: Fumigation cage for aromatics
MECHANISM: Resin or herbs on a small ember went in through the largest hole; then it sat on a smaller-holed face, ember over that hole. Knobs lift it to admit air while upper holes vent smoke, and turning it to another face changes intake and smoulder rate, so holes needed only to differ within a piece; rings are ornament. The thin shell heats fast, knobs give cooler grips, use causes no wear, and the wax specimen is residue. Domestic, bath, theatre and funerary fumigation fits the mixed contexts, a regional form of a common rite, unnamed in texts.
VALUE: It explains knobs as stand-offs, the perforated hollow and the wax specimen together, which symbolic and instrument readings do not. Clean interiors on 10+ pieces, with no soot, charred resin or heat tint and no resin markers by GC-MS, refute it.

IDEA 7
NAME: Hole-signature membership token
MECHANISM: Each was a recognition token of a non-official Gallo-British association, its hole diameters a personal signature checked against a counterpart such as a pegged wooden gauge. A signature must vary within each object and never repeat between objects, exactly the observed pattern; the larger unringed opposite pair fixes the reference axis so the ten ringed sizes are read in order. Knobs and rings make imitation costly; shown rather than used, it stays unworn and uninscribed, while unofficial membership explains textual silence and spread from Gaul to Britain and beyond the frontier. Tokens followed owners into graves, hoards and rivers.
VALUE: It makes the missing shared size scheme a design requirement and fits extra-imperial spread and valued deposition. Measure hole roundness on existing pieces: if scatter within single holes equals the steps between holes on one object, no signature exists and it is refuted.

