# Task: kill test - find the one number that decides whether each idea lives

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 8 candidate ideas. You are a screening engineer with tools: WebSearch/WebFetch and Bash with python3.
For EACH idea, spend about 3 minutes and do exactly two checks, with real numbers in python and a source for every
decisive input. Do not improve or redesign the ideas; judge them as written. Work only in `/home/user/SomeRepository/engine/runs/permafrost/genius/gate_8/`: read no other
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
NAME: One-pass snow-berm ice lane
MECHANISM: At freeze-up a plow makes a single pass down the fast main channel of a big frozen river. It heaps the thin early snow into a low berm along that line and leaves the ice bare on either side. The berm insulates the ice beneath it, so through the early winter the bare sides grow downward much faster. This leaves a smooth upward channel in the ice's underside, and later snow, which falls evenly, does not erase it, so no more clearing is needed. Slightly buoyant pods of crushed high-grade ore are put in through a slot. They rise into the channel and ride the current inside it, so they cannot stray into slow water near the banks or catch on rough ice. A slot at the downstream plant or port lifts them out for concentration where power and reagents already exist.
VALUE: After one plow pass, any large frozen river becomes a self-maintaining, fuel-free winter lane that carries ore from a riverside mine to an existing plant, with no road, vessel or processing plant at the mine.

