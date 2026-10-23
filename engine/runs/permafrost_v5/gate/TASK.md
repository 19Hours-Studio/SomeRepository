# Task: kill test - find the one number that decides whether each idea lives

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 8 candidate ideas. You are a screening engineer with tools: WebSearch/WebFetch and Bash with python3.
Do not improve or redesign the ideas; judge them as written. Work only in `/home/user/SomeRepository/engine/runs/permafrost_v5/gate/`: write files only there, do not
commit. The only other files you may read or import are the verified calculation kit in `/home/user/SomeRepository/engine/kit/`.

The kit holds tested calculators for the checks that killed earlier ideas, and a catalog of KILLER CLASSES (below).
For EACH idea, spend about 3 minutes:
0. SCREEN: go through the catalog and, for every killer class that applies to the idea, compute one margin with the
   kit (required vs available, with a source for each decisive input). Use the kit's functions instead of rewriting
   the physics; write your own code only where the kit has nothing.
1. KILLER: of the screened quantities, the one with the LOWEST margin at the scale the idea needs.
   MARGIN = available / required (1 = just works, 0.1 = fails by 10x, 5 = five times headroom).
2. CHAIN: cost per unit of product delivered to market (per oz, per t of metal, per t of coal, per t LCE, per boe)
   with the idea, against the BEST current practice a competent operator would use, over the whole chain (not one
   link). Use the ledger below for the current cost structure. RATIO = current cost / cost with the idea.

Calculation kit catalog (data):
# Kit catalog: killer classes for Arctic/permafrost screening

```python
import sys; sys.path.insert(0, '/home/user/SomeRepository/engine'); from kit import ice, thermal
from kit import geotech, hydro, naval, econ, stats, climate, data   # data.get('price.fx_rub_usd'), data.find('ice')
```
SI units unless named (FDD in °C·day, Gold in t). Impossible inputs raise ValueError. Tests: `python3 engine/kit/test_kit.py`.
Gate rule: `econ.gate_verdict(margin, ratio)` (margin = available/required).

**1. Season window vs rate × time.** Any seasonal work (dredging, augering, thawing, winter roads, ice fishing-out).
Call `econ.season_capacity`, `econ.window_margin`, `climate.hours_below`, `climate.days_above`.
Seen failing: lake exhausted in 18-31 d of a 300-d plan; −35 °C claimed for 150 d but ~1,460 h exist; 92-d absence vs 51 warm days.
`econ.window_margin(60, 60000, 33*24*0.8)` → 0.63

**2. Ice bearing for parked loads and edges.** Plant, cranes, rail, stockpiles on ice.
`ice.gold_allowable_load` (moving/≤2 h), `ice.stationary_load_capacity`, `ice.edge_capacity_factor` (~0.5 at cracks/slots), `ice.gold_required_thickness`.
Seen: locomotive needs 2.8 m vs 1.2-1.95 m (margin 0.48); 22 t on 0.8 m.
`ice.stationary_load_capacity(1.2, 24) * ice.edge_capacity_factor(1.2)` → ~12 t

**3. Ice thickness vs water depth.** Backwaters, ponds, riffles, wintering barges, under-ice transport, floes lifting stones.
`ice.ice_thickness(FDD, alpha)`, `ice.freezes_to_bed`, `ice.water_under_ice`, `ice.required_depth_under_ice`, `ice.freeze_on_below_ice`, `ice.stone_lift_capacity`, `ice.stacked_ice_capacity`.
Seen: 1.9-2.2 m ice leaves 0-0.6 m water in 2-2.5 m lakes; grounded floe freezes on 31-73 cm (402 vs 141 kg/m² lift).
`ice.freezes_to_bed(1.5, 6000, 0.024)` → True (1.86 m ice, draft 1.70 m)

**4. Frozen-ground strength vs exposure time.** Pillars, roofs, open holes, anchors, frozen dams kept for months-decades.
`geotech.vyalov_fit/vyalov_time_to_failure`, `pillar_tributary_stress`, `web_pillar_stress`, `mark_bieniawski_strength`, `beam_self_weight_stress`, `critical_span`, `adfreeze_strength(T, soil)`.
Seen: pillars 3 MPa vs ~1.25 MPa long-term; caving time 0.015-789 d; anchors at −1…−0.5 °C SF 0.57-1.4.
`geotech.adfreeze_strength(-0.5, 'clay')/geotech.adfreeze_strength(-3, 'clay')` → 0.3

