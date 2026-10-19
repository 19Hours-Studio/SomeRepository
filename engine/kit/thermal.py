"""Thermal models for frozen ground, water and ice: thaw/freeze depth, heat to thaw, water heat budget,
heat transfer to a frozen face, open-water heat loss, radiation, talik under lakes, freezing of backfilled holes.

SI units throughout (m, s, J, W, K/C) unless a parameter name says otherwise (e.g. ``days``, ``FDD`` in C*day).
Volumetric latent heat L_vol (J/m3 of ground) = ice_vol_frac * 917 * 334e3 (see latent_heat_per_m3).
"""
import math

from . import data
from . import climate

RHO_I, LF, CW, SIG = data.RHO_ICE, data.L_FUSION, data.C_W_VOL, data.SIGMA_SB


def _pos(name, v):
    if v is None or not v > 0:
        raise ValueError(f"{name} must be > 0 (got {v})")


# ------------------------------------------------------------------ heat content
def latent_heat_per_m3(ice_vol_frac):
    """Latent heat to melt the ice in 1 m3 of frozen ground, J/m3 = theta_i * rho_i * L.

    ice_vol_frac: volumetric ice content 0-1 (0.15 loose hoisted lumps, 0.25-0.35 saturated gravel,
    0.65-0.9 yedoma). 1 m3 of pure ice = 306 MJ. Source: round2/audit_b/c1_dam.py; all thaw scripts.
    """
    if not 0.0 <= ice_vol_frac <= 1.0:
        raise ValueError("ice_vol_frac must be 0-1")
    return ice_vol_frac * RHO_I * LF


def thaw_energy_per_m3(ice_vol_frac, T0_C, c_frozen=1.8e6, T_end_C=0.0, c_thawed=2.5e6):
    """Heat to take 1 m3 of frozen ground from T0 (<0 C) to T_end (>=0 C), J/m3.

    E = theta_i rho_i L + c_frozen*(0-T0) + c_thawed*T_end. c in J/m3/K (frozen gravel 1.6-2.0e6).
    Reference: 30% ice at -5 C -> ~101 MJ/m3; loose 15% ice -> ~55 MJ/m3 (round2/erp2_b/idea2_icedam.py).
    """
    if T0_C > 0 or T_end_C < 0:
        raise ValueError("need T0_C <= 0 and T_end_C >= 0")
    _pos("c_frozen", c_frozen)
    return latent_heat_per_m3(ice_vol_frac) + c_frozen * (0.0 - T0_C) + c_thawed * T_end_C


# ------------------------------------------------------------------ water heat budget
def water_ratio(E_J_m3, dT_water_K, efficiency=1.0):
    """m3 of water needed per m3 of frozen ground thawed = E/(c_w * dT * eff).

    dT_water: temperature drop actually extracted from the water (inlet - outlet, outlet >= ~0.5 C).
    efficiency: share of that heat reaching the target ground (0-1). Compare with sluice need 3.2-9.9
    m3/m3 (data 'base.sluice_water_ratio_us'). Source: round2/audit_b/c1_dam.py, erp2_b, repair/b.
    """
    _pos("E_J_m3", E_J_m3)
    _pos("dT_water_K", dT_water_K)
    if not 0 < efficiency <= 1:
        raise ValueError("efficiency must be in (0,1]")
    return E_J_m3 / (CW * dT_water_K * efficiency)


def thaw_feed_rate(Q_m3_s, dT_water_K, E_J_m3, efficiency=1.0):
    """Ground thawed by a water flow, m3/s = Q c_w dT eff / E ('feed = flow x temperature').

    Multiply by 86400 for m3/day. Source: round2/erp2_b/idea2_icedam.py (47 L/s, 5 C, ice 0.15 -> 49 m3/h).
    """
    _pos("Q_m3_s", Q_m3_s)
    return Q_m3_s * CW * dT_water_K * efficiency / E_J_m3 if dT_water_K > 0 else 0.0


