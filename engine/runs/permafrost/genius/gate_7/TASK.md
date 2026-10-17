# Task: kill test - find the one number that decides whether each idea lives

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 8 candidate ideas. You are a screening engineer with tools: WebSearch/WebFetch and Bash with python3.
For EACH idea, spend about 3 minutes and do exactly two checks, with real numbers in python and a source for every
decisive input. Do not improve or redesign the ideas; judge them as written. Work only in `/home/user/SomeRepository/engine/runs/permafrost/genius/gate_7/`: read no other
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
NAME: Coal micro-pits beside settlements
MECHANISM: A sled-towed cold-atom gravity gradiometer built to find tunnels (CAP 5) maps shallow coal lenses, half as dense as host rock, near Lena-basin settlements. An autonomous excavator, its dry-stone vision and grasping (CAP 20) retrained to sort frozen coal from rock, mines a few thousand tonnes unattended each winter. Lens rankings and measured ash are stored and updated, so the robot backfills and moves on.
VALUE: A short winter haul replaces hundreds of kilometres of barge and winter road, cutting settlement coal logistics about tenfold.

IDEA 2
NAME: Self-Heating Thaw-Bowl Leach
MECHANISM: A gently sloping pyritic copper-sulfide outcrop is blasted once to rubble in place, tens of metres deep. Each spring its surface is covered with black geotextile that lets air and water through and soaks up the round-the-clock summer sun, and each autumn it is fenced so that drifting snow buries it under an insulating blanket. Once the rubble is warm, bacteria oxidise its own pyrite, which makes sulfuric acid and heat, and the trapped heat thaws the rubble a little deeper every year; the warm column also acts as a chimney, drawing air in at the downslope toe and out through the fabric, so oxygen reaches the whole thawing bowl with no fans. Each spring the snow the fences caught melts and flushes the dissolved copper down to the still-frozen bowl floor, which acts as a natural liner and drains it to a sump at the toe packed with scrap steel, where the copper plates out as cement copper.
VALUE: A whole shallow sulfide orebody, not just its summer thaw layer, leaches itself in place over the years, using sun, snow and its own pyrite for heat, water, acid and air flow, and ships out only cement copper, with no plant, power line or acid supply.

IDEA 3
NAME: Shipyard-Built Floating Concentrator Fleet
MECHANISM: Crushing, grinding and flotation are built as 10 Mt/yr barge modules in an ordinary shipyard at normal productivity, towed by river or sea in summer into a dredged basin beside the deposit, and moored in water kept open by process heat and bubblers. Floating eliminates piles, heated halls and site-built civil works on permafrost. When the orebody is exhausted, the modules are towed to the next deposit.
VALUE: Escaping the 2-3x Far North build premium and reusing hulls across two or three deposits cuts capital per tonne roughly 5-8x.

IDEA 4
NAME: Buoyant Under-Ice Current Packets
MECHANISM: Sealed sacks of about 1 t of ground valuable material each carry a gas bladder, set so the sack is slightly lighter than water and rides pressed against the smooth underside of a frozen river. The current under the ice, which flows all winter, pushes them 25–50 km a day with no fuel or vessel. If a pressure sensor detects a stall, a valve lets out gas so the sack drops back into the flow, then refills it from a cartridge. A net under a slot cut in the ice collects the sacks far downstream.
VALUE: Freight moves along frozen rivers through the whole winter at almost no energy cost, when today nothing moves on them.

IDEA 5
NAME: Night-sky lithium freeze cascade
MECHANISM: Oil fields, gas fields and deep mines on the Siberian Platform already pump up strong calcium-chloride brine (often 0.2–0.5 g/L lithium) and must dispose of it. In winter this brine runs through a chain of shallow trays covered with polymer radiative-cooling film under an infrared-clear windshield. The film sheds heat through the 8–13 µm atmospheric window, so the trays sit about 10 K below air that is already at −40 to −50 °C. Each night every tray freezes past the calcium chloride–ice eutectic (about −50 °C). Ice and calcium chloride hexahydrate lock up together as a crust, while lithium chloride, which stays liquid down to about −75 °C, collects in a shrinking leftover liquid that drains by gravity into the next tray. After a few nights and steps, the liquid is tens of times smaller in volume and richer in lithium and bromide, and goes to an existing lithium plant. The spent crust melts in spring and goes back down the field's own disposal wells.
VALUE: Brine that Siberian oil, gas and mine operators now pay to reinject becomes a large-scale lithium concentrate, made with only the winter sky and the wells they already run.

IDEA 6
NAME: Winter-Only Railway
MECHANISM: Track panels are laid straight onto snow-compacted frozen tundra, with no permanent embankment, and rivers are crossed on artificially thickened ice. The line runs only during the 5–6 months when the ground is rigid. Each autumn, tamping machines re-level the track to undo the summer heave.
VALUE: Rail-scale bulk capacity reaches remote deposits for a fraction of the cost of an all-season Arctic railway.

IDEA 7
NAME: Fusion-Magnet Dry Kimberlite Rejection
MECHANISM: A 20-tesla REBCO coil (CAP 6) stands at the pit rim, its cryocooler dumping heat into winter air. Crushed dry kimberlite falls through its open field gradient: iron- and magnesium-silicate grains are dragged sideways, while diamagnetic diamonds and non-magnetic grains drop straight into a small product stream. Splitter vanes are reset continuously from X-ray diamond counts in each stream.
VALUE: Most kimberlite is rejected dry at the pit, shrinking the heated wet plant and its ore haulage several-fold.

IDEA 8
NAME: Self-Levelling Pressure-Cell Foundations
MECHANISM: Modular plants and camps rest on mats of Vectran-strap pressure cells (CAP 21), flown in folded, that spread load over untouched tundra so ground pressure stays below what the active layer bears. Tilt sensors drive a small compressor that inflates or bleeds individual cells as ice-rich ground settles or heaves, keeping structures level for decades.
VALUE: Facilities go onto raw permafrost in days, skipping pile rigs, freeze-back waits and gravel pads.

