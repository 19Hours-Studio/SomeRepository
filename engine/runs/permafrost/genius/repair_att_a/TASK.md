# Task: repair original ideas against reality WITHOUT losing what makes them original

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 4 ideas an idea engine produced for this question. Blind judges rated them for originality (O) and
order-of-magnitude feasibility (F, out of 10). Your job is NOT to invent new ideas and NOT to replace them with safer
known solutions. Your job is to make each one work while keeping its anchor - the one distinctive idea that makes it
original.

You have tools: WebSearch/WebFetch (check what exists, find real material data, field data and costs) and Bash with
python3 (do every estimate in real code). Work only in `/home/user/SomeRepository/engine/runs/permafrost/genius/repair_att_a/`: read no other files in the repository, do not
modify other files, do not commit.

For each idea, loop until it works or you can prove it cannot:
1. Name its ANCHOR (the distinctive idea) in a few words. This must survive.
2. Find the binding quantity (what decides whether it works at the needed scale - a rate, an energy balance, a
   recovery, a throughput, a safety limit) and compute it in Python with real numbers from the literature (cite the
   source in your notes).
3. BASELINE: compare against the BEST current practice a competent operator would actually use for the same job
   (list at least two real alternatives, including the cheapest one), and compute cost per unit of RECOVERED or
   DELIVERED product (per kg of metal recovered, per tonne delivered), not per tonne of raw material moved, with
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
7. Check novelty: if the repaired design turns out to be a known system, keep the anchor and find the version that is
   not known.
8. Only if no anchor-preserving design can work, say so and give the best honest niche.

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
NAME: Under-Ice Crawler Talik Mining
MECHANISM: A 40-t suction crawler works the thawed lake bed beneath intact ice, staying inside the thaw bulb mapped by resistivity survey. It lifts slurry through one heated 2-m² moon-pool to a sled-mounted wash plant. Closest is ATTEMPT 7: covers added only ~1.5 months and solid ice blocked the dredge; here the ice is the roof, so nothing is sawn or kept open. Deciding quantity: open water, ~2 m² against 1,500 m² (~750× less heat loss), and between lakes the kit is sledded over frozen tundra.
VALUE: Small thaw-lake placers become minable with no stripping, thawing or dredge, which removes the frozen earthmoving that is ~2/3 of placer physical cost.

IDEA 2
NAME: Thermo-Erosion Slab Toppling
MECHANISM: A monitor jets summer creek water into the paystreak only, cutting a 2-m niche along the base of the face, and a hydro-elevator lifts the thawed pay to the sluice. Once the niche is 10-15 m deep, the frozen overburden breaks off as slabs onto the cleaned floor. Closest is ATTEMPT 13: block cutting pays only for premium stone; here gravity replaces the jacks and the slab's own 0.5-1.5 MPa tensile weakness replaces the kerfs. Deciding quantity: niche advance; floods cut niches up to ~10 m deep into river banks in one season, and only the pay is thawed.
VALUE: Overburden moves with no dozing, ripping, drilling or jacking, removing most placer diesel and fleet cost.

IDEA 3
NAME: Barge Highwall Auger Coal
MECHANISM: A spudded barge at a bluff seam near water level bores 1-1.5-m auger entries 60-100 m into the frozen seam. The coal spirals into its hold while the frozen pillars and roof stay in place, so no rock is moved or stacked. Closest is ATTEMPT 17: small Arctic pits closed on weathered, exhausted coal; the auger passes the weathered outcrop and strips nothing. Deciding quantity: auger rate, ~50-150 t/h, so the ~20 kt a year for 5-8 villages takes 1-3 weeks.
VALUE: An estimated ~1,000 rub/t delivered within 150 km, about 3× below a pit plus winter road, with no autonomy needed.

IDEA 4
NAME: Relay Bunker Hull Swap
MECHANISM: Each village keeps a shallow bunker hull that holds a full year's coal and screw-feeds a containerized boiler in a fleet zaton, the sheltered backwater where river fleets already winter. In summer a loaded spare hull arrives and plugs in before the empty one leaves to reload and relieve the next village. Closest is ATTEMPT 21: one missed delivery forced an airlift; here a full hull is always berthed. Deciding quantity: hulls per village, N+1 for N villages, since 12-22-day round trips allow 4-7 relays a season; cooled flue gas blankets each hold to stop freezing and self-heating.
VALUE: Removes transshipment, the shore stockpile, trucking and stockpile loss, with no gap in summer heating.

