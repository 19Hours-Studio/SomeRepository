# Repair log, run b (one line per round: idea | change | decisive number | result)

Scripts: idea1_deflation.py, idea2_oreicedam.py, idea3_pond.py, idea4_pods.py (outputs in out_idea*.txt).
Web fetch was blocked by the proxy, so sources are the WebSearch summaries listed at the bottom plus standard textbook formulas.

## Idea 1: Winter Wind Deflation Placer (anchor: cold dry wind freeze-dries frozen pay gravel by sublimation and blows away the freed light grains, with no liquid water)
- R1 | original: midwinter central Yakutia (-40 C, 1.5 m/s) | coupled energy-balance sublimation 0.014-0.041 mm w.e./d, which frees 0.05-0.15 mm/d (not ~1 mm/d) and needs ~5 km2 per 100k m3 | FAILS by 7-20x on rate
- R1b | model check | windy polar night gives 0.12 mm/d against 0.08-0.15 measured on Alaska tundra; calm Yakutia gives 0.04 against 0.01-0.05 for Siberian midwinter; CRREL tunnel 0.058 cm/month | model OK
- R2 | windy Chukotka/Arctic coast, January | 0.12 mm w.e./d, 0.44 mm/d freed (0.87 mm/d if the ground was drained in autumn); a dry layer of 3 mm cuts it 4x | still too slow on its own
- R3 | move the season to spring (Mar 15 to May 10): sun on dark harrowed gravel (albedo 0.2), still freezing | April 0.42-0.68 mm w.e./d, 2.5-5 mm/d freed; surface melts at noon after about May 10 (Ts +3-4 C) | rate OK
- R4 | in place on the stripped cut, active layer drained in autumn (ice 0.15), lag raked into windrows every day | 23 mm w.e. per season = 0.16 m, plus 0.05 m from midwinter wind = 0.21 m/yr; 0.49 km2 per 100k m3/yr | area OK
- R4b | wind sorting (Shao & Lu 2000) | at U10 7 m/s quartz 25-500 um leaves and no gold moves; cassiterite <177 um is lost; at 10 m/s gold <135 um is lost | harrow only when U10 <= 7-8 m/s
- R5 | cost, keeping -10 mm residue so 2-10 mm nuggets are kept (25% of volume washed clean in summer) | in place $1.69/m3 vs $6.0/m3 now (1.2 L/m3 x $1.5/L / 0.30 fuel share) = 3.6x; on a pad for thick virgin pay = 2.1x | WORKS best on exposed old tailings dumps and thin-overburden placers in windy tundra
- hazard | about 54 kt of <0.5 mm fines per 100k m3, about 31 kt of it silt dust | fences and a trench catch the saltating sand; site the pad so its downwind sector drains to the mine settling pond

## Idea 2: Self-feeding ore-ice dam (anchor: the frozen ore pile is itself the water-holding structure, and stored warm water melts its face at a flow-set rate)
- R1 | thermal check | 101 MJ/m3 (ice 0.30) means 4.3-7.6 m3 water per m3 gravel at 8 C, inside the sluicing range (2.2 m3/m3 in a real placer) | self-dosing holds
- R1b | heat-transfer area | face capacity 560-3700 m3/h against 28 m3/h needed, so feed = flow x temperature, as claimed | OK
- R2 | water source | 60k m3 per season needs 47 L/s (creek baseflow from 5-9 km2); holding all season's water in the basin = 0.36 Mm3 | swap the big basin for a forebay
- R3 | split the structure: permanent frozen core (0.8-1.0 m saturated peat; Stefan thaw 0.52-0.63 m per 100 d) plus a sacrificial ore buttress downstream (75 m thick, retreating 0.83 m/d) | dam-break peak 460 falls to 128 m3/s | safer
- R3b | cost, summer-mined gravel built up in autumn | $5.10 falls to $2.28/m3 = 2.2x (dozer placement is the same as feeding) | not several times
- R4 | strongest regime: winter (underground) placer mining, where the hoist already builds a frozen stockpile that today is thawed with steam or sprinkling, ripped and fed | $6.66 falls to $1.32/m3 = 5.0x on the washing stage | WORKS in that niche

