=== BRIEF ===
TYPE: invent

QUESTION: Propose an architecture for a foldable smartphone (the whole stack that determines how the screen folds, including the display, its supporting layers and the hinge) in which the crease in the folding display is physically absent. It must be invisible to the eye and must stay invisible for at least 2000 open/close cycles. The crease must not be hidden by a matte or anti-glare coating or by any other surface treatment that only reduces its visibility. In current inward-folding phones, such as the Galaxy Z Fold 7, the display stack bends around a small radius. A permanent bend or dent forms along the fold line. It is reported to be about 0.7 mm deep, although no rigorous public measurement exists. Industry reliability tests run to 200,000 or more folds, but they check for breakage, not for crease formation. Reports say that Apple's foldable, with a Samsung Display panel and a laser-drilled metal support plate, is expected to have a crease about a quarter as deep as the Fold 7's. No review units were available as of October 2026. The task is to find a design in which the crease is eliminated, not just reduced.

SUCCESS:
- The answer is a complete architecture covering the display stack layers, the support structure and the hinge. Each layer's role is stated, along with the mechanism by which the crease cannot form or cannot be seen.
- It states how "invisible" would be measured. Examples are residual crease depth in µm and angle in degrees, optical reflection and off-axis visibility, and finger-touch detectability. It gives a target value for each measure.
- It states how persistence over 2000 cycles would be tested, and which conditions (temperature, humidity, time held folded) could break it.
- It states the main physical failure modes, such as plastic creep or permanent deformation of the polymer layers, adhesive creep, and glass fatigue. It also gives the trade-offs against thickness, mass, cost, display brightness and optical quality, touch and stylus feel, and durability.
- It distinguishes what is established by data from what is speculation. It names the cheapest experiment that would test the central claim.
- It is compared honestly with the Apple/Samsung approach that has been reported, and with the Oppo Find N6 approach.

CONSTRAINTS:
- No matte or anti-glare masking coating as the means of hiding the crease.
- The crease must be actually invisible, not just less visible.
- It must stay invisible for at least 2000 open/close cycles.
- It must be a folding smartphone.

CONTEXT:
- Apple's foldable is reportedly using a Samsung Display panel with a laser-drilled metal support plate, about USD 30–35 per plate, made mostly by Fine M-Tec. This comes from analyst reports and is unconfirmed. [Macworld](https://www.macworld.com/article/2848958/report-apples-folding-iphone-wont-have-a-crease-thanks-to-laser-drilled-plates.html), [GSMArena](https://m.gsmarena.com/iphone_folds_creasefree_folding_screen_to_be_made_by_samsung_display-news-68631.php)
- A leak (Weibo) puts the Apple crease at <0.15 mm deep and <2.5° in angle. The Galaxy Z Fold 7 is about 0.7 mm. [AppleInsider](https://appleinsider.com/articles/26/02/25/iphone-fold-hinge-crease-will-be-about-14-the-depth-of-the-galaxy-fold-7/li)
- No peer-reviewed or primary data on crease formation in ultra-thin glass (UTG) stacks was found. [InfinitaLab](https://infinitalab.com/consumer-electronics/evolution-and-challenges-of-foldable-smartphones/)
- One explainer attributes the permanent crease to plastic deformation of the resin layers once the strain at the fold passes a limit. [Xenospectrum](https://xenospectrum.com/en/z-fold8-crease-titanium-hinge/)
- Samsung describes the stack as under compression on the inside of the fold and under tension on the outside ("folding stress"). UTG is typically 30–100 µm thick. [BusinessWire](https://www.businesswire.com/news/home/20200915006287/en/Samsung-Display-Unveils-Foldable-OLED-Panel-with-Worlds-Smallest-Curvature)
- The Oppo Find N6 markets a "zero-feel" crease and a 600k-fold life. An owner's month-long test still saw a crease. [Wccftech](https://wccftech.com/iphone-fold-creaseless-display-longevity-claims-expose-by-oppo-find-n6/amp/), [9to5Mac](https://9to5mac.com/2026/03/17/the-oppo-find-n6-gives-us-a-preview-of-the-iphone-fold-with-a-600k-fold-life/)
- Manufacturers do not publish crease measurements, so comparisons are hard.

DATA:
- Patent databases (USPTO, CNIPA, KIPO) for folding apparatus, hinge and support-plate patents. One example: US 12487643, "Folding apparatus and electronic device".
- Teardowns and lab measurements of the Galaxy Z Fold 7/8, Oppo Find N6, Honor Magic V5 and Pixel 10 Pro Fold (profilometry, white-light interferometry).
- Material data for UTG, colourless polyimide (CPI), OCA/PSA adhesives (creep and recovery), and stainless steel and titanium support plates.
- Display-industry papers (SID, Display Daily, Yole, DSCC).
- The first independent reviews of the iPhone Fold, once available.

ASSUMPTIONS:
- A crease can be eliminated entirely. It may be unavoidable if any layer bends at a small radius.
- "Invisible" is the same for every viewer, angle and lighting. Visibility depends on perception.
- 2000 cycles is the right test for "permanently". It is about 1–2 years of use. Creases also develop with time, temperature and time spent folded.
- The folded geometry (inward fold, hinge shape, thickness) is fixed. It could change, for example to outward folds or a different form factor.
- Apple's approach is a matte coating. Reports describe a mechanical approach (a laser-drilled support plate), not a coating.
- The asker's chosen number of cycles (2000) is a minimum. It may be far below real durability needs.

CORRECTED:
- "Apple used matte coatings to mask the crease" is not supported by the sources. The reports describe a mechanical approach (laser-drilled metal plate under a Samsung Display panel) to reduce crease depth. It is also not a shipped product: it is based on leaks and analyst reports, and no review units were available as of October 2026. I kept the constraint against masking coatings but did not attribute it to Apple.
- I defined "invisible" in measurable terms, because a visual judgement is not checkable.

UNCLEAR:
1. Must the phone still fold inward, with a flat full-width inner display, or could the form factor change (outward fold, rollable, multi-hinge)?
2. Is "invisible" judged by eye, by touch, or by instrument? What viewing conditions apply?
3. Is there a thickness, weight or cost limit?

MODE: standard