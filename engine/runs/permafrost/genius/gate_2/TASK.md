# Task: kill test - find the one number that decides whether each idea lives

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 8 candidate ideas. You are a screening engineer with tools: WebSearch/WebFetch and Bash with python3.
For EACH idea, spend about 3 minutes and do exactly two checks, with real numbers in python and a source for every
decisive input. Do not improve or redesign the ideas; judge them as written. Work only in `/home/user/SomeRepository/engine/runs/permafrost/genius/gate_2/`: read no other
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
NAME: Flash-unlocked refractory gold
MECHANISM: Arsenopyrite concentrate, conductive enough to need no carbon additive, receives one-second current pulses to ~3,000 °C (CAP 15) that destroy the sulphide lattice locking invisible gold and drive arsenic into a cold trap. The porous calcine is leached in dilute chloride, and a whey-protein amyloid aerogel (CAP 18) adsorbs the gold selectively; the loaded sponge is burned to doré. Pulse energy is tuned per batch to measured sulphur and arsenic.
VALUE: Stranded refractory gold deposits become treatable by a flown-in, cyanide-free container instead of a pressure-oxidation plant.

IDEA 2
NAME: Woven lay-flat crude line
MECHANISM: A 100 mm lay-flat hose jacketed in the Vectran strapping of inflatable space habitats (CAP 21) is unreeled by a tracked vehicle along the existing winter road, with no trench or piles. Crude-fired pump skids every ~15 km move the field's ~27 m³/h, dosing pour-point depressant and setting speed from line temperature and pressure. Skid-to-skid mass balance locates leaks; the hose is rewound and reused when the field declines.
VALUE: Turns ~$10/bbl trucking into about $1/bbl, so 300 km tie-ins of small East-Siberian fields to ESPO pay.

IDEA 3
NAME: Bell-Hole Thaw-Lift Mining
MECHANISM: A tracked sonic rig drills cased 0.3 m holes on a 6 m grid through frozen overburden. At bedrock a rotating hot-water jet thaws a 3 m-radius bell of paystreak, an airlift raises the slurry to a sluice, and tailings return to backfill the bell and refreeze, while frozen roof and pillars stand. Jetting time adapts to the gold grade of the returning slurry.
VALUE: Under 1% of overburden is disturbed, cutting fuel from ~11 to ~2 l diesel/g and opening placers too deep to strip.

IDEA 4
NAME: Flash-distilled lithium at the pit
MECHANISM: Crushed pegmatite plus a chloride donor gets a one-second flash Joule pulse (CAP 15), repurposed as a still that boils lithium off as LiCl. Staged condensers catch alkali chlorides hot and Fe/Al chlorides cold; soda ash precipitates Li2CO3 and freed NaCl is recycled. Thermophotovoltaic cells lining the chamber (CAP 7) recapture up to a third of pulse energy; pulse length is retuned from each batch's logged Li:Na condensate ratio.
VALUE: Containerised flash lines replace concentrator, kiln and acid-leach plant, cutting process capital per tonne LCE about tenfold.

IDEA 5
NAME: Thaw-scored slab toppling
MECHANISM: Hot-water jet holes thaw thin slots that score frozen overburden, base included, into slabs ~10 m tall and 3 m thick. Woven Vectran cushions from inflatable space habitats (CAP 21), slid into the back slot and inflated below 1 bar, tip each ~450 t slab into the previous mined-out strip, letting gravity move it. A site model stores hole spacing against measured ice content and retunes it after every topple.
VALUE: Strips frozen overburden using about a tenth of today's dozer-hours and diesel per gram.

IDEA 6
NAME: Flooded-Pit Floating Mine
MECHANISM: After a starter cut the porphyry pit is flooded, and under winter ice its water stays a few degrees above freezing. Benches are drilled and blasted from barges or the ice, a cutter-suction dredge pumps broken ore to a concentrator built from barge modules floating on the same lake, and tailings settle into mined-out depths behind the dredge. Dredging depth and blast pattern follow the block model as the lake deepens.
VALUE: Eliminates the haul fleet, roads, crushers, dewatering, tailings dam and heated foundations, roughly halving capital, the largest cost of Arctic copper.

IDEA 7
NAME: Lake-Breach Thermo-Erosion Canal
MECHANISM: Along a surveyed line from a lowland deposit to a navigable river, the moss is stripped or darkened in a strip with insulating mats along its edges, so the ground beneath thaws first and becomes the weakest path. A sun-warmed thaw lake or a dammed creek at the deposit end is then breached into the strip. Its 10–15 °C water runs down the line, melts the ice-rich yedoma at metres per day by thermo-erosion and carries the collapsing silt to the river. This is the same process that cuts gullies metres deep in days when such lakes drain naturally. Ground-temperature probes show where to darken further before the next lake is released, and once barges can reach the deposit the ore leaves unprocessed for a plant that already has power and reagents.
VALUE: Summer heat stored in lakes digs a barge channel in one or two seasons instead of decades, so a roadless lowland deposit is opened to water freight without building a road.

IDEA 8
NAME: Mast-Hung Coal Belt to Okhotsk
MECHANISM: A rope-supported belt conveyor, its carriage rolling on steel track ropes strung between masts 100-200 m apart, carries South Yakutian coal about 450 km over the Dzhugdzhur range to an Okhotsk Sea jetty. It touches permafrost only at mast footings, spans rivers and gullies without bridges, needs no embankment, and regenerates power on descents, with cold-rated belts running year-round.
VALUE: Moving 20-30 Mt/yr at about $5-8/t instead of a ~$46/t rail tariff removes most of the export chain's largest cost.

