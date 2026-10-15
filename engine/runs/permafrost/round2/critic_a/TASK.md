# Task: adversarial review - find what would make these ideas fail or overstate their value

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 4 ideas, already repaired once against reality by a researcher. Your job is to be the toughest competent
outside reviewer: an engineer who will lose money if any of these claims is wrong. You do NOT fix or improve the
ideas; you find their defects, prove each one with a number, and rank them.

You have tools: WebSearch/WebFetch and Bash with python3 (check every claim in real code). Work only in
`/home/user/SomeRepository/engine/runs/permafrost/round2/critic_a/`: read no other files in the repository, do not modify other files, do not commit.

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
IDEA 1 (mean originality 8.0/10, mean feasibility 6.0/10)
NAME: Carbonyl nickel rides gas pipelines
MECHANISM: Anchor kept: nickel goes to market as Ni(CO)4 vapour carried in a trunk gas line's own flow, and is split back to nickel pellets at the gas plant where the line ends. The repair caps the dose at 0.04 mol%, not 0.1 mol%. At 9.8 MPa a 0.1% dose condenses below about -13 °C, while 0.04% stays at 70% of saturation at -20 °C. That still carries about 37 kt Ni a year on a 38 bcm line. The carbonyl is pumped in as a liquid (3.4 kg/s), the way methanol is injected now, together with 0.15 mol% CO, which keeps it thermodynamically stable up to 80 °C in compressor stations. At the gas plant a recuperated decomposer at 180-200 °C splits out 99.97% of it. It burns 0.12% of the line's gas and costs about $440/t Ni. Carbon guard beds are dropped because activated carbon is poor at holding Ni(CO)4. The best feed is a sulfur-free Ni-Fe material such as awaruite or a pre-reduced calcine, because then there is no SO2 to handle. Injection should be as close to the plant as possible, so the toxic section of line stays short.
VALUE: Moving the nickel costs about $7/t Ni in pipeline share against $1,067/t Ni by truck and rail (about 150x cheaper), but the whole chain is only 1.0-1.8x cheaper than selling concentrate for sulfide feed and 2.0-2.35x for awaruite-type feed.

IDEA 2 (mean originality 5.5/10, mean feasibility 6.5/10)
NAME: Freeze-Engine Vitriol Winning
MECHANISM: Anchor kept: freezing the stored copper leach liquor both powers the plant (the heat released by freezing boils propane, which drives a turbine and condenses in -35 to -45 °C air) and pushes CuSO4·5H2O out of solution. Corrected numbers: the engine gives 12 kJ of electricity per kg of ice at -35 °C air, 15 at -40 °C and 19 at -45 °C, not the claimed 15-30. Dilute liquor (2.5 g/L Cu, 80% recovery) needs 494 kg of ice per kg Cu. That covers 80-104% of the electrowinning power only in -35 to -40 °C air. Ice grown in place on panels in the pond would need 2.55 km² of panels and fails. The repaired design boils propane directly in the liquor (direct-contact crystallizer), separates ice in a wash column, and condenses in air-cooled condensers. For 10 kt Cu a year that is 127 MW of heat, 4.5 MW of electricity and $63M of capital. Iron and acid set how far the liquor can be concentrated, so the process is limited to oxide-ore liquor that is low in iron (Fe ≤ 0.5-1 g/L, acid ≤ 2-3 g/L, iron kept ferric). Under those conditions 80-90% of the copper crystallises each winter.
VALUE: About $1,090/t Cu against $1,420/t Cu for solvent extraction plus electrowinning on diesel power at a remote Arctic heap leach, so roughly 1.3x cheaper, not several times.

IDEA 3 (mean originality 6.5/10, mean feasibility 5.0/10)
NAME: Self-Charging Frost Separator Cascade
MECHANISM: Anchor kept: falling grains charge themselves on the chute lining, and the bins that collect them, wired across to the opposite plates, drive the separating field with no power supply, like a Kelvin water dropper. Many stages are stacked down a slope. Grains charged to 5% of the physical maximum (about 10 µC/kg at 300 µm) drift 30-60 cm sideways while falling between 1.5 m plates. A 1 m wide stage self-charges to 45 kV in about 1.4 s, and it does so even with 10^10 Ω of leakage. A passive corona regulator replaces the spark gap. The repair concerns humidity. Grains at -40 °C air temperature sit at about 90% relative humidity, so the original "dry cold air" claim was wrong. The cascade is therefore enclosed and ventilated with outdoor -40 °C air warmed by the grinding mill's heat (about 690 m³ per tonne of ore). At 0 °C that air is at 1.9% relative humidity, the same dryness as preheating the feed to about 85 °C in an ordinary plant. With middlings recycled, 9 stages that each send 85% of the valuable mineral and 45% of the waste forward lift spodumene ore from 1.2% to 6.1% Li2O at 82% recovery. The circulating load is 7.2x the feed and the total height is about 27 m.
VALUE: About $27/t ore including haul of the 16% mass concentrate, against $105/t to haul raw ore 700 km by winter road (3.9x cheaper), but only about 1.2-1.6x cheaper than an Arctic flotation plant plus haul.

IDEA 4 (mean originality 5.5/10, mean feasibility 5.0/10)
NAME: Night-sky lithium freeze cascade
MECHANISM: Anchor tested as stated: trays under film that radiates through the 8-13 µm atmospheric window are pushed below the CaCl2-ice eutectic (about -50 °C), so CaCl2 hexahydrate and ice lock up together and LiCl stays liquid. At -50 °C that band carries only 30 W/m² (21% of blackbody). With no brine load at all the film settles only 7.8 K below -40 °C air. At -52 °C it removes no net heat unless the air is already -45 °C or colder. At Udachny (January mean -39.4 °C) that gives about 273 usable hours, which freeze about 55 kg of brine per m² each winter. That means 11,600 m² of trays per tonne of lithium carbonate equivalent (LCE) per year, about $55,000/t LCE. Above the eutectic, ambient cold concentrates Li only 1.0-1.55x, so the anchor cannot be rescued at scale. The only workable niche drops the calcium part of the anchor: the same trays freeze sorbent eluate that is free of calcium (LiCl only, eutectic -75 °C) with plain -40 °C air. That concentrates it about 30x using roughly 100 m² per t LCE/yr, about $500/t LCE.
VALUE: As stated the idea is about 10x more expensive than the whole sorption route ($3.4-6.2k/t LCE), so it fails; only the eluate-freezing niche, which does not use the eutectic, is cheaper than the evaporation step it would replace.

