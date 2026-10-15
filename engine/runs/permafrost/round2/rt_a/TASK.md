# Task: repair original ideas against reality WITHOUT losing what makes them original

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 4 ideas an idea engine produced for this question. Blind judges rated them for originality (O) and
order-of-magnitude feasibility (F, out of 10). Your job is NOT to invent new ideas and NOT to replace them with safer
known solutions. Your job is to make each one work while keeping its anchor - the one distinctive idea that makes it
original.

You have tools: WebSearch/WebFetch (check what exists, find real material data, field data and costs) and Bash with
python3 (do every estimate in real code). Work only in `/home/user/SomeRepository/engine/runs/permafrost/round2/rt_a/`: read no other files in the repository, do not
modify other files, do not commit.

For each idea, loop until it works or you can prove it cannot:
1. Name its ANCHOR (the distinctive idea) in a few words. This must survive.
2. Find the binding quantity (what decides whether it works at the needed scale - a rate, an energy balance, a
   recovery, a throughput, a safety limit) and compute it in Python with real numbers from the literature (cite the
   source in your notes).
3. BASELINE: compare against the BEST current practice a competent operator would actually use for the same job
   (list at least two real alternatives, including the cheapest one), and compute cost per unit of RECOVERED or
   DELIVERED product (per kg of metal recovered, per tonne delivered), not per tonne of raw material moved, with
   sourced numbers. Never compare against a strawman nobody would do.
4. CONSISTENCY PASS: list every tolerance, window and limit your design relies on (buoyancy margins, temperature
   limits, strengths, breakdown fields, stage efficiencies, site conditions where you placed it) and check every
   rate you computed against every one of them over the whole operating time (rate x duration vs window). Check
   that the site or route you chose really has the conditions you assumed. Write the check table in your notes.
5. If it fails, change the DESIGN AROUND the anchor (materials, geometry, operating regime, scale, season, which
   resource/cargo/deposit type it is used for) and recompute. Look for the regime where the anchor is strongest.
   Repeat - several rounds per idea is normal.
6. Name the hazards honestly and design them down where possible; say which unknown number decides the idea and the
   cheapest experiment that would measure it (with the sample size it needs).
7. Check novelty: if the repaired design turns out to be a known system, keep the anchor and find the version that is
   not known.
8. Only if no anchor-preserving design can work, say so and give the best honest niche.