**5. Thaw heat transfer at a frozen face.** Jets, creek films, galleries, sprinkling, hot-water drilling.
`thermal.h_gnielinski(..., roughness_factor=1-3)`, `h_jet_stagnation`, `h_ice_water_ashton`, `face_retreat_rate`, `ntu_required`, `efold_length`, `debris_coat_limited_flux`; transport of the thawed debris: `hydro.manning_depth_rect`, `critical_grain_size`, `bedload_capacity`.
Seen: needed h 11-33 kW/m²K (stagnation-only values); 1-2 cm debris coat caps flux; toe channel carries 2-19% of thaw; Shields 0.03 < 0.047 on 0.5-1% floors.
`thermal.face_retreat_rate(thermal.h_gnielinski(1, 0.2), 4, thermal.thaw_energy_per_m3(0.3, -4))*86400` → 9.1 m/day (clean face only)

**6. Water heat budget.** "Warm water/sun/waste heat thaws or keeps open".
`thermal.thaw_energy_per_m3`, `water_ratio`, `thaw_feed_rate`, `water_heat_power`, `open_water_heat_loss`, `water_surface_net_flux`, `melt_power`, `stefan_depth*`, `talik_depth_lake_axis`, `neumann_depth`, `freeze_time_cylinder`.
Seen: pond needs 239-358 W/m² vs 228 sunshine; open water loses 470-750 W/m² at −35…−40 °C; backfill freezes in 93-304 d not "weeks".
`thermal.water_ratio(thermal.thaw_energy_per_m3(0.3, -5), 4)` → 6 m³/m³

**7. Turbidity vs fishery limits.** Dredges, sluices, deflation, tailings into rivers/reservoirs.
`hydro.fines_release_rate`, `full_mixing_increment` (optimistic), `dilution_flow_required`, `allowed_escape_fraction`, `mixing_length`, `silt_curtain_outside`; limit `data.get('limit.fishery_ss_increment_high')` = +0.25 mg/L.
Seen: cutter alone (0.5% escape) needs ~1,900 m³/s of full mixing; 5% escape → +1-2.6 mg/L.
`hydro.dilution_flow_required(hydro.fines_release_rate(600, 1.9, 0.3, 0.005))` → 1,900 m³/s

**8. Market size and fixed-cost break-even.** Village coal, local plants, niche fleets.
`econ.market_share`, `breakeven_volume`, `levelised_cost`, `crf`, `six_tenths_scaling`.
Seen: one barge = 21-27% of Arctic Yakutia utility coal; single village 0.57-1.58x; break-even 4,800 km of road.
`econ.market_share(56e3, data.get('base.arctic_yakutia_utility_coal')[0])` → 0.27

**9. Missing best-practice baseline.** Every "N times cheaper".
`econ.ratio_vs_baseline`, `ceiling_ratio`, `carry_forward_cost`, `delay_pv_factor`; baselines `data.find('base.')` (sluice 3.2-9.9 m³/m³, boulder dozing $2.7-3/m³, matte $100-150/t Ni, grid power $0.05-0.08/kWh, Nome under-ice dredging).
Seen: diesel vs grid site, concentrate vs matte, blasting vs dozing; removing a 5-8% cost share caps the ratio at 1.05-1.09.
`econ.ceiling_ratio(0.05)` → 1.05

**10. Recovery losses.** Dry/wind/ice separation, cheaper-but-lossier routes, lost pods.
`econ.cost_per_recovered_unit`, `parity_recovery`, `breakeven_loss_fraction`, `thermal.freeze_concentration`, `hydro.aeolian_threshold_ustar`, `hydro.settling_velocity`.
Seen: quartz and gold thresholds 0.34-0.37 m/s; brine in ice cuts recovery to 51-71%; Ni/Cu concentrate tolerates 3% loss.
`econ.breakeven_loss_fraction(74.6, 2500)` → 0.029

**11. Floating and under-ice transport.** Pods, barges, frozen-in hulls.
`naval.draught_from_payload`, `payload_at_draught`, `rise_per_tonne`, `slide_threshold_velocity`, `max_buoyancy_to_slide`, `buoyancy_loss_from_melt`, `air_buoyancy_change_per_m`; `ice.edge_line_load_stress`, `ice.glen_strain_rate`, `ice.snow_viscosity`, `thermal.ice_melt_rate`.
Seen: drafts 3.75-3.9 m vs 2.0 m guaranteed; slide needs 0.6-0.95 m/s vs 0.05-0.25 measured; trim window gone in days.
`naval.slide_threshold_velocity(50, 1.0, 1.0, 0.5)` → 0.70 m/s

