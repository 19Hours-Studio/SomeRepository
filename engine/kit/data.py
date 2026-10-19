"""Sourced data for screening Arctic / permafrost resource ideas (Yakutia, Magadan, Chukotka, Siberia).

Every entry is a ``Datum(value, unit, source, note)``.  ``value`` is a float, a ``(low, high)`` tuple for a
range, or a dict (monthly normals, tables).  ``source`` names the primary reference as the harvested scripts
gave it, followed by the harvest location ``[run/...]`` under engine/runs/permafrost/.  ``note`` carries the
caveat that matters for screening (assumption flags, disagreements, validity).

Tags used in sources: [S] sourced by a web search in that run, [L] from the run's value ledger (genius/ledger),
[E]/[est]/[A] an engineering estimate in that run (treat as soft), [REF] textbook value.

Usage::

    from kit import data
    data.get("ice.gold_A_safe")          # -> 3.5
    data.lo_hi("river.lena_delta_under_ice_velocity_main")   # -> (0.12, 0.18)
    data.info("price.winter_road_rub_tkm")                     # full Datum
    data.find("fishery")                                       # keys containing text
    data.MONTHS, data.monthly("Verkhoyansk")                   # monthly normals dict
"""
from collections import namedtuple

Datum = namedtuple("Datum", "value unit source note")


def _d(value, unit, source, note=""):
    return Datum(value, unit, source, note)


MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
MONTH_DAYS = dict(zip(MONTHS, (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)))

# ---------------------------------------------------------------- physical constants (plain floats)
G = 9.81                 # m/s2
RHO_W = 1000.0           # kg/m3 fresh water
RHO_SEA = 1025.0         # kg/m3 sea water
RHO_ICE = 917.0          # kg/m3
L_FUSION = 334e3         # J/kg
L_SUBLIMATION = 2.834e6  # J/kg
L_VAPOUR = 2.5e6         # J/kg (near 0 C)
C_W_VOL = 4.18e6         # J/m3/K water
CP_AIR = 1005.0          # J/kg/K
K_ICE = 2.2              # W/m/K
K_WATER = 0.57           # W/m/K near 0-5 C
SIGMA_SB = 5.670374e-8   # W/m2/K4
R_GAS = 8.314            # J/mol/K
KAPPA = 0.4              # von Karman
EPS0 = 8.854e-12         # F/m
G_PER_OZ = 31.1035

