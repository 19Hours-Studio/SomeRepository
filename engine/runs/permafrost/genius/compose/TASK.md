# Task: compose whole chains from the pieces that survived review

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Single ideas have so far given at most 1.2-3x on ONE link of the chain, never "several times cheaper" on the whole
route from the deposit to the market. Your job is to build WHOLE CHAINS out of the surviving pieces below plus best
current practice, so that the gains of several links multiply, and to compute honestly whether any chain reaches
several times cheaper than current practice.

You have tools: Bash with python3, WebSearch (WebFetch does not resolve domains here), and the verified calculation kit
in `/home/user/SomeRepository/engine/kit/` (catalog below; import it instead of rewriting physics). Work only in `/home/user/SomeRepository/engine/runs/permafrost/genius/compose/`: write files only
there, read no other repository files except the kit, do not commit.

Rules:
1. A chain covers the whole route for one product, from the deposit to the point of sale or use (refinery, port,
   village boiler, consumer), as a sequence of links. Each link is either a piece below (cite it as P<k>) or the best
   current practice. At least two links must be pieces.
2. The pieces must fit together: the same kind of site, season, scale and market. At least one COUPLING where one link
   supplies what another link needs (heat, water, ice, timing, a vessel, a market, a waste stream) - name it and
   compute it.
3. Respect each piece's review findings: use the reviewed numbers and ranges, not the original claims, and fix or
   avoid every listed FATAL/MAJOR defect in the chain design (say how).
4. For each chain, compute in python a link table: link | method | cost per unit of FINAL product now (current
   practice) | with the chain | source or piece. Chain RATIO = total now / total with the chain. Give two ratios:
   against current practice as operated today, and against the best competent alternative (e.g. a local pit where a
   seam outcrops, an on-site concentrator). Respect the ceiling: shares no link touches (taxes, royalties) cap the
   ratio (`econ.ceiling_ratio`).
5. Name the weakest link and the decisive unknown, with the threshold at which the chain drops below 2x.
6. Build at most 4 chains, the strongest first. Drop any chain below 2x against current practice. If no chain reaches
   3x against current practice, say so plainly and give the best you found.

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

Where the money goes today (data):
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

