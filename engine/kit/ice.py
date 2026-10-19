"""Ice models: growth (with snow), bearing capacity (Gold; moving vs stationary; Westergaard edge
reduction), buoyancy/uplift and lift capacity, flexure of the sheet (characteristic length, point and edge
line loads), ice vs water depth (backwaters freezing to the bed), creep and thermal shock.

SI units (m, N, Pa, s) unless the name says otherwise. Gold's formula is used in its native units:
P [kg] = A [kg/cm2] * h [cm]^2.
"""
import math

from . import data
from . import thermal

RHO_W, RHO_I, LF, G = data.RHO_W, data.RHO_ICE, data.L_FUSION, data.G
K_ICE = data.K_ICE


def _pos(name, v):
    if v is None or not v > 0:
        raise ValueError(f"{name} must be > 0 (got {v})")


# ------------------------------------------------------------------ growth
def ice_thickness(FDD, alpha=0.024):
    """Empirical Stefan ice growth h = alpha sqrt(FDD), m (FDD in C*day of AIR freezing degree-days).

    alpha (m/(C d)^0.5): 0.027 windswept/snow-free; 0.017-0.024 typical snow-covered lakes/rivers
    (Michel 1971; data 'ice.alpha_*'); pure Stefan with no snow and no surface resistance ~0.035.
    The snow factor is the dominant uncertainty (+/-30%). Source: genius/repair_final, audit_final,
    round2/erp2_b (a = 2.0-2.7 cm).
    """
    if FDD < 0:
        raise ValueError("FDD must be >= 0")
    if not 0.005 <= alpha <= 0.04:
        raise ValueError("alpha outside 0.005-0.04 m/(C d)^0.5")
    return alpha * math.sqrt(FDD)


def ice_thickness_stefan(FDD, k_ice=K_ICE, h0=0.0):
    """Pure Stefan growth with the ice surface at air temperature (no snow): h = sqrt(h0^2 + 2 k FDD 86400/(rho L)).
    Upper bound (pure Stefan at 5,000-6,500 C*d gives 2.5-2.8 m vs observed 1.2-1.9 m). Source: audit_final."""
    if FDD < 0 or h0 < 0:
        raise ValueError("FDD, h0 >= 0")
    return math.sqrt(h0 ** 2 + 2.0 * k_ice * FDD * 86400.0 / (RHO_I * LF))


def ice_thickness_with_snow(FDD, snow_depth_m, k_snow=0.3, k_ice=K_ICE, h0=0.0):
    """Stefan growth under a snow layer of constant thickness (snow factor done physically):
    rho L [ (h^2-h0^2)/(2k_i) + (h-h0) s/k_s ] = FDD*86400  ->  h. k_snow 0.1-0.35 W/mK (Sturm 1997;
    see snow_conductivity). Source: round2/audit_b/c5_ice.py."""
    if FDD < 0 or snow_depth_m < 0 or h0 < 0:
        raise ValueError("FDD, snow, h0 >= 0")
    _pos("k_snow", k_snow)
    a = 1.0 / (2 * k_ice)
    b = snow_depth_m / k_snow
    c = FDD * 86400.0 / (RHO_I * LF) + a * h0 ** 2 + b * h0
    return (-b + math.sqrt(b * b + 4 * a * c)) / (2 * a)


def snow_conductivity(rho_snow):
    """Effective snow thermal conductivity, W/mK: k = 0.138 - 1.01 rho + 3.233 rho^2 (rho in g/cm3,
    valid 0.156-0.6). Sturm et al. 1997 J Glaciol 43:26. Source: genius/gate_9/gate9_calcs.py."""
    if not 0.156 <= rho_snow <= 0.6:
        raise ValueError("Sturm 1997 valid for 0.156-0.6 g/cm3")
    return 0.138 - 1.01 * rho_snow + 3.233 * rho_snow ** 2


