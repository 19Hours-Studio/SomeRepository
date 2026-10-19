# Task: kill test - find the one number that decides whether each idea lives

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 8 candidate ideas. You are a screening engineer with tools: WebSearch/WebFetch and Bash with python3.
For EACH idea, spend about 3 minutes and do exactly two checks, with real numbers in python and a source for every
decisive input. Do not improve or redesign the ideas; judge them as written. Work only in `/home/user/SomeRepository/engine/runs/permafrost/genius/gate_nokit/`: read no other
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
NAME: Year-Round Under-Ice Talik Crawler
MECHANISM: Anchor: mine the natural thaw bulb under a lake from beneath the intact winter ice, using the ice as roof and work platform. The 40-t crawler cannot fit through a 1.4×1.4 m hole, so it drives in from the shore before freeze-up. It carries a submerged jig, so only about 1% concentrate goes up the 2 m² moon-pool, which takes about 2 kW to keep open. Tailings go by tremie pipe into the crawler's own pit, inside a silt-curtain cell hung from the ice. Without the cell, 540 t/day of fines would add about 3,400 mg/L per day to the ~160k m³ of water under the ice. Load on the ice stays below 25 t until the ice reaches 1.1 m (mid-December at Yakutsk, Stefan a=2.7). The same unit works open water in summer: 270 d/yr at 150 m³/h is about 0.6 Mm³/yr. That needs about 9 ha of lake floor over talik per year, with a 7 m dig against a talik of 25 m or more.
VALUE: About 1,600 rub/g recovered, against about 2,140 for a summer suction dredge and about 1,930 for draining the lake and working it with dozers and a sluice. That is 1.2–1.35× cheaper, not several times, and only for lake placers that cannot be drained.

IDEA 2
NAME: Wintering Coal CHP Barge
MECHANISM: Anchor: the bunker barge that brings the winter's coal stays frozen in at the village and burns its own cargo as a combined heat and power plant. Repair: a thermal-oil coal boiler (80%) feeds an ORC (16% net), run heat-led into the village heat network. The 1.54 MW of reject heat replaces boiler-house coal burned at 65%, so the net extra fuel per kWh_e is about 0. Electric-only would cost 12.7 rub/kWh_e at 10k rub/t; the original 20-30x claim compared kWh of heat from coal with kWh of electricity from diesel. A 0.3 MWe unit needs 1,780 t of coal per winter, which fits one 2,000 t barge, and the 381 m³ of ash fits the hold space freed as coal is burned. Reject heat of 104 kW keeps an ice moat open around the hull and 44 kW keeps the hold unfrozen. Capex dominates the cost: 19-32 rub/kWh at 0.3 MWe (132-237 M rub) and 14 rub/kWh at 1 MWe for district centres.
VALUE: Winter electricity at 14-32 rub/kWh against 45-75 rub/kWh full diesel cost (1.9-4.3x cheaper, up to 6x where costs reach 88 rub/kWh), with the heat nearly free.

