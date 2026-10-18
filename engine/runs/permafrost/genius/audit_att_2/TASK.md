# Task: adversarial review - find what would make these ideas fail or overstate their value

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 4 ideas, already repaired once against reality by a researcher. Your job is to be the toughest competent
outside reviewer: an engineer who will lose money if any of these claims is wrong. You do NOT fix or improve the
ideas; you find their defects, prove each one with a number, and rank them.

You have tools: WebSearch/WebFetch and Bash with python3 (check every claim in real code). Work only in
`/home/user/SomeRepository/engine/runs/permafrost/genius/audit_att_2/`: read no other files in the repository, do not modify other files, do not commit.

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
NAME: Thermal Drift-and-Drop Placer Caving
MECHANISM: Anchor: water thaws only the pay layer, and the frozen overburden then falls under its own weight without any machine handling it. Toppling the face outward fails, because 62 m³ of rubble per metre of face lands in front of the next niche. So a trench is stripped instead (about 9% of the overburden), and remote low-pressure monitors drive 2-m drifts 30–60 m into the frozen pay from its side. A hydro-elevator at the face sends the slurry back to the trench. Each finished drift is widened past its long-term breaking span: 11–18 m for 6 m of overburden at 0.2–0.5 MPa. It stays open while being worked because a short-term strength of about 1 MPa lets it span about 25 m. The roof then drops 2 m in place, and mining retreats along the trench. Thaw rate is 5–10 m/day in theory and 0.15–5 m/day in field data. Water use is 3–8 m³ per m³ of pay, and fuel is about 60 rub/m³. It works best where overburden is 8–15 m thick.
VALUE: With 10 m of overburden, about 1,930 rub/g, against 2,270–3,980 for open cut with dozers and 3,500–7,000 for underground placer mining (1.2–3.6× cheaper). There is no gain with 6 m of overburden or less.

IDEA 2
NAME: Channel-Talik Seam Dredging
MECHANISM: Anchor: a dredge cuts the coal seam in place inside the unfrozen channel talik, where the river has already removed the cover, and pumps it into a hopper barge. Repair: only seams at thalweg level under high bluffs, where a bank pit would have to strip 15-25 m³/t. A leased dredge with a 150 kW cutter cuts lignite (UCS 5-7 MPa) at 46-65 m³/h, which is about 46-65 t/h and matches Kovin's measured 67 t/h. A 10 kt village-cluster year therefore takes 8-25 dredge-days, not "a week", and one dredge visits about 4 bends a season. An on-barge dewatering screen brings the coal to ~32% moisture (3,670 kcal/kg). Cutting in June-July lets stockpiles drain before freeze-up. Delivered cost is 2,700-4,300 rub/t, which is 730-1,170 rub/Gcal.
VALUE: 730-930 rub/Gcal with a shared dredge, against 2,830 rub/Gcal for northern-delivery coal at 15k rub/t (3.0-3.9x cheaper) and 1.4-2.4x below a bank micro-pit under high bluffs. There is no gain where the same seam has thin cover on land.

IDEA 3
NAME: Wintering Barge Bunker Swap
MECHANISM: Anchor: a floating hull is the village's coal bunker and feeds the boiler directly; hulls are swapped, so the coal never touches the shore. Keeping hulls dedicated all year costs 5,700 rub/t with used hulls and 27,000 with new ones, against 1,100–3,400 rub/t saved. So the swap uses the river fleet's idle winter instead. The season's last-voyage barge winters at the village berth as a sealed bunker and leaves after ice-out for summer work. In a sealed hold, only about 1,800 m³ of air enters as coal is drawn, so oxidation adds about 0.3 kW on average and self-heating is negligible. The gas that replaces the coal must be flue gas dried to about 0 °C: raw flue gas is wet, and at 6–9% O₂ it is not inert. As coal is drawn, buoyancy pushes up on the ice at about 80 kN/m, which would crack it. A 55 kW heated moat slot around the hull plus 27 kW of hold heat (3.4% of a 2.4 MW boiler, taken from flue-gas waste heat) prevent this. Draft limits capacity: at 1.2 m of water a 1,500-t hull carries only about 660 t.
VALUE: About 1,360 rub/t where a natural backwater lies within about 150 m of the main boiler. The costs it avoids are transshipment, rehandling, trucking and 5–15% stockpile loss, together 1,100–3,400 rub/t (0.8–2.5×). It loses money if a basin has to be dredged (2,226 rub/t) or a heat main is needed (+1,440 rub/t).

IDEA 4
NAME: Ice-Deck Borehole Talik Mining
MECHANISM: Anchor: drill from winter lake ice into the sub-lake talik, which is already thawed, and mine the pay by borehole hydraulic mining. That means no thaw (saves 90 MJ/m³, about 25 kWh/m³), no dike, no drainage and no stripping. Repair: 1.2 m of ice carries only ~25 t of parked load, so the ice is flood-thickened to ≥1.8 m (Gold's formula at A=3.5 kg/cm² gives 113 t short-term, ~57 t parked). The 20-25 t modules sit more than 57 m apart, and the casing is insulated where it passes through the ice. Loose saturated talik gravel holds no roof and caves into the cavity, so the method is limited to narrow (25-40 m), deep, fine-gravel buried channels (<15 cm, the intake limit). Holes go on an 18 m grid (jet reach R=9 m) and are airlifted at 20-40 m³/h. Drawing stops at D≈3.4-3.9 m³ drawn per m³ of pay, set by on-ice jig grade monitoring; this extracts 86-89% of the pay in each hole's footprint, and tailings go back down mined holes. Cost: 1,130-1,970 rub per m³ drawn, which is 3,000-4,800 rub/g of gold recovered.
VALUE: Recovers gold from narrow, deep sub-lake channels that today go unmined, at 3,000-4,800 rub/g. The cheapest alternative, a summer pontoon suction dredge, costs ≥8,800 rub/g, so this is 1.8-4.4x cheaper; on channels wider than 80 m it is only 1-1.5x cheaper.

