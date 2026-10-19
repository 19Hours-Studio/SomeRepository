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