**12. Thawed-ground slopes and runout.** Thaw slumps, gravity stripping, slurry cells.
`geotech.thawing_slope_fs`, `thawing_slope_critical_thickness`, `thaw_consolidation_ratio`, `bingham_min_flow_thickness`, `consolidation_t90`, `darcy_seepage`, `hydro.froehlich_peak_outflow`.
Seen: 0.2-0.9 m sheets stall (need 0.73-8.2 m); t90 7.6-41 yr; frozen-lump dams leak 0.09-8.5 m³/s.
`geotech.bingham_min_flow_thickness(800, 1600, 4)` → 0.73 m

**13. Can a pilot prove it?** Loss rates, grade differences, reliability.
`stats.zero_failure_upper_bound`, `trials_for_zero_failure`, `poisson_ci`, `sample_size_mean`, `sample_size_two_arms`, `sample_size_proportion`.
Seen: 20 pods prove only <14% loss; 1.16x needs 64-178 block-months per arm.
`stats.trials_for_zero_failure(0.05)` → 59

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

Ground every decisive input in a source or in measured data, not in the idea's own text. Before you use any
calculation you wrote yourself (not from the kit), check it once on a case with a known answer.

VERDICT: ALIVE if MARGIN >= 1 and RATIO >= 1.5; DEAD if MARGIN < 0.3 or RATIO < 1.1; otherwise WOUNDED.
Be strict and fair: a beautiful idea that fails by 10x is DEAD; a dull idea with headroom is ALIVE.

Final answer (text only), exactly this format, one block per idea in the order given:
=== GATE ===
IDEA 1: <name>
SCREEN | <class: margin; class: margin; ...>
KILLER | <quantity> | required <value unit> | available <value unit> (<source>) | MARGIN <number>
CHAIN | <best current practice> | now <cost unit> | with idea <cost unit> | RATIO <number>
VERDICT | <ALIVE/WOUNDED/DEAD> | <one sentence>
NEW FACT | <any hard, sourced fact you found that the ledger did not contain> | <source> (optional, any number)
(same for the other ideas)

THE 8 IDEAS:
IDEA 1
NAME: Downstream coal on empty barges
MECHANISM: On the Kolyma, the summer Northern Delivery convoys bring fuel and goods upstream from Chersky and come back down empty. They pass riverside pits like Zyryanka on the way, so they could carry coal down on that return leg. The cost is only marginal: a short loading stop plus a little extra draft. Return-cargo pricing is common in shipping, but no Kolyma coal-on-the-return contract was found. Such cargo normally fails when directions do not match, and here they do. The deciding quantity is how much load the empty barges can take at late-season water depths, given that shoaling already limits loaded barges to under 50%.
VALUE: Cuts the barge cost per tonne several-fold using vessels that already make the trip, with no new capital.

IDEA 2
NAME: Frozen-in bunker-boiler barge
MECHANISM: A barge carries the full year's coal in summer and stays for the winter in a sheltered backwater (затон) next to the village. Its hold is the coal store, and a boiler module on deck feeds the village heat main through an insulated link to shore. Searches found no frozen-in boiler-barge case. The closest is Akademik Lomonosov, which at 70 MW was far too big for a village and overran its budget 4.1x. This design uses a standard river barge and an off-the-shelf boiler. The deciding quantity is hull survival through about 8 months of ice and the spring breakup flood, which existing backwater wintering of river fleets suggests is manageable.
VALUE: Removes the winter-road last mile, the shore stockpile, double handling and a separate boilerhouse, which by these numbers roughly halves the cost of heat in the village.

IDEA 3
NAME: Frozen-in barge boilerhouse
MECHANISM: A barge from the ageing Lena/Kolyma fleet, near scrap value, gets a containerised boiler and a 2–3 kt coal hold. It arrives at the settlement on high water and is frozen in at a berth, with an air-bubbler kept running to stop ice pressure. All winter it burns its own cargo and sends heat to shore through an insulated pipe. This deletes three steps: transshipment, the shore stockpile and the winter-road last mile. The closest attempt is the Akademik Lomonosov floating plant, which was stopped by 70 MW of scale and a 4x capital overrun. This uses a written-off hull and a boiler of about 1–5 MW. Deciding quantity: annualised hull plus boiler cost per hold-tonne against the last-mile and handling share it removes (about 11,000–15,000 rub/t, est.). That share needs sourcing.
VALUE: A settlement could be fuelled with no winter road and no shore coal yard.