def ice_growth_rate(h_ice, T_surface_C, snow_depth_m=0.0, k_snow=0.3, k_ice=K_ICE):
    """Basal growth rate of an existing ice sheet, m/s = k dT / (R rho L), R = h/k_i + s/k_s (quasi-steady).
    E.g. 1.0 m ice at -30 C surface -> ~1.9 cm/day: a stalled object under the ice is frozen in within
    hours-days (repair/b). Source: repair/b/idea4_pods.py, genius/gate_9."""
    _pos("h_ice", h_ice)
    if T_surface_C >= 0:
        raise ValueError("surface must be below 0 C")
    R = h_ice / k_ice + snow_depth_m / k_snow
    return (-T_surface_C) / R / (RHO_I * LF)


def days_to_thickness(h_target, fdd_per_day, alpha=0.024):
    """Days of steady frost (fdd_per_day C*d/day) for h = alpha sqrt(FDD) to reach h_target."""
    _pos("h_target", h_target)
    _pos("fdd_per_day", fdd_per_day)
    return (h_target / alpha) ** 2 / fdd_per_day


def freeze_on_below_ice(FDD_after_contact, h_ice, snow_depth_m=0.0, porosity=0.30, k_snow=0.3, k_frozen=2.6):
    """Thickness of saturated bed sediment frozen onto the base of an ice sheet after it grounds (m):
    Stefan front behind the ice+snow resistance R0 = h/k_i + s/k_s with L_vol = porosity rho_w L.
    Source: round2/audit_b/c5_ice.py (1.7 m ice, no snow, 775 C*d, n 0.30 -> ~0.73 m: a floe that touches
    the boulders in March stays grounded)."""
    _pos("FDD_after_contact", FDD_after_contact)
    _pos("h_ice", h_ice)
    if not 0 < porosity < 1:
        raise ValueError("porosity in (0,1)")
    R0 = h_ice / K_ICE + snow_depth_m / k_snow
    return thermal.stefan_depth_with_resistance(FDD_after_contact, 86400.0, porosity * 1000.0 * LF, k_frozen, R0)


# ------------------------------------------------------------------ bearing capacity
def gold_allowable_load(h_m, A=3.5, white_ice_m=0.0, flooded_m=0.0, white_factor=0.5, flooded_factor=0.65):
    """Allowable load on floating ice by Gold's formula, tonnes: P[kg] = A[kg/cm2] * h_eff[cm]^2.

    A: 3.5 safe (Gold 1971 lower bound, used for planning), 7 upper limit for normal use, ~17 failure
    expected (cgs.ca Hayley & Proskin keynote; Wikipedia Ice road). h_eff = clear ice + 0.5 white ice
    + 0.65 flooded (built-up) layer (Russian ice-crossing rule, gate_7; white ice 0.5 per Finnish practice).
    Validity: MOVING loads or parking <= 2 h, intact ice away from cracks and open water.
    Use stationary_load_capacity for parked loads and edge_capacity_factor near edges/wet cracks.
    Source: genius/gate_7 (2TE116 2x138 t needs 2.8 m at A 3.5), gate_9, repair_evo_b.
    """
    if h_m < 0 or white_ice_m < 0 or flooded_m < 0:
        raise ValueError("thicknesses must be >= 0")
    if not 1.0 <= A <= 20.0:
        raise ValueError("A outside 1-20 kg/cm2")
    h_eff_cm = 100.0 * (h_m + white_factor * white_ice_m + flooded_factor * flooded_m)
    return A * h_eff_cm ** 2 / 1000.0


def gold_required_thickness(load_t, A=3.5):
    """Effective ice thickness (m) needed for a load in tonnes by Gold's formula h = sqrt(P/A)."""
    _pos("load_t", load_t)
    return math.sqrt(load_t * 1000.0 / A) / 100.0