def water_heat_power(Q_m3_s, dT_K):
    """Heat carried by a water flow cooled by dT, W = Q c_w dT."""
    if Q_m3_s < 0:
        raise ValueError("Q must be >= 0")
    return Q_m3_s * CW * dT_K


def melt_power(ice_m3_per_day, warm_from_C=0.0):
    """Power to melt ice at a volumetric rate, W (optionally warming it from warm_from_C < 0 first).
    Source: genius/audit_final (300 m3/d -> 1.06 MW)."""
    if ice_m3_per_day < 0 or warm_from_C > 0:
        raise ValueError("ice rate >= 0, warm_from_C <= 0")
    return ice_m3_per_day * RHO_I * (LF + 2100.0 * (-warm_from_C)) / 86400.0


# ------------------------------------------------------------------ Stefan / Neumann
def stefan_depth(dT_K, t_s, L_vol, k):
    """One-phase Stefan thaw (or freeze) depth X = sqrt(2 k dT t / L_vol), m.

    dT: surface temperature above (thaw) or below (freeze) 0 C; k: conductivity of the thawed (frozen)
    layer W/m/K; L_vol: J/m3 latent heat of the material changing phase. Neglects sensible heat
    (overestimates depth 5-15% when Stefan number > 0.1). Source: Stefan; round2/audit_b c1 (peat), repair/a.
    """
    for n, v in (("dT_K", dT_K), ("t_s", t_s), ("L_vol", L_vol), ("k", k)):
        _pos(n, v)
    return math.sqrt(2.0 * k * dT_K * t_s / L_vol)


def stefan_time(depth_m, dT_K, L_vol, k):
    """Time for a Stefan front to reach depth: t = L X^2/(2 k dT), s."""
    for n, v in (("depth_m", depth_m), ("dT_K", dT_K), ("L_vol", L_vol), ("k", k)):
        _pos(n, v)
    return L_vol * depth_m ** 2 / (2.0 * k * dT_K)


def stefan_depth_degree_days(degree_days, L_vol, k, n_factor=1.0):
    """Stefan depth from air degree-days (C*day) times an n-factor (surface/air): X = sqrt(2 k n DD 86400/L)."""
    _pos("degree_days", degree_days)
    return stefan_depth(n_factor * degree_days, 86400.0, L_vol, k)


def stefan_depth_with_resistance(dT_K, t_s, L_vol, k, R_surface):
    """Stefan front behind a surface thermal resistance R (m2K/W: snow, ice, insulation, 1/h):

    L (R X + X^2/(2k)) = dT t  ->  X = k(-R + sqrt(R^2 + 2 dT t/(L k))).
    Uses: thaw under a heated floor (gate_7: R 5.2, 20 yr -> 10.7 m), freeze-on below grounded ice
    (round2/audit_b/c5_ice.py: 1.7 m ice, 775 C*d -> 0.73 m), freezing of a sprayed lift.
    """
    if R_surface < 0:
        raise ValueError("R_surface must be >= 0")
    for n, v in (("dT_K", dT_K), ("t_s", t_s), ("L_vol", L_vol), ("k", k)):
        _pos(n, v)
    return k * (-R_surface + math.sqrt(R_surface ** 2 + 2.0 * dT_K * t_s / (L_vol * k)))


def stefan_time_with_resistance(depth_m, dT_K, L_vol, k, R_surface):
    """Inverse of stefan_depth_with_resistance: t = L (R X + X^2/(2k))/dT, s.
    Source: round2/audit_b/c1_dam.py (0.4 m lift, -20 C, h 15 W/m2K -> ~95 h)."""
    if R_surface < 0:
        raise ValueError("R_surface must be >= 0")
    for n, v in (("depth_m", depth_m), ("dT_K", dT_K), ("L_vol", L_vol), ("k", k)):
        _pos(n, v)
    return L_vol * (R_surface * depth_m + depth_m ** 2 / (2.0 * k)) / dT_K


