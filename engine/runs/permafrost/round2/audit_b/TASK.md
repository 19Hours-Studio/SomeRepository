# Task: adversarial review - find what would make these ideas fail or overstate their value

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 12 ideas, already repaired once against reality by a researcher. Your job is to be the toughest competent
outside reviewer: an engineer who will lose money if any of these claims is wrong. You do NOT fix or improve the
ideas; you find their defects, prove each one with a number, and rank them.

You have tools: WebSearch/WebFetch and Bash with python3 (check every claim in real code). Work only in
`/home/user/SomeRepository/engine/runs/permafrost/round2/audit_b/`: read no other files in the repository, do not modify other files, do not commit.

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

THE 12 IDEAS:
IDEA 1
NAME: Self-feeding ore-ice buttress dam
MECHANISM: Anchor kept: the frozen ore pile holds the forebay water, and warm water run over its downstream face thaws it, so feed = flow × ΔT / thaw energy. The regime where this is strongest is a loose winter-hoisted pile (bulk ice 0.15, 50-55 MJ/m³). With creek or forebay water at 5-7 °C it needs 2.2-3.2 m³ of water per m³, which matches what a sluice needs (about 3 m³/m³). The original ice-cemented pile (101 MJ/m³) needs 3.8-8 m³/m³ and is water-limited. A loose pile leaks: its cold content refreezes only 5-16% of its voids. The repair is a 3 m upstream ore skin, spray-sealed in winter (a 0.4 m lift freezes in 10-19 h), under a 0.8-1 m saturated-peat blanket that thaws only 0.42 m in 90 days. The forebay is kept at 3 m or less (sliding safety factor about 5, Froehlich breach peak 34 m³/s against 144 m³/s for a season-long reservoir). Above 8-9 °C cold creek water is blended in, because the water ratio would otherwise fall below 2. The face can thaw about 70 m/day, against the 0.8 m/day needed.
VALUE: Summer washing of winter-mined stockpiles costs about $2.0/m³ ($2.95/g at 0.8 g/m³) against about $4.65/m³ ($6.8/g) for natural thaw plus dozer ripping plus loader plus pumped sluice, or for hydromonitor plus gravel pump, so 2.3x cheaper (not 5x).

IDEA 2
NAME: Solar-pond self-dosing ore pile
MECHANISM: Anchor kept: the frozen ore pile feeds itself. Warm water thaws its face at a rate set by flow × water temperature, so the feed needs no dozer. Two changes from the original: the 1-2 mm film spread over a 40-100 m face is replaced by a channel along the toe of the face, and the ore pile no longer holds back water. In the toe channel, 47-100 L/s at a slope of 0.05-0.08 gives 30-57 Pa of shear, which clears clasts finer than 42-78 mm. The water gives up its heat within e-folding lengths of 10-31 m, so feed still equals flow × heat. Water comes by gravity from a lined solar pond, 0.4 m deep and 0.7-1.5 ha, that warms the creek by 4-6 K. Season output is about 123,000 m³ with the pond, against 54,500 m³ from a 4 °C creek. A fixed weir bypass keeps the chute at 4 m³ of water per m³ or more, while the face alone swings from 2.4 to 12.1. A grizzly and a loader (2-3 h a day) remove the oversize.
VALUE: Feed dozing, ripping and pumping drop out of the washing stage at winter-mined placers. Per recovered gram this is only 1.03-1.13x cheaper than today's stockpile thawing and dozer feed.

IDEA 3
NAME: Trimmed snow-buoyed under-ice ore pods
MECHANISM: Anchor: crushed ore plus dry snow sealed in an ice shell, carried by the current under the winter river ice to a downstream slot, with no vessel and no return trip. Snow needed per tonne is 0.28 m³ for coal, 0.74 for rock ore and 0.86 for sulphide ore. The original strongly buoyant pods fail: pressed against ice near 0 °C (μ about 0.5 at slow speed), a 1 t pod at 0.1-0.3 m/s can carry only 1-12 kg of net buoyancy before it stalls, and a stalled pod freezes into the ice cover at 1-2 cm/day. The repair uses 10 t broadside "fin" pods (5.0 × 2.2 × 1.2 m), soaked to 0 °C and trimmed in the launch slot with a crane load cell to +3 to +9 kg net buoyancy. That keeps drag (about 170 N at 0.16 m/s) larger than buoyancy, so pods dive under ice roughness instead of sticking. Routes are limited to reaches with smooth thermal ice and under-ice velocity of at least 0.2 m/s, mainly regulated rivers below hydropower dams (Kolyma, Vilyuy, Yenisei). An 8-10 cm shell survives transit (6 cm melt in 45 days), 700 km takes 41-68 days, and a pair of slots moves 1,200 t/day, or 144 kt per season.
VALUE: Handling costs about $7.3/t including 5% lost pods, against $59-176/t by winter road over 500-1,500 km (8-24x cheaper) and 1.7-5x cheaper than summer barges, with coal as the best cargo.

