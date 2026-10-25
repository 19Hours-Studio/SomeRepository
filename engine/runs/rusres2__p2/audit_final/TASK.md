# Task: adversarial review - find what would make these ideas fail or overstate their value

QUESTION: For Yamal, Gydan and Taimyr oil and gas, which changes to shipping, trans-shipment, product form or field sequencing would raise delivered tonnes per year from capacity already built or sanctioned, and cut full cost per tonne delivered to a buyer that can legally pay? The comparison is Yamal LNG, Arctic LNG 2 and Vostok Oil/Vankor. The answer must use only Russian-built hulls, liquefaction trains and equipment (Zvezda, Arctic Cascade/Mix, Kazanskompressormash, Kriogenmash, Power Machines) and must not depend on getting around sanctions.
Cases: Arctic LNG 2 trains 1–3 at Utrenneye; Yamal LNG; Murmansk/Ob LNG concepts; Vostok Oil (Payakha, Bukhta Sever terminal, 30 Mt/y target in H2 2027); Taimyr coking coal from Syradasayskoye via Dikson, which shares the Kara Sea route, icebreakers and season.
A good answer: (a) full cost per tonne delivered, including idle sunk capex, trans-shipment and buyer discount (Arctic LNG 2 cargoes sell 30–40% below market); (b) years to first delivered cargo or added cargo; (c) utilisation of built capacity, Kara Sea and Ob Gulf operating days per year for each hull class, and life of pads and pipelines on ice-rich Yamal ground.
The binding constraint to attack: Ice-class hulls (2 Arc7 LNG carriers available to Russia, 21 contracted), winter access to the Ob Gulf, which only Arc7 ships can reach, and legal access to buyers (EU LNG ban and EU tanker and icebreaker service bans from 2027; Rosneft on the US SDN list since Oct 2025).
This is part 2 of 3 of a larger question (context, not instructions): Russia wants to develop and extract minerals and energy in its permafrost regions at the lowest full cost, in the shortest time from investment decision to first production, and with the highest effectiveness. Effectiveness means resource recovery, working time across the year, and how long infrastructure lasts on thawing ground. All three are measured per unit of product delivered to the buyer. T

Below are 2 ideas, already repaired once against reality by a researcher. Your job is to be the toughest competent
outside reviewer: an engineer who will lose money if any of these claims is wrong. You do NOT fix or improve the
ideas; you find their defects, prove each one with a number, and rank them.

You have tools: WebSearch/WebFetch and Bash with python3 (check every claim in real code). Work only in
`/home/user/SomeRepository/engine/runs/rusres2__p2/audit_final/`: read no other files in the repository, do not modify other files, do not commit.

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

THE 2 IDEAS:
IDEA 1
NAME: Size Sever to hulls
MECHANISM: The anchor is unchanged: each month Bukhta Sever receives only what the Russian-built Arc hulls can lift, about 1.54 Mt/y per 69 kt hull on the 15.5-day Murmansk cycle (1.2 Mt/y if winter stretches the cycle to 20 days). The allocation is reversed. Vankor-cluster oil (about 11.6–12.3 Mt in 2026–27) stays on the existing Vankor–Purpe line. That line is rated 25 Mt/y and has 12.7–13.4 Mt/y spare. The oil goes to the export outlet it already sells to, not to domestic refineries, which are already crude-long. South is the cheaper margin: about $57/t to an Asian buyer via Transneft and Kozmino, against about $86/t north via Sever, Murmansk and Suez. The north carries only Payakha oil, and Payakha drilling is scheduled to Zvezda Arc hull deliveries, so no well is drilled whose oil cannot be lifted. Because of that, no surplus ever has to go south and the Payakha–Vankor segment never needs reverse flow.
VALUE: Delivered cost per tonne falls by about $29/t on every Vankor tonne kept south, and holding back 15–25 Mt/y of Payakha capacity by 2–3 years saves $2.4–5.8bn in present value. That is about $80–190 per tonne of the capacity deferred, against the published plan of 30 Mt/y in H2 2027, which needs about 19 hulls that do not exist.

IDEA 2
NAME: Legality-split hull-day swing
MECHANISM: The anchor is unchanged: ice-class hulls stay on the short ice leg wherever a lawful onward hull exists, and train output is set by hull-days. The design now splits cargo by legal status. From 1 Jan 2027 the EU ban removes Zeebrugge and about 15 Mt/y of EU sales. Yamal LNG (not on the US SDN list) would then run its 15 existing Arc7s as a winter shuttle from Sabetta to a Kildin ship-to-ship (STS) transfer point near Murmansk, not the Saam FSU, whose owner is on the SDN list. Clean non-EU conventional hulls take the cargo on to Asia. In summer the fleet splits into 40 direct NSR-east cargoes plus 64 shuttle cargoes. Winter needs only 9.7–11.4 of the 15 hulls, so all 19.7 Mt/y is delivered, against 7.4 Mt/y if the Arc7s carry every cargo to Asia themselves. Arctic LNG 2 cargo has no lawful onward hull, so it moves only on Russian-built Zvezda Arc7s delivering straight to the Chinese buyer (0.49 Mt per hull per year). Train 1 runs at the rate those hulls allow, a 30% duty factor with 4 hulls, and Trains 2–3 become a spares pool. Train 3 is not commissioned.
VALUE: Yamal LNG's full cost falls from about $657/t to about $387/t delivered (ratio 0.59) against realised prices of $442–494/t. Arctic LNG 2 earns about $110–160/t in cash on each delivered tonne, but its full cost (about $1,216/t with 4 hulls) stays far above price until about 33 Zvezda hulls exist.

