# Task: adversarial review - find what would make these ideas fail or overstate their value

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 6 ideas, already repaired once against reality by a researcher. Your job is to be the toughest competent
outside reviewer: an engineer who will lose money if any of these claims is wrong. You do NOT fix or improve the
ideas; you find their defects, prove each one with a number, and rank them.

You have tools: WebSearch/WebFetch and Bash with python3 (check every claim in real code). Work only in
`/home/user/SomeRepository/engine/runs/vs_permafrost_v5/compare/r2/`: read no other files in the repository, do not modify other files, do not commit.

For each idea, attack in this order:
1. Recompute every number the text states (arithmetic, units, mass, energy or memory balances). Flag any that do not reproduce.
2. Consistency: list every tolerance, margin and window the design relies on, and check every rate in the design
   against it over the whole operating time (rate x duration vs window). Check that the conditions assumed really
   hold where the idea is used (site, route, season, workload, hardware) - find measured data.
3. Baseline: is the comparison against the best current practice a competent operator would use, per unit of
   recovered or delivered product or service? Name the real competing alternatives it ignores and recompute the ratio.
4. Assumptions: which decisive numbers (efficiencies, friction, rates, loss fractions, costs) are assumed rather
   than sourced? How far can they move, and does the claim survive the plausible range?
5. Evidence and statistics: are the proposed tests able to show what is claimed (sample sizes, confidence bounds)?
6. Hazards and showstoppers not mentioned (safety, environment, regulation, logistics, scale-up).
Facts marked NEW were found by earlier checks in this run and are not yet verified: do not count them toward FIT,
and do not base a FATAL or MAJOR defect on a NEW fact alone unless you have verified it yourself (its source and,
for measurements, which object and which hole, face or item each number belongs to).
Do not pad: a defect needs a mechanism and a number. If a claim survives your check, say so in one line.

Final answer (text only), exactly this format:
=== REVIEW ===
IDEA 1: <name>
DEFECT | <FATAL/MAJOR/MINOR> | <one sentence: what is wrong> | <the number or source that shows it>
(as many DEFECT lines as needed, most severe first)
SURVIVES | <claims that held up under your check, one line>
RATIO | <whole-chain cost ratio against the best current practice after your corrections: current cost / cost with the idea, one number> | <one line basis>
KNOWN | <yes / partly / no: is this already done or seriously proposed?> | <the closest existing system, project or proposal, with source>
NEW FACT | <any hard fact you found that the material did not contain> | <source> (optional, any number)
(same for the other ideas, in the same order as below)

THE 6 IDEAS:
IDEA 1
NAME: Self-heated barge boilerhouse
MECHANISM: Anchor: the coal barge is itself the village boilerhouse and coal yard, frozen in at the berth. Repair: drop the bubbler. A covered 1 m moat is kept open with the boiler's own spare low-grade heat. It needs about 8 kW against roughly 480 kW of flue loss from a 3 MW boiler (0.3%), or 36 kW if the moat is left uncovered. The hull should sit in a backwater, not in the main channel. It pays best where the shore boilerhouse has to be replaced anyway.
VALUE: A net saving of 0.8–3.4k rub/t out of 15–23k delivered, about 1.04–1.3x cheaper.

IDEA 2
NAME: Single-use ice barges on spring flood
MECHANISM: During the 5-month winter at −30 to −40 °C, crews flood or spray river water on the river ice next to the mine to freeze hollow barge hulls, using ice or pykrete (ice with wood chips) and wood fibre from local forest clearing. No vessel has to be brought in. A hull 60×25×4.5 m with 1.5 m walls uses about 3,000 m³ of ice and carries about 2,500 t of concentrate or coal at 3.5 m draft and 1 m freeboard. Payload per tonne of ice is 0.9, against about 0.09 for a solid ice slab. Flood-freezing builds roughly 0.2 m of ice per day. At breakup, Lena ice drifts at 1–2.5 m/s and covers 160–290 km a day, so the 1,500 km from Yakutsk to the delta takes about 7–17 days. A 1.5 m wall takes about 24 days for the warmth to soak through, and in water at 0.5 °C it melts about 7 cm a day, so the hull lasts the trip. Pykrete also creeps much less than ice if kept below −16 °C. A small tug guides a convoy that launches just after the main ice run. At the river mouth the cargo is moved to ships and the hulls are left to melt, so nothing has to come back upstream and no fleet sits idle for 8 months. The approach also opens small tributaries that are only deep enough during the peak flood for a few weeks. The main risks are ice jams and hull creep, so the first step should be a 1,000 t test hull.
VALUE: My estimate is about $29 per tonne for building the hull plus a share of the tug, against about $77 per tonne average Lena freight (2010 figure). For mines with no river access, the current route is a winter road plus a barge, and the saving should be bigger, but I couldn't source that combined cost.

