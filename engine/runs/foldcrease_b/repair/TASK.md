# Task: repair original ideas against reality WITHOUT losing what makes them original

QUESTION: Propose an architecture for a foldable smartphone (the whole stack that determines how the screen folds, including the display, its supporting layers and the hinge) in which the crease in the folding display is physically absent. It must be invisible to the eye and must stay invisible for at least 2000 open/close cycles. The crease must not be hidden by a matte or anti-glare coating or by any other surface treatment that only reduces its visibility. In current inward-folding phones, such as the Galaxy Z Fold 7, the display stack bends around a small radius. A permanent bend or dent forms along the fold line. It is reported to be about 0.7 mm deep, although no rigorous public measurement exists. Industry reliability tests run to 200,000 or more folds, but they check for breakage, not for crease formation. Apple officially launched its foldable, the iPhone Duo, on 9 September 2026 (on sale since 23 October 2026). Apple's hardware executives say a matte nano-texture coating minimizes the crease's visibility and that the top cover layer can be peeled off and replaced (about $19 with AppleCare); Apple does not claim the crease is gone, and hands-on reports differ on how visible it is. That matte, masking approach is what the asker rejects. The task is to find a design in which the crease is eliminated, not just reduced.
A good answer: 
- The answer is a complete architecture covering the display stack layers, the support structure and the hinge. Each layer's role is stated, along with the mechanism by which the crease cannot form or cannot be seen.
- It states how "invisible" would be measured. Examples are residual crease depth in µm and angle in degrees, optical reflection and off-axis visibility, and finger-touch detectability. It gives a target value for each measure.
- It states how persistence over 2000 cycles would be tested, and which conditions (temperature, humidity, time held folded) could break it.
- It states the main physical failure modes, such as plastic creep or permanent deformation of the polymer layers, adhesive creep, and glass fatigue. It also gives the trade-offs against thickness, mass, cost, display brightness and optical quality, touch and stylus feel, and durability.
- It distinguishes what is established by data from what is speculation. It names the cheapest experiment that would test the central claim.
- It is compared honestly with the Apple/Samsung approach that has been reported, and with the Oppo Find N6 approach.
Constraints: 
- No matte or anti-glare masking coating as the means of hiding the crease.
- The crease must be actually invisible, not just less visible.
- It must stay invisible for at least 2000 open/close cycles.
- It must be a folding smartphone.

