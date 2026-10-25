# Task: kill test - find the one number that decides whether each idea lives

QUESTION: Russia wants to develop and extract minerals and energy in its permafrost regions at the lowest full cost, in the shortest time from investment decision to first production, and with the highest effectiveness. Effectiveness means resource recovery, working time across the year, and how long infrastructure lasts on thawing ground. All three are measured per unit of product delivered to the buyer. The scope covers:
- Hard-rock and placer metals: Norilsk and Taimyr nickel, copper and platinum-group metals; gold in Yakutia, Magadan and Chukotka; Udokan and Baimskaya copper; Tomtor rare earths.
- Diamonds in Yakutia, plus the Arkhangelsk deposits (see CORRECTED).
- Coal in Taimyr, Elga and the rest of Yakutia.
- Oil and gas in Yamal, Gydan and Taimyr.
The whole chain counts: choosing and exploring deposits, building and powering sites, mining or drilling, processing, staffing, and delivering the product. The conditions are:
- Permafrost that is thawing under a warming climate.
- Extreme cold, with short building and shipping seasons.
- Long distances with no roads or railways.
- Ice seasons on the Northern Sea Route (NSR) and the rivers.
- A shortage of workers.
- Expensive energy at remote sites.
- Restricted access to imported mining, drilling and LNG equipment and software since 2022.
What changes to any stage, or to the order in which deposits are developed, would beat the best current practice in Russia and in comparable cold regions (northern Canada, Alaska, Greenland, northern Scandinavia)?
A good answer: 
- Each proposal states its effect, with an estimate and its basis, on three measures: (a) full cost per unit delivered (annualised capital plus operating plus logistics); (b) years from investment decision to first production; (c) effectiveness (recovery, days worked per year, infrastructure life on thawing ground).
- Each proposal is compared with a named benchmark, either Russian (e.g. Yamal LNG, Norilsk, Vankor/Vostok Oil, Kupol/Pavlovskoye, Nord/Elga) or foreign (e.g. Canadian Arctic mines such as Raglan and Diavik, Red Dog in Alaska, Kiruna/Aitik, Greenland).
- It names which deposits or stages it applies to and which it does not.
- It states what physical law or measured data it relies on.
- It lists the equipment or technology by its domestic maker or unrestricted supplier.
- It includes the main risks and how to test the idea within 3–7 years.
Constraints: 
- It must obey known physics.
- It must be deployable within 3–7 years.
- It may use only equipment and technology Russian operators can get from domestic makers or from suppliers not restricted for them.
- It must not depend on ways around sanctions.

Below are 4 candidate ideas. You are a screening engineer with tools: WebSearch/WebFetch and Bash with python3.
Do not improve or redesign the ideas; judge them as written. Work only in `/home/user/SomeRepository/engine/runs/rusres/gate/c1/`: write files only there, do not
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

