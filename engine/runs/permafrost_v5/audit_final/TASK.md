# Task: adversarial review - find what would make these ideas fail or overstate their value

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 9 ideas, already repaired once against reality by a researcher. Your job is to be the toughest competent
outside reviewer: an engineer who will lose money if any of these claims is wrong. You do NOT fix or improve the
ideas; you find their defects, prove each one with a number, and rank them.

You have tools: WebSearch/WebFetch and Bash with python3 (check every claim in real code). Work only in
`/home/user/SomeRepository/engine/runs/permafrost_v5/audit_final/`: read no other files in the repository, do not modify other files, do not commit.

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
RATIO | <whole-chain cost ratio against the best current practice after your corrections: current cost / cost with the idea, one number> | <one line basis>
KNOWN | <yes / partly / no: is this already done or seriously proposed?> | <the closest existing system, project or proposal, with source>
NEW FACT | <any hard fact you found that the material did not contain> | <source> (optional, any number)
(same for the other ideas, in the same order as below)

THE 9 IDEAS:
IDEA 1
NAME: Channel-Talik Seam Dredging
MECHANISM: Anchor: a dredge cuts the coal seam in place inside the unfrozen channel talik, where the river has already removed the cover, and pumps it into a hopper barge. Repair: only seams at thalweg level under high bluffs, where a bank pit would have to strip 15-25 m³/t. A leased dredge with a 150 kW cutter cuts lignite (UCS 5-7 MPa) at 46-65 m³/h, which is about 46-65 t/h and matches Kovin's measured 67 t/h. A 10 kt village-cluster year therefore takes 8-25 dredge-days, not "a week", and one dredge visits about 4 bends a season. An on-barge dewatering screen brings the coal to ~32% moisture (3,670 kcal/kg). Cutting in June-July lets stockpiles drain before freeze-up. Delivered cost is 2,700-4,300 rub/t, which is 730-1,170 rub/Gcal.
VALUE: 730-930 rub/Gcal with a shared dredge, against 2,830 rub/Gcal for northern-delivery coal at 15k rub/t (3.0-3.9x cheaper) and 1.4-2.4x below a bank micro-pit under high bluffs. There is no gain where the same seam has thin cover on land.

IDEA 2
NAME: Barge-Mounted Bluff Auger Coal
MECHANISM: Anchor: a spudded floating auger bores a frozen seam at water level in a river bluff and discharges straight into a hold, so no overburden is moved. At 20 kt/yr the rig sits idle most of the year and costs about 4,100 rub/t. The repaired version runs the whole ~100-day navigation season at about 60 t/h, for about 80 kt/yr. That rate sits between historical augers (21.5 t/h) and highwall miners (100–140 t/h). It fills four hopper barges moored alongside instead of its own hold. Thrust of 150–300 kN is taken by a frame bolted to the face, because three spuds (about 360 kN) are marginal. The frame has about 3 m of vertical travel to follow the 1–3 m drop in low-water stage during a campaign. Holes rise slightly so they drain. Face recovery is 62%, about 190 t per 80 m hole, which uses about 0.9 km of bluff a year.
VALUE: About 1,800 rub/t at a village bank within 150 km. That compares with 2,800–3,700 rub/t for a pit at the bank under a 20–30 m bluff (1.6–2× cheaper) and 7,100–11,600 rub/t for coal hauled 2,000+ km, as from Dzhebariki-Khaya (4–6× cheaper). There is no gain under a bluff of 10 m or less.

IDEA 3
NAME: Self-heated barge boilerhouse
MECHANISM: Anchor: the coal barge is itself the village boilerhouse and coal yard, frozen in at the berth. Repair: drop the bubbler. A covered 1 m moat is kept open with the boiler's own spare low-grade heat. It needs about 8 kW against roughly 480 kW of flue loss from a 3 MW boiler (0.3%), or 36 kW if the moat is left uncovered. The hull should sit in a backwater, not in the main channel. It pays best where the shore boilerhouse has to be replaced anyway.
VALUE: A net saving of 0.8–3.4k rub/t out of 15–23k delivered, about 1.04–1.3x cheaper.

IDEA 4
NAME: Pre-staged flood-crest barges
MECHANISM: Anchor: a loaded barge waits out the ice drift in a sheltered backwater and leaves on the flood crest. Repair: load it in autumn while it is still afloat at a deep berth, so nothing is loaded through ice. It winters in a backwater at least 2.5 m deep, and it is used on a tributary that is navigable only on the spring flood, where there is just one trip a year anyway. With a modelled 12-day recession, a convoy arriving 5–10 days late loses 35–62% of its load. A barge pre-staged at the river mouth goes in full.
VALUE: About 3,100 rub/t against 4,700–11,300 rub/t on that leg today (1.5–3.6x). On the Kolyma main stem the gain is only about 14%.

IDEA 5
NAME: Wintering Coal CHP Barge
MECHANISM: Anchor: the bunker barge that brings the winter's coal stays frozen in at the village and burns its own cargo as a combined heat and power plant. Repair: a thermal-oil coal boiler (80%) feeds an ORC (16% net), run heat-led into the village heat network. The 1.54 MW of reject heat replaces boiler-house coal burned at 65%, so the net extra fuel per kWh_e is about 0. Electric-only would cost 12.7 rub/kWh_e at 10k rub/t; the original 20-30x claim compared kWh of heat from coal with kWh of electricity from diesel. A 0.3 MWe unit needs 1,780 t of coal per winter, which fits one 2,000 t barge, and the 381 m³ of ash fits the hold space freed as coal is burned. Reject heat of 104 kW keeps an ice moat open around the hull and 44 kW keeps the hold unfrozen. Capex dominates the cost: 19-32 rub/kWh at 0.3 MWe (132-237 M rub) and 14 rub/kWh at 1 MWe for district centres.
VALUE: Winter electricity at 14-32 rub/kWh against 45-75 rub/kWh full diesel cost (1.9-4.3x cheaper, up to 6x where costs reach 88 rub/kWh), with the heat nearly free.

