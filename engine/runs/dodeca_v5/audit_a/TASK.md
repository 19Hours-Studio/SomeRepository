# Task: adversarial review - test each explanation against the evidence

QUESTION: What were the Roman dodecahedra? These are small hollow bronze objects with twelve pentagonal faces, a round hole of differing diameter in each face and knobs at the corners, found in the north-western provinces of the Roman Empire and dated to roughly the 2nd-4th centuries AD; no ancient text mentions them. Find the explanation of what they were and how they were used that best accounts for ALL the physical and archaeological evidence, and say how it can be tested.

Below are 8 explanations, mixed and unlabelled. Your job is to be the toughest competent outside specialist. You do
NOT fix or improve the explanations; you test each one against the evidence and rank its defects.

You have tools: WebSearch (WebFetch does not resolve domains here; use search-result excerpts) and Bash with python3.
Work only in `/home/user/SomeRepository/engine/runs/dodeca_v5/audit_a/`: read no other files in the repository, do not modify other files, do not commit.

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
KNOWN | <yes / partly / no: was essentially this explanation proposed before?> | <who proposed it, with source>
NEW FACT | <any hard fact you found that the material did not contain> | <source> (optional, any number)
(same for the other explanations, in the same order as below)

THE 8 EXPLANATIONS:
IDEA 1
NAME: Platonic cosmic receptacle
MECHANISM: The dodecahedron, the Platonic solid tied to the cosmos, was made in Gaul and Britain as a material "receptacle" in Pythagorean-Platonic spirit, a philosophy Druids were said to admire. The twelve pentagonal faces embody the universe; holes and knobs are decorative or ritual variation, hence no standard sizes. A rod-shaped bone object beside the Gellep grave specimen suggests staff mounting, like a scepter of spiritual authority. Absence from Italy follows from its Celtic provincial origin.
VALUE: It explains the geography, lack of wear, lack of standardisation and silence of texts. Proponents propose better-contexted finds and evidence of mounting.

IDEA 2
NAME: Apotropaic household display object
MECHANISM: The piece stood on three knobs in a household or bath shrine. Its triple-ringed holes worked as "eyes" averting harm, and its twelve faces stood for the cosmos. Light passing through the holes mattered more than their exact sizes, so hole sizes are free variation set by the wax modeller. When a house or person ended, the object was retired, sometimes broken or repaired, into wells, rivers, pits, graves and hoards.
VALUE: It explains the random hole sizes, the absence of wear and the mixed deposition, which tool readings cannot. Refutation: per-object tables of the 12 diameters (Guggenberger 1-134) show a consistent ratio scheme, or wear facets concentrate on three-knob triads rather than being absent.

IDEA 3
NAME: Cord-wound divinatory frame
MECHANISM: A private diviner wound wool or linen cord around the knobs and through chosen holes, imitating the Spindle of Necessity or casting lots. The different hole sizes give the twelve faces distinguishable "stations" without inscriptions. The knobs anchor the cord. Use was occasional, so wear is slight, and breakage marks deliberate retirement, as perhaps at Kortessem. Unofficial practice explains the silence of texts and images and the Gallic distribution.
VALUE: It explains knobs, unmarked unequal holes, low wear and mixed civil contexts better than military or tool readings, which fail Facts 11 and 14. Refutation: knob roots and hole rims on Norton Disney and about 15 other pieces show no cord-groove polish and no fibre traces under SEM and FTIR.

IDEA 4
NAME: Farmer's sowing-date instrument
MECHANISM: Aimed at the sun and steadied on its knobs, opposite holes of different diameters act as apertures whose sunlight geometry marks the equinoxes and the autumn window for sowing winter wheat. Different hole pairs correspond to different dates or latitudes, which is why dimensions vary. It needed no markings, being a calendar-by-light.
VALUE: It explains twelve differently sized holes, northern farming provinces and low wear (used a few days a year). Wagemans tested a bronze copy over several years at different latitudes.

IDEA 5
NAME: Unwritten twelve-face lot
MECHANISM: The object was a lot for drawing omens, cast by hand onto soft ground or cloth. Each face was identified by its hole size instead of by numbers. Because the holes had to differ, variation within each object is required, and the lack of any shared scheme between objects follows from each maker setting their own sizes. The two large unringed holes marked the "special" outcomes, and the knobs made the object come to rest on a face. Occasional private use explains the lack of wear and the silence of the texts.
VALUE: Unlike other divination ideas, it makes the absence of inscriptions and the varied holes necessary rather than awkward. Test: check knob tips under a microscope for even, all-round micro-flattening and compare it with the unused Norton Disney piece. If the corpus shows no such wear, the idea is refuted.

IDEA 6
NAME: Coincidence rangefinder
MECHANISM: Looking through a face's small hole at a standard-sized object (a man, a standard, a pole) until it exactly fills the large opposite hole gives distance by proportion. The faces form pairs of differing diameters, giving a range of calibrated distances; knobs let it rest flat or be gripped. Finds at forts link it to military engineering or surveying, like the dioptra.
VALUE: It explains the opposite-hole size contrast and finds in military camps. Sparavigna's test is measuring hole-pair ratios against plausible target sizes and ranges on real objects.

IDEA 7
NAME: Gallo-British elite insignia
MECHANISM: The object was a badge of standing within a north-western provincial network, comparable to crossbow brooches as rank markers. It was held or shown on occasions, not used as a tool. A fixed template (twelve faces, knobs, ringed holes) carried the recognisable identity, while size and finish varied with the owner's means, which explains the weights from 35 g to over 1 kg. It was buried with men and women, hoarded, or broken on transfer, as at Kortessem. Like other informal status goods, it was too local and unofficial to appear in texts or art.
VALUE: It accounts for the confined distribution, the few examples traded beyond the frontier, the varied contexts and the absence of wear better than religious or tool readings do. Refutation test: tabulate object size against findspot status (villa or rich grave versus poor rural site) in Guggenberger's list. If there is no correlation, the idea fails.

IDEA 8
NAME: Thin-wall casting masterpiece
MECHANISM: The object was a provincial bronzesmith's proof of mastery: a hollow geometric shell with a wall of about 0.6–1.6 mm, cast around a clay core. Each face hole held a support for the core and later let the core be broken out. That is why every face has a hole, why hole sizes are freehand and unstandardised, and why the interiors are rough. The knobs are vents or feeders at the corners, which are the last points to fill, later shaped into a decorative finish. The engraved rings and lack of wear show display rather than use. Its value as a valued keepsake explains its presence in graves, hoards and rich houses.
VALUE: It explains the holes in all twelve faces, the varying diameters, the rough interiors, the thin walls that scale with size, and the absence of wear, without needing any user function. Refutation test: CT-scan pieces in Bonn or Tongeren. If the holes were cut through an originally closed shell (tool marks on the hole walls) and there are no core residues or chapter-pin traces, the idea fails.

