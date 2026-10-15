# Task: adversarial review - find what would make these ideas fail or overstate their value

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 12 ideas, already repaired once against reality by a researcher. Your job is to be the toughest competent
outside reviewer: an engineer who will lose money if any of these claims is wrong. You do NOT fix or improve the
ideas; you find their defects, prove each one with a number, and rank them.

You have tools: WebSearch/WebFetch and Bash with python3 (check every claim in real code). Work only in
`/home/user/SomeRepository/engine/runs/permafrost/round2/audit_a/`: read no other files in the repository, do not modify other files, do not commit.

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
NAME: Night-sky lithium freeze cascade
MECHANISM: Anchor tested as stated: trays under film that radiates through the 8-13 µm atmospheric window are pushed below the CaCl2-ice eutectic (about -50 °C), so CaCl2 hexahydrate and ice lock up together and LiCl stays liquid. At -50 °C that band carries only 30 W/m² (21% of blackbody). With no brine load at all the film settles only 7.8 K below -40 °C air. At -52 °C it removes no net heat unless the air is already -45 °C or colder. At Udachny (January mean -39.4 °C) that gives about 273 usable hours, which freeze about 55 kg of brine per m² each winter. That means 11,600 m² of trays per tonne of lithium carbonate equivalent (LCE) per year, about $55,000/t LCE. Above the eutectic, ambient cold concentrates Li only 1.0-1.55x, so the anchor cannot be rescued at scale. The only workable niche drops the calcium part of the anchor: the same trays freeze sorbent eluate that is free of calcium (LiCl only, eutectic -75 °C) with plain -40 °C air. That concentrates it about 30x using roughly 100 m² per t LCE/yr, about $500/t LCE.
VALUE: As stated the idea is about 10x more expensive than the whole sorption route ($3.4-6.2k/t LCE), so it fails; only the eluate-freezing niche, which does not use the eutectic, is cheaper than the evaporation step it would replace.

IDEA 2
NAME: Self-Charging Frost Separator Cascade
MECHANISM: Anchor kept: grains charged on the chute lining build the separating field themselves, through bins cross-wired to the opposite plates, with no power supply. The stated 30 kV/m gives only 4-9 cm of drift (not 30-60) and is space-charge-limited to 0.15 t/h per metre, which would need 7 km of plates. Repaired design: - A 0.3 m gap self-excites to 90 kV (300 kV/m, 8% of breakdown at -40 °C). That gives 41 cm of drift over a 1.5 m fall and 1.47 t/h per metre, or about 700 m of plates in total for 1 Mt/yr. - Insulating grains cannot hand over charge the way water drops do in a Kelvin dropper. Instead, discharges inside the charged grain pile pass about 98% of it to the bin. Leakage must stay above 2.2e10 Ω per metre. - Intake air must be heated to 20-40 °C, not 0 °C, to dry ore with 1-2% moisture: 137 MJ/t against 43-54 MJ/t of mill heat.
VALUE: $3,994/t Li2O delivered against $4,588 for dense-media separation plus haul (the best baseline, 1.15x) and $6,292 for Arctic flotation (1.6x). NICHE.

