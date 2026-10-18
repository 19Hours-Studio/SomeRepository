# Task: adversarial review - find what would make these ideas fail or overstate their value

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 4 ideas, already repaired once against reality by a researcher. Your job is to be the toughest competent
outside reviewer: an engineer who will lose money if any of these claims is wrong. You do NOT fix or improve the
ideas; you find their defects, prove each one with a number, and rank them.

You have tools: WebSearch/WebFetch and Bash with python3 (check every claim in real code). Work only in
`/home/user/SomeRepository/engine/runs/permafrost/genius/audit_att_1/`: read no other files in the repository, do not modify other files, do not commit.

For each idea, attack in this order:
1. Recompute every number the text states (arithmetic, units, mass/energy balances). Flag any that do not reproduce.
2. Consistency: list every tolerance, margin and window the design relies on, and check every rate in the design
   against it over the whole operating time (rate x duration vs window). Check that the site/route/season named
   really has the conditions assumed (temperatures, flows, ice, distances) - find measured data.
3. Baseline: is the comparison against the best current practice a competent operator would use, per unit of
   recovered/delivered product? Name the real competing alternatives it ignores and recompute the ratio.
4. Assumptions: which decisive numbers (efficiencies, friction, rates, loss fractions, costs) are assumed rather
   than sourced? How far can they move, and does the claim survive the plausible range?
5. Evidence and statistics: are the proposed tests able to show what is claimed (sample sizes, confidence bounds)?
6. Hazards and showstoppers not mentioned (safety, environment, regulation, logistics, scale-up).
Do not pad: a defect needs a mechanism and a number. If a claim survives your check, say so in one line.

Final answer (text only), exactly this format:
=== REVIEW ===
IDEA 1: <name>
DEFECT | <FATAL/MAJOR/MINOR> | <one sentence: what is wrong> | <the number or source that shows it>
(as many DEFECT lines as needed, most severe first)
SURVIVES | <claims that held up under your check, one line>
(same for the other ideas, in the same order as below)

THE 4 IDEAS:
IDEA 1
NAME: Frozen-Roof Jet Adits
MECHANISM: Anchor: an unmanned jet and hydro-elevator head on a hose drives 3 m adits along bedrock under intact frozen overburden. Pillars are jetted out on retreat so the roof settles, and only the pay is thawed and lifted. Repair: a realistic creek (6→1 °C, 100 L/s) gives only 2.1 MW, which is 21 m³/h, not 60. Adding a 2 ha black-lined recirculating settling pond (net 80-150 W/m²) brings the heat to 3.7-5.1 MW, which is 35-45 m³/h at 30% heat use (107 MJ/m³ of pay) over a 90-day summer. The adit must never flood, because 6 °C water thaws the roof 2-4 m/day. So adits are driven up-gradient, the hydro-elevator handles 1.3x the inflow, and the portal has an insulated curtain; there is no ventilation because nobody is inside. Advance of 3.7-8 m/h limits the roof's life to 25-45 h, with 3-5 cm of roof thaw, and pillar stress is 0.4-1.2 MPa against 1-2 MPa long-term strength for frozen gravel. Cost: 1,200-1,400 rub/m³ of pay including washing, which is 550-660 rub/g.
VALUE: For frozen placers under ≥20 m of cover it costs 550-660 rub/g, against ~1,040-1,670 rub/g for winter underground mining and 1,270-2,400 rub/g for open pit: 1.6-2.5x cheaper overall and 2-3.5x on the mining step alone. It loses to bulldozer open pits where cover is under 15 m.

IDEA 2
NAME: Year-Round Under-Ice Talik Crawler
MECHANISM: Anchor: mine the natural thaw bulb under a lake from beneath the intact winter ice, using the ice as roof and work platform. The 40-t crawler cannot fit through a 1.4×1.4 m hole, so it drives in from the shore before freeze-up. It carries a submerged jig, so only about 1% concentrate goes up the 2 m² moon-pool, which takes about 2 kW to keep open. Tailings go by tremie pipe into the crawler's own pit, inside a silt-curtain cell hung from the ice. Without the cell, 540 t/day of fines would add about 3,400 mg/L per day to the ~160k m³ of water under the ice. Load on the ice stays below 25 t until the ice reaches 1.1 m (mid-December at Yakutsk, Stefan a=2.7). The same unit works open water in summer: 270 d/yr at 150 m³/h is about 0.6 Mm³/yr. That needs about 9 ha of lake floor over talik per year, with a 7 m dig against a talik of 25 m or more.
VALUE: About 1,600 rub/g recovered, against about 2,140 for a summer suction dredge and about 1,930 for draining the lake and working it with dozers and a sluice. That is 1.2–1.35× cheaper, not several times, and only for lake placers that cannot be drained.

IDEA 3
NAME: Wintering Coal CHP Barge
MECHANISM: Anchor: the bunker barge that brings the winter's coal stays frozen in at the village and burns its own cargo as a combined heat and power plant. Repair: a thermal-oil coal boiler (80%) feeds an ORC (16% net), run heat-led into the village heat network. The 1.54 MW of reject heat replaces boiler-house coal burned at 65%, so the net extra fuel per kWh_e is about 0. Electric-only would cost 12.7 rub/kWh_e at 10k rub/t; the original 20-30x claim compared kWh of heat from coal with kWh of electricity from diesel. A 0.3 MWe unit needs 1,780 t of coal per winter, which fits one 2,000 t barge, and the 381 m³ of ash fits the hold space freed as coal is burned. Reject heat of 104 kW keeps an ice moat open around the hull and 44 kW keeps the hold unfrozen. Capex dominates the cost: 19-32 rub/kWh at 0.3 MWe (132-237 M rub) and 14 rub/kWh at 1 MWe for district centres.
VALUE: Winter electricity at 14-32 rub/kWh against 45-75 rub/kWh full diesel cost (1.9-4.3x cheaper, up to 6x where costs reach 88 rub/kWh), with the heat nearly free.

IDEA 4
NAME: Barge-Mounted Bluff Auger Coal
MECHANISM: Anchor: a spudded floating auger bores a frozen seam at water level in a river bluff and discharges straight into a hold, so no overburden is moved. At 20 kt/yr the rig sits idle most of the year and costs about 4,100 rub/t. The repaired version runs the whole ~100-day navigation season at about 60 t/h, for about 80 kt/yr. That rate sits between historical augers (21.5 t/h) and highwall miners (100–140 t/h). It fills four hopper barges moored alongside instead of its own hold. Thrust of 150–300 kN is taken by a frame bolted to the face, because three spuds (about 360 kN) are marginal. The frame has about 3 m of vertical travel to follow the 1–3 m drop in low-water stage during a campaign. Holes rise slightly so they drain. Face recovery is 62%, about 190 t per 80 m hole, which uses about 0.9 km of bluff a year.
VALUE: About 1,800 rub/t at a village bank within 150 km. That compares with 2,800–3,700 rub/t for a pit at the bank under a 20–30 m bluff (1.6–2× cheaper) and 7,100–11,600 rub/t for coal hauled 2,000+ km, as from Dzhebariki-Khaya (4–6× cheaper). There is no gain under a bluff of 10 m or less.