IDEA 4
NAME: Frozen-in barge as bunker-boilerhouse
MECHANISM: Shallow-draft barges (≤0.8 m) carry coal straight to the settlement on late-summer water. One barge then winters in a deep pool beside the village, holding the coal and a containerised boiler connected to the heat main. This removes the winter-road last mile (about 300 km × 20 rub/t-km ≈ 6,000 rub/t, est.), the transshipment and the stockpile losses. Because the draft is low, barges load fully at Lena-type 150 cm levels, where today's fleets carry under 50%. The closest earlier attempt is ordinary barge-to-depot delivery, which was stopped by shoaling and the need to transship. A search found no prior frozen-in bunker barge. The deciding quantity is whether a pool within 2 km of the village stays deeper than the hull draft plus a 2 m ice cover all winter.
VALUE: An estimated 23,000 to about 7,000 rub/t (about 3.3x) with no new mine, if the per-trip barge cost halves at full load; the same frozen-in hull gives remote Arctic mines a summer-filled winter depot.

IDEA 5
NAME: Long-season tracked sled trains
MECHANISM: One wide-tracked tractor tows 8-12 low-pressure freight sleds over snow and river ice. Ground pressure is low enough to start in October and run into May, about 150+ days against the truck winter road's 45-54 (ATTEMPT 1). One driver moves 150-250 t instead of 25 t per truck, and sleds left at the settlement serve as the coal stockpile. The closest attempts are the 1950s Alaskan cat trains, displaced by trucks and air, and Antarctic traverses, which are costed for fuel loads rather than bulk coal; neither was set against a 45-day road window. The deciding quantity is cost per tonne-km; it must fall below ~5 rub/t-km against the winter road's 20.
VALUE: Inland settlements beyond barge reach could get a winter supply route about three times longer and several times cheaper per tonne.

IDEA 6
NAME: River-thawed bluff lignite scraping
MECHANISM: Many Yakutian rivers cut lignite or coal seams in their bluffs. A sun-facing bluff thaws about 1.5 m deep each summer (est.), so a small excavator can scrape the thawed face without drilling or blasting. The scraped coal goes to a stockpile and moves to the village by a winter road of 30 km or less. A 3 m seam gives about 6 t per metre of face, so about 1 km of face per year covers a village of 1,000 people burning about 6,000 t of coal-equivalent. The closest earlier attempts were Corwin Bluff and Qullissat, which stopped on rare ship calls, falling profit and poor coal. Here the buyer is the village boiler, priced against the 23,000 rub baseline, and no ship is involved. The deciding quantity is summer thaw depth multiplied by the length of seam face within 30 km of the village.
VALUE: Estimated 4,800 rub per coal-equivalent tonne (3,500 kcal lignite, about 4.8x cheaper), which turns stranded small river-bluff deposits into a settlement fuel base.

IDEA 7
NAME: Flood-crest barge launch
MECHANISM: Coal goes from the pit in winter and is loaded onto barges wintering in a sheltered backwater near it. The barges wait out the ice drift and leave on the spring flood crest. That way they travel fully loaded, not under 50% as on summer shoal water. The closest attempt is the "early delivery" voyages, which hit drifting ice and lost the crest. Here the barges shelter during the drift, and the timing is computed from gauge forecasts. Deciding quantity: the days between the reach clearing of ice and water falling below loaded draft, compared with the transit time.
VALUE: The cost per tonne of the main barge haul roughly halves.

IDEA 8
NAME: Frozen-in barge boilerhouse
MECHANISM: A barge carries a full winter's coal in its hold and a containerised boiler on deck. In autumn it is moored and allowed to freeze in at a riverside settlement, and an insulated heat main of about 200 m runs ashore. The boiler burns straight from the hold all winter, so there is no unloading, no shore stockpile, no loader fleet and no second handling; the barge returns empty after breakup to refill at the pit. Barges already winter frozen-in in river backwaters, and no search found a barge used as boilerhouse and bunker (ATTEMPT 23). The deciding quantity is the share of the ~23,000 rub/t spent after the barge haul (handling, stockpile losses, last mile); it must exceed ~65% to reach 3x.
VALUE: Riverside settlements could get boiler coal for roughly the cost of the barge haul alone.

