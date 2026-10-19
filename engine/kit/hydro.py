"""Hydraulics and sediment: open-channel flow, Shields threshold, bedload capacity, jets, pumping and
hydro-elevator power, turbidity (full-mixing increment vs fishery limit, silt curtain), breach outflow,
waves, settling, aeolian threshold, discharge scaling, pipe friction, crude viscosity.

SI units (m, s, kg, Pa, W). Concentrations in mg/L (= g/m3).
"""
import math

from . import data

G, RHO_W = data.G, data.RHO_W


def _pos(name, v):
    if v is None or not v > 0:
        raise ValueError(f"{name} must be > 0 (got {v})")


# ------------------------------------------------------------------ open channels
def manning_velocity(R_h, S, n=0.035):
    """Manning mean velocity V = R^(2/3) S^(1/2)/n, m/s (n 0.03-0.04 gravel channels)."""
    for nm, v in (("R_h", R_h), ("S", S), ("n", n)):
        _pos(nm, v)
    return R_h ** (2.0 / 3.0) * math.sqrt(S) / n


def manning_depth_rect(Q, width, S, n=0.035):
    """Normal depth in a rectangular channel by Manning; returns (depth, hydraulic radius, velocity).
    Source: round2/audit_b/c2_toe.py, rt_b/calc_idea2.py."""
    for nm, v in (("Q", Q), ("width", width), ("S", S), ("n", n)):
        _pos(nm, v)
    lo, hi = 1e-5, 50.0
    for _ in range(120):
        h = 0.5 * (lo + hi)
        A = width * h
        R = A / (width + 2 * h)
        if A * manning_velocity(R, S, n) > Q:
            hi = h
        else:
            lo = h
    h = 0.5 * (lo + hi)
    R = width * h / (width + 2 * h)
    return h, R, Q / (width * h)


def manning_discharge_rect(width, depth, S, n=0.035):
    """Discharge m3/s of a rectangular channel at normal depth (e.g. flow needed to keep a canal at draft depth).
    Source: genius/gate_2, gate_3 (manning_Q)."""
    for nm, v in (("width", width), ("depth", depth)):
        _pos(nm, v)
    A = width * depth
    return A * manning_velocity(A / (width + 2 * depth), S, n)


def bed_shear_stress(R_h, S, rho=RHO_W):
    """Mean bed shear stress tau = rho g R S, Pa."""
    _pos("R_h", R_h)
    _pos("S", S)
    return rho * G * R_h * S


# ------------------------------------------------------------------ sediment threshold and transport
def shields_parameter(tau, d, rho_s=2650.0, rho=RHO_W):
    """Shields number theta = tau / ((rho_s - rho) g d)."""
    _pos("tau", tau)
    _pos("d", d)
    return tau / ((rho_s - rho) * G * d)


def critical_shields_soulsby(d, rho_s=2650.0, rho=RHO_W, nu=1.5e-6):
    """Critical Shields number (Soulsby & Whitehouse 1997): theta_c = 0.30/(1+1.2 D*) + 0.055(1-exp(-0.020 D*)),
    D* = d (g (s-1)/nu^2)^(1/3). Gravel limit ~0.055; gate_5 used it for wave threshold."""
    _pos("d", d)
    Dst = d * (G * (rho_s / rho - 1) / nu ** 2) ** (1.0 / 3.0)
    return 0.30 / (1 + 1.2 * Dst) + 0.055 * (1 - math.exp(-0.020 * Dst))


def critical_shields_slope(S):
    """Slope-dependent critical Shields number for steep channels theta_c = 0.15 S^0.25 (Lamb et al. 2008,
    JGR 113:F02008); 0.071-0.080 at S 0.05-0.08 instead of 0.045. Source: round2/audit_b/c2_toe.py."""
    _pos("S", S)
    if S > 0.3:
        raise ValueError("Lamb et al. calibrated to S <= ~0.3")
    return 0.15 * S ** 0.25


