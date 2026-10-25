# Task: is the mechanism already known?

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

Below are 6 ideas that came through a kill test. For each, find the closest existing work: patents (Google Patents,
Espacenet, USPTO, Justia and similar excerpts), papers and products. Search for its MECHANISM - the principle and the
parts that do the work, in the words of that mechanism and of neighbouring fields - not for the problem it solves: work
on the same problem with another mechanism does not count, and work on another problem with the same mechanism does.
Tools: WebSearch only (WebFetch does not reach hosts here; use search excerpts). At most 4 searches per idea. Do not
judge whether the ideas work and do not improve them. Write no files.

For each idea:
- KNOWN yes = the closest item already has the mechanism that delivers the idea's value;
- KNOWN partly = it has the core mechanism but not the part named in NEW, and that part matters for the value;
- KNOWN no = nothing with this mechanism after the searches (still name the nearest item found).

Final answer (text only), exactly this format, one line per idea in the order given, at most 120 words per idea:
=== KNOWN ===
IDEA 1: KNOWN <yes/partly/no> | CLOSEST: <title or number, owner, year> | <URL> | SAME: <what it already has> | NEW: <what the idea has that it lacks, or "nothing">
(same for the other ideas)

THE 6 IDEAS:
IDEA 1
NAME: Unbonded sliding bend-zone laminate
MECHANISM: Across the 15 mm bend zone, the glass, OLED-on-polyimide and support plate are left unbonded. They are separated by a sealed index-matched silicone fluid film (n ≈ 1.47, about 5 µm thick) and bonded only outside the zone. Each layer then bends about its own neutral axis, so strain is t_i/2R: about 0.75% for 30 µm glass and 0.5% for 20 µm polyimide at R = 2 mm. No adhesive shear creep can lock in a dent. The closest earlier attempt is low-modulus, high-recovery adhesive, which still couples the layers and creeps under heat and humidity. This design removes the adhesive from the bend zone entirely. The deciding quantity is fluid retention and edge-seal integrity over 2,000 cycles, measured as gap uniformity within ±0.5 µm.
VALUE: The polymer creep that sets every shipped crease is removed without adding thickness.

IDEA 2
NAME: Tensioned membrane open state
MECHANISM: In the flat state, hinge cams pull the wing plates apart, putting the fold-zone stack in in-plane tension. The tension straightens residual curvature: deflection falls as tension rises relative to bending stiffness. The closest attempt is Oppo's tolerance-mapped hinge, which fills gaps but applies no restoring force. The deciding quantity is the tension needed for ≤1 µm depth against OCA shear-creep and UTG edge stress limits.
VALUE: Actively flattens whatever crease the materials leave, while reusing hinge parts that phones already have.

IDEA 3
NAME: Gel-slip decoupled glass stack
MECHANISM: In the fold band, the OCA is replaced by an index-matched, sealed silicone gel or fluid that carries the 157 µm interlayer slip as flow with no shape memory. Each solid layer then bends about its own midplane at ε = t/2R ≤ 1%. This differs from creep-recovery OCAs, which still store shear; the deciding quantity is the gel's residual shear set after 8 h folded at 60 °C. The polarizer is replaced by colour-filter-on-encapsulation, which cuts layer separation by about 50 µm.
VALUE: It removes the layer that dominates crease formation, so a crease cannot form under worst-case dwell.

IDEA 4
NAME: Large-radius tensioning teardrop hinge
MECHANISM: A teardrop hinge with R ≥ 3 mm keeps every bonded layer below 0.3% strain. On opening, sliding wing plates put the panel under about 0.1% in-plane tension, pulling any residual curvature flat against a continuous, interlocking plate. This differs from current teardrop hinges, which leave the panel slack and depend on hinge tolerance. The deciding quantity is the residual depth under tension after dwell, versus the tension the edge bonds can hold.
VALUE: It actively flattens the panel each time it opens, using shipped materials, at a cost of about 1.5 mm more folded thickness.

IDEA 5
NAME: Drumhead tension hinge
MECHANISM: A cam in the hinge slides both panel ends outward on opening and applies about 600 N/m of in-plane tension. This pulls any set curvature down onto a flat lapped support plate. With UTG bending stiffness of about 1.6×10⁻⁴ N·m, flattening decays over √(D/T) ≈ 0.5 mm, while the glass strain stays at about 0.03%. The closest earlier attempt is Oppo's tolerance fill, which is static and cannot follow creep; tension adapts automatically as the set grows. The deciding quantity is roughly 90 N of sustained hinge force without causing OCA shear delamination.
VALUE: Flatness is restored on every opening, whatever creep has accumulated.

IDEA 6
NAME: Tensioned drumhead hinge
MECHANISM: In the last few degrees of opening, the hinge cams pull the panel edges outward, applying a measured in-plane membrane tension that elastically pulls any residual dent flat. Load cells in the hinge store the tension that gives zero slope and adapt it with temperature. The closest attempts, perforated plates and the Oppo-mapped hinge, only support the panel from below, and supports cannot remove the panel's own set. The deciding quantity is the tension needed to flatten a 20 µm, 3 mm-wide set compared with the OCA edge-shear creep limit.
VALUE: Flatness becomes an actively controlled state rather than a material hope.