Below are 4 ideas an idea engine produced for this question, with the results of the checks run on them so far
(judges' scores, kill tests or reviews, where present). Your job is NOT to invent new ideas and NOT to replace them with safer
known solutions. Your job is to make each one work while keeping its anchor - the one distinctive idea that makes it
original.

You have tools: WebSearch/WebFetch (check what exists, find real material data, field data and costs) and Bash with
python3 (do every estimate in real code). Work only in `/home/user/SomeRepository/engine/runs/foldcrease_b/repair/`: read no other files in the repository, do not
modify other files, do not commit. At most 6 searches per idea: the kill test, the facts below and the prior art
already cover the literature, so search only for a number the design needs that none of them gives (search results
are the most expensive part of this step).

For each idea, loop until it works or you can prove it cannot:
1. Name its ANCHOR (the distinctive idea) in a few words. This must survive.
2. Find the binding quantity (what decides whether it works at the needed scale - a rate, an energy balance, a
   recovery, a throughput, a safety limit) and compute it in Python with real numbers from the literature (cite the
   source in your notes).
3. BASELINE: compare against the BEST current practice a competent operator would actually use for the same job
   (list at least two real alternatives, including the cheapest one), and compute cost per unit of RECOVERED or
   DELIVERED product (per kg of metal recovered, per tonne delivered, per request served), not per tonne of raw material moved, with
   sourced numbers. Never compare against a strawman nobody would do.
4. CONSISTENCY PASS: list every tolerance, window and limit your design relies on (buoyancy margins, temperature
   limits, strengths, breakdown fields, stage efficiencies, site conditions where you placed it) and check every
   rate you computed against every one of them over the whole operating time (rate x duration vs window). Check
   that the site or route you chose really has the conditions you assumed. Write the check table in your notes.
5. If it fails, change the DESIGN AROUND the anchor (materials, geometry, operating regime, scale, season, which
   resource/cargo/deposit type it is used for) and recompute. Look for the regime where the anchor is strongest.
   Repeat - several rounds per idea is normal.
6. Name the hazards honestly and design them down where possible; say which unknown number decides the idea and the
   cheapest experiment that would measure it (with the sample size it needs).
7. Novelty: a PRIOR ART line, where present, names the closest existing work that a search for this mechanism found.
   Build on it instead of re-inventing it: say what the repaired design adds beyond it, and make that addition carry
   the value. If the repaired design turns out to be a known system, keep the anchor and find the version that is not
   known; if none exists, say KNOWN and give the best version of the known design.
8. Only if no anchor-preserving design can work, say so and give the best honest niche.

Facts that earlier checks in this run found (data; verify before relying on them):
(a slice: all 3 HARD facts and the 12 of 12 other facts that bear most on these candidates, sources omitted; the full ledger with sources is /home/user/SomeRepository/engine/runs/foldcrease_b/evidence.md - read it if you need a source or a fact that is not here)
FACT 1: Apple officially announced its first foldable iPhone, the iPhone Duo, at its 9 September 2026 event; it went on sale on 23 October 2026 | HARD
FACT 2: Apple's hardware engineering VP said the iPhone Duo's matte nano-texture coating minimizes the crease, and Apple chose matte because glossy screens make small surface variations easier to see; Apple does not claim there is no crease | HARD
FACT 3: The iPhone Duo's top cover layer is replaceable (peel off, fit a new one; $19 with AppleCare); the nano-texture polymer is said to be up to 40% harder than industry materials, with a scratch-resistant coating on top; reviewers note less vivid colours and shallower blacks than glossy foldables | HARD (Apple statements), SOFT (reviews)
FACT 4: Hands-on reports differ on how visible the iPhone Duo crease is: some call it barely noticeable, Notebookcheck reports it is visible in real-world videos; long-term visibility is unmeasured | SOFT
FACT 5: The HTX lab measured the iPhone Duo crease at about 48 µm peak-to-valley new and about 167 µm after 3,000 folds, with a 1.24° slope. An older phone in the same test showed 350 µm, and one unnamed rival did better than the Duo. Hands-on reports still see a crease under some lighting. | NEW from gate, check before relying on it
FACT 6: Samsung's Eco² OLED (Galaxy Z Fold3, 2021) already removes the polarizer by putting a colour filter on the encapsulation, saving about 50–100 µm of thickness. | NEW from gate, check before relying on it
FACT 7: A standard static-fold test (5 mm radius, 24 h at 60 °C/93 % RH, then 24 h hanging) left crosslinked PU films at 50–70° and thermoplastic PU at 180°, meaning it did not unfold at all. | NEW from gate, check before relying on it
FACT 8: Oppo's own figure for the Find N6 is about 0.05 mm (50 µm) surface variation. It is a manufacturer claim, not an independent measurement. | NEW from gate, check before relying on it
FACT 9: When folded, bonding at the zone ends forces a membrane mismatch of πd/L = 0.63% into the PI, on top of its 0.5% bending strain. That is sustained tension in a polymer layer, which is exactly what drives creep. | NEW from gate, check before relying on it
FACT 10: iPhone Duo peak-to-valley crease height: 48 µm new, 167 µm after 3000 folds (HTX Studio) | NEW from gate, check before relying on it
FACT 11: With fluid films in place of OCA, the mismatch at each interface is πd/L ≈ 1.4% (d ≈ 45 µm, L = 10 mm). That is about double the 0.75% the idea claims. | NEW from gate, check before relying on it
FACT 12: Foldable OCA storage modulus G′ is about 1.4×10⁵ Pa at −20 °C and about 9×10⁴ Pa at 25 °C | NEW from gate, check before relying on it
FACT 13: Foldable OCA must take more than 300% shear and recover fully after a static fold of up to 10 days | NEW from gate, check before relying on it
FACT 14: Oppo N6: the hinge surface height variance went from 0.2 mm to 0.05 mm, and the crease is 82% shallower than the N5 per TÜV, but no µm value is published | NEW from gate, check before relying on it
FACT 15: iPhone Duo reviews say the nano-texture hides the crease in daily use, but it can still be felt and seen at some angles. This supports the asker's description of Apple's approach. | NEW from gate, check before relying on it
Notes from the user (data; the user may be wrong):
(none)
Keep `LOG.md` in your folder: one line per round (idea, change, decisive number, result). Spend about 45-60 minutes at most.

Final answer (text only): first the 4 repaired ideas in exactly this format, then a short NOTES section (per idea:
anchor kept?, decisive numbers with sources, best-baseline comparison per unit of recovered/delivered product,
consistency table summary, hazards, deciding unknown and experiment, closest existing work, verdict WORKS / NICHE / FAILS).
=== IDEAS ===
IDEA 1
NAME: (max 5 words)
MECHANISM: (2-5 sentences: the anchor first, then the repaired design, with the decisive computed numbers)
VALUE: (1 sentence, with the cost ratio vs the best current practice)
(same for the other ideas, in the same order as below)

THE 4 IDEAS:
IDEA 1
NAME: Tensioned drumhead hinge
MECHANISM: In the last few degrees of opening, the hinge cams pull the panel edges outward, applying a measured in-plane membrane tension that elastically pulls any residual dent flat. Load cells in the hinge store the tension that gives zero slope and adapt it with temperature. The closest attempts, perforated plates and the Oppo-mapped hinge, only support the panel from below, and supports cannot remove the panel's own set. The deciding quantity is the tension needed to flatten a 20 µm, 3 mm-wide set compared with the OCA edge-shear creep limit.
VALUE: Flatness becomes an actively controlled state rather than a material hope.
KILL TEST: killer Peak OCA shear at the edges, held for as long as the phone is open, at the tension needed to flatten a 20 µm, 3 mm-wide set to 2 µm. That needs T ≈ 3.9 kN/m, or about 580 N over a 151 mm fold, given a stack bending stiffness D ≥ 3.9×10⁻⁴ N·m. | margin 0.9 | whole-chain ratio 10.0 | WOUNDED: Closed-loop tension can mechanically flatten the crease by about 10x, but it holds about 580 N in the hinge and the OCA in near-limit shear for as long as the phone is open, well past the 10-day hold the adhesive is designed for.
PRIOR ART (search by mechanism): KNOWN partly | closest: EP 4738056 A1, Apple, 2026 (tension assembly applied only past a threshold hinge angle, i.e. at the end of opening) and US 12541230 https://www.goveda.com/patent/EP-4738056-A1 | it already has: cams or sliders pull the panel in the last degrees of opening, putting the panel in tension to flatten it. | the idea adds: load cells in the hinge that store the zero-slope tension and adapt it with temperature, i.e. closed-loop control. No patent with a tension sensor was found.

IDEA 2
NAME: Gel-slip decoupled glass stack
MECHANISM: In the fold band, the OCA is replaced by an index-matched, sealed silicone gel or fluid that carries the 157 µm interlayer slip as flow with no shape memory. Each solid layer then bends about its own midplane at ε = t/2R ≤ 1%. This differs from creep-recovery OCAs, which still store shear; the deciding quantity is the gel's residual shear set after 8 h folded at 60 °C. The polarizer is replaced by colour-filter-on-encapsulation, which cuts layer separation by about 50 µm.
VALUE: It removes the layer that dominates crease formation, so a crease cannot form under worst-case dwell.
KILL TEST: killer Bending strain in the solid polymer layers that still bend at the phone's small radius (cover PET or CPI, back film); the gel does not change this | margin 0.3 | whole-chain ratio 1.18 | WOUNDED: Even if the gel stores no shear set, the polymer films still bend at about 3x their creep-safe strain, and the polarizer saving is already in Samsung's design, so the gain is at most ~1.2x.
PRIOR ART (search by mechanism): KNOWN partly | closest: US 11546986, Korean-origin family, ~2023 (lubricating layer or air gap lets adjacent layers slip in the bend) and US 10147772 (compliant adhesive gives partial decoupling, multiple neutral planes) https://patents.justia.com/patent/11546986 | it already has: removing or replacing the shear-coupling adhesive in the fold band so layers slip and each bends about its own midplane; low-modulus, high-recovery OCAs. | the idea adds: an index-matched sealed gel or fluid replacing the OCA in the optical stack, with the set after 8 h at 60 °C as the criterion, plus colour-filter-on-encapsulation in place of the polarizer. Searches found no fluid or gel in the OCA position.

IDEA 3
NAME: Unbonded sliding bend-zone laminate
MECHANISM: Across the 15 mm bend zone, the glass, OLED-on-polyimide and support plate are left unbonded. They are separated by a sealed index-matched silicone fluid film (n ≈ 1.47, about 5 µm thick) and bonded only outside the zone. Each layer then bends about its own neutral axis, so strain is t_i/2R: about 0.75% for 30 µm glass and 0.5% for 20 µm polyimide at R = 2 mm. No adhesive shear creep can lock in a dent. The closest earlier attempt is low-modulus, high-recovery adhesive, which still couples the layers and creeps under heat and humidity. This design removes the adhesive from the bend zone entirely. The deciding quantity is fluid retention and edge-seal integrity over 2,000 cycles, measured as gap uniformity within ±0.5 µm.
VALUE: The polymer creep that sets every shipped crease is removed without adding thickness.
KILL TEST: killer Length mismatch between the unbonded layers. The layers are bonded at both ends of the zone and the fluid carries no shear, so a 20 µm PI layer over a 15 mm free span buckles once the mismatch exceeds the clamped Euler strain π²t²/3L². | margin 0.04 | whole-chain ratio 2.0 | DEAD: Bonding the layers at the zone ends means they cannot slide, so a few tens of ppm of thermal or creep mismatch buckles the free PI into a ripple that shows in reflection; the defect moves rather than disappears.
PRIOR ART (search by mechanism): KNOWN partly | closest: US 11546986 "Foldable support and display device" (lubricating layer or air gap in the bend zone so adjacent layers slide), plus US 10147772 (compliant adhesive decoupling layers into multiple neutral planes), Korean-origin family, ~2023 https://patents.justia.com/patent/11546986 | it already has: layers left free to slide in the bend zone, with a lubricating layer, air gap or non-bonded layer so each layer bends about its own neutral plane; adhesive bonding kept outside the bend zone (Samsung Display US 11985770 omits adhesive there) | the idea adds: a sealed, index-matched ~5 µm silicone fluid film between the glass, OLED and support of an optical stack, with a gap-uniformity and edge-seal retention criterion. No fluid-filled optical stack was found; the 11546986 layers are metal supports.

IDEA 4
NAME: Tensioned membrane open state
MECHANISM: In the flat state, hinge cams pull the wing plates apart, putting the fold-zone stack in in-plane tension. The tension straightens residual curvature: deflection falls as tension rises relative to bending stiffness. The closest attempt is Oppo's tolerance-mapped hinge, which fills gaps but applies no restoring force. The deciding quantity is the tension needed for ≤1 µm depth against OCA shear-creep and UTG edge stress limits.
VALUE: Actively flattens whatever crease the materials leave, while reusing hinge parts that phones already have.
KILL TEST: killer Peak shear the OCA must hold for as long as the phone stays open, at 60 °C, to carry the tension that pulls the crease down to ≤1 µm | margin 0.17 | whole-chain ratio 28.0 | DEAD: As written (≤1 µm), the bond has to hold about 6x the shear at which foldable OCAs already creep. The same model says ~120 N/m (0.004 % strain, 2.5 kPa peak shear) would reach the 20 µm target with about 4x margin, so the cheapest test is to tension a coupon of the stack after folding. Note that if the layers bond tightly (cold, about −20 °C) the stiffness rises about 40x and the margin goes away.
PRIOR ART (search by mechanism): KNOWN yes | closest: EP 4738056 A1, Apple, 2026 (tension assembly applies tension to the flexible display in the flat state; spring and slider) https://www.goveda.com/patent/EP-4738056-A1 | it already has: hinge or housing mechanism puts the display in in-plane tension when flat, and relaxes it when folded. Also US 12541230 (tension assembly keeps the panel flat and reduces the crease when unfolded), US 9874904 and US 10852774 (elastic pulling belt). | the idea adds: nothing material. Only the µm-depth tension target against OCA creep and UTG edge-stress limits is specific to the idea.

