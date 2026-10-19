I built four chains. Only one reaches 2x against current practice, none reaches 3x at P50, and against the best competent alternative even the surviving chain is cheaper by less than 1x. The script is /home/user/SomeRepository/engine/runs/permafrost/genius/compose/chains.py and its output is /home/user/SomeRepository/engine/runs/permafrost/genius/compose/chains_out.txt. It uses the kit, a 20,000-draw Monte Carlo and prints P50 (P10-P90). I committed nothing and wrote only in compose/. Inputs marked "est." are my own engineering estimates. Web search added only that D-grade coal is 5,100-5,400 kcal/kg (Kuznetsk example) and that Yakutian institutes already propose local "micro-strip mines" of 10-200 kt/yr for Arctic villages (mining-media.ru).

=== IDEAS ===
IDEA 1
NAME: Frozen-bluff auger coal, shallow bunker hulls
MECHANISM:
- A spudded floating auger (P5, repaired) bores a frozen coal seam in a 20-30 m river bluff during the 60-90 effective days of low water. The repairs use the reviewed 21-38 t/h at 75% availability and 30-50% field recovery, a frame with longer vertical travel, hole mouths kept above the campaign's low water, and remote operation from the tug with bluff monitoring.
- It discharges straight into unpowered 2,000 t hulls drawing 1.26 m (P7). One tug and 3 hulls shuttle the coal 150-300 km to winter-road villages on a shoaling Yana/Indigirka-type river. This replaces about 2,000 km of river haul, a transshipment depot and about 450 km of winter road.
- Coupling: low water is the only time the rig can reach the seam, and also the only time when nothing but hulls drawing 1.3 m or less can run the river (1,746-2,000 t payload at 1.5-2.0 m depth). The rig fills one hull every 5.9 days, so 3 hulls keep it loading with no mine stockpile, loader or transshipment.
- Each hull's last cargo of the season winters loaded as the shore boiler-house's bunker, burned first (P7's anchor). The boiler stays on shore and the hull is empty by January. The coal leaves the seam frozen and has 8-26 days above 0 °C before air means fall below zero on about 21 Sep. Stokers cut a slot as the hull rises 0.96 m. No extra hull is needed.
- Chains built with P4, P6 and the gold pieces all fell below 2x.

VALUE: Fuel heat into village boilers costs 1,700 RUB/Gcal (1,360-2,160) against 4,380 today. That is 2.6x (2.0-3.2x; 20% chance of reaching 3x) against today's long-haul plus winter-road supply. Against the best competent alternative it is 0.82x (0.67-0.98): a bank pit at the same bluff with the same hulls is cheaper and on its own gives 3.2x. One rig supplies about 25 kt/yr, which is 12% of Arctic Yakutia's 205 kt of utility coal and about 8,300 people within 300 km of one bluff.

=== CHAINS ===
CHAIN 1 (P5 + P7). Product: fuel heat into the boiler of a winter-road Arctic village, RUB per Gcal (LHV). Current coal is 5.1-5.4 Gcal/t; the local seam is 3.5-5.0 Gcal/t (est.).

| Link | Now (method) | Now | With the chain (method) | Chain, P50 (P10-P90) | Source |
|---|---|---|---|---|---|
| 1 Mining | Distant pit (Dzhebariki-Khaya/Zyryanka), 3,450 RUB/t including 1.5% tax/other | 657 | P5 auger, 25 kt/yr (18-34 kt); 4,820 RUB/t | 1,170 (900-1,550) | Ledger C2; P5 + review |
| 2 Loading at mine | Inside the haul | 0 | Auger discharges straight into the hull (coupling) | 0 | P5, P7 |
| 3 Haul | River 8,000 + depot 1,500 + 450 km winter road at 20 RUB/t-km = 18,500 RUB/t | 3,524 | P7 hulls, 150-300 km at 3-5 RUB/t-km, part-loaded at 1.5 m depth | 287 (216-382) | Ledger, LORP, P7 |
| 4 Village storage | Depot pile, reload, losses: 1,050 RUB/t | 200 | 23% in P7 bunker hulls (1,620 RUB/t), 77% on a shore pile (780 RUB/t) | 236 (189-296) | P7 + est. |
| Total | 23,000 RUB/t (ledger, est.) | 4,381 | 7,010 RUB/t (5,870-8,550) | 1,701 (1,360-2,160) | |

- **Best competent alternative:** bank pit at 2,800-3,700 RUB/t plus 150-300 RUB/t loading, the same hulls and haul, and a shore pile. That is 921 + 287 + 189 = 1,388 RUB/Gcal, or 5,750 RUB/t.
- **Ratio against current practice:** 2.58x (2.03-3.22). It is at least 2x in 91% of draws and at least 3x in 20%.
- **Ratio against the best competent alternative:** 0.82x (0.67-0.98).
- **Ceiling:** tax/other is the only untouched share (1.5%), giving a 67x ceiling, so it does not bind.

How the review defects are handled:
- **P5:**
  - MAJOR 2 (cycle time): uses the reviewed 21-38 t/h at 75% availability.
  - MAJOR 3 (river stage): low-water campaign only, with a longer-travel frame.
  - MAJOR 4 (field recovery): 30-50%, so 1.24-2.07x more holes per tonne.
  - MAJOR 5 (bluff toe): remote operation from the tug and bluff monitoring, +4-8 M RUB/yr.
  - MAJOR 1 (market): the rig is costed at its real 18-34 kt/yr. It loses to the pit below about 38 kt/yr, and that loss is reported, not hidden.
- **P7:**
  - MAJOR 1 and 4 (summer gap, break-up): the boiler stays on shore and summer heat is 2.8% of the year. The bunker is burned first so the hull is light, and it winters in a backwater at least 2.2 m deep.
  - MAJOR 2 (hold too small): the shore pile covers the rest.
  - MAJOR 3 (one cargo a year per hull): only shuttle hulls winter loaded, so no extra hull is bought. The as-designed version with one dedicated hull per 2,000 t was computed and gives 1.71x.
  - MAJOR 5 (self-heating): the bunker is the last cargo, from a frozen seam, in a covered hold with CO and temperature probes.

**Weakest link: P5 mining.**
- It costs 1,170 RUB/Gcal against 921 for a bank pit at the same bluff.
- P5 only matches the pit above about 38 kt/yr per rig, or under bluffs higher than about 36 m (est.), which is where collapse risk is worst.
- The P7 bunker also costs more than a shore pile (1,620 against 780 RUB/t) and holds only 23% of the coal.

**Decisive unknown: how much coal one floating auger delivers from a frozen seam in a season** (field recovery × effective days × cycle rate). It has never been measured.
- The chain drops below 2x if one rig delivers less than 15,000 t/yr (P50 is 25,000).
- 3x needs at least 35,000 t/yr at 4.25 Gcal/t, or 24,000 t/yr at 5.0 Gcal/t.
- Other thresholds for 2x: seam LHV below 3.23 Gcal/t, or today's price at the boiler below 17,450 RUB/t. River-bank villages that pay 7,100-11,600 RUB/t get only 0.8-1.3x.
- A one-season pilot of 61-138 holes (13-52 rig-days) would pin output per hole to within ±10%.

No chain reaches 3x against current practice at P50. The best found is Chain 1 at 2.6x, and that gain comes from mining locally, not from the pieces.

Dropped chains (P50 below 2x against current practice):
- **Chain 2, P5 + P7 + P6 (1 MWe CHP barge, winter heat and power):** 1.59x (1.31-1.91); 0.91x against the best alternative. CHP power costs 21 RUB/kWh against 18-55 RUB/kWh of avoided diesel fuel, and the standby diesel plant's cost does not go away.
- **Chain 3, P4 + P7:** 1.39x (1.06-1.92); 0.55x against a bank pit. The dredge cuts 13 t/h, reaches one bend a season, and the coal is 2.6-3.4 Gcal/t.
- **Chain 4, P2 + P8 (gold):** 1.42x (1.10-1.72). P1 + P8 gives 1.20x. Gold cannot pass 2.08x even with free earthmoving.
- **Other archetypes:** oil, copper, lithium and export coal have ceilings of 1.89x, 1.03x, 1.0x and 1.69x.