IDEA 4
NAME: Sun-face windrow freeze-dry placer
MECHANISM: Anchor kept: sun and wind sublimate the ice cement of frozen pay with no liquid water, and wind carries off the freed fines while gold stays. In the repaired design, drained pay is piled in autumn into windrows with 37° south faces (~0.06 pore ice instead of 0.15-0.30). The faces shed snow, clear themselves of loose grains, and get 2.6x the irradiance of flat ground. Sorting no longer relies on a threshold window. The saltating sand and any mobile gold (up to ~100-200 µm) settle in the trough between ridges. Only the suspended fraction leaves the site: quartz finer than 63-97 µm and gold finer than 23-35 µm. An hourly energy balance for Tiksi gives a face sublimation of 0.08-0.13 kg/m²/day in March and 0.41-0.67 in April 1-20. The window closes on Apr 20 because faces reach -2 °C or warmer after that. A 0.5 mm dry skin halves the rate and a 3 mm lag cuts it 6x. The season totals 5.2 kg/m², so faces retreat only 0.02-0.09 m.
VALUE: 100,000 m³/yr needs about 0.9 km² raked daily or 213 km of ridges, at $4.4-12.1/m³ ($7.4-20.3/g) against $1.7-6.0/m³ ($2.9-10.1/g) for conventional washing. That is about 0.5x, so it costs more, and only a small niche at waterless sites remains.

IDEA 5
NAME: Spring Sun-Wind Deflation Placer
MECHANISM: Anchor: the cold, dry wind freeze-dries frozen pay gravel by sublimation and blows away the freed silt and light sand without any liquid water, leaving gold, cassiterite and other heavies behind as a lag. In midwinter Yakutia this runs at only 0.014-0.041 mm w.e./day, which frees 0.05-0.15 mm/day of gravel, so the design moves to the windy Arctic tundra in spring (Mar 15 to about May 10), when sun falling on dark, harrowed, still-frozen gravel drives 0.4-0.7 mm w.e./day, freeing 2.5-5 mm/day. Pay gravel is worked in place, either on the stripped cut whose active layer was drained by ditches in autumn (pore ice 0.15 instead of 0.30) or on old tailings dumps, which need no stripping at all. That removes 0.21 m per year, so 100,000 m³ a year needs about 0.5 km². A daily harrow-and-rake pass windrows the lag. Harrowing is done only when the 10 m wind is 7-8 m/s or less: at 7 m/s quartz from 25 to 500 µm leaves and no gold moves. The dry -10 mm residue is about 25% of the volume and is washed clean in a few summer weeks.
VALUE: In place on thin-overburden placers or old tailings, digging, feeding and washing cost about $1.7/m³ against about $6.0/m³ for summer washing today (3.6x cheaper); on a pad for thick virgin pay the gain is only 2.1x.

IDEA 6
NAME: Albedo-steered freeze-dry deflation placer
MECHANISM: Anchor kept: in spring, cold dry wind freeze-dries frozen pay gravel by sublimation and blows away the freed fines without any liquid water, leaving the heavies behind as a lag. An hourly energy-balance model for Pevek shows the claimed 0.4-0.7 mm w.e./day holds for only about 2 weeks. A dark surface begins melting around Apr 28 (7-24 mm/day of melt in May). The repair is to steer the albedo: keep the surface dark while it is cold, then leave the raked, lighter lag (albedo 0.3-0.55) once the surface nears 0 °C. This keeps the surface below 0 °C and gives 13 mm w.e. per season (48 days), times 0.6 for the dry-lag penalty (1 mm of dry grains halves the rate). That frees only 58-109 mm of gravel per year, depending on pore ice of 8-15%, so 100,000 m³/yr needs 0.9-1.4 km² of wind-scoured bench or dump surface. The site also needs a blade pass after each snowfall (spring snowfall of about 10 mm w.e. equals the whole budget), 0.6-1.4 m snow fences, and a low saltation-trap lip downwind. The trap is needed because gold flakes start moving at u* 0.23-0.32 m/s, the same as sand, although gold never goes into suspension (Stokes settling 0.6-6.6 m/s).
VALUE: About $3.7-4.5 per m³ processed (about $8-9 per g recovered at 0.6 g/m³) against $6.0/m³ (about $12.5/g) for bulldozer-sluice washing, so 1.3-1.6x cheaper, not 3.6x; on old tailings it is only about 1x.

