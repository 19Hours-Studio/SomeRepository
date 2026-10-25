# Task: adversarial review - find what would make these ideas fail or overstate their value

QUESTION: For greenfield metal deposits in north-east Russia that have no grid or road, which changes to power supply, construction method, access logistics or development order would cut full cost per unit delivered and the years from investment decision to first metal? The comparison is Kupol/Dvoinoye, Natalka, Baimskaya's 2020 plan, Red Dog and Meliadine. The answer must use only domestic or unrestricted equipment, and it must work through the period when Bilibino has closed and the floating units are not yet running (2026–2030).
Cases: Baimskaya copper-gold (Pevek/Nagleynyn route, Rosatom floating power units 2028–30); Chukotka and Magadan hard-rock and placer gold (Kupol, Natalka, Kolyma placers); Tomtor rare earths (Rosneft, pilot 2027, Anabar/Lena river access).
A good answer: (a) full cost per oz Au or per t Cu or rare-earth oxide delivered, including annualised external-infrastructure capex; (b) years from investment decision to first production, against Natalka (about 4–5 years, then 2 to full rate) and Baimskaya (end-2027 target, already slipped); (c) recovery, operating days per year, and life of tailings, dams and foundations in discontinuous or warm permafrost.
The binding constraint to attack: Firm power in the 2026–2030 gap (about 8 MW of winter spare in Chukotka), the capex of external road and port (Baimskaya rose from $5.5bn to $8bn, about $600m of it road and port), and short seasonal supply windows (winter roads, Pevek's 4–5-month navigation).
This is part 1 of 3 of a larger question (context, not instructions): Russia wants to develop and extract minerals and energy in its permafrost regions at the lowest full cost, in the shortest time from investment decision to first production, and with the highest effectiveness. Effectiveness means resource recovery, working time across the year, and how long infrastructure lasts on thawing ground. All three are measured per unit of product delivered to the buyer. T

Below are 2 ideas, already repaired once against reality by a researcher. Your job is to be the toughest competent
outside reviewer: an engineer who will lose money if any of these claims is wrong. You do NOT fix or improve the
ideas; you find their defects, prove each one with a number, and rank them.

You have tools: WebSearch/WebFetch and Bash with python3 (check every claim in real code). Work only in
`/home/user/SomeRepository/engine/runs/rusres2__p1/audit_final/`: read no other files in the repository, do not modify other files, do not commit.

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
NAME: Kupol winter-road toll hub
MECHANISM: Anchor: third-party high-grade lodes are developed as mine-only satellites. Their ore goes by winter road to the Kupol mill, which runs on its own diesel plant, so it needs none of the 8 MW the Chaun–Bilibino node has spare. Repaired design: haul radius ≤200 km, head grade ≥4 g/t, and at most 0.5 Mt per winter season per corridor. That cap comes from 12,500 loads in a 75-day season, about 167 a day, which matches the Tibbitt–Contwoyto record. Each satellite runs a domestic RADOS X-ray sorter and ships only the sorted fraction (assumed 65% of mass, 93% of the gold). The first target is Kekura's second-stage ore (7.5 g/t, 160 km west of Kupol). Kekura's feasibility study assumed grid power from Bilibino, which has now closed. Ore is stockpiled frozen at Kupol and milled all year. Haul costs $0.22/t-km, or $177/oz at 7.5 g/t. Avoiding a satellite mill, tailings dam and power plant saves $322/oz. The extra milling adds only about 1.7 MW and 3.4 kt a year of diesel at Kupol.
VALUE: Full cost is $863/oz delivered against $1,018/oz for a stand-alone Kekura-type mill (0.85×), and first gold comes about 2 years after decision against about 4 for the stand-alone mill and 4–5 for Natalka. At 300 km the advantage almost disappears ($20–45/oz).

IDEA 2
NAME: Diesel-sized first line, nuclear expansion
MECHANISM: Anchor: a diesel-sized starter on leased domestic or unrestricted gensets comes first. The nuclear-sized expansion follows when the floating units deliver, and the gensets then move to other sites. Repaired design: the starter is no longer a separate 6 Mt/y plant. That version still fails: $8.3k/t Cu net against $2.0k/t for the full plan, and a $45m a year margin on $1.08bn of capex. Instead, line 1 of the Baimskaya plant now under construction (start planned for end-2028) runs at a throughput sized to 80 MW of leased gensets. It uses the SAG mill and one of two ball mills at a coarser grind, on the highest-grade benches. That gives 15 Mt/y of ore at about 0.51% Cu (the first-decade head implied by the feasibility study), 67 kt Cu and 98 koz Au a year. It burns 117 kt of diesel a year at $0.30/kWh, which takes 6 tanker calls into Pevek and needs 174k m³ of tankage. With fuel coming in and concentrate going out on the same trucks, that is about 7,000 loads a year: 20 a day on the all-season road, or 78 a day on a winter road alone. Net cash cost is $1.95k/t Cu after gold credit. Line 1 is also commissioned on diesel, so the ramp-up is done before the reactors arrive.
VALUE: Each year the floating units slip, the bridge earns about $0.52bn of cash margin ($0.29bn at Cu $8k / Au $2.8k) from a plant whose $8bn would otherwise cost about $1.2bn a year to carry idle. Waiting idle earns nothing in those years.