IDEA 2
NAME: Cold-sealed rolling snow-log pods
MECHANISM: Anchor kept: crushed ore plus snow sealed in an ice shell, carried by the current under winter river ice with no vessel and no return trip. The near-neutral +3 to +9 kg trim fails by orders of magnitude. Shell melt alone (the idea's own 6 cm) costs -196 kg of buoyancy. Snow at 250-350 kg/m³ creeps under hydrostatic load and loses 95-5,300 kg of buoyancy per day (Vionnet 2012 viscosity), and the trapped air gives 521 kg per metre of depth (a Cartesian-diver instability). The repair: a 1.6 m diameter rolling "log", snow pre-compacted to 550 kg/m³ (0.74 m³/t for coal, 1.6 for rock ore), sealed at -35 °C so it self-pressurises to +14.9 kPa, with a +750 kg margin. Creep then costs only 0.6-1.4% (about 100 kg) per 45 days. But rolling needs a mean under-ice velocity of 0.20-0.41 m/s, and getting past ice keels of 5-20 cm needs 0.62-0.95 m/s. Measured under-ice velocities are 0.05-0.25 m/s (Lena delta), and tailwater at +0.5 to +2 °C below dams melts the shell in 0.3-1.1 days.
VALUE: If it ran, pods would cost about $6.8/t for coal against about $124/t by winter road and $27-33/t by summer barge plus stockpiling (4-5x cheaper than the barge), but no surveyed reach has the required velocity, so the ratio is moot.

IDEA 3
NAME: Under-ice river drift pods
MECHANISM: In winter, slightly buoyant torpedo-shaped pods of concentrate are pushed through a slot cut in the ice of a big Siberian river's main channel. They ride the current along the smooth underside of the ice, out of reach of wind and waves, to a downstream recovery station with a boom and slot at a port. Weekly current profiles taken through the ice show where the flow stays fast. Where it slows, or where slush ice builds a dam below the ice, a relay slot is cut, the pods are lifted past the blockage and released again, and the spacing between releases is adjusted to the measured speed.
VALUE: Ore reaches Arctic ports during the frozen months and is already on the quay, instead of competing for the short summer window on the river.

IDEA 4
NAME: Midnight-sun salt-gradient power pond
MECHANISM: An insulated, lined pond holds a salinity gradient made from local Siberian Platform brines. The gradient traps summer insolation in the dense bottom layer at 60–80 °C, and in winter the ice lid adds insulation. In winter an organic Rankine cycle draws heat from the bottom layer and rejects it to −40 °C air. That temperature difference of about 110 K roughly doubles the efficiency of solar-pond plants in temperate climates. Gradient sensors trigger brine injection whenever the non-convecting layer starts to mix.
VALUE: Supplies winter heat and electricity to remote operations from local salt and sunlight, cutting the fuel that has to come in by winter road.

IDEA 5
NAME: Superconducting rotating-field grinding pipe
MECHANISM: Polyphase rotating-field coils (CAP 11), built for truck charging, are wound with REBCO tape (CAP 6), built for fusion, around a stationary non-magnetic pipe. The field whirls loose steel needles through the ore slurry so they collide and grind it; field speed is tuned to the measured product size, and capacity grows by adding pipe sections. There is no rotating shell, girth gear, liner or 1,000-t foundation.
VALUE: Makes grinding, the heaviest and most foundation-hungry block of a porphyry concentrator's capital, roughly ten times lighter to build on permafrost.

IDEA 6
NAME: Self-feeding ore-ice dam
MECHANISM: In early winter, the pay gravel stockpiled in autumn is laid across a creek in layers and sprayed with water, so the dam itself is frozen ore. A peat cover on its crest and upstream face keeps it frozen while spring snowmelt fills the basin behind it. All summer a fixed timber gate lets a steady flow of sun-warmed basin water run down the dam's bare downstream face. This water melts the ice cement at a rate set by the flow, so gravel drops into the water at roughly the right ratio for washing. The mix runs straight down a riffled chute, where cassiterite, wolframite or gold settle and the light gravel goes to a pit. The stored water and its head do both the feeding and the separation, with no loaders, pumps, fuel or reagents.
VALUE: A roadless placer can run a full washing season unattended from one autumn stockpile and one winter's snow, cutting out the summer fuel, pumps and loaders that make up most of its cost.

IDEA 7
NAME: Self-feeding ore-ice buttress dam
MECHANISM: Anchor kept: the frozen ore pile holds the forebay water, and warm water run over its downstream face thaws it, so feed = flow × ΔT / thaw energy. The regime where this is strongest is a loose winter-hoisted pile (bulk ice 0.15, 50-55 MJ/m³). With creek or forebay water at 5-7 °C it needs 2.2-3.2 m³ of water per m³, which matches what a sluice needs (about 3 m³/m³). The original ice-cemented pile (101 MJ/m³) needs 3.8-8 m³/m³ and is water-limited. A loose pile leaks: its cold content refreezes only 5-16% of its voids. The repair is a 3 m upstream ore skin, spray-sealed in winter (a 0.4 m lift freezes in 10-19 h), under a 0.8-1 m saturated-peat blanket that thaws only 0.42 m in 90 days. The forebay is kept at 3 m or less (sliding safety factor about 5, Froehlich breach peak 34 m³/s against 144 m³/s for a season-long reservoir). Above 8-9 °C cold creek water is blended in, because the water ratio would otherwise fall below 2. The face can thaw about 70 m/day, against the 0.8 m/day needed.
VALUE: Summer washing of winter-mined stockpiles costs about $2.0/m³ ($2.95/g at 0.8 g/m³) against about $4.65/m³ ($6.8/g) for natural thaw plus dozer ripping plus loader plus pumped sluice, or for hydromonitor plus gravel pump, so 2.3x cheaper (not 5x).

IDEA 8
NAME: Gun-Launched Gliding Freight Shuttle
MECHANISM: Two fixed guns, one at the deposit and one at a railhead or river port more than 100 km away, fire 0.5 t steel casings steeply upward at a modest 0.6–0.8 km/s. Near the top of the arc each casing unfolds spring-loaded wings and glides the rest of the way, steered by satellite-guided fins onto a sand catch bed beside the other gun. Gliding carries a casing several times farther per unit of launch energy than a purely ballistic arc and lands it slowly, so the guns are cheaper and wear less, the casings and wings are reused, and landing errors shrink from tens of metres to a few. Casings fly out full of concentrate and come back full of diesel and reagents, each inbound load carrying more fuel than the outbound shot burns, so the same loop powers the gun, the mill and the camp, with no road, convoy or seasonal return route.
VALUE: A stranded deposit is linked both ways all year, concentrate out and fuel and reagents in, by two fixed installations and no corridor at all, using a fraction of the energy and wear of a purely ballistic link.