IDEA 3
NAME: Ice-Deck Borehole Talik Mining
MECHANISM: Anchor: drill from winter lake ice into the sub-lake talik, which is already thawed, and mine the pay by borehole hydraulic mining. That means no thaw (saves 90 MJ/m³, about 25 kWh/m³), no dike, no drainage and no stripping. Repair: 1.2 m of ice carries only ~25 t of parked load, so the ice is flood-thickened to ≥1.8 m (Gold's formula at A=3.5 kg/cm² gives 113 t short-term, ~57 t parked). The 20-25 t modules sit more than 57 m apart, and the casing is insulated where it passes through the ice. Loose saturated talik gravel holds no roof and caves into the cavity, so the method is limited to narrow (25-40 m), deep, fine-gravel buried channels (<15 cm, the intake limit). Holes go on an 18 m grid (jet reach R=9 m) and are airlifted at 20-40 m³/h. Drawing stops at D≈3.4-3.9 m³ drawn per m³ of pay, set by on-ice jig grade monitoring; this extracts 86-89% of the pay in each hole's footprint, and tailings go back down mined holes. Cost: 1,130-1,970 rub per m³ drawn, which is 3,000-4,800 rub/g of gold recovered.
VALUE: Recovers gold from narrow, deep sub-lake channels that today go unmined, at 3,000-4,800 rub/g. The cheapest alternative, a summer pontoon suction dredge, costs ≥8,800 rub/g, so this is 1.8-4.4x cheaper; on channels wider than 80 m it is only 1-1.5x cheaper.

IDEA 4
NAME: Frozen-Roof Jet Adits
MECHANISM: Anchor: an unmanned jet and hydro-elevator head on a hose drives 3 m adits along bedrock under intact frozen overburden. Pillars are jetted out on retreat so the roof settles, and only the pay is thawed and lifted. Repair: a realistic creek (6→1 °C, 100 L/s) gives only 2.1 MW, which is 21 m³/h, not 60. Adding a 2 ha black-lined recirculating settling pond (net 80-150 W/m²) brings the heat to 3.7-5.1 MW, which is 35-45 m³/h at 30% heat use (107 MJ/m³ of pay) over a 90-day summer. The adit must never flood, because 6 °C water thaws the roof 2-4 m/day. So adits are driven up-gradient, the hydro-elevator handles 1.3x the inflow, and the portal has an insulated curtain; there is no ventilation because nobody is inside. Advance of 3.7-8 m/h limits the roof's life to 25-45 h, with 3-5 cm of roof thaw, and pillar stress is 0.4-1.2 MPa against 1-2 MPa long-term strength for frozen gravel. Cost: 1,200-1,400 rub/m³ of pay including washing, which is 550-660 rub/g.
VALUE: For frozen placers under ≥20 m of cover it costs 550-660 rub/g, against ~1,040-1,670 rub/g for winter underground mining and 1,270-2,400 rub/g for open pit: 1.6-2.5x cheaper overall and 2-3.5x on the mining step alone. It loses to bulldozer open pits where cover is under 15 m.

IDEA 5
NAME: Barge-Mounted Bluff Auger Coal
MECHANISM: Anchor: a spudded floating auger bores a frozen seam at water level in a river bluff and discharges straight into a hold, so no overburden is moved. At 20 kt/yr the rig sits idle most of the year and costs about 4,100 rub/t. The repaired version runs the whole ~100-day navigation season at about 60 t/h, for about 80 kt/yr. That rate sits between historical augers (21.5 t/h) and highwall miners (100–140 t/h). It fills four hopper barges moored alongside instead of its own hold. Thrust of 150–300 kN is taken by a frame bolted to the face, because three spuds (about 360 kN) are marginal. The frame has about 3 m of vertical travel to follow the 1–3 m drop in low-water stage during a campaign. Holes rise slightly so they drain. Face recovery is 62%, about 190 t per 80 m hole, which uses about 0.9 km of bluff a year.
VALUE: About 1,800 rub/t at a village bank within 150 km. That compares with 2,800–3,700 rub/t for a pit at the bank under a 20–30 m bluff (1.6–2× cheaper) and 7,100–11,600 rub/t for coal hauled 2,000+ km, as from Dzhebariki-Khaya (4–6× cheaper). There is no gain under a bluff of 10 m or less.

IDEA 6
NAME: Channel-Talik Seam Dredging
MECHANISM: Anchor: a dredge cuts the coal seam in place inside the unfrozen channel talik, where the river has already removed the cover, and pumps it into a hopper barge. Repair: only seams at thalweg level under high bluffs, where a bank pit would have to strip 15-25 m³/t. A leased dredge with a 150 kW cutter cuts lignite (UCS 5-7 MPa) at 46-65 m³/h, which is about 46-65 t/h and matches Kovin's measured 67 t/h. A 10 kt village-cluster year therefore takes 8-25 dredge-days, not "a week", and one dredge visits about 4 bends a season. An on-barge dewatering screen brings the coal to ~32% moisture (3,670 kcal/kg). Cutting in June-July lets stockpiles drain before freeze-up. Delivered cost is 2,700-4,300 rub/t, which is 730-1,170 rub/Gcal.
VALUE: 730-930 rub/Gcal with a shared dredge, against 2,830 rub/Gcal for northern-delivery coal at 15k rub/t (3.0-3.9x cheaper) and 1.4-2.4x below a bank micro-pit under high bluffs. There is no gain where the same seam has thin cover on land.

IDEA 7
NAME: Thermal Drift-and-Drop Placer Caving
MECHANISM: Anchor: water thaws only the pay layer, and the frozen overburden then falls under its own weight without any machine handling it. Toppling the face outward fails, because 62 m³ of rubble per metre of face lands in front of the next niche. So a trench is stripped instead (about 9% of the overburden), and remote low-pressure monitors drive 2-m drifts 30–60 m into the frozen pay from its side. A hydro-elevator at the face sends the slurry back to the trench. Each finished drift is widened past its long-term breaking span: 11–18 m for 6 m of overburden at 0.2–0.5 MPa. It stays open while being worked because a short-term strength of about 1 MPa lets it span about 25 m. The roof then drops 2 m in place, and mining retreats along the trench. Thaw rate is 5–10 m/day in theory and 0.15–5 m/day in field data. Water use is 3–8 m³ per m³ of pay, and fuel is about 60 rub/m³. It works best where overburden is 8–15 m thick.
VALUE: With 10 m of overburden, about 1,930 rub/g, against 2,270–3,980 for open cut with dozers and 3,500–7,000 for underground placer mining (1.2–3.6× cheaper). There is no gain with 6 m of overburden or less.

IDEA 8
NAME: Wintering Barge Bunker Swap
MECHANISM: Anchor: a floating hull is the village's coal bunker and feeds the boiler directly; hulls are swapped, so the coal never touches the shore. Keeping hulls dedicated all year costs 5,700 rub/t with used hulls and 27,000 with new ones, against 1,100–3,400 rub/t saved. So the swap uses the river fleet's idle winter instead. The season's last-voyage barge winters at the village berth as a sealed bunker and leaves after ice-out for summer work. In a sealed hold, only about 1,800 m³ of air enters as coal is drawn, so oxidation adds about 0.3 kW on average and self-heating is negligible. The gas that replaces the coal must be flue gas dried to about 0 °C: raw flue gas is wet, and at 6–9% O₂ it is not inert. As coal is drawn, buoyancy pushes up on the ice at about 80 kN/m, which would crack it. A 55 kW heated moat slot around the hull plus 27 kW of hold heat (3.4% of a 2.4 MW boiler, taken from flue-gas waste heat) prevent this. Draft limits capacity: at 1.2 m of water a 1,500-t hull carries only about 660 t.
VALUE: About 1,360 rub/t where a natural backwater lies within about 150 m of the main boiler. The costs it avoids are transshipment, rehandling, trucking and 5–15% stockpile loss, together 1,100–3,400 rub/t (0.8–2.5×). It loses money if a basin has to be dredged (2,226 rub/t) or a heat main is needed (+1,440 rub/t).

