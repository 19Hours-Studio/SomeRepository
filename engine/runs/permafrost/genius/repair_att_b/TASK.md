# Task: repair original ideas against reality WITHOUT losing what makes them original

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 4 ideas an idea engine produced for this question. Blind judges rated them for originality (O) and
order-of-magnitude feasibility (F, out of 10). Your job is NOT to invent new ideas and NOT to replace them with safer
known solutions. Your job is to make each one work while keeping its anchor - the one distinctive idea that makes it
original.

You have tools: WebSearch/WebFetch (check what exists, find real material data, field data and costs) and Bash with
python3 (do every estimate in real code). Work only in `/home/user/SomeRepository/engine/runs/permafrost/genius/repair_att_b/`: read no other files in the repository, do not
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
NAME: Ice-Deck Borehole Talik Mining
MECHANISM: Lakes over 200 m have taliks 36-67 m deep, beyond dredge reach. On them, skid rigs drill from the ice through gravel that is already thawed, jet-pump the pay at bedrock to a wash plant on the ice, and send tailings back down the hole. Closest is ATTEMPT 12: borehole mining in frozen ground stayed at one-well scale. Deciding quantity: thaw energy, which is zero in a talik, while 1.2-m ice carries ~50 t, so a dozen rigs can grid the lake and move for free.
VALUE: Deep placers under lakes are mined without a dike, drainage, stripping or thaw, at drill-rig capital.

IDEA 2
NAME: Frozen-Roof Jet Adits
MECHANISM: From the face, a jet and hydro-elevator head on a hose drives 3-m adits along bedrock under intact frozen overburden, thawing and lifting only the pay. Pillars are jetted out on retreat, so the roof settles as one slab with the vegetation mat untouched. Closest is ATTEMPT 14: drift mining died on costly fire and steam thaw; now the heat comes from creek water and nobody goes underground. Deciding quantity: water heat; 100 L/s cooled by 9 K carries ~3.8 MW, ~60 m³/h of pay at 30% use, so a season's pay needs a few weeks of one creek.
VALUE: Pay is mined without moving any overburden, which removes stripping, the largest physical placer cost.

IDEA 3
NAME: Channel-Talik Seam Dredging
MECHANISM: Where a seam crops out on the riverbed of an outside bend, a leased cutter-suction dredge cuts it underwater in the unfrozen channel talik and pumps it to a draining hopper barge. Thin interburden goes back into the cut, and the dredge keeps clear of the bluff toe. Closest is ATTEMPT 16: Susquehanna dredging only recovered washed-down fines; here the source is the seam in place. Deciding quantity: cutting rate in weak coal measures, ~100-300 m³/h, so a village cluster's year takes about a week, with no thawing.
VALUE: Local coal reaches villages with no stripping or bank works, leaving only short barge freight.

IDEA 4
NAME: Wintering Coal CHP Barge
MECHANISM: The bunker barge carries a coal boiler and a ~0.3 MW organic-Rankine set and, wintering in a fleet zaton, supplies the village's winter heat and power. In summer the existing diesel station runs alone, and its jacket heat covers the light heat load. Closest is ATTEMPT 20: a 70 MW floating plant overran its capital 4.1×; this is a used hull and a container kit. Deciding quantity: fuel cost per kWh, ~1-2 rub of coal against 30-45 rub of diesel, a 20-30× gap.
VALUE: Removes most of the 80-362 rub/kWh isolated-grid power bill as well as the heat cost, with no new grid.