What was tried before and why it did not solve the problem (data):
ATTEMPT 1: Winter ice road to remote mines | Tibbitt-Contwoyto, NWT Canada (Ekati, Diavik, Gahcho Kue); Yakutian zimniki | standard practice | WHY IT DID NOT SOLVE IT: season, not road cost: open 54 days in 2019 (7,489 loaded trucks, 257,176 t); 2026 peak window 45 days vs 65-70 historic, so airlift | https://skillings.net/arctic-logistics-crisis-record-warmth-shuts-diamond-mine-ice-roads
ATTEMPT 2: Icebreaking ships from the field | Yamal LNG, Sabetta, Novatek, 2017 | standard, giant flows only | WHY IT DID NOT SOLVE IT: needs 16.5 Mt/yr LNG to carry ~16 Arc7 carriers at ~$316m each (~$5bn, press figures) | https://offshore-energy.biz/russias-yamal-lng-project-adds-two-arc7-carriers-as-first-shipment-nears
ATTEMPT 3: Rail to tidewater | Baffinland Mary River: Steensby railway approved 2012, dropped 2014; 100 km tote road to Milne Inlet used instead | costed and rejected | WHY IT DID NOT SOLVE IT: Steensby rail $5.7bn est. (~5x Milne line) to lift 4.2 to 22 Mt/yr; company later owed $1.07bn | https://www.rcinet.ca/eye-on-the-arctic/?p=154201
ATTEMPT 4: Pipeline over permafrost | Trans-Alaska 1975-77; Mackenzie Valley gas, Canada | TAPS built; Mackenzie costed and shelved | WHY IT DID NOT SOLVE IT: TAPS ~$8bn, ~half elevated, 124,000 heat pipes; Mackenzie C$16.2bn on hold 2012, abandoned 2017 as shale cut gas prices | https://en.wikipedia.org/wiki/Mackenzie_Valley_Pipeline
ATTEMPT 5: Cold-water needle thawing, then bucket-line dredge | Fairbanks Exploration Co 1928-59; Klondike Dredge No. 4, April-November | standard until ~1960 | WHY IT DID NOT SOLVE IT: thaw leads a year ahead (points 16 ft apart, 6+ weeks each, 4-5 thaw months), 26 cents/yd3 in 1954-58; subarctic dredging costs 2-3x temperate | https://dggs.alaska.gov/webpubs/usbm/un/text/mulligan_1967.pdf https://www.911metallurgist.com/?p=978570
ATTEMPT 6: Offshore dredge in Arctic water | Bima, Nome, Inspiration/WestGold, 1986-90 | pilot dropped | WHY IT DID NOT SOLVE IT: water open only from mid-June, storms; 126,924 oz in five seasons, two profitable | https://en.wikipedia.org/wiki/Bima_(dredge)
ATTEMPT 7: Winter dredging with covers or hangar | Siberian Federal University, polycarbonate hangar over dredge pit, 2020-23 | paper stage, no operating case found | WHY IT DID NOT SOLVE IT: covers add only ~1.5 months; later solid ice blocks dredge movement | https://scholar.sfu.ru/publication/504653455-867958319
ATTEMPT 8: Drain the lake, then dig | Diavik A154 dike, NWT, 2001-02 | standard for kimberlite | WHY IT DID NOT SOLVE IT: 3.9 km dike up to 25 m high, 30 m of lake-bottom sediment stripped first; mine C$1.3bn, viable only for diamonds | https://northernminer.com/news/canada-s-second-diamond-mine-prepares-for-startup/1000148810
ATTEMPT 9: Dredge a talik under lake ice | NOT FOUND. Searched English and Russian: placer under thermokarst lake, подозерные талики россыпи драга, winter ice-cutting dredge, Kolyma/Yukon/Fairbanks winter dredging | -
ATTEMPT 10: Rip, blast and dozer-strip frozen overburden | Yakutian open pits and placers | standard | WHY IT DID NOT SOLVE IT: frozen rock needs mandatory drilling and blasting, and blasted rock refreezes; no per-m3 figure found | https://vestnik.magtu.ru/en/134-archive/no-2-2026/1920-40.html
ATTEMPT 11: Saw or cut frozen ground | Soviet trials, Sergeev, 1950s | dropped | WHY IT DID NOT SOLVE IT: disc saws and drop-hammer cutters "useless"; narrow-channel cutters wore blades fast | https://apps.dtic.mil/sti/html/tr/AD0648510/index.html
ATTEMPT 12: Leave overburden frozen, mine by borehole | Ryveem River, Chukotka (semi-commercial); US Bureau of Mines prototype 1997-98 | pilot, stayed small | WHY IT DID NOT SOLVE IT: calculated ceiling 1 t gold/yr for a 30 m placer, one-well scale | https://www.rudmet.ru/journal/1793/article/30642/?language=en
ATTEMPT 13: Quarry-style block cutting with jacks | wire-saw limestone quarry (Ireland), blocks to 1,000 t | standard in dimension stone | WHY IT DID NOT SOLVE IT: largest blocks are 1/30 of 30,400 t, and priced for premium stone | https://www.stonefed.org.uk/app/uploads/2021/02/McKeonFeature.pdf
ATTEMPT 14: Drift mining under frozen cover | Fairbanks and Klondike 1890s-1920s; Magadan | niche | WHY IT DID NOT SOLVE IT: fire thawed ~12 in per night; steam thaw 34 cents/yd3 at Coal Creek, "too expensive"; dredges overtook | https://www.nps.gov/yuch/learn/historyculture/steam-boiler.htm
ATTEMPT 15: Ships coal at a coast bluff | Corwin Bluff, Cape Beaufort, Alaska, 1880s-1901 | dropped | WHY IT DID NOT SOLVE IT: only seasonal ship calls, mine attempt c.1884, one Nome shipment 1900-01; no tonnage series found | https://dggs.alaska.gov/webpubs/usgs/of/text/of71-0061.pdf
ATTEMPT 16: Floating dredge mining coal | Susquehanna River, Pennsylvania, c.1900-1972 | ended | WHY IT DID NOT SOLVE IT: ~75,000 t/yr, ~2 Mt in total, fines recovery not a mine | https://unchartedlancaster.com/2023/06/17/scraping-the-bottom-dredging-for-coal-on-the-susquehanna/
ATTEMPT 17: Small Arctic pit for local heat | Qullissat, Greenland (closed 1972); Longyearbyen Mine 7 (plant closed 2023) | closed | WHY IT DID NOT SOLVE IT: Qullissat 30-40 kt/yr, 570 kt total, shut on falling profit and poor coal; Mine 7 ~30 kt/yr local, high-grade coal exhausted | https://en.wikipedia.org/wiki/Qullissat https://www.highnorthnews.com/en/node/58713
ATTEMPT 18: Village coal instead of oil | NW Alaska, Dames & Moore for Alaska Power Authority, 1980 | studied, not built | WHY IT DID NOT SOLVE IT: oil is subsidized: Wainwright residents paid $1.50/gal vs $7.83 commercial (2009) | https://www.nrel.gov/state-local-tribal/etipp-community-wainwright-alaska
ATTEMPT 19: Rock cover to keep ground frozen | Qinghai-Tibet railway crushed-rock revetment; Kivalina, Alaska | standard on rail; village niche | WHY IT DID NOT SOLVE IT: crushed rock alone cools less than thermosyphons (over 80 cm needed); Kivalina seawall lost 1,000 of 1,600 ft in 2007 | https://phys.org/news/2021-05-mitigation-permafrost-tibet-plateau.html https://gov.alaska.gov/admin-orders/administrative-order-no-231/
ATTEMPT 20: Floating plant as village heat source | Akademik Lomonosov, Pevek, 2020 | in use | WHY IT DID NOT SOLVE IT: cost rose RUB 9bn to 37bn (4.1x); 70 MW and 50 Gcal/h, far above a village | https://bellona.org/news/nuclear-issues/2015-05-new-documents-show-cost-russian-nuclear-power-plant-skyrockets
ATTEMPT 21: Winter fuel after missing the last barge | Nome, Alaska, 2012 | one-off | WHY IT DID NOT SOLVE IT: 1.3m gal needed a Russian tanker plus icebreaker through 300 nmi of ice; airlift meant 300+ flights | https://response.restoration.noaa.gov/node/342
ATTEMPT 22: Shallow river barges to depots | Lena, Yana, Indigirka | standard | WHY IT DID NOT SOLVE IT: shoaling: Lena levels of 150 cm let shallow fleets load under 50% | https://en.portnews.ru/news/167121
ATTEMPT 23: Barge as winter boilerhouse and coal bunker | NOT FOUND. Searched English and Russian: плавучая котельная баржа зимовка, floating boiler house, frozen-in barge heating, winter fuel barge storage | -
LESSONS: Season, not distance, binds: ice road 45-54 days, dredges 5-6 months, open water from mid-June, thaw 4-5 months.
Scale kills: ships, rail and pipe need 4-22 Mt/yr to repay ($316m carriers, $5.7bn rail, C$16bn pipe); village and placer flows (30-75 kt/yr, 1 t gold) never repaid.
Frozen ground resists tools (blade wear, refreezing, saws useless); only summer-temperature water thaws cheaply, at a year's lead.
Small coal and plant schemes died when a captive buyer or subsidy vanished, or when capital overran 4x.
A new answer needs a winter-capable, sub-1 Mt/yr unit with no thaw lead, on-site storage and no subsidy dependence.

