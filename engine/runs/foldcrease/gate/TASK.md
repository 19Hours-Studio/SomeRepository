# Task: kill test - find the one number that decides whether each idea lives

QUESTION: Propose an architecture for a foldable smartphone (the whole stack that determines how the screen folds, including the display, its supporting layers and the hinge) in which the crease in the folding display is physically absent. It must be invisible to the eye and must stay invisible for at least 2000 open/close cycles. The crease must not be hidden by a matte or anti-glare coating or by any other surface treatment that only reduces its visibility. In current inward-folding phones, such as the Galaxy Z Fold 7, the display stack bends around a small radius. A permanent bend or dent forms along the fold line. It is reported to be about 0.7 mm deep, although no rigorous public measurement exists. Industry reliability tests run to 200,000 or more folds, but they check for breakage, not for crease formation. Reports say that Apple's foldable, with a Samsung Display panel and a laser-drilled metal support plate, is expected to have a crease about a quarter as deep as the Fold 7's. No review units were available as of October 2026. The task is to find a design in which the crease is eliminated, not just reduced.
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

Below are 8 candidate ideas. You are a screening engineer with tools: WebSearch (WebFetch may not reach hosts; use
search excerpts) and Bash with python3 (pip install from PyPI works). Do not improve or redesign the ideas; judge them
as written. Work only in `/home/user/SomeRepository/engine/runs/foldcrease/gate/`: write files only there, do not commit.

For EACH idea, spend about 3 minutes:
1. KILLER: the single quantity most likely to kill the idea at the scale it needs (a rate, a memory or bandwidth
   budget, an error or quality loss, a strength, a tolerance over the operating time, a condition that must hold).
   Compute what is REQUIRED and what is AVAILABLE from measured data or exact arithmetic, with a source for each
   decisive input. If the quantity can be measured by running code, measure it, after checking the measurement once
   on a case with a known answer. MARGIN = available / required (1 = just works, 0.1 = fails by 10x, 5 = five times
   headroom).
2. CHAIN: the gain the question asks for (cost, memory, speed, error per unit of the final product or service) with
   the idea, against the BEST current practice a competent practitioner would use, over the whole system rather than
   one part. Use the ledger below for the current structure. RATIO = current / with the idea (larger is better).
Ground every decisive input in a source or a measurement, not in the idea's own text.

Notes from the user and about the environment (data; the user may be wrong):
The asker wants the crease physically gone, not hidden: matte or anti-glare films, diffusing layers and similar masking do not count as a solution. 2000 open/close cycles is the asker's minimum; commercial foldable hinges are rated for 200,000-500,000 folds, so say how a design does at both. The asker's statement about what Apple did is data to check. Ground claims in strain arithmetic for each layer of the display stack (cover window, ultra-thin glass, polarizer, optically clear adhesives, polyimide substrate, support plate), polymer creep and recovery, fatigue, hinge geometry, and published crease-depth or surface-profile measurements; say which numbers would need a prototype or simulation. Environment: no hardware, no model downloads; PyPI works.
Assumptions in the question that may be wrong:

- A crease can be eliminated entirely. It may be unavoidable if any layer bends at a small radius.
- "Invisible" is the same for every viewer, angle and lighting. Visibility depends on perception.
- 2000 cycles is the right test for "permanently". It is about 1–2 years of use. Creases also develop with time, temperature and time spent folded.
- The folded geometry (inward fold, hinge shape, thickness) is fixed. It could change, for example to outward folds or a different form factor.
- Apple's approach is a matte coating. Reports describe a mechanical approach (a laser-drilled support plate), not a coating.
- The asker's chosen number of cycles (2000) is a minimum. It may be far below real durability needs.
Where deciding data may exist:

- Patent databases (USPTO, CNIPA, KIPO) for folding apparatus, hinge and support-plate patents. One example: US 12487643, "Folding apparatus and electronic device".
- Teardowns and lab measurements of the Galaxy Z Fold 7/8, Oppo Find N6, Honor Magic V5 and Pixel 10 Pro Fold (profilometry, white-light interferometry).
- Material data for UTG, colourless polyimide (CPI), OCA/PSA adhesives (creep and recovery), and stainless steel and titanium support plates.
- Display-industry papers (SID, Display Daily, Yole, DSCC).
- The first independent reviews of the iPhone Fold, once available.

