=== REFRAMES ===

**ASSUMPTIONS:**
- A crease can be "physically absent", meaning zero residual deformation. (contradicted: every polymer and adhesive layer creeps viscoelastically, and every shipped fix is a relative cut of −20% to −82%, never zero)
- "Invisible" is one binary property. In practice it depends on depth, slope, lighting angle and touch, and no threshold is defined.
- The Fold 7's ~0.7 mm depth is a known baseline. (contradicted: no public µm profilometry exists for any phone)
- Apple's crease is about ¼ of the Fold 7's. (contradicted as fact: it is a leak, with no review units)
- The cover glass is the lever. (contradicted: the polymer and OCA layers set the crease, and UTG tests prove survival, not flatness)
- Open/close cycle count is the stress that matters. (contradicted: OCA needs hours to recover, so time held folded and temperature dominate, and no one has published them)
- Balancing the neutral plane can give zero crease. (contradicted: it balances only one fold state)
- Heat-based self-healing is available. (contradicted: it needs about 60–70 °C, above phone-safe limits)
- A larger radius is free. (contradicted: radius is capped by folded thickness, about 8.7 mm on the Fold 7)
- The fold must be an inward book fold. (not stated; any folding phone with one continuous screen qualifies)
- Cost is irrelevant. (partly contradicted: foldable yield is below 30%, so any added step is priced through yield; the ledger's "3× cheaper" target has no room, but the asker never set it)

**REFRAME 1:** What residual profile is below what a person can see or feel, and can a stack be designed to stay below it? The profile would be set by maximum slope in mrad, depth in µm, specular-reflection contrast at grazing light, and finger detectability. | CHANGES: target goes from "physically absent" to a measured, sub-perceptual threshold | IMPORTANCE: high | POSSIBILITY: high | WHY: the asker's real aim is "the eye cannot see it". Zero deformation is unattainable, but a threshold below perception is testable.

**REFRAME 2:** Restate persistence as a dwell-time × temperature × humidity budget, not 2000 cycles. 2000 cycles at 1 per day is about 5.5 years and about 10⁴ hours folded overnight. At 50 per day it is about 40 days. | CHANGES: unit of the durability requirement | IMPORTANCE: high | POSSIBILITY: high | WHY: creep is driven by time under load. A design that passes 2000 fast cycles can still fail after one night folded in a hot pocket.

**REFRAME 3:** For each layer (PI substrate, OCAs, polarizer or its replacement, support plate, cover), what strain does it carry at the chosen radius? Can every layer be kept inside its fully recoverable regime under worst-case dwell, and which layer sets the limit? | CHANGES: from whole-stack invention to finding the binding layer | IMPORTANCE: high | POSSIBILITY: medium | WHY: the material puts the cause in the polymer and adhesive layers. Fixing the one layer that sets the limit is how an architecture gets built.

**REFRAME 4:** First measure surface profiles of a Fold 7 and a Find N6 by profilometry, new and after 2000 cycles with dwell, and only then design. | CHANGES: puts the baseline experiment ahead of the design | IMPORTANCE: medium | POSSIBILITY: high | WHY: it is the cheapest decisive experiment, and it replaces rumoured depths. It does not deliver an architecture by itself.

**REFRAME 5:** Within a fixed folded-thickness budget of about 9–10 mm, what fold radius and hinge-surface tolerance keep all layers recoverable? Can a teardrop geometry meet that? | CHANGES: makes the thickness-versus-crease trade explicit | IMPORTANCE: medium | POSSIBILITY: medium | WHY: radius works, but its cost is thickness, and the 0.05 mm tolerance of Oppo's hinge surfaces is itself a candidate visible line.

**REFRAME 6:** Remove the crease for no more than about +$20–40 in module cost without lowering panel yield. | CHANGES: adds a cost and yield constraint | IMPORTANCE: low–medium | POSSIBILITY: medium | WHY: this keeps the result manufacturable. A cost cut is not the asker's goal, so this belongs as a check, not as the question.

**KEEP:** 1, 3. Reframe 1 defines success. Reframe 3 locates the mechanism. Reframe 2's dwell budget should be the test condition for both.