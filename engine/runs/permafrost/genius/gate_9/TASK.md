# Task: kill test - find the one number that decides whether each idea lives

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 8 candidate ideas. You are a screening engineer with tools: WebSearch/WebFetch and Bash with python3.
For EACH idea, spend about 3 minutes and do exactly two checks, with real numbers in python and a source for every
decisive input. Do not improve or redesign the ideas; judge them as written. Work only in `/home/user/SomeRepository/engine/runs/permafrost/genius/gate_9/`: read no other
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
NAME: Snow-Bedded Seasonal Crude Hose
MECHANISM: Each November a reel-sled lays a 300-km polyurethane lay-flat hose along the winter-road route and a groomer buries it in compacted snow, which supports and insulates it; associated-gas-fired booster pumps keep light crude moving. The field produces its whole annual volume in the five winter months and is shut in over summer, so the reservoir itself is the storage tank. In April the hose is purged with nitrogen, reeled and reused.
VALUE: Replaces ~$10/bbl trucking with roughly $2-3/bbl for small stranded East-Siberian fields, with no permanent pipeline.

IDEA 2
NAME: Creeping-floor solar copper pond
MECHANISM: An insulated, lined salt-gradient pond is floored with crushed chalcocite-rich copper ore. The dark ore absorbs sunlight like a solar pond's black bottom and sits in the 60–80 °C chloride bottom brine, which is also the leach liquor. In winter the hot brine drives an organic Rankine cycle that dumps its heat into −40 °C air at about twice the efficiency of temperate solar ponds. That power runs a divided cell: cuprous copper in brine drawn from under the ore plates out as powder, and the anode makes cupric chloride that goes back to attack the ore. The chalcocite simply splits into copper and sulfur, with no acid, oxygen or other reagent used up. Fresh ore goes in down a submerged chute along one bank, and a slow submerged scraper, run on the pond's own power, drags the bed across the floor to a sump where leached residue is lifted out. The pond therefore leaches a continuous stream of ore instead of a single batch.
VALUE: A remote chalcocite deposit in the Transbaikal permafrost can produce copper metal year-round at mine scale from local salt and summer sun, with no fuel, acid, oxygen plant or power line.

IDEA 3
NAME: Transpolar Drift Freight
MECHANISM: Sealed, buoyant ore containers with satellite tags are set into Laptev Sea fast ice near the Lena delta. The Transpolar Drift carries the ice and containers to Fram Strait in 2–3 years without fuel or escort. When the floes melt, the containers float in open water and ships pick them up by their tag positions.
VALUE: Bulk ore can reach European waters with no icebreakers, paying only the cost of time.

IDEA 4
NAME: Under-Ice Sphere Strings
MECHANISM: Rigid spheres about 1 m across, with closed-cell foam shells, sealed holds and no gas, valves or electronics, are trimmed to about 0.5% positive buoyancy and clipped about every 20 m onto a light floating rope, in strings of a hundred or more. A string rides against the smooth underside of a big Siberian river's winter ice and rolls downstream with the current; because the drag on the whole string pulls each sphere along, none can stall in slack water or behind an ice keel long enough to freeze in, and the flow pushes the string down and around ridges and hanging dams. Since these rivers flow north from the railway, strings pushed through a slot at an upstream railhead carry diesel, brought to neutral buoyancy by dense reagents such as acid or lime in a second hold, down to a riverside mine. There they are emptied, refilled with concentrate, re-trimmed and pushed back under the ice to a boom at a downstream port that catches each string by its lead rope, and the empties go back upriver by barge in summer.
VALUE: Through the seven months when nothing else moves on the river, the current under the ice both supplies a riverside mine with fuel and reagents and carries its concentrate to port, without losing cargo to freeze-in and with no vehicles, fuel or tending.

IDEA 5
NAME: Relocatable Frozen-Tundra Ore Railway
MECHANISM: Worn rail panels, which mainline track renewals retire every year at near-scrap cost, are laid by a standard track-laying train straight onto frozen tundra compacted with snow, with no embankment. Rivers are crossed on ice thickened by repeated flooding, tamping machines re-level the line each autumn to undo the summer heave, and trains run only in the 5–6 months when the ground is rigid. Because the line carries rail-scale tonnage at rail cost, it hauls raw ore to a mill on the permanent network where grid power and reagents already exist, and the empty trains come back with fuel, so the deposit needs only a pit and a loading ramp. When the deposits it serves are worked out, the same panels are lifted and relaid to the next group of deposits, so the line's capital cost is mostly labour, is reused, and is small enough for deposits shipping a few hundred thousand tonnes a year.
VALUE: Mid-size remote deposits, not only giant ones, get rail-scale haulage of raw ore to grid-powered mills for a small fraction of the cost of an all-season Arctic railway, with no plant on permafrost.

IDEA 6
NAME: Self-Charging Frost Separator Cascade
MECHANISM: Dry crushed ore slides down a chute lined with a chosen material, so each mineral picks up its own sign of charge, and in −40 °C air, which holds almost no water vapour, that charge does not leak away. The grains fall between two plates into two metal-lined bins, each wired to the plate on the far side, so the charge carried into the bins keeps driving the plates up to a spark-gap cap of tens of kilovolts, as in a Kelvin water dropper. One unpowered pass gives only a modest upgrade, but each stage costs only a lining, two plates and a few metres of drop, so a dozen stages are stacked down a hillside or pit wall: each stage's concentrate bin feeds the next stage's chute, and a small conveyor lifts the reject of the lower stages back into the feed. The cascade reaches shipping grade with no power supply, water or reagent for the separation, and its only settings are the splitters, moved according to the grade measured in each bin.
VALUE: Remote deposits make shipping-grade concentrate on site all winter from dry ore, with no water, reagent or power for the separation, cutting the tonnage to be hauled by 5–20 times.

IDEA 7
NAME: Robot drift-mining under frozen roof
MECHANISM: Instead of stripping 5-15 m of frozen overburden, an autonomous excavator tunnels only the 1-2 m pay gravel on bedrock, using the frozen ground above as roof. Its sodium-ion pack (CAP 9) works at −40°C and emits no exhaust heat, so the roof stays frozen. Its dry-stone-walling autonomy (CAP 20) stacks cobbles into mortarless pillars behind the face and re-plans spans from face scans, so no pay is left in pillars.
VALUE: Moves 5-10x less ground per gram, attacking earthmoving, about two-thirds of physical placer cost.

IDEA 8
NAME: Black-sand-steered bedrock moles
MECHANISM: Battery robots cut drifts along bedrock under intact frozen overburden left as roof, removing only the 1-1.5 m gold layer. Quantum magnetometers built for GPS-free navigation (CAP 4) serve as ore-ahead sensors: magnetite black sand travels with gold, so robots steer up the magnetic gradient and store a 3D pay map. Sodium-ion packs working at −40 °C (CAP 9) emit no exhaust heat, so winter air ventilates the drifts without thawing the roof.
VALUE: Ends stripping, cutting volume moved and diesel per gram of placer gold about tenfold.

