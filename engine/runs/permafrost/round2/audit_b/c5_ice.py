"""Checks for Ideas 7, 9, 12 (ice boulder lift)."""
import math

NET = 1000 - 917  # kg/m2 per m of ice
SUB = 2650 - 1000  # submerged rock kg/m3
for h in (1.6, 1.7, 1.8, 3.1, 3.2, 3.3):
    print(f"ice {h} m: net lift {NET*h:.0f} kg/m2 -> {NET*h/SUB:.3f} m3 stone/m2")

print("\n--- freeze-on below ice after ice meets the bed (Stefan with ice + snow resistance) ---")
k_i, k_f, k_s = 2.2, 2.6, 0.3
for n in (0.30, 0.35):
    Lv = n * 334e6
    for FDD in (91, 300, 775):
        for h_ice in (1.7, 3.2):
            for snow in (0.0, 0.15, 0.30):
                R0 = h_ice / k_i + snow / k_s
                # Lv*(R0*X + X^2/(2k_f)) = FDD*86400
                a = Lv / (2 * k_f)
                b = Lv * R0
                c = -FDD * 86400
                X = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
                sub_w = (1 - n) * SUB - n * NET  # frozen gravel submerged weight kg/m3
                load = X * sub_w
                if FDD in (91, 775):
                    print(f"n={n} FDD={FDD} ice={h_ice} snow={snow}: X={X*100:.1f} cm, load {load:.0f} kg/m2 vs buoyancy {NET*h_ice:.0f}")

print("\n--- Idea 9: gap statistics ---")
D = 2.12
for h, lab in ((1.8, "mean"),):
    print(f"mean gap: {D - 0.917*h:.2f} m")
for sigma in (0.08, 0.12, 0.15, 0.20):
    h99 = 1.8 + 2.326 * sigma
    print(f"sigma {sigma}: 99% ice {h99:.2f} m -> gap {D-0.917*h99:.2f} m")
# Orajarvi CV 14% ; FDD CV ~ 8% -> sqrt -> 4%
print("FDD CV 8% -> ice CV", 0.5 * 8, "% -> sigma", 0.04 * 1.8)
print("Orajarvi measured CV:", 10 / 72)
# boulder thermal bridge (1D series bound)
z_top = D - 1.5          # boulder top depth below water surface
h_ice = 1.8
z_bot_ice = 0.917 * h_ice
R_ice = z_bot_ice / 2.2
for k_r in (2.5, 3.0, 3.5):
    zf = z_top + (R_ice - z_top / 2.2) * k_r
    print(f"k_rock={k_r}: 1D freezing isotherm beside rock column at {zf:.2f} m vs ice bottom {z_bot_ice:.2f} m, floor {D} m -> remaining gap {D-zf:.2f} m (design 0.30-0.47)")
# net lift statement 101-126 vs computed
print("1.8 m ice net lift:", NET * 1.8, "kg/m2; stated 101-126 implies effective ice", 101 / NET, 126 / NET, "m")
# boulder floe area
for Dm in (1.5, 2.5):
    Vb = math.pi / 6 * Dm ** 3
    Wsub = Vb * SUB
    print(f"sphere {Dm} m: {Vb:.2f} m3, submerged {Wsub:.0f} kg -> floe {Wsub/126:.0f}-{Wsub/101:.0f} m2; in air {Vb*2650:.0f} kg")
# ice plate characteristic length
for h in (1.7, 1.8, 3.2):
    for E in (2e9, 5e9):
        Dp = E * h ** 3 / (12 * (1 - 0.33 ** 2))
        l = (Dp / 9810) ** 0.25
        P03 = 8 * 0.3 * math.sqrt(Dp * 9810)
        print(f"ice {h} m E={E/1e9:.0f} GPa: characteristic length {l:.1f} m; point force to deflect 0.3 m: {P03/1e6:.1f} MN")

print("\n--- Idea 12 ---")
for h, X in ((1.7, 0.044), (3.2, 0.044)):
    sub_w = 0.65 * SUB - 0.35 * NET
    lift = (NET * h - X * sub_w) / SUB
    print(f"ice {h}: net after 4.4 cm freeze-on {(NET*h - X*sub_w):.0f} kg/m2 -> {lift:.3f} m3/m2")
Vb = math.pi / 6 * 0.8 ** 3
print(f"0.8 m sphere: {Vb:.3f} m3, submerged {Vb*SUB:.0f} kg, in air {Vb*2650:.0f} kg; 5-9 m2 x 95 kg/m2 = {5*95}-{9*95} kg")
# boulder spacing at cover 10-20%
for cov in (0.1, 0.2):
    print(f"cover {cov}: mean spacing of 0.8 m boulders ~{0.8*math.sqrt(math.pi/4/cov):.1f} m")
print("cost ratio idea12:", 2.7 / 5.7, 3.0 / 5.1, "; idea 7 claims $1 vs $6; idea 12 own ice cost 5.1-5.7 ->", 5.1 / 1, 5.7 / 1, "x idea 7")
# idea 9 cost
print("idea 9 ratio:", 4 / 2.5, 8 / 2.0, "; vs dozer push 2.7-3.0:", 2.7 / 2.5, 3.0 / 2.0)
