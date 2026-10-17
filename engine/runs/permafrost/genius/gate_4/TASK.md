# Task: kill test - find the one number that decides whether each idea lives

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 8 candidate ideas. You are a screening engineer with tools: WebSearch/WebFetch and Bash with python3.
For EACH idea, spend about 3 minutes and do exactly two checks, with real numbers in python and a source for every
decisive input. Do not improve or redesign the ideas; judge them as written. Work only in `/home/user/SomeRepository/engine/runs/permafrost/genius/gate_4/`: read no other
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
NAME: Freeze-Engine Vitriol Winning
MECHANISM: Copper-bearing liquor from a summer heap leach is stored in a pond, where it stays liquid at 0–4 °C under the winter ice. Through the winter nearly all of it is frozen in successive passes over coils, and the heat given off as it freezes boils propane, which drives a turbine and condenses in finned radiators open to −35 to −50 °C air, giving roughly 15–30 kJ of electricity per kilogram frozen. Each pass leaves a stronger drained brine, until copper sulfate reaches saturation and crystallises out as blue vitriol while the far more soluble ferric sulfate stays dissolved, so freezing both powers the plant and separates the copper from the iron. The crystals are redissolved in the spent electrolyte of a small, clean electrowinning cell run on the same power, and in spring the ferric, acidic brine and the ice meltwater, with any copper trapped in it, return to the heap as its oxidant and acid.
VALUE: A remote copper heap leach makes its own winter power, separates its copper from iron and wins clean cathode copper with no solvent extraction, no diesel and almost no acid shipped in.

IDEA 2
NAME: Frozen-gravel dry gold plant
MECHANISM: Frozen placer gravel is dug in winter and fed, still below −30 °C, through a light impact breaker. The brittle ice cement shatters while pebbles and gold grains stay whole. A screen then removes the pebbles, and a rising air stream blows away the ice chips and silt. The remaining sand passes over a corona-roll electrostatic separator, which throws off conducting gold and black sand while quartz and ice stay pinned to the roll. Mineral-sands plants have to heat their feed to dry it for this step, but −30 °C air holds almost no water, so the frost does that drying for free. A permanent magnet then strips out magnetite and leaves a gold concentrate. Electrostatic force grips fine and flaky gold best, which are exactly the sizes that air and water tables lose.
VALUE: Placer operators in Yakutia, Magadan and Chukotka can mine all winter straight from frozen ground and recover their fine gold, using a small generator and no thawing, water, ponds or reagents.

IDEA 3
NAME: Winter Wind Deflation Placer
MECHANISM: All winter, frozen placer pay gravel is ripped and spread a few centimetres thick over a broad pad of flat, windy tundra next to the cut. The dry −30 °C wind sublimes the pore ice from the top of the layer, freeing up to about a millimetre a day, and because no liquid water ever forms, the freed silt and light quartz and feldspar sand blow off loose into a snow fence. Gold, cassiterite, wolframite and other heavy grains stay behind; a daily harrow exposes fresh frozen layer, and the residue is swept up and dry-screened to remove the gravel. Because the rate is fixed per square metre, the pad is sized by area (about a square kilometre handles a season's pay gravel), and the silt-free residue, a small fraction of the original volume, is stockpiled so that the short summer wash plant finishes the whole year's ore in a few weeks of clear water, with no mud reaching the river.
VALUE: Placer mines gain a second production season in midwinter and finish all their ore in a few clean-water summer weeks, with no water, reagent or silt discharge and almost no fuel for the winter concentration.

IDEA 4
NAME: Etched thermokarst freight canals
MECHANISM: The surface of ice-rich yedoma is stripped or darkened along a planned line toward a navigable river, while insulating mats protect the banks as a mask. Each summer, meltwater ponds in the strip, absorbs more sun and deepens the thaw. Mud drains away until thawing stops at ice-poor ground, leaving a channel deep enough for barges. Ground-temperature probes guide each year's re-darkening and widening, like etch-rate control.
VALUE: Solar heat does the digging, so lowland deposits get a waterway for the cost of surface treatment instead of a road at millions of dollars per kilometre.

IDEA 5
NAME: Snow-Sculpted Under-Ice Sluice
MECHANISM: Before freeze-up, placer sand screened in summer is laid as a long windrow beside a riffle mat on the bed of a river reach that keeps flowing all winter. Through the winter, snow is scraped off a band of ice across the reach above the mat and piled on the ice upstream and downstream of it. Bare ice grows much faster than snow-covered ice, so the band grows a keel that squeezes the whole river's flow beneath it and speeds up the current over the windrow, faster each month as the keel deepens. The faster current strips the windrow grain by grain: light grains leave downstream, gold and heavy minerals drop into the riffles, and in late winter the mat is lifted through a slot and the concentrate is cleaned by hand.
VALUE: A placer mine can wash a full season's sand during winter at several times the natural under-ice rate, with frost building the sluice and the river powering it, so the short summer is spent only digging and no washing fuel, pumps or heated plant are needed.

IDEA 6
NAME: Sub-ambient photonic permafrost shields
MECHANISM: Pads, embankments, tailings and foundations are covered with polymer radiative-cooling film. It reflects sunlight and radiates heat through the 8-13 µm atmospheric window, so the surface stays below air temperature even in the 24-hour summer sun. Buried thermistors show where the ground is warming, and more film layers or wider coverage go there.
VALUE: Ice-rich ground stays frozen with no power, piles or thermosyphons, so foundations cost far less and stop failing.

IDEA 7
NAME: Grinding mill brews its lixiviant
MECHANISM: Copper-nickel ore is dry-ground in steel-ball mills under nitrogen-hydrogen gas, so freshly abraded iron from balls and liners fixes ammonia at ~45 °C and 1 bar (CAP 14). The ammonia-rich off-gas feeds an ammoniacal leach that dissolves metals from the just-ground ore as ammine complexes; ammonia is stripped, recycled and topped up by the mill. Hydrogen comes from on-site electrolysis, and the gas mix is tuned to ore sulphur content.
VALUE: The plant runs on power, air and water alone, ending inbound reagent convoys.

IDEA 8
NAME: Cold-Dry-Air Charge Sorting
MECHANISM: Crushed dry rock is tumbled against a plate so that different minerals pick up different electric charges. The near-zero moisture of −40 °C air stops that charge from leaking away. The grains fall between two charged plates and are pushed into separate bins according to their charge. Readings from each bin continuously adjust the plate voltage and the dividers between bins.
VALUE: Valuable material is separated from waste on site through the winter with no water, cutting the tonnage to be hauled by 5–20 times.