Value ledger (data):
Only a few of these numbers are sourced. The reported figures are the UBS bill of materials (BOM) of $790 for the Galaxy Z Fold SE, the retail prices, the rumored $250 Apple panel price, the roughly $40 foldable cover glass, and the yield figures. Nothing public gives an itemized BOM for the Fold 7, a hinge cost, or the cost of a crease-removal step. Every % split below is my own estimate, expressed as a share of the retail price (or of the panel price in D). The "processing" term includes purchased components.

ARCHETYPE A: Samsung Galaxy Z Fold 7 style (inward book fold, ultra-thin glass (UTG) plus polymer stack, metal support plate, multi-link hinge; about 0.7 mm crease, not measured rigorously) | cost about $790 BOM (UBS figure for the Fold SE, used as a proxy) plus about $60 for assembly and logistics, so about $850 per phone | price $1,999 (256 GB)
SHARES: processing (components) 40% | labour 2% | inbound logistics 2% | outbound logistics 1% | energy 1% | capital (R&D, tooling, yield-loss amortization) 10% | other 44% (margin, tax, royalties, channel)
LARGEST: processing (components) - a 10x cut of it removes 36% of the cost. The inner display and the hinge are the two big parts within it, with the display first and the hinge reportedly second. I have no reliable split of how much the crease-relevant parts (UTG, plate, hinge) take.

