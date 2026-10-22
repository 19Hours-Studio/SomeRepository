"""Hole diameters (mm) of individual Roman dodecahedra, as found in search-result excerpts.

Every number below was read from a search excerpt quoting the named source. No value is
estimated or interpolated here. Provenance quality is graded in `grade`:
  A  = published per-hole table (peer/preprint literature quoting the excavation report)
  B  = museum-supplied or caliper measurements reported second-hand by an enthusiast page
  C  = partial / garbled excerpt, assignment of values to faces uncertain -> not analysed
"""

OBJECTS = {
    "Jublains": dict(
        grade="A",
        source=("Guillier, Delage & Besombes 2008 (excavation report) as tabulated by "
                "Sparavigna 2012, arXiv 1204.6497; object 59 mm high, 74 mm max diam., 81 g "
                "(nunc.ch / Grull). Museum: Musee archeologique departemental de Jublains."),
        precision=0.5,
        # ring A around unringed oval pole 1, ring B around unringed oval pole 1'
        # ring order as numbered in the source (2..6 and 2'..6')
        pole_A=(26.0, 21.5),          # face 1, oval, unringed
        pole_B=(25.5, 21.5),          # face 1', oval, unringed (Grull 2016 gives 22.5 x 21.5)
        ring_A=[21.5, 16.5, 21.0, 11.5, 17.0],   # faces 2,3,4,5,6
        ring_B=[10.5, 15.5, 22.0, 17.0, 22.0],   # faces 2',3',4',5',6'
        # opposite pairs given by the source: (1',1),(2',6),(3',5),(5',3),(4',4),(6',2)
        # i.e. ring_A index i  <->  ring_B index 4-i
    ),
    "Tongeren": dict(
        grade="B",
        source=("Gallo-Romeins Museum Tongeren piece (wingarden.de, quoting F. Bongart "
                "Eschweiler, 'Kultstaetten'; same list on atomicshrimp.com and Straight Dope "
                "forum). 81 mm high with knobs, 66 mm without, 172 g. Opposite pairs given; "
                "no ring/pole information. 4th pair 23.0/26.3 (wingarden) vs 23.0/26.0 "
                "(Atomic Shrimp)."),
        precision=0.1,
        pairs=[(10.6, 13.0), (13.8, 14.0), (25.2, 27.0), (23.0, 26.3), (15.6, 17.8),
               (20.3, 20.5)],
    ),
    "Romford": dict(
        grade="B",
        source=("Private find, garden north of Romford (Essex), c.1987, Brian Campbell; "
                "vernier-caliper E-W / N-S hole diameters reported on celticnz.co.nz "
                "'Decoding the Druidic Dodecahedron' parts 1-11. Faces 6, 7, 9 not retrieved. "
                "Opposite-face relations not known."),
        precision=0.01,
        faces={1: (22.31, 22.46), 2: (12.29, 12.23), 3: (15.92, 16.11), 4: (15.85, 15.85),
               5: (18.75, 18.77), 8: (11.31, 11.44), 10: (18.95, 19.03), 11: (13.61, 13.56),
               12: (16.04, 15.99)},
    ),
}

# Partial / not analysed (fewer than 8 reliably assigned holes, or photo-derived)
PARTIAL = {
    "Avenches": ("Musee romain d'Avenches; measured by S. Bosse Buchanan, Sparavigna "
                 "1206.0946 App. B. Excerpts give (1,1') 24.2/26.5 (the two unringed, "
                 "largest), (4',4) 14.5/13.4, (6',2) 14.2/15.4, a pair 20.2/17.6, 5'=20.6 "
                 "(table cols disagree). Museum label: 9-26 mm. Remaining holes not retrieved."),
    "Hunt Museum HCM 157": ("Limerick; museum letter quoted on celticnz.co.nz: F1 24.2, F2 17.9, "
                            "F4 15.7, F5 11.9, F6 15.3, F7 14.3 (inch conversion implies 15.2); "
                            "further unassigned 18.8, 16.2, 12.1, 21.8 (may include ring "
                            "diameters). Height 4.9 cm."),
    "Vienne / Coulon": "Sparavigna 1206.0946: diameters read from photographs with a grid; partial.",
    "Carnuntum 1 (Greiner no.78)": ("Kurzweil 1957 and Greiner 1996 tables not retrieved; blog "
                                   "notes one hole 16.0 (Kurzweil) vs 16.3 (Greiner) and one "
                                   "pair with zero difference."),
    "Fishguard (BM 1924,0411.1)": "range only, 27.67-40.55 mm",
    "Radelfingen": "range only, 9.5-27 mm; 98 g, 70 mm (VRGS)",
    "Goodrich Castle": "Guggenberger 2000: all openings the same size (only such case)",
    "Schwarzenacker 2008RMS0196": "DDB: each through-axis one large + one small hole, no two equal",
}
