# NOTES: sources, consistency tables, hazards (calc.py holds every computation)

## Sources found this session (S#); [REF] = textbook value, not fetched; [ASM] = assumption, swept in calc.py
- S1 Creighton et al. 2018, TEM talik under a thermokarst lake: 91 m (thermal model 80 m). epic.awi.de/id/eprint/49565
- S2 SPbU, Arctic limnosystems: talik ~25 m under a Yakutian lake, ~10 m under a Yamal lake; ~2 m of ice. pureportal.spbu.ru
- S3 ETKS dredge-worker duties: cutting trenches in the ice around the pontoon, removing ice and shuga in winter, freezing out the pontoon. ppt.ru/classifier/etks/drager-5
- S4 SIBRAN, winter shelf-placer technology: the Nome (Alaska) shelf dredge has worked at 9-12 m since 1986. sibran.ru
- S5 SFU 2023, hangar-type cover over a dredge pit to lengthen the season. scholar.sfu.ru/publication/50731330
- S6 AIME 1954 "Arctic Gold Dredging": insulated double walls and heating; the stacker is the most vulnerable part. onemine.org
- S7 Yukon Geological Survey: excavator plus floating plant, US$0.90 per loose yd3 processed; 1997 Fortymile floater, ~$1/yd3 excluding stripping. open.yukon.ca
- S8 ZabGU method: hydro-needle thawing uses ~10 m3 of water per m3 of ground (216,000 m3 for 21,600 m3)
- S9 Nafikov (SFU) dissertation: the dredge season in the Far North is 160-180 days, and cold raises costs.
- S10 E3S 2020 (Yakutia Regional Energy Commission data): delivered coal 3.5-25 k rub/t, 3-8x the shipping-point price, 2,000-3,000 km routes, delivery up to 2-2.5 years
- S11 ЖКХ РС(Я) tender: 100,778 t to the Abyy, Verkhnekolymsk, Srednekolymsk and Nizhnekolymsk coal depots, starting price 701.57 Mrub, i.e. 6,962 rub/t delivered (saby.ru tender 245260724)
- S12 yk24.ru / news.ati.su 2025: Verkhoyansk district burns 77 kt/yr; the Yana and Indigirka are too shallow, so coal moved to the Dzhebariki-Khaya to Batagay winter road (~32 kt, >260 Mrub saved)
- S13 EBRD 2012: fuel plus transport are 75% of heat operating costs in northern Sakha.
- S14 Yakutsk retail coal 4.5-9.5 k rub/t; Kuzbass FCA 1.0-1.45 k rub/t
- S15 crushed-rock revetment (CRR) cools permafrost by winter convection; recommended >80 cm on south slopes, 1.0-1.5 m (CRST 2006; ACCR 2022; GEO2010)
- S16 a 5,000 t barge cost ~$3 M (Ukraine, 2020); Russian shipbuilding costs 2.5-3x Chinese (gazeta.ru 2025)
- S17 Akademik Lomonosov floating NPP at Pevek: 70 MWe, 50 Gcal/h of heat
- S18 ETH HEAP (Science Robotics 2023): an autonomous 12 t excavator built a 6 m x 65 m dry-stone wall from multi-tonne boulders; placement rate not published
- REF: Stefan ice-growth law with snow coefficient 0.017-0.024 m/sqrt(degC·d); Lachenbruch 1957 lake-talik solution; Maykut 1978 lead heat loss 400-700 W/m2; SP 25.13330 long-term adfreeze ~0.2 MPa at -2..-3 C; Caterpillar handbook dozer fuel 55-75 l/h
- ASM (swept): dredge 1 Mm3/season, 1.1 MW; unit costs in rub/m3; diesel 90 rub/l; grade; river freight 3-5 rub/t-km (the ideas' own figure, not verified); barge, boiler and heat-main capex

## Consistency tables (limit | value relied on | computed rate x duration | ok?)
IDEA 1
| limit | design value | check | ok |
|---|---|---|---|
| lake must not freeze to the bottom | depth >=2 m | max ice 1.2-1.9 m | yes, with >=0.1 m margin; choose >=2.5 m |
| talik reaches bedrock | R>=50 m | steady 15-22 m; >=45 yr to reach 15 m | yes for lakes >=100 m across that are older than ~50 yr |
| dredge reach | 250 L class ~18 m | water+silt+pay 9-14.5 m | yes; deep basins (24-42 m) need 380-600 L dredges |
| winter pond heat | <=1500 m2 open | 0.69-0.81 MW vs 0.99 MW waste heat over 150 d | yes for diesel-electric dredges; no for grid-fed (+41-49 rub/m3) |
| sheet ice ahead | sawn, not melted | 300-850 m3/d; ~500 m of cut per day | yes (one ice saw per shift) |
| season | 300 d at 0.7 winter productivity | vs 160-180 d (S9) | assumed; pilot must measure it |

IDEA 2
| limit | design value | check | ok |
|---|---|---|---|
| jacked face strength | long-term frozen silt ~1 MPa [REF] | 0.11-0.23 MPa | yes, FS>4 |
| reaction (next block's frozen base) | 0.2 MPa x A | FS 3.5 with flooded kerfs, 1.7 dry | only flooded; next block's pay thawed only after the push |
| summer water window | ~80 d of creek water >4 C [ASM] | cycle 13-31 d per row | 2-6 blocks per row; drill-limited set of 6-18 blocks per rig |
| slot refreeze | 0.2 m slot | ~1.2 d | slots flushed with creek water |
| diesel claim 0.1 l/m3 | kerf + jack | 0.12-0.23 l/m3 | ~0.12-0.15 only with 40 m blocks |

IDEA 3
| limit | design value | check | ok |
|---|---|---|---|
| in-place restack balance | swell 0.4 | overburden/seam <=2.5 | site rule |
| dry-stone rate | 5-30 m3/h | 7.8-94 kt/season cap | needs >=15 m3/h for 40+ kt |
| navigation | ~110 d, 60 mining d | 24-56 kt/season | yes |
| water depth at the face | outer-bend bluffs | deep channel at cut banks | yes, check each site |

IDEA 4
| limit | design value | check | ok |
|---|---|---|---|
| draft vs river | <=1.5 m | 8 kt hull 3.9 m; 2 kt 100x22 m hull 1.26 m | only the 2 kt hull fits |
| absence window | ~1 Jun - 1 Sep = 92 d | trip 12-22 d | yes in the sub-Arctic; no where summer heating is needed |
| bunker vs demand | 2 kt | 1.3 MW mean, 3.2 MW peak, 270 d | ~300-700 people per barge |
| capital | used hull 30 Mrub | 2,250 rub/t, or ~0 with summer charter | new hull (+11,250 rub/t) fails |