def critical_grain_size(tau, theta_c=0.045, rho_s=2650.0, rho=RHO_W):
    """Largest grain (m) a flow with bed shear tau can move: d = tau/(theta_c (rho_s-rho) g).
    Source: round2/rt_b/calc_idea2.py (47 L/s toe channel: 30 Pa, ~42 mm)."""
    _pos("tau", tau)
    _pos("theta_c", theta_c)
    return tau / (theta_c * (rho_s - rho) * G)


def bedload_capacity(tau, d, rho_s=2650.0, rho=RHO_W, method="wong_parker", theta_c=None):
    """Bedload transport capacity per metre width, m2/s of solids (multiply by width and
    86400/(1-porosity) for bulk m3/day).

    method 'wong_parker' (default): q* = 3.97 (theta - 0.0495)^1.5 (Wong & Parker 2006, J Hydraul Eng 132:1159,
    a reanalysis of Meyer-Peter-Mueller's own data); 'mpm': q* = 8 (theta - 0.047)^1.5 (original 1948).
    DISAGREEMENT resolved: genius/gate_3, gate_4, repair_evo_a used MPM (8); round2/audit_b used WP 3.97 -
    MPM overpredicts ~2x, WP adopted. q = q* sqrt((s-1) g d^3).
    Key screening fact: gravity transport of thawed gravel needs 14-145 m3 water per m3 gravel at slopes
    0.05-0.08 (audit_b), far above sluice water (3-10 m3/m3).
    """
    if method == "wong_parker":
        coef, tc = 3.97, 0.0495 if theta_c is None else theta_c
    elif method == "mpm":
        coef, tc = 8.0, 0.047 if theta_c is None else theta_c
    else:
        raise ValueError("method 'wong_parker' or 'mpm'")
    th = shields_parameter(tau, d, rho_s, rho)
    if th <= tc:
        return 0.0
    return coef * (th - tc) ** 1.5 * math.sqrt((rho_s / rho - 1) * G * d ** 3)


# ------------------------------------------------------------------ jets, pumps, lifts
def jet_centreline_velocity(u0, d0, x, K=6.2):
    """Centreline velocity of a SUBMERGED round turbulent jet, m/s: u_c = u0 K d0/x beyond the potential core
    (x > K d0), u0 inside it. K ~6 (5.8-6.5): Rajaratnam 1976 'Turbulent Jets'; fitted B=6.02 in arXiv
    2608.30900. A jet of creek water under water loses 90% of its velocity within ~60 nozzle diameters, so
    face-sweeping monitors in flooded workings act only near the nozzle. Water jets in AIR (hydraulic
    monitors) stay compact much longer: working length 350-450 d (monitor_working_length)."""
    for nm, v in (("u0", u0), ("d0", d0), ("x", x)):
        _pos(nm, v)
    return u0 if x <= K * d0 else u0 * K * d0 / x


def monitor_working_length(d_nozzle):
    """Effective working range (m) of a hydraulic monitor jet in air: 350-450 nozzle diameters -> (low, high).
    Source: genius/audit_evo_2 (50-75 mm nozzles -> 18-34 m)."""
    _pos("d_nozzle", d_nozzle)
    return 350 * d_nozzle, 450 * d_nozzle


def pumping_power(Q, head, eta=0.75, rho=RHO_W):
    """Shaft power W = rho g Q H / eta (head in m of the pumped fluid). For a pressure rise dp use head = dp/(rho g).
    Source: textbook; gate_2 (6 m3 at 2 MPa / 0.7 = 17 MJ per m3 of ground)."""
    for nm, v in (("Q", Q), ("head", head), ("eta", eta), ("rho", rho)):
        _pos(nm, v)
    if eta > 1:
        raise ValueError("eta <= 1")
    return rho * G * Q * head / eta


