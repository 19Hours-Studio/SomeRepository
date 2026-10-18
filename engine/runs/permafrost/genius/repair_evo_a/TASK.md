# Task: repair original ideas against reality WITHOUT losing what makes them original

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 4 ideas an idea engine produced for this question. Blind judges rated them for originality (O) and
order-of-magnitude feasibility (F, out of 10). Your job is NOT to invent new ideas and NOT to replace them with safer
known solutions. Your job is to make each one work while keeping its anchor - the one distinctive idea that makes it
original.

You have tools: WebSearch/WebFetch (check what exists, find real material data, field data and costs) and Bash with
python3 (do every estimate in real code). Work only in `/home/user/SomeRepository/engine/runs/permafrost/genius/repair_evo_a/`: read no other files in the repository, do not
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
NAME: Drowned-Valley Reservoir Floor Dredging
MECHANISM: A submersible-pump dredge reaching 40 m mines placer valleys drowned for decades under Far-North hydro reservoirs such as the Kolyma. It works below the minimum drawdown level, where above-zero bottom water has thawed the whole floor, not just a lake centre. It works in open water only, so it needs no ice sawing, pond heating or moving between lakes. Deciding quantity: thawed area. A dredge needs about 0.1 km² a year against tens of km² of drowned floor, a margin of more than 100×.
VALUE: Gold recovered with neither stripping nor thawing, removing the frozen-ground earthmoving that is about two-thirds of physical placer cost.

IDEA 2
NAME: Creek-Undercut Overburden Caving
MECHANISM: Creek water runs through a starter gallery along the paystreak, thawing the pay and washing it to a sluice, the way a river cuts a niche into an Arctic bluff. Once the undercut reaches 10-20 m, the frozen overburden fails as a cantilever (0.5-2 MPa bending stress against 0.5-1.5 MPa tensile strength) and drops as intact slabs into the sluiced void, with no jacks, needles or backfill. Deciding quantity: heat delivered to the face. A 1 m³/s creek cooled by 8 K delivers about 33 MW, more than 300× a 108 kW hot-water drill.
VALUE: Gravity moves the overburden and free creek heat thaws the pay, removing most ripping and dozing.

IDEA 3
NAME: Barge Highwall Coal Augers
MECHANISM: A barge-mounted auger bores 1.5-2 m holes 100-200 m into a frozen coal seam from a river bluff at summer water level, leaving coal webs as pillars and conveying the coal into the hold. Deciding quantity: rock handled per tonne of coal. It is zero instead of 1.77 t, so stone placement, revetment and surplus riprap disappear and the bluff stays frozen. A 40 t/h auger cuts a 20 kt village season in about three weeks, so one barge can rotate among several rivers.
VALUE: Village coal with neither stripping nor a winter road, the two largest costs of a micro-pit (est. 2-3× cheaper).

IDEA 4
NAME: Docked Multi-Year Bunker Hull
MECHANISM: A surplus 8,000 t river hull is brought in once while empty (about 0.65 m light draught) and moored for good in a gated basin dug beside the heat network. It is fitted with an automatic boiler, and its hold is topped up ship-to-ship each summer from a riverside mine; boiler flue gas blankets the hold against self-heating. Deciding quantity: bunker capacity. The hold carries 2.3-4 winters of a 2,000-3,500 t burn, so the boiler never leaves, a low-water year can skip delivery, and the hull never meets the ice run.
VALUE: Removes transshipment, shore stockpiles, trucking and the shore boiler house (est. half of today's 8,080 rub/t) and ends winters lost to a failed delivery.

