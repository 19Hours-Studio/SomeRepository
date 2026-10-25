=== LEDGER ===
KIND: defect
METRIC: residual crease depth in the unfolded, flat, powered-off state, in µm (IEC 62715-6-22:2023 method), plus deflectometry slope distortion with the panel on | THRESHOLD: 60 µm. Prototypes below this rated "good" or better in a 25-person study of 17 prototypes (Seoul National University, AHFE 2023). That is "good", not "invisible". No published threshold for invisibility exists, so it is probably well below 60 µm. Deeper creases and larger radii were more visible, and depth mattered most.

ARCHETYPE A: Samsung Z Fold7 / Apple iPhone Duo. Inward fold on a small radius, with UTG (ultra-thin glass), a polymer cover layer and OCA (optically clear adhesive) bonded, a metal support plate and a teardrop hinge. Apple adds a nano-texture matte layer, which masks the crease but doesn't change its depth. | now: about 700 µm reported, unverified. I found no rigorous measurement for the Fold7 or the Duo. Reviews say "shallower, still present". That is roughly 10x the 60 µm threshold. | target: <20 µm after 2000 cycles. This is my own guess, one third of the 60 µm "good" limit, and it is not a perception limit.
SHARES (my judgment, not measured; additive): bend geometry and plastic set from the small radius 35 | creep of the polymer cover and PI films 20 | OCA creep and stress relaxation while folded 15 | support plate and stiffness step at the fold 15 | hinge flatness and gap 5 | other 10
LARGEST: bend geometry and plastic set - removing it removes about 35% of the defect. Strain scales roughly as thickness divided by radius, so a larger radius or a thinner stack cuts it directly.

ARCHETYPE B: Oppo Find N6. Thicker "Auto-Smoothing / Dome Memory" glass (reported as 50% thicker than UTG), a carbon-fibre support plate, a titanium hinge, laser-scanned and 3D-printed hinge surfaces, and a 0.03 mm assembly tolerance. | now: 80–82% less crease depth than the Find N5, TÜV Rheinland-certified per press reports. No µm value is published, and Oppo says the crease is not physically removed. If the N5 were near 700 µm, the N6 would be about 130 µm. That is an assumption, and it would still be about 2x the 60 µm threshold. | target: <20 µm
SHARES (judgment): bend geometry 30 | polymer creep 15 | OCA creep 15 | support plate and step 15 | hinge flatness (0.2 mm cut to 0.05 mm) 10 | other 15
LARGEST: bend geometry - removing it removes about 30%. The N6 attacks the hinge and glass, but a bend still forms.

ARCHETYPE C: Creep-managed stack from patents. The outer cover is stiffer than the inner one, so the fold recovers. Low-creep or high-recovery OCA. LG Chem's PET-based coating is claimed to survive 200,000 folds. | now: no public crease data. Patents say organic films "creep after prolonged folding", so the panel does not fully flatten. | target: <20 µm
SHARES (judgment): polymer film creep 30 | OCA creep 25 | bend geometry 20 | support plate 10 | hinge 5 | other 10
LARGEST: polymer film creep - removing it removes about 30%.

Reading across A, B and C: the shares are my judgment, not measured. The largest term in all three is the bend itself, meaning the radius and the stack thickness. Polymer and adhesive creep are second. Matte coatings change none of these terms. The central claim to test is that a crease-free stack needs a large-radius or non-bending fold, with glass and metal layers kept elastic and polymers and OCA kept out of the load path. The cheapest test is to fold coupons of the candidate stack 2000 times, with 24 hours folded at 60 °C/90% RH after each 500 cycles. Then measure depth with a profilometer or deflectometer, and compare against a Fold7-style stack and an N6-style stack.

STATES (worst first): folded and held for hours or days at 60–85 °C and high humidity (creep) | unfolded after 2000 cycles at room temperature | cold, about −20 °C, where the polymers stiffen and the glass is brittle | display on at a grazing angle under a window or lamp, where distortion shows most | display off with a glossy reflection of a straight line (deflectometry) | fingertip drag across the fold, which is a touch test | stylus or nail pressure at the fold line

SOURCES:
- https://openaccess.cms-conferences.org/publications/book/978-1-958651-47-6/article/978-1-958651-47-6_25
- https://sid.org/Portals/sid/Files/SID-Digest/docs/77-5.pdf
- https://www.vde-verlag.de/iec-standards/251630/iec-62715-6-22-2023.html
- https://www.androidauthority.com/oppo-find-n6-zero-feel-crease-durability-3648272
- https://www.oppo.com/en/newsroom/stories/oppo-find-n6-zero-feel-crease-foldable-innovation/
- https://m.gsmarena.com/oppo_offers_behindthescenes_look_at_how_it_achieved_find_n6s_creaseless_display-news-71735.php
- https://counterpointresearch.com/de/insights/crease-control-in-foldables
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12433131
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12065551
- https://shopsavvy.com/answers/samsung-galaxy-z-fold-7-screen-crease-visible