def stationary_load_capacity(h_m, hours, A=3.5, long_term_factor=0.5):
    """Allowable PARKED load (t). Gold's formula applies to moving loads and parking <= 2 h (Gold 1971;
    data 'ice.parking_limit_h'); beyond that the sheet creeps (deflection grows, microcracking) and there is
    no published universal reduction factor. Screening heuristic: <= 2 h -> Gold; 2 h - 7 days -> x0.5
    (repair_evo_b 'parked loads x0.5'); > 7 days -> ValueError (needs creep/deflection analysis and
    freeboard monitoring). Never treat a parked plant, crane or stockpile on ice as a moving load.
    """
    if hours < 0:
        raise ValueError("hours >= 0")
    P = gold_allowable_load(h_m, A)
    if hours <= 2.0:
        return P
    if hours <= 7 * 24:
        return long_term_factor * P
    raise ValueError("load parked > 7 days: Gold's formula does not apply; do a creep analysis")


def characteristic_length(h, E=5e9, nu=0.33, k_found=RHO_W * G):
    """Characteristic length of a floating plate l = (E h^3/(12(1-nu^2) k))^(1/4), m (k = rho_w g)."""
    _pos("h", h)
    _pos("E", E)
    return (E * h ** 3 / (12 * (1 - nu ** 2) * k_found)) ** 0.25


def point_load_deflection(P_N, h, E=5e9, nu=0.33, k_found=RHO_W * G):
    """Central deflection of an infinite floating plate under a point load, m: w = P/(8 sqrt(D k)) (Hertz/Wyman).
    Source: round2/audit_b/c5_ice.py (1.7-3.2 m ice: 7-29 MN to bend it 0.3 m; l = 18-35 m: a thick sheet
    bridges a boulder field instead of settling onto it)."""
    _pos("P_N", P_N)
    D = E * h ** 3 / (12 * (1 - nu ** 2))
    return P_N / (8.0 * math.sqrt(D * k_found))


def _b_equiv(a, h):
    return math.sqrt(1.6 * a * a + h * h) - 0.675 * h if a < 1.724 * h else a


def westergaard_interior_stress(P_N, h, a, E=5e9, nu=0.33, k_found=RHO_W * G):
    """Max bending stress (Pa) under a circular load of radius a in the interior of a plate on a Winkler
    foundation (Westergaard 1926 = 1948): sigma = 3(1+nu)P/(2 pi h^2) [ln(l/b) + 0.6159],
    b = sqrt(1.6a^2+h^2)-0.675h for a < 1.724h else a. Identical to 0.275(1+nu)P/h^2 log10(Eh^3/(k b^4)).
    Source: Westergaard 1926/1948; Ioannides et al. 1985 (TRB 'Westergaard solutions reconsidered')."""
    _pos("P_N", P_N)
    _pos("a", a)
    l = characteristic_length(h, E, nu, k_found)
    return 3 * (1 + nu) * P_N / (2 * math.pi * h * h) * (math.log(l / _b_equiv(a, h)) + 0.6159)


def westergaard_edge_stress(P_N, h, a, E=5e9, nu=0.33, k_found=RHO_W * G, method="1948"):
    """Max bending stress (Pa) for a load at a FREE EDGE (open lead, wet crack, slot, shoreline crack).

    method '1948' (recommended; Ioannides et al. 1985 show the 1926 edge formula is unconservative):
      sigma = 3(1+nu)P/(pi(3+nu)h^2) [ln(Eh^3/(100 k a^4)) + 1.84 - 4nu/3 + (1-nu)/2 + 1.18(1+2nu)a/l]
    method '1926': sigma = 0.529(1+0.54nu)P/h^2 [log10(Eh^3/(k b^4)) - 0.71]  (= 0.572P/h^2(4log(l/b)+0.359) at nu 0.15)
    """
    _pos("P_N", P_N)
    _pos("a", a)
    l = characteristic_length(h, E, nu, k_found)
    if method == "1948":
        return 3 * (1 + nu) * P_N / (math.pi * (3 + nu) * h * h) * (
            math.log(E * h ** 3 / (100 * k_found * a ** 4)) + 1.84 - 4 * nu / 3 + (1 - nu) / 2 + 1.18 * (1 + 2 * nu) * a / l)
    if method == "1926":
        b = _b_equiv(a, h)
        return 0.529 * (1 + 0.54 * nu) * P_N / (h * h) * (math.log10(E * h ** 3 / (k_found * b ** 4)) - 0.71)
    raise ValueError("method must be '1948' or '1926'")


