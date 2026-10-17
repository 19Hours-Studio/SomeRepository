# Task: kill test - find the one number that decides whether each idea lives

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 8 candidate ideas. You are a screening engineer with tools: WebSearch/WebFetch and Bash with python3.
For EACH idea, spend about 3 minutes and do exactly two checks, with real numbers in python and a source for every
decisive input. Do not improve or redesign the ideas; judge them as written. Work only in `/home/user/SomeRepository/engine/runs/permafrost/genius/gate_5/`: read no other
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
NAME: Plume-Assay Needle Drilling
MECHANISM: A sled-mounted ~100 kW gyrotron (CAP 24) vaporises a finger-thin hole through frozen overburden and ore with no bit, rods or drilling fluid, so permafrost never thaws and no water or core is hauled. A nitrogen purge lifts the rock vapour; a spectrometer reads its atomic emission lines every few centimetres, and the condensed fume is bagged as a check sample. The rig steps across a coarse grid and adds holes wherever the plume chemistry spikes.
VALUE: Remote deposits gain bankable grade and tonnage at a fraction of the cost and time of core drilling with fly-out assays.

IDEA 2
NAME: Spray-Ice Drift Pods
MECHANISM: Each autumn, coal or concentrate is sealed in heavy plastic bulk bags on the new Laptev Sea ice, and seawater pumped up through the ice is sprayed into the −40 °C air over each load until it is encased in a thick ice block with the hull shape of Nansen's Fram, so that ice pressure squeezes it upward instead of crushing it. Several cubic metres of ice per tonne make the whole block float even with dense concentrate inside, so the hull costs only the pumping and a bag, is never returned, is thick enough to outlast two melt seasons, and carries a cheap satellite beacon frozen in with the load. The Transpolar Drift carries the blocks to the ice edge in Fram Strait in about two years, where an ordinary ship finds them by beacon and lifts out the bags. Launch points are chosen from satellite ice-motion maps traced backward from Fram Strait, keeping only those whose paths reliably lead out rather than into the Beaufort Gyre, and the choice is updated each season from the beacon logs.
VALUE: Bulk coal and concentrate move from the Laptev coast to the North Atlantic at almost no freight cost, with no engines, icebreakers or port and no pod hulls to build or bring back, in exchange for about two years in transit.

IDEA 3
NAME: Self-Sorting Wave-and-Ice Pond
MECHANISM: Over a stripped, ice-rich placer, a spillway holds a shallow pond of the ground's own meltwater. The pond absorbs the round-the-clock summer sun and thaws the gravel beneath it, wind waves lift silt and sand over the spillway, and their pressure pulses jig gold and heavy sand down through the stones onto the frozen floor. Each autumn the pond is set just shallower than the winter ice will grow, so the ice freezes onto the tops of the stones. In spring the spillway is closed, snowmelt lifts the bottom-fast ice, and the wind pushes the floes and their stones onto a dump shore, the way lake ice builds boulder ramparts. The spillway is lowered each year so the thin heavy layer rides down with the thaw front to bedrock, where only that layer is dug and washed.
VALUE: Even in the cobbly gravels typical of Siberian placers, sun, wind and winter ice remove the silt, sand and stones in place, so only a few percent of the deposit is ever dug and washed, with no pumps, washing-plant fuel or reagents.

IDEA 4
NAME: Stored Meltwater Barge Pulse
MECHANISM: In winter, sprayed water builds an ice wall across a small creek, and a peat cover keeps it from melting. Snowmelt fills the basin behind it, and the water is released through a gate in midsummer as a timed crest. Flat-bottomed barges ride the crest down to a river deep enough for ships. Downstream depth gauges control the gate opening so the crest stays deeper than the barges' draft for the whole distance.
VALUE: Creeks that are too shallow for boats become seasonal freight routes from remote deposits, with no road or dredging.

IDEA 5
NAME: Self-Charging Frost Separator Cascade
MECHANISM: Anchor kept: grains charged on the chute lining build the separating field themselves, through bins cross-wired to the opposite plates, with no power supply. The stated 30 kV/m gives only 4-9 cm of drift (not 30-60) and is space-charge-limited to 0.15 t/h per metre, which would need 7 km of plates. Repaired design: - A 0.3 m gap self-excites to 90 kV (300 kV/m, 8% of breakdown at -40 °C). That gives 41 cm of drift over a 1.5 m fall and 1.47 t/h per metre, or about 700 m of plates in total for 1 Mt/yr. - Insulating grains cannot hand over charge the way water drops do in a Kelvin dropper. Instead, discharges inside the charged grain pile pass about 98% of it to the bin. Leakage must stay above 2.2e10 Ω per metre. - Intake air must be heated to 20-40 °C, not 0 °C, to dry ore with 1-2% moisture: 137 MJ/t against 43-54 MJ/t of mill heat.
VALUE: $3,994/t Li2O delivered against $4,588 for dense-media separation plus haul (the best baseline, 1.15x) and $6,292 for Arctic flotation (1.6x). NICHE.

IDEA 6
NAME: Woven pressure-shell concentrator
MECHANISM: Flotation cells, tanks, thickener walls and the building envelope are Vectran-strap woven shells (CAP 21) holding slurry instead of cabin air: 6 m of slurry is 0.8 bar, about a sixth of demonstrated burst. They ship folded and sit on insulated gravel pads, needing no piles, structural steel or welders; only rotors and pumps are rigid, and cells are added as throughput grows.
VALUE: Turns the steel, piling and erection core of a 41% capital share into a one-summer flat-pack build at about a tenth of the cost.

IDEA 7
NAME: Fire-controlled ballistic ore transfer
MECHANISM: A gas or electric gun on the deposit fires steel-cased slugs of 100-500 kg of concentrate at about 1.5 km/s into a sand-and-water catch basin at a railhead or river port more than 100 km away. Radar measures where each round lands, and that miss distance corrects elevation and charge for the next round, exactly like artillery adjusting fire. Casings are recovered and sent back on the seasonal supply route.
VALUE: A stranded deposit is connected to market by two fixed installations and no corridor at all.

IDEA 8
NAME: Village Coal Gasified Underfoot
MECHANISM: Where a settlement sits on coal-bearing strata, as across much of the Lena basin, directional wells from its boiler-house yard reach the seam, are linked, and gasify it in place with injected air and steam. Tar-stripped syngas fires the existing boilers through new gas burners; a 10 kt/yr village consumes under half a hectare of seam a year, so one new well pair every few years suffices.
VALUE: The barge-plus-winter-road chain, about 85% of delivered fuel cost, disappears, making settlement heat roughly three times cheaper.