def neumann_depth(T_surface, T_initial, t_s, L_vol, k_thawed=1.8, k_frozen=2.4, C_thawed=2.6e6, C_frozen=2.0e6):
    """Two-phase Neumann solution for thaw of frozen ground (initially T_initial < 0) under a surface held
    at T_surface > 0: X = 2 lambda sqrt(t), lambda solving
    ku Ts e^{-l^2/au}/(sqrt(pi au) erf(l/sqrt au)) + kf T0 e^{-l^2/af}/(sqrt(pi af) erfc(l/sqrt af)) = L l.

    Includes the cold content of the frozen ground (Stefan does not). Source: genius/audit_evo_1/idea2_check.py
    (ice 25%, T0 -4 C, 40 yr: 5.6/8.5/10.8/12.7 m at 1/2/3/4 C bottom water). Defaults from that run.
    """
    if T_surface <= 0 or T_initial > 0:
        raise ValueError("need T_surface > 0 >= T_initial")
    for n, v in (("t_s", t_s), ("L_vol", L_vol), ("k_thawed", k_thawed), ("k_frozen", k_frozen)):
        _pos(n, v)
    au, af = k_thawed / C_thawed, k_frozen / C_frozen

    def f(lam):
        a = k_thawed * T_surface * math.exp(-lam ** 2 / au) / (math.sqrt(math.pi * au) * math.erf(lam / math.sqrt(au)))
        b = k_frozen * T_initial * math.exp(-lam ** 2 / af) / (math.sqrt(math.pi * af) * math.erfc(lam / math.sqrt(af)))
        return a + b - L_vol * lam

    lo, hi = 1e-12, 1e-2
    while f(hi) > 0:
        hi *= 2
        if hi > 1:
            raise ValueError("no Neumann root (check inputs)")
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return 2.0 * 0.5 * (lo + hi) * math.sqrt(t_s)


def talik_depth_lake_axis(radius_m, T_ground_surface, T_lake_bottom, geo_gradient=0.03):
    """Steady talik depth (m below lake bed) on the axis of a circular lake, Lachenbruch (1957) disk source:

    T(z) = Tg + G z + (Tb - Tg)(1 - z/sqrt(z^2+R^2));  first z where T <= 0.
    Returns math.inf for a through-talik (no frozen ground above the permafrost base -Tg/G).
    Off-axis the talik is much shallower (only ~25-30% of a 100 m lake has the axis depth - audit_final).
    Steady state takes decades-centuries (Stefan time to 15 m >= ~45 yr). Measured: 91 m TEM under a
    thermokarst lake, ~25 m Yakutian lake, ~12 m Yukechi (data 'ground.lake_talik_measured').
    Source: genius/repair_final/calc.py, audit_final/audit_talik2d.py.
    """
    _pos("radius_m", radius_m)
    _pos("geo_gradient", geo_gradient)
    if T_ground_surface >= 0 or T_lake_bottom <= 0:
        raise ValueError("need mean ground surface T < 0 and lake bottom T > 0")
    Tg, Tb, G, R = T_ground_surface, T_lake_bottom, geo_gradient, radius_m

    def f(z):
        return Tg + G * z + (Tb - Tg) * (1.0 - z / math.sqrt(z * z + R * R))

    zmax = -Tg / G + 1.0
    z, step = 0.0, 0.05
    while z < zmax:
        if f(z + step) <= 0:
            lo, hi = z, z + step
            for _ in range(60):
                m = 0.5 * (lo + hi)
                lo, hi = (m, hi) if f(m) > 0 else (lo, m)
            return 0.5 * (lo + hi)
        z += step
    return math.inf