An adversarial reviewer has examined the current versions. Answer EVERY defect it lists: fix it in
the design, refute it with a computed number, or concede it in the verdict. Its review:
<<<REVIEW
=== REVIEW ===
IDEA 1: Carbonyl nickel rides gas pipelines
DEFECT | FATAL | The safety fix ("inject close to the plant") cancels the value, which needs a long carbonyl-laden run from a remote source, and any useful length holds a toxic inventory that routine pipeline venting releases. | The 2,159 km x 1,420 mm Power of Siberia at 0.04 mol% holds about 1,021 t Ni(CO)4 (0.47 t/km, 14 t per 30 km block-valve section). Gazprom's own 2021 repair vents of 0.9-2.7 Mm3 would each release 2.6-7.7 t Ni(CO)4 (NIOSH IDLH 2 ppm, so 1.8-5.5e8 m3 of air at IDLH; OSHA PEL 0.001 ppm). Every local offtake between injection and plant would also deliver 400 ppm carbonyl.
DEFECT | MAJOR | The cost items the text leaves out are larger than the transport saving they are meant to beat. | The line runs open-loop on CO: the 0.15% dose plus the 4 CO bound in each carbonyl is 137 kt CO/yr, or 3.7 t CO per t Ni, worth $550-1,100/t Ni at $150-300/t CO. Power of Siberia is at full capacity (38.8 bcm in 2025), so the 0.19% of capacity used displaces 72 Mm3/yr of sales gas, worth $94-234/t Ni net of the CO fuel credit (13-33x the stated $7/t). Add the $440/t decomposer and the total is $1,080-1,780/t Ni against $1,060/t of avoided truck and rail.
DEFECT | MAJOR | The specified 99.97% split leaves sales gas above occupational limits. | The 0.03% slip leaves 0.12 ppm Ni(CO)4 (plus 0.31 mol% CO) in gas sent to China. A leak at 1-4.4% gas in air gives 1.2-5.3 ppb, above the 1 ppb PEL. Also, 99.97% is exactly the equilibrium ceiling at 180 °C and 98 bar (99.971% with dH 161 kJ/mol, dS 410 J/molK), so there is no kinetic margin; only 200 °C reaches 99.995%.
DEFECT | MAJOR | No sulfur-free feed exists near any trunk line, and the only nearby nickel project falls in the 1.0-1.8x sulfide case, not "several times". | Searches find no Russian awaruite resource, only placer occurrences in Kamchatka and Koryak. Kun-Manie is sulfide at 0.76% Ni, 700 km NE of Blagoveshchensk, and still needs a 320-338 km road to the BAM railway, so the pipeline does not remove the road leg.
DEFECT | MINOR | CO at 0.147 bar partial pressure makes iron carbonyl formation from the pipe steel thermodynamically favoured at line temperatures; the rate (kinetics) is untested. | Equilibrium pFe(CO)5 is 0.077 bar at 15 °C, above the 0.039 bar Ni(CO)4 partial pressure, over 9.3e6 m2 of wetted steel. The Fe would co-deposit in the Ni product.
DEFECT | MINOR | The 0.12% gas burn needs a very large high-pressure recuperator that is not visibly costed. | It needs at least 88% recuperation on about 380 MW of 7-10 MPa gas-gas duty (861 kg/s heated by 190 K), roughly 34,000-57,000 m2 at U = 300-500 W/m2K.
DEFECT | MINOR | The 150x transport ratio is set against hauling concentrate, not the matte or metal a competent remote operator ships. | $1,067/t Ni equals $107/t of 10% Ni concentrate. Shipping 70% Ni matte costs about $150/t Ni, so the ratio is about 20x, and transport is under 7% of the nickel price anyway.
SURVIVES | 37.1 kt Ni/yr and 3.42 kg/s reproduce (20 °C standard). A 0.1% dose condenses at -12 °C (claimed -13). The 0.04% dose is at 61% of saturation at -20 °C (claimed 70%, so the claim is conservative). With CO the carbonyl stays stable up to 78-87 °C at 98 bar (claimed 80 °C), or 67-82 °C at 55-75 bar compressor suction, above normal discharge temperatures.

