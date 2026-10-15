=== IDEAS ===
IDEA 1
NAME: Albedo-steered freeze-dry deflation placer
MECHANISM: Anchor kept: in spring, cold dry wind freeze-dries frozen pay gravel by sublimation and blows away the freed fines without any liquid water, leaving the heavies behind as a lag. An hourly energy-balance model for Pevek shows the claimed 0.4-0.7 mm w.e./day holds for only about 2 weeks. A dark surface begins melting around Apr 28 (7-24 mm/day of melt in May). The repair is to steer the albedo: keep the surface dark while it is cold, then leave the raked, lighter lag (albedo 0.3-0.55) once the surface nears 0 °C. This keeps the surface below 0 °C and gives 13 mm w.e. per season (48 days), times 0.6 for the dry-lag penalty (1 mm of dry grains halves the rate). That frees only 58-109 mm of gravel per year, depending on pore ice of 8-15%, so 100,000 m³/yr needs 0.9-1.4 km² of wind-scoured bench or dump surface. The site also needs a blade pass after each snowfall (spring snowfall of about 10 mm w.e. equals the whole budget), 0.6-1.4 m snow fences, and a low saltation-trap lip downwind. The trap is needed because gold flakes start moving at u* 0.23-0.32 m/s, the same as sand, although gold never goes into suspension (Stokes settling 0.6-6.6 m/s).
VALUE: About $3.7-4.5 per m³ processed (about $8-9 per g recovered at 0.6 g/m³) against $6.0/m³ (about $12.5/g) for bulldozer-sluice washing, so 1.3-1.6x cheaper, not 3.6x; on old tailings it is only about 1x.

IDEA 2
NAME: Self-feeding ore-ice buttress dam
MECHANISM: Anchor kept: the frozen ore pile holds the forebay water, and warm water run over its downstream face thaws it, so feed = flow × ΔT / thaw energy. The regime where this is strongest is a loose winter-hoisted pile (bulk ice 0.15, 50-55 MJ/m³). With creek or forebay water at 5-7 °C it needs 2.2-3.2 m³ of water per m³, which matches what a sluice needs (about 3 m³/m³). The original ice-cemented pile (101 MJ/m³) needs 3.8-8 m³/m³ and is water-limited. A loose pile leaks: its cold content refreezes only 5-16% of its voids. The repair is a 3 m upstream ore skin, spray-sealed in winter (a 0.4 m lift freezes in 10-19 h), under a 0.8-1 m saturated-peat blanket that thaws only 0.42 m in 90 days. The forebay is kept at 3 m or less (sliding safety factor about 5, Froehlich breach peak 34 m³/s against 144 m³/s for a season-long reservoir). Above 8-9 °C cold creek water is blended in, because the water ratio would otherwise fall below 2. The face can thaw about 70 m/day, against the 0.8 m/day needed.
VALUE: Summer washing of winter-mined stockpiles costs about $2.0/m³ ($2.95/g at 0.8 g/m³) against about $4.65/m³ ($6.8/g) for natural thaw plus dozer ripping plus loader plus pumped sluice, or for hydromonitor plus gravel pump, so 2.3x cheaper (not 5x).

IDEA 3
NAME: Drawdown-timed ice boulder lift
MECHANISM: Anchor kept: bottom-fast pond ice freezes onto the boulder tops and a spring water rise floats them off. The original timing (ice reaching the boulders in March) fails. The remaining 775 °C·days of frost freeze 39 cm of gravel onto the floe base, a load of 402 kg/m² against 141 kg/m² of buoyancy, so the floe stays grounded. The repair keeps the pond deeper than the ice until about Apr 25, then draws it down so the ice settles onto the boulders for the last 91 °C·days only. That freezes on only 4.4 cm of gravel, so 1.7 m natural ice lifts 0.058 m³/m² of stone and 3.2 m flood-built ice lifts 0.133 m³/m². A 0.8 m boulder needs 5-9 m² of floe to break out, so only a surface boulder armour of about 10-20% cover can be cleared, not boulders buried in the pay. Floating strips 30 × 100 m are sawn and winched into a dump bay.
VALUE: About $5.1-5.7 per m³ of boulder against $2.7-3.0/m³ for a dozer push or excavator grapple on drained ground (about 0.5x), so it pays only where machines cannot reach, such as surface armour inside a flooded dredge pond.

