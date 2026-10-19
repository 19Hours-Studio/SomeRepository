# Inventory of models and data harvested for engine/kit

Scope read: `engine/runs/permafrost/` → `round2/{audit_a,audit_b,critic_a,critic_b,erp2_a,erp2_b,rt_a,rt_b}`,
`repair/{a,b}`, `roast/`, `genius/gate_1..9, gate_r1_1, gate_r1_2`, `genius/{audit_final,audit_evo_1,audit_evo_2}`,
`genius/{repair_final,repair_evo_a,repair_evo_b,ledger}` (scripts, REVIEW.md, LOG/NOTES, printed outputs; TASK.md
prompts were not used). "Recurs" = number of run folders in which the model/value was recomputed (approximate).
Defects quote the review verdicts (FATAL/MAJOR) that the model exposed. "Kit" = where it now lives.

## 1. Physical and economic models

| # | Model | Harvested in (examples) | Recurs | Defects it exposed | Kit |
|---|---|---|---|---|---|
| 1 | Latent heat / thaw energy of frozen ground E = θρL + CΔT | audit_b c1/c2, critic_b I2, erp2_b I2, repair/b I2, gate_2, gate_8, audit_evo_2, repair_evo_a | 12 | FATAL loose pile ≠ ice-cemented (101 vs 50-55 MJ/m³); MAJOR 7 °C ratio wrong | `thermal.thaw_energy_per_m3`, `latent_heat_per_m3` |
| 2 | Water heat budget: feed = QcΔT/E, water ratio E/(cΔT) | audit_b, critic_b, erp2_b, rt_b, repair/b, gate_8, audit_evo_2 | 8 | MAJOR feed tracks creek temperature (6x swing); 8 °C water unavailable; ratio below sluice need | `thermal.water_ratio`, `thaw_feed_rate`, `water_heat_power` |
| 3 | Stefan thaw/freeze depth (+surface resistance, degree-days) | audit_b c1/c5, critic_b I2/I3, erp2_b, repair/a, repair/b, audit_final, audit_evo_1/2, gate_4, gate_7, gate_r1_1, repair_final, repair_evo_b | 15 | FATAL floe freezes onto bed (31-73 cm vs 141 kg/m² lift); MAJOR thaw behind open rock 1.7-4.6 m; heated building 10.7 m | `thermal.stefan_*`, `ice.freeze_on_below_ice` |
| 4 | Neumann two-phase / 1-D enthalpy talik under a reservoir | audit_evo_1, repair_evo_a | 2 | MAJOR no talik margin: each 1 °C bottom water = 2.3-2.9 m | `thermal.neumann_depth` |
| 5 | Steady talik under a circular lake (Lachenbruch 1957) | audit_final (axis + 2-D), repair_final | 3 | MAJOR talik reaches the dig column only under 25-30% of the lake | `thermal.talik_depth_lake_axis` |
| 6 | Convection to a frozen face: Dittus-Boelter, Gnielinski ×3 roughness, Stanton, jet stagnation, flat plate, Ashton ice-water | audit_b c2, erp2_b, rt_b, repair/b, critic_b, roast, repair_evo_a, audit_evo_2 | 8 | MAJOR e-folding length 63-400 m (heat passes the face); required h at top of measured range; debris coat caps flux; +0.01 K melts shells | `thermal.h_*`, `face_retreat_rate`, `efold_length`, `ntu_required`, `debris_coat_limited_flux`, `ice_melt_rate` |
| 7 | Open-water / pond / moat heat loss (bulk sensible+latent+LW) | gate_r1_1, audit_final, repair_final, audit_evo_1, audit_evo_2, repair_evo_a/b | 7 | MAJOR calm-air pond loss used; 1 MW waste heat too small in wind; outage freezes moat 0.22-0.25 m/day | `thermal.open_water_heat_loss`, `open_water_freezing_rate` |
| 8 | Summer pond energy balance (Brutsaert LW, bulk fluxes) | audit_b c2, audit_evo_2, gate_8, gate_9 | 4 | MAJOR pond needs more than all sunshine (239-358 vs 228 W/m²) | `thermal.water_surface_net_flux`, `climate.toa_daily_mean_irradiance` |
| 9 | Freezing time of backfill (cylindrical enthalpy; two-sided slab) | audit_evo_2, repair_final (slot refreeze) | 2 | FATAL backfill "within weeks" impossible: 93-304 d per hole, 1.3-15 yr per panel | `thermal.freeze_time_cylinder`, `freeze_time_slab_two_sided` |
| 10 | Planck 8-13 µm band / sky-window radiative cooling | audit_a, critic_a, erp2_a, repair/a, gate_7 | 5 | FATAL night-sky eutectic freezing: 30 W/m² at −50 °C, 273 h/yr | `thermal.planck_band_exitance` |
| 11 | Scheil/Rayleigh freeze concentration | audit_a ×2, critic_a, gate_4 | 4 | MAJOR brine trapped in ice: 30x → 15-21x, 51-71% recovery | `thermal.freeze_concentration`, `frozen_fraction_for_concentration` |
| 12 | Carnot "freeze engine" work per kg ice | audit_a, critic_a, erp2_a, rt_a, repair/a, gate_4 | 6 | MAJOR season average and fans cut output to 33-50% of EW | `thermal.heat_engine_work` |
| 13 | Hours below a threshold from monthly means (normal model) | audit_a ×2, critic_a, rt_a, erp2_a, repair/a | 6 | MAJOR −35 °C assumed for 150 days; only ~1,460 h exist | `climate.hours_below` |
| 14 | Degree-days and warm-window days from normals | audit_final, erp2_b, gate_4, gate_6 | 4 | MAJOR 92-day absence longer than non-heating window (51 d Chokurdakh) | `climate.degree_days`, `days_above` |
| 15 | Vapour pressure / humidity / drying capacity (Murphy-Koop, Magnus) | audit_a, critic_a, erp2_a, rt_a, roast, gate_4, repair/b | 7 | FATAL humidity fix ignores ore ice (74 vs 19-27 MJ/t); "free drying" margin 0.008 | `climate.psat_*`, `vapour_density` |
| 16 | Ice growth h = α√FDD, pure Stefan, snow resistance | erp2_b, critic_a, audit_b c5, audit_final, repair_final, repair_evo_b ×2, repair/b | 8 | MINOR/MAJOR ice window optimistic; "touch in March" band narrower than scatter | `ice.ice_thickness*`, `snow_conductivity`, `ice_growth_rate` |
| 17 | Gold's formula P = A h², flooded layer 0.65 rule | gate_7, gate_9, repair_evo_b | 3 | DEAD/WOUNDED: locomotive needs 2.8 m vs 1.2-1.95 m (margin 0.48) | `ice.gold_allowable_load`, `gold_required_thickness`, `stationary_load_capacity` |
| 18 | Floating-plate flexure: l, point deflection, edge line load (Hetényi) | audit_b c5, audit_b c3, repair_evo_a, audit_evo_2 | 4 | MAJOR 1.7-3.2 m sheet bridges boulders (7-29 MN for 0.3 m); hull uplift cracks ice | `ice.characteristic_length`, `point_load_deflection`, `edge_line_load_*`, `westergaard_*` |
| 19 | Ice buoyancy, stone lift, stacked ice, ice vs water depth | audit_b c5, critic_b I3, erp2_b I3, rt_b I3, repair/b, audit_final, roast, gate_7 | 8 | FATAL zero-freeboard lift 0.05 stone/ice; sawn ice cannot be sunk; riffle depth 2.3-3.0 m | `ice.ice_net_buoyancy`, `stone_lift_capacity`, `stacked_ice_capacity`, `water_under_ice`, `freezes_to_bed`, `required_depth_under_ice` |
| 20 | Glen creep, snow viscosity (Vionnet), thermal shock | audit_b c3/c6, erp2_b | 3 | FATAL snow buoyancy creeps 47-72%/day; −35 °C shell cracks in 0 °C water (24 MPa) | `ice.glen_strain_rate`, `snow_viscosity`, `thermal_shock_stress` |
| 21 | Drag vs friction stall window, slide threshold, melt and air buoyancy drift | audit_b, critic_b, rt_b, erp2_b, repair/b, roast, gate_6/7/8/9 | 10 | FATAL trim window used up in days; measured under-ice 0.05-0.25 m/s vs 0.6-0.95 needed | `naval.drag_force`, `max_buoyancy_to_slide`, `slide_threshold_velocity`, `buoyancy_loss_from_melt`, `air_buoyancy_change_per_m` |
| 22 | Displacement / draught / payload / rise per tonne | gate_7, gate_r1_2, audit_final, audit_evo_1/2, repair_final, repair_evo_a/b | 8 | MAJOR 3-3.9 m draft vs 1.5-2.9 m guaranteed depth; light hull impossible | `naval.*` |
| 23 | Frozen-ground strength vs time (Vyalov) and long-term values | audit_evo_2 (fit); gate_r1_2, repair_evo_a/b, audit_final (values) | 5 | MAJOR caving time spans 0.015-789 d; pillars 3 MPa vs 1.25 MPa long-term | `geotech.vyalov_*` |
| 24 | Roof/beam self-weight stress, critical span, cantilever | repair_evo_a, audit_evo_2, audit_final | 3 | MAJOR roof does not cave at ≥20 m cover; overhang 0.56-2.24 MPa breaks block | `geotech.beam_self_weight_stress`, `critical_span` |
| 25 | Pillar tributary / web stress, Mark-Bieniawski | gate_r1_2, audit_evo_1, repair_evo_a, repair_evo_b, audit_evo_2 | 5 | MAJOR 30-40 m cover doubles pillar stress (2.7-3.6 MPa) | `geotech.pillar_tributary_stress`, `web_pillar_stress`, `mark_bieniawski_strength` |
| 26 | Infinite slope / thaw-consolidation (McRoberts-Morgenstern) | audit_evo_1, repair_evo_b ×2 | 3 | MAJOR detachment at 10-12° not robust (z_crit 1.47 vs 1.6 m) | `geotech.infinite_slope_fs`, `thawing_slope_*`, `thaw_consolidation_ratio` |
| 27 | Bingham runout thickness | audit_evo_1, repair_evo_b | 2 | MAJOR thin sheets stall (need 0.73-8.2 m) | `geotech.bingham_*` |
| 28 | Consolidation t90 | audit_evo_1 | 1 | MAJOR cell holds fluid mud 7.6-41 yr | `geotech.consolidation_t90` |
| 29 | Adfreeze strength vs temperature (SNiP/SP tables) | gate_6, rt_b, audit_evo_1, repair_evo_a, repair_final, gate_9 | 6 | MAJOR anchors at −1…−0.5 °C: SF 0.57-1.4 | `geotech.adfreeze_strength`, `adfreeze_capacity` |
| 30 | Darcy seepage, hydrostatic sliding, thaw settlement | critic_b, audit_b, erp2_b, gate_7 | 4 | FATAL hoisted frozen lumps leak 0.09-8.5 m³/s | `geotech.darcy_seepage`, `sliding_fs`, `hydrostatic_thrust`, `thaw_settlement` |
| 31 | Manning, Shields (0.045 / Lamb slope / Soulsby), bedload MPM/Wong-Parker | audit_b c2, rt_b, critic_b, gate_2/3/4, repair_evo_a, audit_evo_2 | 8 | FATAL toe channel carries 2-19% of thaw; gravel won't flow at 0.5-1% (Shields 0.026-0.043) | `hydro.manning_*`, `shields_parameter`, `critical_shields_*`, `critical_grain_size`, `bedload_capacity` |
| 32 | Jets: centreline decay, monitor length; pumping and hydro-elevator power | audit_evo_2, gate_2, repair_evo_a | 3 | MAJOR sump must stay within 18-34 m of face; jet power assumptions | `hydro.jet_centreline_velocity`, `monitor_working_length`, `pumping_power`, `hydro_elevator_power` |
| 33 | Turbidity: release rate, full-mixing increment vs +0.25 mg/L, silt curtain | repair_evo_a, audit_evo_1, audit_evo_2 | 3 | FATAL full mixing assumed; cutter alone uses the allowance (needs ~1,900 m³/s) | `hydro.fines_release_rate`, `full_mixing_increment`, `dilution_flow_required`, `allowed_escape_fraction`, `silt_curtain_outside`, `mixing_length` |
| 34 | Breach peak (Froehlich 1995) | audit_b, critic_b, erp2_b, rt_b, repair/b | 5 | MAJOR forebay flood 2,700x baseflow on the crew | `hydro.froehlich_peak_outflow` |
| 35 | Fetch-limited waves (CEM/SPM), orbital velocity, fluidisation | critic_b, repair/b, gate_5 | 3 | FATAL no wave sorting (0.03 vs 0.09 m/s threshold) | `hydro.wave_growth_cem`, `wave_orbital_velocity` |
| 36 | Settling (Schiller-Naumann), aeolian threshold (Shao-Lu), u* | audit_b c4, critic_b, erp2_b, rt_b, repair/b | 5 | FATAL wind cannot separate gold from quartz (0.34-0.37 m/s) | `hydro.settling_velocity`, `aeolian_threshold_ustar`, `climate.friction_velocity` |
| 37 | Runoff, v~Q^m, pipe friction, Walther viscosity | gate_2/3/5/6/9 | 5 | DEAD canal/pulse ideas (lake 12 Mm³ vs 75 needed) | `hydro.runoff_mean_discharge`, `velocity_from_discharge`, `pipe_pressure_drop`, `walther_*` |
| 38 | CRF, levelised cost, capital charge | ledger, all gates, erp2_a, rt_a, repair_final, repair_evo_* | 15 | — (basis of every chain ratio) | `econ.crf`, `annualised_capex`, `levelised_cost` |
| 39 | Carrying cost / delay PV / inventory carry | audit_evo_1, critic_b, gate_1/5/9, rt_b | 6 | MAJOR pre-stripping 4-9 yr ahead: 3x → 1.1-2.5x | `econ.carry_forward_cost`, `delay_pv_factor`, `inventory_carry_cost` |
| 40 | Break-even volume/grade/distance/loss | erp2_a, gate_r1_1, repair_evo_b, roast, audit_evo_2 | 6 | FATAL break-even 4,800 km; grade 0.84 kg/m³ | `econ.breakeven_volume`, `breakeven_loss_fraction` |
| 41 | Ratio vs best-practice baseline, ceiling, gate verdict | all gates, all audits | 20 | MAJOR baseline wrong in ~1/3 of reviewed ideas | `econ.ratio_vs_baseline`, `ceiling_ratio`, `gate_verdict` |
| 42 | Cost per recovered unit, parity recovery | gate_1, erp2_b, rt_b, repair_evo_* | 6 | MAJOR washing stage small share per gram | `econ.cost_per_recovered_unit`, `parity_recovery` |
| 43 | Market share / demand | audit_final, audit_evo_1, gate_3, gate_r1_2 | 4 | MAJOR one barge = 21-27% of Arctic Yakutia coal | `econ.market_share` |
| 44 | Rate × time season window | almost every review (e.g. audit_final, audit_evo_1, gate_r1_2) | 20 | FATAL lake exhausted in 18-31 days; 62-95 d augering vs 60-120 d | `econ.season_capacity`, `window_margin` |
| 45 | Statistics: zero-failure bound, rule of 3, sample sizes, Poisson | audit_a, audit_b, critic_b ×2, rt_b, roast, audit_final ×2, audit_evo_1 | 10 | MINOR/MAJOR pilots cannot show reliability (59 failure-free trials for 5%) | `stats.*` |