IDEA 2: Freeze-Engine Vitriol Winning
DEFECT | FATAL | Boiling propane in direct contact with liquor at its freezing point makes propane hydrate, not just ice. | Propane boils at 3.75-4.5 bar at -2 to -8 °C, which is 2.8-3.0x the ice-hydrate-vapour equilibrium pressure (1.27-1.6 bar, from 1.0 bar at -14 °C and Q1 at 1.72 bar). If just 1% of the frozen water forms C3H8·17H2O, it locks 0.71 kg propane per kg Cu ($356/t Cu). The hydrate-free alternative, n-butane, runs at 0.25-0.85 bar vacuum and has not been costed.
DEFECT | MAJOR | The design assumes -35 °C air for its whole 150-day run, which real sites do not have, so the engine covers much less of the electrowinning power. | 4.94 Mt ice at 127 MW needs 3,609 h. Estimated hours at or below -35 °C: Udachny (January mean -39.4 °C) about 1,500 h; Chara at Udokan, the only Russian SX-EW copper site (January mean -31.8 °C), 300-530 h. On the idea's own output curve (zero at -18 °C air), the season average covers 72% of EW power at Udachny and 36% at Chara, not 80-104%. The diesel top-up costs $280-430/t Cu, which brings $1,090 to $1,370-1,520 against $1,420.
DEFECT | MAJOR | Fans on the air-cooled condenser eat much of the 4.5 MW gross output, and they are not counted. | Rejecting 122.5 MW with a 5-12 K air temperature rise moves 6,700-16,400 m3/s of air. At 100-150 Pa and 65% fan efficiency that is 1.0-3.8 MW, or 23-84% of the 4.5 MW.
DEFECT | MAJOR | The baseline assumes diesel power, but the relevant site has grid power. | Udokan has a 50 MW substation built and 146 MW more under construction. Grid power at $0.05-0.07/kWh makes EW power $100-140/t Cu instead of $600/t, which puts SX-EW at about $920-960/t Cu, below the $1,090 claimed.
DEFECT | MAJOR | The scale and the $63M capital cost have no precedent. | 380 kg/s of ice is 1,368 t/h, 46x GEA's largest custom wash-column freeze-concentration plant (30 t/h of water removed).
DEFECT | MAJOR | Concentrating the liquor about 114-fold drives magnesium sulfate to saturation, but the spec limits only Fe and acid. | At 80% recovery, MgSO4 hydrate saturates (about 40 g Mg per kg water) once feed Mg exceeds 0.35 g/L. Recirculated heap-leach liquor usually carries more than that, and with no SX step the impurities go straight into the crystals and on to electrowinning.
DEFECT | MINOR | The 90% end of the "80-90% crystallises" claim is inconsistent with the acid limit. | Ignoring the common-ion effect, 90% recovery needs 228x concentration, which turns 2-3 g/L acid into 31-41 wt% H2SO4, freezing below about -37 °C (battery-acid chart). Even 80% gives 18-25 wt%, freezing at -12 to -22 °C, where the engine produces no power.
DEFECT | MINOR | Storing each year's leach liquor over summer means an acid copper pond on permafrost. | That is 4.94 Mm3 of liquor per 10 kt Cu (about 1 km2 at 5 m depth), with leakage and thawed-ground risk.
SURVIVES | 494 kg ice per kg Cu reproduces (CuSO4 solubility 14.3 g/100 g, giving 988 g ice per 2.0 g Cu). 12/15/19 kJ/kg is 29-35% of Carnot, which is plausible. EW coverage at constant -35/-40 °C air works out to 1.65/2.06 kWh/kg Cu. 127 MW for 150 days is consistent.

IDEA 3: Self-Charging Frost Separator Cascade
DEFECT | MAJOR | The stated drift cannot happen at the stated voltage. | A 30-60 cm drift at 10 µC/kg over a 1.5 m fall needs 196-392 kV/m, and since the gap must be at least as wide as the drift, at least 59-235 kV. At 45 kV the absolute maximum is 26 cm. With a 1 m gap the drift is 5-7 cm (drag-included simulation, entry speed 0-1.5 m/s).
DEFECT | MAJOR | The humidity fix assumes the ore itself is dry, and permafrost ore is not. | The 690 m3/t (892 kg) of 0 °C air can take up 0 kg/t of water at 1.9% RH, and only 3.3 kg/t (0.33% moisture) even when saturated. Ore with 1-3% ice needs 28-85 MJ/t of drying heat, 0.8-2.4x the whole mill heat (36 MJ/t). Published feldspar/quartz tribo-separation also needed more than 100 °C preheat (CNR Cagliari).
DEFECT | MAJOR | The 85%/45% split per stage is assumed, not measured, and the claim falls apart within a plausible range. | Spodumene, quartz, feldspar and mica are all silicates, and ternary feldspar/quartz mixes needed HF pretreatment. 80/50 gives 4.6% Li2O at 75% recovery; 75/55 gives 2.9% at 67%; 85/55 gives 3.3%.
DEFECT | MAJOR | Space charge from the separated grain streams limits throughput, so a 1 m stage does not scale. | Keeping the stream counter-field under 10-30% of a 100-180 kV/m field allows about 0.2-1.0 t/h per metre of plates. A 1 Mt/yr plant at 7.2x circulating load (900 t/h) needs 900-4,700 m of plate width, 100-520 m per stage, inside a ventilated 27 m enclosure.
DEFECT | MINOR | Mill heat is too small to warm the ventilation air. | 690 m3/t warmed by 40 K needs 10 kWh/t; dry Bond grinding to 300 µm (Wi 10-14) gives 5.8-8.7 kWh/t.
DEFECT | MINOR | "Never tried" is wrong for the separation itself, and the baseline leaves out dry pre-concentration. | Leoben (2018) ran free-fall electrostatic separation on Koralm spodumene ore. TOMRA XRT sorting already runs at over 1,000 t/h at Pilgangoora. Against flotation plus haul the idea is only 1.2-1.6x cheaper (conceded).
SURVIVES | Charge of 5% of the breakdown limit is 8.4-10 µC/kg. RH 1.9% at 0 °C reproduces. The cascade reproduces (feed at the bottom stage gives 82.4% recovery, 6.5% Li2O, 15% mass, 7.1x throughput). Charging to 45 kV in 1.4 s against 1e10 Ω (4.5 µA) works with 0.2-1 kg/s of grains. $105/t for 700 km is $0.15/t-km, a normal winter-road rate.