DATA = {
    # ------------------------------------------------------------ constants with provenance
    "const.rho_ice": _d(917.0, "kg/m3", "[REF] CRC; used in every harvested script"),
    "const.latent_fusion": _d(334e3, "J/kg", "[REF] CRC; all scripts"),
    "const.latent_ice_per_m3": _d(306e6, "J/m3 of ice", "917 x 334e3 [round2/audit_b/c1_dam.py]"),
    "const.latent_sublimation": _d(2.834e6, "J/kg", "[REF] used in round2/critic_b, rt_b, repair/b"),
    "const.k_ice": _d(2.2, "W/m/K", "[REF] round2/audit_b/c5_ice.py, audit_final"),
    "const.k_snow_settled": _d((0.1, 0.35), "W/m/K", "Sturm 1997 k=0.138-1.01rho+3.233rho^2 (rho g/cm3) [genius/gate_9]",
                               "0.3 used for fresh-ish snow in round2/audit_b/c5_ice.py"),
    "const.c_frozen_gravel_vol": _d((1.6e6, 2.0e6), "J/m3/K", "[REF] Andersland & Ladanyi typical; round2/audit_b, erp2_b",
                                    "1.8-2.0e6 most used"),
    "const.k_thawed_silt": _d((1.2, 1.5), "W/m/K", "[REF] genius/repair_evo_b/calc_idea2.py, audit_evo_1 (1.3)"),
    "const.k_frozen_gravel": _d((2.0, 2.8), "W/m/K", "[REF] genius/repair_evo_a/idea1.py (kf 2.8), audit_evo_2 (2.0)"),
    "const.k_peat_saturated": _d(0.5, "W/m/K", "[REF] round2/audit_b/c1_dam.py, repair/b"),
    "const.diesel_lhv": _d((35.8e6, 36.0e6), "J/l", "[REF] genius/gate_2 (35.8), repair_final (36)"),
    "const.diesel_genset_l_per_kwh": _d(0.27, "l/kWh", "[E] genius/ledger/ledger_calc.py"),
    "const.ni_co4_idlh_ppm": _d(2.0, "ppm", "NIOSH NPG 0444 [round2/audit_a/calc_carbonyl.py]"),

    # ------------------------------------------------------------ climate: monthly normals (deg C)
    "climate.Verkhoyansk.monthly": _d(dict(zip(MONTHS, (-45.3, -41.6, -29.6, -12.4, 3.7, 13.2, 16.4, 11.5, 2.6,
                                                         -14.3, -34.7, -43.4))), "C",
                                      "Wikipedia climate table via search [genius/audit_final/audit_calc.py]",
                                      "FDD from these monthly means ~6,690 C*d"),
    "climate.Udachny.monthly": _d({"Oct": -12.0, "Nov": -29.8, "Dec": -36.0, "Jan": -39.4, "Feb": -35.2,
                                   "Mar": -24.3, "Apr": -11.0}, "C",
                                  "Wikipedia/climate-data.org via search [round2/critic_a/calc/climate_hours.py]",
                                  "Oct and Apr assumed [E]; Jan -39.4 sourced (repair/a S14)"),
    "climate.Chara.monthly": _d({"Nov": -21.0, "Dec": -31.1, "Jan": -31.8, "Feb": -26.3, "Mar": -16.2}, "C",
                                "Jan -31.8 Wikipedia via search [round2/rt_a/calc/idea2.py]",
                                "Chara = Udokan SX-EW site; months other than Jan not sourced"),
    "climate.Yakutsk.monthly": _d({"Nov": -27.0, "Dec": -36.5, "Jan": -38.6, "Feb": -32.5, "Mar": -20.1,
                                   "May": 7.5, "Jun": 16.4, "Jul": 19.5, "Aug": 15.2, "Sep": 6.1}, "C",
                                  "kupi.com / weather compilations [round2/erp2_a/NOTES.md; genius/gate_4]",
                                  "Nov and Mar from memory in erp2_a; Feb given as -31..-34"),
    "climate.Pevek.monthly": _d({"Mar": -21.4, "Apr": -14.3, "May": -2.2}, "C",
                                "Wikipedia climate table [round2/erp2_b/NOTES.md]",
                                "May mean daily max +1.0 C: dark gravel melts from ~28 Apr"),
    "climate.Tiksi.monthly": _d({"Mar": -27.0, "Apr": -19.5, "May": -7.6}, "C",
                                "Wikipedia/pogoda.ru [round2/rt_b/calc_idea1.py]",
                                "DISAGREES: round2/critic_b gives May mean -4.1; April mean daily max ~-11"),
    "climate.Susuman.summer": _d({"Jul": 14.9, "Aug": 10.9}, "C",
                                 "weatherapi/Wikipedia [genius/audit_evo_2/check5.py]", "MAAT -11.5 C (gate_6)"),
    "climate.Susuman.maat": _d(-11.5, "C", "Wikipedia Susuman [genius/gate_6/gate6_calc.py S18]",
                               "annual amplitude ~26.5 K used in gate_6 sine model"),
    "climate.Chokurdakh.summer": _d({"May": -4.9, "Jun": 6.7, "Jul": 10.6, "Aug": 8.1, "Sep": 1.6}, "C",
                                    "climate tables via search [genius/audit_final/audit_calc.py]",
                                    "only 51 days with mean >8 C (heating needed in summer)"),
    "climate.Srednekolymsk.summer": _d({"Jun": 11.2, "Jul": 13.9, "Aug": 10.1, "Sep": 3.2}, "C",
                                       "climate tables via search [genius/audit_final/audit_calc.py]",
                                       "May -1..+1 C; 78-80 days with mean >8 C"),
    "climate.Norilsk.summer": _d({"Jun": 6.0, "Jul": 14.4, "Aug": 10.0, "Sep": 3.0}, "C",
                                 "climate-zone.com; kupi.com Jul 13.8 [genius/gate_4/work/gate4_calcs.py]"),
    "climate.upper_Kolyma_typical.monthly": _d({"Oct": -12, "Nov": -27, "Dec": -33, "Jan": -35, "Feb": -32,
                                                "Mar": -24, "Apr": -12, "May": -1}, "C",
                                               "[E] Bilibino/Seymchan-like normals [round2/erp2_b/idea3_icefloat.py]",
                                               "gives FDD ~5,100 C*d"),
    "climate.hourly_sd_within_month": _d((5.0, 8.0), "K",
                                         "[E] used for hours-below-threshold estimates [round2/critic_a, rt_a, erp2_a]",
                                         "hourly station data were unreachable; result sensitive (x2) to this SD"),
    "climate.fdd_kolyma_yana_valleys": _d((5000, 6500), "C*d", "[E] genius/repair_final/calc.py",
                                          "Verkhoyansk ~6,690 from normals"),
    "climate.fdd_tiksi": _d(5500, "C*d", "[REF] textbook [genius/repair_evo_b/calc_idea1.py]"),
    "climate.fdd_yakutia_range": _d((4500, 7000), "C*d", "[REF] genius/repair_evo_b/calc_idea4.py"),
    "climate.thawing_index_N_Yakutia": _d((1600, 1800), "C*d", "[REF] Batagay/Deputatsky [genius/repair_evo_b/calc_idea2.py]"),
    "climate.hours_le_minus45_Udachny": _d((142, 375), "h/yr", "normal model on monthly means [round2/critic_a]",
                                           "~273 h central estimate"),
    "climate.hours_le_minus35_Yakutsk": _d(1460, "h/yr", "normal model [round2/audit_a/calc_vitriol.py]"),
    "climate.ghi_Yakutsk_MJm2_month": _d({"May": 565.6, "Jun": 632.7, "Jul": 603.4, "Aug": 444.1, "Sep": 276.5},
                                         "MJ/m2/month", "SNiP climatology Table 17 (dnaop.com/html/66253_7.html) [genius/gate_8]"),
    "climate.ghi_Oymyakon_Jul": _d(611.7, "MJ/m2/month", "dnaop.com/html/66253_7.html [round2/audit_b/c2_toe.py]",
                                   "= 228 W/m2 mean; May and Sep much lower"),
    "climate.kirensk_record_low": _d(-57.8, "C", "Wikipedia Kirensk [genius/gate_2]"),
    "climate.tundra_snowpack": _d((0.35, 0.30), "m depth, g/cm3",
                                  "UNESCO Indigirka tentative list [round2/critic_b]",
                                  "~105 mm w.e.; snow-off late May-early June (NOAA Barrow)"),
    "climate.spring_snowfall_Pevek": _d(10.0, "mm w.e.", "[round2/erp2_b] 2-3 wet days/month (kupi.com)",
                                        "same size as a whole spring sublimation budget"),
    "climate.tundra_sublimation": _d((0.06, 0.15), "mm w.e./day", "North Slope eddy covariance; tc-2023-153 [round2/erp2_b; gate_4]",
                                     "Siberian midwinter 0.01-0.05 mm/d (repair/b)"),
    "climate.wind_pevek_yuzhak": _d((40, 60), "m/s gusts", "bigenc.ru Pevek yuzhak [round2/audit_b]"),
    "climate.upper_kolyma_ground_temp": _d((-3.8, -0.1), "C", "Kriosfera Zemli 2024 [genius/audit_evo_2]",
                                           "warm permafrost: backfill freezes slowly"),
    "climate.anadyr_precip": _d(0.346, "m/yr", "bigenc.ru [genius/gate_7/calc.py]"),

    # ------------------------------------------------------------ ice
    "ice.gold_A_safe": _d(3.5, "kg/cm2", "Gold 1971; Wikipedia Ice road; tac-atc.ca barrette.pdf [genius/gate_7, gate_9]",
                          "P[kg] = A h[cm]^2; lower-bound (safe) value for moving/short-parked loads"),
    "ice.gold_A_short_term": _d(7.0, "kg/cm2", "Gold 1971 upper/short-term; Finnish tests [genius/gate_7]",
                                "recommended A range 3.5-10 kg/cm2"),
    "ice.parking_limit_h": _d(2.0, "h", "Gold 1971 / ice-road guidance (Wikipedia Ice road)",
                              "longer stationary loads creep: engineering analysis required"),
    "ice.crossing_flooded_layer_factor": _d(0.65, "-", "Russian ice-crossing rule h_eff = h_nat + 0.65 h_flooded [genius/gate_7]"),
    "ice.alpha_snow_free_windy": _d(0.027, "m/(C*d)^0.5", "[REF] Michel 1971 / Lepparanta [genius/audit_final, repair_evo_b]"),
    "ice.alpha_snow_covered": _d((0.017, 0.024), "m/(C*d)^0.5", "[REF] Michel 1971 [genius/repair_final/calc.py]"),
    "ice.alpha_lake_typical": _d((0.020, 0.027), "m/(C*d)^0.5", "Stefan/Ashton, Michel 1971 [round2/erp2_b NOTES]",
                                 "a=2.4 cm/(C d)^0.5 typical for snow-covered lakes"),
    "ice.flexural_strength": _d((0.5, 1.0), "MPa", "[REF] round2/audit_b/c3_pods.py; repair_evo_a (0.5-0.8)"),
    "ice.tensile_strength": _d((1.0, 3.0), "MPa", "[REF] round2/audit_b c3_pods (2-3); King & Fletcher thermal shock"),
    "ice.youngs_modulus_sheet": _d((2e9, 5e9), "Pa", "[REF] effective E of river/lake ice sheet [round2/audit_b/c5_ice.py]"),
    "ice.glen_A_0C": _d(2.4e-24, "Pa^-3/s", "Glen law n=3 at 0 C [round2/audit_b/c6_pod8.py]"),
    "ice.thermal_expansion": _d(5.1e-5, "1/K", "[REF] round2/audit_b/c3_pods.py"),
    "ice.friction_ice_ice": _d((0.15, 0.76), "-", "arXiv 1502.04173 [genius/gate_6]",
                               "0.5 near melting, slow, with hold time (round2/audit_b, repair/b)"),
    "ice.friction_hull_ice": _d((0.02, 0.47), "-", "Vance 1980 Katmai Bay via MDPI Lubricants 11:314 [genius/gate_8]"),
    "ice.lena_tabaga_end_winter": _d((1.2, 1.4), "m", "MSU Lomonosov-2017 [genius/gate_7]"),
    "ice.arctic_tundra_rivers_max": _d((1.5, 2.0), "m", "E3S Conf 163:05003 (2020) [genius/gate_9]"),
    "ice.kolyma_river": _d((0.8, 1.3), "m", "BRE Kolyma [genius/repair_evo_a/idea1.py]"),
    "ice.upper_kolyma_end_winter": _d((1.05, 2.5), "m", "water-rf.ru [genius/audit_evo_1]"),
    "ice.lake_ice_lena_delta": _d((1.5, 2.0), "m", "Russian lake summary [repair/b; genius/repair_final S2]"),
    "ice.landfast_sea_ice_laptev": _d(2.0, "m", "FI 5,500 C*d [genius/repair_evo_b]",
                                      "breakup July; midseason breakouts by cyclones (EGUsphere-2026-826)"),
    "ice.under_cover_deposition_velocity": _d((0.61, 0.8), "m/s",
                                              "Kivisild (Fr 0.08) 0.61, MacLachlan 0.69, IAHR 1986 0.8; MDPI Water 15:4242 [round2/audit_b]",
                                              "frazil deposits (hanging dams) below this mean velocity"),
    "ice.water_ice_C_w": _d(1622.0, "W s^0.8 m^-2.6 K^-1", "Ashton 1986 h=C_w U^0.8/D^0.2 [round2/critic_b/calc_extra.py]"),
    "ice.water_temp_under_lena_delta_ice": _d((-0.1, 0.8), "C", "Fedorova et al. 2020 E3S 163:05003 [roast/roast.py]"),
    "ice.basal_growth_under_1_1p8m": _d((0.01, 0.019), "m/day", "Stefan at -30 C surface [repair/b out_idea4]",
                                        "a stopped object is frozen in within hours-days"),
    "ice.krasnoyarsk_tailwater_open": _d((200, 300), "km", "Wikipedia Krasnoyarsk Dam [round2/audit_b]",
                                         "warm releases: polynya + frazil below dams"),

    # ------------------------------------------------------------ rivers, seasons, depths
    "river.lena_delta_under_ice_velocity_main": _d((0.12, 0.18), "m/s", "Fedorova et al. 2020, E3S 163:05003 [genius/gate_8 S1]"),
    "river.lena_delta_under_ice_velocity_bykovskaya": _d((0.20, 0.25), "m/s", "Fedorova et al. 2020 [genius/gate_8]"),
    "river.lena_delta_under_ice_velocity_olenek": _d((0.05, 0.11), "m/s", "Fedorova et al. 2020 [genius/gate_8]"),
    "river.lena_mean_velocity_lower": _d((0.5, 0.7), "m/s", "booksite.ru BSE [genius/gate_6 S9]"),
    "river.lena_kyusyur_mean_Q": _d(17773.0, "m3/s", "Wikipedia Lena [genius/gate_6 S10]"),
    "river.lena_kyusyur_winter_Q": _d((1378.0, 2814.0), "m3/s", "hess-2016-254 [genius/gate_6 S11]"),
    "river.velocity_discharge_exponent": _d(0.34, "-", "Leopold & Maddock v~Q^m [genius/gate_6]"),
    "river.kolyma_runoff": _d((123e9, 643e9), "m3/yr, m2", "BSE Kolyma [genius/gate_5]", "~190 mm/yr, 47% snow-fed"),
    "river.kolyma_april_to_annual_Q": _d(0.052, "-", "GRDC Kolymskaya 162.7/3109 m3/s [genius/gate_4]",
                                         "small streams freeze to the bed"),
    "river.kolyma_srednekolymsk_winter_Q": _d((61.0, 127.0), "m3/s", "GRDC monthly means P2998500 [genius/gate_8 S3]",
                                              "DISAGREES with ~327 m3/s derived in round2/rt_b from Majhi 2007 "
                                              "post-dam increments (+130..268 m3/s); GRDC is measured, take it unless "
                                              "post-1980 data are confirmed"),
    "river.kolyma_natural_april_min": _d(23.5, "m3/s", "bigenc.ru Kolyma [round2/audit_b]"),
    "river.chukotka_low_water_specific_Q": _d(10.0, "L/s/km2", "Lomonosov Geogr. J. 2023 [genius/gate_3]"),
    "river.central_yakutia_runoff": _d((1.0, 80.0), "mm/yr", "EGU2020-1095 (1-15), EGU2018-16001 (wettest 80) [genius/gate_3]"),
    "river.kolyma_main_stem_summer_T": _d((10.0, 15.0), "C", "BSE (dic.academic.ru) [genius/gate_8 S18]"),
    "river.small_stream_T_penalty": _d(4.7, "K colder", "Samokhvalov & Ukhov 2018 (order I-II vs VI-VII) [round2/critic_b]"),
    "river.guaranteed_depth_lena": _d({"Ust-Kut-Vitim": 2.2, "Sinsk-Yakutsk": 2.6, "Yakutsk-Zhigansk": 2.9,
                                       "Arctic Lena-basin reaches": 2.0, "upper Lena low water": 1.0}, "m",
                                      "Mintrans notices 2025-2026 [genius/audit_evo_1, gate_r1_2, gate_7]",
                                      "only 3,558 km of >16,000 km Lena-basin network has guaranteed dimensions"),
    "river.yana_indigirka_low_water_depth": _d((1.5, 2.0), "m", "yk24.ru 2025 [genius/repair_final S12]",
                                               "coal moved to winter road because rivers too shallow"),
    "river.lena_flood_rise": _d((9.0, 15.0), "m", "Britannica [genius/audit_evo_2]"),
    "river.kolyma_stage_range": _d(14.0, "m", "BRE [genius/audit_evo_1]"),
    "river.yana_verkhoyansk_frozen_to_bed": _d((70, 110), "days/yr", "[genius/audit_evo_2]"),
    "river.kolyma_ice_cover_days": _d(200, "days", "BRE [genius/repair_evo_a/idea1.py]"),
    "river.open_water_season_days": _d((110, 120), "days", "[E] genius/repair_final (110 nav, 60 mining), repair_evo_a (120)"),
    "river.navigation_end_zyryanka_srednekolymsk": _d("10 Oct", "date", "neftegaz.ru northern delivery [round2/audit_b]"),
    "river.kolyma_reservoir_levels": _d({"NPU": 451.5, "UMO": 432.0, "FPU": 457.6}, "m a.s.l.",
                                        "RusHydro [genius/audit_evo_1]", "19.5 m seasonal rise; filled 1980-1994"),
    "river.kolyma_reservoir_volume_area": _d((14.56e9, 441e6), "m3, m2", "[genius/gate_r1_1] mean depth 33 m"),
    "river.dredge_season_far_north": _d((160, 180), "days", "Nafikov SFU dissertation [genius/repair_final S9]",
                                        "Urals/W Siberia 340-350 d (Mining Encyclopedia)"),

    # ------------------------------------------------------------ ground
    "ground.adfreeze_note": _d(None, "-", "SNiP 2.02.04-88 / SP 25.13330 Raf tables (dnaop.com/html/31372_5.html)",
                               "see geotech.adfreeze_strength; lab tests per GOST 12248.8-2020 for design"),
    "ground.frozen_sandy_gravel_ucs": _d((5.0, 8.0), "MPa", "[REF] Tsytovich at -4 C [genius/repair_evo_b/calc_idea3.py]",
                                         "long-term ~1/3-1/4 of short-term"),
    "ground.frozen_gravel_long_term": _d((1.25, 2.0), "MPa", "[E] genius/gate_r1_2 (1.25 at -3..-5 C), repair_evo_b (1.5-2)",
                                         "CRREL permafrost tunnel creep and roof fall (Bjella 2008)"),
    "ground.frozen_overburden_tensile": _d({"long_term": (0.2, 0.5), "short_term": (1.0, 2.0)}, "MPa",
                                           "[E] genius/repair_evo_a/idea2.py; audit_evo_2"),
    "ground.thawed_undrained_strength": _d((0.8, 9.0), "kPa", "Harris et al. 1995 PPP 6:293 [genius/audit_evo_1]"),
    "ground.cv_thawed_ice_rich_silt": _d((1e-8, 1e-6), "m2/s", "[REF] genius/repair_evo_b/calc_idea2.py"),
    "ground.yedoma_ice_content": _d((0.65, 0.90), "vol fraction", "epic.awi.de 35773 [genius/gate_2]"),
    "ground.fine_permafrost_ice": _d((0.30, 0.90), "vol fraction", "USGS Bull 1083A (Black) [genius/gate_2]"),
    "ground.thaw_subsidence_yedoma_lakes": _d((0.062, 0.15), "m/yr", "Ulrich et al. 2017; Fedorov & Konstantinov max [genius/gate_4]"),
    "ground.batagay_headwall_retreat": _d((5.0, 15.0), "m/yr", "Kizyakov et al. 2024 [genius/repair_evo_b]"),
    "ground.lake_talik_measured": _d({"TEM thermokarst lake": 91.0, "model": 80.0, "Yakutian lake": 25.0,
                                      "Yukechi 2015 coring": 12.0}, "m",
                                     "Creighton 2018; SPbU; Yukechi coring [genius/repair_final, audit_final]"),
    "ground.subsea_permafrost_buor_khaya": _d((24.75, 0.035), "m below seabed at 750-800 m offshore; m/yr degradation",
                                              "Overduin et al. 2015 [genius/audit_evo_2, repair_evo_b]",
                                              "coast retreat 1-2 m/yr"),
    "ground.excavator_frozen_dig_depth": _d(0.25, "m", "dnaop.com/html/45827_6.html [genius/gate_9]",
                                            "excavators dig frozen ground without pre-loosening only to ~0.25 m"),
    "ground.sandy_gravel_phi": _d((33, 40), "deg", "geotechdata.info (loose 35) [genius/gate_6]"),

    # ------------------------------------------------------------ prices and costs (2026 unless stated)
    "price.fx_rub_usd": _d(84.0, "RUB/USD", "[L] CBR early Oct 2026 83.2-85.5 [genius/ledger]",
                           "other runs used 85-90; use 84"),
    "price.diesel_exchange_rub_l": _d(64.8, "RUB/l", "[L] exchange 77,177 RUB/t, 15 Jun 2026 [genius/ledger]"),
    "price.diesel_site_rub_l": _d((120.0, 150.0), "RUB/l", "[L] Yakutia retail 122.99 RUB/l 12 Oct 2026 [genius/ledger]",
                                  "delivered remote site; ~$1.4-1.8/l"),
    "price.power_mine_diesel": _d(0.49, "USD/kWh", "[L] 0.27 l/kWh x 130 RUB/l + 6 RUB/kWh = ~41 RUB/kWh [genius/ledger]",
                                  "DISAGREES with $0.15 (round2/audit_a) and $0.30 (erp2_a, rt_a); isolated Far-North "
                                  "diesel 10-40 RUB/kWh (ipolytech, repair/a S7). Ledger is newest and itemised"),
    "price.power_fnpp_rub_kwh": _d(6.45, "RUB/kWh (2020)", "[L] Baimskaya floating NPP [genius/ledger]", "x1.51 CPI to 2026"),
    "price.power_grid_hydro": _d((0.05, 0.08), "USD/kWh", "Udachny/Vilyuy-Svetlinskaya grid [round2/audit_a]",
                                 "Udokan has 50 MW grid substation + 146 MW building (critic_a)"),
    "price.winter_road_rub_tkm": _d(20.0, "RUB/t-km", "[L][S] ledger cross-cutting [genius/ledger, gate_3]",
                                    "= $0.24/t-km. Other runs: $0.118 (round2/audit_b), $0.117 (repair/b), "
                                    "$0.15-0.20 unsourced (erp2_a), $0.177 model (erp2_b)"),
    "price.river_barge_rub_tkm": _d((3.0, 5.0), "RUB/t-km", "[L] LORP [genius/ledger, gate_2]",
                                    "repair_final: 'the ideas' own figure, not verified'"),
    "price.lorp_seasonal_haul_rub_t": _d(8000.0, "RUB/t", "[L] LORP 2025 revenue/tonnes [genius/ledger]"),
    "price.nsr_general_cargo_rub_t": _d((15000.0, 17000.0), "RUB/t", "[L] genius/gate_1, gate_5"),
    "price.summer_barge_usd_tkm": _d((0.025, 0.03), "USD/t-km", "[E] round2/erp2_b NOTES, repair/b", "assumption"),
    "price.truck_usd_tkm": _d((0.037, 0.10), "USD/t-km", "[E] repair/b (0.037), erp2_a (0.10)"),
    "price.rail_rzd_rub_tkm": _d(3.9, "RUB/t-km", "[E] genius/gate_6 (assumed tariff)"),
    "price.settlement_coal_at_boiler": _d(23000.0, "RUB/t", "[L] archetype C2 [genius/ledger]",
                                          "logistics 85%; E3S 2020: delivered coal 3.5-25 kRUB/t"),
    "price.kolyma_depot_coal": _d(6962.0, "RUB/t", "ZhKKh tender 701.57 MRUB/100,778 t (saby.ru) [genius/repair_final S11]"),
    "price.export_coal_fob": _d(83.0, "USD/t", "[L] archetype C1 delivered cost; price $106 [genius/ledger]"),
    "price.gold": _d(4150.0, "USD/oz", "[L] genius/ledger"),
    "price.placer_gold_delivered_cost": _d(2550.0, "USD/oz", "[L] archetype A (6,900 RUB/g) [genius/ledger]",
                                           "shares: energy .10 labour .20 inbound .12 outbound .002 processing .20 "
                                           "capital .15 other .22; earthmoving ~2/3 of physical cost; 11 l diesel/g"),
    "price.copper_conc_delivered_cost": _d(8500.0, "USD/t Cu", "[L] archetype B Baimskaya [genius/ledger]",
                                           "capital 41%; Cu price $13,980"),
    "price.lce_delivered_cost": _d(10200.0, "USD/t LCE", "[L] archetype D Kolmozerskoye [genius/ledger]",
                                   "capital 42%; LCE price $19,750"),
    "price.lithium_lce": _d(20000.0, "USD/t LCE", "Benchmark Sept 2026 [round2/audit_a]"),
    "price.nickel_lme": _d(17000.0, "USD/t", "LME Aug 2026 (yieh.com) [genius/gate_6]"),
    "price.tin": _d(30066.0, "USD/t", "World Bank 2024 average [genius/repair_evo_b]"),
    "price.cbr_key_rate": _d(0.14, "1/yr", "CBR Sep 2026 [genius/gate_5]"),
    "price.capital_charge_ledger": _d(0.124, "1/yr", "ledger B: $3,485/t vs $28k per annual t [genius/gate_4]"),
    "price.mining_wage_rub_month": _d(155.6e3, "RUB/month", "end-2024 average mining wage [genius/audit_final]",
                                      "x1.3 fully loaded"),
    "price.fifo_worker_year": _d(5.0e6, "RUB/yr", "[L] wage 240k/mo + social + flights + camp [genius/ledger]"),
    "price.dozer_D375_hour": _d(160.0, "USD/h", "drom.ru, hh.ru [round2/erp2_b]", "loader ~$70/h"),
    "price.co_merchant": _d((150.0, 300.0), "USD/t CO", "[E] round2/audit_a, critic_a"),
    "price.russian_aisc_gold_2022": _d(1018.0, "USD/oz", "WGC [round2/erp2_b NOTES]"),

    # ------------------------------------------------------------ best-practice baselines
    "base.sluice_water_ratio_us": _d((3.2, 9.9), "m3 water/m3", "USBM 650-2,000 gal/yd3 (911metallurgist) [round2/audit_b]",
                                     "Yukon trommel 4.1-4.4; Yukon atlas 3.2-14; RU T:L 1:10-1:20; kuzstu 2023 optimum ~3"),
    "base.boulder_dozer_grapple": _d((2.7, 3.0), "USD/m3 boulder", "[E] round2/erp2_b idea3 (excavator $3.0, dozer $2.65)",
                                     "dozers handle boulders to 1.0-1.2 m (ztu.edu.ua); drill-blast only >1.5 m"),
    "base.layer_thaw_dozing": _d((110.0, 0.30), "RUB/m3, l/m3", "[E] genius/repair_final/calc.py", "cheapest stripping"),
    "base.hydraulic_stripping_fairbanks": _d(0.23, "m/day", "ASME landmark history [genius/audit_evo_1]",
                                             "36-48 giants, 150-180 d/yr; Russian gidrovskrysha"),
    "base.open_cut_placer_usd_m3_moved": _d(5.81, "USD/m3 moved", "[L-derived] genius/gate_r1_1 (SR 18)"),
    "base.underground_placer_m3_shift": _d(33.4, "m3/machine-shift", "Kularzoloto, rudmet MJ 09/16 [genius/gate_9]"),
    "base.matte_shipping": _d((100.0, 150.0), "USD/t Ni", "[round2/audit_a, critic_a]", "vs trucking concentrate $1,067/t Ni"),
    "base.dms_spodumene": _d((0.6, 5.7, 0.90), "% Li2O feed, % conc, recovery", "Kazakh ore DMS [roast; genius/gate_4]"),
    "base.dle_cost": _d((3400.0, 6200.0), "USD/t LCE", "Argonne overview (TechConnect 2026) [repair/a S15]"),
    "base.pt_timah_cash_cost": _d(17900.0, "USD/t Sn", "FY24 [genius/audit_evo_2]"),
    "base.sx_ew_grid_vs_diesel": _d((1086.0, 1590.0), "USD/t Cu", "[E] round2/erp2_a"),
    "base.ew_specific_energy": _d(2.0, "kWh/kg Cu", "standard industry [repair/a]; Faraday 2 V 90% CE = 1.87"),
    "base.freeze_conc_largest": _d(30.0, "t/h water removed", "GEA wash-column plant [round2/critic_a]"),
    "base.hot_water_drill_rate": _d((0.57, 0.62), "m/min in clean ice", "Talalay et al. 2018 (42 kW) [genius/audit_final]"),
    "base.autonomous_drystone_rate": _d(2.15, "m3/h", "ETH HEAP pilot wall [genius/audit_final]"),
    "base.excavator_mtbf": _d((80.0, 100.0), "h", "Komatsu PC4000-6 study [genius/gate_r1_2]"),
    "base.monitor_working_length": _d((350, 450), "nozzle diameters", "[genius/audit_evo_2]"),
    "base.cutterhead_resuspension": _d((0.0002, 0.0393), "fraction", "Nakai 1978; hydraulic-dredge mean 0.77% (USACE/Clarke) [genius/audit_evo_1]"),
    "base.nome_under_ice_dredging": _d(90, "days (mid-Jan to mid-Apr)", "KNOM / Nome practice [genius/audit_evo_2]"),
    "base.arctic_yakutia_utility_coal": _d((205e3, 67798), "t/yr (2016), people", "[genius/audit_final] ~3.0 t/person",
                                          "2024 all waterborne communal coal in Yakutia 122 kt (PortNews)"),
    "base.peat_nordic_yield": _d((300.0, 1000.0), "m3/ha/yr", "Malkki & Frilander 1997 [genius/gate_r1_2]"),

    # ------------------------------------------------------------ regulatory / safety limits
    "limit.fishery_ss_increment_high": _d(0.25, "mg/L above background",
                                          "Minselkhoz Order 552/2016, highest & first category fishery [genius/audit_evo_1, repair_evo_a]",
                                          "judged at a control section near the source, not after full mixing"),
    "limit.fishery_ss_increment_second": _d(0.75, "mg/L above background", "Minselkhoz Order 552/2016, second category"),
    "limit.water_code_art56": _d(None, "-", "RF Water Code art. 56 [round2/audit_b]", "bans dumping waste/cargo into water bodies"),
    "limit.ni_co4_aegl2_1h": _d(0.036, "ppm", "AEGL-2 60 min [round2/audit_a]", "AEGL-3 0.16 ppm; OSHA PEL 0.001 ppm"),
    "limit.iec61010_stored_energy": _d(0.35, "J", "IEC 61010 [round2/audit_a]"),
    "limit.coal_self_heating": _d((55.0, 50.0), "C, ppm CO", "P&I club guidance [genius/audit_final]"),
    "limit.ew_chloride": _d((25.0, 30.0), "mg/L", "[round2/audit_a]"),
    "limit.silt_curtain_efficiency": _d({"floating_alone": 0.45, "cage_type": 0.80, "combined_floating": 0.61,
                                         "combined_cage": 0.95}, "fraction removed",
                                        "Hong Kong EPD EIA EM&A manual targets (epd.gov.hk eia_1742009)",
                                        "design targets, not field results; hanging curtains in crossflow often "
                                        "ineffective (ASCE JWPCOE 2015); gaps leak (HR Wallingford HRPP560)"),
    "limit.hydro_elevator_efficiency": _d((0.17, 0.35), "-", "Pak 1959 (0.17-0.2), Veselov 1956 (0.2-0.35) via mgu.bg",
                                          "best swirl designs ~0.41 (Minarbekov, kazhydromet)"),
}


