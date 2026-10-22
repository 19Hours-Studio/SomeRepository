# Task: the desk test - do the hole sizes of Roman dodecahedra fall into classes, or form a continuum?

Context: the leading explanation of the Gallo-Roman bronze dodecahedra (about 130 hollow pieces, 12 pentagonal faces
each with a round hole, knobs at the 20 corners, north-western provinces, 2nd-4th c. AD) is a divination lot whose
faces are told apart by hole-size CLASS. On the one piece with a published per-hole table (Jublains, Sparavigna 2012,
arXiv 1204.6497) the ten ringed holes fall into three tight classes (about 11, 16.5 and 21.5 mm) and the five faces
around each of the two unringed pole holes carry the same set. The rival explanations predict no classes (random or
continuous sizes): staff mount, cosmic emblem, fumigation cage, candle shade. One object decides nothing; this task
tests the pattern on as many objects as the published record allows.

You are a careful quantitative archaeologist. Tools: WebSearch (WebFetch and curl do NOT reach any host in this
environment; work from search-result excerpts and run many targeted searches) and Bash with python3. Work only in
`/home/user/SomeRepository/engine/runs/dodeca/tests/holes/`: read no other files in the repository, write files only
there, do not commit.

Steps:
1. COLLECT: find every published set of hole diameters for individual dodecahedra (all 12 holes, or as many as are
   given), with object name, museum, overall size and weight if given, and the exact source of each number. Search in
   English, French, German and Dutch (e.g. "dodecaedre gallo-romain diametre des trous", "Pentagondodekaeder Lochdurchmesser",
   "dodecaeder gaten diameter"), arXiv (Sparavigna 2012, 2014), Guggenberger 2013 and Guggenberger & Leach 2025, Nouwen
   1993, museum catalogues (Tongeren, Bonn, Trier, Corbridge, Newhall/Derby, Norton Disney, Jublains, Geneva), and
   enthusiast measurement pages. NEVER invent or estimate a diameter; mark anything read from a photo or second-hand.
2. ANALYSE in python, per object with at least 8 measured holes: (a) are the sizes clustered into classes? Use the
   largest-gap ratio and a gap statistic against two null models simulated 100,000 times: uniform sizes over the
   object's range, and sizes cut freehand with a realistic scatter (say 0.5-1 mm) around a smooth continuum; give the
   probability of the observed clustering under each null. (b) Do the two pole hemispheres carry the same multiset?
   (c) Are opposite holes equal, systematically unequal, or random? Report n honestly; with few objects say what can
   and cannot be concluded.
3. PREDICTIONS: for each explanation (lot with size classes; staff or emblem; fumigation; candle), state what it
   predicts for (a)-(c) and whether the data support, contradict or cannot decide.

Final answer (text only), at most 900 words:
=== HOLES ===
DATA: one line per object: name | museum/source | n holes measured | the diameters (mm) | notes
ANALYSIS: the results of (a)-(c) per object and pooled, with probabilities under both nulls
VERDICT: does the record show classes, a continuum, or is it undecidable, and how strongly
PREDICTIONS: one line per explanation: supported / contradicted / undecided, and why
NEXT: the 3 objects or publications whose full tables would decide it
