# Task: kill test - find the one number that decides whether each idea lives

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

Below are 4 candidate ideas. You are a screening engineer with tools: WebSearch (WebFetch may not reach hosts; use
search excerpts) and Bash with python3 (pip install from PyPI works). Do not improve or redesign the ideas; judge them
as written. Work only in `/home/user/SomeRepository/engine/runs/foldcrease_b/gate/c2/`: write files only there, do not commit.

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

Ledger: where the cost or the defect comes from (data):
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

Ceilings computed from the ledger (data):
Target: bring the defect from its value now to the target in each archetype (factor = now / target; 3x where the ledger gives no numbers). Ceiling = 1 / (share no answer can change: the floor). 'needs' = the fewest sources of the defect that must be removed entirely to reach the target.
ARCHETYPE A: Samsung Z Fold7 / Apple iPhone Duo. Inward fold on a small radius, with UTG (ultra-thin gl | now/target 3.0x | floor 10.0% -> ceiling 10.0x | removing one source: bend geometry and plastic set from the small radius 1.54x; creep of the polymer cover and pi films 1.25x; oca creep and stress relaxation while folded 1.18x; support plate and stiffness step at the fold 1.18x; hinge flatness and gap 1.05x | 3x needs: bend geometry and plastic set from the small radius, creep of the polymer cover and pi films, oca creep and stress relaxation while folded | TIGHT
ARCHETYPE B: Oppo Find N6. Thicker "Auto-Smoothing / Dome Memory" glass (reported as 50% thicker than U | now/target 3.0x | floor 15.0% -> ceiling 6.7x | removing one source: bend geometry 1.43x; polymer creep 1.18x; oca creep 1.18x; support plate and step 1.18x; hinge flatness 1.11x | 3x needs: bend geometry, polymer creep, oca creep, support plate and step | NO ROOM
ARCHETYPE C: Creep-managed stack from patents. The outer cover is stiffer than the inner one, so the fo | now/target 3.0x | floor 10.0% -> ceiling 10.0x | removing one source: polymer film creep 1.43x; oca creep 1.33x; bend geometry 1.25x; support plate 1.11x; hinge 1.05x | 3x needs: polymer film creep, oca creep, bend geometry | TIGHT

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

THE 4 IDEAS:
IDEA 1
NAME: Unbonded sliding bend-zone laminate
MECHANISM: Across the 15 mm bend zone, the glass, OLED-on-polyimide and support plate are left unbonded. They are separated by a sealed index-matched silicone fluid film (n ≈ 1.47, about 5 µm thick) and bonded only outside the zone. Each layer then bends about its own neutral axis, so strain is t_i/2R: about 0.75% for 30 µm glass and 0.5% for 20 µm polyimide at R = 2 mm. No adhesive shear creep can lock in a dent. The closest earlier attempt is low-modulus, high-recovery adhesive, which still couples the layers and creeps under heat and humidity. This design removes the adhesive from the bend zone entirely. The deciding quantity is fluid retention and edge-seal integrity over 2,000 cycles, measured as gap uniformity within ±0.5 µm.
VALUE: The polymer creep that sets every shipped crease is removed without adding thickness.

IDEA 2
NAME: Liquid-coupled slip stack
MECHANISM: In a 10 mm bend strip, the bonded OCA is replaced by a sealed, index-matched fluid film. This lets the UTG, the touch/polarizer layer and the OLED-on-PI each bend about their own neutral plane, so ε ≈ 30 µm/(2×2 mm) ≈ 0.75% instead of about 4% for a bonded stack. Outside the strip, the layers stay bonded with normal OCA. The closest attempt, thin or high-recovery OCA, failed because it stays bonded and so stays strained; a fluid has no shape memory. The deciding quantity is whether the perimeter seal holds the fluid gap uniform to within ±1 µm through 2000 cycles at 45 °C.
VALUE: Removes the creeping layer itself rather than reducing its creep.

IDEA 3
NAME: Tensioned drumhead hinge
MECHANISM: In the last few degrees of opening, the hinge cams pull the panel edges outward, applying a measured in-plane membrane tension that elastically pulls any residual dent flat. Load cells in the hinge store the tension that gives zero slope and adapt it with temperature. The closest attempts, perforated plates and the Oppo-mapped hinge, only support the panel from below, and supports cannot remove the panel's own set. The deciding quantity is the tension needed to flatten a 20 µm, 3 mm-wide set compared with the OCA edge-shear creep limit.
VALUE: Flatness becomes an actively controlled state rather than a material hope.

IDEA 4
NAME: Drumhead tension hinge
MECHANISM: A cam in the hinge slides both panel ends outward on opening and applies about 600 N/m of in-plane tension. This pulls any set curvature down onto a flat lapped support plate. With UTG bending stiffness of about 1.6×10⁻⁴ N·m, flattening decays over √(D/T) ≈ 0.5 mm, while the glass strain stays at about 0.03%. The closest earlier attempt is Oppo's tolerance fill, which is static and cannot follow creep; tension adapts automatically as the set grows. The deciding quantity is roughly 90 N of sustained hinge force without causing OCA shear delamination.
VALUE: Flatness is restored on every opening, whatever creep has accumulated.

