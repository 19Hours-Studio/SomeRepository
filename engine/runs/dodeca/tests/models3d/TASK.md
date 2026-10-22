# Task: inventory of published 3D models and scans of Roman dodecahedra

Context: the leading explanations of the Gallo-Roman bronze dodecahedra (about 130 hollow pieces, 12 pentagonal faces
each with a round hole, knobs at the 20 corners) can be tested on detailed 3D models: all 12 hole diameters per piece
(do they fall into size classes?) and the shape of the 20 knob tips against their bases (are they evenly rounded by
throwing, worn on one face only, or fresh?). Published 3D models exist (museum photogrammetry and laser scans on
Sketchfab and elsewhere, university scans such as the Norton Disney piece, research datasets).

You are a careful researcher. Tools: WebSearch (WebFetch and curl do NOT reach any host in this environment; work
from search-result excerpts and run many targeted searches, e.g. "dodecahedron sketchfab roman", "dodecaedre
gallo-romain 3D", "Pentagondodekaeder 3D Modell Museum", "Roman dodecahedron photogrammetry", "Norton Disney
dodecahedron 3D scan", museum names: Tongeren, Bonn LVR, Trier, Corbridge, British Museum, Grand Curtius, Jublains,
Rijksmuseum van Oudheden, Nijmegen Valkhof, Saalburg). Work only in
`/home/user/SomeRepository/engine/runs/dodeca/tests/models3d/`: read no other files in the repository, write files
only there, do not commit.

For every model or scan record: object (findspot, museum, inventory number), who made the model and how
(photogrammetry, structured light, CT, laser), the host and URL, whether the file is downloadable and in which format,
licence, approximate resolution or triangle count if given, and whether anyone has published measurements made on it
(hole diameters, knob shape, wall thickness, CT sections). NEVER invent a model or URL; say when a model is only
mentioned and not found.

Final answer (text only), at most 700 words:
=== MODELS ===
MODEL 1: object | museum/inv. | maker and method | host URL | downloadable? format, licence | resolution | measurements published?
(as many as found)
BEST FOR THE TESTS: the 3-6 models whose resolution is good enough to measure hole diameters to about 0.5 mm and to
see knob-tip shape, with the exact URLs to download.