def info(key):
    """Return the full Datum for ``key`` (raises KeyError with suggestions)."""
    try:
        return DATA[key]
    except KeyError:
        near = find(key.split(".")[-1])
        raise KeyError(f"{key!r} not in kit.data; similar: {near[:8]}") from None


def get(key):
    """Return the value of ``key``."""
    return info(key).value


def lo_hi(key):
    """Return (low, high) for a range entry, or (v, v) for a scalar."""
    v = get(key)
    if isinstance(v, tuple):
        return v[0], v[-1]
    if isinstance(v, (int, float)):
        return v, v
    raise ValueError(f"{key} is not scalar/range: {type(v).__name__}")


def find(text):
    """Keys whose name, note or source contains ``text`` (case-insensitive)."""
    t = text.lower()
    return [k for k, d in DATA.items() if t in k.lower() or t in str(d.note).lower() or t in str(d.source).lower()]


def monthly(site):
    """Monthly normals dict for a site name, e.g. monthly('Verkhoyansk')."""
    for suffix in (".monthly", ".summer"):
        k = f"climate.{site}{suffix}"
        if k in DATA:
            return dict(DATA[k].value)
    raise KeyError(f"no monthly normals for {site!r}; have: "
                   f"{sorted({k.split('.')[1] for k in DATA if k.startswith('climate.') and isinstance(DATA[k].value, dict)})}")
