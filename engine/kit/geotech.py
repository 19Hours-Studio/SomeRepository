"""Geotechnics of frozen and thawing ground: strength vs time (Vyalov), roof spans and pillars,
infinite-slope and thaw-consolidation slope stability, Bingham runout, consolidation time, adfreeze
strength vs temperature, seepage, sliding.

SI units: stresses in Pa unless the name ends in _MPa/_kPa; unit weights gamma in N/m3; lengths m; time s.
"""
import math

from . import data

G = data.G


def _pos(name, v):
    if v is None or not v > 0:
        raise ValueError(f"{name} must be > 0 (got {v})")


# ------------------------------------------------------------------ strength vs time
def vyalov_fit(sigma1, t1, sigma2, t2):
    """Fit Vyalov's long-term strength law sigma(t) = beta / ln(t/B) through two (strength, time) points.
    Returns (beta, B). Typical: short-term 1-2 MPa at ~60 s, long-term 0.2-0.5 MPa at 50 yr (frozen
    overburden in tension) or 5-8 MPa short / 1.5-2 MPa long in compression (frozen sandy gravel, -4 C).
    Source: Vyalov 1959/1986 (Tsytovich); genius/audit_evo_2/check5.py."""
    for n, v in (("sigma1", sigma1), ("t1", t1), ("sigma2", sigma2), ("t2", t2)):
        _pos(n, v)
    if not (t2 > t1 and sigma2 < sigma1):
        raise ValueError("need t2 > t1 and sigma2 < sigma1 (strength falls with time)")
    r = sigma1 / sigma2
    lnB = (math.log(t2) - r * math.log(t1)) / (1 - r)
    beta = sigma1 * (math.log(t1) - lnB)
    return beta, math.exp(lnB)


def vyalov_strength(t_s, beta, B):
    """Strength after load duration t: sigma = beta/ln(t/B) (same units as beta). Valid t > B*e."""
    _pos("t_s", t_s)
    if t_s <= B:
        raise ValueError("t must exceed B")
    return beta / math.log(t_s / B)


def vyalov_time_to_failure(sigma, beta, B):
    """Time (s) until a constant stress sigma fails frozen ground: t = B exp(beta/sigma).
    Spans orders of magnitude for small changes of the fitted long-term strength - quote a range."""
    _pos("sigma", sigma)
    return B * math.exp(beta / sigma)


# ------------------------------------------------------------------ beams, spans, pillars
def beam_self_weight_stress(gamma, span, thickness, support="fixed"):
    """Max bending stress (Pa) in a roof/bridge beam of frozen ground or ice loaded by its own weight
    (per unit width): fixed-fixed sigma = gamma L^2/(2h); simply supported 3 gamma L^2/(4h);
    cantilever 3 gamma L^2/h. Compare with tensile strength (frozen overburden 0.2-0.5 MPa long-term,
    1-2 MPa short-term; data 'ground.frozen_overburden_tensile').
    Source: genius/audit_evo_2/check1.py (19 kN/m3, 25 m span, 10 m cover -> 0.59 MPa), repair_evo_a/idea2.py."""
    for n, v in (("gamma", gamma), ("span", span), ("thickness", thickness)):
        _pos(n, v)
    k = {"fixed": 0.5, "simple": 0.75, "cantilever": 3.0}.get(support)
    if k is None:
        raise ValueError("support must be 'fixed', 'simple' or 'cantilever'")
    return k * gamma * span ** 2 / thickness


def critical_span(sigma_t, gamma, thickness, support="fixed"):
    """Span (m) at which beam_self_weight_stress reaches sigma_t."""
    _pos("sigma_t", sigma_t)
    return math.sqrt(sigma_t / beam_self_weight_stress(gamma, 1.0, thickness, support))


def pillar_tributary_stress(gamma, depth, extraction):
    """Average pillar stress by tributary area, Pa = gamma H / (1 - e), e = extraction ratio (0-1).
    Source: genius/gate_r1_2 (20 kN/m3, 30 m, 80% -> 3.0 MPa vs ~1.25 MPa long-term frozen gravel)."""
    _pos("gamma", gamma)
    _pos("depth", depth)
    if not 0 <= extraction < 1:
        raise ValueError("extraction in [0,1)")
    return gamma * depth / (1.0 - extraction)


def web_pillar_stress(gamma, depth, web_width, opening_width):
    """Tributary stress on a long web (strip) pillar between parallel openings (auger holes, rooms),
    Pa = gamma H (w + B)/w. Source: genius/audit_evo_1/idea34_check.py, repair_evo_a/idea3.py."""
    for n, v in (("gamma", gamma), ("depth", depth), ("web_width", web_width), ("opening_width", opening_width)):
        _pos(n, v)
    return gamma * depth * (web_width + opening_width) / web_width