def hydro_elevator_power(Q_slurry, lift, rho_slurry=1300.0, eta=0.25):
    """Power W to lift slurry with a hydro-elevator (jet pump) = rho_s g Q H / eta, eta 0.17-0.35
    (Pak 1959; Veselov 1956; best swirl designs ~0.41) - 3x a centrifugal pump. data 'limit.hydro_elevator_efficiency'."""
    if not 0.05 <= eta <= 0.5:
        raise ValueError("hydro-elevator efficiency outside 0.05-0.5")
    return pumping_power(Q_slurry, lift, eta, rho_slurry)


# ------------------------------------------------------------------ turbidity vs fishery limits
def fines_release_rate(solids_m3_h, bulk_density_t_m3, fines_frac, escape_frac):
    """Mass rate of fines escaping to the water, kg/s = solids (m3/h) x density x fines fraction x escape.
    Escape: cutterhead resuspension 0.02-3.9% (Nakai 1978), hydraulic-dredge mean 0.77%; plant tailings
    return ALL fines unless contained. Source: genius/audit_evo_1/idea2_check.py (600 m3/h, 1.9 t/m3, 30%,
    0.5% -> 0.48 kg/s)."""
    for nm, v in (("solids_m3_h", solids_m3_h), ("bulk_density_t_m3", bulk_density_t_m3)):
        _pos(nm, v)
    if not 0 <= fines_frac <= 1 or not 0 <= escape_frac <= 1:
        raise ValueError("fractions 0-1")
    return solids_m3_h * bulk_density_t_m3 * 1000.0 / 3600.0 * fines_frac * escape_frac


def full_mixing_increment(mass_rate_kg_s, Q_m3_s):
    """Suspended-solids increment (mg/L) if a release mixes completely into river discharge Q:
    dC = m/Q x 1000. OPTIMISTIC bound: compliance with the fishery limit (+0.25 mg/L, Minselkhoz Order
    552/2016) is judged at a control section near the source, long before full mixing (see mixing_length)."""
    if mass_rate_kg_s < 0:
        raise ValueError("mass rate >= 0")
    _pos("Q_m3_s", Q_m3_s)
    return mass_rate_kg_s / Q_m3_s * 1000.0


def dilution_flow_required(mass_rate_kg_s, limit_mg_L=0.25):
    """Discharge (m3/s) that must fully mix a release to stay within the increment limit: Q = m/limit."""
    _pos("limit_mg_L", limit_mg_L)
    return mass_rate_kg_s * 1000.0 / limit_mg_L


def allowed_escape_fraction(limit_mg_L, Q_m3_s, solids_kg_s, fines_frac):
    """Largest fraction of the fines that may escape while the fully-mixed increment stays <= limit."""
    _pos("solids_kg_s", solids_kg_s)
    _pos("fines_frac", fines_frac)
    return limit_mg_L / 1000.0 * Q_m3_s / (solids_kg_s * fines_frac)


def silt_curtain_outside(c_inside_mg_L, efficiency=0.45):
    """Concentration outside a silt curtain = c_in (1 - efficiency). Design targets (HK EPD EIA): floating
    curtain alone 0.45, cage-type 0.80, combined 0.61-0.95; hanging curtains in crossflow often ineffective
    (ASCE JWPCOE 2015) and gaps leak. Under ice or in current, do not assume > 0.45 without a field test."""
    if c_inside_mg_L < 0 or not 0 <= efficiency < 1:
        raise ValueError("c >= 0, 0 <= efficiency < 1")
    return c_inside_mg_L * (1.0 - efficiency)


def transverse_mixing_coefficient(depth, u_star, c=0.6):
    """Transverse turbulent mixing coefficient eps_y = c d u*, m2/s (c ~0.6, range 0.3-1.0 for natural
    channels; Fischer et al. 1979 Mixing in Inland and Coastal Waters, ch.5). u* = sqrt(g R S)."""
    _pos("depth", depth)
    _pos("u_star", u_star)
    return c * depth * u_star


