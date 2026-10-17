# Task: kill test - find the one number that decides whether each idea lives

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 8 candidate ideas. You are a screening engineer with tools: WebSearch/WebFetch and Bash with python3.
For EACH idea, spend about 3 minutes and do exactly two checks, with real numbers in python and a source for every
decisive input. Do not improve or redesign the ideas; judge them as written. Work only in `/home/user/SomeRepository/engine/runs/permafrost/genius/gate_6/`: read no other
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
NAME: Carbonyl nickel rides gas pipelines
MECHANISM: Anchor kept: nickel travels as Ni(CO)4 vapour in the Power of Siberia line's own gas flow (9.8 MPa, 38 bcm/yr) and is split back out at the Amur gas plant where the line ends. Repaired design: 0.027 mol% carries 25 kt Ni/yr, which is Kun-Manie scale. That dose is at a saturation ratio of 0.25 at -10 °C. Compressor discharge is capped at 45 °C, so only 0.035% CO is needed to keep the carbonyl stable (the original 0.15% was sized for 80 °C). At the plant, a cold-oil absorber (20-60 kg/s of oil, 10-16 stages) catches 99.999% and leaves 2.7 ppb in sales gas, instead of heating the whole 879 kg/s stream (423 MW gross). The concentrated carbonyl is then decomposed at 200 °C. Propane hydrate does not apply here; the binding cost is CO make-up of 2.53 t CO per t Ni (about $514/t Ni).
VALUE: The physics works, but the pipeline leg costs about $960/t Ni more than running the same carbonyl refinery at the BAM/PoS junction and shipping pellets by rail, which saves only $27/t Ni of freight (about 0.03x). The whole chain at $6.6-8.4k/t Ni is no cheaper than selling concentrate at 70-75% payability ($5.4-6.1k/t Ni lost), so it FAILS on cost.

IDEA 2
NAME: Jacked Frozen-Block Stripping
MECHANISM: Overlapping hot-water-drilled holes cut frozen overburden into 20×20 m blocks, and summer creek water injected at bedrock thaws only the gold-bearing gravel beneath one block. Hydraulic jacks bracing against the next frozen block push the ~8,000-t block into the previously mined cell, exposing the thawed paystreak for excavator and sluice. Blocks advance downstream like sliding-puzzle tiles; kerf spacing adapts to measured ice content.
VALUE: Overburden is pushed rather than ripped, using about 0.1 l diesel/m³ instead of ~1 l/m³, cutting placer earthmoving roughly tenfold.

IDEA 3
NAME: Carbonyl nickel in gas pipelines
MECHANISM: This is set up beside a trunk line that ends at a gas processing or LNG plant. A small side stream of the line's own gas is partly burned to carbon monoxide and hydrogen. This gas first reduces roasted nickel ore to metal. Then, cooled to about 50 °C at a few bar, it carries the nickel off as nickel tetracarbonyl vapour, while iron, copper and rock stay behind. The vapour is metered into the line at about 0.1 mol%, which stays below its condensation pressure even in permafrost-chilled sections. A little extra carbon monoxide stops it breaking down in compressor stations, and the line runs under the same rules already used for lines carrying toxic sour gas. At the plant, heated beds in the inlet train, where mercury guard beds already sit, split the vapour into pure nickel pellets and carbon monoxide. The carbonyl never leaves the plant fence and no customer ever receives it.
VALUE: A line already carrying about 38 billion m³ of gas a year could also deliver about 100,000 t of refined nickel a year from a deposit along its route. It needs no new transport route and no reagents brought in, and nothing changes for gas customers.

