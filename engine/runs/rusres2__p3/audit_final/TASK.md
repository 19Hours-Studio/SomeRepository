# Task: adversarial review - find what would make these ideas fail or overstate their value

QUESTION: For the producing Norilsk/Taimyr nickel-copper-PGM complex, which changes to mining or development order, processing of lower-grade and disseminated ore, equipment substitution, or foundation design and monitoring would cut full cost per tonne of nickel-equivalent delivered and raise recovery and structure life? The comparison is the current Norilsk practice (Talnakh concentrator expansion, Sulphur Programme), Raglan and Kiruna/Aitik. It must not overstate thaw where engineering faults (Ambarnaya, the 2021 concentrator collapse) were the cause.
Cases: Talnakh/Oktyabrskoye rich and cuprous ore; Norilsk-1 disseminated ore; Maslovskoye (low grade, rich in PGM); Nadezhda and Talnakh processing; Dudinka-Murmansk delivery; ageing industrial and residential structures on Norilsk ground.
A good answer: (a) full cost per tonne of nickel-equivalent delivered, where capital is about 37% of the total and foundation losses about 1–2%; (b) years from investment decision to added output or capacity, against Talnakh modernisation (47bn RUB for +34%) and the Sulphur Programme's slip of at least 2 years; (c) recovery for each ore type, plant availability, and design life of foundations against the 1 cm/yr deepening of thaw and Nornickel's thermometric borehole forecasts to 2050.
The binding constraint to attack: Sustaining and processing capital with foreign contractors and equipment gone (Sulphur Programme cost +40–70%), falling grade as Maslovskoye and disseminated ore come in, and the life of structures where maintenance and design faults count as much as thaw.
This is part 3 of 3 of a larger question (context, not instructions): Russia wants to develop and extract minerals and energy in its permafrost regions at the lowest full cost, in the shortest time from investment decision to first production, and with the highest effectiveness. Effectiveness means resource recovery, working time across the year, and how long infrastructure lasts on thawing ground. All three are measured per unit of product delivered to the buyer. T

Below are 2 ideas, already repaired once against reality by a researcher. Your job is to be the toughest competent
outside reviewer: an engineer who will lose money if any of these claims is wrong. You do NOT fix or improve the
ideas; you find their defects, prove each one with a number, and rank them.

You have tools: WebSearch/WebFetch and Bash with python3 (check every claim in real code). Work only in
`/home/user/SomeRepository/engine/runs/rusres2__p3/audit_final/`: read no other files in the repository, do not modify other files, do not commit.

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
NAME: Gate Talnakh-3 on refill
MECHANISM: Anchor: the third Talnakh complex (TOF-3) is approved only together with a costed plan to refill the Norilsk concentrator (NOF) capacity it frees, and the pair is judged on full cost per added tonne of recovered Ni-eq. Ni-eq here counts PGM, not just Ni. The repaired refill is Norilsk-1 disseminated ore (+4 Mtpa, toward the 7 Mtpa already planned) plus a costed NOF life-extension package. That package keeps the new 9 Mtpa disseminated-ore concentrator deferred, and Maslovskoye comes second. In Ni-eq Maslovskoye is 2.66% (about 76% of its value is PGM), the same as Talnakh ore and 1.6× Norilsk-1, so the earlier "600k RUB per tonne Ni" ranking was wrong. Base case: the pair adds about 96 kt Ni-eq/yr at about $6,800/t, against $7,900/t for Nornickel's plan to build the new concentrator now (median ratio 0.88, range 0.76–1.00). If the Talnakh mines cannot supply extra ore, TOF-3 alone just moves ore and gains about 6 kt/yr from better recovery, at $26,800/t. The gate then reverses the decision: the pair costs $9,700/t and the plan $11,800/t. XRT sorting is kept only as an option once NOF is full. It pays only if the sorter keeps at least about 97% of the metal (+7–13 kt/yr at $7,400–10,200/t).
VALUE: The pair costs about 0.82–0.88× the best real alternative per added tonne of Ni-eq. Where TOF-3 would only move ore, it avoids a step costing 2.8× more per tonne, and it saves about 65 bn RUB of upfront capex (base case) while foreign equipment is unavailable.

IDEA 2
NAME: Availability as capacity
MECHANISM: Anchor: one parts registry pools spares across the Western-built underground fleet, ranks failure modes by Ni-eq tonnes lost, and sends the worst part families to domestic reverse-engineering and casting first. The stock is re-optimised every quarter from measured mean time between failures (MTBF). With 6 mines and a 9-month grey-import lead time, a pooled stock is 46–62% the size of separate site stocks for the same service. With the same budget, the chance a part is on hand when needed rises from 80% to 99.5% (Poisson model). Ranking by Ni-eq sends the first effort to the rich-ore fleets: one lost LHD-hour there costs about 6.3 t Ni-eq, against 1.2 t on Norilsk-1 ore (5.2×). That makes the programme 1.7× more effective than ranking by machine-hours. Base case: availability rises about 7 percentage points, output by about 29 kt Ni-eq/yr (3.6% of the group), at about $2,700 per added tonne. Gains count only while the mines, not the concentrators, are the limit (taken as 60%). It breaks even if domestic parts last at least 0.30× as long as the original parts.
VALUE: Each added tonne costs about $2,700, roughly 0.35× the $7,300–8,100 of a brownfield capacity stage. Group full cost falls about 2.6% within 6–18 months, which is real but not a 1.5× cut.

