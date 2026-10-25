=== REVIEW ===
IDEA 1: Gated diesel bridge plus pooled spares
DEFECT | MAJOR | A Q4 2027 gate leaves about 10 months to build 173k m³ of tankage on cooled piles and fill it before the last Pevek ship of 2028. Thermosyphon piles set in summer 2028 do not freeze in until the following winter, so full tanks cannot stand on them in autumn 2028. The bridge most likely starts in 2030, which is when the floating units are now due. | Pevek is open about 3 months a year ([Canadian Mining Journal](https://canadianminingjournal.com/featured-article/beating-tough-odds-on-top-of-the-world)). The first unit is due in 2028 and the fourth in 2030 ([Kommersant](https://www.kommersant.ru/doc/8878824)). The first Chinese-built hull reached Baltic Shipyard in spring 2026 ([Bellona](https://bellona.org/news/nuclear-issues/2026-08-floating-nuclear-power-was-a-russian-curiosity-now-others-want-to-give-it-a-shot)).
DEFECT | MAJOR | The plan ignores the road. 146 kt of diesel in and 222 kt of concentrate out must cross the roughly 430 km between Nagleynyn and the deposit. That is about 10,500 loads of 35 t, so this version depends on the unbuilt all-season road that IDEA 4 calls the binding constraint. | (146+222)/0.035 = 10.5k loads. Nagleynyn is about 430 km from Baimskaya ([NEI](https://www.neimagazine.com/news/first-ritm-for-baim-fnpp-manufactured/)).
DEFECT | MAJOR | The energy balance does not close. 146 kt at 0.225 kg/kWh is 649 GWh, a 74 MW average on 80 MW installed. That is a 93% load factor with no reserve on an island grid carrying a SAG mill. At the stated 65 MW average, the burn would be 128 kt. | Python: 146e6/0.225/8760 = 74.1 MW.
DEFECT | MAJOR | Pooled spares rely on a 9-month grey-import lead time, which is a way around sanctions. The task forbids that. | Stated in the mechanism.
DEFECT | MAJOR | Nickel side: the Poisson pooling claims behind the +15 kt do not reproduce (see IDEA 2). Lost LHD-hours on rich ore are also counted at 6.3 t Ni-eq, while IDEA 6 says those same mines are limited by their hoists. In a hoist-limited mine a marginal LHD-hour is worth about 0 t. | See IDEA 2.
DEFECT | MINOR | Break-even at 0.44 years of slip implies about $110–163m of fixed bridge cost, at a slip-year margin of $250–370m. The tankage alone is $173m, before genset mobilisation and lease. | Python: 0.44 × margin.
DEFECT | MINOR | The tankage is exactly one year of fuel (146/0.84 = 174k m³), with no allowance for unfillable tank space or for a late ice season. | Python.
SURVIVES | 12.2 Mt/y giving 48 kt Cu and 77 koz Au is consistent with a head of about 0.44% and 88% recovery. The Ni-eq arithmetic ($10.05k to $9.965k/t) reproduces. Line 1 ready in 2029 matches GDK's own date ([EastRussia](https://www.eastrussia.ru/news/zapusk-baimskogo-goka-otlozhili-do-2029-goda/)).
RATIO | 1.005 | Copper gives about 1.02 only if the units slip and the 2028 timing works, which is unlikely. Nickel gives about 1.005 after the pooling and hoist corrections.
KNOWN | partly | Nornickel and BelAZ signed a JV in September 2026 that includes a full repair base, and a Sosnovoborsk plant for 150 units a year is planned ([Interfax](https://interfax.com/newsroom/top-stories/117294/)). Diesel-powered Chukotka mines supplied through Pevek, such as Kupol, are standard practice.
NEW FACT | The Baimskaya plant is 70 Mt/y on two lines, so line 1 is about 35 Mt/y. The floating units total 424–440 MW, three running and one in reserve. | [Kaz Minerals BFS](https://www.kazminerals.com/completion-of-baimskaya-bankable-feasibility-study/)

IDEA 2: Availability as capacity
DEFECT | MAJOR | The Poisson claims do not reproduce. At an 80–83% fill rate per site, pooling the same stock across 6 sites gives at most 97.3%, not 99.5%. The pooled stock needed for equal service is at least 88% of separate stocks, not 46–62%. | Python scan of λ from 0.05 to 10 over 274 cases: pooled fill 0.27–0.973, stock ratio at least 0.88.
DEFECT | MAJOR | It contradicts IDEA 6. If the rich-ore deep mines are hoist-limited, a lost LHD-hour there costs about 0 t, not 6.3 t. The 5.2× ratio and the claim of being 1.7× more effective then collapse. | Skalisty hoisting is fixed at 1.5 Mt/y (SCS-1) plus 0.24 Mt/y (VS-10) ([Rudmet](https://rudmet.ru/journal/1297/article/22101/)).
DEFECT | MAJOR | It depends on grey imports, which the task forbids. | Stated 9-month grey-import lead time.
DEFECT | MAJOR | It is the uncorrected version of IDEA 1(1). The same programme there was re-estimated to +15 kt at $5.4k a tonne, against +29 kt at $2.7k here. The +7 percentage points of availability is unsourced. | IDEA 1 text.
SURVIVES | The group arithmetic holds: (806×10.05 + 29×2.7)/835 gives −2.5%, and 6.3 t per hour implies about 105 t/h at about 6% Ni-eq, which is plausible for an LHD.
RATIO | 1.005 | Using IDEA 1's corrected +15 kt at $5.4k, then cut further for hoist-limited mines.
KNOWN | partly | Nornickel's import substitution and the BelAZ repair JV ([Interfax](https://interfax.com/newsroom/top-stories/119023/)).

IDEA 3: Pre-staged flood-crest barges
DEFECT | MAJOR | A 2.5 m backwater is too shallow to winter a loaded barge. Long-term mean end-April ice is 1.42–1.67 m at the Kolyma, Yana and Indigirka mouths, which leaves 0.83–1.08 m of water under the ice. That is less than a loaded barge's draught, so the barge is locked in ice and sits on the bottom before winter drawdown is even counted. | [AARI spring 2016](https://old.aari.ru/resources/f0021/2016_spring.pdf). Python: 2.5 − ice.
DEFECT | MAJOR | Ice-jam surges during break-up are the main hazard at a river mouth. A loaded fuel barge crushed there is a spill, and the cost of that risk is missing. | Mechanism only; no number in the material.
DEFECT | MINOR | The 3,100 rub/t figure holds only if the barge would otherwise sit idle. A dedicated one-trip barge carries a capital charge of 10–25k rub/t a year (60–150m rub, 16%, 20 years, 1,000 t). | Python.
DEFECT | MINOR | The 35–62% loss is modelled, not measured. A linear 12-day recession gives 42–83%. | Python.
DEFECT | MINOR | It serves few of the deposits in scope. Tomtor and most hard-rock sites rely on winter roads. | 
SURVIVES | The 1.5–3.6× ratio reproduces from the stated figures (4,700/3,100 and 11,300/3,100).
RATIO | 1.01 | Whole chain. The gain applies only to one flood-only leg.
KNOWN | partly | Wintering fleets in backwaters and delivering to small rivers on the spring flood is standard practice in the Lena basin. I could not confirm that barges winter there loaded.

IDEA 4: Half bridge on the winter road
DEFECT | MAJOR | It needs about twice the tankage. Tankers reach Pevek in July–October and the winter road runs from late January to April. Pevek must therefore hold the whole year's fuel (107k m³), and the mine must hold May to January (about 85k m³). That is about 192k m³ against 106k, roughly +$86m, which turns the +$102m EV into about +$16m and the low-price case into about −$57m. | Kupol's road runs late January to end April ([Canadian Mining Journal](https://canadianminingjournal.com/featured-article/beating-tough-odds-on-top-of-the-world)). Python.
DEFECT | MAJOR | 130 days is longer than the real Chukotka window of about 95 days, and the right benchmark is Kupol, not Tibbitt–Contwoyto. Kupol's road averaged about 19 trips a day in 2008. At 95 days the plan needs about 69 loads a day, 3.6× Kupol, over an 800 km route, which takes about 160 trucks. | Kupol 2008: 1,944 trips. 6,600/95 = 69.
DEFECT | MAJOR | It shares IDEA 1's gate-to-tank-farm timing defect and the same 14% shortfall in the energy balance (90 kt implies a 45.7 MW average, not 40 MW). | Python.
DEFECT | MINOR | Tibbitt–Contwoyto's 158 a day is a season average, not a daily record: 10,922 loads over about 67–70 days. | [CBC](https://amp.cbc.ca/news/canada/north/diamond-mine-ice-road-expected-to-have-record-year-1.2937270)
DEFECT | MINOR | The $3.0k/t low-price cash cost is unsourced. Diesel power alone is $4.1k/t Cu, against a gold credit of $4.5k/t at $2.8k gold. | Python.
SURVIVES | 6,600 loads works out to 34.7 t per load for 90 kt of fuel plus 139 kt of concentrate, which is feasible. 51 a day over 130 days is correct arithmetic.
RATIO | 1.00 | The extra tankage cancels the expected value.
KNOWN | partly | A 450 km ice road from Bilibino to Peschanka is already planned for GDK Baimskaya ([EastRussia](https://www.eastrussia.ru/news/ledovye-dorogi-dlya-gdk-baimskaya-postroyat-na-chukotke/)). Kupol's winter road from Pevek is the precedent.

IDEA 5: Size Sever to hulls
DEFECT | MAJOR | The baseline is wrong. Vostok Oil's first cargo in September 2026 was a blend of Vankor and Payakha crude, so current practice already lifts what hulls allow. The $29/t and $2.4–5.8bn are measured against a plan nobody can execute, not against what is done today. | Kpler via [energynews.pro](https://energynews.pro/en/rosneft-ships-first-oil-cargo-from-arctic-bukhta-sever-terminal)
DEFECT | MAJOR | Running only Payakha oil through a 790 km trunk sized for 100 Mt/y means 1.5–3 Mt/y, or 1.5–3% of design. Line fill is 0.53–0.76 Mt (for 1.0–1.2 m pipe), and oil would sit 64–180 days in Arctic pipe. That is a wax and minimum-throughput risk, and it is the likely reason Vankor oil is blended north. | Python. 100 Mt/y design ([S&P](https://www.spglobal.com/energy/en/news-research/latest-news/crude-oil/090626-russia-launches-major-vostok-oil-project-with-first-arctic-loading)).
DEFECT | MINOR | The hull-limited premise was not binding in 2026. Valentin Pikul waited 84 days for cargo. | [Barents Observer](https://www.thebarentsobserver.com/news/tanker-crew-waited-84-days-at-remotest-arctic-terminal/457741)
DEFECT | MINOR | $80–190/t does not reproduce. The figures give $77–80 per tonne-year deferred, or $160–232 per tonne of annual capacity. | Python.
DEFECT | MINOR | Kozmino access is allocated by the Energy Ministry's export schedule. Rosneft cannot simply choose it. | 
SURVIVES | The 69 kt hull is right (Valentin Pikul, 69k dwt, Arc6). 1.54 Mt/y per hull and about 19 hulls for 30 Mt/y reproduce. A south cost of $57/t is plausible: the ESPO tariff is 3,896.51 rub/t, about $43–49 ([Interfax](https://www.interfax.ru/business/1061300)), plus port and freight.
RATIO | 1.00 | Measured against actual practice.
KNOWN | yes | The [Carnegie analysis (July 2025)](https://carnegieendowment.org/ru/russia-eurasia/politika/2025/07/russia-new-oil-project) notes that existing pipelines already export Vankor-cluster oil.

IDEA 6: Shaft-bottom XRT sorting, hoist-bound mines
DEFECT | MAJOR | "Hoist-bound" assumes the mining side has +11% to +40% spare capacity: breaking, LHDs, ventilation and cooling at 2 km. Nothing shows that exists. If it does not, the gain is zero. | Python: mined ore ×1.108 and ×1.401.
DEFECT | MAJOR | I found no production-scale XRT sorting installed underground. Mittersill, Renison and Mt Carbine all sort on surface, so 2–3 years is optimistic, especially in rockburst-prone deep levels. The domestic 150 t/h sorter is not named or verified. | [Mittersill](https://onemine.org/documents/x-ray-transmission-based-sorting-at-the-mittersill-tungsten-mine) rejects 22% at surface.
DEFECT | MAJOR | It contradicts IDEA 2, which values rich-ore LHD-hours as output in these same mines. | 
DEFECT | MINOR | Skalisty can hoist 1.74 Mt/y in total, not 2 Mt/y. Turning coarse rejects into cemented backfill needs an underground plant that is not costed. | [Rudmet](https://rudmet.ru/journal/1297/article/22101/)
SURVIVES | ×1.095 and ×1.36 hoisted, NPV ×1.083–1.307, reject ratio 0.40 t/t and 2 units of 150 t/h all reproduce (Python).
RATIO | 1.01 | Applies to a few hoist-limited mines only, and probably to fewer.
KNOWN | partly | Renison crushes underground and sorts by XRT on surface ([Global Mining Review](https://www.globalminingreview.com/mining/14012022/tomra-mining-delivers-sensor-based-sorting-at-renison-tin-mine/amp/)).

IDEA 7: Diesel-sized first line, nuclear expansion
DEFECT | MAJOR | IDEA 1 already corrected this: the same 80 MW fleet gives 12.2 Mt/y, not 15. Here 117 kt of diesel for 15 Mt is 34.7 kWh/t, against 53 kWh/t in IDEA 1 and about 40 kWh/t for the full design. Output is overstated by about 23%, and 15 Mt is 43% of line 1's 35 Mt/y. | Python.
DEFECT | MAJOR | The trucking does not work. Fuel tankers cannot back-haul bulk concentrate. 310 kt of concentrate is about 8,850 loads at 35 t, against the stated 7,000, which implies 44 t per load. | Python.
DEFECT | MAJOR | It shares the gate-to-tank-farm timing defect and the doubled tankage problem in the winter-road case. 78 a day implies a 90-day season, which conflicts with IDEA 4's 130 days. | Python: 7,000/78 = 90.
DEFECT | MINOR | Coarser grind with full design recovery: 0.51% head at 88% recovery is assumed. The higher head conflicts with IDEA 1's implied 0.44%, and at that head 15 Mt gives 59 kt Cu. | Python.
DEFECT | MINOR | The $1.2bn a year idle carry is sunk either way. The real value is the margin minus bridge costs. Diesel power alone is $2.33k/t Cu, against $0.78k on nuclear at $0.10/kWh. | Python.
SURVIVES | The $0.539bn margin is correct arithmetic at the stated cost. 174k m³ is about 1.25× of 117 kt, which gives a reserve margin.
RATIO | 1.01 | Rescaled to 12.2 Mt with the timing correction.
KNOWN | partly | Same precedent as IDEA 1: diesel-powered Chukotka mines (Kupol) and diesel during construction at Peschanka.
NEW FACT | GDK says commissioning will start in 2028 and commercial operation in 2029 (December 2024). | [EastRussia](https://www.eastrussia.ru/news/zapusk-baimskogo-goka-otlozhili-do-2029-goda/)