## Idea 3: Self-sorting wave-and-ice pond (anchor: the placer's own pond sorts it in place; bottom-fast winter ice freezes onto the stones and floats them off)
- R1 | waves (CEM fetch-limited, F 500 m, U 12) | Hs 0.14 m, bottom orbital 0.03 m/s at 1 m depth; seepage pumped by waves 6e-4 m/s against fluidisation 0.018-0.11 m/s | wave jigging FAILS (30-100x short)
- R1b | fines leaving over the spillway | 0.07-0.35 kg/m2/yr against 760 kg/m2 of fines, i.e. 2,000-11,000 years (18-88 yr even with the creek routed through) | FAILS
- R1c | thaw under the pond | 1.4-2.25 m per summer | works, but water thawing is known practice
- R2 | ice rafting, buoyancy-limited | natural ice 1.56-1.83 m lifts 0.08-0.09 m3 stone/m2/yr; flooding the ice 1.5 m thicker gives 0.15-0.17 | slow but real
- R2b | value if only the oversize goes | washing cut to 65-80% of volume = 1.25-1.5x | not several times
- R3 | niche: freeze-and-float clearing of boulders (bouldery placers that dredges reject); time the pond depth so ice reaches the boulder tops in March, over a still-thawed talik | about $1.1/m3 of boulder against about $6 to drill, blast and doze (assumed) | NICHE
- R4 | where sorting would work | needs a fetch of 10 km or more (Hs 0.6 m, u 0.6 m/s at 1.5 m), which is a natural shore, i.e. ordinary beach-placer genesis | not novel

## Idea 4: Snow-buoyed ice-shell ore pods (anchor: ore plus dry snow sealed in an ice shell, carried by the under-ice current, with no vessel and no return)
- R1 | buoyancy | snow per tonne: coal 0.28 m3, rock 0.74, sulphide 0.86 (claim of ~1 m3 holds) | OK
- R1b | sliding under the ice | 1 t cube at 0.1-0.3 m/s tolerates only 1.3-12 kg net buoyancy at mu 0.5 (ice-ice near 0 C, slow); stopped pods freeze in at 1-1.9 cm/day | original FAILS (pods stall and freeze in)
- R2 | almost neutral pod: trimmed in the slot with a crane load cell to +3..+9 kg; broadside fin shape | drag 169 N at 0.16 m/s > B*g, so the pod dives under roughness | sliding OK where section velocity >= 0.2 m/s
- R3 | melt and route | +0.01 C water melts 6 cm in 45 d (shell 8-10 cm); 700 km takes 41-68 d | fits a Nov-May season
- R4 | 10 t pods (5.0 x 2.2 x 1.2 m), 6 pods/h per slot | 144 kt per 120-day season, $7.3/t including 5% loss | 8-24x cheaper than winter road over 500-1500 km; 1.7-5x vs summer barge
- R5 | strongest regime: coal (least snow), regulated rivers below HPPs (Kolyma, Vilyuy, Yenisei) with strong winter flow, smooth thermal-ice reaches | loss rate unknown | NICHE-to-WORKS; needs a tracked trial of about 20 pods

## Sources (WebSearch summaries)
- Siberian midwinter canopy-snow sublimation 0.01-0.05 mm/d; eastern-Asia snow 0.2-1.0 mm/d when windy; Alaska tundra mean 0.08-0.15 mm/d (openpolar.no hyp.6675, hyp.1183; tc-19-1739-2025)
- CRREL SR 81-8 (Johansen et al. 1981): dried silt layer grows 0.058 cm/month in the permafrost tunnel; Douglas & Mellon 2019 Nat Commun: a lag slows sublimation
- Residual aeolian placers (AusIMM NZ 2004); dry concentrators recover 10-15% less than wet (911metallurgist); drying the feed is the known difficulty
- Shao & Lu 2000 saltation threshold; USACE CEM fetch-limited wave growth; Ergun; Stefan; Froehlich 1995 breach peak
- Douglas et al. 2023 JGR-ES: ablation-limited permafrost bank erosion is linear in water T and falls with pore ice; about 3x higher than smooth-wall theory
- zolotodb.ru/article/213 (2,200 L water per m3 sands); zolotodb 10674 (washing cost 133-183 rub/m3 at 360 rub/g gold, i.e. 0.37-0.51 g/m3); trud.igduran 2023 (water supply is 60-100% of wash-plant energy)
- Yukon placer income model 2008 (65-130 kL diesel per season for <40k to 200k m3); YGS placer overview (fuel ~30% of mining cost)
- Kolyma memoir (Escape from the Future): winter-mined sands piled up and thawed with steam hoses; Lund 1951: creek water at summer temperature is the cheapest thawing medium
- Lena delta under-ice currents 5-25 cm/s, lake ice >1.5-2 m, lake water up to 23 C in summer
- Ice friction near melting rises at slow speed and with hold time (Schulson; JAP 2004 crossover ~0.01 m/s; PRX 2021)
- Truck rate 69.6 rub/truck-km in 2024 (Monopoliya, retail.ru); Manitoba: winter-road freight +60% vs all-weather road
- Ice-push boulder ridges sorting cobbles from 1-2 m depth (Arctic 35(2):312, 1982); 1869 account of river ice carrying granite blocks