# ------------------------------------------------------------------ heat transfer to a frozen face / ice
def h_dittus_boelter(U, Dh, nu=1.6e-6, k=data.K_WATER, Pr=12.0, n=0.4):
    """Turbulent convection coefficient, W/m2K: Nu = 0.023 Re^0.8 Pr^n (n 0.4 heating the wall... use 0.4).

    Valid Re > 1e4, 0.6 < Pr < 160, smooth duct. Water near 1-5 C: nu 1.5-1.75e-6, Pr 11-13, k 0.57.
    Underestimates rough gravel faces ~3x (Douglas et al. 2023) - see h_gnielinski(roughness_factor).
    Source: round2/audit_b/c2_toe.py; genius/repair_evo_a/idea2.py (gallery 1 m3/s -> ~860 W/m2K).
    """
    for nme, v in (("U", U), ("Dh", Dh), ("nu", nu), ("k", k), ("Pr", Pr)):
        _pos(nme, v)
    Re = U * Dh / nu
    if Re < 1e4:
        raise ValueError(f"Dittus-Boelter needs Re>1e4 (Re={Re:.0f})")
    return 0.023 * Re ** 0.8 * Pr ** n * k / Dh


def h_gnielinski(U, Dh, nu=1.57e-6, k=data.K_WATER, Pr=11.6, roughness_factor=1.0):
    """Gnielinski turbulent coefficient, W/m2K: f=(0.79 ln Re - 1.64)^-2,
    Nu = (f/8)(Re-1000)Pr / (1 + 12.7 sqrt(f/8)(Pr^(2/3)-1)); valid 3e3 < Re < 5e6, 0.5 < Pr < 2000.

    roughness_factor 1-3: Douglas et al. 2023 (JGR-ES) measured permafrost-bank ablation ~3x smooth-wall theory.
    Preferred over Dittus-Boelter (better-sourced, lower error). Source: genius/audit_evo_2/check5.py
    (1-3 m/s, Dh 0.1-0.2 m, x3 -> 8-22 kW/m2K).
    """
    for nme, v in (("U", U), ("Dh", Dh), ("nu", nu), ("k", k), ("Pr", Pr), ("roughness_factor", roughness_factor)):
        _pos(nme, v)
    Re = U * Dh / nu
    if not 3e3 <= Re <= 5e6:
        raise ValueError(f"Gnielinski valid 3e3<Re<5e6 (Re={Re:.0f})")
    f = (0.79 * math.log(Re) - 1.64) ** -2
    Nu = (f / 8) * (Re - 1000) * Pr / (1 + 12.7 * math.sqrt(f / 8) * (Pr ** (2.0 / 3.0) - 1))
    return roughness_factor * Nu * k / Dh


def h_jet_stagnation(v_jet, d_nozzle, nu=1.57e-6, k=data.K_WATER, Pr=11.6, C=0.715):
    """Heat-transfer coefficient at the stagnation point of an impinging round water jet, W/m2K:
    Nu_d = C Re_d^0.5 Pr^0.4 (laminar stagnation-point solution, Sibulkin 1952 Nu=0.763(a d/nu)^0.5 Pr^0.4
    with velocity gradient a ~0.88 v/d -> C ~0.715). Stagnation point only: face-average is several times
    lower, and a jet spreads its heat over roof/ribs (need hA, not h).
    Source: genius/audit_evo_2/check5.py (50 mm at 10-15 m/s -> 12-15 kW/m2K).
    """
    for nme, v in (("v_jet", v_jet), ("d_nozzle", d_nozzle), ("nu", nu), ("k", k), ("Pr", Pr)):
        _pos(nme, v)
    Re = v_jet * d_nozzle / nu
    return C * Re ** 0.5 * Pr ** 0.4 * k / d_nozzle


def h_flat_plate_turbulent(U, L, nu=1.79e-6, k=0.56, Pr=13.4):
    """Average turbulent flat-plate coefficient, W/m2K: Nu_L = 0.037 Re_L^0.8 Pr^(1/3) (Re_L 5e5-1e8).
    Source: Incropera; roast/roast.py (pod 5 m at 0.2 m/s -> ~390 W/m2K)."""
    for nme, v in (("U", U), ("L", L), ("nu", nu), ("k", k), ("Pr", Pr)):
        _pos(nme, v)
    return 0.037 * (U * L / nu) ** 0.8 * Pr ** (1.0 / 3.0) * k / L