Not implemented (idea-specific chemistry/physics, kept in the run scripts): Ni(CO)₄ vapour pressure and
equilibrium, Fe(CO)₅, plume half-life (audit_a, critic_a, erp2_a, rt_a, repair/a, gate_6); triboelectric drift,
space charge, cascade gambler's-ruin (audit_a, critic_a, erp2_a, rt_a, roast, gate_5); Bond comminution (audit_a,
critic_a); surface-energy-balance sublimation models (erp2_b, rt_b, repair/b, critic_b); Hertz-Knudsen
evaporation, Shomate enthalpy (gate_1/2); Plouff prism gravity (gate_7); Raupach drag partition (critic_b);
Kremser absorber (erp2_a); n-butane/propane Antoine and hydrate lines (audit_a, rt_a, critic_a).
Westergaard plate stresses were not in the harvest; they were added for the requested edge reduction.

## 2. Recurring data values (all in `kit/data.py` with source strings)

| Value | Source (harvest) | Recurs | Kit key |
|---|---|---|---|
| Monthly normals: Verkhoyansk (12 months), Udachny, Yakutsk, Chara, Pevek, Tiksi, Susuman, Chokurdakh, Srednekolymsk, Norilsk | Wikipedia/kupi/climate-data via search (audit_final, critic_a, rt_a, erp2_a/b, rt_b, gate_4) | 12 | `climate.<site>.monthly/summer` |
| Hourly SD within month 5-8 K | assumption (critic_a, rt_a, erp2_a) | 6 | `climate.hourly_sd_within_month` |
| FDD 4,500-7,000; Verkhoyansk 6,690; Tiksi 5,500 | repair_final, audit_final, repair_evo_b | 7 | `climate.fdd_*` |
| GHI Yakutsk May-Sep; Oymyakon July 611.7 MJ/m² | SNiP Table 17 (gate_8, audit_b) | 3 | `climate.ghi_*` |
| Ice α 0.017-0.027; end-of-winter ice: Lena 1.2-1.4 m, tundra rivers 1.5-2.0, Kolyma 0.8-1.3, upper Kolyma 1.05-2.5, landfast 2.0 | Michel 1971; MSU; E3S 2020; BRE (gate_7/9, repair_*) | 9 | `ice.*` |
| Gold A 3.5 / 7 / ~17; parking ≤2 h | Gold 1971 (gate_7, gate_9, repair_evo_b; web check) | 3 | `ice.gold_A_*`, `ice.parking_limit_h` |
| Under-ice velocities Lena delta 0.05-0.25 m/s; under-ice water −0.1…+0.8 °C | Fedorova et al. 2020 (erp2_b, roast, gate_6/7/8/9, repair/b) | 7 | `river.lena_delta_*`, `ice.water_temp_*` |
| Frazil deposition limit 0.61-0.8 m/s; Krasnoyarsk tailwater open 200-300 km | MDPI Water 15:4242; Wikipedia (audit_b, critic_b, erp2_b) | 3 | `ice.under_cover_deposition_velocity`, `ice.krasnoyarsk_tailwater_open` |
| Kolyma flows, April/annual 5.2%, runoff 190 mm; Lena Q; guaranteed depths 1.0-2.9 m | GRDC, BSE, Mintrans (gate_3/4/5/6/8, gate_r1_2, audit_evo_1) | 8 | `river.*` |
| Kolyma reservoir NPU 451.5 / UMO 432 m | RusHydro (audit_evo_1, repair_evo_a) | 2 | `river.kolyma_reservoir_levels` |
| Ledger: FX 84; diesel 64.8 exchange / 120-150 site RUB/l; mine diesel power 41 RUB/kWh ($0.49); FNPP 6.45 RUB/kWh; winter road 20 RUB/t-km; LORP 3-5 RUB/t-km; archetypes A/B/C/D/E | genius/ledger (all gates) | 11 | `price.*` |
| Sluice water 3.2-9.9 m³/m³ (RU 10-20, kuzstu ~3) | USBM/911metallurgist, Yukon atlas (audit_b, critic_b, erp2_b, gate_8, repair/b, rt_b) | 6 | `base.sluice_water_ratio_us` |
| Boulder dozer/grapple $2.7-3.0/m³; dozer limit 1.0-1.2 m | erp2_b, critic_b, audit_b | 3 | `base.boulder_dozer_grapple` |
| Fishery SS limit +0.25 / +0.75 mg/L | Minselkhoz Order 552/2016 (repair_evo_a, audit_evo_1) | 2 | `limit.fishery_*` |
| Adfreeze Raf tables | SNiP 2.02.04-88 / SP 25.13330 (gate_6, audit_evo_1; web-checked) | 6 | `geotech._ADFREEZE_KPA` |
| Frozen-ground strengths: UCS 5-8 MPa, long-term 1.25-2 MPa, tensile 0.2-0.5 MPa long-term | Tsytovich / estimates (repair_evo_*, gate_r1_2, audit_evo_2) | 5 | `ground.*` |
| Ice friction 0.15-0.76 (ice-ice), 0.02-0.47 (hull) | arXiv 1502.04173; Vance 1980 (gate_6/8, repair/b, rt_b) | 6 | `ice.friction_*` |
| Arctic Yakutia coal 205 kt/yr, 3 t/person; Yakutia waterborne communal coal 122 kt | audit_final, audit_evo_1 | 2 | `base.arctic_yakutia_utility_coal` |
| Silt-curtain efficiency 0.45-0.95; hydro-elevator η 0.17-0.35 | web search (HK EPD; Pak/Veselov) | new | `limit.*` |

