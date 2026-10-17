# Task: kill test - find the one number that decides whether each idea lives

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 8 candidate ideas. You are a screening engineer with tools: WebSearch/WebFetch and Bash with python3.
For EACH idea, spend about 3 minutes and do exactly two checks, with real numbers in python and a source for every
decisive input. Do not improve or redesign the ideas; judge them as written. Work only in `/home/user/SomeRepository/engine/runs/permafrost/genius/gate_1/`: read no other
files in the repository, write files only there, do not commit.

1. KILLER: the single quantity most likely to kill the idea at the scale it needs (a rate, flux, force, energy
   balance, recovery, strength, tolerance-vs-drift over the operating time, or a site condition that must hold).
   Compute what is REQUIRED and what is AVAILABLE (measured data, physical limits). MARGIN = available / required
   (1 = just works, 0.1 = fails by 10x, 5 = five times headroom).
2. CHAIN: cost per unit of product delivered to market (per oz, per t of metal, per t of coal, per t LCE, per boe)
   with the idea, against the BEST current practice a competent operator would use, over the whole chain (not one
   link). Use the ledger below for the current cost structure. RATIO = current cost / cost with the idea.

Value ledger (data):
ARCHETYPE A: seasonal open-cut placer: dozers/rippers strip frozen overburden, sluice washing plants, diesel via summer sea/river plus winter road, gold flown to refinery | delivered cost ~6,900 rub/g = ~$2,550/oz (Susumanzoloto 2025 RAS ~6,200 rub/g, escalated) | price $4,150/oz
SHARES (est.): energy 10% | labour/camp 20% | inbound logistics 12% | outbound logistics 0.2% | processing (spares, repairs, contractors, washing) 20% | capital 15% | other 22% (MET 6% + 10% of price above $1,900 = $474/oz)
LARGEST: other (MET/taxes) - a 10x cut of it removes 20% of delivered cost. Earthmoving frozen ground (diesel ~11 l/g, fleet, operators) is ~2/3 physically.
ARCHETYPE B: Baimskaya design: 70 Mt/yr Cu-Au open pit + flotation, floating-NPP power, 5,000-bed FIFO camp, 1.4 Mt/yr concentrate trucked 428 km to own Arctic port, then NSR (Jul-Nov) to China | delivered cost ~$8,500/t Cu CIF China gross, ~$2,500 net of 490 koz/yr gold (est.) | price Cu $13,980/t (LME, 31 Jul 2026), Au $4,150/oz
SHARES (est.): energy 11% | labour/camp 11% | inbound logistics 3% | outbound logistics 5% | processing 15% (2026 TC/RC benchmark $0) | capital 41% ($8.5bn BFS capex) | other 14%
LARGEST: capital - a 10x cut of it removes 37% of delivered cost.
ARCHETYPE C: export: open pit + wash plant, then RZD ~2,000 km to Vanino/Vostochny (Elga's own 531-km railway + Okhotsk port: ~$12/t vs ~$46/t, est.); settlements: small pit (Zyryanka, Dzhebariki-Khaya), then river/river-sea barge plus winter-road last mile | delivered cost export ~$83/t FOB; settlement ~23,000 rub/t (~$275/t) at the boiler (est.) | price $106/t FOB Vostochny, 5,500 kcal (Sep 2026); settlement: subsidised
SHARES (est., export / settlement): energy 5/3% | labour/camp 10/4% | inbound logistics 4/1.5% | outbound logistics 55/85% | processing 11/3% | capital 11/2% | other 4/1.5%
LARGEST: outbound logistics - a 10x cut of it removes 50% (export) / 76% (settlement) of delivered cost.
ARCHETYPE D: Kolmozerskoye design: open-pit spodumene pegmatite (1.96 Mt ore/yr), DMS/flotation concentrate, chemical plant making 45 kt/yr Li2CO3/LiOH. Brine alternative: DLE on 169-383 mg/L oilfield brine (INK, since Apr 2026, costs undisclosed) | delivered cost ~$10,200/t LCE (est.) | price $19,750/t Li2CO3 CIF Asia (2 Sep 2026)
SHARES (est.): energy 9% | labour/camp 14% | inbound logistics 4% | outbound logistics 1.5% | processing 18% | capital 42% (91 bn rub capex + 40 bn rub road) | other 12%
LARGEST: capital - a 10x cut of it removes 38% of delivered cost.
ARCHETYPE E: 0.2 Mt/yr East-Siberian field: early-production facility, associated-gas power, crude trucked ~300 km by winter/all-season road to ESPO, Transneft to Kozmino | delivered cost ~$82/bbl FOB Kozmino (est.) | price ESPO ~$100/bbl (Brent $106 on 12 Oct 2026; ESPO near Brent parity)
SHARES (est.): energy 1% | labour/camp 6% | inbound logistics 2% | outbound logistics 20% (trucking $10 + ESPO tariff $6/bbl) | processing 5% | capital 13% | other 53% (MET+NDD ~$43/bbl; full Sep-2026 MET 38,312 rub/t = $62/bbl)
LARGEST: other (fiscal take) - a 10x cut of it removes 48% of delivered cost (largest physical term: outbound, 10x removes 18%).
CROSS-CUTTING:
- Diesel (84 RUB/USD): exchange price 77k rub/t (~65 rub/l, Jun 2026); Yakutia retail 123 rub/l (Oct 2026); remote sites 120-150 rub/l ($1.4-1.8/l, est.), about half of it logistics.
- Power: Sakhaenergo isolated-grid tariffs 80-362 rub/kWh (2024); mine-scale diesel ~41 rub/kWh ($0.49, est.); Baimskaya's floating NPP 6.45 rub/kWh (2020 prices); grid hook-up expected to cut Nezhda TCC ~$40/oz.
- Freight: winter road ~20 rub/t-km ($0.24); LORP river barge ~8,000 rub/t per seasonal haul (~3-5 rub/t-km, est.); NSR general cargo Arkhangelsk-Pevek 15-17k rub/t; RZD coal tariff ~61% of FOB (Kuzbass); ESPO pipe ~3,750 rub/t (est.).
- FIFO labour: wages Chukotka 261k, Magadan 214k rub/month (May 2026); fully loaded ~5 M rub (~$60k) per worker-year (est.), ~2 workers per post.
- Construction premium: Far North builds cost 2-3x central Russia; Baimskaya capex is $28k per annual t Cu ($44k including state road/port/NPP, 1.1 trn rub) vs $22.4k global: 1.3-2x.
SOURCES:
https://ulus.media/2026/10/16/czeny-na-benzin-rastut-v-regionah-rossii-gde-toplivo-stoit-dorozhe-chem-v-yakutii/
https://www.dp.ru/a/2026/06/15/cena-letnego-dizelja-na-birzhe
https://base.garant.ru/408314055/f7ee959fd36b5699076b35abf4f52c5c/
https://perevozka24.com/yakutiya/perevozki-po-zimniku-search
https://paluba.media/news/206159
https://umcashipping.ru/price/
https://finance.mail.ru/article/na-chukotke-i-v-magadanskoj-oblasti-srednie-zarplaty-prevysili-200-tysyach-rublej-69198263/
https://finance.rambler.ru/realty/56611182-ispytanie-holodom-kak-vedut-stroitelstvo-na-kraynem-severe/
https://zolotodb.ru/article/13150/?page=all
https://metallicheckiy-portal.ru/news/2026/5/27/susumanzoloto_v_2025_godu_na_354_sokratilo_chistuy_pribil_po_rsbu
https://www.interfax.ru/business/964690
https://www.kazminerals.com/media/22180/completion-of-baimskaya-feasibility-study-final-20210928.pdf
https://www.eastrussia.ru/news/vsesezonnuyu-dorogu-ot-baimskogo-goka-postroyat-na-chukotke/
https://www.bigpowernews.ru/news/document126824.phtml
https://www.spglobal.com/market-intelligence/en/news-insights/research/2025/12/capital-demands-soar-for-new-copper-supply
http://arctica-ac.ru/docs/journals/59/ocenka-potenciala-iperspektivy-osvoeniya-malyh-mestorojdeniy-tverdyh-poleznyh-is.pdf
https://vgudok.com/novosti/tarif-rzhd-sostavlyaet-61-ot-stoimosti-uglya-fob-v-portah-vostoka
https://www.vedomosti.ru/business/news/2026/09/21/1230393-ugol-portu-vostochnii
https://www.interfax.ru/business/986137
https://axis-intelligence.com/lithium-price/
https://ru.themoscowtimes.com/2026/10/09/sbory-po-neftyanomu-ndpi-v-byudzhet-rf-mogut-vyrasti-na-38-v-oktsen-raschyot-reyter-a208245
https://fomag.ru/news-streem/tsena-brent-na-birzhe-ice-prevyshala-106-za-barrel-vpervye-s-29-sentyabrya/

VERDICT: ALIVE if MARGIN >= 1 and RATIO >= 1.5; DEAD if MARGIN < 0.3 or RATIO < 1.1; otherwise WOUNDED.
Be strict and fair: a beautiful idea that fails by 10x is DEAD; a dull idea with headroom is ALIVE.

Final answer (text only), exactly this format, one block per idea in the order given:
=== GATE ===
IDEA 1: <name>
KILLER | <quantity> | required <value unit> | available <value unit> (<source>) | MARGIN <number>
CHAIN | <best current practice> | now <cost unit> | with idea <cost unit> | RATIO <number>
VERDICT | <ALIVE/WOUNDED/DEAD> | <one sentence>
(same for the other ideas)

THE 8 IDEAS:
IDEA 1
NAME: Tuned-Burst Frozen Ground Ripping
MECHANISM: Lithotripsy-style transducer arrays (CAP 23), coupled to a frozen face through a brine film, fire ultrasound bursts tuned to the grain size of ice-cemented gravel or silt, so the weak ice bonds between grains fatigue and fail while the stones stay whole. A light loader scrapes off each loosened, still-frozen layer, and burst frequency is retuned as scanned grain size changes. Unheated rigs run through polar night on sodium-ion packs that keep over 90% capacity at −40 °C (CAP 9).
VALUE: Frozen overburden and ore are dug year-round by small electric machines, without explosives or waiting for summer thaw.

IDEA 2
NAME: Transpolar drift cargo pods
MECHANISM: Reusable sealed pods, shaped like Nansen's Fram so that ice pressure squeezes them upward instead of crushing them, are filled with coal or concentrate whose value does not suffer from slow delivery. In autumn they are set on newly formed Laptev Sea ice, drift with the ice to the ice edge at Fram Strait, and are picked up there by an ordinary ship. Comparing daily satellite radar maps of the ice gives drift paths traced backward from the Fram Strait exit. Starting sites whose paths turn off into the Beaufort Gyre are dropped, new sites are added where paths converge on the exit, and pod placement is re-optimized each season from beacon logs.
VALUE: Bulk cargo moves from the Laptev coast to the North Atlantic with no engines, no icebreakers and no infrastructure, trading about two years in transit for almost no freight cost.

IDEA 3
NAME: Flash-and-electrolyse lithium containers
MECHANISM: One-second Joule pulses (CAP 15), designed for rare-earth fly ash, flip carbon-mixed spodumene concentrate into an acid-leachable phase without a kiln. An ambient-temperature electrolyser (CAP 16), designed for cement, splits recycled sodium sulphate into sulphuric acid that leaches the lithium and caustic that purifies it into hydroxide, regenerating the sulphate. With no acid plant or bulk reagent imports, containers supplied by winter road replace the converter.
VALUE: Removes most of a 91 bn rub plant and the 40 bn rub all-season road, cutting a 42% capital share several- to tenfold.

IDEA 4
NAME: Spodumene Through Nepheline Alumina Kilns
MECHANISM: Spodumene concentrate is blended into kiln feed at Russia's existing nepheline-limestone sinter alumina plants (Achinsk, Pikalyovo); at 1,250°C the lime opens spodumene as in the old lime-roast lithium process, and its alumina joins plant output. Dissolved lithium is caught by steps already running: it co-precipitates as lithium-aluminium hydroxide during CO2 carbonation or crystallizes as carbonate in the soda-potash evaporators. Only a small strip-and-purify circuit is new.
VALUE: Lithium carbonate capacity for roughly a tenth of a greenfield chemical plant's capital, the largest cost term.

IDEA 5
NAME: Resonant kimberlite unmaking
MECHANISM: Kimberlite lumps cross a water bath swept by burst-wave ultrasound of the kind that grinds kidney stones through skin (CAP 23), its frequency stepped up as fragments shrink. Stress amplitude exceeds altered kimberlite's tensile strength but stays about a hundred times below diamond's, so the matrix turns to sand while diamonds pass unbroken. Sand is screened off, leaving a small heavy residue for sorting.
VALUE: A containerised, crusher-free plant processes kimberlite and recovers large stones whole.

IDEA 6
NAME: Ore stream as heat battery
MECHANISM: Crushed gold-quartz ore waits weeks in insulated silos, charged with cheap surplus electricity to ~600 °C like the soapstone heat battery (CAP 10), then discharged through air loops to heat camp and plant through winter. Each cycle drives quartz through its 573 °C inversion, whose sudden volume jump microcracks grain boundaries, so the cooled ore grinds far more easily and releases its gold. Charging is scheduled by heat demand and power price.
VALUE: One kilowatt-hour pays twice, covering an Arctic mine's two largest energy bills: heating and grinding.

IDEA 7
NAME: Floating bluff coal miner
MECHANISM: Many river settlements sit near bluffs where coal seams outcrop. A self-propelled barge with an autonomous excavator works the bluff nearest each settlement during the navigation season, cutting frozen coal into its hold, unloading at the riverside yard, then moving to the next exposure. Its dry-stone-walling autonomy (CAP 20) re-stacks the removed rock slabs as a mortarless revetment, so the cut bank cannot thaw and slump.
VALUE: Replaces a 1,000-2,000 km barge-plus-winter-road chain with a 10-100 km haul, cutting settlement coal's 85% logistics share about tenfold.

IDEA 8
NAME: Frozen Placer Dry-Washing
MECHANISM: In deep winter, frozen placer gravel is dug and crushed while it stays below −20 °C. At that temperature the ice behaves as a brittle, light mineral. Air tables and dry-washers separate the gold and heavy minerals from gravel and ice by density, with no water at all, and the tailings are stacked frozen.
VALUE: Placer mining can run all year without thawing, water or tailings ponds.

