=== IDEAS ===
IDEA 1
NAME: Carbonyl nickel rides gas pipelines
MECHANISM: Anchor kept: nickel travels as Ni(CO)4 vapour (0.04 mol%) inside a trunk gas line's own flow and is split back to metal where the line ends. Injection now goes in only downstream of the last local offtake. Before any planned vent, injection stops for one transit time (10 h per 300 km, 72 h for the full 2,159 km at 8.3 m/s) and Gazprom's mobile compressor units pump the section down, so planned vents release almost no carbonyl. Compressor discharge is capped at 50 °C, which cuts the CO stabiliser from 0.15% to 0.05% (equilibrium needs 0.032%), so CO use falls from 3.70 to 2.51 t per t Ni, against a hard minimum of 1.91. A 250 °C nickel-bed polisher after the decomposer leaves 0.09 ppb Ni(CO)4 in the sales gas at equilibrium (4.5 ppb at 200 °C). Unsolved: a rupture still releases about 12 t Ni(CO)4 per 30 km section, which is 8.8e8 m³ of air at the IDLH. Its 40-60 s half-life in air means only 0.3-2% survives 1 km downwind, but CO in the plume can slow the breakdown to minutes.
VALUE: The pipeline-specific cost is $109-947/t Ni (one-way CO plus lost line capacity, minus the CO's value as fuel), against about $100-150/t Ni to ship pellets or matte, so it loses to best practice unless CO is a free by-product costing under about $56/t; it beats only trucking concentrate ($1,067/t Ni), by 0.8-1.9x.

IDEA 2
NAME: Freeze-Engine Vitriol Winning
MECHANISM: Anchor kept: freezing stored copper leach liquor both drives a heat engine (the heat of freezing boils the working fluid, which condenses in Arctic air) and crystallises CuSO4·5H2O. Propane is replaced by n-butane, which forms no hydrate on its own and was the direct-contact fluid in the 1960s-70s secondary-refrigerant freeze-desalination pilots. It boils at 0.87-0.97 bar against the liquor and condenses at 0.19-0.30 bar. Freezing is staged so that most ice forms while the liquor is still dilute, which keeps the ice-weighted freezing point at -0.8 °C. Copper recovery is capped at 80% and feed acid at 2.5 g/L, and the 90% case is dropped. Fans would eat about half the output, so a 60-80 m natural-draft dry tower (47-52 Pa of draft at -35 °C) replaces them, and freezing is scheduled into the coldest hours. That gives 6-9 kJ per kg of ice, enough for 42-63% of electrowinning power at Udachny-type cold but only 24-44% at Chara (Udokan). A richer 10 g/L leach solution cuts ice from 492 to 123 kg per kg Cu and the freeze step to $105-165/t Cu, but then the engine covers only about 12% of electrowinning power.
VALUE: At 2.5 g/L the route is 0.56-0.86x as cheap as grid-powered SX-EW at Udokan (i.e. dearer) and 0.83-1.08x at an off-grid diesel site; only an off-grid, low-Mg, 10 g/L case reaches about 1.1-1.4x cheaper.

IDEA 3
NAME: Self-Charging Frost Separator Cascade
MECHANISM: Anchor kept: grains charge themselves on the chute lining, and the bins that catch them, wired across to the opposite plates, build the separating field with no power supply, like a Kelvin water dropper. The field is reset to 150 kV/m across a 0.5 m gap (75 kV, 5% of air breakdown), which gives 17-23 cm of drift per side in a drag-included simulation without grains hitting the plates (200 kV/m would hit them). The sorted charge delivers only 0.4-1.4 µA per metre of plate width, so self-excitation needs at least 5e10 Ω of leakage resistance per 10 m channel. Space charge caps each channel at 0.17-0.5 t/h per metre of plate width, so each stage is a stack of alternating-polarity plates at 0.5 m pitch: 170-525 channels, each 10 m wide, for 1 Mt/yr. Ore moisture is removed by a closed air loop through an outdoor cold trap at -30 °C, which gives 2% RH at the separator. Mill heat and diesel-generator waste heat supply the drying heat: 9-19 MJ/t at 0.2-0.4% ice, 47 MJ/t at 1% ice. With middlings recycled, eight stages reach 6.2% Li2O at 82% recovery only if each stage sends forward 85% of the spodumene and 45% of the waste. A 80/50 split needs 22 stages and 23x circulating load, and a 75/55 split cannot reach 6% at all.
VALUE: $4,100-4,960 per t of Li2O recovered at the railhead, against $6,430-7,390 for XRT sorting plus DMS (the cheapest real alternative) and $7,400-8,270 for Arctic DMS plus flotation, so 1.3-1.8x cheaper, and only if a measured per-stage split of 85/45 or better holds.

IDEA 4
NAME: Night-sky lithium freeze cascade
MECHANISM: The anchor (night-sky cooling that drives CaCl2 brine below its -50 °C eutectic) cannot be rescued. Even with a heat pump rejecting to -40/-45 °C air, it needs 5.5-15 MWh per t LCE and must freeze 450-910 t of brine per t LCE, and the leftover liquor is still about 30% CaCl2, so DLE is still needed. Above the eutectic, cold concentrates lithium only 1.25x. The surviving niche keeps only "Arctic cold concentrates lithium" and applies it to Ca-free sorbent eluate. Reverse osmosis first takes the eluate to 6 g/L Li (37 bar osmotic pressure). Two stages of spray freezing (snowmaking guns rather than trays) then take it to 20.6 g/L by draining the unfrozen brine and collecting the early melt. That moves 53% of the Li per pass, needs 62 t of ice per t LCE, and gives a product that freezes at -14 °C. Late melt at ≤1.1 g/L Li goes back to the RO feed, so no lithium is lost in the ice, and winter-only freezing needs 0.37 Mm³ of stored RO concentrate, not 2.2-7.3 Mm³.
VALUE: $110-240/t LCE against $470-1,085/t LCE for the MVR evaporator it replaces (2-4x cheaper for that step), but that is only 5-15% off the $3.4-6.2k/t LCE whole route, and the night-sky/eutectic anchor is not used.

=== NOTES ===
All calculations are in `/home/user/SomeRepository/engine/runs/permafrost/round2/rt_a/calc/idea1.py`, `idea2.py`, `idea3.py` and `idea4.py`. The round log and consistency tables are in `/home/user/SomeRepository/engine/runs/permafrost/round2/rt_a/LOG.md`. Hourly climate data was unreachable (Open-Meteo, NOAA and Wikipedia all blocked), so hours below each temperature are estimated from monthly means with a 5-8 K hourly spread. The Chara monthly means come from a Wikipedia search snippet.

**IDEA 1: FAILS** (the physics and planned-vent safety can be designed; the value cannot)
- **Anchor kept?** Yes.
- **Decisive numbers.**
  - Line holds 888 t Ni(CO)4 (0.41 t/km); transit time 3.0 days.
  - CO needed to keep the carbonyl stable: 0.032% at 50 °C, 0.114% at 80 °C (using the reviewer's ΔH 161 kJ/mol, ΔS 410 J/mol·K).
  - CO consumed: 2.51 t per t Ni, against a floor of 1.91.
  - Polisher residual: 0.09 ppb at 250 °C.
  - Half-life in air: about 40 s (Wikipedia), under 1 min (INERIS). The National Academies chapter says the breakdown is slower when CO is present.
  - Mobile compressor pump-down keeps up to 80% of a section's gas (Gazprom figures, via compressortech2).
- **Best baselines ($/t Ni delivered).**
  - Ship pellets from an on-site carbonyl refinery: about $100. The decomposer exists in both routes, so it cancels.
  - Ship 70% Ni matte: $150 (reviewer).
  - Truck concentrate: $1,067. Kun-Manie's study plans 350 kt/yr of concentrate, 24.3 kt payable Ni, and a 338 km road to the BAM railway.
  - The pipeline route costs $109-947. Nickel transport is about 0.9% of the nickel price, so even a win would barely matter.
- **Reviewer defects.**
  - FATAL (toxic inventory and vents): planned vents fixed by purge plus pump-down. Rupture risk is conceded. Offtakes are fixed only by shortening the carbonyl-laden run, which cuts the value.
  - CO and displaced-gas cost: conceded, recomputed above.
  - Slip into sales gas: fixed by the 250 °C polisher.
  - No sulfur-free feed near a trunk line: conceded.
  - Fe(CO)5 from pipe steel: the lower CO pressure (0.088 bar) cuts equilibrium Fe(CO)5 about 13x, but it is still favoured; the rate is unknown.
  - Recuperator: conceded and not costed.
  - Transport baseline: accepted; matte and pellets are now the baseline.
- **Consistency check.** Fails on rupture inventory and on site (no nickel source on any trunk line). Requires discharge ≤50 °C.
- **Hazards.** Ni(CO)4 (IDLH 2 ppm; it reaches IDLH at 0.5% gas in air, 10x more dilute than the flammable limit); about 0.21% CO left in sales gas.
- **Deciding unknown and experiment.** Plume decay rate with CO present. Test in a 1 m³ chamber: 3 temperatures x 3 CO levels x 5 replicates = 45 runs. Economically, a CO cost under $56/t is needed, which in practice means free by-product CO.
- **Closest existing work.** Inco/Vale carbonyl refining; methanol injection into gas lines.

**IDEA 2: NICHE** (fails at Udokan; about parity to 1.4x only off-grid)
- **Anchor kept?** Yes.
- **Decisive numbers.**
  - n-butane vapour pressure (NIST Antoine): 0.97 bar at -2 °C, 0.30 bar at -30 °C. Turbine exhaust is 309 m³/s.
  - Ice per kg Cu: 492.
  - Net work: 3.3 kJ per kg ice with fans at -35 °C; 6.4-9.2 kJ with natural draft.
  - Electrowinning taken as 2.0 kWh/kg Cu.
  - SX step cost: $236-555/t Cu. Basis is USGS SX-EW capex of $1,500-3,700 per t/yr (1991), doubled for escalation, with 40% of it assigned to SX.
- **Best baselines.** SX-EW on grid at Udokan: $606-925/t Cu, against $1,081 for this route. SX-EW on diesel: $1,086-1,405, against $1,306.
- **Reviewer defects.**
  - FATAL propane hydrate: fixed with n-butane.
  - Too few -35 °C hours: recomputed; coverage is 24-63% of electrowinning power.
  - Fan power: natural-draft tower.
  - Grid at Udokan: accepted, and the route loses there.
  - Scale and capex precedent: conceded. The wash column is dropped (capex $63M to $41M) because ice purity does not matter: entrained liquor goes back to the heap.
  - MgSO4 saturation: feed Mg must stay ≤0.39-0.73 g/L with the mother liquor bled (about 1-2% of the volume) and its copper recovered by cementation. This limits it to low-Mg oxide ore.
  - 90% recovery: conceded.
  - Acid pond on permafrost: 1.2-5 Mm³ per 10 kt Cu, double-lined; risk conceded.
- **Consistency check.** Fails at 90% recovery. Natural draft works only in air at or below -25 °C. Flammability risk from butane under vacuum.
- **Hazards.** Air leaking into a butane loop that runs below atmospheric pressure; the acid pond.
- **Deciding unknown and experiment.** Copper solubility and Mg uptake into crystals at -1 to -15 °C in acidic liquor. Bench butane freeze-crystallisation on real leach liquor: 3 acid x 3 Mg levels x 3 replicates = 27 runs, plus 10 hydrate-free runs of 48 h each.
- **Closest existing work.** Butane freeze-desalination pilots (US patents 3992170, 3616612; Blaw-Knox 35,000 gpd pilot); eutectic freeze crystallisation.

**IDEA 3: NICHE** (1.3-1.8x, conditional on the measured split)
- **Anchor kept?** Yes. Searches found no self-excited separator. Free-fall electrostatic tests on spodumene ore are already known (Leoben 2018, Haas thesis, Koralm ore).
- **Decisive numbers.**
  - Drift: 17-23 cm per side at 150 kV/m.
  - Charging current: 0.4-1.4 µA per metre; leakage resistance needed ≥5e10 Ω per channel.
  - Throughput: 0.17-0.5 t/h per metre of plate width.
  - Fresh granite absorbs ≤0.4% water (stonespecialist), so pegmatite ice is about 0.2-0.4%.
  - Generator waste heat is about 97 MJ/t of ore at 15 kWh/t.
- **Best baselines.**
  - XRT plus DMS: $6,430-7,390 per t Li2O.
  - DMS plus flotation: $7,400-8,270.
  - These processing costs are my own estimates, anchored to Ewoyaa (C1 cost $377/t of concentrate) and Bougouni (DMS capex $65M per 1 Mtpa).
- **Reviewer defects.**
  - Drift at 45 kV: fixed.
  - Wet permafrost ore: cold-trap air loop plus waste heat, up to about 2% ice. At 3% ice it fails.
  - Split assumed, not measured: conceded and decisive.
  - Space charge: treated as sizing, with 1,730-5,250 m of plate width.
  - Mill heat too small: generator waste heat covers it.
  - "Never tried": the separation is conceded as known; the self-excited field is still new; XRT sorting added as a baseline.
- **Hazards.** 75 kV static discharge; respirable quartz dust from dry grinding.
- **Deciding unknown and experiment.** The per-stage split (85/45 needed). Lab free-fall separator with Faraday-cup charge measurement on ≥200 grains per mineral: 3 sizes x 3 temperatures x 10 runs of 5 kg = 90 runs. Also measure the leakage resistance of one 10 m channel at 75 kV.
- **Closest existing work.** K+S ESTA free-fall separation of potash (US patents 4276154, 4743362); TOMRA XRT sorting.

**IDEA 4: FAILS** for the anchor; **NICHE** only without it
- **Anchor kept?** No (conceded).
- **Decisive numbers.**
  - Heat-pump variant: COP 4.9-6.5.
  - RO osmotic pressure: 37 bar at 6 g/L Li, 62 bar at 10 g/L.
  - Field data on spray-frozen water (wastewater and snowmelt, not LiCl): more than 50% of impurities leave with the unfrozen water (Gao 1998, U Alberta), and up to 90% of chloride comes out in the first 19% of the melt.
  - MVR uses 20-60 kWh per m³ evaporated (vendor figures, Shachi). The MVR capex of $1-1.5M per m³/h is my assumption.
  - CleanTech's pilot RO took eluate from 710 to 2,194 mg/L Li.
- **Reviewer defects.**
  - FATAL anchor cost: conceded.
  - Ice growth per square metre: fixed with spray piles (6-22 snowmaking guns for 20 kt LCE/yr).
  - Lithium trapped in ice: the late melt is recycled to the RO feed; per-pass yield is 53%.
  - RO as the real competitor: RO now runs first.
  - Summer storage: 0.37 Mm³.
- **Consistency check.** The product needs air at or below -26 °C: fine at Udachny in December-February, marginal at Chara. The partition data come from NaCl wastewater, not LiCl, so they are unverified here.
- **Hazards.** Ice-pile stability; brine leaks; LiCl spray drift.
- **Deciding unknown and experiment.** The share of lithium that drains out and comes out in the early melt, for LiCl at 6-13 g/L. Field spray test: 3 temperatures x 2 concentrations x 5 piles of about 5 m³ = 30 piles.
- **Closest existing work.** U Alberta spray freezing of wastewater; RO and osmotically assisted RO (OARO) concentration of DLE eluate.

Sources:
- https://en.wikipedia.org/wiki/Nickel_tetracarbonyl
- https://www.ineris.fr/sites/ineris.fr/files/contribution/Documents/19_NICKEL%20v1.pdf
- https://www.nap.edu/read/12018/chapter/13
- https://compressortech2.com/news/gazprom-to-expand-mobile-compressor-station-fleet/8016221.article
- https://www.miningweekly.com/article/kun-manie-nickelcopper-sulphide-project-russia-update-2023-03-10
- https://patents.google.com/patent/US3992170A/en
- https://pmc.ncbi.nlm.nih.gov/articles/PMC10666149
- https://search.library.wisc.edu/digital/A5X7AVV22D2URO8R/text/AN4RFDJGCJFGCF9D
- https://pureadmin.unileoben.ac.at/portal/en/publications/analysis-of-a-spodumene-ore-in-regard-of-its-processability-by-dry-processing(a0a6f31a-7e73-4c3d-bb0b-fca82deb2b4f).html
- https://patents.google.com/patent/US4743362
- https://stonespecialist.com/news/ask-expert-granite-frost-resistant
- https://www.miningweekly.com/print-version/costs-rise-at-ewoyaa-as-dfs-is-delivered-2023-06-29
- https://www.investegate.co.uk/announcement/rns/kodal-minerals--kod/bougouni-project-dms-development-opportunity/7169037
- https://era.library.ualberta.ca/items/2fbe4d5e-adfe-44b2-87cd-0eea3caf7659/download/9bff151f-1ae1-4aca-898a-2b38653df3f9
- https://www.globalminingreview.com/mining/14052024/cleantech-lithiums-dle-pilot-plant-produces-high-quality-eluate/
- https://lilacsolutions.com/news/the-eluate-advantage-how-dle-output-drives-project-costs
- https://www.shachiengineering.com/wp-content/uploads/2023/02/Self-cleaning-evaporator-driven-by-MVR-–-the-way-to-go_Shachi_2021.pdf
- https://en.wikipedia.org/wiki/Chara_(rural_locality)