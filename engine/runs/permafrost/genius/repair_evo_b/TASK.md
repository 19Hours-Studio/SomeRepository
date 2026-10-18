# Task: repair original ideas against reality WITHOUT losing what makes them original

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 4 ideas an idea engine produced for this question. Blind judges rated them for originality (O) and
order-of-magnitude feasibility (F, out of 10). Your job is NOT to invent new ideas and NOT to replace them with safer
known solutions. Your job is to make each one work while keeping its anchor - the one distinctive idea that makes it
original.

You have tools: WebSearch/WebFetch (check what exists, find real material data, field data and costs) and Bash with
python3 (do every estimate in real code). Work only in `/home/user/SomeRepository/engine/runs/permafrost/genius/repair_evo_b/`: read no other files in the repository, do not
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
NAME: Brine-Thawed Shelf Tin Dredging
MECHANISM: A seagoing bucket-line dredge works known shelf tin placers such as Vankina Bay in the 80-100-day open-water season, where thousands of years of seawater have left the sediments unfrozen. Deciding quantity: depth to ice-bonded permafrost below the seabed. Drilling off the Lena delta found it tens of metres down within a few km of shore, several times the 5-15 m pay column, over thousands of km². No thawing, winter work or overland moves are needed.
VALUE: Tin mined with no stripping, thawing or roads, the items that dominate onshore placer cost.

IDEA 2
NAME: Thaw-Consolidation Gravity Stripping
MECHANISM: The stripping surface is graded at 8-10° toward the mined cell and sprinkled with creek water. Each time summer thaw reaches ice-rich muck, meltwater is released faster than it can drain, pore pressure carries the weight, and the thawed sheet slides intact into the cell like a natural active-layer detachment. Deciding quantity: excess pore-pressure ratio at the thaw front. Muck with 40-80% ice holds it near 0.85, which lowers the sliding threshold to about 5°, half the graded slope.
VALUE: Gravity replaces dozing of thawed layers, today's cheapest practice at 0.30 l/m³, removing most stripping fuel, fleet and operators.

IDEA 3
NAME: Barge Augers for Terrace Placers
MECHANISM: A barge works river terraces whose gold- or tin-bearing gravel lies at summer water level, boring 1.5-2 m auger holes 50-100 m along the frozen paystreak. The auger flights feed the gravel to an onboard warm-water scrubber and jig, tailings refill the finished holes, and 10-20 m of frozen overburden stays in place as roof. Deciding quantity: overburden moved per m³ of pay. It is zero instead of 5-10 m³, and a 2-m opening is 5-10× narrower than the span at which frozen ground fails. Suits gravels with clasts under about 0.4 m.
VALUE: Removes frozen-ground earthmoving, two-thirds of physical placer cost, with river access replacing winter roads.

IDEA 4
NAME: Shipyard-Built Floating Mine Plants
MECHANISM: The concentrator, power house and camp for a riverside or coastal deposit are built as hulls in an ordinary southern yard, towed in during open water, and floated into a pond dug at the site, where they freeze in for good. Crushers and mills stand on bedrock at the pond edge. Deciding quantity: the cost of building on permafrost. A floating hull is indifferent to the talik its own heat makes under the pond, so piles, thermosyphons and the 2-3× Far-North construction premium drop out.
VALUE: Builds most of the plant at central-Russia cost, cutting the largest cost line (capital, 41-42%) for an estimated 10-20% off delivered cost.