Final answer (text only), in this order:
=== IDEAS ===
IDEA 1
NAME: (max 6 words)
MECHANISM: (3-6 sentences: the links in order, which pieces, the coupling, what fixes the reviewed defects)
VALUE: (1-2 sentences: chain RATIO against current practice and against the best competent alternative, for what product and market size)
(same for each further chain)
=== CHAINS ===
CHAIN 1: the link table, the two ratios, the weakest link, the decisive unknown and its threshold
(same for each further chain)

THE 8 PIECES (each with its blind review):
P1
NAME: Self-Detaching Thaw-Face Stripping
MECHANISM: Anchor kept: excess pore pressure at the thaw front of ice-rich muck carries the thawed layer downslope into the mined cell by gravity. The mechanism checks out: R = α/(2√cv) is 0.9-1.6, which puts the frictional sliding threshold at about 2-5°. The original layout fails, though: with 0.5-2 kPa of cohesion, a whole surface graded at 5-8° only slides once the sheet is 1.9-12 m thick, more than the 1.6 m that thaws in a season. Repaired design: cut long, south-facing faces at 10-12° and sprinkle them with creek water. Sheets 0.2-0.9 m thick then detach several times a season, which keeps the face bare and thawing about 3 m per season. Each metre of face yields 115-138 m³ per season, so 0.5 Mm³ needs about 4 km of face. The slurry (yield stress under 500 Pa) runs down the roughly 4° drop into the adjacent mined cell and settles to 0.64 of its frozen volume. Stripping has to start 4-9 seasons ahead of mining.
VALUE: Stripping drops from about $1.0/m³ (natural thaw plus dozing) to about $0.3/m³, 3× cheaper. That cuts delivered gold cost by about 15% in ordinary muck and by up to about 40% in Yedoma (over 60% ice), where dozers bog down and the alternative is digging frozen ground at about $3.5/m³.
BLIND REVIEW:
- MAJOR: The approach is not new, and the baseline leaves out hydraulic stripping of frozen muck, which has been practised for a century and removes muck about 10x faster per unit of face. (Fairbanks Exploration Co. ran 36-48 giants for 150-180 days a year, thawing and removing overburden at about 9 in/day (0.23 m/day = 34-41 m per season), against 3 m per season here (ASME landmark history). Russian placer practice already uses hydraulic stripping (гидровскрыша) and sprinkler thawing (дождевальная оттайка).)
- MAJOR: The 3x cost ratio leaves out the cost of carrying stripping 4-9 seasons ahead of mining. ($0.30/m³ carried forward 4-9 yr at 10-15% becomes $0.44-1.06/m³ at mining, against $1.10-1.15 for one-season natural thaw, so the advantage is 1.1-2.5x. At 20% and 9 yr it is 0.78x, worse than baseline (python).)
- MAJOR: Detachment at 10-12° is not robust: at the high-cohesion/low-R corner the critical sheet is about one full season of natural thaw, and the design's own 0.9 m upper sheet gives 1.6-2.3 m/season, not 3 m. (Infinite-slope check with γ 16.5 kN/m³, γ'/γ 0.45, φ' 28°: z_crit at 10°, c' 2 kPa, R 0.9 is 1.47 m, against 1.6 m natural thaw. Stefan with periodic removal (k 1.3 W/mK, 10 °C, 100 d): 0.45 m sheets give 3.3-4.7 m, 0.9 m sheets give 1.6-2.3 m. At 1.6-2.3 m per season the yield is ~60-100 m³ per m and the face for 0.5 Mm³ is 5-8 km. Lab thaw of sandy silt on a 12° slope (Harris et al. 1995, PPP 6:293) gave creep, no rapid failure.)
- MAJOR: The runout depends on a slurry yield stress below 500 Pa that is not sourced; with measured thawed strengths the thin sheets stall on the 4° path and re-bury the toe, which is how natural thaw slumps stabilise. (Measured undrained strength after thaw is 0.8-9 kPa (Harris et al. 1995). A Bingham layer at ρ 1600 kg/m³ needs h ≥ τy/(ρ g sin4°) = 0.73-8.2 m to flow. Even at 500 Pa it needs ≥0.46 m, against 0.2-0.9 m sheets.)
- MAJOR: The mined cell must hold fluid mud for years: the slurry reaches 0.64 of its frozen volume only after consolidation, and at first it occupies about 0.95 of it. (The cv implied by R 0.9-1.6 is 0.5-2.8 m²/yr, so t90 = 0.85H²/cv = 7.6-41 yr for a 5 m single-drainage fill. Ice-to-water shrinkage is only 9% of the ice volume. The cell therefore needs ~50% more capacity than designed, plus a slurry dyke beside the active cut.)
- SURVIVES: The thaw-consolidation sliding threshold reproduces at 1.8-6.4° for φ' 25-33° and γ'/γ 0.4-0.5. 0.5 Mm³ ÷ 115-138 m³/m = 3.6-4.3 km. The 15%/40% gold-cost cuts imply plausible stripping shares of 21%/44%. About 3 m/season is physically possible if sheets stay ≤0.45 m and the mean surface temperature is ≥10 °C.

