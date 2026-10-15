# NOTES (scripts: idea1_deflation.py, idea2_icedam.py, idea3_icefloat.py, idea4_pods.py; outputs *_out.txt)

## Sources used
- Pevek normals: Wikipedia climate table (Mar -21.4, Apr -14.3, May -2.2 C mean; May mean max +1.0 C). Spring is the driest season, with 2-3 wet days a month (kupi.com).
- Measured surface sublimation of Arctic snow: 0.06-0.07 mm/d (North Slope, eddy covariance) and 0.08-0.15 mm/d (6 sites, tc-2023-153).
- NOAA GML Barrow snow cycle: tundra snow-off is in early June.
- Lena delta under-ice velocity, Apr 2019: main channel 0.12-0.18 m/s, Bykovskaya 0.20-0.25, Olenekskaya 0.05-0.11 (Fedorova et al. 2020, E3S Conf 163:05003).
- Krasnoyarsk tailwater 40 km below the dam: still about 2 C off the natural winter temperature (Tech. Phys. 2025, via search). The Yenisei does not freeze near Krasnoyarsk.
- Sluicing water: about 3 m3 per m3 (kuzstu 2023). Plant throughput 1,118-1,458 m3/d (trud.igduran 52/50).
- Russian AISC $1,018/oz in 2022 (WGC). Polyus Lena alluvials grade about 0.6 g/m3 (9.8 Mm3). So all-in cost is about $20/m3, and feed+wash is about $5-7/m3 (derived).
- D375A new price 96-156 Mrub (drom.ru); dozer operator 230 krub/month (hh.ru). From these: D375-class about $160/h, loader about $70/h.
- Snow viscosity: Vionnet et al. 2012 (Crocus). Grain thresholds: Shao & Lu 2000. Flux: Kawamura. Snow fences: Tabler, capacity 8.5 H^2.2 t/m. Breach peak: Froehlich 1995. Ice growth: a*sqrt(FDD), a = 2.0-2.7.
- Precedents: Reimnitz et al. 1987 (anchor ice rafts seabed sediment); High-Arctic lake diamicts rafted when meltwater lifts the ice; Lake Hoare floating boulders; historic Klondike/Alaska ground sluicing; Russian hydro-thawing (гидрооттайка).
- Estimates (not sourced, marked as such): $0.03/t-km for summer barges, tractor at $90/h, crane and slot costs.

## Consistency tables (summary)
### I1 (Pevek, albedo-controlled)
| limit | value | over the season | ok? |
|---|---|---|---|
| surface Ts < 0 C (no liquid) | dark surface melts from about doy 118 | the window is doy 74 to about 130 with albedo raised to 0.3-0.55 | OK only with control |
| net sublimation | 0.0-0.28 mm/d before mid-April, 0.4-0.6 mm/d for about 2 weeks | 13 mm w.e. gross per season | claimed 22-39 mm: FAIL, now 13 |
| dry lag < 1 mm | 1 mm halves the rate | daily rake | factor 0.6 |
| snow on field | spring snowfall about 10 mm w.e. | blade pass after each event | OK at a cost |
| drift | 3-18 t/m in spring | fence 0.6-1.4 m (Tabler) | OK |
| gold not suspended | Stokes 0.6-6.6 m/s against u* 0.3 | always | OK |
| gold not saltating | flakes u*t 0.23-0.32 against u* 0.26-0.30 at 6-7 m/s (0.39-0.46 in gusts) | gusts exceed it | FAIL, so a downwind trap lip is needed |
| fetch | capacity 0.12-0.36 t/m/d against supply 1.0 kg/m2/d | strips 120-350 m across the wind | OK |

### I2
| limit | value | ok? |
|---|---|---|
| water per m3 equals sluice need (2-6) | loose pile at 5-7 C gives 2.2-3.2 | OK (above 9 C it is <2: blend cold water) |
| face heat transfer | 70 m/d capacity against 0.8 m/d | OK |
| watertight | loose pile self-seals only 5-16% of voids | sprayed skin needed |
| skin thaw from forebay | peat blanket 0.42 m per 90 d < 0.8-1 m | OK |
| sliding (3 m forebay) | thrust 44 kN/m against about 235 kN/m friction of skin+peat, FS about 5 | OK; >6 m head FS about 1.3, so keep the forebay at 3 m or less |
| breach | 34 m3/s (8,000 m3, 3 m) | OK with a spillway channel |

### I3
| limit | value | ok? |
|---|---|---|
| floe buoyancy against frozen-on gravel | March contact: 402 > 141 kg/m2 | FAIL |
| drawdown contact about Apr 25 | 46 kg/m2 of gravel, net 0.058 (1.7 m) / 0.133 (3.2 m) m3/m2 | OK |
| breakout of 0.8 m boulder | 5-9 m2 of floe each | OK for 10-20% cover |
| talik under the pond until drawdown | water deeper than ice until Apr 25 | OK by design |

### I4
| limit | value | ok? |
|---|---|---|
| trim window +3..+9 kg | melt -196 kg; creep up to kg/d-scale; air 521 kg/m | FAIL |
| water 0.00 C | +0.5 C melts 8.5 cm/d | FAIL near dams |
| rolling (repair) | needs mean 0.2-0.4 m/s; keels need 0.6-1.0 m/s | measured 0.05-0.25: FAIL |
| creep (repair, 550 kg/m3, cold-sealed) | 0.6-1.4% per 45 d, about 100 kg < 750 margin | OK |
