# Task: kill test - find the one number that decides whether each idea lives

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 6 candidate ideas. You are a screening engineer with tools: WebSearch/WebFetch and Bash with python3.
For EACH idea, spend about 3 minutes and do exactly two checks, with real numbers in python and a source for every
decisive input. Do not improve or redesign the ideas; judge them as written. Work only in `/home/user/SomeRepository/engine/runs/permafrost/genius/gate_r1_1/`: read no other
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

THE 6 IDEAS:
IDEA 1
NAME: Borehole Bell Placer Mining
MECHANISM: Over placers buried under 20-60 m of frozen overburden, a 0.6 m hole is drilled to bedrock. A folding cutter lowered through it mills the frozen pay into a 15 m-wide bell, an airlift lifts the cuttings to a mobile wash plant, and the bell is left to cave. The grams from each bell update a stored grade model that places the next hole. Deciding quantity: overburden moved per m³ of pay, ~0.04 against 6-30 in open cut; it has headroom because the hole-to-bell area ratio is 1:600 and there is no trench and there are no pillars.
VALUE: Deep placers that no open cut can reach are mined with ~20x less earthmoving per gram, removing about half of delivered cost.

IDEA 2
NAME: Borehole Slurry Coal Underfoot
MECHANISM: Where a settlement sits over a regional coal seam at 50-300 m depth, known from Soviet basin drilling, a rig in the boiler yard drills down to it and a rotating warm-water jet cuts a cavity 15-20 m in radius. The coal slurry is airlifted up the same hole, dewatered and burned next to the hole. Sonar volumes and ash content of each cavity are stored and decide where the next hole goes. Deciding quantity: drilled metres per tonne, ~0.03 (a 150 m hole yields ~5,000 t); it has headroom because a continuous seam needs no hunting for lenses.
VALUE: Settlements above the Lena and other coal basins burn coal from beneath themselves, cutting out the barge-plus-winter-road chain.

IDEA 3
NAME: Under-Ice Regold of Old Ponds
MECHANISM: Soviet open-cut placer pits and dredge ponds across Kolyma now hold water over thawed, already-broken gravel and tailings that lost fine gold to crude sluices. A small floating plant (a suction dredge plus centrifugal concentrators) works them year-round under the ice, where the water stays above freezing. The grade recovered from each pond is stored and ranks the next pond. Deciding quantity: dig depth, 3-15 m against a 45 m dredge reach; it has headroom because nothing has to be stripped, thawed or blasted.
VALUE: Gold lost decades ago is recovered for a few dollars of earthmoving per gram instead of tens.

IDEA 4
NAME: Basal-Slot Robots, Creeping Roof
MECHANISM: From one shaft per square kilometre, 0.4 m-high battery crawlers cut only the basal gravel and the top of the fractured bedrock, conveying the cuttings to a wash plant at the shaft. Behind them the frozen roof creeps down and closes the slot, so the mine needs no pillars and no trench. Gold per metre goes into a shared stored map that steers the swarm along rich streaks. Deciding quantity: the share of placer gold in the basal 0.4 m, typically 60-80%; it has headroom because the volume cut per gram falls 13-20x compared with stripping.
VALUE: Placers are worked year-round with an order of magnitude less earthmoving and almost no surface disturbance.

IDEA 5
NAME: Seam-Cutting Collier Ships
MECHANISM: Where a thick coal seam meets deep water, as in Chukotka's Bering coalfield, an ice-class bulk carrier moors at the outcrop. Its own boom cutter mills frozen coal above and below the waterline straight into the hold, and the ship then sails to Asia; the cut becomes a sheltered berth that deepens as mining goes on. A seam model updated from each cut sets the next mooring. Deciding quantity: loading time, ~5 days for 50,000 t at 400 t/h, which adds ~$2-3/t; it has headroom because rail, port and stockpiles (~$46/t, 55% of FOB cost) disappear.
VALUE: Export coal reaches Asian buyers without a railway or terminal, cutting delivered cost by about 40%.

IDEA 6
NAME: Talik Dredging Under Lakes
MECHANISM: Beneath thermokarst lakes deeper than ~2 m, and beneath reservoirs that drowned placer valleys, the ground has thawed tens of metres down. A floating dredge with an onboard gold plant works these pre-thawed gravels year-round under the winter ice, with no stripping or thawing. Summer electrical soundings map each talik into a stored model, and the dredge's path follows the thawed zone. Deciding quantity: depth to pay inside the talik, 10-40 m against a 45 m dredge reach; it has headroom because nature has already thawed and softened the overburden.
VALUE: Placer gravels that nature has already thawed are mined continuously, removing about half of delivered cost.