## 3. Disagreements between harvested versions and the choice made

| Model / value | Versions found | Chosen (reason) |
|---|---|---|
| Bedload transport | MPM q* = 8(θ−0.047)^1.5 (gate_3, gate_4, repair_evo_a) vs Wong-Parker 3.97(θ−0.0495)^1.5 (audit_b) | Wong-Parker 2006 default (peer-reviewed reanalysis of MPM's own data; MPM ~2x high); MPM kept as option |
| Shao-Lu threshold | A_N 0.0123, γ 3e-4 (audit_b, critic_b, erp2_b, rt_b) vs 0.0111 / 2.9e-4 (repair/b) | Published Shao & Lu 2000 values 0.0123 / 3e-4 |
| Edge line load on ice | M = 0.3224 P/β (audit_evo_2) vs M = 0.32 P l_c (repair_evo_a) | Hetényi 0.3224 P/β; the l_c form is low by √2 (1/β = √2 l_c) |
| Pillar strength | 0.64 + 0.54 w/h (audit_evo_1) vs 0.64 + 0.36 w/h (repair_evo_a) | Mark-Bieniawski strip form 0.54 (0.36 is Bieniawski's square-pillar formula) |
| Zero-failure bound | Rule of three 3/n (audit_b, critic_b, rt_b, audit_final) vs exact 1−0.05^(1/n) (roast) | Exact; rule of three kept as `stats.rule_of_three` |
| Face heat transfer | Dittus-Boelter (audit_b, repair_evo_a), Stanton 0.0015-0.006 (repair/b, rt_b), Gnielinski ×3 (audit_evo_2) | Gnielinski with roughness factor 1-3 (Douglas et al. 2023) preferred; others kept for cross-checks |
| Ice-water h for shells/pods | Ashton 1622 V^0.8/D^0.2 (critic_b), flat plate (roast), assumed 400 (rt_b) | Ashton (river-ice standard); agree within 10% |
| Wave growth | SPM 0.0016 U²/g… (repair/b) vs CEM u*-based (gate_5) | CEM 2002 (same answers within 1%) |
| Open-water loss | Bulk formula (gate_r1_1, audit_final, repair_final) vs h = 5.7+3.8u (audit_evo_2) vs measured 484 W/m² (Makinson) | Bulk formula, documented as ~20% above the Makinson measurement |
| Ice growth coefficient | α 0.017-0.024 / 0.027 (several) vs Stefan × 0.7 / 0.45 (repair/b) | α table (Michel 1971) + physical snow-resistance form |
| n-butane Antoine | 3.85002/909.65/−36.146 (audit_a, NIST range 195-273 K) vs 4.35576/1175.581/−2.071 (rt_a, NIST range 272-425 K mislabelled) | Not in kit; audit_a coefficients are the valid ones below 0 °C |
| Winter road rate | 20 RUB/t-km = $0.24 (ledger [S]) vs $0.117-0.118 (audit_b, repair/b), $0.15-0.20 (erp2_a), $0.177 (erp2_b) | Ledger value; others recorded in the note |
| Diesel power price | $0.49/kWh (ledger) vs $0.15 (audit_a), $0.30 (erp2_a, rt_a), 10-40 RUB/kWh (repair/a) | Ledger (newest, itemised) |
| Kolyma winter discharge at Srednekolymsk | 61-127 m³/s (GRDC, gate_8) vs ~327 m³/s (rt_b from Majhi 2007 increments) | GRDC measured monthly means; post-dam figure flagged as unverified |
| Tiksi May mean | −7.6 °C (rt_b) vs −4.1 °C (critic_b) | Both recorded; not used in tests |
| FX | 84 (ledger) vs 85-90 (repair_final, erp2_a, repair/a) | 84 |