def mixing_length(U, width, eps_y, source="bank"):
    """Distance (m) for a continuous release to become fully mixed across a river (Fischer et al. 1979):
    L = 0.4 U W^2/eps_y for a bank (side) source, 0.1 U W^2/eps_y for a centre-line source. Wide Arctic
    rivers need tens-hundreds of km: within that distance the plume is far above the fully-mixed value."""
    for nm, v in (("U", U), ("width", width), ("eps_y", eps_y)):
        _pos(nm, v)
    k = {"bank": 0.4, "centre": 0.1}.get(source)
    if k is None:
        raise ValueError("source 'bank' or 'centre'")
    return k * U * width ** 2 / eps_y


# ------------------------------------------------------------------ hazards, waves, particles
def froehlich_peak_outflow(volume_m3, head_m):
    """Dam/forebay breach peak outflow Qp = 0.607 V^0.295 H^1.24, m3/s (Froehlich 1995). Fitted to heads
    >= ~3.4 m and large volumes; extrapolation to small forebays is rough. Source: round2/audit_b, erp2_b,
    repair/b (8,000 m3 at 3 m -> 34 m3/s). Seyba placer dam failure (Oct 2019) killed >= 15."""
    _pos("volume_m3", volume_m3)
    _pos("head_m", head_m)
    return 0.607 * volume_m3 ** 0.295 * head_m ** 1.24


def wave_growth_cem(U10, fetch_m):
    """Fetch-limited deep-water wave height and peak period (USACE Coastal Engineering Manual 2002, II-2):
    Cd = 0.001(1.1+0.035 U10), u* = U10 sqrt(Cd), g Hm0/u*^2 = 4.13e-2 (gF/u*^2)^0.5,
    g Tp/u* = 0.651 (gF/u*^2)^(1/3). Returns (Hm0 m, Tp s). Preferred over the older SPM form used in
    repair/b (similar answers). Source: genius/gate_5."""
    _pos("U10", U10)
    _pos("fetch_m", fetch_m)
    us = U10 * math.sqrt(0.001 * (1.1 + 0.035 * U10))
    X = G * fetch_m / us ** 2
    return 4.13e-2 * X ** 0.5 * us ** 2 / G, 0.651 * X ** (1.0 / 3.0) * us / G


def wavenumber(T, depth):
    """Linear-wave wavenumber k (1/m) from the dispersion relation w^2 = g k tanh(k h)."""
    _pos("T", T)
    _pos("depth", depth)
    w = 2 * math.pi / T
    k = w * w / G
    for _ in range(200):
        k = w * w / (G * math.tanh(k * depth))
    return k


def wave_orbital_velocity(H, T, depth):
    """Near-bed orbital velocity amplitude (linear theory) u_b = pi H / (T sinh(k h)), m/s.
    Small-pond waves (fetch < 1 km) give < 0.03 m/s at 1 m depth: no wave sorting of a placer bed."""
    _pos("H", H)
    return math.pi * H / (T * math.sinh(wavenumber(T, depth) * depth))


def settling_velocity(d, rho_p, rho_f=1.4, mu=1.62e-5):
    """Terminal settling velocity of a sphere, m/s, with Schiller-Naumann drag Cd = 24/Re (1+0.15 Re^0.687)
    (Re < 800). Defaults: cold air (rho 1.4, mu 1.62e-5); for water use rho_f 1000, mu 1.7e-3.
    Source: round2/audit_b/c4_deflation.py (gold 10-20 um in air 0.06-0.24 m/s)."""
    _pos("d", d)
    if rho_p <= rho_f:
        raise ValueError("particle must be denser than fluid")
    w = (rho_p - rho_f) * G * d * d / (18 * mu)
    for _ in range(500):
        Re = rho_f * w * d / mu
        w_new = (rho_p - rho_f) * G * d * d / (18 * mu * (1 + 0.15 * Re ** 0.687))
        if abs(w_new - w) < 1e-12:
            break
        w = 0.5 * (w + w_new)
    if rho_f * w * d / mu > 800:
        raise ValueError("Re > 800: outside Schiller-Naumann range")
    return w