def h_ice_water_ashton(U, depth, C_w=1622.0):
    """Water-to-ice heat-transfer coefficient under a river ice cover, W/m2K: h = C_w U^0.8 / D^0.2
    (Ashton 1986, River and Lake Ice Engineering; C_w = 1622). U depth-mean velocity m/s, D flow depth m.
    Hundredths of a degree of supercooling/superheat matter (Ashton 1973). Source: round2/critic_b/calc_extra.py.
    """
    _pos("U", U)
    _pos("depth", depth)
    return C_w * U ** 0.8 / depth ** 0.2


def h_from_stanton(St, U):
    """h = St rho_w c_w U (W/m2K); St 0.0015-0.002 smooth, ~0.005 rough (repair/b, rt_b)."""
    _pos("St", St)
    _pos("U", U)
    return St * CW * U


def ice_melt_rate(h, dT_K):
    """Melt (ablation) rate of an ice surface in water dT above 0 C, m/s = h dT/(rho_i L).
    Multiply by 86400 for m/day. Source: roast/roast.py, critic_b."""
    if h < 0 or dT_K < 0:
        raise ValueError("h, dT >= 0")
    return h * dT_K / (RHO_I * LF)


def face_retreat_rate(h, dT_K, E_J_m3):
    """Retreat rate of a frozen-ground face washed by water dT above 0 C, m/s = h dT / E.
    Valid only while thawed debris is carried away (a 1-2 cm debris coat caps the flux at k dT/coat)."""
    _pos("E_J_m3", E_J_m3)
    if h < 0 or dT_K < 0:
        raise ValueError("h, dT >= 0")
    return h * dT_K / E_J_m3


def debris_coat_limited_flux(k_debris, dT_K, coat_m):
    """Conductive heat flux through a thawed debris coat, W/m2 = k dT / thickness (critic_b: k 2.0)."""
    _pos("coat_m", coat_m)
    return k_debris * dT_K / coat_m


def efold_length(Q_m3_s, h, wetted_contact_m):
    """Distance over which the water-to-face temperature excess falls by 1/e, m: L = Q rho c/(h P).
    P = wetted perimeter actually in contact with frozen material. Source: round2/audit_b/c2_toe.py."""
    for nme, v in (("Q_m3_s", Q_m3_s), ("h", h), ("wetted_contact_m", wetted_contact_m)):
        _pos(nme, v)
    return Q_m3_s * CW / (h * wetted_contact_m)


def ntu_required(T_in, T_out, T_surface=0.0):
    """Number of transfer units to cool water from T_in to T_out against a surface at T_surface:
    eps = (T_in-T_out)/(T_in-T_surface), NTU = -ln(1-eps). hA_required = NTU * m_dot * c.
    Source: genius/audit_evo_2/check5.py (4 -> 0.9 C, 0.125 m3/s -> hA >= 781 kW/K)."""
    if not T_in > T_out > T_surface:
        raise ValueError("need T_in > T_out > T_surface")
    eps = (T_in - T_out) / (T_in - T_surface)
    return -math.log(1.0 - eps)


