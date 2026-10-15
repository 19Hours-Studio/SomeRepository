# Task: adversarial review - find what would make these ideas fail or overstate their value

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 4 ideas, already repaired once against reality by a researcher. Your job is to be the toughest competent
outside reviewer: an engineer who will lose money if any of these claims is wrong. You do NOT fix or improve the
ideas; you find their defects, prove each one with a number, and rank them.

You have tools: WebSearch/WebFetch and Bash with python3 (check every claim in real code). Work only in
`/home/user/SomeRepository/engine/runs/permafrost/round2/critic_b/`: read no other files in the repository, do not modify other files, do not commit.

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
IDEA 1 (mean originality 7.5/10, mean feasibility 5.0/10)
NAME: Spring Sun-Wind Deflation Placer
MECHANISM: Anchor: the cold, dry wind freeze-dries frozen pay gravel by sublimation and blows away the freed silt and light sand without any liquid water, leaving gold, cassiterite and other heavies behind as a lag. In midwinter Yakutia this runs at only 0.014-0.041 mm w.e./day, which frees 0.05-0.15 mm/day of gravel, so the design moves to the windy Arctic tundra in spring (Mar 15 to about May 10), when sun falling on dark, harrowed, still-frozen gravel drives 0.4-0.7 mm w.e./day, freeing 2.5-5 mm/day. Pay gravel is worked in place, either on the stripped cut whose active layer was drained by ditches in autumn (pore ice 0.15 instead of 0.30) or on old tailings dumps, which need no stripping at all. That removes 0.21 m per year, so 100,000 m³ a year needs about 0.5 km². A daily harrow-and-rake pass windrows the lag. Harrowing is done only when the 10 m wind is 7-8 m/s or less: at 7 m/s quartz from 25 to 500 µm leaves and no gold moves. The dry -10 mm residue is about 25% of the volume and is washed clean in a few summer weeks.
VALUE: In place on thin-overburden placers or old tailings, digging, feeding and washing cost about $1.7/m³ against about $6.0/m³ for summer washing today (3.6x cheaper); on a pad for thick virgin pay the gain is only 2.1x.

IDEA 2 (mean originality 6.0/10, mean feasibility 5.5/10)
NAME: Self-feeding ore-ice buttress dam
MECHANISM: Anchor: the frozen ore pile itself holds the water, and stored warm water run over its bare downstream face melts the ice cement at a rate set by the flow, so the dam doses its own gravel into a riffled chute. Calculation confirms the self-dosing: releasing 1 m³ of ice-cemented gravel takes 101 MJ, which is 4.3-7.6 m³ of 8 °C water, inside the normal sluicing range (a working placer uses 2.2 m³ per m³). The face can transfer heat 20-100x faster than needed, so feed really does equal flow times water temperature. The repair splits the structure into two parts. One is a permanent frozen core under 0.8-1.0 m of saturated peat (it thaws only 0.5-0.6 m per summer). The other is a sacrificial ore buttress downstream, 75 m thick and retreating 0.8 m a day. Creek baseflow (about 47 L/s for 60,000 m³ a season) passes through a small forebay instead of a season-long reservoir, which cuts the dam-break peak from 460 to 128 m³/s. It is used where it is strongest: winter (underground) placer mining, where the hoist already builds a frozen stockpile that today has to be thawed with steam or sprinkling, ripped and fed by dozer.
VALUE: For winter-mined placers the summer washing stage drops from about $6.7 to about $1.3 per m³ (5x cheaper), with no feed dozers, pumps or ripping; for summer-mined gravel built up in autumn the gain is only 2.2x.

IDEA 3 (mean originality 6.0/10, mean feasibility 5.5/10)
NAME: Freeze-and-float boulder pond
MECHANISM: Anchor kept: a pond over the placer lets winter bottom-fast ice freeze onto the stones, and the spring water rise floats the ice off with the stones in it. The in-place sorting part fails by orders of magnitude. Pond waves give a bottom orbital velocity of only 0.03 m/s at 1 m depth, and the pore flow they pump is 6×10⁻⁴ m/s against the 0.02-0.1 m/s needed to fluidise (jig) the gravel. Fines leaving over the spillway would take 2,000-11,000 years, so that part is dropped. The repaired design times the pond depth so the ice (natural 1.6-1.8 m, or 3.1-3.3 m when built up by flooding the ice surface) reaches the boulder tops only in March, while the summer-thawed talik below stays unfrozen. Each m² of floe then lifts 0.08-0.17 m³ of stone a year, and a tractor winch, not the wind, drags the floes to a dump bay. The pond's 1.4-2.2 m of summer thaw prepares the ground.
VALUE: Clearing boulders by ice costs about $1/m³ of boulder against about $6/m³ to drill, blast and doze them (roughly 6x cheaper), which opens bouldery placers that dredges reject; overall washing is only 1.25-1.5x cheaper, so this is a niche.

IDEA 4 (mean originality 6.5/10, mean feasibility 4.5/10)
NAME: Trimmed snow-buoyed under-ice ore pods
MECHANISM: Anchor: crushed ore plus dry snow sealed in an ice shell, carried by the current under the winter river ice to a downstream slot, with no vessel and no return trip. Snow needed per tonne is 0.28 m³ for coal, 0.74 for rock ore and 0.86 for sulphide ore. The original strongly buoyant pods fail: pressed against ice near 0 °C (μ about 0.5 at slow speed), a 1 t pod at 0.1-0.3 m/s can carry only 1-12 kg of net buoyancy before it stalls, and a stalled pod freezes into the ice cover at 1-2 cm/day. The repair uses 10 t broadside "fin" pods (5.0 × 2.2 × 1.2 m), soaked to 0 °C and trimmed in the launch slot with a crane load cell to +3 to +9 kg net buoyancy. That keeps drag (about 170 N at 0.16 m/s) larger than buoyancy, so pods dive under ice roughness instead of sticking. Routes are limited to reaches with smooth thermal ice and under-ice velocity of at least 0.2 m/s, mainly regulated rivers below hydropower dams (Kolyma, Vilyuy, Yenisei). An 8-10 cm shell survives transit (6 cm melt in 45 days), 700 km takes 41-68 days, and a pair of slots moves 1,200 t/day, or 144 kt per season.
VALUE: Handling costs about $7.3/t including 5% lost pods, against $59-176/t by winter road over 500-1,500 km (8-24x cheaper) and 1.7-5x cheaper than summer barges, with coal as the best cargo.

