# Task: adversarial review - find what would make these ideas fail or overstate their value

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 4 ideas, already repaired once against reality by a researcher. Your job is to be the toughest competent
outside reviewer: an engineer who will lose money if any of these claims is wrong. You do NOT fix or improve the
ideas; you find their defects, prove each one with a number, and rank them.

You have tools: WebSearch/WebFetch and Bash with python3 (check every claim in real code). Work only in
`/home/user/SomeRepository/engine/runs/permafrost/genius/audit_evo_1/`: read no other files in the repository, do not modify other files, do not commit.

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
NAME: Self-Detaching Thaw-Face Stripping
MECHANISM: Anchor kept: excess pore pressure at the thaw front of ice-rich muck carries the thawed layer downslope into the mined cell by gravity. The mechanism checks out: R = α/(2√cv) is 0.9-1.6, which puts the frictional sliding threshold at about 2-5°. The original layout fails, though: with 0.5-2 kPa of cohesion, a whole surface graded at 5-8° only slides once the sheet is 1.9-12 m thick, more than the 1.6 m that thaws in a season. Repaired design: cut long, south-facing faces at 10-12° and sprinkle them with creek water. Sheets 0.2-0.9 m thick then detach several times a season, which keeps the face bare and thawing about 3 m per season. Each metre of face yields 115-138 m³ per season, so 0.5 Mm³ needs about 4 km of face. The slurry (yield stress under 500 Pa) runs down the roughly 4° drop into the adjacent mined cell and settles to 0.64 of its frozen volume. Stripping has to start 4-9 seasons ahead of mining.
VALUE: Stripping drops from about $1.0/m³ (natural thaw plus dozing) to about $0.3/m³, 3× cheaper. That cuts delivered gold cost by about 15% in ordinary muck and by up to about 40% in Yedoma (over 60% ice), where dozers bog down and the alternative is digging frozen ground at about $3.5/m³.

IDEA 2
NAME: Reservoir-Talik Tributary Dredging
MECHANISM: Anchor: placers drowned under a Far-North hydro reservoir get thawed by the water above them, so they can be mined from open water with no stripping-by-thaw, pond building or ice sawing. Reality check: after 40 years a 1-D enthalpy model gives a talik of only 5.8/8.5/10.8/12.5 m for mean bottom water at 1/2/3/4 °C, so the "whole floor thawed" claim is false for deep main-valley sections. The repaired design targets drowned tributary mouths with total sections of 8 m or less and an overburden:pay ratio of 2 or less, on the 130 km² band 1.5-25 m below the minimum operating level (UMO, 432 m). It uses an electric 600 m³/h submerged-pump cutter dredge fed from the Kolyma HPP grid, starts at ice-off when the reservoir is at its lowest, and discharges tailings below the surface into the mined-out cut. That discharge keeps fines escape under the 0.5-1.3 % that the fishery limit allows; at 5 % escape the plume would add 1.0-2.6 mg/L. Modelled cost is 526-683 rub/m³ of section (1.2 Mm³ per 120-day season).
VALUE: It adds a resource that is now sterilised, at roughly the same cost as open-cut placer gold (0.7-1.0× of 1,050-2,000 rub/g at the same section), not several times cheaper.

IDEA 3
NAME: Re-Floatable Pond-Moored Mine Plants
MECHANISM: Anchor kept: the concentrator, power house and camp float on hulls built in a shipyard, in a pond dug at the site, so the talik their heat creates does not matter. The pond is 6 m deep (2.2 m of maximum ice, 3 m of draft and a margin). Waste heat keeps a 2 m moat open around each hull against ice pressure, using 0.9-1.6 MW of the roughly 35 MW the power house rejects. Mills stand on bedrock 20-50 m back from the edge to allow for 0.5-2 m/yr of bank retreat. The hulls (130×14 m, 3 m draft, about 2.9 kt payload each) fit the 135×14.3 m White Sea-Baltic canal locks. Against the best current practice, a modular plant on piles, a cold-permafrost site gains nothing (capex +4%). The anchor pays off in one regime: warm, ice-rich ground where foundations are 20-25% of capex, cheap $3k/t barge hulls, and short-lived (5-7 year) riverside or coastal deposits. There the plant is re-floated and towed to the next deposit, keeping 45-55% of its value.
VALUE: In that regime capex is 15-19% below a modular plant on piles and delivered cost 10-14% lower. On ordinary cold permafrost the gain is about 0%.

IDEA 4
NAME: Bluff-Anchored Barge Coal Augers
MECHANISM: Anchor: a floating highwall auger drills a frozen river-bluff coal seam at summer water level and loads straight into the hold, so no rock is moved. A cycle model of a 1.8 m × 100 m hole (331 t) gives 33-53 t/h, so a 20 kt season is 60 holes, 26 days and 145 m of bluff; the original 40 t/h claim holds. Repairs: the 300 kN thrust goes into two adfreeze anchors in the frozen bluff (283-424 kN each) instead of spuds (about 100 kN usable each). Webs are 0.6 m where cover is up to 30 m and 0.9 m deeper (unfrozen safety factor 3.1/1.5/0.9 at 15/30/50 m with 0.6 m webs). A ±3 m adjustable frame gives a 60-120 day water-level window against the 26 days needed. Hole mouths are plugged afterwards against oxidation. One barge must serve at least about 60 kt/yr on one river system; one village alone costs about 6,500 rub/t.
VALUE: About 3,200 rub/t delivered to the village shore against 5,300-10,300 rub/t for long-haul river coal and 3,700-7,400 rub/t for a micro-pit plus winter road (1.2-3.2× cheaper).