IDEA 7
NAME: Freeze-and-float boulder pond
MECHANISM: Anchor kept: a pond over the placer lets winter bottom-fast ice freeze onto the stones, and the spring water rise floats the ice off with the stones in it. The in-place sorting part fails by orders of magnitude. Pond waves give a bottom orbital velocity of only 0.03 m/s at 1 m depth, and the pore flow they pump is 6×10⁻⁴ m/s against the 0.02-0.1 m/s needed to fluidise (jig) the gravel. Fines leaving over the spillway would take 2,000-11,000 years, so that part is dropped. The repaired design times the pond depth so the ice (natural 1.6-1.8 m, or 3.1-3.3 m when built up by flooding the ice surface) reaches the boulder tops only in March, while the summer-thawed talik below stays unfrozen. Each m² of floe then lifts 0.08-0.17 m³ of stone a year, and a tractor winch, not the wind, drags the floes to a dump bay. The pond's 1.4-2.2 m of summer thaw prepares the ground.
VALUE: Clearing boulders by ice costs about $1/m³ of boulder against about $6/m³ to drill, blast and doze them (roughly 6x cheaper), which opens bouldery placers that dredges reject; overall washing is only 1.25-1.5x cheaper, so this is a niche.

IDEA 8
NAME: Short-haul trimmed under-ice ore pods
MECHANISM: Anchor kept: crushed ore or coal and snow sealed in an ice shell drift with the current under winter ice, with no vessel and no return trip. The rigid ice shell is essential: in a flexible bag, a 0.7 m change in ice draft would change buoyancy by 390 kg. An HDPE skid on top (μ 0.15, assumed) widens the trim window to 90-404 kg. Pods are filled in autumn at -4 °C, which adds only +10 kg of cold-reserve buoyancy against +65 kg for contents at -25 °C, so no open soaking slot is needed. Pods are 1.2 m tall with a 7-13 cm shell. At 3.7, 11 or 18.4 kg/day of buoyancy loss (water +0.01, +0.03 or +0.05 K), usable trips are only 76-428 km. Coal pods carry 8 t with flooded voids and a 1.76 m³ snow pocket. Routes run in early winter (ice 0.6-1.0 m, so 1.75-2.1 m of depth is needed), more than 1,400 km below the Kolyma dam polynya, and deliver to consumers that burn the cargo in winter. The test case is Zyryanka coal to Srednekolymsk, about 330 km, with roughly 327 m³/s and 0.18-0.33 m/s under the ice.
VALUE: Estimated at $10-20/t delivered, against $39/t by winter road over the same 330 km (1.9-3.9x) and $12-37/t by summer barge plus a stockpile (0.6-3.7x). That is not the 8-24x claimed, and it is unproven.

IDEA 9
NAME: Ice-lift oversize boulder clean-up
MECHANISM: Anchor kept: pond ice freezes onto stones and the spring rise floats the ice off with the stones in it. The design now uses a gap: water depth is set so the ice bottom stays at least 0.3 m above the mined pit floor in 99% of winters. With the snow ploughed off, ice is 1.8 ± 0.08 m and the depth is 2.12 m. The floor never freezes and no gold-bearing matrix is caught. Only oversize (over 1.2 m) left standing on the floor after the gravel is mined is gripped, with P ≈ 1.00. Ploughed spring ice gives 101-126 kg/m² of net lift, so a 1.5 m boulder needs 21-31 m² of floe. Adfreeze grip margins are 1.6-4.9x for 1.5 m boulders but only 0.6-1.8x for 2.5 m boulders, which caps the method at about 2 m. The pond sits below grade in the mined-out pit, so there is no dam, and floes are winched from shore.
VALUE: Clearing oversize by ice costs about $2-2.5/m³ of boulder against $4-8/m³ for secondary blasting, about 2-3x cheaper for the oversize alone. That is only 0.04-2.5% of the cost per recovered gram, so it is a niche.

