"""Hole diameters (mm) of individual Roman dodecahedra -- v2, verified against primary texts
(2026-10-22/23).  v1 (search excerpts only) is kept as sources/data_v1_backup.py.

Every number below was read from the full text, table or figure named in `source`;
nothing is estimated or interpolated.  Copies of the sources are in sources/.

Grades
  A  = first-hand per-hole table or labelled drawing in the excavation/owner publication,
       or a museum caliper table published verbatim
  B  = second-hand copy of a first-hand table (author's original not seen), or face/pair
       assignment that rests on an assumption stated in `notes`
  C  = partial, photo- or grid-read, or garbled -> listed in PARTIAL, not analysed

Per object
  faces     : face label -> diameter (mm); a tuple = two measured diameters (oval or
              min/max), analysed as their mean
  poles     : the two UNRINGED opposite faces (production pair), None if not known
  opposite  : list of opposite face pairs as given/implied by the source, None if unknown
  ringA/B   : the five faces around pole 1 / pole 1', in Duval (1981) order (counter-
              clockwise seen from above, ring B seen through the object), None if unknown
  independent: False if the value set is probably a re-measurement of another entry
"""

OBJECTS = {
    "Jublains": dict(
        grade="A",
        museum="Musee archeologique departemental de Jublains (Mayenne, F); Guggenberger no. 98",
        source=("Guillier, Delage & Besombes 2008, Revue archeologique de l'Ouest 25, 269-289, "
                "https://journals.openedition.org/rao/680 : par. 48 (size, weight, rings) and "
                "Fig. 12 'rabattement des 12 faces' (docannexe/image/680/img-16.png; per-face "
                "diameters printed on the figure; drawn 'selon les preconisations de P.-M. Duval "
                "(1981)', par. 49). Same values in Sparavigna 2012, arXiv 1204.6497, p. 2."),
        size="59 mm high resting, 48-52 mm face to face, 74 mm max., edge 21 mm",
        weight_g=81,
        type="10 ringed (concentric circles) + opposite unringed oval pair 1/1' (par. 48)",
        precision=0.5,
        faces={"1": (26.0, 21.5), "2": 21.5, "3": 16.5, "4": 21.0, "5": 11.5, "6": 17.0,
               "1'": (25.5, 21.5), "2'": 10.5, "3'": 15.5, "4'": 22.0, "5'": 17.0, "6'": 22.0},
        poles=("1", "1'"),
        ringA=["2", "3", "4", "5", "6"], ringB=["2'", "3'", "4'", "5'", "6'"],
        opposite=[("1", "1'"), ("2", "2'"), ("3", "3'"), ("4", "4'"), ("5", "5'"), ("6", "6'")],
        opposite_basis=("Duval 1981 convention (Gallia 39, p. 198: 'les faces opposees aux faces "
                        "1, 2, ... portent respectivement les n. 1', 2', ...'), cited by the report "
                        "(par. 49); Fig. 12 geometry agrees (ring B dashed = seen through, both "
                        "rings counter-clockwise, poles' vertices point opposite ways). Lalanne "
                        "(kadath.be/pdf/dodecaedres.pdf p. 2) pairs the faces the same way."),
        superseded_opposite=[("1", "1'"), ("2'", "6"), ("3'", "5"), ("5'", "3"), ("4'", "4"),
                             ("6'", "2")],  # Sparavigna 2012 p. 2 -- not the report's convention
        independent=True,
        corrections_v1=("values confirmed; OPPOSITE PAIRS CORRECTED from Sparavigna's (2',6),(3',5),"
                        "(4',4),(5',3),(6',2) to (k,k'); ring A/B order now Duval's; 'Grull 2016 "
                        "22.5x21.5' note dropped (primary report gives 25.5x21.5)."),
    ),
    "Vienne": dict(
        grade="A",
        museum="private collection of P.-M. Duval (found at Vienne, Isere, F; no context); "
               "Guggenberger no. 58",
        source=("Duval 1981, 'Comment decrire les dodecaedres gallo-romains', Gallia 39, 195-200, "
                "doi 10.3406/galia.1981.1829: Fig. 3 (p. 199; diameters printed on each face, "
                "column B = faces opposite column A) and text p. 200. Same values in Sparavigna "
                "1206.0946 Table V."),
        size="external diameter without knobs 55 mm (p. 200)",
        weight_g=None,
        type=("10 ringed + unringed opposite pair 1/1' = the two largest holes (p. 200: '0 [filets] "
              "pour 23 et 24 mm (1 et 1')'); rims of 1/1' less regular, 'comme s'ils avaient ete "
              "uses ... par un baton qui les aurait traverses' (p. 200)"),
        precision=0.5,
        faces={"1": 24.0, "2": 22.0, "3": 15.0, "4": 20.0, "5": 13.5, "6": 20.0,
               "1'": 23.0, "2'": 19.0, "3'": 22.0, "4'": 14.0, "5'": 22.0, "6'": 14.0},
        poles=("1", "1'"),
        ringA=["2", "3", "4", "5", "6"], ringB=["2'", "3'", "4'", "5'", "6'"],
        opposite=[("1", "1'"), ("2", "2'"), ("3", "3'"), ("4", "4'"), ("5", "5'"), ("6", "6'")],
        opposite_basis="explicit (Fig. 3 caption; Duval's own convention)",
        independent=True,
        corrections_v1="new object (v1 had it as 'photo-read, partial'; it is a first-hand table)",
        notes=("text p. 200 lists 22 mm holes as '2, 3', 5'' and ring counts '3 pour 22 mm (2, 2', "
               "5')'; Fig. 3 gives 2' = 19 mm, 3' = 22 mm -> the figure is used."),
    ),
    "Avenches": dict(
        grade="A",   # values; pairing B (see opposite_basis)
        museum="Site et Musee romain d'Avenches (CH), inv. 1882/1936; Guggenberger no. 86",
        source=("caliper measurements by Sandrine Bosse Buchanan (museum), published as Table B1, "
                "Appendix B of Sparavigna, arXiv 1206.0946v2 (2012), p. 8; pairs in Table II "
                "p. 3. Type and inv. no.: Guggenberger 2013, Math. Intelligencer 35(4) Fig. 2 "
                "caption ('the most common type with circles around ten of the twelve holes, "
                "height including knobs approximately 68 mm')."),
        size="about 68 mm with knobs (Guggenberger 2013); 58.5 mm diameter, B = 46.5 mm "
             "(Sparavigna 1206.0946 p. 3, '58.5 cm' sic)",
        weight_g=None,
        type=("most common type: 10 ringed + 2 unringed (Guggenberger 2013); which pair is "
              "unringed is NOT stated in a source seen; 1/1' assumed (largest pair, 1' 'probably "
              "elliptic', labels follow the Jublains figure)"),
        precision=0.01,
        faces={"1": (26.46, 26.62), "2": 15.44, "3": 18.31, "4": 13.4, "5": 10.43,
               "6": (17.38, 17.85), "1'": (24.16, 25.08), "2'": (19.9, 20.43), "3'": 8.68,
               "4'": (14.27, 14.68), "5'": (20.4, 20.83), "6'": 14.18},
        poles=("1", "1'"),
        ringA=None, ringB=None,   # cyclic order unknown
        opposite=[("1", "1'"), ("6'", "2"), ("4'", "4"), ("3'", "5"), ("5'", "3"), ("2'", "6")],
        opposite_basis=("B: Sparavigna's Table II, using her Jublains scheme (2',6),(3',5),(4',4),"
                        "(5',3),(6',2). Whether the museum labelled the faces by that scheme or "
                        "by the Jublains drawing (Duval, k opposite k') is not stated. Alternative "
                        "(k,k') run as sensitivity."),
        alt_opposite=[("1", "1'"), ("2", "2'"), ("3", "3'"), ("4", "4'"), ("5", "5'"), ("6", "6'")],
        independent=True,
        corrections_v1=("v1 had only 5 pairs, partly wrong ('pair 20.2/17.6', '5'=20.6'); full "
                        "12-value museum table now used; v1 of arXiv 1206.0946 had rounded "
                        "values (e.g. (6',2) 14/14) superseded by v2."),
    ),
    "Carnuntum 1 (Mereaux)": dict(
        grade="B",
        museum="Museum Carnuntinum (A); presumably Guggenberger/Greiner no. 78 (the piece "
               "Kurzweil 1957 studied)",
        source=("P. Mereaux(-Tanguy), 'Le dodecaedre: mesureur d'angle?', Kadath 1975 (not seen), "
                "copied in Sparavigna 1206.0946 Table III p. 3 and in B. Lalanne, 'Dodecaedres "
                "boulets', kadath.be/pdf/dodecaedres.pdf p. 1 (from the 2013 reprint in 'Le "
                "genie technologique des anciens'). Both copies give identical pairs."),
        size=("63 mm between parallel faces (Lalanne) -- but Sparavigna uses B = 40 mm for "
              "Carnuntum and 63 mm for Tongres: the two copies swap the sizes"),
        weight_g=None,
        type="unknown (no ring information)",
        precision=0.1,
        pairs=[(20.1, 20.3), (13.2, 13.7), (21.4, 22.4), (25.0, 26.5), (15.3, 17.3), (10.5, 13.0)],
        poles=None, ringA=None, ringB=None,
        opposite_basis="explicit: 'trous des faces opposees' (Lalanne p. 1)",
        independent=True,
        corrections_v1="new (v1 knew only a blog remark about Kurzweil/Greiner)",
        notes=("selection bias: Mereaux published Carnuntum because Kurzweil had noticed that "
               "opposite holes 'semblent identiques a l'oeil' (Sparavigna ref. 12 quote)."),
    ),
    "Tongeren (Mereaux)": dict(
        grade="B",
        museum="Provinciaal Gallo-Romeins Museum Tongeren (B) -- 'le dodecaedre de ce musee' "
               "(1975, director Smeesters); which inventory piece is not stated",
        source=("Mereaux 1975 as copied in Sparavigna 1206.0946 Table IV p. 3 and Lalanne, "
                "kadath.be/pdf/dodecaedres.pdf p. 1 (identical pairs)."),
        size="40 mm between parallel faces (Lalanne; Sparavigna B = 63 mm, see Carnuntum)",
        weight_g=None,
        type="unknown (no ring information)",
        precision=0.1,
        pairs=[(16.0, 16.2), (7.5, 8.5), (10.5, 12.5), (20.0, 22.5), (12.5, 15.5), (12.5, 16.5)],
        poles=None, ringA=None, ringB=None,
        opposite_basis="explicit (Lalanne p. 1)",
        independent=True,
        corrections_v1="new",
    ),
}

# Value sets kept out of the analysis (fewer than 8 reliable holes, photo/grid-read, or no
# per-hole data in the full text).  Filled from primary-source checks; see RESULT.md table.
PARTIAL = {
    "Coulon A / Coulon B (Sparavigna 1206.0946 Tables VI-VII, Figs. C1-C2)":
        "grid-read from a 1910 book photo, in quarter-grid units, no mm -> grade C",
    "Trier 1-4 (Faust 2003, Funde u. Ausgr. Bez. Trier 35, 31-35)":
        "full text read: lost pieces and fragments, no per-hole diameters",
    "Carmarthen, Soc. Antiquaries inv. 119 (Hill 1994, Antiq. J. 74, 289)":
        "p. 289 read (edge 40 mm, 86 mm between faces, no grooves, XRF); pp. 290-292 paywalled",
    "Enns 1 (Guggenberger 2013 Fig. 5; Guggenberger 2000, Mitt. Museumverein Lauriacum 38)":
        "per-face measurements drawn in Fig. 5, figure not accessible (paywall) -> not used",
}

# 3D-scan measurements (scan_objects.py -> data_scans.py), added 2026-10-23
from data_scans import SCANS as _SCANS  # noqa: E402
OBJECTS.update(_SCANS)
