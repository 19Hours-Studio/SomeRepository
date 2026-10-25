# Task: adversarial review - test each explanation against the evidence

QUESTION: What were the Roman dodecahedra? These are small hollow bronze objects with twelve pentagonal faces, a round hole of differing diameter in each face and knobs at the corners, found in the north-western provinces of the Roman Empire and dated to roughly the 2nd-4th centuries AD; no ancient text mentions them. Find the explanation of what they were and how they were used that best accounts for ALL the physical and archaeological evidence, and say how it can be tested.

Below are 7 explanations, mixed and unlabelled. Your job is to be the toughest competent outside specialist. You do
NOT fix or improve the explanations; you test each one against the evidence and rank its defects.

You have tools: WebSearch (WebFetch does not resolve domains here; use search-result excerpts) and Bash with python3.
Work only in `/home/user/SomeRepository/engine/runs/vs_dodeca_v5/compare/r1/`: read no other files in the repository, do not modify other files, do not commit.

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
FACT 31: A 4th-c. silvered-lead dodecahedron from Saint-Pierre Cathedral, Geneva (excavated 1982), carries the Latin zodiac names on its 12 faces, so FACT 19 holds only for the hollow bronze type | NEW from audit_a, check before relying on it | ge.ch/actualite/objets-archeologiques-episode1-3-11-2021
FACT 32: A Roman icosahedron from Arloff, long misclassified as a dodecahedron, is in the LVR-LandesMuseum Bonn; the polyhedral family is wider than the dodecahedron | NEW from audit_a, check before relying on it | en.wikipedia.org/wiki/Roman_dodecahedron
FACT 33: The Gellep bone rod (~15 cm × 3 cm) was too decayed to recover, so the sceptre link cannot be re-examined | NEW from audit_a, check before relying on it | livescience (above)
FACT 34: A knobbed regular dodecahedron always rests on 5 knobs around one face, never on 3 (convex-hull check) | NEW from audit_a, check before relying on it | own python calculation
FACT 35: calc.py, cited as the source of FACT 7, is not in the audit folder; recomputing gives a wall of 0.60-1.58 mm before subtracting the holes, which confirms the range | NEW from audit_a, check before relying on it | own recalculation
FACT 36: **Tongeren** (opposite pairs 10.6/13.0, 13.8/14.0, 25.2/27.0, 23.0/26.3, 15.6/17.8, 20.3/20.5 mm). Opposite pairs differ by 0.2–3.3 mm, 10.1 mm in total, against 40.2 mm for chance pairing. Exact p = 0.0005. | NEW from reality, check before relying on it | [wingarden.de](http://www.wingarden.de/wing/dodekaeder.html); holes.py
FACT 37: **Sparavigna's 12-hole table** (10.5–22 mm plus two ovals of about 26×21.5 mm, pairs as she published them). Opposite pairs differ by 13.0 mm in total, against 35.2 mm for chance. Exact p = 0.010, and the result holds whichever oval axis is used. Four of the six pairs differ by 1 mm or less. The two pairs that don't match, 10.5/17 and 15.5/11.5, would also match if two face labels were swapped, so this may be a labelling slip. Combining both objects gives p ≈ 7×10⁻⁵. | NEW from reality, check before relying on it | [arxiv 1204.6497](https://arxiv.org/pdf/1204.6497), [1206.0946](https://www.arxiv.org/pdf/1206.0946); holes.py
FACT 38: Where this table comes from is unclear. The same numbers are credited to Jublains (Sparavigna), to a 59 mm, 81 g piece that is possibly from Avenches ([nunc.ch](https://nunc.ch/en/gallo-roman-dodecahedron-twelve-faces-zero-answers/)), and to Krefeld-Gellep. FACT 3's "Newhall" data and FACT 6's Newhall weight (81 g) are probably this same object counted twice. | NEW from reality, check before relying on it | search excerpts above
FACT 39: Two measurements of the same hole on a Carnuntum piece differ by 0.3 mm (16.0 vs 16.3 mm), which gives a sense of measurement error. This is far smaller than the gap between paired holes and random pairing. Greiner's re-measurement found one opposite pair with zero difference, which rules out the rangefinder reading for that pair. | NEW from reality, check before relying on it | [liberalter.wordpress.com](https://liberalter.wordpress.com/2025/09/02/wozu-diese-romischen-dodecahedra/) (blog, secondary)
FACT 40: In Roman Britain tallow candles were the normal light and oil lamps were concentrated in the 1st century, at Colchester and London | NEW from audit_final, check before relying on it | cim-web.adlibhosting.com/ais6/Details/collect/181098
FACT 41: The knob balls are not perfectly regular, which suggests they were made without a mould | NEW from audit_final, check before relying on it | en.wikipedia.org/wiki/Roman_dodecahedron
FACT 42: The Geneva dodecahedron (silvered lead, zodiac names) was found in 1982 near Saint-Pierre Cathedral; FACT 31 is confirmed apart from the date | NEW from audit_final, check before relying on it | grandcurtius.be/en/museums-collections/archaeology/dodecahedron
FACT 43: The Arloff icosahedron in Bonn is confirmed, and dated to the 3rd century | NEW from audit_final, check before relying on it | en.wikipedia.org/wiki/Roman_dodecahedron; thedebrief.org

For each explanation:
1. Go through the hard facts. Which does it CONTRADICT (FATAL), which does it need an extra unsupported assumption
   for (MAJOR), which does it leave unexplained although they are distinctive (MAJOR if the feature is distinctive,
   MINOR otherwise)?
2. Specificity: does it explain the distinctive features themselves, or would it fit any object of that period
   ("ritual", "status", "decoration" without a mechanism for the features is a MAJOR defect)?
3. Is the decisive test it proposes actually able to refute it, is it feasible with existing material, and what
   result would refute it?
Facts marked NEW were found by earlier checks in this run and are not yet verified: do not count them toward FIT,
and do not base a FATAL or MAJOR defect on a NEW fact alone unless you have verified it yourself (its source and,
for measurements, which object and which hole, face or item each number belongs to).
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

THE 7 EXPLANATIONS:
IDEA 1
NAME: Rangefinder, gauge or knitting tool
MECHANISM: This covers the practical-tool ideas. Sighting through opposite holes, which differ in size, would give a distance to a target of known size, as with Sparavigna's vexillum example (ranges of about 15–200 m). Other versions have it as a gauge for pipes or coins, or a frame for knitting glove fingers on the knobs.
VALUE: This is the only family of ideas that gives the hole-size differences a measuring use. However, no standard sizes, no wear, no textile residue and the votive find contexts all argue against it. Decisive test: microscope inspection of knob and hole edges for thread-groove or abrasion wear. Their absence, which current reports already suggest, rules these ideas out.

IDEA 2
NAME: Gallo-Celtic cult object, cosmological or divinatory
MECHANISM: Each dodecahedron was a valued religious object made locally in the Celtic-heritage north-west. It probably stood for the cosmos: in Plato's *Timaeus* the dodecahedron is the shape of the universe, and Pythagorean ideas reached Gaul by way of the Druids (Leach & Guggenberger 2025). It was used in rites, possibly divination, which may have involved thread or sighting through the holes. It may also have been carried on a staff, since in the 1966 Gellep woman's grave a rod-shaped bone lay beside one. The holes all differ in size, so each face can be told apart, which a divination object needs and a measuring tool cannot have. The knobs let it stand on any face or sit on a mount, and they also prevent it rolling like a die. Lost-wax casting means every piece is a one-off with no standard size, which fits a ritual object rather than a measure. No text mentions them because the cult was local and passed on by word of mouth, as Druidic lore was.
VALUE: This idea alone accounts for the narrow distribution (about 70% Gaul and Germany, about 20% Britain, almost none in Italy or the East), the lack of wear, the soft alloy, and the careful deposits in graves, coin hoards, rivers and pits, which are classic votive patterns. Cheap test: a blind use-wear and residue survey (microscope, FTIR/GC-MS of the interior and hole rims) on about 20 museum pieces. The prediction is no tool wear, but possible traces of wax, textile or organic offerings, with deposition rates in graves, hoards and rivers well above those for ordinary bronze tools at the same sites.

IDEA 3
NAME: Bronzesmith's hollow-casting display piece
MECHANISM: The dodecahedron was a showpiece from regional north-western workshops that demonstrated difficult thin-wall hollow casting. No guild "masterpiece" institution is needed for this, and there is no Roman evidence for one. The core was held and later removed through the face openings, set along the six axes, so opposite openings came out matched in size. Finishing (triple rings, one plain and sometimes oval pair) varied from workshop to workshop. The knobs were cast-on ornament and feet, not vents. Nobody used it for anything, so it shows no wear. People kept it as a valued item and placed it in graves and hoards, and its distribution follows the workshop tradition.
VALUE: It explains the pierced faces, the axis matching, the thin walls and the lack of wear without assuming any use. It cannot explain why one pair is consistently left unringed, made larger and sometimes oval across the corpus, or the rod beside the Gellep piece. The same rim test refutes it if the unringed pair does show fitting marks or wear that the ringed holes lack.

IDEA 4
NAME: Masterpiece or prestige display object
MECHANISM: Bronzesmiths made it to show off their skill (Rüdiger Schwarz's idea): a hollow, accurately faceted lost-wax casting with graded holes and knobs. Owners kept it as a status piece or heirloom.
VALUE: This explains why there is no wear, no standard size and no text. It also explains why owners valued them enough to bury them in graves and hoards. Against it: a demonstration of casting skill should not need a lead-heavy alloy (Norton Disney is about 26% lead, which is worse for casting) or the same 12-hole layout repeated across about 134 pieces. Test: XRF and CT surveys of casting quality across the corpus. A masterpiece hypothesis predicts consistently high quality, while a cult object allows crude examples.

IDEA 5
NAME: Seasonal sighting calendar for sowing
MECHANISM: You look through a pair of opposite holes at the sun or a star such as the Pleiades. The day the sun's noon height (or a star's rising) just fills the aperture sets the date to sow winter grain. Because the opposite holes differ in size, each pair gives a different angle and so a different date. Pieces of different sizes would then be versions made for different latitudes.
VALUE: This explains why the holes differ and why opposite faces are paired. It also explains a north-western, agricultural spread without needing written instructions. Decisive test: compute each pair's viewing angle (arctan of the hole-diameter difference over the face-to-face distance) for catalogued specimens and check it against the latitude of each find spot. No correlation would falsify it, and the lack of standard sizes already weighs against it.

IDEA 6
NAME: Staff-mounted provincial symbolic bronze head
MECHANISM: The dodecahedron was a prestige object with symbolic meaning, made in regional bronze workshops of Gaul, the Rhineland and Britain. It was a lost-wax shell about 1 mm thick cast around a clay core. Every face is pierced because the core had to be supported during casting and broken out afterwards. The holes were then finished to a six-axis plan. Opposite holes were sized alike, very clearly on Tongeren and weakly on the second published table. Ten holes were ringed. One larger, unringed and sometimes oval opposite pair formed a through-axis, by which the head could be fitted onto a rod or handle. The bone object (about 15 × 3 cm) found right beside the Gellep piece, in the grave of a wealthy woman from about AD 350, suggests this. When it was not mounted, the corner knobs let it stand on any face as a finished ornament. Its meaning was probably cosmological or astral: the 4th-century Geneva lead dodecahedron carries the twelve zodiac names, so in this region a twelve-face solid could stand for the twelve signs. Well-off civilians of both sexes owned it, and some soldiers did too. They used it rarely or in ceremonies, which is why wear is slight. They valued it enough to repair it (Kortessem) and to put it in rich graves and hoards. It belonged to a north-western provincial tradition, carried by people moving to the Danube forts and across the river. That explains why it is missing from the Mediterranean and why no Greek or Latin author describes it.
VALUE: It is the only reading that accounts at once for: - a hole in every face; - holes that vary in size but match axis by axis; - the special unringed opposite pair found across the corpus; - thin, unworn shells; - the repaired, grave and hoard contexts.

IDEA 7
NAME: Unwritten twelve-face lot
MECHANISM: The object was a lot for drawing omens, cast by hand onto soft ground or cloth. Each face was identified by its hole size instead of by numbers. Because the holes had to differ, variation within each object is required, and the lack of any shared scheme between objects follows from each maker setting their own sizes. The two large unringed holes marked the "special" outcomes, and the knobs made the object come to rest on a face. Occasional private use explains the lack of wear and the silence of the texts.
VALUE: Unlike other divination ideas, it makes the absence of inscriptions and the varied holes necessary rather than awkward. Test: check knob tips under a microscope for even, all-round micro-flattening and compare it with the unused Norton Disney piece. If the corpus shows no such wear, the idea is refuted.