Facts already collected for this question (data; check a decisive one before relying on it, and search only for
what is missing):
(a slice: all 144 HARD facts and the 12 of 195 other facts that bear most on these candidates, sources omitted; the full ledger with sources is /home/user/SomeRepository/engine/runs/rusres/evidence.md - read it if you need a source or a fact that is not here)
FACT 1: Nornickel Norilsk Division proven+probable ore reserves at 1 Jan 2024 were 1,203 Mt (709 Mt proven, 494 Mt probable) at about 0.71% Ni, 1.31% Cu, 4.52 g/t 6PGM. The Talnakh ore field holds 676 Mt proven (about 0.67% Ni, 1.33% Cu, 4.25 g/t 6PGM) and 389 Mt probable (about 0.94% Ni, 1.64% Cu, 5.17 g/t 6PGM). The estimates were done by SRK in 2021. The search tool said the column headers were garbled, so the Ni and Cu grade reading is an interpretation. | HARD
FACT 2: Norilsk-1 disseminated ore: 32 Mt proven at about 0.25% Ni, 0.33% Cu, 4.56 g/t 6PGM (1 Jan 2024). Mining is in the northern part of the deposit. | HARD
FACT 7: Maslovskoye (Nornickel licence since the 2015 discovery) has B+C1+C2 reserves of 206.8 Mt. They contain about 33,087 koz Pd, 13,040 koz Pt, 711 kt Ni, 1,098 kt Cu, 26 kt Co and 1,268 koz Au. Grades are 5.0 g/t Pd, 2.0 g/t Pt, 0.3% Ni and 0.5% Cu, so it is a low-grade, PGM-rich ore. The State Commission on Mineral Reserves (GKZ) approved it on 12 Oct 2018 (Minutes 5561). | HARD
FACT 9: Nornickel drilled five 200 m thermometric boreholes in 2022 (Norilsk, Talnakh, Oganer, Kayerkan, Dudinka) to forecast permafrost change to 2050. Site permafrost thickness figures were not found. | HARD
FACT 10: Baimskaya (Peschanka) JORC resource: 9.9 Mt Cu at 0.39% and about 16.6 Moz Au at 0.21 g/t (M+I+Inf). The licence area is about 1,300 km². | HARD
FACT 11: An earlier KAZ Minerals figure (2018–2019) was 9.5 Mt Cu at 0.43% and 16.5 Moz Au at 0.23 g/t. The pre-feasibility study (PFS) assumed 250 kt Cu and 400 koz Au a year for 10 years, 60 Mtpa through two concentrators, and a mine life of about 25 years. | HARD
FACT 19: Polyus JORC reserves at 31 Dec 2024: 1,833 Mt at 1.8 g/t, containing 105.2 Moz. Sukhoi Log is 637 Mt at 2.1 g/t (43.5 Moz). Olimpiada is 30.7 Moz, Blagodatnoye 11.2 Moz, Natalka 9.6 Moz, Kuranakh 7.1 Moz and Verninskoye 3.1 Moz. | HARD
FACT 20: Polyus reserves in earlier years: Natalka about 16 Moz (2017) and about 14 Moz (2021), so reserves are falling with depletion. Kuranakh was 6.4 Moz and Kuranakh alluvials 0.54 Moz in the 2021 update. | HARD
FACT 26: Alrosa JORC at 1 July 2018 (Micon): resources 1,064 Mct, reserves 628 Mct, excluding the Mir underground mine, which has been suspended since Aug 2017. | HARD
FACT 32: Elga coking coal: about 2.2 Bt under JORC, in southern Yakutia 415 km from Neryungri. Mining began in 2011; output was 20 Mt in 2022; project life is about 100 years; planned capacity is 11.7 Mt (older figure). Another source gives 2.8 Bt reserves plus resources. Licence expiry was not found. | SOFT
FACT 33: Elgaugol: Mechel bought it in 2007, sold 49% to Gazprombank in 2016, and sold the remaining 51% to A-Property in April 2020. | HARD
FACT 40: Novatek resource base: 2,261 bcm gas and 189 Mt liquids (2021, D&M); 2,244 bcm and 197 Mt (2020). In 2019, SEC proved gas was 2,234 bcm and PRMS proved+probable was 3,901 bcm. | HARD
FACT 42: Available permafrost datasets: NSIDC "Land Resources of Russia" (1:20M–1:40M, coarse) and the 1:2.5M Geocryological Map of Russia (1991–96, 16 sheets). Yamal has a regionalisation into 52 geocryological regions. | HARD
FACT 43: Yamal LNG final investment decision (FID) was taken in December 2013. The project cost was about $26.9–27bn. That covers the South Tambey field, the LNG plant (three 5.5 mtpa trains plus a small fourth train) and the Sabetta port. | HARD
FACT 44: Yamal LNG train 1 loaded its first cargo in December 2017, about 4 years after FID. Train 2 started in July 2018 and train 3 in November 2018. Novatek said train 2 came six months early and train 3 more than a year ahead of the original schedule. Reaching 16.5 mtpa took about 5 years from FID. | HARD
FACT 48: Arctic LNG 2 FID was in 2019. It was planned as three 6.6 mtpa trains (19.8 mtpa) on concrete gravity-based structures. Planned start dates were 2023, 2024 and 2025–26. The planned cost was $21.3bn, and TotalEnergies targeted 20–30% lower cost per tonne than Yamal. | HARD
FACT 51: Arctic LNG 2 was added to the US SDN list in November 2023. Train 1 was paused for winter in 2024. By May 2025 it was idle with full tanks waiting for tankers, and train 2 lacked power capacity. Train 1 therefore ran well below design from 2023 to 2025 against a plan of full output at about 2.5 years after FID. | SOFT
FACT 54: Vankor: Vankorneft was set up in 2004 and commercial production began 21 Sept 2009, about 5 years later, in an area with no infrastructure. Output peaked at about 22 mt in 2016. The four-field group had fallen to about 14.8 mt by 2023. | HARD
FACT 57: Nornickel Sulphur Programme: announced in 2018 at $2.5bn with a 75% SO2 cut by 2023. The cost rose to $3.5bn in 2019 with the deadline moved to end-2025. It was later reported at up to $4.3bn, with the target date moved out two years because foreign contractors withdrew. Cost growth was 40–70% and the delay at least 2 years. | HARD
FACT 58: The first stage of the Sulphur Programme at the Nadezhda smelter (gas capture, acid plant, gypsum and sulphur output) started in October 2023 and cost about 180bn roubles (about $2bn). | HARD
FACT 59: Talnakh concentrator modernisation (done 2017) cost 47bn roubles and raised capacity 34%, from 7.6 to 10.2 mtpa. That is about 18 roubles per tonne of added annual capacity, derived by me as about 1.8bn roubles per extra mtpa. | HARD
FACT 61: Nornickel 2023: cash operating costs were $5.3bn, down 19% mainly from the weaker rouble. Capex fell 29% to about $3bn, partly because foreign suppliers' self-sanctions forced projects to be rescheduled. Revenue was $14.4bn and EBITDA margin 48%. No cost per tonne of Ni-eq was found. | HARD
FACT 62: Nornickel cash operating costs were $5.1bn in 2024, down 3% on 2023. 2022 was $6.54bn. | HARD
FACT 65: Polyus total cash cost (TCC) was $389/oz in 2023, down 25% on 2022, from the weaker rouble, higher grades and an antimony by-product credit. 2024 guidance was $450–500/oz. This is TCC, not AISC. | HARD
FACT 66: Natalka TCC was $490/oz in 2023, up 11%, from lower grades and the mineral extraction tax rate rising from 1.2% to 2.4%. In H2 2023 it was $452/oz, helped by better recovery from favourable ore mineralogy. A flotation circuit was planned for 2025. | HARD
FACT 67: Polyus group gold recovery was 81.8% in 2022 and 82.7% in 2021. | HARD
FACT 68: Polyus per-mine TCC in H1 2022: Natalka $382/oz, Olimpiada $433, Blagodatnoye $405, Verninskoye $404, Kuranakh $645/oz. | HARD
FACT 69: Natalka's Q3 2018 AISC was $1,143/oz, against Olimpiada at $395/oz. The gap shows the large share of capex and stripping in a ramping mine. | HARD
FACT 70: Kupol/Dvoinoye (Kinross segment): production cost of sales was $304.5m in 2020 and $314.1m in 2019. Metal sales were $904.6m in 2020. Dvoinoye ore processed was 326 kt in 2020 against 435 kt in 2019. Dividing by gold-equivalent ounces gives the cost per ounce, but the ounce count was not in the excerpts. | HARD
FACT 71: Udokan first stage (BMC/Udokan Copper): 15 mtpa ore and up to 150 kt/y Cu. Production of concentrate began 11 Sept 2023. A hydrometallurgical plant was due in Q2 2024. Cathode copper started 2 Sept 2026 after a fire delay. The 2018 plan was first production in 2021, and 2008 plans had construction starting in 2010 and design capacity in 2016. | HARD
FACT 73: Baimskaya (KAZ Minerals 2020): capex rose from $5.5bn to about $8bn. The causes were a revised tailings facility, about a one-year delay, and about $600m for a port and about 200 km of road. Target was 70 mtpa ore and first production by end-2027. Roughly $114 of capex per tonne of annual ore throughput, derived by me. | HARD
FACT 75: Elga output: 4.3 mt in 2019 and 5.83 mt in Jan–Nov 2020, against a 30 mt run-of-mine design (about 23 mt product) set in 2008. 26 mt were mined in 2023, up 30% from 20 mt in 2022. Reaching design output took about 12 years from the 2011 rail opening. Mechel sold 51% for 89bn roubles (about $1.17bn). | HARD
FACT 79: Alrosa's Mir mine flooded and stopped in 2017. Restoration was priced at 73bn roubles, with 6–8 years of construction, so a restart is unlikely before about 2030. Reserves are 68.6 Mct. | HARD
FACT 80: Alrosa produced 34.6 Mct in 2023. Sales were 322.6bn roubles and net profit 85.2bn roubles. Cost of sales in 2024 was 157.5bn roubles, down 11%. Dividing by 2024 carats would give cost per carat, but I did not find the 2024 carat count. | HARD
FACT 85: Norilsk CALM site (Grebenets, Tolmanov, Streletskiy, 2005–2020): mean thaw depth in loam was 96 cm, against about 80 cm in the 1980s. The deepening trend is about 1 cm/yr, and thaw depth varies by up to 200% between microlandscapes. | HARD
FACT 86: Western Yamal (Marre-Sale, Earth Cryosphere Institute): mean annual ground temperature rose 1.5–2.2 °C over 43 years (1980–2021), with the most on flat and polygonal tundra and the least in flooded lake basins. The depth of zero annual amplitude is 13–16 m. | HARD
FACT 87: Marre-Sale is described as the fastest-warming permafrost in the western Russian Arctic since the 1970s, at about 0.06 °C/yr at the zero-amplitude depth. | HARD
FACT 88: In the 43-year Marre-Sale record, active-layer thickness rose only slowly despite warming. Moss thickening and ground subsidence as ice-rich permafrost thaws offset the deepening. Drained terrain responded most, wet tundra showed decreasing thickness, and floodplains showed no change. Thaw depth is therefore a poor proxy for ice-rich ground degradation. | HARD
FACT 90: Nadym and Salekhard: the 2012 GIS-based study (Arctic, Antarctic, and Alpine Research 44(3)) is the source of the +40%/20% decline figures. Foundation capacity is computed from modelled ground temperature, active-layer depth and soil properties. | HARD
FACT 95: Ambarnaya tank collapse, 29 May 2020, about 20,000 t of diesel spilled. Norilsk Nickel blamed permafrost thaw. Rostekhnadzor found pile foundations too weak and poor maintenance. | HARD
FACT 96: Panarctic hazard (Hjort et al. 2018): 70% of current infrastructure in the permafrost domain (range 48–87%) lies in zones with high potential for near-surface thaw by 2050. 45% of Russian Arctic hydrocarbon fields lie in zones where thaw instability could cause serious damage. | HARD
FACT 97: Yamal tabular ground ice: layers of 10 m or more, at depths from near-surface to tens of metres. Exposures at the Neytinskiye lakes show about 20 m of ice at 5–26 m depth. Thickness and distribution diminish northward from Bovanenkovo to Kharasavey. Thermocirque and landslide features are tied to its degradation. | HARD
FACT 101: InSAR near Bovanenkovo (Sentinel-1): seasonal subsidence up to 180 mm/yr in subsidence zones, and 60–120 mm/yr at three sites in 2017–18. This is seasonal active-layer movement, not net settlement. Stacked interferograms carry about 1 cm error. | HARD
FACT 102: Central Yamal subsidence: in situ and Sentinel-1 agree at 3.9 and 4.3 mm per 100 thaw degree-days. | HARD
FACT 104: Central Yakutia: mean annual air temperature rose from –9.6 °C (1980) to –6.7 °C (2019), about 0.07 °C/yr, and is linked to thermokarst and alas expansion. Yakutsk air temperature rose about 3 °C in 1966–2023. | HARD
FACT 107: Four-borehole study (2023): permafrost warming of 0.02–0.16 K/yr against air warming of 0.09–0.11 K/yr, with a weak, inconsistent relationship. Warming rates cannot be transferred between boreholes. | HARD
FACT 109: Arctic warming 1979–2021 was 3.8 times the global rate (range 3.7–4.1). The Barents Sea near Novaya Zemlya warmed up to 7 times. | HARD
FACT 112: Sea ice, September minimum: NSIDC gives 4.60 million km² on 10 Sep 2025 (10th lowest). The 1979–2024 trend is –12.4% per decade, about –77,000 km²/yr. There is no significant trend in September minima for 2007–2025. | HARD
FACT 113: AARI-based studies show a statistically significant fall in July–September ice extent in the Kara, Laptev, East Siberian and Chukchi seas, with an abrupt drop after 2005. The NE Kara and E. Siberian seas lost more than 40% of ice area in 1980–2011. | HARD
FACT 114: NSR transit season length varies strongly year to year. The 15 seasons of 2008–2022 are too few for a trend, and the east and west sectors have different drivers. May Kara Sea extent predicts ice-free navigation 2–3 months ahead. | HARD
FACT 116: CMIP6 (16 models): September ice-free around 2076 under SSP2-4.5 and around 2055 under SSP5-8.5. Under SSP1-2.6 September extent stays above 2 million km². Open-water ships get an Aug–Oct window in 2045–55. PC6 ships' window shifts to Oct–Dec in 2021–30. No 2035 NSR-specific figure found. | HARD
FACT 117: Laptev fast ice reaches about 2 m in mid-winter (2.5 m in the coldest winters). Kara fast ice peaks April–May and fills the Ob and Yenisei estuaries until about July. The Vilkitsky Strait is a hazardous point. | HARD
FACT 119: River ice 2001–2024 (Ob, Yenisei, Lena, 6 rivers): freeze-up delayed by 9.0 days on average, breakup 7.8 days earlier, ice duration 14.1 days shorter. Over 65% of segments show this. | HARD
FACT 122: Tibbitt–Contwoyto winter road (Canada, the best-documented benchmark): 1981–2010 mean season 65 days (range 47–78). Projected 58 days in the 2020s and 49 in the 2050s. The shortest season on record was 49 days (1991). A 2021 lake-ice model puts the tipping point at about 2 °C of warming. | HARD
FACT 124: Chara basin (Udokan): seismicity under current norms is rated 9 points or more. The site sits between the Kodar and Udokan ridges. A basin 125 km long and up to 35 km wide has about 5,000 m of neotectonic amplitude. | HARD
FACT 127: Tailings and dams in permafrost: Colomac dam (NWT) seepage rose from 6 gpm (1996) to about 300 gpm (1999) over a talik in the valley bottom. The Mt Nansen thermosyphon plan assumes a 50-year life and fails if warming is unabated. A Nunavut frozen-core dam had a 7-year design life. | HARD
FACT 130: NSR cargo in 2025 was 37.02 Mt, down 0.87 Mt (−2.3%) on 2024. Gekon attributes the fall to bulk cargo, LNG and oil. Mintrans separately says the plan was exceeded by 5.5% at the same 37.02 Mt. | HARD
FACT 132: The 2018 presidential decree targeted 80 Mt on the NSR by 2024 and 200 Mt by 2030. Actual 2024 traffic was about 38 Mt. Analysts see no convincing growth points for 2026. | HARD
FACT 133: CHNL transit data for 2025: 103 transits by 88 vessels (52 east, 51 west), about 3.2 Mt of cargo, +6.2% in voyages and +3.2% in cargo. Season ran 30 Jun–17 Nov (about 4.5 months) in poor ice. Transit is therefore only about 9% of the 37 Mt total (my calculation); the rest is destination traffic. | HARD
FACT 134: Within 2025 transit, bulk-carrier voyages rose from 15 to 23 and container voyages from 11 to 15. Crude alone was 1.83 Mt (Kommersant, quoted by CHNL). | HARD
FACT 138: The Yamal LNG Arc7 fleet of 15 ships was complete by end-2019. Round trip to NW Europe is about 20 days, which gives 22–23 deliveries a month. Winter cargo is trans-shipped at Zeebrugge under a 20-year contract for up to 8 Mt/yr; Arc7 ships go east by NSR in summer. | HARD
FACT 139: Arctic LNG 2 has contracted 21 Arc7 tankers. The lead Zvezda-built ship, Alexey Kosygin, was handed over in late 2025. Russia had only two Arc7 LNG carriers at end-2025 (the second is Christophe de Margerie). Three Hanwha-built carriers became unavailable after US sanctions on Sovcomflot units. About 200 NOVATEK engineers were sent to Zvezda. | HARD
FACT 140: Alexey Kosygin (172,600 m³) discharged at the floating storage unit in Ura Bay near Murmansk. The Saam FSU in the Barents Sea can be reached by conventional carriers in winter. The Utrenneye plant in the Ob Gulf is reachable in winter only by Arc7 ships. | HARD
FACT 142: Nuclear icebreakers, project 22220: Arktika, Sibir (Dec 2021) and Ural (Nov 2022) are delivered. Chukotka's handover moved to 2027. Leningrad was 31.45% built in May 2026. Two more 60 MW icebreakers were contracted with Baltiysky Zavod for Dec 2028 and Dec 2030. | HARD
FACT 147: Pevek's Nagleynyn terminal for Baimsky: design throughput 1.842 Mt/yr, channel depth 12.3 m, ships up to 40,000 dwt. Funding is above RUB 27.6 bn for 2023–26, with 2026 as the planned start (2023 statements). | HARD
FACT 150: Chukotka has paved roads only in towns, and winter roads elsewhere. The Kolyma–Anadyr federal route via Omsukchan–Omolon is being tendered in sections. The existing "Arktika" winter road goes via Burustakh–Chersky. | HARD
FACT 154: Bilibino NPP: unit 1 stopped in 2018. Unit 2 was stopped in Dec 2025, and units 3 and 4 were scheduled to be shut down on 11 and 22 Dec 2025. The plant is the only heat source for Bilibino town. | HARD
FACT 158: Northern delivery carries about 3.2 Mt of cargo a year, mostly fuel. Rosatom Arktika became the single sea operator for 15 years and delivered 159.2 kt to Chukotka in 2025. Supply is by sea in summer and by winter roads from Magadan and Yakutsk in winter. | HARD
FACT 167: Red Dog (Alaska): concentrate moves 84 km by road to port and ships only July–October. In 2019 the season ran 122 days with 23 ships loaded. Storage holds 950,000 wmt between seasons. Two lightering barges serve ships anchored 3 nautical miles offshore. | HARD
FACT 168: Mary River (Baffinland): permit 4.2 Mt/yr, ore shipped in open water mid-July to mid-October only. The record was 4.1 Mt on 56 trips of 72,600 t average. Winter-shipping extension was opposed by local hunters, and the company was under creditor protection in mid-2026. | HARD
FACT 171: Arctic LNG 2 trains use licensed Linde MFC4 liquefaction (three cooling cycles, adapted for cold and the compact gravity-based structure). Novatek's own Arctic Cascade and Arctic Mix are not used there. The Linde licence was bought, but Linde has left Russia. | SOFT
FACT 172: Arctic Cascade runs only on Yamal LNG Train 4, at 0.9 Mt/y. Arctic Cascade is planned for Ob LNG and Arctic Mix for Murmansk LNG. Both are Novatek-patented. | HARD
FACT 173: Yamal LNG Train 4 was described as the first LNG line with mainly Russian equipment. Reported suppliers: Kazanskompressormash (gas compressor unit), Kriogenmash (cryogenic heat exchanger), Atomenergomash (vaporisers and pumps), Roscosmos-linked firms (expander). Low-temperature alloy piping had to be replaced; delay damage was estimated at RUB 0.9bn. | SOFT
FACT 176: Yamal LNG Trains 1–3 use APCI-C3MR with Nuovo Pignone (Baker Hughes) turbo-compressors, three drives per train. That is a Western spares dependence for the largest operating Russian LNG plant. | SOFT
FACT 179: Wison New Energies stopped all Russian work in June 2024 (Reuters via BOE Report). This removed a Chinese equipment channel because of secondary-sanction risk. | HARD
FACT 181: GTE-170 (Power Machines, built at LMZ): lead prototype assembled December 2022. Total investment exceeds RUB 15bn, of which RUB 4.8bn is state subsidy. The development programme started in 2018. By January 2026 the second GTE-170.1 was being prepared for shipment to Artyomovskaya TPP-2 (Far East), so serial output is at the level of units. | HARD
FACT 199: Nornickel Group average headcount was 78,738 in 2024 (2023: 78,374; 2022: 80,562). Average monthly salary was RUB 207 thousand, 2.1 times the national average. Salaries rose 69% over 2019–2024, with a 10% rise in 2024. Turnover was 11.4% in 2023, and in 2024 only "in line with industry" is stated. 94.3% are covered by the collective agreement. | HARD
FACT 202: Northern pay rules: Labour Code art. 317 sets the percentage northern allowance (from 10% rising to 80–100% of earnings by region and length of service). In Chukotka and the Severo-Evensky district of Magadan Oblast it is paid at the 100% maximum. Rotation (вахта) workers get the allowance on general rules (art. 302). Regions are listed in Government Decree No. 1946 of 16.11.2021. Young workers on the Far North can get the maximum allowance without a service record. | HARD
FACT 204: Magadan Oblast population fell by 1,339 in 2022 to 134,568 (1 January 2023): migration loss 805, natural loss 534. | HARD
FACT 205: Ground-cooling (thermosiphon) systems GET/VET: underground cooling pipes plus an aboveground heat exchanger, working without electricity. They work only in the cold season. A GET system has a condenser fin area of about 100 m², and is installed at the foundation stage (used at Chayanda). The market lacks a single approach to their use. No Fundamentstroyarkos price or capacity figure was found. | SOFT
FACT 206: US sanctioned Arctic LNG 2 (SDN list) in November 2023. Western parts and service channels were shut for the Arctic LNG 2 trains at that point, and Chinese suppliers' sanction risk followed (see FACTS 8–9). | HARD
FACT 209: Arctic LNG 2 cargoes sold to Chinese buyers at 30–40% discounts since Aug 2025. Cargoes went for $28–32m against a market value above $44m. The first cargo (28 Aug) sold $3–4/mmBtu below the Asian benchmark of about $11. The project cost is quoted at $21bn. | SOFT
FACT 211: A US State Department spokesperson warned that business with Arctic LNG 2 carries "significant sanctions risk", including for foreign banks processing related payments. China is the only known buyer. | HARD
FACT 212: Arctic LNG 2 owners are Novatek 60% and TotalEnergies, CNPC, CNOOC and Mitsui/JOGMEC consortium 10% each. Foreign banks and shareholders stopped funding from March 2022. About €9.5bn of project finance had been planned. | HARD
FACT 215: EU 20th package (adopted 23 Apr 2026): services to Russian-flagged icebreakers and LNG tankers banned from 25 Apr 2026. From 1 Jan 2027 the ban covers any LNG tanker or icebreaker operating in or for Russia, whatever the flag. EU operators must end LNG terminal services to Russian-controlled entities by 1 Jan 2027. | HARD
FACT 216: The 20th package also added 46 shadow-fleet vessels (total 632) and port-transaction bans on Murmansk, Tuapse and Karimun. The full maritime-services ban was left as a future legal basis because there was no unanimity. | HARD
FACT 217: The EU 19th package includes a Russian LNG import ban from 1 Jan 2027, brought forward from 1 Jan 2028, with a phased split between short-term and long-term contracts. | HARD
FACT 218: China's customs data show Russian LNG imports up 18.2% in 2025 to 9.79 Mt, worth $4.98bn, the same value as 2024. Russia is China's third-largest LNG supplier. S&P Global (Aug 2026) attributes the growth mainly to discounted Arctic LNG 2 cargoes. | HARD
FACT 219: OFAC sanctioned Rosneft and Lukoil plus dozens of subsidiaries on 22 Oct 2025 (EO 14024). Entities 50% or more owned are blocked, and non-US banks face secondary-sanctions exposure. This applies to the Vostok Oil owner. | HARD
FACT 220: The UK sanctioned Rosneft and Lukoil on 15 Oct 2025, including Nayara Energy (India, 49% Rosneft). | HARD
FACT 221: Vostok Oil: the Sechin 2019 pitch was 8.5 trn RUB of investment against 2.6 trn RUB of tax breaks over 30 years. Ministry of Energy cost estimate about 10 trn RUB. The Vankor Arctic MET deduction was about 125 bn RUB in 2021 and about 102 bn RUB in 2024. | SOFT
FACT 225: Baimskaya: KAZ Minerals bought 75% for $675m up front plus $225m deferred for the remaining 25% (2018). The project holds 9.5 Mt Cu and 16.5 Moz Au, with a plan of 250 kt/y Cu and 400 koz/y Au. | HARD
FACT 227: Udokan Copper (USM, Usmanov) began concentrate in 2023. A Dec 2023 fire damaged the cathode plant, planned for Q2 2024, and cathode output started Sept 2026, about 3 years late. Sanctions complicated replacement-equipment imports. Phase-1 investment was estimated at $2.9bn, including a Sber/Gazprombank/VEB syndicated loan under state-backed project finance. | HARD
FACT 229: Key rate: the Bank of Russia held 14.00% on 11 Sept 2026 after a cut on 24 Jul 2026. It was 16.5% in Oct 2025. The 23 Oct 2026 outcome is not confirmed. | HARD
FACT 230: Draft windfall tax (bill 618-9, from 1 Jan 2027) taxes the gain over the 2025 average world price once the 2026–28 price exceeds it by more than 10%. The rate is 20% for gold and 30% for most others. It is capped at 15% of revenue net of MET, and oil, gas, coal, diamonds and uranium are excluded. | HARD
FACT 232: The Accounts Chamber called the tax burden on gold miners insufficient and urged systemic rent taxation. An earlier Finance Ministry proposal was a 10% MET surcharge on gold above $1,900/oz. | HARD
FACT 233: Coal: export duties (4–7%, tied to the rouble rate) from autumn 2023 were cancelled for coking coal from 1 Dec 2024 and for thermal coal and anthracite from 1 Jan 2025. A 10% MET surcharge on coal applied from 2025 (Mintorg rail-tariff measures also in force). | HARD
FACT 235: Government coal support 2025: 12.8% RZD export discount (1 May–31 Dec 2025), tariff coefficients 0.4 and 0.895, budget compensation to RZD, and tax and premium deferrals. | HARD
FACT 236: China's customs data show Russian coal imports of 80.4 Mt in Jan–Nov 2025, down 8.6%. Russia's share was 18.6%, second place. China reimposed import duties in 2024: 6% on thermal coal, 3% on coking coal and anthracite. | HARD
FACT 237: Elga: Mechel sold 51% of the Elga Coal Complex to A-Property (Avdolyan) for 89 bn RUB in 2020, and Gazprombank kept 49%. Elga's coking-coal reserves are cited at 2.2 bn t, and a 321 km railway to the BAM was planned. | HARD
FACT 238: Alrosa 2025 IFRS: profit 36.2 bn RUB (19.2 bn in 2024) on revenue of 235.1 bn RUB. Output fell 10% to 29.8 Mct. | HARD
FACT 239: Alrosa H1 2026: net loss 9.5 bn RUB (profit 40.6 bn in H1 2025). Revenue including subsidies fell 33% to 91.7 bn RUB, inventory was 150.8 bn RUB, and 2026 output is guided to 25–26 Mct. Low-margin assets were suspended in 2025–26. | HARD
FACT 240: The G7/EU ban on direct imports of Russian diamonds took effect 1 Jan 2024, with a phased ban on stones processed in third countries from 1 Mar 2024. Alrosa's CEO called the market in deep crisis with prices falling for a second year (Nov 2024). | HARD
FACT 241: Nornickel 2025: revenue $13.76bn (+10%), EBITDA $5.67bn, net profit $2.47bn (+36%). LME nickel averaged 10% lower, and the company cites sanctions, high rates and a strong rouble as headwinds. | HARD
FACT 243: LBMA suspended six Russian gold and silver refiners in March 2022, and G7 states (UK, US, Canada, Japan) agreed in June 2022 to stop Russian gold imports. Palladium and platinum refineries stayed on the LPPM list. Russia holds about 40% of mined palladium. | HARD
FACT 244: Polyus 2025: gold 2.5–2.6 Moz, record capex $2.2bn, mostly Sukhoi Log. TCC guidance was $525–575/oz, and a higher MET on realized price raised cost. Target of 6 Moz/y by 2030. | HARD
FACT 245: Novatek 2025 IFRS: net profit 183.0 bn RUB (493.5 bn in 2024), normalized 206.5 bn RUB, revenue 1,445.6 bn RUB, normalized EBITDA 859.3 bn RUB. Non-cash one-offs of 301 bn RUB. | HARD
FACT 249: Arctic programme figures: about 20 bn RUB for 2026–28, personnel-cost reimbursement to 267 residents for 10.5k staff, and over 11k planned in 2026. Murmansk: 198 residents, 269.8 bn RUB portfolio, 60.6 bn actually invested (2025). Arkhangelsk: 297 residents, 272.4 bn RUB declared, 59.6 bn actually invested. | HARD
FACT 251: Permafrost rules: Government resolution No. 854 (25 Jun 2024) set state background monitoring of permafrost, which is environmental monitoring and not a foundation-monitoring mandate. | HARD
FACT 253: Law 57-FZ: a foreign investor with 25% or more of a licensee of a federal-significance subsoil plot controls it. More than 25% needs Government Commission approval, with no known precedent. A state-controlled foreign buyer is capped at 25%. | HARD
FACT 254: Subsoil Law changes: Federal Law 141-FZ (7 Jun 2025, in force 18 Jun 2025) amended Articles 10 and 43 on geological study. Law 554-FZ (29 Dec 2025, in force 9 Jan 2026) amended the Subsoil Law (content on maps and land only). | HARD
FACT 256: Norilsk TPP-3 spill, 29 May 2020. About 21,000 t of diesel escaped; the tank held 21,163 t. The EU eNatech database gives 17,500 t (21,000 m³). | HARD
FACT 257: Rostekhnadzor found "interrelated technical and organizational violations" at the construction and operation stages. It found no melting permafrost under the foundation. This contradicts Nornickel's first blaming of thaw. | HARD
FACT 258: The ERM report found several piles set in permafrost instead of bedrock as designed. It also found pitting corrosion and holes in the tank bottom. It faulted Nornickel for ignoring warning signs and for not building containment. | HARD
FACT 260: Nornickel's 2 June 2020 statement blamed "sudden subsidence of supports" that had stood 30+ years without problems. Prosecutors tied the soil and slab subsidence to permafrost thaw. The prosecutor general ordered an audit of similar permafrost facilities. | HARD
FACT 262: Rosprirodnadzor sued for 148 bn RUB. Nornickel put the damage at about 21.4 bn RUB, 7 times lower. In February 2021 the Krasnoyarsk arbitration court awarded 146.177 bn RUB. | HARD
FACT 264: The Norilsk concentrator collapse was on 20 Feb 2021, not 2020. A transfer point and walkway galleries fell during repair work; 3 died and at least 8 were hurt. Investigators say defects found in July 2018 went unrepaired for 2.5 years. Four staff were detained, including the concentrator's chief engineer. | HARD
FACT 270: The Hjort et al. 2022 review (Nature Rev. Earth Environ., ~170 papers) found damaged shares of building stock from under 10% to 80%. Russia had the highest share. 30–50% of critical circumpolar infrastructure is at high risk by 2050. Russian road upkeep losses from permafrost for 2020–2050 are about US$7 bn (422 bn RUB) on the existing network. | HARD
FACT 271: The Hjort 2018 Nature Communications paper (vol. 9, 5147) maps infrastructure hazard under projected warming to 2050. Proven mitigations are convection embankments, thermosyphons and pile foundations. | HARD
FACT 272: Mir mine flooding, 4 Aug 2017. 151 people were underground; 143 were rescued; 8–9 died. Search ended 26 Aug with 37.4 thousand m³ of water in the pit. | HARD
FACT 273: Rostekhnadzor head Aleshin (Nov 2017) blamed design error. The early-2000s "dry conservation" project of the pit ignored rock fracturing and the need for long-term pumping. The site has high water inflow and rock salt. | HARD
FACT 275: Vorkuta Severnaya, 25 and 28 Feb 2016. Three explosions at 780 m depth killed 36 (miners and rescuers). 26 bodies were never recovered. The mine was flooded and sealed. Vedomosti put the loss at $71.5 m. | HARD
FACT 277: Baimskaya (KAZ Minerals, Nov 2020). Capex rose to about $8 bn nominal. Drivers were external infrastructure, a revised tailings facility and a one-year delay. The company took on a ~200 km road and part of a port (~$600 m). First production was moved to end-2027 and the BFS to H1 2021. | HARD
FACT 278: Udokan phase 1 was ~$2.9 bn for 15 Mt/y ore and 150 kt/y copper. Concentrate began Sept 2023 after the 2008 tender. | HARD
FACT 282: Tomtor. Putin (Nov 2024) criticised owners who took the deposits "many years ago" and are "not investing". Rosneft took over the operator in May 2025, with pilot mining expected in 2027. The Buranny site holds 11.4 Mt of ore. | HARD
FACT 283: Arctic LNG 2 was planned for T1 2023, T2 2024 and T3 2026, 19.8 Mt/y in total. T1 was finished in Dec 2023 but sold nothing for lack of ice-class tankers and sanctions. It was halted from 11 Oct 2024, restarted around March 2025, and stopped again in May 2025. T2 started May 2025 but lacked power modules. | HARD
FACT 287: Natalka. First dore Dec 2017 at 50% of design throughput (14–15 kt/d). Group recovery fell to 83.4% in 2017, partly due to ramp-up there. 2019 reached full capacity. 2022 output was 444.7 koz against 503.3 koz in 2021. A flotation circuit was planned for 2025. | HARD
FACT 289: Snap Lake. Care and maintenance from 4 Dec 2015, then flooding of the underground works. The final closure plan was filed in 2019 at about $85 m. Security held was about $31–39 m. | HARD
FACT 290: Giant Mine (NWT). The cleanup estimate rose from about $1 bn (2010) to $4.38 bn, with work to 2038. 237,000 t of arsenic trioxide dust is to be kept frozen in chambers. | HARD
FACT 292: Red Dog. Teck never met the 1998 TDS limit, because lime treatment adds dissolved solids. A 2004 suit settled with a roughly $120 m, 54-mile ocean pipeline plan. Waste-rock drainage reaches 90,000 mg/L TDS and is a major closure cost. | HARD
FACT 293: Mary River. The NIRB rejected Phase 2 in May 2022 and ministers upheld that on 16 Nov 2022. Phase 2 would have doubled output to 12 Mt/y, with a second railway to Steensby; the licence stays at 6 Mt/y. | HARD
FACT 296: Isua. London Mining went bankrupt in 2014 after the iron-ore price fell. General Nice's licence was revoked in Nov 2021 for inactivity and missed guarantee payments. | HARD
FACT 299: Snøhvit Future compression upgrade. The 2022 plan (PDO) estimate was NOK 13.2 bn; it is now above NOK 20 bn, and the upgrade was delayed (Dec 2025). | HARD
FACT 300: Yamal LNG (3 trains × 5.5 Mtpa, finished end-2018) was built from 142 modules and 365 pipe racks, over 480,000 t, fabricated at Asian yards from Nov 2014 to Aug 2017. A Yamal LNG director said modules cut the construction period by 1.5 years against conventional methods. | HARD
FACT 302: A 640,000 t GBS was towed about 2,000 km from Belokamenka to Utrenneye in about 21 days in July–Aug 2023. A second followed in July–Aug 2024. Each is designed for up to 6.6 Mtpa. | HARD
FACT 305: Arctic LNG 2 Train 1 started in late Dec 2023. Novatek and its foreign shareholders declared force majeure after US sanctions. The terminal at Utrenneye is about 70 km from Sabetta. | HARD
FACT 308: Yamal's Arc7 carriers were designed for NSR to Asia in summer only, and for westbound (Europe) voyages in winter. A later design allows year-round operation. The NSR is usable for these ships mainly from July to late November. The Asian leg takes 19–21 days against 35 days via Suez. | SOFT
FACT 309: Rosatom's land-based RITM-200N SMR at Ust-Kuyga, Yakutia, is 55 MW, with a 60-year life and 5-year refuelling. The construction licence was issued in April 2023 and commissioning is targeted for 2028. Camps for 250 and 683 people and a 12 km road were built by 2024. A two-reactor variant is under discussion. No capex has been published. Rosatom claims it will halve regional electricity cost. | HARD
FACT 312: Raglan (Glencore, Nunavik) runs two 3 MW Enercon E-82 turbines and about 3 MW of storage. These save about 4 million L of diesel a year. A 2021 federal grant of C$7.1M supports 2 more turbines (about 6.6 million L a year saved) and 4 MW more storage. Total site diesel use is about 50 million L a year. | HARD
FACT 315: Diavik's 4-turbine wind farm (9.2 MW, 2012) supplies about 17 GWh a year, displacing about 4–5 million L of diesel (about 10% of fuel). A 3.5 MW solar plant (built Feb–Jul 2024) saves about 1 million L a year and supplies up to 25% of power during closure work to 2029. Diavik was expected to end operations in early 2026. | HARD
FACT 316: Red Dog (Alaska) ships concentrate in a fixed window. The 2024 season ran 12 Jul–26 Oct (1.4 Mt wet, 22 ships, from barges). The 2025 season ran 11 Jul–21 Oct (1.2 Mt wet, 22 ships). | HARD
FACT 317: Teck guided Red Dog zinc down to 375–415 kt in 2026 and 330–370 kt in 2027, because slippage on a fault in the Aqqaluk pit forced mining of lower-grade areas. | HARD
FACT 318: Mary River (Baffinland) shipped about 6 Mt in 2024 on 70 ore carriers, within the approved 6 Mtpa cap. The season is limited by ice and a narwhal management plan. In 2022 the company did not break ice to start the season, which delayed and shortened it by 1–2 weeks. The 10% workforce cut in Oct 2024 followed weak iron ore prices. The Steensby rail (year-round shipping) construction was still unfunded. | HARD
FACT 319: Willow (ConocoPhillips, North Slope): capex was raised to $8.5–9 bn (from $7–7.5 bn), with first oil in early 2029. It was about 50% complete at the Nov 2025 update. Peak output is about 180 kb/d and reserves about 600 Mbbl, and inflation added about $700M. | HARD
FACT 320: Trans-Alaska pipeline: more than 124,000 ammonia heat pipes were installed in the mid-1970s on the vertical support members (VSMs). Non-condensable gas degraded some pipes. CO2 recharge worked as a repair. At Lost Creek, 8 thermal VSMs were replaced and 60 freestanding thermosyphons added. | HARD
FACT 321: A 2024 study of 14 embankments on the Qinghai–Tibet network (2003–2020) found thermosyphon cooling weakening under warming, with taliks re-forming where they had been removed. The cause is a falling air-temperature freezing index. | HARD
FACT 323: Alaska North Slope tundra travel season fell from about 200 days (1970s) to about 130 days recently. The ice-road season ranged 123–209 days in the first decade after 2003 and 161–200 days afterwards. The state moved to an operating standard of −5 °C or colder in the top 30 cm of soil (23 °F), with snow-packing and ice stockpiling. | HARD
FACT 324: Russia's state background permafrost monitoring regulation was approved by Government Decree No. 854 of 25.06.2024, built on the Roshydromet network, with open data. | HARD
FACT 327: Sentinel-1 InSAR on Yamal (2017–18) measured seasonal surface change of 60–120 mm/yr, up to 180 mm/yr in active-layer zones. Subsidence was 3.9–4.3 mm per 100 thaw degree-days, matching in-situ data. Snow cover creates an early-thaw gap in the record. These are ground-surface values, not structural settlement. | HARD
FACT 328: Aitik (Boliden) trolley-assist: a 2018 pilot of 700 m with four Cat 795F trucks. The expansion cost SEK 300M ($31.2M), adding 3 km of line and 10 trucks. Boliden estimated diesel cut by 5,500 m³ a year and life-of-mine transport GHG down by nearly 15%. | HARD
FACT 329: Kiruna (LKAB) main level 1365 m cost SEK 12.4 bn and took about 4.5 years to build per E&MJ. It is run with driverless electric trains, and ore output was to rise from about 27 to 35 Mtpa. Granitor gives a 10-year build period for the level, and LKAB's own 2018 announcement says it was completed around 2017, so the build time is disputed. | SOFT
FACT 330: Agnico Eagle Meliadine 2024: 378,886 oz gold (+4%), 1,966 kt milled at 6.22 g/t. Meadowbank complex 2024 payable production was 504,719 oz. Company all-in sustaining cost (AISC) was $1,239/oz. No mill recovery figure was found. | HARD
FACT 332: Dry-stacked or filtered tailings in the cold: freeze-thaw cycles alter density and permeability, and thaw rapidly reduces bearing capacity. Winter-frozen layers can leave man-made permafrost lenses that settle on thaw. Coupled freeze-thaw models are immature and long-term Arctic monitoring data is scarce. Keno Hill's dry stack reported the permafrost surface remained frozen. | SOFT
FACT 333: The Eagle Gold (Yukon) heap leach failed in June 2024. The independent review board found a steep section with a history of poor drainage failed, with owner and contractor "actions and inactions" contributing. Millions of tonnes of cyanide-laced ore were released. The sources do not mention permafrost as a cause. | HARD
FACT 334: Microreactor costs have no built-unit data. Westinghouse expects about $0.25/kWh for the first units. DOE/INL puts the Alaska remote-application average at $0.54/kWh. An MIT-led study found diesel+wind, microreactor and other options all at about $0.42–0.45/kWh. The Bruce Power/Westinghouse study found up to 44% savings versus diesel. A Canadian roadmap found 24 mines needing about 600 MWe, mostly 5–20 MWe. | SOFT
FACT 335: Snøhvit Future (Hammerfest LNG electrification): cost estimate rose from NOK 13.2 bn (2022) to NOK 26.5 bn (2026 value), blamed on plant operations, weather and tunnel rock. Compression is planned for 2029 and electrification for 2030, with the project 60% complete. | HARD