IDEA 3
NAME: Carbonyl nickel rides gas pipelines
MECHANISM: Anchor kept: nickel travels as Ni(CO)4 vapour (0.04 mol%) inside a trunk gas line's own flow and is split back to metal where the line ends. Injection now goes in only downstream of the last local offtake. Before any planned vent, injection stops for one transit time (10 h per 300 km, 72 h for the full 2,159 km at 8.3 m/s) and Gazprom's mobile compressor units pump the section down, so planned vents release almost no carbonyl. Compressor discharge is capped at 50 °C, which cuts the CO stabiliser from 0.15% to 0.05% (equilibrium needs 0.032%), so CO use falls from 3.70 to 2.51 t per t Ni, against a hard minimum of 1.91. A 250 °C nickel-bed polisher after the decomposer leaves 0.09 ppb Ni(CO)4 in the sales gas at equilibrium (4.5 ppb at 200 °C). Unsolved: a rupture still releases about 12 t Ni(CO)4 per 30 km section, which is 8.8e8 m³ of air at the IDLH. Its 40-60 s half-life in air means only 0.3-2% survives 1 km downwind, but CO in the plume can slow the breakdown to minutes.
VALUE: The pipeline-specific cost is $109-947/t Ni (one-way CO plus lost line capacity, minus the CO's value as fuel), against about $100-150/t Ni to ship pellets or matte, so it loses to best practice unless CO is a free by-product costing under about $56/t; it beats only trucking concentrate ($1,067/t Ni), by 0.8-1.9x.

IDEA 4
NAME: Night-sky lithium freeze cascade
MECHANISM: The anchor (night-sky cooling that drives CaCl2 brine below its -50 °C eutectic) cannot be rescued. Even with a heat pump rejecting to -40/-45 °C air, it needs 5.5-15 MWh per t LCE and must freeze 450-910 t of brine per t LCE, and the leftover liquor is still about 30% CaCl2, so DLE is still needed. Above the eutectic, cold concentrates lithium only 1.25x. The surviving niche keeps only "Arctic cold concentrates lithium" and applies it to Ca-free sorbent eluate. Reverse osmosis first takes the eluate to 6 g/L Li (37 bar osmotic pressure). Two stages of spray freezing (snowmaking guns rather than trays) then take it to 20.6 g/L by draining the unfrozen brine and collecting the early melt. That moves 53% of the Li per pass, needs 62 t of ice per t LCE, and gives a product that freezes at -14 °C. Late melt at ≤1.1 g/L Li goes back to the RO feed, so no lithium is lost in the ice, and winter-only freezing needs 0.37 Mm³ of stored RO concentrate, not 2.2-7.3 Mm³.
VALUE: $110-240/t LCE against $470-1,085/t LCE for the MVR evaporator it replaces (2-4x cheaper for that step), but that is only 5-15% off the $3.4-6.2k/t LCE whole route, and the night-sky/eutectic anchor is not used.

IDEA 5
NAME: Night-sky lithium freeze cascade
MECHANISM: Anchor tested: trays radiating through the 8-13 µm window push Ca-Li brine below the CaCl2-ice eutectic (-49.8 °C) so Ca locks up and LiCl stays liquid. My own band model agrees with the original: - With no brine load the film settles 8.1 K below -40 °C air. - A film at -52 °C cools only when the air is at -45 °C or colder. That is 288 hours a winter, freezing 36 kg per m². - So the trays need 13,000-35,600 m² per t LCE per year (Udachnaya brine averages 147 mg/L Li). Keeping the anchor above the eutectic does not help: crystallising CaCl2·6H2O from brines with 36-40% CaCl2 needs only plain -40 °C air (Li concentrates x1.3-1.9), and radiative trays add only x1.81 to x1.92. Only niche: freeze-concentrate Ca-free sorbent eluate in thin flooded layers with -40 °C air (about 100 m² per t LCE), which drops the anchor.
VALUE: As stated, at least $65-178k/t LCE against $3.4-6.2k for the whole sorption route, so it FAILS. The eluate niche beats RO plus mechanical evaporation ($690-1,150/t LCE on diesel) only off-grid; on grid power that route costs $260-440/t LCE.

IDEA 6
NAME: Carbonyl nickel rides gas pipelines
MECHANISM: Anchor kept: nickel goes to market as Ni(CO)4 vapour carried in a trunk gas line's own flow, and is split back to nickel pellets at the gas plant where the line ends. The repair caps the dose at 0.04 mol%, not 0.1 mol%. At 9.8 MPa a 0.1% dose condenses below about -13 °C, while 0.04% stays at 70% of saturation at -20 °C. That still carries about 37 kt Ni a year on a 38 bcm line. The carbonyl is pumped in as a liquid (3.4 kg/s), the way methanol is injected now, together with 0.15 mol% CO, which keeps it thermodynamically stable up to 80 °C in compressor stations. At the gas plant a recuperated decomposer at 180-200 °C splits out 99.97% of it. It burns 0.12% of the line's gas and costs about $440/t Ni. Carbon guard beds are dropped because activated carbon is poor at holding Ni(CO)4. The best feed is a sulfur-free Ni-Fe material such as awaruite or a pre-reduced calcine, because then there is no SO2 to handle. Injection should be as close to the plant as possible, so the toxic section of line stays short.
VALUE: Moving the nickel costs about $7/t Ni in pipeline share against $1,067/t Ni by truck and rail (about 150x cheaper), but the whole chain is only 1.0-1.8x cheaper than selling concentrate for sulfide feed and 2.0-2.35x for awaruite-type feed.

IDEA 7
NAME: Freeze-Engine Vitriol Winning
MECHANISM: Anchor kept: freezing stored copper leach liquor both drives a heat engine (the heat of freezing boils the working fluid, which condenses in Arctic air) and crystallises CuSO4·5H2O. Propane is replaced by n-butane, which forms no hydrate on its own and was the direct-contact fluid in the 1960s-70s secondary-refrigerant freeze-desalination pilots. It boils at 0.87-0.97 bar against the liquor and condenses at 0.19-0.30 bar. Freezing is staged so that most ice forms while the liquor is still dilute, which keeps the ice-weighted freezing point at -0.8 °C. Copper recovery is capped at 80% and feed acid at 2.5 g/L, and the 90% case is dropped. Fans would eat about half the output, so a 60-80 m natural-draft dry tower (47-52 Pa of draft at -35 °C) replaces them, and freezing is scheduled into the coldest hours. That gives 6-9 kJ per kg of ice, enough for 42-63% of electrowinning power at Udachny-type cold but only 24-44% at Chara (Udokan). A richer 10 g/L leach solution cuts ice from 492 to 123 kg per kg Cu and the freeze step to $105-165/t Cu, but then the engine covers only about 12% of electrowinning power.
VALUE: At 2.5 g/L the route is 0.56-0.86x as cheap as grid-powered SX-EW at Udokan (i.e. dearer) and 0.83-1.08x at an off-grid diesel site; only an off-grid, low-Mg, 10 g/L case reaches about 1.1-1.4x cheaper.

IDEA 8
NAME: Carbonyl nickel rides gas pipelines
MECHANISM: Anchor kept: nickel travels as Ni(CO)4 vapour in the Power of Siberia line's own gas flow (9.8 MPa, 38 bcm/yr) and is split back out at the Amur gas plant where the line ends. Repaired design: 0.027 mol% carries 25 kt Ni/yr, which is Kun-Manie scale. That dose is at a saturation ratio of 0.25 at -10 °C. Compressor discharge is capped at 45 °C, so only 0.035% CO is needed to keep the carbonyl stable (the original 0.15% was sized for 80 °C). At the plant, a cold-oil absorber (20-60 kg/s of oil, 10-16 stages) catches 99.999% and leaves 2.7 ppb in sales gas, instead of heating the whole 879 kg/s stream (423 MW gross). The concentrated carbonyl is then decomposed at 200 °C. Propane hydrate does not apply here; the binding cost is CO make-up of 2.53 t CO per t Ni (about $514/t Ni).
VALUE: The physics works, but the pipeline leg costs about $960/t Ni more than running the same carbonyl refinery at the BAM/PoS junction and shipping pellets by rail, which saves only $27/t Ni of freight (about 0.03x). The whole chain at $6.6-8.4k/t Ni is no cheaper than selling concentrate at 70-75% payability ($5.4-6.1k/t Ni lost), so it FAILS on cost.

IDEA 9
NAME: Self-Charging Frost Separator Cascade
MECHANISM: Anchor kept: grains charge themselves on the chute lining, and the bins that catch them, wired across to the opposite plates, build the separating field with no power supply, like a Kelvin water dropper. The field is reset to 150 kV/m across a 0.5 m gap (75 kV, 5% of air breakdown), which gives 17-23 cm of drift per side in a drag-included simulation without grains hitting the plates (200 kV/m would hit them). The sorted charge delivers only 0.4-1.4 µA per metre of plate width, so self-excitation needs at least 5e10 Ω of leakage resistance per 10 m channel. Space charge caps each channel at 0.17-0.5 t/h per metre of plate width, so each stage is a stack of alternating-polarity plates at 0.5 m pitch: 170-525 channels, each 10 m wide, for 1 Mt/yr. Ore moisture is removed by a closed air loop through an outdoor cold trap at -30 °C, which gives 2% RH at the separator. Mill heat and diesel-generator waste heat supply the drying heat: 9-19 MJ/t at 0.2-0.4% ice, 47 MJ/t at 1% ice. With middlings recycled, eight stages reach 6.2% Li2O at 82% recovery only if each stage sends forward 85% of the spodumene and 45% of the waste. A 80/50 split needs 22 stages and 23x circulating load, and a 75/55 split cannot reach 6% at all.
VALUE: $4,100-4,960 per t of Li2O recovered at the railhead, against $6,430-7,390 for XRT sorting plus DMS (the cheapest real alternative) and $7,400-8,270 for Arctic DMS plus flotation, so 1.3-1.8x cheaper, and only if a measured per-stage split of 85/45 or better holds.

IDEA 10
NAME: Freeze-Engine Vitriol Winning
MECHANISM: Anchor kept: freezing the stored copper leach liquor runs a Rankine engine that rejects heat to Arctic air, and the same freezing crystallises CuSO4·5H2O. Repairs: (1) The direct-contact refrigerant changes from propane to n-butane. Propane boiling at -6 to -8 °C (3.5-3.9 bar) sits inside the propane-hydrate field. (2) Fan power is now counted: 8.7 kJ per kg of ice against 15.2 gross at -40 °C. The fans are replaced by a natural-draft dry tower. (3) Integrated over a real Yakutsk November-March winter, the engine nets 7.6 kJ per kg of ice. That covers 50% of electrowinning power at 2.5 g/L, not 80-104%. (4) Freezing costs $1.5-2.5 per m³ of feed, so dilute liquor loses. The process is moved to 10-15 g/L liquor from leach-solution recycle on siliceous low-Mg oxide ore (Mg ≤ 2 g/L, Fe ≤ 1 g/L, since impurities concentrate 24x). There it needs 77-117 kg of ice per kg Cu, and the engine supplies 8-12% of electrowinning power.
VALUE: $1,222-1,379/t Cu against $1,590/t Cu for diesel-powered solvent extraction plus electrowinning (1.15-1.3x cheaper), but it loses to grid-powered SX-EW ($1,086/t). NICHE.

IDEA 11
NAME: Freeze-Engine Vitriol Winning
MECHANISM: Anchor kept: freezing the stored copper leach liquor both powers the plant (the heat released by freezing boils propane, which drives a turbine and condenses in -35 to -45 °C air) and pushes CuSO4·5H2O out of solution. Corrected numbers: the engine gives 12 kJ of electricity per kg of ice at -35 °C air, 15 at -40 °C and 19 at -45 °C, not the claimed 15-30. Dilute liquor (2.5 g/L Cu, 80% recovery) needs 494 kg of ice per kg Cu. That covers 80-104% of the electrowinning power only in -35 to -40 °C air. Ice grown in place on panels in the pond would need 2.55 km² of panels and fails. The repaired design boils propane directly in the liquor (direct-contact crystallizer), separates ice in a wash column, and condenses in air-cooled condensers. For 10 kt Cu a year that is 127 MW of heat, 4.5 MW of electricity and $63M of capital. Iron and acid set how far the liquor can be concentrated, so the process is limited to oxide-ore liquor that is low in iron (Fe ≤ 0.5-1 g/L, acid ≤ 2-3 g/L, iron kept ferric). Under those conditions 80-90% of the copper crystallises each winter.
VALUE: About $1,090/t Cu against $1,420/t Cu for solvent extraction plus electrowinning on diesel power at a remote Arctic heap leach, so roughly 1.3x cheaper, not several times.

IDEA 12
NAME: Self-Charging Frost Separator Cascade
MECHANISM: Anchor kept: falling grains charge themselves on the chute lining, and the bins that collect them, wired across to the opposite plates, drive the separating field with no power supply, like a Kelvin water dropper. Many stages are stacked down a slope. Grains charged to 5% of the physical maximum (about 10 µC/kg at 300 µm) drift 30-60 cm sideways while falling between 1.5 m plates. A 1 m wide stage self-charges to 45 kV in about 1.4 s, and it does so even with 10^10 Ω of leakage. A passive corona regulator replaces the spark gap. The repair concerns humidity. Grains at -40 °C air temperature sit at about 90% relative humidity, so the original "dry cold air" claim was wrong. The cascade is therefore enclosed and ventilated with outdoor -40 °C air warmed by the grinding mill's heat (about 690 m³ per tonne of ore). At 0 °C that air is at 1.9% relative humidity, the same dryness as preheating the feed to about 85 °C in an ordinary plant. With middlings recycled, 9 stages that each send 85% of the valuable mineral and 45% of the waste forward lift spodumene ore from 1.2% to 6.1% Li2O at 82% recovery. The circulating load is 7.2x the feed and the total height is about 27 m.
VALUE: About $27/t ore including haul of the 16% mass concentrate, against $105/t to haul raw ore 700 km by winter road (3.9x cheaper), but only about 1.2-1.6x cheaper than an Arctic flotation plant plus haul.