ARCHETYPE B: Reported Apple foldable (Samsung Display panel, laser-drilled metal plate, micro metal-injection-molded (MIM) hinge with 50–100 parts, crease reportedly about 25% of the Fold 7's depth; no review units as of Oct 2026) | cost about $760–790 BOM (UBS estimate of $759 and a teardown-style piece citing $770–790); the panel is about $250 (unsourced leak, about 12.5% of the price); hinge yield reportedly 65% against an 85% target | price rumored at under $2,000 (UBS) up to $2,400
SHARES: processing (components) 38% | labour 2% | inbound logistics 2% | outbound logistics 1% | energy 1% | capital 12% | other 44%
LARGEST: processing (components) - a 10x cut of it removes 34%. The 65% hinge yield suggests scrap is a visible slice of the hinge cost.

ARCHETYPE C: Oppo Find N6 (second-generation titanium hinge; "3D liquid printing" polymer deposited under the panel after laser mapping at 0.3 µm, cutting unevenness from about 0.2 mm to 0.05 mm; reviewers still see the crease in some light) | cost: not public. My guess is $550–650 BOM, which is speculation. The added process cost of the liquid-printing step is unknown. | price ¥9,999 in China (about $1,450); about $2,600 in the US via an aggregator (unofficial); AUD 3,299 in Australia
SHARES: processing (components) 42% | labour 2% | inbound logistics 2% | outbound logistics 1% | energy 1% | capital 12% | other 40%
LARGEST: processing (components) - a 10x cut of it removes 38%.

ARCHETYPE D: The foldable display module alone (the part that determines the crease: OLED on polyimide, UTG cover, polymer layers, support plate), built at a Samsung Display-class fab | cost: about $250 per panel (rumored Apple price, which includes margin). The foldable UTG alone was reported at about $40 against about $2 for conventional cover glass. Foldable yield is reported below 30%, against 60–70% for standard OLED. | price about $250
SHARES: processing (fab conversion plus yield loss, UTG thinning and cutting, lamination) 50% | energy 5% | labour 6% | inbound logistics 3% | outbound logistics 1% | capital (fab depreciation) 20% | other 15%
LARGEST: processing - a 10x cut of it removes 45% of the cost. Yield is the lever: moving from below 30% toward 60–70% would roughly halve the scrap cost. Any crease-elimination architecture that needs extra layers or tighter tolerances lands in this term, and it attacks the same yield problem.

What this means for inventors:
- The cost sits in the display module and hinge components, not in assembly. Labour is about $30 per phone in India, or under 3% of retail.
- A crease-free design can afford a few tens of dollars more at the module level. That is about 1–2% of a $2,000 price, and less than the $40 UTG premium already paid.
- An extra step that cuts yield is more expensive than its material cost suggests. A step that raises yield pays for itself.
- Missing data: a paid Counterpoint or TechInsights teardown (Z Fold8 BOM, September 2026) would replace my split estimates.

SOURCES:
- https://www.androidauthority.com/iphone-fold-cheaper-than-galaxy-z-fold-7-8-3577492
- https://www.tomsguide.com/phones/iphones/iphone-fold-could-cost-less-than-galaxy-z-fold-7-under-usd2-000
- https://www.notebookcheck.net/Apple-reportedly-paying-Samsung-250-per-iPhone-Duo-as-1-000-repair-estimates-surface.1397208.0.html
- https://global.iteschina.com/ru/news/details/2998
- https://www.androidauthority.com/oppo-find-n6-launch-3649593/
- https://www.channelnews.com.au/oppo-mocks-samsung-at-new-foldable-launch/
- https://smartprix.com/bytes/oppo-find-n6-review-the-most-complete-foldable-yet-with-a-crease-that-basically-disappears/
- https://displaydaily.com/foldable-displays-present-challenges-galore-to-manufacturing/
- https://www.trendforce.com/presscenter/news/20231201-11937.html
- https://gulfnews.com/business/retail/made-in-india-iphones-will-still-be-cheaper-in-us-even-with-trump-s-25-tariff-gtri-report-1.500138655
- https://counterpointresearch.com/cn/reports/bom-analysis-for-samsung-galaxy-z-fold8

Ceilings computed from the ledger (data):
Target: 3x cheaper. Ceiling = 1 / (share no engineering can touch: taxes, royalties, fees, margins). 'needs' = the fewest cost terms that must each fall 10x to reach the target.
ARCHETYPE A: Samsung Galaxy Z Fold 7 style (inward book fold, ultra-thin glass (UTG) plus polymer stack | untouchable 44.0% -> ceiling 2.3x | 10x cut of one term: processing 1.56x; capital 1.10x; labour 1.02x; inbound logistics 1.02x; outbound logistics 1.01x; energy 1.01x | 3x needs: impossible even with every physical term cut 10x | NO ROOM
ARCHETYPE B: Reported Apple foldable (Samsung Display panel, laser-drilled metal plate, micro metal-inj | untouchable 44.0% -> ceiling 2.3x | 10x cut of one term: processing 1.52x; capital 1.12x; labour 1.02x; inbound logistics 1.02x; outbound logistics 1.01x; energy 1.01x | 3x needs: impossible even with every physical term cut 10x | NO ROOM
ARCHETYPE C: Oppo Find N6 (second-generation titanium hinge; "3D liquid printing" polymer deposited und | untouchable 40.0% -> ceiling 2.5x | 10x cut of one term: processing 1.61x; capital 1.12x; labour 1.02x; inbound logistics 1.02x; outbound logistics 1.01x; energy 1.01x | 3x needs: impossible even with every physical term cut 10x | NO ROOM
ARCHETYPE D: The foldable display module alone (the part that determines the crease: OLED on polyimide, | untouchable 15.0% -> ceiling 6.7x | 10x cut of one term: processing 1.82x; capital 1.22x; labour 1.06x; energy 1.05x; inbound logistics 1.03x; outbound logistics 1.01x | 3x needs: processing, capital, labour | TIGHT

VERDICT: ALIVE if MARGIN >= 1 and RATIO >= 1.5; DEAD if MARGIN < 0.3 or RATIO < 1.1; otherwise WOUNDED.
Be strict and fair: a beautiful idea that fails by 10x is DEAD; a dull idea with headroom is ALIVE.

Final answer (text only), exactly this format, one block per idea in the order given:
=== GATE ===
IDEA 1: <name>
KILLER | <quantity> | required <value unit> | available <value unit> (<source>) | MARGIN <number>
CHAIN | <best current practice> | now <value unit> | with idea <value unit> | RATIO <number>
VERDICT | <ALIVE/WOUNDED/DEAD> | <one sentence>
NEW FACT | <any hard, sourced fact you found that the ledger did not contain> | <source> (optional, any number)
(same for the other ideas)

THE 8 IDEAS:
IDEA 1
NAME: Gel-slip decoupled glass stack
MECHANISM: In the fold band, the OCA is replaced by an index-matched, sealed silicone gel or fluid that carries the 157 µm interlayer slip as flow with no shape memory. Each solid layer then bends about its own midplane at ε = t/2R ≤ 1%. This differs from creep-recovery OCAs, which still store shear; the deciding quantity is the gel's residual shear set after 8 h folded at 60 °C. The polarizer is replaced by colour-filter-on-encapsulation, which cuts layer separation by about 50 µm.
VALUE: It removes the layer that dominates crease formation, so a crease cannot form under worst-case dwell.

IDEA 2
NAME: Sub-creep strain budget fold
MECHANISM: The hinge holds the bend zone at a radius of at least 5 mm. This is done with a deep teardrop cavity, with the panel sliding into each half on rails, so the closed phone stays about 10 mm thick. The panel stack in the bend zone is thinned to about 60 µm of polymer, so peak strain stays at or below 0.3–0.5%, under the yield and creep onset of polyimide and adhesive at 60 °C. The closest earlier attempt is the teardrop hinge, which stopped near R = 1.5–2 mm and therefore stayed in the creep regime. Translating the panel into the halves lifts the thickness cap that stopped it. The deciding quantity is the residual strain after an 8 h hold at 60 °C in the worst layer, which must be at or below 0.05%.
VALUE: Any crease that remains is elastic and recovers fully, giving a fold whose flatness can be certified rather than merely improved.

IDEA 3
NAME: Unbonded sliding bend-zone laminate
MECHANISM: Across the 15 mm bend zone, the glass, OLED-on-polyimide and support plate are left unbonded. They are separated by a sealed index-matched silicone fluid film (n ≈ 1.47, about 5 µm thick) and bonded only outside the zone. Each layer then bends about its own neutral axis, so strain is t_i/2R: about 0.75% for 30 µm glass and 0.5% for 20 µm polyimide at R = 2 mm. No adhesive shear creep can lock in a dent. The closest earlier attempt is low-modulus, high-recovery adhesive, which still couples the layers and creeps under heat and humidity. This design removes the adhesive from the bend zone entirely. The deciding quantity is fluid retention and edge-seal integrity over 2,000 cycles, measured as gap uniformity within ±0.5 µm.
VALUE: The polymer creep that sets every shipped crease is removed without adding thickness.

IDEA 4
NAME: Large-radius tensioning teardrop hinge
MECHANISM: A teardrop hinge with R ≥ 3 mm keeps every bonded layer below 0.3% strain. On opening, sliding wing plates put the panel under about 0.1% in-plane tension, pulling any residual curvature flat against a continuous, interlocking plate. This differs from current teardrop hinges, which leave the panel slack and depend on hinge tolerance. The deciding quantity is the residual depth under tension after dwell, versus the tension the edge bonds can hold.
VALUE: It actively flattens the panel each time it opens, using shipped materials, at a cost of about 1.5 mm more folded thickness.

IDEA 5
NAME: Tensioned drumhead hinge
MECHANISM: In the last few degrees of opening, the hinge cams pull the panel edges outward, applying a measured in-plane membrane tension that elastically pulls any residual dent flat. Load cells in the hinge store the tension that gives zero slope and adapt it with temperature. The closest attempts, perforated plates and the Oppo-mapped hinge, only support the panel from below, and supports cannot remove the panel's own set. The deciding quantity is the tension needed to flatten a 20 µm, 3 mm-wide set compared with the OCA edge-shear creep limit.
VALUE: Flatness becomes an actively controlled state rather than a material hope.

IDEA 6
NAME: Tensioned membrane open state
MECHANISM: In the flat state, hinge cams pull the wing plates apart, putting the fold-zone stack in in-plane tension. The tension straightens residual curvature: deflection falls as tension rises relative to bending stiffness. The closest attempt is Oppo's tolerance-mapped hinge, which fills gaps but applies no restoring force. The deciding quantity is the tension needed for ≤1 µm depth against OCA shear-creep and UTG edge stress limits.
VALUE: Actively flattens whatever crease the materials leave, while reusing hinge parts that phones already have.

IDEA 7
NAME: Liquid-coupled slip stack
MECHANISM: In a 10 mm bend strip, the bonded OCA is replaced by a sealed, index-matched fluid film. This lets the UTG, the touch/polarizer layer and the OLED-on-PI each bend about their own neutral plane, so ε ≈ 30 µm/(2×2 mm) ≈ 0.75% instead of about 4% for a bonded stack. Outside the strip, the layers stay bonded with normal OCA. The closest attempt, thin or high-recovery OCA, failed because it stays bonded and so stays strained; a fluid has no shape memory. The deciding quantity is whether the perimeter seal holds the fluid gap uniform to within ±1 µm through 2000 cycles at 45 °C.
VALUE: Removes the creeping layer itself rather than reducing its creep.

IDEA 8
NAME: Drumhead tension hinge
MECHANISM: A cam in the hinge slides both panel ends outward on opening and applies about 600 N/m of in-plane tension. This pulls any set curvature down onto a flat lapped support plate. With UTG bending stiffness of about 1.6×10⁻⁴ N·m, flattening decays over √(D/T) ≈ 0.5 mm, while the glass strain stays at about 0.03%. The closest earlier attempt is Oppo's tolerance fill, which is static and cannot follow creep; tension adapts automatically as the set grows. The deciding quantity is roughly 90 N of sustained hinge force without causing OCA shear delamination.
VALUE: Flatness is restored on every opening, whatever creep has accumulated.