# ------------------------------------------------------------------ open water / ponds
def open_water_heat_loss(T_air, U, T_water=0.0, C_h=1.5e-3, C_e=1.5e-3, eps_sky=0.70, rh_ice=1.0, p_Pa=101325.0):
    """Winter heat loss from open water (pond, moat, polynya, dredge slot) by bulk formulae, W/m2:

    q = rho cp C_h U (Tw-Ta) + rho Lv C_e U (q_s(Tw) - q_a) + 0.97 sigma Tw^4 - eps_sky sigma Ta^4.
    Validity: T_air < T_water, U 1-15 m/s at 10 m. Calibration: Makinson Inlet polynya measured ~484 W/m2
    at -30 C, 5 m/s (this model gives ~590, i.e. ~20% high); Maykut 1978 leads 400-700 W/m2. In calm air a
    free-convection floor (~5 W/m2K sensible) applies. Source: genius/gate_r1_1 (748 W/m2 at -40 C, 5 m/s),
    audit_final, repair_final.
    """
    if U < 0:
        raise ValueError("U >= 0")
    if T_air >= T_water:
        raise ValueError("bulk loss formula needs T_air < T_water")
    rho = climate.air_density(T_air, p_Pa)
    H = rho * data.CP_AIR * C_h * U * (T_water - T_air)
    es = climate.psat_water(T_water)
    ea = rh_ice * (climate.psat_ice(T_air) if T_air <= 0 else climate.psat_water(T_air))
    LE = rho * data.L_VAPOUR * C_e * U * 0.622 * (es - ea) / p_Pa
    LW = 0.97 * SIG * (T_water + 273.15) ** 4 - eps_sky * SIG * (T_air + 273.15) ** 4
    return H + LE + LW


def open_water_freezing_rate(q_W_m2):
    """Ice growth rate on open water losing q W/m2, m/s = q/(rho_i L) (500 W/m2 -> ~6 mm/h)."""
    if q_W_m2 < 0:
        raise ValueError("q >= 0")
    return q_W_m2 / (RHO_I * LF)


def water_surface_net_flux(SW_down, T_air, T_water, rh=0.7, U=3.0, cloud=0.7, albedo=0.07, C=1.3e-3):
    """Summer net heat gain of a pond surface, W/m2 (positive = water gains):
    (1-albedo)SW + 0.97 eps_a sigma Ta^4 - 0.97 sigma Tw^4 + rho cp C U (Ta-Tw) + rho Lv C U 0.622(ea-es(Tw))/p,
    eps_a = 1.24 (ea[hPa]/Ta)^(1/7)(1+0.22 c^2) (Brutsaert with cloud). Source: genius/audit_evo_2/check5.py
    (3 ha pond at 7 C in August, Susuman, Kt 0.40-0.45 -> 3.1-3.6 MW)."""
    if SW_down < 0 or not 0 <= rh <= 1 or not 0 <= cloud <= 1:
        raise ValueError("SW>=0, rh and cloud in 0-1")
    es = lambda T: 6.112 * math.exp(17.67 * T / (T + 243.5))  # hPa
    ea = rh * es(T_air)
    Tk = T_air + 273.15
    eps = 1.24 * (ea / Tk) ** (1.0 / 7.0) * (1 + 0.22 * cloud * cloud)
    LW = 0.97 * eps * SIG * Tk ** 4 - 0.97 * SIG * (T_water + 273.15) ** 4
    H = 1.2 * data.CP_AIR * C * U * (T_air - T_water)
    LE = 1.2 * data.L_VAPOUR * C * U * 0.622 * (ea - es(T_water)) / 1013.0
    return (1 - albedo) * SW_down + LW + H + LE


# ------------------------------------------------------------------ radiation
def blackbody_exitance(T_K):
    """sigma T^4, W/m2."""
    _pos("T_K", T_K)
    return SIG * T_K ** 4


def planck_band_exitance(T_K, lam1=8e-6, lam2=13e-6, n=4000):
    """Hemispherical blackbody exitance in a wavelength band, W/m2 (pi * integral of Planck radiance).
    8-13 um 'sky window' at -50 C = 30.0 W/m2 (21.3% of sigma T^4): the reason night-sky cooling at
    eutectic temperatures is tiny. Source: round2/audit_a, critic_a, repair/a idea4 (multiple reproductions)."""
    _pos("T_K", T_K)
    if not 0 < lam1 < lam2:
        raise ValueError("0 < lam1 < lam2")
    h, c, kB = 6.62607015e-34, 2.99792458e8, 1.380649e-23
    dl = (lam2 - lam1) / n
    s = 0.0
    for i in range(n):
        l = lam1 + (i + 0.5) * dl
        s += 2 * math.pi * h * c * c / l ** 5 / (math.exp(h * c / (l * kB * T_K)) - 1.0)
    return s * dl