def edge_capacity_factor(h, a=0.3, E=5e9, nu=0.33, method="1948"):
    """Ratio allowable-load-at-edge / allowable-load-in-interior = sigma_interior/sigma_edge (same P).
    Typically 0.45-0.65: a load at a crack, lead, slot or the shore hinge carries about half of Gold's
    interior value. Use: gold_allowable_load(...) * edge_capacity_factor(...)."""
    return westergaard_interior_stress(1.0, h, a, E, nu) / westergaard_edge_stress(1.0, h, a, E, nu, method=method)


def edge_line_load_stress(P_N_per_m, h, E=5e9, nu=0.33, k_found=RHO_W * G, edge="free"):
    """Max bending stress (Pa) in an ice sheet loaded by a line load along its edge (e.g. uplift/downdrag of
    a frozen-in hull, quay or pier as water level or cargo changes). Semi-infinite beam on elastic
    foundation (Hetenyi 1946): beta = (k/(4D))^(1/4); M_max = 0.3224 P/beta (free edge) or P/(2 beta)
    (clamped/rotation-fixed edge); sigma = 6M/h^2.
    DISAGREEMENT resolved: genius/repair_evo_a used M = 0.32 P l_c (l_c = characteristic_length), which is
    low by sqrt(2) because 1/beta = sqrt(2) l_c; audit_evo_2 used the Hetenyi form (adopted here).
    Source: genius/audit_evo_2/check5.py (3 kt uplift, 1.5-2 m ice -> 1.6-3.6 MPa vs 0.5-1 MPa flexural)."""
    _pos("P_N_per_m", P_N_per_m)
    _pos("h", h)
    D = E * h ** 3 / (12 * (1 - nu ** 2))
    beta = (k_found / (4 * D)) ** 0.25
    if edge == "free":
        M = 0.3224 * P_N_per_m / beta
    elif edge == "clamped":
        M = P_N_per_m / (2 * beta)
    else:
        raise ValueError("edge must be 'free' or 'clamped'")
    return 6 * M / h ** 2


def edge_line_load_capacity(sigma_allow, h, E=5e9, nu=0.33, edge="free"):
    """Line load (N/m) at which edge_line_load_stress reaches sigma_allow (e.g. flexural strength 0.5-1 MPa)."""
    _pos("sigma_allow", sigma_allow)
    return sigma_allow / edge_line_load_stress(1.0, h, E, nu, edge=edge)


# ------------------------------------------------------------------ buoyancy / uplift / depth
def ice_net_buoyancy(h):
    """Net buoyancy of floating fresh-water ice, kg per m2 = (rho_w - rho_i) h (83 kg/m2 per m)."""
    if h < 0:
        raise ValueError("h >= 0")
    return (RHO_W - RHO_I) * h


def stone_lift_capacity(h, surface_load_kg_m2=0.0, top_melt_m=0.0, frozen_on_sediment_m=0.0,
                        porosity=0.35, rho_stone=2650.0):
    """m3 of stone per m2 a floe can lift at ZERO freeboard (no margin):
    [ (rho_w-rho_i)(h - top_melt) - load - W'_frozen_sediment ] / (rho_stone - rho_w).
    Frozen-on sediment submerged weight = t[(1-n)(rho_s-rho_w) - n(rho_w-rho_i)].
    Neutral stone/ice volume ratio is only 83/1650 = 0.05. Source: round2/audit_b/c5_ice.py, critic_b, erp2_b."""
    if h < 0 or surface_load_kg_m2 < 0 or top_melt_m < 0 or frozen_on_sediment_m < 0:
        raise ValueError("inputs must be >= 0")
    Wsed = frozen_on_sediment_m * ((1 - porosity) * (rho_stone - RHO_W) - porosity * (RHO_W - RHO_I))
    B = (RHO_W - RHO_I) * max(h - top_melt_m, 0.0) - surface_load_kg_m2 - Wsed
    return B / (rho_stone - RHO_W)


