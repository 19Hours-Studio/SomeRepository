# Task: adversarial review - find what would make these ideas fail or overstate their value

QUESTION: Russia wants to develop and extract minerals and energy in its permafrost regions at the lowest full cost, in the shortest time from investment decision to first production, and with the highest effectiveness. Effectiveness means resource recovery, working time across the year, and how long infrastructure lasts on thawing ground. All three are measured per unit of product delivered to the buyer. The scope covers:
- Hard-rock and placer metals: Norilsk and Taimyr nickel, copper and platinum-group metals; gold in Yakutia, Magadan and Chukotka; Udokan and Baimskaya copper; Tomtor rare earths.
- Diamonds in Yakutia, plus the Arkhangelsk deposits (see CORRECTED).
- Coal in Taimyr, Elga and the rest of Yakutia.
- Oil and gas in Yamal, Gydan and Taimyr.
The whole chain counts: choosing and exploring deposits, building and powering sites, mining or drilling, processing, staffing, and delivering the product. The conditions are:
- Permafrost that is thawing under a warming climate.
- Extreme cold, with short building and shipping seasons.
- Long distances with no roads or railways.
- Ice seasons on the Northern Sea Route (NSR) and the rivers.
- A shortage of workers.
- Expensive energy at remote sites.
- Restricted access to imported mining, drilling and LNG equipment and software since 2022.
What changes to any stage, or to the order in which deposits are developed, would beat the best current practice in Russia and in comparable cold regions (northern Canada, Alaska, Greenland, northern Scandinavia)?
A good answer: 
- Each proposal states its effect, with an estimate and its basis, on three measures: (a) full cost per unit delivered (annualised capital plus operating plus logistics); (b) years from investment decision to first production; (c) effectiveness (recovery, days worked per year, infrastructure life on thawing ground).
- Each proposal is compared with a named benchmark, either Russian (e.g. Yamal LNG, Norilsk, Vankor/Vostok Oil, Kupol/Pavlovskoye, Nord/Elga) or foreign (e.g. Canadian Arctic mines such as Raglan and Diavik, Red Dog in Alaska, Kiruna/Aitik, Greenland).
- It names which deposits or stages it applies to and which it does not.
- It states what physical law or measured data it relies on.
- It lists the equipment or technology by its domestic maker or unrestricted supplier.
- It includes the main risks and how to test the idea within 3–7 years.
Constraints: 
- It must obey known physics.
- It must be deployable within 3–7 years.
- It may use only equipment and technology Russian operators can get from domestic makers or from suppliers not restricted for them.
- It must not depend on ways around sanctions.

Below are 6 ideas, already repaired once against reality by a researcher. Your job is to be the toughest competent
outside reviewer: an engineer who will lose money if any of these claims is wrong. You do NOT fix or improve the
ideas; you find their defects, prove each one with a number, and rank them.

You have tools: WebSearch/WebFetch and Bash with python3 (check every claim in real code). Work only in
`/home/user/SomeRepository/engine/runs/rusres/audit_final/`: read no other files in the repository, do not modify other files, do not commit.

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
NAME: Fuel on empty coal-barge legs
MECHANISM: Anchor: one Kolyma flow rides on the other flow's empty leg. The data reverse the direction. Only about 3 kt of dry cargo goes upstream against 165 kt of coal coming down, so at most 1.8% of the coal could ride on returning barges. The ~165 coal-barge legs going back upstream empty are the real spare capacity. About 17 kt/yr of Northern Delivery fuel would ride those legs in 42 t collapsible fuel bladders, with the coal hold acting as spill containment. That needs 17 of the 165 legs, about 100 bladders and 24 per shoal-limited 1,000 t leg.
VALUE: About 2,100 rub/t for the river leg against 2,700–12,000 rub/t for a dedicated 38–54-year-old tanker (1.3–5.7x). That is under 10% of the delivered diesel price. The real value is not having to replace the tanker fleet.

IDEA 2
NAME: Shaft-bottom XRT sorting, hoist-bound mines
MECHANISM: Anchor: domestic X-ray transmission (XRT) sorters at the shaft bottom reject waste lumps before hoisting, and the rejects go straight into stope backfill. The repair moves it from "freeing concentrator capacity" to deep mines where the 2.1 km shafts set the limit, such as Skalisty and the Talnakh/Oktyabrskoye deep levels. There every tonne of waste rejected below ground is replaced by ore in the fixed skip capacity. With the fines (about 35% of ore) bypassing the sorter, metal hoisted per year rises ×1.095 at Selebi-type results (15% rejected, 2% metal lost) and ×1.36 at stringer-type results (44%, 4%). After counting the metal lost for good in the backfill, metal NPV is still ×1.085–1.31 over a 30-year reserve at 14%. Two or three 150 t/h units cover 2 Mt/yr hoisted. Rejects of at most 0.41 t per t of ore fit in the backfill needed (0.44–0.67 t per t), so no tailings go to the surface. The design is restricted to cuprous/stringer and massive ores at contacts. Disseminated Norilsk-1 and Maslovskoye ore is left out (16% metal loss at 23% rejection on disseminated test ore), as are mines where hoisting is not the limit.
VALUE: Each extra tonne of Ni-eq from a hoist-bound deep mine costs $5.0–8.3k by sorting against $6.7–12.6k from a new deep shaft, 1.2–1.8× cheaper. It comes in about 2–3 years instead of about 10 years of shaft sinking.