P2
NAME: Pond-Heated Jet Undercut Caving
MECHANISM: Anchor: creek water thaws and removes the pay from under the frozen overburden, and the overburden then caves onto bedrock under its own weight, with no stripping and no roof support. A creek flowing through a gallery fails: at valley slopes of 0.5-1 % the Shields number is 0.026-0.043, below the 0.047 needed to move gravel, so the thawed gravel stays put and the gold settles on the gallery floor under the caving roof. Repaired design: low-pressure jets (monitors) using water from the solar-warmed recycle pond and the creek (a 3 ha pond absorbs about 5.4 MW in July-August) thaw the face. Heat delivered vs needed is 1.27 at 4 °C and 2.5 at 7 °C, at 7 m³ of water per m³ of gravel. A hydro-elevator lifts the slurry to a sluice at the portal. Panels about 25 m wide retreat with nobody underground, and the roof caves within hours to days (0.58 MPa bending stress against 0.2-0.5 MPa long-term tensile strength). Two monitors give about 216 k m³ of pay per 70-day season at about 650 rub/m³ (556-965 across the sensitivity range).
VALUE: For deep, thin frozen placers (overburden:pay ratio 6 or more) it costs about 620 rub/g against 1,100-2,650 rub/g for the cheaper of open-cut and drill-blast underground mining, 1.8-3.4× cheaper.
BLIND REVIEW:
- MAJOR: The roof is not shown to cave "within hours to days": bending stress falls as 1/cover, and across the idea's own range of long-term strength the time to failure spans five orders of magnitude, with no caving at all for thicker cover. (sigma=gamma*L^2/(2h) with gamma=19 kN/m3 and L=25 m gives 0.59 MPa at 10 m of cover, 0.40 at 15 m, 0.30 at 20 m and 0.20 at 30 m. A Vyalov law sigma=beta/ln(t/B), fitted to 1-2 MPa short-term and 0.2-0.5 MPa 50-yr strength, gives a time to failure at 0.58 MPa of 0.015-789 days. At 20 m or more of cover the roof never fails if the long-term strength is 0.35 MPa or above. Rochev (Gornyi Zh. 2016) cites the "stable roof" of frozen pay as the reason borehole hydraulic mining works.)
- MAJOR: Output depends on a face thaw rate that is assumed, not sourced: two monitors at 1,543 m3/d each on a 25 m face means the face retreats 21-62 m/d (pay 3-1 m), which needs a face-average heat flux of 22-66 kW/m2. (That flux needs h=11-33 kW/m2K at the ~2 K mean dT allowed by water going in at 4 C and leaving at 0.9 C. A sweeping jet would have to hold that over the whole face, all the time. It is the top of the range for a rough fast film (8-22 kW/m2K at 1-3 m/s; Gnielinski x3 roughness per Douglas et al. 2023) and equals jet stagnation values (12-15 kW/m2K for a 50 mm jet at 10-15 m/s). Each monitor needs hA of at least 781 kW/K; at h=3-6 kW/m2K that means 130-260 m2 of wetted frozen surface against a 50 m2 face, so the heat goes into roof, ribs and bedrock rather than pay.)
- MAJOR: The cost ratio does not reproduce, and the idea's own sensitivity range wipes most of it out. (650/620 implies 1.05 g/m3 recovered. 1,100/620 = 1.77x and 2,650/620 = 4.27x (not 3.4x). At the 965 rub/m3 end, 920 rub/g gives only 1.20x against 1,100 rub/g, which is not "several times".)
- MAJOR: It is not new, and it ignores the direct competitor: thawing frozen placer pay with water jets and lifting it as slurry has been field-tested, and borehole hydraulic mining is the baseline for deep thin frozen placers. (The USBM/NIOSH prototype borehole miner (Tech News 460, Tenderfoot Creek, AK; 0.3 m pay under 13 m cover) jet-thawed the pay and pumped it up. Arens et al. (Gornyi Zh. 2019) used warm-water jetting with an airlift at the Ryveem placer in Chukotka and designed for up to 1 t Au/yr.)
- MAJOR: By its own Shields result (0.026-0.043 < 0.047), gravel will not flow along a 0.5-1% floor, so the hydro-elevator sump must stay within one jet working length of the face and be moved every few hours under unsupported roof. That contradicts "nobody underground". (A monitor's working length is 350-450 nozzle diameters, about 18-34 m for 50-75 mm nozzles, while the face retreats 21-62 m/d.)
- MAJOR: Gold in the bedrock is lost: 4-7 C jets cannot dig frozen fractured bedrock, which is normally mined as part of the pay, yet recovery is costed as if equal to open-cut. (Taking the usual 0.2-0.5 m of bedrock (typical practice, not sourced here), that is 7-50% of a 1-3 m pay layer. Each 10% of gold left behind raises the 620 rub/g by about 11%.)
- MAJOR: Water inrush and thermokarst are not mentioned: caving 6-18 m of cover in the valley floor brings cracks and subsidence right under the creek and beside the 3 ha pond that feed the jets. (Subsidence of 0.7-0.9 times the extracted height (assumed caving factor) is 0.7-2.7 m over 25 m panels.)
- SURVIVES: The Shields figures reproduce at constant discharge (tau* ~ S^0.7, ratio 1.62 against 1.65 stated). 5.4 MW is a plausible July-August average for the pond (4.7-6.5 MW from the energy balance). The water flow (0.25 m3/s) and thaw demand (3.3 MW) are consistent, and 0.58 MPa holds at 10 m of cover.

P3
NAME: Ice-Deck Borehole Talik Mining
MECHANISM: Anchor: drill from winter lake ice into the sub-lake talik, which is already thawed, and mine the pay by borehole hydraulic mining. That means no thaw (saves 90 MJ/m³, about 25 kWh/m³), no dike, no drainage and no stripping. Repair: 1.2 m of ice carries only ~25 t of parked load, so the ice is flood-thickened to ≥1.8 m (Gold's formula at A=3.5 kg/cm² gives 113 t short-term, ~57 t parked). The 20-25 t modules sit more than 57 m apart, and the casing is insulated where it passes through the ice. Loose saturated talik gravel holds no roof and caves into the cavity, so the method is limited to narrow (25-40 m), deep, fine-gravel buried channels (<15 cm, the intake limit). Holes go on an 18 m grid (jet reach R=9 m) and are airlifted at 20-40 m³/h. Drawing stops at D≈3.4-3.9 m³ drawn per m³ of pay, set by on-ice jig grade monitoring; this extracts 86-89% of the pay in each hole's footprint, and tailings go back down mined holes. Cost: 1,130-1,970 rub per m³ drawn, which is 3,000-4,800 rub/g of gold recovered.
VALUE: Recovers gold from narrow, deep sub-lake channels that today go unmined, at 3,000-4,800 rub/g. The cheapest alternative, a summer pontoon suction dredge, costs ≥8,800 rub/g, so this is 1.8-4.4x cheaper; on channels wider than 80 m it is only 1-1.5x cheaper.
BLIND REVIEW:
- MAJOR: A 9 m reach for an underwater jet in gravel is not credible without megawatt-scale pumping: at 9 m the jet's centreline speed is 1.2–3.4 m/s, against 1.6–2.8 m/s needed to move 5–15 cm gravel. Reaching it takes ≥10–15 MPa and 237–419 m³/h, and the jet's fuel alone costs 0.24–3x the whole stated cost per m³. Cut gravel also has to travel 9 m to the intake over a floor sloping only 6–18° (pay 1–3 m), below its ~30–35° angle of repose (Jet decay u_c = 6.2·d/x·u₀; 0.66–1.74 MW of hydraulic power = 475–3,454 rub/m³ of fuel at 20–40 m³/h, against 1,130–1,970 rub/m³ total.)
- MAJOR: The ice margin rests on Gold's formula, which is for moving loads, yet the modules stay parked for days beside an open cased hole on partly flooded ice (NWT DOT 2015: Gold's guidance is "not appropriate" for stationary loads and drill pads. Westergaard's edge-to-interior factor of 0.66 cuts 57 t to 38 t; counting the flooded layer at 50% cuts it to 26 t, against 20–25 t modules (safety factor 1.0–1.3). Each hole takes 1.6–11 d.)
- MAJOR: On an 18 m square grid, R=9 m circles leave 21.5% of each cell outside any jet, so recovery per unit area is at most 68–70%, not 86–89%; the rest is left behind unless spacing drops to 12.7 m, which doubles the number of holes (π/4 = 0.785; 0.785 × 0.86–0.89 = 0.68–0.70; (18/12.73)² = 2.0.)
- MAJOR: The baseline ignores draining the lake and dry-mining the talik, which is already thawed and needs no thaw energy. Where the cover is thin enough to strip, the open-cut cost used in Idea 1 overlaps this idea's cost (2,270–3,980 rub/g against 3,000–4,800 rub/g gives 0.47–1.33x.)
- SURVIVES: 90 MJ = 25 kWh; Gold with A=3.5 gives 50/113 t short-term and 25/57 t halved for 1.2/1.8 m ice; 57 m is 2.6–3.0 ice characteristic lengths, enough to keep loads from interacting; the cost-per-gram range reproduces with an implied 1.3–1.6 g recovered per m³ of pay; 1.6–11 d per hole fits a ~100-day ice season.

P4
NAME: Channel-Talik Seam Dredging
MECHANISM: Anchor: a dredge cuts the coal seam in place inside the unfrozen channel talik, where the river has already removed the cover, and pumps it into a hopper barge. Repair: only seams at thalweg level under high bluffs, where a bank pit would have to strip 15-25 m³/t. A leased dredge with a 150 kW cutter cuts lignite (UCS 5-7 MPa) at 46-65 m³/h, which is about 46-65 t/h and matches Kovin's measured 67 t/h. A 10 kt village-cluster year therefore takes 8-25 dredge-days, not "a week", and one dredge visits about 4 bends a season. An on-barge dewatering screen brings the coal to ~32% moisture (3,670 kcal/kg). Cutting in June-July lets stockpiles drain before freeze-up. Delivered cost is 2,700-4,300 rub/t, which is 730-1,170 rub/Gcal.
VALUE: 730-930 rub/Gcal with a shared dredge, against 2,830 rub/Gcal for northern-delivery coal at 15k rub/t (3.0-3.9x cheaper) and 1.4-2.4x below a bank micro-pit under high bluffs. There is no gain where the same seam has thin cover on land.
BLIND REVIEW:
- MAJOR: The Kovin cross-check is false: Kovin's ~67 t/h comes from a 750 kW bucket-wheel cutter on a ~10 MW dredge, not a 150 kW cutter. Scaled by cutter power, 150 kW gives ~13 t/h, so a 10 kt year takes 31–52 dredge-days and one dredge serves about 1 bend a season, not 4 (4,400,863 t ÷ 66,056 h = 66.6 t/h (Serbian 2024 paper); Kovin I has a 750 kW cutter and 10,090 kW total (DredgePoint); 66.6/750×150 = 13.3 t/h. The claimed 46–65 m³/h implies 8.3–11.7 MJ/m³ = 1.2–2.3×UCS, which only ideal sharp-tool cutting reaches, and no test backs it.)
- MAJOR: 32% total moisture after slurry transport and a dewatering screen is impossible for a true lignite: with 10–15% surface moisture, the coal's own (bed) moisture would have to be ≤20–24% (brown-coal class B3), whereas classes B1/B2 are 30–>40% (Totals of 37–49% give LHV 2,640–3,400 kcal/kg (dry ash-free GCV 6,800, 12% ash), raising rub/Gcal by ×1.08–1.39. Soviet classes: B1 >40%, B2 30–40%, B3 <30%.)
- MAJOR: The June–July window cannot hold 4 bends: these rivers are ice-free only from early June, and break-up brings ice jams and floods (Kolyma is under ice ~250 d/yr and ice-free only from early June (Britannica, Wikipedia). 4 × (8–25 d + 3 d transit) = 44–112 d; at 25 d per bend only 1–2 bends fit in 45–61 d, so 730–930 rub/Gcal holds only at the low end of the dredge-day range.)
- MAJOR: Fresh brown coal sits in stockpiles through the warm Aug–Sep months before freeze-up, brown coal is the rank most prone to self-heating, and no storage limit or fire control is costed (Brown coal in open storage starts to self-ignite after ≥2 weeks (TPU); the plan stores it ≥60 d before freeze-up.)
- SURVIVES: 2,700–4,300 ÷ 3.67 = 736–1,172 rub/Gcal and 15,000/2,830 = 5.3 Gcal/t reproduce; 3,670 kcal/kg at 32% moisture is consistent with dry ash-free GCV 6,300–7,200 and 8–15% ash; the cutting energy is within 1.2–2.3×UCS.

P5
NAME: Barge-Mounted Bluff Auger Coal
MECHANISM: Anchor: a spudded floating auger bores a frozen seam at water level in a river bluff and discharges straight into a hold, so no overburden is moved. At 20 kt/yr the rig sits idle most of the year and costs about 4,100 rub/t. The repaired version runs the whole ~100-day navigation season at about 60 t/h, for about 80 kt/yr. That rate sits between historical augers (21.5 t/h) and highwall miners (100–140 t/h). It fills four hopper barges moored alongside instead of its own hold. Thrust of 150–300 kN is taken by a frame bolted to the face, because three spuds (about 360 kN) are marginal. The frame has about 3 m of vertical travel to follow the 1–3 m drop in low-water stage during a campaign. Holes rise slightly so they drain. Face recovery is 62%, about 190 t per 80 m hole, which uses about 0.9 km of bluff a year.
VALUE: About 1,800 rub/t at a village bank within 150 km. That compares with 2,800–3,700 rub/t for a pit at the bank under a 20–30 m bluff (1.6–2× cheaper) and 7,100–11,600 rub/t for coal hauled 2,000+ km, as from Dzhebariki-Khaya (4–6× cheaper). There is no gain under a bluff of 10 m or less.
BLIND REVIEW:
- MAJOR: The 1,800 rub/t needs 80 kt/yr of sales within 150 km of one bluff, and below about 23-35 kt/yr the rig loses to a pit at the same bank. (From the idea's own two points (20 kt gives 4,100 rub/t, 80 kt gives 1,800): fixed cost ≈ 61 M rub/yr and variable ≈ 1,030 rub/t, so it breaks even with a 2,800-3,700 rub/t pit at 23-35 kt/yr. The whole of Yakutia's 2024 northern supply delivery to utility and production enterprises was >312 kt of all fuels together, so 80 kt would be about 26% of it from one site.)
- MAJOR: 60 t/h as a season average is not supported by auger cycle times, because adding and pulling 13 auger flights and re-bolting the reaction frame every 2.1-2.4 m dominate each cycle. (80 kt in 100 days is 33 t/h around the clock, one 190 t hole every 5.7 h with no downtime. Cutting at 60-140 t/h, plus 26 flight moves at 6-9 min and 1-2 h to move and re-bolt, takes 5.0-9.1 h per hole: 21-38 t/h at 100% availability (USGS planning rate 175-250 t/shift ≈ 22-31 t/h). At 75% availability that is 38-68 kt/yr and 1,930-2,650 rub/t, only 1.06-1.9x cheaper than the pit.)
- MAJOR: 3 m of frame travel cannot follow the river over a 100-day navigation season, which includes the flood recession and rain floods, not just a 1-3 m low-water drop; and holes at the waterline flood whenever the river rises above their mouths. (Kolyma: high water from mid-May to September and a level range up to 14 m (Great Russian Encyclopedia); Lena ice-jam level of 13 m at Peledui in May 2026.)
- MAJOR: 62% is the geometric face recovery; field auger recovery is much lower once short, deviated or collapsed holes are counted, so each tonne needs more holes and more bluff. (Practical recovery is 30-50% against 78% theoretical (Ukrainian auger practice with BShK and AVSh rigs). That means 1.2-2.1x more holes per tonne and 1.1-1.9 km of bluff a year instead of 0.9.)
- MAJOR: The crew and barge work at the toe of a 20-30 m permafrost bluff on an outer bend, the kind that fails by thermo-erosional undercutting and block collapse, and the rig removes 62% of the seam at that toe. (No exclusion zone, bluff monitoring or crew protection is costed; summer thaw of the face and flooded hole mouths attack the toe throughout the 100-day campaign.)
- SURVIVES: 190 t per 80 m hole matches a 1.50-1.53 m auger at 1.30-1.35 t/m³; the 1.56-2.06x and 3.9-6.4x ratios reproduce; the 0.9 m webs carry ρgH/(1−0.62) = 1.0-1.55 MPa at 20-30 m of cover, well within short-term frozen-coal strength; 150-300 kN of thrust against about 360 kN of spud capacity is fairly called "marginal".

P6
NAME: Wintering Coal CHP Barge
MECHANISM: Anchor: the bunker barge that brings the winter's coal stays frozen in at the village and burns its own cargo as a combined heat and power plant. Repair: a thermal-oil coal boiler (80%) feeds an ORC (16% net), run heat-led into the village heat network. The 1.54 MW of reject heat replaces boiler-house coal burned at 65%, so the net extra fuel per kWh_e is about 0. Electric-only would cost 12.7 rub/kWh_e at 10k rub/t; the original 20-30x claim compared kWh of heat from coal with kWh of electricity from diesel. A 0.3 MWe unit needs 1,780 t of coal per winter, which fits one 2,000 t barge, and the 381 m³ of ash fits the hold space freed as coal is burned. Reject heat of 104 kW keeps an ice moat open around the hull and 44 kW keeps the hold unfrozen. Capex dominates the cost: 19-32 rub/kWh at 0.3 MWe (132-237 M rub) and 14 rub/kWh at 1 MWe for district centres.
VALUE: Winter electricity at 14-32 rub/kWh against 45-75 rub/kWh full diesel cost (1.9-4.3x cheaper, up to 6x where costs reach 88 rub/kWh), with the heat nearly free.
BLIND REVIEW:
- MAJOR: The baseline is wrong: the village diesel plant has to stay for summer, the shoulder months and standby, so the barge saves only diesel fuel, not the full 45-75 rub/kWh cost. (Avoided fuel = 0.28-0.46 kg/kWh × 66-120k rub/t ≈ 18-55 rub/kWh (isolated-settlement diesel at 43-66k rub/t and 231-460 g/kWh per EUROSOLAR Russia; Yakutia retail diesel about 88 rub/L). Against that, 19-32 rub/kWh is 0.6-2.9x cheaper, not 1.9-4.3x.)
- MAJOR: All of the saving comes from combined heat and power, which a shore-based ORC at the existing boiler house would get without the barge's penalties; a floating Arctic CHP feeding a town heat network also already exists. (The barge alone loses 104 + 44 = 148 kW, 9.6% of the 1.54 MW reject heat, and adds ice and flood risk and a heat main from the bank. Akademik Lomonosov at Pevek (70 MWe + 50 Gcal/h, in service since 2019-20).)
- MAJOR: Wintering at a village bank rather than a protected backwater exposes a barge wired to shore heat mains and cables to spring ice drift and ice-jam floods, and it must be cut loose while the village still needs heat. (Lena ice jam in May 2026: Peledui gauge at 13.05 m against a 12.0 m critical level; Kolyma level range up to 14 m (Great Russian Encyclopedia). Loaded draft plus 1.5-2 m of ice needs about 4-5 m of late-winter water depth at the berth.)
- MAJOR: The cheapest figure (14 rub/kWh at 1 MWe) does not fit the single-barge concept, and "up to 6x" pairs that 1 MWe cost with a small village's 88 rub/kWh diesel. (1 MWe burns 1,780/0.3 = 5,930 t per 194-day winter, which is three 2,000 t barges. At matched size the ratio is 88 ÷ 19-32 = 2.8-4.6x, before the avoided-cost correction.)
- MAJOR: The cost does not show round-the-clock certified staff for a thermal-oil coal boiler plus ORC (a hazardous production facility), and the village boiler house and its stokers stay on as heat standby. (My estimate of about 9 staff (2 per shift) at about 1.5 M rub/yr each is 13.5 M rub/yr, or +7.5-10 rub/kWh over 1.3-1.8 GWh/yr. Capex alone at 10-15% over 15 years already gives 10.5-29 rub/kWh.)
- SURVIVES: Energy balance (0.3/(0.8×0.16) = 2.34 MW of coal, 1.575 MW reject heat, 1.54/0.65 = 2.37 MW displaced); electric-only 12.7 rub/kWh (at about 22 MJ/kg); ash 381 m³ (15% ash, 0.7 t/m³) against 2,094 m³ of hold freed; moat 104 kW keeps about 0.5-0.7 m of open water at −40/−50 °C; ORC 16% is conservative (AHDB: about 17% of fuel).

P7
NAME: Wintering Miner-Barge Boilerhouses
MECHANISM: Anchor: the coal barge is itself the village boilerhouse; its hold is the winter coal bunker, it freezes into a backwater beside the heat network, and it leaves after the spring ice breaks up to refill. Repaired: unpowered 2,000 t barges (100×22 m, drawing 1.26 m instead of 3.5-3.9 m for 5,000-8,000 t hulls, which the shoaling Yana and Indigirka cannot float). Each carries a containerized automatic coal boiler (1.3 MW average, 3.2 MW peak, enough for about 300-700 people). One tug serves several barges, the hold is loaded directly by the floating bluff miner or a riverside mine, and the haul is at most 300-800 km. The barge is away from the village for 92 summer days; its own round trip takes only 12-22 days, which leaves about 75 days of paid freight work that covers the cost of a used hull.
VALUE: 3,000-5,000 rub/t at 300-800 km against about 8,080 rub/t for current river supply plus transshipment, trucking and stockpile losses, so 1.6-2.7× cheaper; at the original 1,500 km with new 8,000 t hulls it is 0.66-0.88× (more expensive), and it only fits sub-Arctic river villages that need no summer heating.
BLIND REVIEW:
- MAJOR: The 92-day summer absence is longer than the no-heating window at most villages on the named rivers, so a shore boiler and stockpile must stay, bringing back the transshipment, trucking and stockpile costs counted as savings. (Days with a daily mean above 8 °C, from monthly normals: Chokurdakh 51 (41 heating days uncovered), Srednekolymsk as a proxy for mid-river sub-Arctic villages 78-80 (12-14 uncovered); only Verkhoyansk-type upper-Yana sites (90 days) fit.)
- MAJOR: The 2,000 t hold does not reliably last the winter and cannot be topped up once the barge is frozen in. (1.3 MW over a 275-314-day season with the chain's own 18 MJ/kg coal at η 0.75-0.85 needs 2,019-2,612 t, plus 2-10% (26-132 kW) to keep the hold coal from freezing; Idea 3's 7 t/person makes 2,000 t enough for 286 people, not 300-700; the stated 2.46 peak-to-average ratio contradicts degree-days (1.62-1.73 at Verkhoyansk), and a real 3.2 MW peak means a 1.85-1.98 MW average = 2,460-3,490 t.)
- MAJOR: The 1.6-2.7× comes mostly from the shorter haul, which a conventional barge from the same source also gets, while the bunker barge carries one cargo a year. (The same concept at 1,500 km is 0.66-0.88×; in the same 92 days a conventional hull makes 4-7 coal round trips of 12-22 days (8,000-14,000 t vs 2,000 t), so hull and tug capital per tonne is 4-7× higher, offset only by an unsourced "75 days of paid freight".)
- MAJOR: The village's only heat source has to keep running, frozen in beside the bank, through spring break-up, when ice runs and the water rises by metres. (On the Yana at Batagay and Ust-Kuyga, ice runs have carried vessels onto the ice and behind islands (Mintrans, 2002); the Indigirka stood ~3.5 m above its 2009-2017 mean in 2017; Chokurdakh's June mean is 6.7 °C, so heat is still needed then.)
- MAJOR: Coal stored about 9 months beside a boiler either freezes (if wet) or, kept warm, can self-heat, and the design has no monitoring or inerting. (P&I guidance: coal at ≥55 °C may ignite spontaneously and CO ≥50 ppm signals self-heating; keeping the hold unfrozen takes 26-132 kW.)
- SURVIVES: 92 − (12 to 22) = 70-80 days ("about 75"); 8,080/5,000 to 8,080/3,000 = 1.62-2.69×; 2,000 t matches 1.3 MW only with 21 MJ/kg coal over Verkhoyansk's 275-day season (1,730-1,960 t); Verkhoyansk's 90-day warm window fits the 92-day absence to within ~2 days.

P8
NAME: Re-Floatable Pond-Moored Mine Plants
MECHANISM: Anchor kept: the concentrator, power house and camp float on hulls built in a shipyard, in a pond dug at the site, so the talik their heat creates does not matter. The pond is 6 m deep (2.2 m of maximum ice, 3 m of draft and a margin). Waste heat keeps a 2 m moat open around each hull against ice pressure, using 0.9-1.6 MW of the roughly 35 MW the power house rejects. Mills stand on bedrock 20-50 m back from the edge to allow for 0.5-2 m/yr of bank retreat. The hulls (130×14 m, 3 m draft, about 2.9 kt payload each) fit the 135×14.3 m White Sea-Baltic canal locks. Against the best current practice, a modular plant on piles, a cold-permafrost site gains nothing (capex +4%). The anchor pays off in one regime: warm, ice-rich ground where foundations are 20-25% of capex, cheap $3k/t barge hulls, and short-lived (5-7 year) riverside or coastal deposits. There the plant is re-floated and towed to the next deposit, keeping 45-55% of its value.
VALUE: In that regime capex is 15-19% below a modular plant on piles and delivered cost 10-14% lower. On ordinary cold permafrost the gain is about 0%.
BLIND REVIEW:
- MAJOR: The idea is not new, and relocating floating plants has turned out to be expensive. (Floating wet concentrators in ponds dug at the site are standard in mineral sands. Kenmare moved the 7,100 t WCP B 23 km to Pilivili on a US$106M budget, which then overran by about 17%. That is ~$15-17k per tonne of plant, against $3k/t for hull steel. Bucket-line gold dredges have floated their processing plants in their own ponds since the 1920s. The 45-55% retained value has no source.)
- MAJOR: The 3 m draft cannot reach the riverside deposits that the only paying regime relies on. (Guaranteed Lena depths are 2.2 m (Ust-Kut to Vitim), 2.6 m (Sinsk to Yakutsk) and 2.9 m (Yakutsk to Zhigansk), with ~1 m on the upper Lena in low water. At 2.2 m draft the payload drops from 2.9 to ~1.6 kt (lightship ~2.0 kt implied), so about twice as many hulls are needed.)
- MAJOR: The foundation saving is overstated: the mills, which carry the heaviest dynamic loads, still stand on bedrock foundations, and the 20-25% foundation share of capex is assumed. (From the claim, the hull/pond/moat penalty is 20-25% minus 15-19% = 5-6% of capex. If the foundations actually saved are 10-15% of capex, or 60% of 20-25% once the mills are excluded, the capex saving is 4-10% and the delivered-cost gain about 3-7%.)
- MAJOR: By its own numbers it fails the brief: 10-14% lower delivered cost in one niche and about 0% elsewhere is not several times cheaper. (The idea's own VALUE line.)
- SURVIVES: The moat heat is conservative: a bulk-flux estimate gives 0.2-1.0 MW per hull for 592 m² of moat (wind 2-10 m/s, -30 to -55 °C), against 0.9-1.6 MW claimed. A 130×14×3 m hull displaces 4.6-5.2 kt, consistent with 2.9 kt payload. The 135×14.3 m locks with 4 m depth are confirmed. A floating hull is indifferent to settlement of the pond floor. Cold permafrost giving ~0% gain is credible.