IDEA 6
NAME: Fuel on empty coal-barge legs
MECHANISM: Anchor: one Kolyma flow rides on the other flow's empty leg. The data reverse the direction. Only about 3 kt of dry cargo goes upstream against 165 kt of coal coming down, so at most 1.8% of the coal could ride on returning barges. The ~165 coal-barge legs going back upstream empty are the real spare capacity. About 17 kt/yr of Northern Delivery fuel would ride those legs in 42 t collapsible fuel bladders, with the coal hold acting as spill containment. That needs 17 of the 165 legs, about 100 bladders and 24 per shoal-limited 1,000 t leg.
VALUE: About 2,100 rub/t for the river leg against 2,700–12,000 rub/t for a dedicated 38–54-year-old tanker (1.3–5.7x). That is under 10% of the delivered diesel price. The real value is not having to replace the tanker fleet.

IDEA 7
NAME: Ice-Deck Borehole Talik Mining
MECHANISM: Anchor: drill from winter lake ice into the sub-lake talik, which is already thawed, and mine the pay by borehole hydraulic mining. That means no thaw (saves 90 MJ/m³, about 25 kWh/m³), no dike, no drainage and no stripping. Repair: 1.2 m of ice carries only ~25 t of parked load, so the ice is flood-thickened to ≥1.8 m (Gold's formula at A=3.5 kg/cm² gives 113 t short-term, ~57 t parked). The 20-25 t modules sit more than 57 m apart, and the casing is insulated where it passes through the ice. Loose saturated talik gravel holds no roof and caves into the cavity, so the method is limited to narrow (25-40 m), deep, fine-gravel buried channels (<15 cm, the intake limit). Holes go on an 18 m grid (jet reach R=9 m) and are airlifted at 20-40 m³/h. Drawing stops at D≈3.4-3.9 m³ drawn per m³ of pay, set by on-ice jig grade monitoring; this extracts 86-89% of the pay in each hole's footprint, and tailings go back down mined holes. Cost: 1,130-1,970 rub per m³ drawn, which is 3,000-4,800 rub/g of gold recovered.
VALUE: Recovers gold from narrow, deep sub-lake channels that today go unmined, at 3,000-4,800 rub/g. The cheapest alternative, a summer pontoon suction dredge, costs ≥8,800 rub/g, so this is 1.8-4.4x cheaper; on channels wider than 80 m it is only 1-1.5x cheaper.

IDEA 8
NAME: Frozen-bluff auger coal, shallow bunker hulls
MECHANISM: - A spudded floating auger (P5, repaired) bores a frozen coal seam in a 20-30 m river bluff during the 60-90 effective days of low water. The repairs use the reviewed 21-38 t/h at 75% availability and 30-50% field recovery, a frame with longer vertical travel, hole mouths kept above the campaign's low water, and remote operation from the tug with bluff monitoring. - It discharges straight into unpowered 2,000 t hulls drawing 1.26 m (P7). One tug and 3 hulls shuttle the coal 150-300 km to winter-road villages on a shoaling Yana/Indigirka-type river. This replaces about 2,000 km of river haul, a transshipment depot and about 450 km of winter road. - Coupling: low water is the only time the rig can reach the seam, and also the only time when nothing but hulls drawing 1.3 m or less can run the river (1,746-2,000 t payload at 1.5-2.0 m depth). The rig fills one hull every 5.9 days, so 3 hulls keep it loading with no mine stockpile, loader or transshipment. - Each hull's last cargo of the season winters loaded as the shore boiler-house's bunker, burned first (P7's anchor). The boiler stays on shore and the hull is empty by January. The coal leaves the seam frozen and has 8-26 days above 0 °C before air means fall below zero on about 21 Sep. Stokers cut a slot as the hull rises 0.96 m. No extra hull is needed. - Chains built with P4, P6 and the gold pieces all fell below 2x.
VALUE: Fuel heat into village boilers costs 1,700 RUB/Gcal (1,360-2,160) against 4,380 today. That is 2.6x (2.0-3.2x; 20% chance of reaching 3x) against today's long-haul plus winter-road supply. Against the best competent alternative it is 0.82x (0.67-0.98): a bank pit at the same bluff with the same hulls is cheaper and on its own gives 3.2x. One rig supplies about 25 kt/yr, which is 12% of Arctic Yakutia's 205 kt of utility coal and about 8,300 people within 300 km of one bluff.

IDEA 9
NAME: Scrape-thawed river-bluff lignite
MECHANISM: Anchor: the river has already exposed the seam, so it is mined by natural thaw only, with no drilling, blasting or overburden stripping. Repair: scrape a 0.1 m thawed layer off the bluff face every 1–3 days. Each scrape restarts the thaw, so the face thaws 3–7 cm/day, or 2.7–5.6 m per 85-day season, against 0.9–1.35 m when the face is left alone (a 1951 placer-mining paper reports about 10 cm/day on a freshly exposed surface). The best regime is one bluff with a seam at least 6 m thick, supplying 20 kt/yr to several villages from about 850 m of face. It works only above high water, behind a berm and settling sump, and the whole face has to retreat together so that no frozen overhang forms.
VALUE: About 3,200 rub/t of lignite, or 1,390 rub per useful Gcal. That is 2.8–4.3x cheaper than imported hard coal at 3,850–5,900 rub/Gcal, but only 1.0–1.5x cheaper than a conventional micro-pit on the same deposit, and 1.3–2.0x if one village is served alone.