def mark_bieniawski_strength(S1, width, height, length=math.inf):
    """Pillar strength (units of S1): S1 (0.64 + 0.54 w/h - 0.18 w^2/(L h)) (Mark-Bieniawski, NIOSH).
    For long strip webs (L -> inf) this is 0.64 + 0.54 w/h.
    DISAGREEMENT resolved: genius/repair_evo_a used 0.64 + 0.36 w/h (Bieniawski square-pillar formula),
    which understates strip/web strength; audit_evo_1 used the Mark-Bieniawski strip form (adopted).
    S1 = in-situ strength (coal ~6.2 MPa)."""
    for n, v in (("S1", S1), ("width", width), ("height", height), ("length", length)):
        _pos(n, v)
    corr = 0.0 if math.isinf(length) else 0.18 * width ** 2 / (length * height)
    return S1 * (0.64 + 0.54 * width / height - corr)


# ------------------------------------------------------------------ slopes and runout
def infinite_slope_fs(c, phi_deg, gamma, z, beta_deg, pore_ratio=0.0, gamma_w=1000 * G):
    """Infinite-slope factor of safety with seepage parallel to the slope:
    FS = [c + (gamma - m gamma_w) z cos^2 b tan phi] / (gamma z sin b cos b); m = pore_ratio (0 dry, 1
    water table at surface). c in Pa, gamma N/m3. Textbook (e.g. Duncan & Wright)."""
    for n, v in (("gamma", gamma), ("z", z)):
        _pos(n, v)
    if not 0 < beta_deg < 90 or c < 0 or not 0 <= pore_ratio <= 1:
        raise ValueError("0<beta<90, c>=0, 0<=pore_ratio<=1")
    b, p = math.radians(beta_deg), math.radians(phi_deg)
    return (c + (gamma - pore_ratio * gamma_w) * z * math.cos(b) ** 2 * math.tan(p)) / (gamma * z * math.sin(b) * math.cos(b))


def thaw_consolidation_ratio(thaw_depth, t_s, cv):
    """Morgenstern & Nixon (1971) thaw-consolidation ratio R = alpha/(2 sqrt(cv)), alpha = X/sqrt(t).
    R > ~1 means excess pore pressure builds faster than it drains. cv of thawed ice-rich silt
    1e-8..1e-6 m2/s. Source: genius/repair_evo_b/calc_idea2.py (1.6 m in 100 d, cv 1e-7 -> R 0.86)."""
    for n, v in (("thaw_depth", thaw_depth), ("t_s", t_s), ("cv", cv)):
        _pos(n, v)
    return thaw_depth / math.sqrt(t_s) / (2.0 * math.sqrt(cv))


def thawing_slope_fs(c, phi_deg, gamma, gamma_buoyant, z, beta_deg, R):
    """McRoberts & Morgenstern (1974) infinite thawing slope:
    FS = c/(gamma z sin b cos b) + (gamma'/gamma) tan phi / ((1 + 2R^2) tan b).
    Frictional threshold angle 1.8-6.4 deg for phi' 25-33, gamma'/gamma 0.4-0.5, R 0.9-1.6 (audit_evo_1).
    c in Pa, gammas in N/m3."""
    for n, v in (("gamma", gamma), ("gamma_buoyant", gamma_buoyant), ("z", z)):
        _pos(n, v)
    if not 0 < beta_deg < 90 or c < 0 or R < 0:
        raise ValueError("0<beta<90, c>=0, R>=0")
    b = math.radians(beta_deg)
    return c / (gamma * z * math.sin(b) * math.cos(b)) + (gamma_buoyant / gamma) * math.tan(math.radians(phi_deg)) / ((1 + 2 * R * R) * math.tan(b))


def thawing_slope_critical_thickness(c, phi_deg, gamma, gamma_buoyant, beta_deg, R):
    """Thawed-sheet thickness (m) at which thawing_slope_fs = 1 (cohesive sheets thinner than this stay put);
    inf if the frictional term alone keeps FS >= 1. Source: genius/audit_evo_1 (10 deg, c' 2 kPa, R 0.9 ->
    1.47 m vs 1.6 m seasonal thaw), repair_evo_b/calc_idea2b.py."""
    b = math.radians(beta_deg)
    fric = (gamma_buoyant / gamma) * math.tan(math.radians(phi_deg)) / ((1 + 2 * R * R) * math.tan(b))
    if fric >= 1:
        return math.inf
    return c / (gamma * math.sin(b) * math.cos(b) * (1 - fric))


def bingham_min_flow_thickness(tau_y, rho, beta_deg):
    """Minimum thickness (m) for a Bingham slurry layer to keep flowing on slope beta: h = tau_y/(rho g sin b).
    Thinner sheets stop and re-bury the toe (how thaw slumps stabilise). Thawed ice-rich muck has undrained
    strength 0.8-9 kPa (Harris et al. 1995). Source: genius/audit_evo_1 (rho 1600, 4 deg: 0.73-8.2 m)."""
    _pos("tau_y", tau_y)
    _pos("rho", rho)
    if not 0 < beta_deg < 90:
        raise ValueError("0<beta<90")
    return tau_y / (rho * G * math.sin(math.radians(beta_deg)))