IDEA 4
NAME: Cold-sealed rolling snow-log pods
MECHANISM: Anchor kept: crushed ore plus snow sealed in an ice shell, carried by the current under winter river ice with no vessel and no return trip. The near-neutral +3 to +9 kg trim fails by orders of magnitude. Shell melt alone (the idea's own 6 cm) costs -196 kg of buoyancy. Snow at 250-350 kg/m³ creeps under hydrostatic load and loses 95-5,300 kg of buoyancy per day (Vionnet 2012 viscosity), and the trapped air gives 521 kg per metre of depth (a Cartesian-diver instability). The repair: a 1.6 m diameter rolling "log", snow pre-compacted to 550 kg/m³ (0.74 m³/t for coal, 1.6 for rock ore), sealed at -35 °C so it self-pressurises to +14.9 kPa, with a +750 kg margin. Creep then costs only 0.6-1.4% (about 100 kg) per 45 days. But rolling needs a mean under-ice velocity of 0.20-0.41 m/s, and getting past ice keels of 5-20 cm needs 0.62-0.95 m/s. Measured under-ice velocities are 0.05-0.25 m/s (Lena delta), and tailwater at +0.5 to +2 °C below dams melts the shell in 0.3-1.1 days.
VALUE: If it ran, pods would cost about $6.8/t for coal against about $124/t by winter road and $27-33/t by summer barge plus stockpiling (4-5x cheaper than the barge), but no surveyed reach has the required velocity, so the ratio is moot.

NOTES
Files are in /home/user/SomeRepository/engine/runs/permafrost/round2/erp2_b/: LOG.md (one line per round), NOTES.md (sources and full check tables), idea1_deflation.py, idea2_icedam.py, idea3_icefloat.py, idea4_pods.py, and *_out.txt.

IDEA 1
- Anchor kept: yes.
- Decisive numbers:
  - Season sublimation is 13 mm w.e. gross at Pevek and 6 mm in the calm upper Kolyma, from my energy-balance model using Pevek normals (Mar -21.4, Apr -14.3, May -2.2 °C mean, Wikipedia).
  - Measured snow-surface sublimation is 0.06-0.15 mm/day (North Slope eddy covariance, tc-2023-153). My model reproduces about 0 to -0.1 for a white surface.
  - Freed gravel is 58-109 mm/yr, against the 210 mm claimed.
  - Tundra snow-off is in early June (NOAA, Barrow).
  - Thresholds are from Shao and Lu 2000.
- Baseline per unit recovered: bulldozer-sluice at $6.0/m³ ($12.5/g) and tailings retreatment by trommel at $4.0/m³. The new method is $3.7-4.5/m³, about $8-9/g. The $6/m³ washing cost is derived from Russian AISC of $1,018/oz (World Gold Council) and the Polyus 0.6 g/m³ grade, and is not a quoted figure.
- Consistency: melt starts about doy 118 without albedo control. The dry lag must stay under 1 mm. Snowfall equals the sublimation budget. Gusts move gold flakes. Fetch must be 120-350 m.
- Hazards:
  - fine-gold loss in gusts
  - silt dust deposited on downwind snow (possibly As or Hg-bearing)
  - re-cementing by midday melt
- Deciding unknown: real net season sublimation and fine-gold retention on a raked, albedo-steered surface. Cheapest experiment: 10 plots of 10 × 10 m on a Pevek dump, Mar-May, with erosion pins and lysimeters, plus about 1,000 tagged gold flakes (75-300 µm) per plot to estimate losses within about ±0.5%.
- Closest existing work: natural deflation lags and desert pavements, Australian dry-blowing and air jigs. Freeze-drying permafrost gravel as the drying step for dry concentration seems untried. Its best niche is waterless benches, where it replaces $9-13/m³ of thermal-drying fuel.
- Verdict: NICHE.

IDEA 2
- Anchor kept: yes. The ore pile holds the water through a sprayed ore skin under a peat blanket.
- Decisive numbers:
  - 50-55 MJ/m³ for a loose pile, giving 2.2-3.2 m³ of water per m³ at 5-7 °C, against about 3 m³/m³ sluice water need (kuzstu 2023).
  - Face heat-transfer coefficient about 7,500 W/m²K.
  - Froehlich breach peaks 34 against 144 m³/s.
  - A 47 L/s creek at 6 °C feeds 60 m³/h, so 60,000 m³ takes about 42 days.
- Baseline: natural thaw plus dozer plus loader plus pumped sluice, or hydromonitor plus gravel pump, both about $4.65/m³ ($6.8/g at 0.8 g/m³ and 85% recovery). These come from a machine-hour cost model built on D375 prices of 96-156 Mrub (drom.ru) and an operator wage of 230 krub/month (hh.ru), not from quoted operating costs. New: $2.0/m³ ($2.95/g), 2.3x cheaper.
- Consistency: a loose pile leaks, so the skin is needed. The peat blanket thaws 0.42 m against 0.8-1 m available. Sliding safety factor about 5 at 3 m head. Water above 9 °C overfeeds the sluice and must be blended.
- Hazards:
  - a thermo-erosion notch through the skin (keep the forebay at 3 m or less, give it a spillway, and move the crest header)
  - slumping of the thawed face onto workers
- Deciding unknown: the real bulk ice content and in-pile temperature of hoisted stockpiles. Experiment: a 500 m³ test pile with a skin and a 3 m forebay, at 10 or more flow and temperature operating points, to check that feed = Q·ρc·ΔT/E within ±20%.
- Closest existing work: historic Klondike/Alaska ground sluicing and Russian hydro-thawing (гидрооттайка). The self-dosing ore-skin dam is not known.
- Verdict: WORKS (for winter-mined and stockpiled sands).

IDEA 3
- Anchor kept: yes.
- Decisive numbers:
  - Ice buoyancy is 83 kg/m³, so 141 kg/m² for 1.7 m of ice.
  - Ice thickness from 2.4·√FDD with FDD about 5,140 °C·days gives 1.72 m.
  - March contact freezes on 39 cm of gravel; drawdown contact freezes on 4.4 cm.
  - Net lift is 0.058 m³/m² (1.7 m ice) and 0.133 m³/m² (3.2 m ice).
- Baseline per m³ of boulder: excavator grapple $3.0, dozer $2.7, drill-blast only for boulders over 1.5 m. The idea's $6/m³ drill-blast-doze baseline is a strawman for typical boulders. The ice method costs $5.1-5.7/m³.
- Hazards:
  - people and tractors working on rotten spring ice
  - floe grounding failure in warm or late-frost years
  - turbidity when the dump bay melts out
- Deciding unknown: the frozen-on gravel thickness and the breakout fraction after a drawdown-timed contact. Experiment: a 0.5 ha pond with 3 drawdown dates × 2 ice thicknesses and 200 tagged boulders, giving the lift fraction within about ±7%.
- Closest existing work: natural ice rafting (Reimnitz 1987; High-Arctic lake diamicts; Lake Hoare). Engineered use for boulder clearing is not known.
- Verdict: NICHE (flooded dredge-pond surface armour only, about 0.5-1x).

IDEA 4
- Anchor kept: yes.
- Decisive numbers:
  - Buoyancy drift of the original pod (melt -196 kg, creep, air 521 kg/m) against a ±3-9 kg window.
  - The repaired pod needs a mean velocity of 0.2-0.4 m/s to roll and 0.6-1.0 m/s to pass keels.
  - Measured under-ice velocity: Lena delta 0.05-0.25 m/s (Fedorova 2020).
  - Krasnoyarsk tailwater is still about 2 °C off the natural winter temperature 40 km below the dam.
- Baseline per tonne delivered over 700 km: winter-road truck about $124/t (my cost model); summer barge plus stockpile about $27-33/t. The $0.03/t-km barge rate is an estimate, not sourced.
- Hazards:
  - lost pods (5% or more) freezing into the cover
  - hanging dams forming behind trapped pods
  - pods in the way of ice crossings
  - ore contamination of rivers
- Deciding unknown: rolling resistance and keel trapping under natural river ice. Experiment: 20 instrumented dummy logs in one 20 km reach, with ADCP velocity profiling, giving the arrival fraction within about ±10%.
- Closest existing work: timber log drives (open water only) and frazil underturning theory.
- Verdict: FAILS. Best honest niche is a single test on a fast, smooth, 0 °C regulated reach below a polynya edge, if such a reach exists.

Sources (from WebSearch/WebFetch):
- [Fedorova et al. 2020, E3S Conf.](https://www.e3s-conferences.org/10.1051/e3sconf/202016305003)
- [tc-2023-153 (Arctic sublimation)](https://tc.copernicus.org/preprints/tc-2023-153/tc-2023-153.pdf)
- [NOAA snow cycle](https://www.cmdl.noaa.gov/grad/snowcycle.html)
- [Pevek (Wikipedia)](https://wikipedia.com/wiki/Pevek)
- [kupi.com Pevek weather](https://www.kupi.com/en-ae/explore/russian-federation/pevek/weather)
- [WGC 2023 costs](https://www.gold.org/goldhub/gold-focus/2023/04/gold-miners-costs-reached-record-high-2022-dropped-final-quarter-year)
- [Polyus alluvials (Wood Mackenzie)](https://www.woodmac.com/reports/metals-polyus-alluvials-closed-gold-mine-42342780/)
- [kuzstu 2023](https://science.kuzstu.ru/wp-content/Events/Conference/RM/2023/RM23/pages/Articles/010601.pdf)
- [trud.igduran](https://trud.igduran.ru/index.php/psu/article/download/52/50)
- [drom.ru D375](https://auto.drom.ru/dealer327804/)
- [hh.ru operator vacancy](https://hh.ru/vacancy/132830786)
- [Reimnitz 1987 (USGS)](https://pubs.usgs.gov/publication/70014840)
- [Lake Hoare boulders](https://repository.lsu.edu/geo_pubs/606)
- [Kolyma stream temperature (narfu)](https://aer.narfu.ru/upload/iblock/e51/175_181.pdf)
- [Krasnoyarsk tailwater (sfu)](https://scholar.sfu-kras.ru/publication/89061943)