IDEA 4
NAME: Snow-buoyed ice-shell ore pods
MECHANISM: Pods are made on the spot at a slot cut in the main-channel ice of a big north-flowing river. Crushed high-grade ore and enough dry snow to float it (roughly a cubic metre of snow per tonne of ore) are packed into a mould and sprayed with river water. The −40 °C air freezes this overnight into a sealed ice shell. The pods float up against the smooth underside of the ice and ride the current, out of reach of wind and waves, to a boom and recovery slot at a plant or year-round port downstream. There they are lifted out and cracked open, and the ice is thrown away. The 0 °C river cannot melt the pods, they cost nothing and they never go back upstream, so throughput is limited only by how fast the two slots work. Whole ore can therefore travel, and separation stays at an existing concentrator.
VALUE: A riverside deposit can send ore all winter to a downstream plant or port with no vessels, fuel, pod fleet or return haul, using only snow, river water and cold.

IDEA 5
NAME: Cold-Brine Leach, Crude-Carried Gold
MECHANISM: At a crude-oil pump station near a gold or platinum-metal deposit, ore is heap-leached all year with a strong calcium chloride brine that stays liquid far below −30 °C. The chlorine and acid the leach needs are made on site by electrolysing a bleed of the same brine with the station's existing power, so only top-up salt is shipped in. A side stream of the line's own crude, dosed with a gold extractant made only of carbon, hydrogen and oxygen such as dibutyl carbitol, is stirred once through the metal-loaded brine and rejoins the line as a density-tracked slug. As a result the site needs no carbon columns, elution, electrowinning, smelter or gold room. At the coastal terminal the slug is cut into its own tank and washed with hot oxalic acid, which drops the gold out as metal powder, and the crude is exported as ordinary crude.
VALUE: A deposit beside a crude pipeline can leach and recover precious metal right through the Siberian winter with only a heap, a mixer and an electrolysis cell on site and only salt brought in.

IDEA 6
NAME: Seasonal thermal-diode ground thaw
MECHANISM: Each spring, black UV-stable geotextile is laid over the deposit to absorb round-the-clock summer sun. Each autumn, rows of cheap snow fences are set up to trap a thick snow blanket that blocks most winter refreezing. Buried temperature strings track the thaw front, and film coverage and fence spacing are re-tuned every season to maximise net heat gain, so the unfrozen zone deepens year after year. Light rippers and loaders can then dig the thawed gravel without blasting or heavy frozen-ground machinery.
VALUE: Replaces diesel-intensive excavation of frozen ground with free solar heat for placers and shallow overburden.

IDEA 7
NAME: River-to-Pole Drift Pods
MECHANISM: Sealed, buoyant, satellite-tagged pods with rounded, sledge-like hulls like Nansen's Fram ride up instead of being crushed when ice squeezes them. They are filled at the deposit itself and launched into a north-flowing river such as the Lena, Yana or Indigirka, whose summer current carries them to the delta with no barge or fuel. A boom at the delta gathers the pods. In early winter they are hauled over the fast ice and set on young ice at its outer edge, where offshore winds push the new ice into the Transpolar Drift, which carries it to Fram Strait in 2–3 years. A pod freed by melt floats on and is frozen in again the next winter. Because no leg of the route costs anything per tonne-kilometre, the pods can carry screened run-of-mine ore instead of concentrate, and ships collect them by tag position and take them to a European plant that has the power and reagents to separate the metal.
VALUE: A roadless deposit on any Arctic-draining river can send its ore to a powered plant with no road, barge, icebreaker, fuel or on-site concentrator.

IDEA 8
NAME: Ice-Shell Under-Ice Ore Drift
MECHANISM: Run-of-mine ore goes into 1 t sacks, each with a thin plastic air bladder, and is frozen into a shell of river water in a simple mould. The trapped air plus the ice make each package slightly lighter than water, so the float itself comes free from the winter and nothing has to be shipped back upstream. The packages sit in a slot pool until they warm to 0 °C and are then pushed under the ice of a large river that flows all winter. In 0 °C water the shell cannot melt, and the current carries the packages 10–40 km a day to a net under a slot at a downstream town with power, where an ordinary mill separates the metal and the shells melt away. Packages that snag are freed at breakup and caught by a boom at the same site, and the only consumable is one liner per tonne.
VALUE: Moving whole ore costs almost nothing per tonne and nothing returns upstream, so even ordinary-grade deposits upriver of a powered town need no plant, power, reagents or return freight of their own.

