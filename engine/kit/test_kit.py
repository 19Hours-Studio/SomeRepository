"""Tests for engine/kit. Run:  python3 engine/kit/test_kit.py   -> prints 'OK kit: <n> checks'.

Every numeric check names its reference: a textbook/literature value, or a value printed/stated in a
harvested script or review under engine/runs/permafrost/ (path given). Tolerances reflect the rounding of
the reference (e.g. a review quoting '0.59 MPa' is checked to ~1-2%).
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kit import climate, data, econ, geotech, hydro, ice, naval, stats, thermal  # noqa: E402

N = 0
FAIL = []


def check(name, got, ref, rtol=0.02, atol=0.0):
    global N
    N += 1
    ok = abs(got - ref) <= max(atol, rtol * abs(ref))
    if not ok:
        FAIL.append(f"{name}: got {got!r}, expected {ref!r} (rtol {rtol}, atol {atol})")


def check_true(name, cond):
    global N
    N += 1
    if not cond:
        FAIL.append(f"{name}: condition false")


def check_raises(name, fn, *a, **k):
    global N
    N += 1
    try:
        fn(*a, **k)
    except ValueError:
        return
    FAIL.append(f"{name}: no ValueError raised")


DAY, YR = 86400.0, 3.156e7

# ====================================================================== climate
V = data.monthly("Verkhoyansk")
# genius/audit_final/audit_calc.py: Verkhoyansk FDD from monthly normals ~6,690 C*d
check("FDD Verkhoyansk", climate.degree_days(V)[0], 6690, 0.005)
# genius/audit_final: days with daily mean > 8 C: Verkhoyansk 90, Chokurdakh 51, Srednekolymsk 78-80
check("days>8 Verkhoyansk", climate.days_above(V, 8), 90, atol=0)
chok = dict(zip(data.MONTHS, [-34.0, -33.0, -27.0, -18.0, -4.9, 6.7, 10.6, 8.1, 1.6, -12.0, -26.0, -32.0]))
check("days>8 Chokurdakh", climate.days_above(chok, 8), 51, atol=0)
for may, ref in ((-1.0, 78), (1.0, 80)):
    s = dict(zip(data.MONTHS, [-38.0, -35.0, -26.0, -13.0, may, 11.2, 13.9, 10.1, 3.2, -12.0, -28.0, -36.0]))
    check(f"days>8 Srednekolymsk May {may}", climate.days_above(s, 8), ref, atol=0)
U = data.monthly("Udachny")
# round2/critic_a REVIEW: Udachny ~273 h <= -45 C, estimated 142-375 h (SD 5-8 K)
check("Udachny <=-45 sd5", climate.hours_below(U, -45, 5), 142, 0.01)
check("Udachny <=-45 sd8", climate.hours_below(U, -45, 8), 375, 0.01)
# round2/audit_a REVIEW: 140-283 h for within-month SD 5-7 K (Dec -36, Jan -39.4, Feb -35)
djf = {"Dec": -36.0, "Jan": -39.4, "Feb": -35.0}
check("Udachny DJF sd5", climate.hours_below(djf, -45, 5), 140, 0.01)
check("Udachny DJF sd7", climate.hours_below(djf, -45, 7), 283, 0.01)
# round2/audit_a REVIEW: Yakutsk-type winter ~1,460 h <= -35 C
check("Yakutsk <=-35", climate.hours_below({"Nov": -28, "Dec": -38, "Jan": -39, "Feb": -34, "Mar": -21}, -35, 6), 1460, 0.01)
check("hours above+below = total", climate.hours_above(djf, -45, 6) + climate.hours_below(djf, -45, 6), 24 * 90, 1e-9)
# Murphy & Koop 2005 / roast/roast.py: 0.9*psat_ice(-40 C) = 11.6 Pa; genius/gate_4: e_ice(-30 C) = 38.0 Pa
check("psat_ice -40", 0.9 * climate.psat_ice(-40), 11.6, 0.005)
check("psat_ice -30", climate.psat_ice(-30), 38.0, 0.003)
# WMO/CRC: saturation vapour pressure over water at 0 C = 611.2 Pa
check("psat_water 0", climate.psat_water(0), 611.2, 0.001)
# round2/critic_a & repair/a: -40 C air at 90% RH(ice) warmed to 0 C -> RH 1.9%
check("RH 1.9%", 0.9 * climate.psat_ice(-40) / climate.psat_water(0), 0.019, 0.02)
# genius/gate_4: saturated vapour density over ice at -30 C = 0.339 g/m3
check("vapour density -30", climate.vapour_density(-30) * 1e3, 0.339, 0.01)
# Duffie & Beckman Example 1.10.1: H0 at 43 N on 15 April (n=105) = 33.8 MJ/m2 (Gsc 1367)
check("H0 Duffie-Beckman", climate.toa_daily_mean_irradiance(43, 105, 1367) * DAY / 1e6, 33.8, 0.005)
# round2/critic_b: U10 7 m/s, z0 0.5-3 mm -> u* 0.28-0.35 m/s
check("u* z0 0.5 mm", climate.friction_velocity(7, 0.0005), 0.28, 0.02)
check("u* z0 3 mm", climate.friction_velocity(7, 0.003), 0.345, 0.01)
# ideal gas: dry air at 0 C, 1 atm = 1.292 kg/m3
check("air density 0 C", climate.air_density(0), 1.292, 0.002)
check_raises("hours_below bad month", climate.hours_below, {"Foo": -30}, -40)
check_raises("hours_below sd<=0", climate.hours_below, djf, -40, 0)
check_raises("psat_ice above 0", climate.psat_ice, 5)
check_raises("days_above needs 12 months", climate.days_above, djf, 8)

# ====================================================================== thermal
E30 = thermal.thaw_energy_per_m3(0.30, -5)
# round2/erp2_b/idea2_out.txt: ice-cemented pile 30% ice at -5 C = 100.9 MJ/m3; loose lumps 15% = 54.9 MJ/m3
check("thaw energy 0.30", E30 / 1e6, 100.9, 0.002)
check("thaw energy 0.15", thermal.thaw_energy_per_m3(0.15, -5) / 1e6, 54.9, 0.002)
# CRC: 1 m3 of ice = 917 kg x 334 kJ/kg = 306 MJ (round2/audit_b/c1_dam.py)
check("latent per m3 ice", thermal.latent_heat_per_m3(1.0) / 1e6, 306.3, 0.001)
# round2/erp2_b: 8 C water cooled to 0.5 C at 85% heat use -> 3.8 m3 water per m3 (ice 0.30)
check("water ratio", thermal.water_ratio(E30, 7.5, 0.85), 3.8, 0.01)
# round2/erp2_b: Q 47 L/s, 5 C, ice 0.15 -> feed 49.3 m3/h
check("thaw feed rate", thermal.thaw_feed_rate(0.047, 4.5, thermal.thaw_energy_per_m3(0.15, -5), 0.85) * 3600, 49.3, 0.005)
# round2/critic_b REVIEW: the dam design needs 748 kW, i.e. 3.8 K extracted from 47 L/s
check("water heat power", thermal.water_heat_power(0.047, 3.8) / 1e3, 748, 0.005)
# round2/critic_b/calc_idea2.py: peat (80-90% water, k 0.5) thaws 0.48-0.67 m for 800-1,400 C*d (Stefan)
check("Stefan DD low", thermal.stefan_depth_degree_days(800, 0.9 * 334e6, 0.5), 0.48, 0.01)
check("Stefan DD high", thermal.stefan_depth_degree_days(1400, 0.8 * 334e6, 0.5), 0.67, 0.01)
# genius/audit_final: 300 m3/day of ice -> 1.06 MW latent
check("melt power", thermal.melt_power(300) / 1e6, 1.06, 0.005)
# round2/audit_b/c1_dam.py: peat (80% water, k 0.5) under 7 C water for 90 d thaws 0.45 m (Stefan)
check("Stefan peat", thermal.stefan_depth(7, 90 * DAY, 0.8 * 334e6, 0.5), 0.45, 0.01)
# repair/a/idea2_out.txt: Stefan ice on panel at dT 6 K over 150 d = 1.06 m per face
check("Stefan panel ice", thermal.stefan_depth(6, 150 * DAY, 917 * 334e3, 2.2), 1.06, 0.005)
check("Stefan time inverse", thermal.stefan_time(1.06, 6, 917 * 334e3, 2.2) / DAY, 150, 0.01)
# genius/repair_final: thaw to 15 m below a lake floor (ice 0.25, k 2, dT 3) takes >= ~45 yr
check("Stefan time talik 15 m", thermal.stefan_time(15, 3, 0.25 * 917 * 334e3, 2.0) / YR, 45.5, 0.02)
# genius/gate_7/calc.py 8_killer: heated building R 5.2 m2K/W, 20 yr, dT 20, ice 40% -> 10.7 m thaw
Lv_b = 0.4 * 917 * 334e3 + 2.0e6 * 4
check("Stefan with resistance", thermal.stefan_depth_with_resistance(20, 20 * YR, Lv_b, 1.4, 5.2), 10.7, 0.005)
# round2/audit_b REVIEW: 0.4 m lift, one-sided Stefan at -20 C, h 15 -> ~95 h
check("lift freeze time", thermal.stefan_time_with_resistance(0.4, 20, 0.35 * 334e6, 2.5, 1 / 15) / 3600, 95, 0.01)
check("Stefan resistance consistency", thermal.stefan_depth_with_resistance(20, thermal.stefan_time_with_resistance(3.0, 20, Lv_b, 1.4, 5.2), Lv_b, 1.4, 5.2), 3.0, 1e-6)
# genius/audit_evo_1 REVIEW: Neumann (ice 25%, ground -4 C, 40 yr) 5.6/8.5/10.8/12.7 m at 1/2/3/4 C
for Tw, ref in ((1, 5.6), (2, 8.5), (3, 10.8), (4, 12.7)):
    check(f"Neumann Tw={Tw}", thermal.neumann_depth(Tw, -4, 40 * 365.25 * DAY, 306e6 * 0.25), ref, 0.01)
check_true("Neumann < Stefan (cold content)", thermal.neumann_depth(2, -4, 40 * YR, 306e6 * 0.25) <
           thermal.stefan_depth(2, 40 * YR, 306e6 * 0.25, 1.8))
# genius/repair_final LOG: steady talik 15-22 m at R 50 m, 36-67 m at R 100 m (Ts -6, Tb +3, G 0.03)
check("talik R50", thermal.talik_depth_lake_axis(50, -6, 3, 0.03), 22.3, 0.01)
check("talik R100", thermal.talik_depth_lake_axis(100, -6, 3, 0.03), 67.0, 0.01)
check_true("talik through (R 200 warm)", math.isinf(thermal.talik_depth_lake_axis(200, -2, 4, 0.03)))
# genius/repair_evo_a LOG: Dittus-Boelter in a 2x1.5 m gallery, 1 m3/s -> h ~860 W/m2K
check("Dittus-Boelter", thermal.h_dittus_boelter(1.0 / 1.8, 4 * 1.8 / 3.8, 1.52e-6, 0.57, 11.2), 860, 0.01)
# genius/audit_evo_2 REVIEW: Gnielinski x3 roughness, 1-3 m/s, Dh 0.1-0.2 -> 8-22 kW/m2K
check("Gnielinski low", thermal.h_gnielinski(1, 0.2, roughness_factor=3) / 1e3, 7.8, 0.01)
check("Gnielinski high", thermal.h_gnielinski(3, 0.1, roughness_factor=3) / 1e3, 22.3, 0.01)
# genius/audit_evo_2 REVIEW: jet stagnation 50 mm at 10-15 m/s -> 12-15 kW/m2K
check("jet stagnation 10", thermal.h_jet_stagnation(10, 0.05) / 1e3, 12.3, 0.01)
check("jet stagnation 15", thermal.h_jet_stagnation(15, 0.05) / 1e3, 15.0, 0.01)
# roast/roast.py: turbulent flat plate, 5 m pod at 0.2 m/s -> h 390 W/m2K
check("flat plate", thermal.h_flat_plate_turbulent(0.2, 5.0), 390, 0.01)
# round2/critic_b/calc_extra.py: Ashton h = 1622 V^0.8/D^0.2 -> 360-500 W/m2K at 0.2-0.3 m/s, D 3 m
check("Ashton 0.2", thermal.h_ice_water_ashton(0.2, 3), 359, 0.005)
check("Ashton 0.3", thermal.h_ice_water_ashton(0.3, 3), 497, 0.005)
# repair/b/out_idea2.txt: St 0.0015, U 0.5 -> h 3142 W/m2K (c_w 4.19e6 there; 4.18e6 here)
check("Stanton h", thermal.h_from_stanton(0.0015, 0.5), 3142, 0.005)
# roast/roast.py: h 390 W/m2K (pod lagging 0.2 m/s): +0.02 K -> 2.2 mm/day, +0.5 K -> 55.0 mm/day of shell melt
check("ice melt +0.02 K", thermal.ice_melt_rate(390, 0.02) * DAY * 1000, 2.2, 0.01)
check("ice melt +0.5 K", thermal.ice_melt_rate(390, 0.5) * DAY * 1000, 55.0, 0.005)
# round2/critic_b: the stated 6 cm per 45 d corresponds to only ~+0.01 K at h 360-500 (Ashton)
check("ice melt 0.01 K 45 d", thermal.ice_melt_rate(thermal.h_ice_water_ashton(0.3, 3), 0.01) * 45 * DAY, 0.06, 0.12)
# round2/critic_b: debris coat - 0.8 m/day at 101 MJ/m3 needs 935 W/m2; k 2.0, dT 7.5 -> coat <= 1.6 cm
check("debris coat flux", thermal.debris_coat_limited_flux(2.0, 7.5, 0.016), 937.5, 0.001)
check("face retreat", thermal.face_retreat_rate(7496, 6, thermal.thaw_energy_per_m3(0.15, -5)) * DAY, 70.7, 0.01)  # erp2_b: 70.73 m/d
# genius/audit_evo_2 REVIEW: 4 C water to 0.9 C at 0.125 m3/s per monitor needs hA >= 781 kW/K
check("NTU hA", thermal.ntu_required(4, 0.9) * 0.125 * 4.186e6 / 1e3, 781, 0.002)
# round2/rt_b/calc_idea2.py: toe channel 47 L/s, 0.6 m, S 0.05, St 0.002-0.006 -> e-folding length 31-10 m
_dt, _Rt, _Vt = hydro.manning_depth_rect(0.047, 0.6, 0.05, 0.035)
check("e-fold St 0.002", thermal.efold_length(0.047, thermal.h_from_stanton(0.002, _Vt), 0.6 + 2 * _dt), 31.0, 0.01)
check("e-fold St 0.006", thermal.efold_length(0.047, thermal.h_from_stanton(0.006, _Vt), 0.6 + 2 * _dt), 10.3, 0.01)
# genius/gate_r1_1: open water at -40 C, 5 m/s, bulk Ch 1.5e-3 -> 748 W/m2
check("open water -40/5", thermal.open_water_heat_loss(-40, 5), 748, 0.01)
# Makinson Inlet polynya measured ~484 W/m2 at -30 C, 5 m/s (genius/audit_final); bulk model within 25%
check("open water vs Makinson", thermal.open_water_heat_loss(-30, 5, T_water=-1.0), 484, 0.25)
# genius/repair_final: Maykut 1978 leads 400-700 W/m2; model at -35 C, 3 m/s ~460-470
check("open water -35/3", thermal.open_water_heat_loss(-35, 3), 465, 0.03)
# genius/audit_final REVIEW: open pond losing 500 W/m2 freezes ~6 mm/h
check("open water freezing", thermal.open_water_freezing_rate(500) * 3600 * 1000, 5.9, 0.01)
# genius/audit_evo_2 REVIEW: 3 ha pond at 7 C in August (Susuman 10.9 C, Kt 0.40-0.45) -> 3.1-3.6 MW
for Kt, ref in ((0.40, 3.13), (0.45, 3.62)):
    SW = Kt * climate.toa_daily_mean_irradiance(62.8, 227)
    check(f"pond Aug Kt {Kt}", thermal.water_surface_net_flux(SW, 10.9, 7) * 3e4 / 1e6, ref, 0.02)
# round2/audit_a, critic_a, repair/a (x3): 8-13 um band at -50 C = 30.0 W/m2 = 21.3% of sigma T^4
check("Planck band -50", thermal.planck_band_exitance(223.15), 30.0, 0.005)
check("Planck band share", thermal.planck_band_exitance(223.15) / thermal.blackbody_exitance(223.15), 0.213, 0.005)
# repair/a/idea4_out.txt: +20 C: 132.7 W/m2 (31.7%); -40 C: 39.1 W/m2
check("Planck band +20", thermal.planck_band_exitance(293.15), 132.7, 0.005)
check("Planck band -40", thermal.planck_band_exitance(233.15), 39.1, 0.005)
# Stefan-Boltzmann: sigma 273.15^4 = 315.6 W/m2
check("blackbody 0 C", thermal.blackbody_exitance(273.15), 315.6, 0.001)
# genius/audit_evo_2/check2b.py: isolated 2.2 m hole, 35% water: 304 d (-3 C), 164 d (-5 C), 93 d (-8 C)
for Tg, ref in ((-3, 304), (-5, 164), (-8, 93)):
    check(f"hole freeze R1.1 {Tg}", thermal.freeze_time_cylinder(1.1, Tg, 0.35), ref, 0.03)
# genius/audit_evo_2 REVIEW: a 1.6 m hole takes 87-161 d (-5..-3 C)
check("hole freeze R0.8 -3", thermal.freeze_time_cylinder(0.8, -3, 0.35), 161, 0.03)
# genius/audit_evo_2 REVIEW: panel (slab) freezing 1.3-15 yr at -5..-2 C (water 0.30-0.40)
check("slab freeze fast", thermal.freeze_time_slab_two_sided(1.598 * 0.30 * 334e6, 2.0, 5) / YR, 1.33, 0.02)
check("slab freeze slow", thermal.freeze_time_slab_two_sided(1.598 * 0.40 * 334e6, 2.0, 2) / YR, 14.8, 0.02)
# round2/audit_a/calc_lithium.py: Scheil f=1/30: k 0.1 -> 21x, 71% kept; k 0.2 -> 15x, 51%
cf, kept = thermal.freeze_concentration(1 / 30, 0.1)
check("Scheil k0.1 cf", cf, 21.4, 0.01)
check("Scheil k0.1 kept", kept, 0.71, 0.01)
check("Scheil k0.2 kept", thermal.freeze_concentration(1 / 30, 0.2)[1], 0.51, 0.01)
# genius/gate_4: CF 20 with K 0.1 needs f = 0.964 frozen
check("frozen fraction for CF", thermal.frozen_fraction_for_concentration(20, 0.1), 0.964, 0.001)
# repair/a/idea2_out.txt: freeze engine 55% Carnot, -6 C to air+12: 11.7 kJ/kg at -35 C, 15.1 at -40 C
check("engine -35", thermal.heat_engine_work(334e3, -6, -23, 0.55) / 1e3, 11.7, 0.005)
check("engine -40", thermal.heat_engine_work(334e3, -6, -28, 0.55) / 1e3, 15.1, 0.005)
check_raises("thaw energy T0>0", thermal.thaw_energy_per_m3, 0.3, 2)
check_raises("ice frac >1", thermal.latent_heat_per_m3, 1.2)
check_raises("water ratio dT 0", thermal.water_ratio, 1e8, 0)
check_raises("Stefan negative time", thermal.stefan_depth, 5, -1, 1e8, 2)
check_raises("talik warm ground", thermal.talik_depth_lake_axis, 50, 1, 3)
check_raises("DB laminar", thermal.h_dittus_boelter, 0.01, 0.01)
check_raises("Gnielinski range", thermal.h_gnielinski, 1e-3, 0.01)
check_raises("open water warm air", thermal.open_water_heat_loss, 5, 3)
check_raises("hole freeze warm ground", thermal.freeze_time_cylinder, 1.0, 1.0, 0.3)
check_raises("Neumann bad T", thermal.neumann_depth, -1, -4, 1e8, 1e8)

# ====================================================================== ice
# Michel 1971 alpha / genius/repair_final: FDD 5000-6500 -> 1.2-1.9 m lake ice
check("ice alpha low", ice.ice_thickness(5000, 0.017), 1.20, 0.01)
check("ice alpha high", ice.ice_thickness(6500, 0.024), 1.93, 0.01)
# round2/erp2_b/idea2_out.txt: FDD 5141, a 2.4 -> 1.72 m
check("ice erp2_b", ice.ice_thickness(5141, 0.024), 1.72, 0.005)
# genius/audit_final REVIEW: pure Stefan, no snow, 5,000-6,500 C*d -> 2.49-2.84 m
check("pure Stefan 5000", ice.ice_thickness_stefan(5000), 2.49, 0.005)
check("pure Stefan 6500", ice.ice_thickness_stefan(6500), 2.84, 0.005)
check("snow-free = pure Stefan", ice.ice_thickness_with_snow(5000, 0.0), ice.ice_thickness_stefan(5000), 1e-9)
check_true("snow reduces growth", ice.ice_thickness_with_snow(5000, 0.3) < 0.5 * ice.ice_thickness_stefan(5000))
# Sturm et al. 1997 / genius/gate_9: rho 0.45 g/cm3 -> k 0.34 W/mK
check("Sturm snow k", ice.snow_conductivity(0.45), 0.338, 0.005)
# repair/b/out_idea4.txt: basal growth 1.9 cm/day under 1.0 m ice, 1.0 cm/day under 1.8 m (surface -30 C)
check("basal growth 1.0", ice.ice_growth_rate(1.0, -30) * DAY * 100, 1.9, 0.03)
check("basal growth 1.8", ice.ice_growth_rate(1.8, -30) * DAY * 100, 1.0, 0.04)
# round2/audit_b REVIEW: freeze-on through 1.7 m ice, 0-0.3 m snow, 775 C*d -> 31-73 cm
check("freeze-on 1.7 no snow", ice.freeze_on_below_ice(775, 1.7, 0.0, 0.30), 0.73, 0.01)
check("freeze-on 1.7 snow", ice.freeze_on_below_ice(775, 1.7, 0.3, 0.35), 0.31, 0.02)
# round2/audit_b REVIEW idea 12: 91 C*d with ~0.3 m snow -> 4.4 cm; snow-free 8.5-9.9 cm
check("freeze-on 91 snow", ice.freeze_on_below_ice(91, 1.7, 0.3, 0.30), 0.044, 0.01)
check("freeze-on 91 no snow", ice.freeze_on_below_ice(91, 1.7, 0.0, 0.30), 0.099, 0.01)
check("days to thickness", ice.days_to_thickness(0.8, 5500 / 240, 0.027), (0.8 / 0.027) ** 2 / (5500 / 240), 1e-9)
# genius/repair_evo_b calc_idea1: Gold A 3.5 -> 22 t at 0.8 m, 50 t at 1.2 m, 113 t at 1.8 m
for h, ref in ((0.8, 22.4), (1.2, 50.4), (1.8, 113.4)):
    check(f"Gold {h} m", ice.gold_allowable_load(h), ref, 0.002)
# genius/gate_7: 2TE116 (2 x 138 t) needs 281 cm at A 3.5; h_eff = 1.3 + 0.65*1.0 = 1.95 m
check("Gold required 2TE116", ice.gold_required_thickness(276), 2.81, 0.002)
check("Gold flooded layer", ice.gold_allowable_load(1.3, flooded_m=1.0), 3.5 * 195 ** 2 / 1000, 1e-9)
check("stationary <= 2 h = Gold", ice.stationary_load_capacity(1.0, 1.5), ice.gold_allowable_load(1.0), 1e-12)
check("stationary 24 h halved", ice.stationary_load_capacity(1.0, 24), 0.5 * ice.gold_allowable_load(1.0), 1e-12)
check_raises("stationary > 7 days", ice.stationary_load_capacity, 1.0, 400)
# round2/audit_b/c5_ice.py REVIEW: l = 18-35 m and 7-29 MN to deflect 1.7-3.2 m ice by 0.3 m (E 2-5 GPa)
check("char length 1.7/2GPa", ice.characteristic_length(1.7, 2e9), 17.5, 0.01)
check("char length 3.2/5GPa", ice.characteristic_length(3.2, 5e9), 35.4, 0.01)
check("point load 1.7", 0.3 / ice.point_load_deflection(1.0, 1.7, 2e9) / 1e6, 7.2, 0.01)
check("point load 3.2", 0.3 / ice.point_load_deflection(1.0, 3.2, 5e9) / 1e6, 29.4, 0.01)
# Westergaard: generic-nu interior = textbook numeric form at nu 0.15: 0.316 P/h^2 (4 log10(l/b) + 1.069)
h_, a_, E_ = 0.25, 0.15, 30e9
l_ = ice.characteristic_length(h_, E_, 0.15, 80e6)
b_ = math.sqrt(1.6 * a_ ** 2 + h_ ** 2) - 0.675 * h_
check("Westergaard interior numeric form", ice.westergaard_interior_stress(1e5, h_, a_, E_, 0.15, 80e6),
      0.316 * 1e5 / h_ ** 2 * (4 * math.log10(l_ / b_) + 1.069), 0.003)
# Westergaard 1926 edge numeric form at nu 0.15: 0.572 P/h^2 (4 log10(l/b) + 0.359) (pavement texts)
check("Westergaard 1926 edge numeric form", ice.westergaard_edge_stress(1e5, h_, a_, E_, 0.15, 80e6, method="1926"),
      0.572 * 1e5 / h_ ** 2 * (4 * math.log10(l_ / b_) + 0.359), 0.003)
# Ioannides et al. 1985: 1926 edge formula unconservative -> 1948 edge stress higher; edge carries ~half
check_true("1948 edge > 1926 edge", ice.westergaard_edge_stress(1e5, 1.0, 0.3) > ice.westergaard_edge_stress(1e5, 1.0, 0.3, method="1926"))
check("edge capacity factor 1 m ice", ice.edge_capacity_factor(1.0), 0.47, 0.02)
# genius/audit_evo_2 REVIEW: 3 kt uplift on a 130.8x22 m hull, 1.5-2 m ice, E 5 GPa -> 1.6-3.6 MPa
Pline = 3e6 * 9.81 / (2 * (130.8 + 22))
check("edge line load free 2.0", ice.edge_line_load_stress(Pline, 2.0, 5e9) / 1e6, 1.64, 0.01)
check("edge line load clamped 1.5", ice.edge_line_load_stress(Pline, 1.5, 5e9, edge="clamped") / 1e6, 3.64, 0.01)
check("edge capacity inverse", ice.edge_line_load_stress(ice.edge_line_load_capacity(0.8e6, 1.5), 1.5) / 1e6, 0.8, 1e-9)
# round2/erp2_b: 1.7 m ice buoyancy 141 kg/m2 lifts 0.086 m3 stone/m2; 3.2 m -> 0.161; +4.4 cm gravel -> 0.058
check("ice buoyancy", ice.ice_net_buoyancy(1.7), 141.1, 0.001)
check("stone lift 1.7", ice.stone_lift_capacity(1.7), 0.086, 0.01)
check("stone lift 3.2", ice.stone_lift_capacity(3.2), 0.161, 0.005)
check("stone lift frozen-on", ice.stone_lift_capacity(1.7, frozen_on_sediment_m=0.044), 0.058, 0.01)
# genius/audit_final REVIEW: sheet carries only 0.11-0.17 m of stacked ice (1.2-1.9 m sheet)
check("stacked ice 1.2", ice.stacked_ice_capacity(1.2), 0.11, 0.02)
check("stacked ice 1.9", ice.stacked_ice_capacity(1.9), 0.17, 0.02)
# round2/critic_b: ice 1.2-2.0 m + 1.2 m pod -> 2.3-3.0 m depth at every riffle
check("depth under ice low", ice.required_depth_under_ice(1.2, 1.2, 0), 2.30, 0.005)
check("depth under ice high", ice.required_depth_under_ice(2.0, 1.2, 0), 3.03, 0.005)
# genius/audit_final: 2-2.5 m lakes with 1.91-2.18 m ice keep 0-0.6 m water
check("water under ice", ice.water_under_ice(2.5, 2.0), 2.5 - 0.917 * 2.0, 1e-9)
check_true("backwater freezes to bed", ice.freezes_to_bed(1.5, 6500, 0.024))
check_true("deep pool stays liquid", not ice.freezes_to_bed(3.0, 6500, 0.024))
# round2/audit_b REVIEW: Glen A 2.4e-24 at 0 C: 0.44-2.2 MPa -> 1.8-222 %/day
check("Glen low", ice.glen_strain_rate(0.44e6) * DAY * 100, 1.77, 0.01)
check("Glen high", ice.glen_strain_rate(2.2e6) * DAY * 100, 221, 0.01)
# round2/erp2_b/idea4_out.txt: snow 250 kg/m3 under 20 kPa creeps 72.154 %/day (Vionnet 2012)
check("snow creep 250", 20e3 / ice.snow_viscosity(250) * DAY * 100, 72.154, 0.001)
# round2/audit_b REVIEW: 550 kg/m3 creep only 0.02-0.03 %/day
check("snow creep 550", 13e3 / ice.snow_viscosity(550) * DAY * 100, 0.0215, 0.02)
# round2/audit_b REVIEW: ice sealed at -35 C into 0 C water: E alpha dT/(1-nu) ~ 24 MPa
check("thermal shock", ice.thermal_shock_stress(35) / 1e6, 24.0, 0.005)
check_raises("ice alpha out of range", ice.ice_thickness, 5000, 0.1)
check_raises("Gold negative h", ice.gold_allowable_load, -1)
check_raises("Gold silly A", ice.gold_allowable_load, 1.0, 50)
check_raises("Sturm range", ice.snow_conductivity, 0.9)
check_raises("growth above 0", ice.ice_growth_rate, 1.0, 5)
check_raises("edge type", ice.edge_line_load_stress, 1e4, 1.0, edge="hinged")

# ====================================================================== geotech
yr = YR
# genius/audit_evo_2 REVIEW: Vyalov fits (1-2 MPa at 60 s, 0.2-0.5 MPa at 50 yr): failure at 0.58 MPa in 0.015-789 days
b1, B1 = geotech.vyalov_fit(1.0e6, 60, 0.2e6, 50 * yr)
b2, B2 = geotech.vyalov_fit(2.0e6, 60, 0.5e6, 50 * yr)
check("Vyalov fastest", geotech.vyalov_time_to_failure(0.58e6, b1, B1) / DAY, 0.0153, 0.01)
check("Vyalov slowest", geotech.vyalov_time_to_failure(0.58e6, b2, B2) / DAY, 789, 0.01)
check("Vyalov fit passes point", geotech.vyalov_strength(50 * yr, b2, B2), 0.5e6, 1e-9)
# genius/audit_evo_2 REVIEW: gamma 19 kN/m3, 25 m span: 0.59 MPa at 10 m cover, 0.20 at 30 m (fixed beam)
check("roof 10 m", geotech.beam_self_weight_stress(19e3, 25, 10) / 1e6, 0.59, 0.01)
check("roof 30 m", geotech.beam_self_weight_stress(19e3, 25, 30) / 1e6, 0.20, 0.02)
# genius/repair_evo_a LOG: spans to cave 11-28 m for long-term 0.2-0.5 MPa (h 6-15 m, rho 1900)
check("critical span low", geotech.critical_span(0.2e6, 1900 * 9.81, 6), 11.3, 0.01)
check("critical span high", geotech.critical_span(0.5e6, 1900 * 9.81, 15), 28.4, 0.01)
# genius/gate_r1_2: 20 kN/m3, 30 m, 80% extraction -> 3.0 MPa pillar stress
check("tributary pillar", geotech.pillar_tributary_stress(20e3, 30, 0.8) / 1e6, 3.0, 1e-9)
# genius/audit_evo_1 REVIEW: Mark-Bieniawski web SF 3.4/1.7/1.0 at 15/30/50 m (6.2 MPa coal, 0.6 m web, 1.8 m hole)
S = geotech.mark_bieniawski_strength(6.2, 0.6, 1.8)
for H, ref in ((15, 3.4), (30, 1.7), (50, 1.0)):
    check(f"web SF {H} m", S / (geotech.web_pillar_stress(25e3, H, 0.6, 1.8) / 1e6), ref, 0.02)
# textbook (dry cohesionless infinite slope): FS = tan(phi)/tan(beta) = tan30/tan20 = 1.586
check("infinite slope dry", geotech.infinite_slope_fs(0, 30, 18e3, 2, 20), math.tan(math.radians(30)) / math.tan(math.radians(20)), 1e-9)
# genius/audit_evo_1 REVIEW: thaw-consolidation threshold angles ~1.8 and ~6.4 deg
for gg, phi, R, ref in ((0.40, 25, 1.6, 1.75), (0.45, 33, 0.9, 6.37)):
    fs1 = lambda beta: geotech.thawing_slope_fs(0, phi, 16.5e3, gg * 16.5e3, 1.0, beta, R) - 1
    lo, hi = 0.1, 45.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if fs1(mid) > 0 else (lo, mid)
    check(f"thaw slope threshold {phi}/{R}", lo, ref, 0.02)
# genius/audit_evo_1 REVIEW: z_crit at 10 deg, c' 2 kPa, R 0.9 = 1.47 m
check("critical sheet", geotech.thawing_slope_critical_thickness(2e3, 28, 16.5e3, 0.45 * 16.5e3, 10, 0.9), 1.47, 0.005)
# genius/repair_evo_b/calc_idea2: 1.6 m thaw in 100 d, cv 1e-7 -> R 0.86
check("thaw consolidation ratio", geotech.thaw_consolidation_ratio(1.6, 100 * DAY, 1e-7), 0.86, 0.005)
# genius/audit_evo_1 REVIEW: Bingham 0.8-9 kPa, rho 1600, 4 deg -> 0.73-8.2 m; 500 Pa -> 0.46 m
check("Bingham 0.8 kPa", geotech.bingham_min_flow_thickness(800, 1600, 4), 0.73, 0.01)
check("Bingham 9 kPa", geotech.bingham_min_flow_thickness(9000, 1600, 4), 8.2, 0.01)
check("Bingham 500 Pa", geotech.bingham_min_flow_thickness(500, 1600, 4), 0.46, 0.01)
check("Bingham stop angle inverse", geotech.bingham_stop_angle(500, 1600, 0.4566), 4.0, 0.002)
# genius/audit_evo_1 REVIEW: t90 = 0.85 H^2/cv, 5 m, cv 0.5-2.8 m2/yr -> 7.6-41(42) yr
check("t90 fast", geotech.consolidation_t90(5, 2.8 / yr) / yr, 7.6, 0.01)
check("t90 slow", geotech.consolidation_t90(5, 0.5 / yr) / yr, 42.4, 0.01)
# SNiP 2.02.04-88 Raf (gate_6 S8): sand 0.20 MPa at -2 C, 0.26 at -3 C; clay (SP 25.13330, audit_evo_1): 60/100/200 kPa
check("adfreeze sand -2", geotech.adfreeze_strength(-2, "sand"), 200e3, 1e-9)
check("adfreeze sand -3", geotech.adfreeze_strength(-3, "sand"), 260e3, 1e-9)
check("adfreeze clay -0.5", geotech.adfreeze_strength(-0.5, "clay"), 60e3, 1e-9)
check("adfreeze clay -1", geotech.adfreeze_strength(-1, "clay"), 100e3, 1e-9)
check("adfreeze clay -3", geotech.adfreeze_strength(-3, "clay"), 200e3, 1e-9)
check("adfreeze interpolation", geotech.adfreeze_strength(-1.25, "clay"), 115e3, 1e-9)
# genius/audit_evo_1: anchor capacity scales with Raf: two anchors at -1 C give half the -3 C capacity
check("adfreeze capacity ratio", geotech.adfreeze_capacity(0.47, 6, -1) / geotech.adfreeze_capacity(0.47, 6, -3), 0.5, 1e-9)
# round2/critic_b: K 1e-3..1e-1 m/s, 8 m head, 75 m, 800 m2 -> 0.09-8.5 m3/s
check("Darcy low", geotech.darcy_seepage(1e-3, 8, 75, 800), 0.085, 0.01)
check("Darcy high", geotech.darcy_seepage(1e-1, 8, 75, 800), 8.5, 0.01)
# round2/audit_b REVIEW: 3 m skin x 3.5 m high, mu 0.5, 3 m head -> SF 2.4
check("sliding SF", geotech.sliding_fs(0.5, 3 * 3.5 * 20e3, geotech.hydrostatic_thrust(3)), 2.4, 0.01)
# genius/gate_7: 10.7 m thaw x strain 0.2 = 2.14 m settlement
check("thaw settlement", geotech.thaw_settlement(10.7, 0.2), 2.14, 1e-9)
check_raises("Vyalov wrong order", geotech.vyalov_fit, 0.5e6, 60, 1e6, 1e9)
check_raises("adfreeze out of table", geotech.adfreeze_strength, -8, "sand")
check_raises("adfreeze soil", geotech.adfreeze_strength, -2, "peat")
check_raises("extraction 1", geotech.pillar_tributary_stress, 20e3, 30, 1.0)
check_raises("slope beta 0", geotech.infinite_slope_fs, 0, 30, 18e3, 2, 0)
check_raises("beam support", geotech.beam_self_weight_stress, 19e3, 25, 10, "pinned")

# ====================================================================== hydro
# round2/rt_b LOG: toe channel 47 L/s, 0.6 m, S 0.05: tau 30 Pa, clasts < 42 mm; 100 L/s, 0.8 m, S 0.08: 57 Pa, < 78 mm
d1, R1, V1 = hydro.manning_depth_rect(0.047, 0.6, 0.05, 0.035)
t1 = hydro.bed_shear_stress(R1, 0.05)
check("toe tau", t1, 30, 0.02)
check("toe clast", hydro.critical_grain_size(t1) * 1000, 42, 0.01)
d2, R2, V2 = hydro.manning_depth_rect(0.10, 0.8, 0.08, 0.035)
check("toe2 clast", hydro.critical_grain_size(hydro.bed_shear_stress(R2, 0.08)) * 1000, 78, 0.01)
check("Manning continuity", d1 * 0.6 * V1, 0.047, 1e-6)
# round2/audit_b REVIEW: Lamb et al. 2008 theta_c = 0.071-0.080 at S 0.05-0.08
check("Lamb 0.05", hydro.critical_shields_slope(0.05), 0.071, 0.005)
check("Lamb 0.08", hydro.critical_shields_slope(0.08), 0.080, 0.005)
# Soulsby 1997: theta_c -> ~0.055 for coarse gravel (D* large)
check("Soulsby gravel", hydro.critical_shields_soulsby(0.05), 0.055, 0.02)
# round2/audit_b REVIEW: 47-100 L/s, S 0.05-0.08, d50 10-20 mm carries 28-610 m3/day (WP .. MPM)
_, Ra, _ = hydro.manning_depth_rect(0.047, 1.0, 0.05, 0.035)
check("bedload WP low", hydro.bedload_capacity(hydro.bed_shear_stress(Ra, 0.05), 0.02, theta_c=0.047) / 0.65 * DAY, 28, 0.03)
_, Rb, _ = hydro.manning_depth_rect(0.10, 1.0, 0.08, 0.035)
check("bedload MPM high", hydro.bedload_capacity(hydro.bed_shear_stress(Rb, 0.08), 0.01, method="mpm") / 0.65 * DAY, 610, 0.01)
check("bedload below threshold", hydro.bedload_capacity(1.0, 0.05), 0.0, atol=0)
# Rajaratnam 1976: submerged round jet u_c/u0 = K d/x (K ~6.2) beyond the core
check("jet decay", hydro.jet_centreline_velocity(15, 0.05, 3.0), 15 * 6.2 * 0.05 / 3.0, 1e-9)
check("jet core", hydro.jet_centreline_velocity(15, 0.05, 0.2), 15, 1e-12)
# genius/audit_evo_2: monitor working length 350-450 d -> 18-34 m for 50-75 mm nozzles
check("monitor length", hydro.monitor_working_length(0.075)[1], 33.75, 1e-9)
# genius/gate_2: 6 m3 water at 2 MPa per m3 ground, pump 0.7 -> 17.1 MJ/m3 (before engine efficiency)
check("pumping energy", hydro.pumping_power(6, 2e6 / (1000 * 9.81), 0.7) / 1e6, 17.14, 0.002)
# Pak 1959/Veselov 1956: hydro-elevator eta 0.17-0.35 -> power 3x a 0.75 centrifugal pump at eta 0.25
check("hydro-elevator x3", hydro.hydro_elevator_power(0.1, 20, 1000, 0.25) / hydro.pumping_power(0.1, 20, 0.75), 3.0, 1e-9)
# genius/audit_evo_1 REVIEW: 600 m3/h, 1.9 t/m3, 30% fines, 0.5% escape -> 0.48 kg/s; needs ~1,900 m3/s for +0.25 mg/L
m_f = hydro.fines_release_rate(600, 1.9, 0.30, 0.005)
check("fines release", m_f, 0.475, 0.002)
check("dilution flow", hydro.dilution_flow_required(m_f, 0.25), 1900, 0.002)
# genius/repair_evo_a LOG: 5% escape of 15% fines (300 m3/h, 120 d, 70%) -> +1.0..+2.6 mg/L at 800..300 m3/s
fines_rate = 300 * 24 * 120 * 0.7 * 1.8 * 1000 * 0.15 / (120 * DAY)
check("full mixing 300", hydro.full_mixing_increment(fines_rate * 0.05, 300), 2.6, 0.02)
check("full mixing 800", hydro.full_mixing_increment(fines_rate * 0.05, 800), 0.98, 0.02)
check("allowed escape", hydro.allowed_escape_fraction(0.25, 300, fines_rate / 0.15, 0.15), 0.0048, 0.02)
# HK EPD EIA targets: floating curtain alone 45% removal
check("silt curtain", hydro.silt_curtain_outside(10, 0.45), 5.5, 1e-9)
# Fischer et al. 1979: eps_y = 0.6 d u*; bank source fully mixed after 0.4 U W^2/eps_y
eps = hydro.transverse_mixing_coefficient(3, 0.05)
check("eps_y", eps, 0.09, 1e-9)
check("mixing length", hydro.mixing_length(0.3, 500, eps), 0.4 * 0.3 * 500 ** 2 / 0.09, 1e-9)
# round2/erp2_b, repair/b, rt_b: Froehlich 8,000 m3 at 3 m -> 34; 60,000 m3 at 6 m -> 144; 4,000/1.5 -> 11.6
check("Froehlich 8k", hydro.froehlich_peak_outflow(8000, 3), 34, 0.02)
check("Froehlich 60k", hydro.froehlich_peak_outflow(60000, 6), 144, 0.005)
check("Froehlich 4k", hydro.froehlich_peak_outflow(4000, 1.5), 11.6, 0.005)
# genius/gate_5: CEM U10 10, F 1 km -> Hm0 0.159 m, Tp 1.03 s, u_bed 0.0217 m/s at 1 m, 0.137 at 0.5 m
Hm, Tp = hydro.wave_growth_cem(10, 1000)
check("CEM Hm0", Hm, 0.159, 0.005)
check("CEM Tp", Tp, 1.03, 0.005)
check("orbital 1 m", hydro.wave_orbital_velocity(Hm, Tp, 1.0), 0.0217, 0.01)
check("orbital 0.5 m", hydro.wave_orbital_velocity(Hm, Tp, 0.5), 0.1374, 0.005)
# round2/critic_b: Hs 0.1, T 1.2 s, 1 m depth -> 0.032 m/s
check("orbital critic_b", hydro.wave_orbital_velocity(0.1, 1.2, 1.0), 0.032, 0.02)
# round2/audit_b REVIEW: drag-corrected settling in air: gold 10-20 um 0.06-0.24 m/s
check("settling gold 10 um", hydro.settling_velocity(10e-6, 19300), 0.064, 0.02)
check("settling gold 20 um", hydro.settling_velocity(20e-6, 19300), 0.24, 0.01)
# Stokes check in water: quartz 50 um: (2650-1000) g d^2/(18 mu) = 1.32 mm/s (Re << 1)
check("settling Stokes water", hydro.settling_velocity(50e-6, 2650, 1000, 1.7e-3), 1650 * 9.81 * 2.5e-9 / (18 * 1.7e-3), 0.02)  # Re 0.04: drag correction 1.6%
# round2/critic_b (Shao & Lu 2000): quartz 25 um 0.34, 500 um 0.35; gold minimum 0.37 m/s at 40 um (rho_air 1.35)
check("Shao-Lu quartz 25", hydro.aeolian_threshold_ustar(25e-6, 2650, 1.35), 0.34, 0.01)
check("Shao-Lu quartz 500", hydro.aeolian_threshold_ustar(500e-6, 2650, 1.35), 0.35, 0.01)
check("Shao-Lu gold 40", hydro.aeolian_threshold_ustar(40e-6, 19300, 1.35), 0.37, 0.01)
# genius/gate_6: Lena 0.6 m/s at 17,773 m3/s -> 0.29 m/s at 2,000 m3/s (m 0.34)
check("v from Q", hydro.velocity_from_discharge(0.6, 17773, 2000), 0.29, 0.02)
# genius/gate_3: 1,000 km2 x 80 mm/yr -> 2.535 m3/s
check("runoff", hydro.runoff_mean_discharge(1000, 80), 2.535, 0.002)
# genius/gate_3: Manning 12 m x 1.0 m lane, S 5e-4, n 0.035 -> 6.92 m3/s; gate_2 15 x 1.5, 1e-4, 0.03 -> 8.7
check("Manning Q gate_3", hydro.manning_discharge_rect(12, 1.0, 0.0005, 0.035), 6.918, 0.002)
check("Manning Q gate_2", hydro.manning_discharge_rect(15, 1.5, 1e-4, 0.03), 8.7, 0.005)
# genius/gate_2: ESPO 6.95 cSt at 20 C, Siberian Light slope -> 124 cSt at -57.8 C; friction 51 bar/15 km (+8.9 rise = 60)
B = hydro.walther_slope(11.28, 10, 5.81, 40)
nu_cold = hydro.walther_viscosity(6.95, 20, -57.8, B)
check("Walther -57.8", nu_cold, 124, 0.01)
check("pipe dP", hydro.pipe_pressure_drop(0.2e9 / 851 / (8760 * 3600), 0.1, 15000, 124e-6, 851 * (1 + 0.0008 * 77.8)) / 1e5, 51.1, 0.01)
check_raises("manning Q<=0", hydro.manning_depth_rect, 0, 1, 0.01)
check_raises("Lamb steep", hydro.critical_shields_slope, 0.5)
check_raises("bedload method", hydro.bedload_capacity, 30, 0.01, method="einstein")
check_raises("silt curtain 100%", hydro.silt_curtain_outside, 10, 1.0)
check_raises("settling buoyant", hydro.settling_velocity, 1e-4, 900, 1000, 1.7e-3)
check_raises("pipe transitional", hydro.pipe_pressure_drop, 0.00377, 0.1, 100, 1.6e-5, 900)  # Re ~3000
check_raises("hydro-elevator eta", hydro.hydro_elevator_power, 0.1, 20, 1300, 0.9)

# ====================================================================== naval
# genius/audit_evo_1 REVIEW: 130 x 14 x 3 m displaces 4.6-5.2 kt (Cb 0.85-0.95); payload ~1.6 kt at 2.2 m
check("displacement low", naval.displacement_t(130, 14, 3, 0.85), 4641, 0.001)
check("displacement high", naval.displacement_t(130, 14, 3, 0.95), 5187, 0.001)
check("payload at 2.2 m", naval.payload_at_draught(130, 14, 2.2, 2000, 0.9), 1604, 0.002)
check("draught inverse", naval.draught(naval.displacement_t(100, 20, 2.5, 0.9), 100, 20, 0.9), 2.5, 1e-9)
# genius/audit_evo_2 REVIEW: Awp 2,878 m2, 3 kt burned -> hull rises ~1.05 m
check("rise per tonne", 3000 * naval.rise_per_tonne(2878), 1.04, 0.01)
check("TPC", naval.tonnes_per_cm(2878), 28.78, 1e-9)
# genius/repair_final LOG: 8 kt hold 130x22 m -> 3.9 m; 2 kt 100x22 m -> 1.26 m
check("draft 8 kt", naval.draught_from_payload(8000, 130, 22), 3.88, 0.005)
check("draft 2 kt", naval.draught_from_payload(2000, 100, 22), 1.26, 0.005)
# genius/audit_evo_2 REVIEW: afloat bunker hull, 3.3 m loaded draught + 0.5 m -> ~3.8 m of water at winter low level
check("depth needed afloat", naval.depth_needed(3.3, 2.0, 0.5), 3.8, 1e-9)
# round2/critic_b: 1.2 m pod under 2.0 m ice -> 3.0 m (no clearance)
check("depth needed under ice", naval.depth_needed(1.2, 2.0, 0.0, under_ice=True), 3.03, 0.005)
# round2/critic_b: 39.3 m2 shell, 6 cm/45 d melt -> 4.35 kg/day buoyancy loss
check("melt buoyancy", naval.buoyancy_loss_from_melt(39.3, 0.06 / 45), 4.35, 0.005)
# round2/erp2_b: 5.4 m3 compressible air -> ~521 kg per metre of depth
check("air pocket", naval.air_buoyancy_change_per_m(5.4), 521, 0.01)
# round2/critic_b: 170 N drag at 0.16 m/s on 5.0x1.2 m implies Cd 2.21
check("drag", naval.drag_force(0.16, 6.0, 2.21), 170, 0.002)
# repair/b/out_idea4.txt: drag 26.2 N, mu 0.5 -> max net buoyancy 5.4 kg
check("max buoyancy", naval.max_buoyancy_to_slide(0.2, 1.31, 1.0, 0.5), 5.4, 0.015)
# genius/gate_8 results: 1 m3 pod +1% buoyant, Cd 0.85, A pi/4, mu 0.05 -> slide threshold 0.121 m/s
check("slide threshold", naval.slide_threshold_velocity(10.0, math.pi / 4, 0.85, 0.05), 0.121, 0.005)
check("net buoyancy", naval.net_buoyancy_kg(2.0, 1500), 500, 1e-9)
check_raises("Cb > 1", naval.displacement_t, 100, 20, 3, 1.2)
check_raises("negative melt", naval.buoyancy_loss_from_melt, 10, -0.1)

# ====================================================================== econ
# textbook annuity table: CRF(10%, 25 yr) = 0.11017; genius/rt_a: CRF(12%, 15) = 0.147
check("CRF 10/25", econ.crf(0.10, 25), 0.11017, 0.0005)
check("CRF 12/15", econ.crf(0.12, 15), 0.147, 0.002)
check("CRF r=0", econ.crf(0.0, 20), 0.05, 1e-12)
check("levelised", econ.levelised_cost(1e6, 5e4, 1e4, 0.10, 25), (1e6 * econ.crf(0.10, 25) + 5e4) / 1e4, 1e-12)
# round2/erp2_a LOG: anchor $960/t Ni extra vs $0.20/t-km winter road -> break-even 4,800 km
check("break-even", econ.breakeven_volume(960, 0.20), 4800, 1e-9)
# genius/audit_evo_1 REVIEW: $0.30/m3 carried 4-9 yr at 10-15% -> $0.44-1.06/m3
check("carry low", econ.carry_forward_cost(0.30, 0.10, 4), 0.44, 0.005)
check("carry high", econ.carry_forward_cost(0.30, 0.15, 9), 1.06, 0.005)
# round2/critic_b: 3-5 yr delay at 10-15% -> PV factor 0.75-0.50
check("delay PV", econ.delay_pv_factor(0.10, 3), 0.751, 0.002)
check("delay PV 5", econ.delay_pv_factor(0.15, 5), 0.497, 0.002)
check("inventory carry", econ.inventory_carry_cost(100, 0.14, 2), 29.96, 0.001)  # gate_5: 2 yr at 14% -> x0.2996
# genius/gate_9: free logistics share 8% -> ceiling 1.087
check("ceiling", econ.ceiling_ratio(0.08), 1.087, 0.001)
check("ratio", econ.ratio_vs_baseline(2550, 1700), 1.5, 1e-12)
# genius/gate_* verdict rule
check_true("verdict ALIVE", econ.gate_verdict(1.2, 1.6) == "ALIVE")
check_true("verdict DEAD margin", econ.gate_verdict(0.2, 3.0) == "DEAD")
check_true("verdict DEAD ratio", econ.gate_verdict(5.0, 1.05) == "DEAD")
check_true("verdict WOUNDED", econ.gate_verdict(0.6, 1.3) == "WOUNDED")
# round2/erp2_b: $2.01/m3 at 0.8 g/m3, 85% -> $2.95/g
check("cost per gram", econ.cost_per_recovered_unit(2.01, 0.8, 0.85), 2.95, 0.005)
# genius/gate_1 idea 8 expression: R_req = 0.85 var/(C - fixed) with ledger A shares -> 0.696
C_A = 2550.0
fixed_A = 0.22 * C_A
var_A = C_A - fixed_A - (C_A * 0.15 * 0.5 + C_A * 0.20 / 3)
check("parity recovery", econ.parity_recovery(0.85, C_A, fixed_A, var_A), 0.6956, 0.002)
# roast/roast.py: coal $100/t saving $74.6 -> 42.7%; SC6 $900 -> 7.7%
check("break-even loss coal", econ.breakeven_loss_fraction(0.117 * 700 - 7.3, 100), 0.427, 0.003)
check("break-even loss SC6", econ.breakeven_loss_fraction(0.117 * 700 - 7.3, 900), 0.077, 0.01)
# genius/audit_final REVIEW: 42-56 kt = 21-27% of 205 kt Arctic Yakutia utility coal
check("market share", econ.market_share(56e3, 205e3), 0.27, 0.02)
check("six-tenths", econ.six_tenths_scaling(100, 1, 2), 100 * 2 ** 0.6, 1e-12)
# genius/audit_evo_1 REVIEW: 60 kt at 33-40 t/h and 80-100% availability -> 62-95 days of augering
check("season days", 60000 / econ.season_capacity(40, 1, 24, 1.0), 62.5, 0.005)
check("window margin", econ.window_margin(60, 60000, 33 * 24 * 0.8), 60 / (60000 / (33 * 24 * 0.8)), 1e-12)
check("freight", econ.freight_cost(20, 300), 6000, 1e-12)  # ledger: 300 km winter road x 20 RUB/t-km
check("RUB->USD", econ.rub_to_usd(8400), 100, 1e-12)
check_raises("break-even never", econ.breakeven_volume, 100, 1, 2)
check_raises("recovery > 1", econ.cost_per_recovered_unit, 2, 1, 1.5)
check_raises("crf n=0", econ.crf, 0.1, 0)
check_raises("ceiling share 1", econ.ceiling_ratio, 1.0)

# ====================================================================== stats
# Garwood exact Poisson: n=5 -> (1.6235, 11.6683) (standard tables); genius/audit_evo_1: 0.32-2.3x
lo, hi = stats.poisson_ci(5)
check("Poisson low", lo, 1.6235, 0.001)
check("Poisson high", hi, 11.6683, 0.001)
check("Poisson zero", stats.poisson_ci(0)[1], 3.6889, 0.001)  # tables: 0 events -> upper 3.689
check("Poisson 10", stats.poisson_ci(10)[0], 4.7954, 0.001)
# roast/roast.py: zero losses in 20/59/299 pods -> p < 13.9% / 5.0% / 1.0%
check("zero-failure 20", stats.zero_failure_upper_bound(20), 0.139, 0.005)
check("zero-failure 59", stats.zero_failure_upper_bound(59), 0.050, 0.02)
check("zero-failure 299", stats.zero_failure_upper_bound(299), 0.010, 0.01)
check("trials for 5%", stats.trials_for_zero_failure(0.05), 59, atol=0)
check("trials for 1%", stats.trials_for_zero_failure(0.01), 299, atol=0)
check("rule of three", stats.rule_of_three(60), 0.05, 1e-12)
# round2/critic_b: grade CV 0.6-1.0, 5% at 2 sigma -> 576-1,600 samples
check("n mean low", stats.sample_size_mean(0.6, 0.05, 2), 576, 0.001)
check("n mean high", stats.sample_size_mean(1.0, 0.05, 2), 1600, 0.001)
# genius/audit_final REVIEW: CV 0.3-0.5, 1.16x at 95%/80% -> 64-178 per arm
check("two arms low", stats.sample_size_two_arms(0.3, 1.16), 64, 0.01)
check("two arms high", stats.sample_size_two_arms(0.5, 1.16), 178, 0.01)
# round2/critic_b: 5% loss +/- 2% -> 456 pods; round2/audit_a: 45% split +/- 3 points -> ~1,000 grains
check("proportion 5%", stats.sample_size_proportion(0.05, 0.02), 456, 0.002)
check("proportion 45%", stats.sample_size_proportion(0.45, 0.03), 1056, 0.002)
check("counts", stats.counts_for_precision(0.05), 1600, 1e-12)
# round2/audit_a: 8 random-polarity stages all right: 0.5^8 = 0.4%
check("all succeed", stats.all_succeed(0.5, 8), 0.0039, 0.01)
check("normal ppf", stats.normal_ppf(0.975), 1.95996, 1e-5)
check_raises("Poisson negative", stats.poisson_ci, -1)
check_raises("zero-failure n=0", stats.zero_failure_upper_bound, 0)
check_raises("two arms ratio 1", stats.sample_size_two_arms, 0.3, 1.0)

# ====================================================================== data integrity
bad = [k for k, d in data.DATA.items()
       if not (isinstance(d.source, str) and len(d.source) > 5 and isinstance(d.unit, str) and d.unit)]
check_true(f"every data entry has a source and unit (bad: {bad})", not bad)
bad_m = [k for k, d in data.DATA.items() if k.endswith((".monthly", ".summer")) and not set(d.value) <= set(data.MONTHS)]
check_true(f"monthly normals use month keys (bad: {bad_m})", not bad_m)
check("data FX", data.get("price.fx_rub_usd"), 84.0, 1e-12)
check("data lo_hi", data.lo_hi("river.lena_delta_under_ice_velocity_main")[1], 0.18, 1e-12)
check_true("data find", "limit.fishery_ss_increment_high" in data.find("fishery"))
try:
    data.get("no.such.key")
    check_true("data missing key raises", False)
except KeyError:
    check_true("data missing key raises", True)

if FAIL:
    print(f"FAILED {len(FAIL)} of {N} checks:")
    for f in FAIL:
        print("  " + f)
    sys.exit(1)
print(f"OK kit: {N} checks")
