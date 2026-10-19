"""Floating bodies: displacement, draught vs payload, waterplane rise per tonne, depth needed under ice,
net buoyancy and its drift (melt, compressible air), drag and the stall window of objects pressed against
an ice ceiling.

SI units; masses in tonnes where the name says _t, else kg.
"""
import math

from . import data

RHO_W, RHO_I, G = data.RHO_W, data.RHO_ICE, data.G


def _pos(name, v):
    if v is None or not v > 0:
        raise ValueError(f"{name} must be > 0 (got {v})")


def displacement_t(L, B, T, Cb=0.9, rho=RHO_W):
    """Displacement (t) = rho L B T Cb / 1000 (Cb 0.85-0.9 river barges, ~1.0 pontoons).
    Source: genius/audit_evo_1/idea34_check.py (130x14x3 m -> 4.6-5.2 kt)."""
    for nm, v in (("L", L), ("B", B), ("T", T), ("Cb", Cb)):
        _pos(nm, v)
    if Cb > 1.0:
        raise ValueError("Cb <= 1")
    return rho * L * B * T * Cb / 1000.0


def draught(total_mass_t, L, B, Cb=0.9, rho=RHO_W):
    """Draught (m) for a total mass (lightship + payload) in tonnes: T = m/(rho L B Cb)."""
    _pos("total_mass_t", total_mass_t)
    return total_mass_t * 1000.0 / (rho * L * B * Cb)


def draught_from_payload(payload_t, L, B, Cb=0.88, light_frac=0.22, rho=RHO_W):
    """Draught (m) when lightship ~ light_frac x payload (dumb river barges ~0.2-0.25).
    Source: genius/repair_final/calc.py (8 kt hold in 130x22 m -> 3.9 m vs 1.5-2 m Arctic rivers)."""
    return draught(payload_t * (1 + light_frac), L, B, Cb, rho)


def payload_at_draught(L, B, T, lightship_t, Cb=0.9, rho=RHO_W):
    """Payload (t) at a draught limited by guaranteed river depth = displacement - lightship.
    Lena guaranteed depths 2.0-2.9 m, upper Lena ~1 m in low water (data 'river.guaranteed_depth_lena')."""
    return displacement_t(L, B, T, Cb, rho) - lightship_t


def rise_per_tonne(waterplane_area_m2, rho=RHO_W):
    """Change of draught per tonne loaded/unloaded, m/t = 1000/(rho Awp) (wall-sided hull).
    Source: genius/audit_evo_2 (Awp 2,878 m2: burning 3 kt of bunker coal lifts the hull 1.05 m - it cracks
    the ice it is frozen into)."""
    _pos("waterplane_area_m2", waterplane_area_m2)
    return 1000.0 / (rho * waterplane_area_m2)


def tonnes_per_cm(waterplane_area_m2, rho=RHO_W):
    """Tonnes per centimetre immersion = rho Awp / 1e5."""
    _pos("waterplane_area_m2", waterplane_area_m2)
    return rho * waterplane_area_m2 / 1e5


def depth_needed(draft, h_ice=0.0, under_keel_clearance=0.4, under_ice=False):
    """Water depth (m) needed at winter low water.

    Frozen-in / wintering hull (under_ice=False): max(draft, 0.917 h_ice) + clearance - the hull must float
    and the surrounding ice must not ground (shallow backwaters freeze to the bed).
    Object passing BELOW an ice cover (under_ice=True: pods, towed strings): 0.917 h_ice + draft + clearance.
    Source: genius/audit_evo_2 (3.3 m loaded draught + 0.5 m -> ~3.8 m vs shallow-river backwaters),
    round2/critic_b (1.2-2 m ice + 1.2 m pod -> 2.3-3.0 m at every riffle)."""
    _pos("draft", draft)
    if h_ice < 0 or under_keel_clearance < 0:
        raise ValueError("inputs >= 0")
    ice_d = RHO_I / RHO_W * h_ice
    if under_ice:
        return ice_d + draft + under_keel_clearance
    return max(draft, ice_d) + under_keel_clearance


def net_buoyancy_kg(volume_m3, mass_kg, rho=RHO_W):
    """Net buoyancy (kg, + floats, - sinks) = rho V - m."""
    _pos("volume_m3", volume_m3)
    if mass_kg < 0:
        raise ValueError("mass >= 0")
    return rho * volume_m3 - mass_kg


def buoyancy_loss_from_melt(area_m2, melt_m):
    """Net buoyancy lost (kg) when melt_m of an ice shell of given area melts: area x melt x (rho_w - rho_i).
    Source: round2/audit_b c3_pods, critic_b (39.3 m2, 6 cm per 45 d -> 4.35 kg/day vs a +3..+9 kg trim)."""
    if area_m2 < 0 or melt_m < 0:
        raise ValueError("inputs >= 0")
    return area_m2 * melt_m * (RHO_W - RHO_I)


def air_buoyancy_change_per_m(air_volume_m3, depth_m=0.0, p_atm=101325.0, rho=RHO_W):
    """Buoyancy change (kg) per metre of extra depth for a COMPRESSIBLE air/snow pocket (isothermal Boyle):
    dB/dz = rho V rho g / p(z). A flexible pod is a Cartesian diver (unstable); 5.4 m3 air -> ~520 kg/m
    (round2/erp2_b). Rigid shells avoid it."""
    _pos("air_volume_m3", air_volume_m3)
    p = p_atm + rho * G * depth_m
    return rho * air_volume_m3 * rho * G / p


def drag_force(U, area_m2, Cd=1.0, rho=RHO_W):
    """Drag N = 0.5 rho Cd A U^2 (bluff box ~1-2, sphere 0.47, streamlined 0.1-0.2)."""
    if U < 0:
        raise ValueError("U >= 0")
    _pos("area_m2", area_m2)
    return 0.5 * rho * Cd * area_m2 * U * U


def max_buoyancy_to_slide(U, area_m2, Cd=1.0, mu=0.5, rho=RHO_W):
    """Largest net buoyancy (kg) an object pressed against an ice ceiling can have and still be dragged along
    by current U: B_max = drag/(mu g). mu ice-ice near 0 C 0.15-0.76 (0.5 slow, with hold time),
    hull/polymer 0.02-0.47. Stalled objects freeze in within hours-days (ice basal growth 1-2 cm/day).
    Source: repair/b/idea4_pods.py, round2/rt_b, roast."""
    _pos("mu", mu)
    return drag_force(U, area_m2, Cd, rho) / (mu * G)


def slide_threshold_velocity(net_buoyancy_kg, area_m2, Cd=1.0, mu=0.5, rho=RHO_W):
    """Current speed (m/s relative to the object) at which drag = mu x net buoyancy weight:
    u = sqrt(2 mu B g/(rho Cd A)). Compare with MEASURED under-ice velocities (Lena delta 0.05-0.25 m/s)
    and remember near-ice flow is slower than the depth mean. Source: genius/gate_7, gate_8."""
    if net_buoyancy_kg < 0:
        raise ValueError("net buoyancy >= 0")
    _pos("area_m2", area_m2)
    return math.sqrt(2.0 * mu * net_buoyancy_kg * G / (rho * Cd * area_m2))