IDEA 3
NAME: Hull-paced domestic Arctic Cascade trains
MECHANISM: The anchor is unchanged: copy the domestic 0.9 Mtpa Arctic Cascade Train 4 many times instead of building 6.6 Mtpa trains that need imported or first-of-kind drives. In the repaired design, trains are added only at Sabetta and only as fast as Arc7 hulls arrive. Each train needs about 0.55 hull: a hull carries about 1.63 Mt/y when it runs 150 days a year east on the NSR and spends the winter shuttling 12-day round trips to the Saam/Ura FSU near Murmansk. In winter this shuttle replaces the 20-day Zeebrugge run, which the EU bans from 2027. With this matching, all added output can be shipped year-round, which fixes the kill metric. The trains have two roles. First, they are a domestic-drive hedge for the Nuovo Pignone strings on Trains 1–3: each 1% of availability lost there is 0.165 Mt/y. Second, they are the growth path once Arctic LNG 2's idle 13.2 Mtpa is full. That needs about 8 hulls, so it happens around 2030–33 at 1–2 hulls a year from Zvezda. No new trains go to Utrenneye before then.
VALUE: Full delivered cost is about $236/t, against $295/t for a Yamal T1–3-type train (1.25x) and $257/t for a large domestic-drive train (1.09x). First LNG is about 3 years after the decision for a series copy, against 4–4.5. But it is 1.5x worse than simply filling Arctic LNG 2's idle trains, which is why it is held back until those are full.

IDEA 4
NAME: Pre-staged flood-crest barges
MECHANISM: Anchor: a loaded barge waits out the ice drift in a sheltered backwater and leaves on the flood crest. Repair: load it in autumn while it is still afloat at a deep berth, so nothing is loaded through ice. It winters in a backwater at least 2.5 m deep, and it is used on a tributary that is navigable only on the spring flood, where there is just one trip a year anyway. With a modelled 12-day recession, a convoy arriving 5–10 days late loses 35–62% of its load. A barge pre-staged at the river mouth goes in full.
VALUE: About 3,100 rub/t against 4,700–11,300 rub/t on that leg today (1.5–3.6x). On the Kolyma main stem the gain is only about 14%.

IDEA 5
NAME: Level-crusher conveyor decline for Talnakh
MECHANISM: The anchor is unchanged: crush ore at the level and carry it on a fixed belt, replacing truck haulage. The belt no longer stops at an existing shaft. It runs up a 14° decline all the way to surface, and serves as the hoisting route for the Talnakh concentrator expansion from 10 to 18 Mtpa in place of a new 2.1 km skip shaft. Nornickel's shafts advanced only 150–322 m in 2017, so sinking takes 6.5–14 years, plus about 1.5 years to equip. A 4.1 km decline (1,000 m lift) driven by drill-and-blast from 2–3 headings at 150 m/month takes about 1–2.3 years, plus about 1 year to install the belt. It is lifted by three flights of ST3150 belt (or two of ST5000) at 1,600 t/h, drawing 5.1 MW, or 3.2 kWh/t against 3.4 for a skip.
VALUE: Cost per tonne of ore is $2.9–4.0, against $3.6–5.3 for a new shaft. That is only about 1–2% of full cost per tonne of nickel-equivalent, so the gain is not cost. The gain is ore 4–11 years sooner for 8 Mt/y, worth about $1.5–3.5bn PV. That holds only if hoisting is what limits the expansion.

IDEA 6
NAME: Cold-margin triaged thermosyphon retrofit
MECHANISM: Anchor: borehole temperatures plus InSAR rank existing foundations by remaining pile capacity, and retrofit thermosyphons only on the worst ones, only where the winter is cold enough. The cutoff is now a computed number: the cooling margin M, which is winter heat a unit can pull out of the ground divided by the yearly heat flowing in per pile. In 2050 climate (+2.5 K in winter), M is 1.53 at Norilsk, 2.10 at Udachny/Mirny and 1.57 at Pevek, which pass the M ≥ 1.5 cutoff. It is 1.05 at Salekhard, 0.88 at Nadym, 0.90 at Fairbanks and 0.41 at Beiluhe on the Qinghai–Tibet line, which fail. That ranking matches where cooling was actually seen to fade on the Trans-Alaska pipeline (TAPS) and the Qinghai–Tibet line (F320–321). Triage step 0 is the cheapest fix: reopen crawlspace vents and repair utility leaks. Only structures that keep warming after that get vertical units drilled with low-headroom rigs from the ventilated crawlspace, or inclined units from the outside edge for buildings under about 20 m wide. That is about 50 of the 165 monitored Norilsk/Talnakh structures and about 8,500 units. Each unit finishes cooling the ground to the target in about one winter.
VALUE: It keeps structures on thawing ground in service past 2050 for about $64M, against $198M for retrofitting all 165 structures and $196–392M for new piles to bedrock. That is about 3× cheaper than either. It adds only about $3–19 per t Ni-eq (0.04–0.20% of full cost) and avoids an expected $26–86M/yr of thaw-related losses.