IDEA 3
NAME: Fuel on empty coal-barge legs
MECHANISM: Anchor: one Kolyma flow rides on the other flow's empty leg. The data reverse the direction. Only about 3 kt of dry cargo goes upstream against 165 kt of coal coming down, so at most 1.8% of the coal could ride on returning barges. The ~165 coal-barge legs going back upstream empty are the real spare capacity. About 17 kt/yr of Northern Delivery fuel would ride those legs in 42 t collapsible fuel bladders, with the coal hold acting as spill containment. That needs 17 of the 165 legs, about 100 bladders and 24 per shoal-limited 1,000 t leg.
VALUE: About 2,100 rub/t for the river leg against 2,700–12,000 rub/t for a dedicated 38–54-year-old tanker (1.3–5.7x). That is under 10% of the delivered diesel price. The real value is not having to replace the tanker fleet.

IDEA 4
NAME: Pre-staged flood-crest barges
MECHANISM: Anchor: a loaded barge waits out the ice drift in a sheltered backwater and leaves on the flood crest. Repair: load it in autumn while it is still afloat at a deep berth, so nothing is loaded through ice. It winters in a backwater at least 2.5 m deep, and it is used on a tributary that is navigable only on the spring flood, where there is just one trip a year anyway. With a modelled 12-day recession, a convoy arriving 5–10 days late loses 35–62% of its load. A barge pre-staged at the river mouth goes in full.
VALUE: About 3,100 rub/t against 4,700–11,300 rub/t on that leg today (1.5–3.6x). On the Kolyma main stem the gain is only about 14%.

IDEA 5
NAME: Winter-cold salt removal for lithium brines
MECHANISM: Deep brines under the Siberian Platform carry up to 600 mg/L of lithium in very salty water (170–631 g/L), close to the Kovykta gas field. Evaporation ponds can't work in that climate, and boiling off water takes about 2.26 GJ per tonne. Most salts dissolve less as brine gets colder, and quick-freezing has been patented as a way to drop sodium and potassium salts out first so lithium is enriched. The idea is to spray or pond the brine in −40 °C winter air, which costs nothing, so those salts crystallise out before the lithium extraction step. These brines are calcium-chloride rich, so they won't freeze to ice at −40 °C. The saving comes from salts dropping out, not from freezing out water.
VALUE: The extraction plant would treat a smaller volume of cleaner, more lithium-rich brine. I haven't costed this. The test is to chill real Kovykta brine to −40 °C in the lab and measure the lithium enrichment.

IDEA 6
NAME: Kite-towed sled trains, no roads
MECHANISM: Large automated towing kites, the kind already built for ships, pull trains of steel-runner sleds over natural snow on the windy Arctic coastal tundra and on sea ice, for example from Taymyr or Anabar mines to Northern Sea Route loading points. No winter road is built or maintained. A 320 m² SkySails kite gives up to 32 t of pull at peak. Sled friction on snow is roughly 0.05–0.1, so one kite moves a 320–640 t train. The Inuit Windsled has shown the idea at small scale: 2–3 t loads, 10–15 km/h, up to 248–270 km a day, and 1,541 km in 17 days. Fuel use is close to zero. Two things limit it. Friction rises sharply below −30 °C, and inland Yakutia is nearly calm in winter, so it only works on the windy coastal belt. Trains would still need tractor backup.
VALUE: The trains need almost no fuel and no road building. I couldn't find a sourced ruble-per-tonne-km rate for Arctic winter roads, so I can't give a per-tonne saving. A 3–5 train pilot should measure it.

