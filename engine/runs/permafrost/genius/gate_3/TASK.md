# Task: kill test - find the one number that decides whether each idea lives

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 8 candidate ideas. You are a screening engineer with tools: WebSearch/WebFetch and Bash with python3.
For EACH idea, spend about 3 minutes and do exactly two checks, with real numbers in python and a source for every
decisive input. Do not improve or redesign the ideas; judge them as written. Work only in `/home/user/SomeRepository/engine/runs/permafrost/genius/gate_3/`: read no other
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
NAME: Whole-Ore Ballast Swap
MECHANISM: Ice-class LNG carriers fill up by volume long before they reach their weight limit, so both legs from Arctic terminals carry thousands of tonnes of seawater ballast. That is far more free tonnage than any mine's concentrate. Sealed cassettes of crushed but unconcentrated ore take the place of that ballast in the double-bottom spaces and are swapped for seawater at the port where the LNG is unloaded. An ordinary mill there, with grid power and cheap reagents, separates the metal. On the empty return leg the cassettes come back full of diesel, and summer river barges on the Ob and Yenisei shuttle them between the deposits and the terminal, so the mine itself runs only drills, loaders and a crusher.
VALUE: A remote Arctic mine can do without its concentrator, power plant and reagent supply altogether, because the hard step of separating metal moves to a warm, powered port on freight that is already paid for.

IDEA 2
NAME: Robot-Built Self-Dredging Rivers
MECHANISM: Each winter, autonomous excavators that scan, grasp and stack irregular boulders without mortar (CAP 20) work the dry bars and frozen bed of a shallow tributary between deposit and navigable river, building dry-stone wing dams that pinch every riffle. The spring flood, squeezed through the gaps, scours a deep continuous channel that shallow-draft barges use all summer. After each flood the robots re-scan the bed and lengthen, raise or notch walls where scour fell short or overshot.
VALUE: Hundreds of kilometres of unused small rivers become maintained freight waterways for a fraction of a road's cost.

IDEA 3
NAME: Supply drones survey while flying
MECHANISM: Cargo drones on 500 Wh/kg cells (CAP 8) resupply remote camps, navigating by quantum magnetometers against crustal-field maps (CAP 4) where satellite navigation is jammed. The map-mismatch residuals that navigation normally discards are logged with inertial positions and fused into a steadily sharpening anomaly map. Residual patterns resembling kimberlite pipes or magnetite skarns automatically route the next flight lower over them.
VALUE: Exploration of roadless Siberia becomes a free by-product of routine logistics.

IDEA 4
NAME: Village Coal-Slurry Wells
MECHANISM: Where coal-bearing strata lie beneath or beside a settlement, boreholes reach the seam, a warm-water jet cuts the frozen coal and an airlift lifts the slurry. The slurry is milled and thickened into coal-water fuel and pumped a few hundred metres into a retrofitted boiler, so the coal is never dried, barged, stockpiled or trucked. Wells are added as cavities exhaust.
VALUE: For settlements on coal-bearing ground, it removes the barge and winter-road haulage that makes up ~85% of boiler-gate coal cost.

IDEA 5
NAME: Pulse-Sorting Weir Staircase
MECHANISM: Folded rubber weirs are flown in and inflated in series on a small tributary below a deposit, where they store snowmelt and rain in a chain of ponds. Frost-broken ore is spread in a riffled side lane of the stretch below each weir. Each timed gate release sends a measured flood pulse over the ore that sweeps clay, silt and light rock into the next pond, where they settle as tailings, while gold, cassiterite, diamonds or other heavy minerals stay in the riffles to be scooped out. The same pulses carry shallow-draft barges of this concentrate over each shallow stretch to the navigable river, and after the season the weirs are deflated and flown out, leaving no road, plant or tailings dam.
VALUE: A roadless placer or heavy-mineral deposit gets its washing plant, tailings ponds and haul route from one seasonal staircase of water, with no pumps, fuel or reagents.

IDEA 6
NAME: Relay flood-pulse ore barges
MECHANISM: Inflatable rubber weirs are flown in folded and set up in series on a small tributary between the deposit and a navigable river; each pond fills with snowmelt and rain. Shallow-draft barges loaded with concentrate wait in the top pond. A hydraulic routing model times the gate releases so that each pulse lifts the barges over the next shallow stretch into the pond below, and the model re-plans from water-level gauges after every pulse. Empty barges are winched back across the flat pools, and the weirs are deflated after the season, leaving no road or rail.
VALUE: Turns an ordinary summer stream into a temporary waterway, so bulk tonnage moves at water-freight cost without building a corridor.

IDEA 7
NAME: Highwall-Mined Frozen Paystreaks
MECHANISM: One trench is cut along the placer valley to bedrock; from it a remote-controlled coal highwall miner bores parallel 1.5 m entries 300 m sideways along the bedrock contact, taking only the gold-bearing gravel. The frozen overburden, as strong as weak rock, stands unsupported as roof between narrow pillars and is never stripped. Gravel is cut year-round, stockpiled and washed in summer.
VALUE: Earthmoving and diesel per gram fall roughly 8-10x, removing about half of placer delivered cost and opening deep-overburden placers.

IDEA 8
NAME: Paid ore ballast on LNG carriers
MECHANISM: Ice-class LNG carriers leave Arctic terminals with full tanks but under their weight limit, so they also carry thousands of tonnes of seawater ballast. Sealed cassettes of briquetted concentrate, brought by barge from deposits on the Yenisei and Ob, take the place of that ballast in double-bottom spaces and are swapped for seawater at the port where the LNG is unloaded. For each voyage, cargo reports and the ship's draft from AIS tracking give the ratio of paid tonnes to available deadweight. That ratio sets how many cassettes the next loading plan assigns, turning ballast space into cargo space.
VALUE: Arctic concentrate rides ships that already sail to Asian and European markets, at almost no extra cost for fuel or icebreakers.