Notes from the user and about the environment (data; the user may be wrong):
The asker wants a professional, deeply sourced answer: hundreds of sources, numbers with units and years. Use official
Russian statistics and registers (Rosstat, Rosnedra, the Ministry of Natural Resources and its state reports on
mineral resources), company annual reports and presentations (Nornickel, Alrosa, Polyus, Rosneft, Novatek,
Gazprom Neft, Udokan Copper, Kaz Minerals for Baimskaya, Elga Coal), Russian-language technical literature (for
example the Melnikov Permafrost Institute of SB RAS and mining journals) as well as international sources. Proposals
must not depend on circumventing sanctions.
Assumptions in the question that may be wrong:

- The three measures can be traded off against each other, and one ordering of deposits is best.
- Thaw is the main cause of infrastructure failure, though engineering faults may be as important.
- All listed resources are in continuous permafrost, though some sit in discontinuous or no permafrost.
- The NSR is the main way to move product, but rail, river, or processing near the site may beat it.
- More output is the goal, though some listed projects may not be worth building at all.
Where deciding data may exist:

- Rosatom/NSR administration traffic statistics and ice-class fleet lists.
- Russian Ministry of Natural Resources (Rosnedra) reserves balance, the GKZ.
- Company reports from Nornickel, Polyus, Kinross-era Kupol, Novatek, Rosneft, Alrosa and Mechel/Elga.
- Permafrost temperature records: GTN-P and the Roshydromet/Earth Cryosphere Institute (Moscow) monitoring networks.
- Rostekhnadzor accident reports.
- Published capex and opex of the foreign benchmark mines (technical reports under Canadian NI 43-101 rules).
- Global Energy Monitor or IEA-style cost data for LNG.

