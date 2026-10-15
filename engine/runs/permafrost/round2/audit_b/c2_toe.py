"""Checks for Idea 2 (solar-pond self-dosing pile): Shields, transport capacity, heat-exchange length, solar pond."""
import math

g = 9.81
rho = 1000.0
s = 2.65
nu = 1.75e-6  # water near 1 C

# --- shear stress and Shields-critical size ---
def depth_for(Q, w, S, n=0.035):
    # Manning, rectangular channel, solve for depth
    lo, hi = 1e-3, 2.0
    for _ in range(100):
        h = 0.5 * (lo + hi)
        A = w * h
        P = w + 2 * h
        R = A / P
        V = (1 / n) * R ** (2 / 3) * S ** 0.5
        if V * A > Q:
            hi = h
        else:
            lo = h
    return h, R, Q / (w * h)

for Q in (0.047, 0.100):
    for S in (0.05, 0.08):
        for w in (0.5, 1.0):
            h, R, V = depth_for(Q, w, S)
            tau = rho * g * R * S
            d_c045 = tau / (0.045 * (s - 1) * rho * g)
            thc = 0.15 * S ** 0.25          # Lamb et al. 2008 slope-dependent critical Shields
            d_lamb = tau / (thc * (s - 1) * rho * g)
            print(f"Q={Q*1000:.0f} L/s S={S} w={w}: h={h*100:.1f} cm R={R*100:.1f} cm V={V:.2f} m/s tau={tau:.0f} Pa "
                  f"d_crit(0.045)={d_c045*1000:.0f} mm, d_crit(Lamb th={thc:.3f})={d_lamb*1000:.0f} mm")

# --- bedload transport capacity (Meyer-Peter Mueller, Wong-Parker 2006 coefficient) ---
def mpm_qs(tau, d, thc=0.047, coef=3.97, exp=1.5):
    th = tau / ((s - 1) * rho * g * d)
    if th <= thc:
        return 0.0
    return coef * (th - thc) ** exp * math.sqrt((s - 1) * g * d ** 3)  # m2/s solids

print("\nTransport capacity (solids m3/s per channel) vs feed")
for Q in (0.047, 0.100):
    for S in (0.05, 0.08):
        w = 1.0
        h, R, V = depth_for(Q, w, S)
        tau = rho * g * R * S
        for d in (0.005, 0.010, 0.020, 0.030):
            q_wp = mpm_qs(tau, d) * w
            q_mpm = mpm_qs(tau, d, coef=8.0) * w
            bulk_day_wp = q_wp / 0.65 * 86400
            bulk_day_mpm = q_mpm / 0.65 * 86400
            print(f"Q={Q*1000:.0f} S={S} d50={d*1000:.0f}mm tau={tau:.0f}: capacity {bulk_day_wp:.0f} (WP) / {bulk_day_mpm:.0f} (MPM) bulk m3/day")

# required feed: 123,000 m3/season; season length from water use
for E in (101e6, 60e6):
    for Qw in (0.047, 0.100):
        dT = 9.0  # warmed water ~ 4 + 5
        r = E / (4.18e6 * dT)
        feed_day = Qw * 86400 / r
        days = 123000 / feed_day
        print(f"E={E/1e6:.0f}, Q={Qw*1000:.0f} L/s, 9C: water ratio {r:.2f}, feed {feed_day:.0f} m3/day -> {days:.0f} days for 123,000 m3")

# --- heat exchange e-folding length in toe channel ---
k_w = 0.57
Pr = 13.0
print("\nE-folding length")
for Q in (0.047, 0.100):
    for S in (0.05, 0.08):
        w = 1.0
        h, R, V = depth_for(Q, w, S)
        Dh = 4 * R
        Re = V * Dh / nu
        Nu = 0.023 * Re ** 0.8 * Pr ** 0.4
        hc = Nu * k_w / Dh
        for P_contact in (0.5, 1.0 + 2 * h):  # one wall only vs full wetted perimeter on frozen material
            for rough in (1.0, 3.0):
                Lef = Q * 4.18e6 / (rough * hc * P_contact)
                print(f"Q={Q*1000:.0f} S={S}: Re={Re:.2e} h_c={hc:.0f} W/m2K, contact P={P_contact:.2f} m, roughness x{rough}: L_e={Lef:.0f} m")

# --- solar pond energy needed ---
print("\nSolar pond")
for Q in (0.047, 0.100):
    for dT in (4, 6):
        P = Q * 4.18e6 * dT
        for A in (7000, 15000):
            print(f"Q={Q*1000:.0f} L/s dT={dT} K: {P/1e6:.2f} MW, area {A} m2 -> {P/A:.0f} W/m2 net gain needed")
# Oymyakon July global radiation 611.7 MJ/m2/month (dnaop table via search) -> W/m2
print("July Oymyakon mean GHI W/m2:", 611.7e6 / (31 * 86400))
# residence time
for A in (7000, 15000):
    for Q in (0.047, 0.100):
        print(f"pond {A} m2 x 0.4 m, Q {Q*1000:.0f} L/s: residence {A*0.4/(Q*86400):.2f} d")

# ratio checks
print("\n123000/54500 =", 123000 / 54500, "; (4+5)/4 =", 9 / 4, "; (4+4)/4 =", 8 / 4, "; (4+6)/4 =", 10 / 4)
for r in (2.4, 12.1):
    print(f"face water ratio {r} for E=101 => dT = {101e6/(4.18e6*r):.1f} K")
