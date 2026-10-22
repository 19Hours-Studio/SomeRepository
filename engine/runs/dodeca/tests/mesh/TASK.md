# Task: a validated measuring tool for 3D models of Roman dodecahedra

Context: the Gallo-Roman bronze dodecahedra are hollow regular dodecahedra (4-11 cm across faces), each of the 12
pentagonal faces pierced by one round hole (6-40 mm, sizes differ within a piece), a knob (a small sphere, often on a
short neck) at each of the 20 corners. Two tests need measurements on 3D models (OBJ, STL, PLY, GLB, as published on
Sketchfab and similar): (1) all 12 hole diameters per piece, plus which holes are opposite each other, to test whether
sizes fall into classes and whether the two hemispheres around an opposite "pole" pair carry the same set; (2) the
shape of each of the 20 knob tips against its base (tip radius of curvature, flattening, asymmetry), to test whether
tips are evenly rounded by wear (as from throwing), worn on one face only, or fresh.

Build the tool in `/home/user/SomeRepository/engine/runs/dodeca/tests/mesh/`: write files only there, read no other
files in the repository, do not commit. You may `pip install` packages from PyPI (PyPI is reachable; other hosts are
not), e.g. trimesh, numpy, shapely, scipy, rtree, manifold3d - prefer few dependencies, and record them in
requirements.txt.

Requirements:
1. `measure.py <mesh file> [--units mm|cm|m|auto] [--out result.json]`: loads the mesh, works out the scale (models
   may be in arbitrary units; use --units, or auto from the overall face-to-face size if a size in mm is given with
   --size-mm), finds the 12 face planes (e.g. by clustering face normals of the outer surface), and for each face fits
   the hole: the inner contour of a planar section just inside the outer face, circle (and ellipse) fit, giving
   diameter, ovality and centre offset. It identifies the 6 opposite pairs. It finds the 20 knobs (geometry around
   the dodecahedron vertex directions) and for each fits a sphere to the outermost cap and reports tip radius,
   flattening (tip radius against the radius of the knob body) and the direction of any flat facet. It must cope with
   noisy photogrammetry meshes, missing knobs and broken pieces (report what is missing rather than failing).
2. `analyse.py result.json`: the statistics for the tests: clustering of the hole diameters into classes (largest-gap
   ratio and a gap statistic against two nulls simulated 100,000 times: uniform over the observed range, and a smooth
   continuum with 0.5-1 mm freehand scatter), whether the two hemispheres around each opposite pair carry the same
   multiset, whether opposite holes are equal; and for the knobs, whether tip rounding is even across all 20, limited
   to the 5 knobs of one face, or absent.
3. VALIDATION (the tool is worthless without it): generate synthetic dodecahedron meshes in python with KNOWN hole
   diameters (including a Jublains-like case with three classes 11 / 16.5 / 21.5 mm, and a continuum case), known
   knob radii, and controlled damage: Gaussian surface noise like photogrammetry (0.05-0.2 mm), a missing knob, one
   face broken off, arbitrary scale and rotation, and worn knobs (tips flattened evenly on all 20, or on the 5 of one
   face). Show in `validation.md` that the tool recovers diameters within 0.3 mm, finds the opposite pairs, separates
   classes from continuum, and detects even vs one-face knob wear, with a table of true vs measured values.

Final answer (text only), at most 500 words:
=== MESH TOOL ===
FILES: what each file does and how to run it
VALIDATION: the true-vs-measured table summary and the error bounds
LIMITS: what kinds of real models it may fail on, and what resolution it needs