IDEA 4: Night-sky lithium freeze cascade
DEFECT | FATAL | The named anchor (freezing CaCl2 brine below its eutectic under night sky) fails, as the text concedes. | It costs $55,000/t LCE, 8.9-16x the whole sorption route ($3.4-6.2k/t LCE).
DEFECT | MAJOR | The niche's 100 m2 per t LCE/yr needs far more ice per square metre than a static tray can grow in one winter. | It needs 1.8-6.1 t ice/m2 per winter for eluate at 1.0-0.3 g/L Li (48-197 W/m2 average). Stefan-type growth over 4,000-6,000 freezing degree-days gives 1.2-1.9 t/m2. So area must be 1-3.2x larger ($500-1,600/t LCE), or thin layers must be harvested mechanically, which is not costed.
DEFECT | MAJOR | Lithium trapped in the ice is not accounted for. | Progressive freezing to 30x with an effective distribution coefficient of 0.05-0.2 leaves 16-49% of the Li in the ice (the concentration actually reached is 15-25x). Recovering it means remelting or recycling 180-600 t of ice per t LCE.
DEFECT | MAJOR | The step it claims to beat is evaporation, but competent DLE flowsheets concentrate eluate with reverse osmosis first, and RO costs about the same. | RO took CleanTech's pilot eluate from 710 to 2,194 mg/L. LiCl osmotic pressure is only 14-35 bar at 2-5 g/L Li. At $0.3-1/m3, the 188-626 m3 of eluate per t LCE costs about $60-630/t LCE, comparable to the $500/t claimed, and RO runs all year.
DEFECT | MINOR | Sorption runs all year but freezing runs about 5 months, so eluate must be stored. | That is 110-365 m3 per t LCE held over summer, or 2.2-7.3 Mm3 of ponds for a 20 kt LCE/yr plant.
SURVIVES | The 8-13 µm band at -50 °C carries 30.0 W/m2 (21.3% of blackbody). Udachny has about 273 h at or below -45 °C (estimated 142-375 h). 11,600 m2 x 55 kg/m2 implies 294 mg/kg Li, consistent with Siberian CaCl2 brines of up to 600 mg/L. $55k/t LCE works out to $4.7/m2/yr. Concentrating only 1.0-1.55x above the eutectic is plausible.

Note: WebFetch, Open-Meteo and NOAA were unreachable (DNS failure or proxy 403). Hours below the temperature thresholds are therefore estimated from published monthly means (Udachny: November -29.8, December -36.0, January -39.4, February -35.2, March -24.3 °C; Chara January -31.8 °C) with an hourly standard deviation of 5-8 K, not from hourly station records.

Files are in /home/user/SomeRepository/engine/runs/permafrost/round2/critic_a/calc/:
- idea1_carbonyl.py
- idea2_freeze.py
- climate_hours.py
- idea3_cascade.py
- idea3_frost.py
- idea4_nightsky.py
REVIEW>>>

Keep `LOG.md` in your folder: one line per round (idea, change, decisive number, result). Spend about 45-60 minutes at most.

Final answer (text only): first the 4 repaired ideas in exactly this format, then a short NOTES section (per idea:
anchor kept?, decisive numbers with sources, best-baseline comparison per unit of recovered/delivered product,
consistency table summary, hazards, deciding unknown and experiment, closest existing work, verdict WORKS / NICHE / FAILS).
=== IDEAS ===
IDEA 1
NAME: (max 5 words)
MECHANISM: (2-5 sentences: the anchor first, then the repaired design, with the decisive computed numbers)
VALUE: (1 sentence, with the cost ratio vs the best current practice)
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