Ledger: where the cost or the defect comes from (data):
KIND: cost

I ran no new searches. Every number below comes from the supplied facts (cited as F#), or is my own estimate, marked "est." Unit costs and shares are estimates built from F# data, not company-published splits.

ARCHETYPE A: Gydan/Yamal pipeline-gas to LNG, modular plant on a gravity base, Arc7 shipping (Yamal LNG T1–3, F43–F44, F300) | cost ≈ $7–8/mmBtu delivered (est.). Capital is about $27bn over 16.5 Mtpa, or $1.6bn per Mtpa (F45). Annualised at 10% over 20 years, that is about $190/t, or $3.7/mmBtu. | Arctic LNG 2 cargoes sold at $3–4/mmBtu below the Asian benchmark of about $11 (F209).
SHARES: capital 47 | outbound logistics (Arc7, transshipment) 22 | processing (liquefaction, field, drilling) 10 | energy (fuel gas, own power) 6 | labour 3 | inbound logistics 2 | other (MET, fees, margin) 10
LARGEST: capital - a 10x cut of it removes 42% of the cost. Outbound logistics is the second largest. Train 4's unit capex of $450–500 per t/y against $1,100 on T1–3 (F174) shows capital is where the range is.

ARCHETYPE B: Norilsk underground Ni-Cu-PGM mining, Talnakh concentrator, Kola/Norilsk smelting, Dudinka–Murmansk shipping (F59, F61–F62, F199, F241) | cost ≈ $8bn/yr full cost (est.). That is cash opex of $5.1bn in 2024 plus about $3bn capex (F61–F62), or about 59% of 2025 revenue of $13.76bn. Cost per tonne of Ni-eq was not found. | prices: Ni in structural surplus (F242); Cu about $12k/t (F246).
SHARES: capital 37 | labour 27 | processing, spares, consumables 11 | energy 6 | outbound logistics 5 | inbound logistics 3 | other (MET, export duty, windfall tax) 11
LARGEST: capital - a 10x cut removes 33%. Labour is next. Pay is RUB 207k/month for about 78.7k staff (F199), about RUB 195bn/yr or $2.1bn (est.). Spares and equipment are a separate risk: about half of suppliers were lost (F63).

ARCHETYPE C: Open-pit gold on permafrost, CIL/flotation, road/winter-road supply (Polyus Natalka, Magadan; F65–F69) | cost ≈ $490/oz total cash cost (TCC) in 2023 (F66). Mature AISC is probably about $700/oz (est.). | gold price far above cost; Polyus 2025 TCC guidance $525–575/oz (F244).
SHARES (of TCC, est.): processing, reagents, mining consumables 30 | labour 25 | energy 12 | inbound logistics (fuel, reagents, winter road) 12 | outbound logistics 1 | capital 0 (excluded from TCC) | other (MET at 2.4%, G&A) 20
LARGEST: processing - a 10x cut removes 27%. Recovery is a lever on the same line: group recovery was 81.8% (F67), and Natalka's flotation is planned for 2025 (F66). Ramp-up capex is what blows up full cost: Natalka AISC was $1,143/oz against Olimpiada's $395/oz (F69).

ARCHETYPE D: Greenfield copper-gold with no infrastructure (Baimskaya; benchmark KAZ Minerals feasibility study) (F73, F149, F151, F277) | cost ≈ $6,500/t Cu, pre-gold credit (est.). Capex is about $8bn for about 300 kt/y Cu, so annualised capital is about $2,900/t Cu at 10% over 25 years. Opex is my assumption. | LME 2026 average forecast about $11,975/t (F246).
SHARES (est.): capital 44 | outbound logistics (800 km road, Pevek port, NSR window of 3–4 months) 10 | energy (nuclear floating units) 10 | processing 14 | labour 8 | inbound logistics 4 | other 10
LARGEST: capital - a 10x cut removes 40%. Of that, $600m is for road and port (F73), and power was priced at RUB 190bn (about $2bn) in 2021 and has risen since (F151). First production slipped from 2021 to 2027 or later (F12, F73).

SCHEDULE AND EFFECTIVENESS SIGNALS THE COST SHARES HIDE
- **Yamal LNG:** about 4 years from the 2013 FID to first LNG (F44).
- **Udokan:** concentrate about 4.5 years after the 2019 construction start (F72); cathode copper came 3 years late (F227).
- **Elga:** about 12 years to design output after the rail opened (F75).
- **Foundations on thawing ground:** pile bearing capacity has fallen 20–40% in Salekhard and Nadym since the 1970s, and a loss above 55% is projected for Norilsk by the 2040s (F89, soft). Design norms do not yet fully include warming (F92).
- **Cold and ice:**
  - Cold raises equipment failure rates up to 6–7 times (F111).
  - The Red Dog shipping window is 122 days (F167).
  - The NSR is usable for Arc7 ships mainly from July to late November (F308).
- **Utrenneye:** the plant is reachable in winter only by Arc7 ships (F140).

STATES: the cost shares hold in these conditions, worst first: Jan–Feb at −40 to −50 °C, when equipment failures peak (F111) | the ice-bound shipping season outside the Jul–Nov window (F118, F308) | thaw season, with active-layer movement of 60–180 mm/yr (F101) | the sanctions-limited spares and equipment channel, 2022 onward (F63, F187) | ramp-up years, when capex and stripping load the unit cost (F69, F287).

SOURCES:
https://ar2023.nornickel.ru/en/business-overview.1.html
https://www.nsenergybusiness.com/projects/yamal-lng-project
https://www.lngindustry.com/liquefaction/22112018/yamal-lng-commences-third-lng-train-production/
https://www.technipfmc.com/media/p51juylp/yamal_lng_case_study.pdf
https://abnews.ru/2018/11/22/tretya-liniya-yamal-spg
https://www.rcinet.ca/eye-on-the-arctic/2025/11/19/russias-novatek-gives-deep-discounts-to-sell-sanctioned-arctic-lng-to-chinese-buyers-sources-say/
https://www.mining.com/web/nornickels-2023-profit-slumps-51/
https://nornik-upload.storage.yandexcloud.net/iblock/100/k049676q8k1b5prvttswpaz2hqkd7mx1/IFRS_review_2024_eng_full.pdf
https://www.kitco.com/news/off-the-wire/2026-02-11/nornickel-reports-36-rise-net-profit
https://sr2024.nornickel.ru/en/about-norilsk-nickel/key-figures.html
https://financialfilings.com/filings/polus/earnings-release/2021/1393877/
https://www.lse.co.uk/rns/PLZL/operating-results-for-2h-2022-and-full-year-2022-u17bfwzlh9j2zyk.html
https://www.lse.co.uk/rns/60GT/3rd-quarter-results-9i5cbv9d1v46o4w.html
https://www.miningweekly.com/article/russia-infrastructure-plans-raise-risk-for-baimskaya-copper-project-kaz-2020-11-18
https://www.kommersant.ru/doc/6594989
https://www.eastrussia.ru/news/stroitelstvo-vl-dlya-baimskogo-goka-zavershaetsya-na-chukotke-/
https://www.thebarentsobserver.com/arctic/permafrost-thaw-will-have-devastating-impact-on-buildings/105619

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

THE 4 IDEAS:
IDEA 1
NAME: Plant-chilled foundations
MECHANISM: Run a glycol loop through the pile caps of an LNG plant, cooled by its own refrigeration and kept running in summer. Thermosyphons from Fundamentstroyarkos would still cover the winter. A summer heat flux of about 5 W/m² over 1 km² is about 5 MW of heat, or about 2.5 MW of electricity at a COP of 2. That is under 1% of the plant's drive power. The closest earlier attempts are TAPS and the Qinghai–Tibet thermosyphons, which fade as winters warm. An active loop does not depend on how cold the winter is. The deciding quantity is the summer heat flux, measured in boreholes.
VALUE: Holds pile capacity at the design γt for the life of the plant, whatever the warming.

IDEA 2
NAME: Murmansk winter shuttle loop
MECHANISM: In winter, Arc7 ships run only Sabetta/Utrenneye–Murmansk and back, unloading into existing floating storage there. Conventional tankers then carry the LNG onward. The closest earlier attempt is the Zeebrugge transshipment, whose roughly 5,000 km leg wastes scarce Arc7 tonnage and which the EU ban from 2027 closes. The deciding quantity is Arc7 round-trip days in the January–April ice. Risk: storage capacity at Murmansk. The test, over 3 years, is to log turnaround times for the existing ships.
VALUE: The cargo each Arc7 ship delivers per year rises about 1.5–2x (est.), which removes the shipping bottleneck that left Arctic LNG 2 Train 1 unsold. Outbound logistics, the second-largest cost share, falls roughly 25–35%.

IDEA 3
NAME: Rock-socketed piles with slip sleeves
MECHANISM: Carry new and rebuilt plant loads on bored steel piles set into rock below the frozen ground, and coat the shaft inside the frozen layer with a bitumen slip layer, so thaw adds only small drag load instead of removing the pile's support. Use TMK pipe and Chinese piling rigs. The closest earlier attempts are pile design to SP 25.13330, which has lost 20–55% of capacity (F89), and the Ambarnaya piles set in ice-rich ground (F325). Ground cooling is not involved, so a warming climate does not erode the support. The design applies at Norilsk, Udokan and Baimskaya, but not on deep Yamal sediments. The deciding quantity is depth to competent rock, which must be 30 m or less; test it with load-cell piles monitored for 3–5 thaw seasons.
VALUE: Structure life of 50+ years, for about 1–3% more capex.

IDEA 4
NAME: Numbers-up Arctic Cascade trains
MECHANISM: Train 4's 0.9 Mtpa Arctic Cascade design, which is domestic and already running, is copied in series at Utrenneye and Sabetta. Each copy shares the existing gravity base, port, gas gathering and Arc7 berths, instead of scaling to 6.6 Mtpa trains on imported turbines. The closest earlier attempt is Arctic LNG 2, which stalled because only 4 of its 20 Baker Hughes turbines were delivered and the GTE-170 exists only at unit scale. Small trains avoid both by using domestic drives. The deciding quantity is whether series-built trains hold unit capex below $600/t/y once the alloy piping is replaced. Risks are low-temperature metallurgy and efficiency losses at small scale. The test, over 3–5 years, is to build 3 trains, then measure their capex and how many days a year they run.
VALUE: Annualised capital falls about 60% and delivered cost falls about 20–30%, against the Yamal LNG Trains 1–3 benchmark. First LNG comes about 2–3 years after the decision, against 4 for Yamal LNG, with no imported drives.