# ------------------------------------------------------------------ freezing of backfill
def freeze_time_cylinder(radius_m, T_ground, water_frac, k=2.0, C_vol=2.4e6, T_fill=1.0, r_max=None,
                         cells_in_hole=8, t_max_days=5000):
    """Days for water-saturated backfill in an isolated cylindrical hole (radius R, initially T_fill > 0)
    to freeze completely by conduction into surrounding frozen ground at T_ground (< 0), held at r_max.

    Explicit enthalpy finite-volume model (latent heat water_frac*334e6 J/m3 inside the hole only, uniform
    k and C). Validity: conduction only (no convection/seepage), infinite cold ground (r_max default
    max(15 m, 10 R)); neighbouring holes compete for the same cold -> a panel freezes far slower
    (see freeze_time_slab_two_sided). Returns math.inf if not frozen by t_max_days.
    Source: genius/audit_evo_2/check2b.py (R 1.1 m, 35% water: 304 d at -3 C, 164 d at -5 C, 93 d at -8 C).
    """
    _pos("radius_m", radius_m)
    if T_ground >= 0:
        raise ValueError("T_ground must be < 0 C")
    if not 0 < water_frac <= 1:
        raise ValueError("water_frac must be in (0,1]")
    if T_fill < 0:
        raise ValueError("T_fill must be >= 0")
    r_max = r_max or max(15.0, 10.0 * radius_m)
    dr = radius_m / cells_in_hole
    n = int(round(r_max / dr))
    r = [(i + 0.5) * dr for i in range(n)]
    rf = [i * dr for i in range(n + 1)]
    Lh = water_frac * 334e6
    L = [Lh if ri < radius_m else 0.0 for ri in r]
    H = [L[i] + C_vol * T_fill if r[i] < radius_m else C_vol * T_ground for i in range(n)]
    n_in = sum(1 for ri in r if ri < radius_m)
    alpha = k / C_vol
    dt = 0.2 * dr * dr / alpha
    coef = [dt / (ri * dr) for ri in r]
    t, tmax = 0.0, t_max_days * 86400.0
    Tb = T_ground
    while t < tmax:
        T = [(h / C_vol) if h < 0 else ((h - Li) / C_vol if h > Li else 0.0) for h, Li in zip(H, L)]
        flux = [0.0] * (n + 1)
        for i in range(1, n):
            flux[i] = -k * (T[i] - T[i - 1]) / dr
        flux[n] = -k * (Tb - T[n - 1]) / (dr / 2)
        for i in range(n):
            H[i] -= (rf[i + 1] * flux[i + 1] - rf[i] * flux[i]) * coef[i]
        t += dt
        if max(H[:n_in]) <= 0.0:
            return t / 86400.0
    return math.inf


def freeze_time_slab_two_sided(latent_J_m2, k, dT_K, C_vol=2.4e6):
    """Time to absorb a latent load Q (J per m2 of slab) by conduction into two semi-infinite frozen
    half-spaces at dT below 0 C with their faces held at 0 C: Q = 2*2 k dT sqrt(t/(pi alpha)) ->
    t = pi alpha (Q/(4 k dT))^2, s. Panel-scale bound for backfilled rooms/holes between pillars.
    Source: genius/audit_evo_2/check2.py (1.3-15 yr at -5..-2 C)."""
    for nme, v in (("latent_J_m2", latent_J_m2), ("k", k), ("dT_K", dT_K), ("C_vol", C_vol)):
        _pos(nme, v)
    return math.pi * (k / C_vol) * (latent_J_m2 / (4.0 * k * dT_K)) ** 2