def stacked_ice_capacity(h):
    """Thickness of ice blocks (m) that can be stacked on a floating sheet before its top floods:
    (rho_w-rho_i) h / rho_i (1.2-1.9 m sheet -> 0.11-0.17 m). Sawn ice cannot be 'sunk' and must be hauled.
    Source: genius/audit_final/audit_calc.py."""
    if h < 0:
        raise ValueError("h >= 0")
    return (RHO_W - RHO_I) * h / RHO_I


def ice_draft(h, rho_water=RHO_W):
    """Draft of floating ice, m = rho_i/rho_w h (0.917 h in fresh water)."""
    if h < 0:
        raise ValueError("h >= 0")
    return RHO_I / rho_water * h


def water_under_ice(water_depth, h_ice, level_drop=0.0):
    """Liquid water left under a floating sheet, m = (depth - level_drop) - 0.917 h.
    <= 0 means the backwater/pond/riffle freezes to the bed (and keeps freezing into it), so under-ice
    flow, fish wintering, process water and talik maintenance are gone. Source: audit_final, gate_7, critic_b."""
    if water_depth < 0 or h_ice < 0 or level_drop < 0:
        raise ValueError("inputs >= 0")
    return water_depth - level_drop - ice_draft(h_ice)


def freezes_to_bed(water_depth, FDD, alpha=0.024, level_drop=0.0):
    """True if the end-of-winter ice (alpha sqrt(FDD)) grounds in water of the given depth."""
    return water_under_ice(water_depth, ice_thickness(FDD, alpha), level_drop) <= 0.0


def required_depth_under_ice(h_ice, object_height, clearance=0.3):
    """Water depth needed to pass an object of given height under (or hull draft beside) a floating sheet:
    0.917 h + object_height + clearance, m. Source: round2/critic_b (1.2-2 m ice + 1.2 m pod -> 2.3-3.0 m)."""
    if object_height < 0 or clearance < 0:
        raise ValueError("inputs >= 0")
    return ice_draft(h_ice) + object_height + clearance


# ------------------------------------------------------------------ creep and shock
def glen_strain_rate(sigma_Pa, A=2.4e-24, n=3.0):
    """Ice creep strain rate 1/s = A sigma^n (Glen's law; A = 2.4e-24 Pa^-3 s^-1 at 0 C, Cuffey & Paterson).
    Warm (0 C) ice under ~0.5-2 MPa creeps percent-per-day: ice shells/beams are not rigid near 0 C.
    Source: round2/audit_b/c6_pod8.py."""
    if sigma_Pa < 0:
        raise ValueError("sigma >= 0")
    return A * sigma_Pa ** n


def snow_viscosity(rho_snow, T_C=0.0):
    """Compactive viscosity of snow, Pa s (Vionnet et al. 2012, Crocus): 7.62237e6 (rho/250) exp(0.1(-T) + 0.023 rho).
    Volumetric creep rate = stress/viscosity. Source: round2/audit_b/c3_pods.py, erp2_b."""
    if not 50 <= rho_snow <= 917:
        raise ValueError("rho_snow 50-917 kg/m3")
    if T_C > 0:
        raise ValueError("T_C <= 0")
    return 7.62237e6 * (rho_snow / 250.0) * math.exp(0.1 * (0.0 - T_C) + 0.023 * rho_snow)


def thermal_shock_stress(dT_K, E=9e9, alpha=5.1e-5, nu=0.33):
    """Restrained thermal stress in ice, Pa = E alpha dT/(1-nu). Cold ice (-35 C) put into 0 C water cracks
    (King & Fletcher: median cracking at -16 C; ice tensile strength 1-3 MPa). Source: round2/audit_b/c3_pods.py."""
    if dT_K < 0:
        raise ValueError("dT >= 0")
    return E * alpha * dT_K / (1 - nu)