def bingham_stop_angle(tau_y, rho, thickness):
    """Slope (deg) below which a Bingham layer of given thickness stops: asin(tau_y/(rho g h))."""
    _pos("thickness", thickness)
    s = tau_y / (rho * G * thickness)
    if s >= 1:
        return 90.0
    return math.degrees(math.asin(s))


def consolidation_t90(drainage_path, cv, Tv=0.848):
    """Time (s) to 90% primary consolidation t90 = 0.848 H^2/cv (Terzaghi; H = drainage path: full layer
    for single drainage, half for double). Source: genius/audit_evo_1 (5 m fill, cv 0.5-2.8 m2/yr -> 7.6-41 yr)."""
    _pos("drainage_path", drainage_path)
    _pos("cv", cv)
    return Tv * drainage_path ** 2 / cv


# ------------------------------------------------------------------ adfreeze
_ADFREEZE_KPA = {
    # SNiP 2.02.04-88 / Posobie Table 4.2 (dnaop.com/html/31372_5.html), design shear resistance along the
    # freezing surface Raf (kPa) vs ground temperature (C). Points at sand -2/-3 and clay -0.5/-1/-2/-3 were
    # also used in genius/gate_6 (SNiP) and audit_evo_1 (SP 25.13330).
    "clay": ((-0.3, 40), (-0.5, 60), (-1.0, 100), (-1.5, 130), (-2.0, 150), (-2.5, 180), (-3.0, 200),
             (-3.5, 230), (-4.0, 250)),
    "sand": ((-0.3, 50), (-0.5, 80), (-1.0, 130), (-1.5, 160), (-2.0, 200), (-2.5, 230), (-3.0, 260)),
}


def adfreeze_strength(T_C, soil="clay", surface_factor=1.0):
    """Design adfreeze (freezing-surface shear) strength Raf, Pa, linear interpolation in the SNiP/SP table.

    soil 'clay' (clays/silts, -0.3..-4 C) or 'sand' (-0.3..-3 C); surface_factor gamma_af multiplies the
    table (1.0 concrete/steel; ~0.9 treated timber). Outside the table -> ValueError (test per GOST
    12248.8-2020). Key screening fact: near 0 C (riverbanks washed by 10-15 C water, warm permafrost
    -0.1..-3.8 C in the upper Kolyma) Raf falls 3-4x from its -3 C value.
    """
    if soil not in _ADFREEZE_KPA:
        raise ValueError("soil must be 'clay' or 'sand'")
    tab = _ADFREEZE_KPA[soil]
    if not tab[-1][0] <= T_C <= tab[0][0]:
        raise ValueError(f"T {T_C} C outside table {tab[-1][0]}..{tab[0][0]} C for {soil}")
    for (t1, r1), (t2, r2) in zip(tab, tab[1:]):
        if t2 <= T_C <= t1:
            return 1e3 * surface_factor * (r1 + (r2 - r1) * (T_C - t1) / (t2 - t1))
    return 1e3 * surface_factor * tab[0][1]


def adfreeze_capacity(perimeter, frozen_length, T_C, soil="clay", surface_factor=1.0):
    """Pull-out/shear capacity (N) of an anchor/pile/embedded body = Raf(T) * perimeter * frozen length."""
    _pos("perimeter", perimeter)
    _pos("frozen_length", frozen_length)
    return adfreeze_strength(T_C, soil, surface_factor) * perimeter * frozen_length


# ------------------------------------------------------------------ water-retaining / sliding
def darcy_seepage(K, head, length, area):
    """Darcy seepage Q = K (H/L) A, m3/s (K m/s). Loose hoisted frozen rock K 1e-3..1e-1 m/s -> a 'frozen
    dam' of lumps leaks 0.09-8.5 m3/s (critic_b): it is not watertight unless ice-saturated."""
    for n, v in (("K", K), ("head", head), ("length", length), ("area", area)):
        _pos(n, v)
    return K * head / length * area


def hydrostatic_thrust(head, rho=1000.0):
    """Horizontal water thrust per metre of wall, N/m = 0.5 rho g H^2."""
    _pos("head", head)
    return 0.5 * rho * G * head ** 2


def sliding_fs(mu, weight_N, thrust_N, uplift_N=0.0):
    """Sliding safety factor of a gravity block/dam = mu (W - U)/T (all per metre)."""
    _pos("thrust_N", thrust_N)
    if mu < 0 or weight_N < 0 or uplift_N < 0:
        raise ValueError("mu, W, U >= 0")
    return mu * (weight_N - uplift_N) / thrust_N


def thaw_settlement(thaw_depth, thaw_strain):
    """Settlement (m) = thaw depth x thaw strain (ice-rich ground 0.1-0.4). Source: genius/gate_7 (strain 0.2)."""
    if thaw_depth < 0 or not 0 <= thaw_strain < 1:
        raise ValueError("thaw_depth >= 0, 0 <= strain < 1")
    return thaw_depth * thaw_strain