def aeolian_threshold_ustar(d, rho_p, rho_air=1.23, A_N=0.0123, gamma=3e-4):
    """Saltation threshold friction velocity u*t = sqrt(A_N (rho_p/rho_a g d + gamma/(rho_a d))), m/s
    (Shao & Lu 2000, JGR 105:22437). gamma 1.65e-4..5e-4 N/m (cohesion).
    DISAGREEMENT resolved: repair/b used A_N 0.0111, gamma 2.9e-4; the published Shao & Lu values 0.0123 and
    3e-4 (used in audit_b, critic_b, erp2_b, rt_b) are adopted. Quartz 25-500 um and fine gold have
    near-identical thresholds (0.34-0.37 m/s): wind does not separate gold from sand."""
    _pos("d", d)
    _pos("rho_p", rho_p)
    return math.sqrt(A_N * (rho_p / rho_air * G * d + gamma / (rho_air * d)))


# ------------------------------------------------------------------ discharge, pipes, oil
def velocity_from_discharge(v_ref, Q_ref, Q, m=0.34):
    """At-a-station hydraulic geometry v = v_ref (Q/Q_ref)^m (Leopold & Maddock 1953, m ~0.34).
    Winter under-ice velocities are far below summer means (Lena delta 0.05-0.25 m/s measured)."""
    for nm, v in (("v_ref", v_ref), ("Q_ref", Q_ref), ("Q", Q)):
        _pos(nm, v)
    return v_ref * (Q / Q_ref) ** m


def runoff_mean_discharge(area_km2, runoff_mm_per_yr):
    """Mean discharge m3/s from basin area and annual runoff depth. Central Yakutia 1-80 mm/yr; Kolyma ~190.
    Source: genius/gate_3 (1,000 km2 x 80 mm -> 2.5 m3/s)."""
    _pos("area_km2", area_km2)
    if runoff_mm_per_yr < 0:
        raise ValueError("runoff >= 0")
    return area_km2 * 1e6 * runoff_mm_per_yr / 1000.0 / (365.25 * 86400)


def pipe_pressure_drop(Q, D, L, nu, rho):
    """Darcy-Weisbach friction loss in a full pipe, Pa: f = 64/Re (Re < 2300) or Blasius 0.316 Re^-0.25
    (4e3 < Re < 1e5); transitional 2300-4000 raises ValueError. Source: genius/gate_2 (ESPO crude in 0.1 m
    hose at -57.8 C, 124 cSt -> 51 bar/15 km friction)."""
    for nm, v in (("Q", Q), ("D", D), ("L", L), ("nu", nu), ("rho", rho)):
        _pos(nm, v)
    A = math.pi * D * D / 4
    V = Q / A
    Re = V * D / nu
    if Re < 2300:
        f = 64.0 / Re
    elif 4000 <= Re <= 1e5:
        f = 0.316 * Re ** -0.25
    else:
        raise ValueError(f"Re={Re:.0f} outside laminar/Blasius range")
    return f * L / D * rho * V * V / 2.0


def walther_slope(nu1_cSt, T1_C, nu2_cSt, T2_C):
    """ASTM D341 (Walther) slope B from two kinematic viscosities: log log(nu+0.7) = A - B log T."""
    Z = lambda nu: math.log10(math.log10(nu + 0.7))
    return (Z(nu1_cSt) - Z(nu2_cSt)) / (math.log10(T2_C + 273.15) - math.log10(T1_C + 273.15))


def walther_viscosity(nu_ref_cSt, T_ref_C, T_C, B):
    """Kinematic viscosity (cSt) at T from a reference point and Walther slope B (ASTM D341).
    Valid above the pour point only (light E-Siberian crude pour point ~-40 C). Source: genius/gate_2, gate_9."""
    _pos("nu_ref_cSt", nu_ref_cSt)
    Z = math.log10(math.log10(nu_ref_cSt + 0.7)) + B * (math.log10(T_ref_C + 273.15) - math.log10(T_C + 273.15))
    return 10 ** (10 ** Z) - 0.7
