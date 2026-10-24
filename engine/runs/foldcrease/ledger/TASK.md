# Task: the value ledger - where the cost actually goes today

QUESTION the ledger serves: Propose an architecture for a foldable smartphone (the whole stack that determines how the screen folds, including the display, its supporting layers and the hinge) in which the crease in the folding display is physically absent. It must be invisible to the eye and must stay invisible for at least 2000 open/close cycles. The crease must not be hidden by a matte or anti-glare coating or by any other surface treatment that only reduces its visibility. In current inward-folding phones, such as the Galaxy Z Fold 7, the display stack bends around a small radius. A permanent bend or dent forms along the fold line. It is reported to be about 0.7 mm deep, although no rigorous public measurement exists. Industry reliability tests run to 200,000 or more folds, but they check for breakage, not for crease formation. Reports say that Apple's foldable, with a Samsung Display panel and a laser-drilled metal support plate, is expected to have a crease about a quarter as deep as the Fold 7's. No review units were available as of October 2026. The task is to find a design in which the crease is eliminated, not just reduced.
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

You are a cost researcher. Build the ledger that tells inventors WHERE THE COST IS today, with sourced numbers, for the
3-5 archetypes (a concrete use case + the way a competent practitioner does it today, best current practice) most
relevant to the question. "Cost" is what the question asks to reduce or improve - money, energy, memory, time,
bandwidth, error - per unit of the final product or service. Tools: WebSearch (WebFetch does not reach hosts here; use
excerpts) and Bash with python3. At most 15 searches. Write files only in the current directory; do not commit.

For each archetype give: best current practice in one line; the cost per unit of final product or service; the cost
split in % that sums to 100 across 4-8 terms natural to this domain (for physical goods use exactly: energy | labour |
inbound logistics | outbound logistics | processing | capital | other), always ending with "other" = the part that no
answer to this question could change (for goods: taxes, royalties, fees, margins); the largest term.

Final answer (text only), exactly this shape, at most 700 words:
=== LEDGER ===
ARCHETYPE A: <best practice> | cost <number unit per unit of product or service> | <price or target, if any>
SHARES: <term> x% | <term> y% | ... | other t%
LARGEST: <term> - a 10x cut of it removes <p>% of the cost
(same for B, C, ...)
SOURCES: short list of URLs.
