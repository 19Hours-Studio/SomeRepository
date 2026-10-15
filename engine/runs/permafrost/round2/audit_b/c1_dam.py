"""Checks for Idea 1 and Idea 11 (self-feeding ore-ice buttress dam)."""
import math

RHO_W = 1000.0
CW = 4.18e6          # J/m3/K volumetric heat capacity water
L_ICE = 334e3 * 917  # J per m3 of ice = 306 MJ/m3
print("latent heat per m3 ice MJ:", L_ICE / 1e6)

# --- thaw energy of a loose winter-hoisted pile (bulk ice 0.15) ---
for ice in (0.15,):
    for solids in (0.55, 0.65):
        for T in (-5, -10, -15, -20):
            c_vol = solids * 2.0e6 + ice * 1.9e6  # J/m3/K (rock ~2.0 MJ/m3K, ice 1.9)
            E = ice * L_ICE + c_vol * (-T)
            print(f"loose pile ice={ice} solids={solids} T={T}: E={E/1e6:.1f} MJ/m3")

# --- water ratio with 5-7 C water ---
def ratio(E, dT):
    return E / (CW * dT)

for E in (50e6, 55e6, 101e6):
    print(f"E={E/1e6:.0f} MJ/m3: full cooling 5C -> {ratio(E,5):.2f}, 7C -> {ratio(E,7):.2f}, 8C -> {ratio(E,8):.2f}, 9C -> {ratio(E,9):.2f}")
# effective dT implied by stated ranges
for E, r in ((50e6, 2.2), (55e6, 3.2), (101e6, 3.8), (101e6, 8.0), (101e6, 4.3), (101e6, 7.6)):
    print(f"stated ratio {r} for E={E/1e6:.0f}: implied effective dT = {E/(CW*r):.2f} K")

# --- loose pile cold content refreezing voids ---
for T in (-2, -5, -10, -20):
    for air_voids in (0.20, 0.25):
        c_vol = 0.62 * 2.0e6 + 0.15 * 1.9e6
        frozen_water = c_vol * (-T) / (334e3 * 1000)   # m3 water frozen per m3 pile
        print(f"T={T} voids={air_voids}: refreeze {frozen_water:.3f} m3/m3 = {100*frozen_water/air_voids:.0f}% of voids")

# --- 0.4 m spray-sealed lift freezing time ---
# saturated gravel lift, porosity 0.35 water -> latent 0.35*334e6 J/m3
Lv = 0.35 * 334e6
for Tair in (-20, -30, -40):
    for h in (15, 30):
        # Stefan with surface resistance, one-sided (top) : t = Lv*(X/h + X^2/(2k))/dT
        k = 2.5
        X = 0.4
        t1 = Lv * (X / h + X * X / (2 * k)) / (-Tair)
        # two-sided: top to air, bottom into cold pile (assume pile -15 C, k 2.0, pile semi-infinite approx -> treat as 0.2 m each side)
        Xh = 0.2
        t_top = Lv * (Xh / h + Xh * Xh / (2 * k)) / (-Tair)
        print(f"Tair={Tair} h={h}: one-sided {t1/3600:.1f} h, top half {t_top/3600:.1f} h")

# --- peat blanket thaw (Stefan) ---
for Tw, days in ((5, 90), (6, 90), (7, 90), (9, 90), (7, 110)):
    k_thawed = 0.5
    Lp = 0.80 * 334e6
    X = math.sqrt(2 * k_thawed * Tw * days * 86400 / Lp)
    print(f"peat under {Tw} C water for {days} d: thaw {X:.2f} m")

# --- Froehlich (1995) peak breach outflow Qp = 0.607 V^0.295 H^1.24 ---
def froehlich(V, H):
    return 0.607 * V ** 0.295 * H ** 1.24
def V_for(Q, H):
    return (Q / (0.607 * H ** 1.24)) ** (1 / 0.295)
for Q, H in ((34, 3), (144, 3), (144, 4), (128, 3), (128, 5), (460, 5), (460, 8)):
    print(f"Froehlich: Qp={Q} m3/s with H={H} m needs V={V_for(Q,H):,.0f} m3")
# season-long reservoir for 60,000 m3 at ratio 6.4 -> 384,000 m3 water
for V, H in ((384000, 3), (384000, 5), (384000, 8), (10000, 3)):
    print(f"Froehlich V={V:,} H={H}: {froehlich(V,H):.0f} m3/s")

# --- face thaw capacity 70 m/day: required heat transfer coefficient ---
for E in (50e6, 101e6):
    for dT in (5, 7):
        q = 70 * E / 86400
        print(f"70 m/day at E={E/1e6:.0f}: q={q/1e3:.1f} kW/m2, h needed at dT={dT}: {q/dT:.0f} W/m2K")

# --- Idea 11 season sizing ---
Q = 0.047
water_day = Q * 86400
for r in (4.3, 6.4, 7.6):
    days = 60000 * r / water_day
    print(f"47 L/s, ratio {r}: season {days:.0f} d, face retreat 0.8 m/d -> {0.8*days:.0f} m buttress")
print("daily water m3:", water_day)

# --- cost per gram ---
for c in (2.0, 4.65):
    for rec in (0.8, 0.85):
        print(f"${c}/m3 at 0.8 g/m3, recovery {rec}: ${c/(0.8*rec):.2f}/g")
print("ratio 4.65/2.0 =", 4.65 / 2.0, "; idea 11 ratio 6.7/1.3 =", 6.7 / 1.3)

# --- sliding safety factor of 3 m skin at end of season ---
gam_w = 9.81
for skin in (3.0, 5.0):
    for Hd in (3.5, 4.0):
        thrust = 0.5 * gam_w * 3.0 ** 2           # kN/m (3 m forebay)
        W = skin * Hd * 20.0                       # kN/m frozen ore 20 kN/m3
        uplift = 0.5 * gam_w * 3.0 * skin          # full triangular uplift if base seeps
        for mu in (0.5, 0.7):
            sf = mu * W / thrust
            sf_u = mu * (W - uplift) / thrust
            print(f"skin {skin} m, height {Hd} m, mu {mu}: SF {sf:.1f} (with uplift {sf_u:.1f})")