IDEA 10
NAME: Cold-sealed rolling snow-log pods
MECHANISM: Anchor kept: crushed ore plus snow sealed in an ice shell, carried by the current under winter river ice with no vessel and no return trip. The near-neutral +3 to +9 kg trim fails by orders of magnitude. Shell melt alone (the idea's own 6 cm) costs -196 kg of buoyancy. Snow at 250-350 kg/m³ creeps under hydrostatic load and loses 95-5,300 kg of buoyancy per day (Vionnet 2012 viscosity), and the trapped air gives 521 kg per metre of depth (a Cartesian-diver instability). The repair: a 1.6 m diameter rolling "log", snow pre-compacted to 550 kg/m³ (0.74 m³/t for coal, 1.6 for rock ore), sealed at -35 °C so it self-pressurises to +14.9 kPa, with a +750 kg margin. Creep then costs only 0.6-1.4% (about 100 kg) per 45 days. But rolling needs a mean under-ice velocity of 0.20-0.41 m/s, and getting past ice keels of 5-20 cm needs 0.62-0.95 m/s. Measured under-ice velocities are 0.05-0.25 m/s (Lena delta), and tailwater at +0.5 to +2 °C below dams melts the shell in 0.3-1.1 days.
VALUE: If it ran, pods would cost about $6.8/t for coal against about $124/t by winter road and $27-33/t by summer barge plus stockpiling (4-5x cheaper than the barge), but no surveyed reach has the required velocity, so the ratio is moot.

IDEA 11
NAME: Self-feeding ore-ice buttress dam
MECHANISM: Anchor: the frozen ore pile itself holds the water, and stored warm water run over its bare downstream face melts the ice cement at a rate set by the flow, so the dam doses its own gravel into a riffled chute. Calculation confirms the self-dosing: releasing 1 m³ of ice-cemented gravel takes 101 MJ, which is 4.3-7.6 m³ of 8 °C water, inside the normal sluicing range (a working placer uses 2.2 m³ per m³). The face can transfer heat 20-100x faster than needed, so feed really does equal flow times water temperature. The repair splits the structure into two parts. One is a permanent frozen core under 0.8-1.0 m of saturated peat (it thaws only 0.5-0.6 m per summer). The other is a sacrificial ore buttress downstream, 75 m thick and retreating 0.8 m a day. Creek baseflow (about 47 L/s for 60,000 m³ a season) passes through a small forebay instead of a season-long reservoir, which cuts the dam-break peak from 460 to 128 m³/s. It is used where it is strongest: winter (underground) placer mining, where the hoist already builds a frozen stockpile that today has to be thawed with steam or sprinkling, ripped and fed by dozer.
VALUE: For winter-mined placers the summer washing stage drops from about $6.7 to about $1.3 per m³ (5x cheaper), with no feed dozers, pumps or ripping; for summer-mined gravel built up in autumn the gain is only 2.2x.

IDEA 12
NAME: Drawdown-timed ice boulder lift
MECHANISM: Anchor kept: bottom-fast pond ice freezes onto the boulder tops and a spring water rise floats them off. The original timing (ice reaching the boulders in March) fails. The remaining 775 °C·days of frost freeze 39 cm of gravel onto the floe base, a load of 402 kg/m² against 141 kg/m² of buoyancy, so the floe stays grounded. The repair keeps the pond deeper than the ice until about Apr 25, then draws it down so the ice settles onto the boulders for the last 91 °C·days only. That freezes on only 4.4 cm of gravel, so 1.7 m natural ice lifts 0.058 m³/m² of stone and 3.2 m flood-built ice lifts 0.133 m³/m². A 0.8 m boulder needs 5-9 m² of floe to break out, so only a surface boulder armour of about 10-20% cover can be cleared, not boulders buried in the pay. Floating strips 30 × 100 m are sawn and winched into a dump bay.
VALUE: About $5.1-5.7 per m³ of boulder against $2.7-3.0/m³ for a dozer push or excavator grapple on drained ground (about 0.5x), so it pays only where machines cannot reach, such as surface armour inside a flooded dredge pond.

