"""Idea 4 - Trimmed snow-buoyed under-ice ore pods."""
import math
rho_w, rho_i = 1000.0, 917.0
print("== 1. Snow per tonne (voids flooded vs sealed) ==")
cargo = {"coal": (1350, 0.82), "rock ore": (2700, 1.65), "sulphide": (4500, 2.6)}
for rs in (75, 100, 200, 300):
    row = []
    for name, (rho_o, bulk) in cargo.items():
        sub = 1000*(1 - rho_w/rho_o)    # submerged weight kg per t, voids flooded
        row.append(f"{name}: {sub/(rho_w-rs):.2f}")
    print(f" snow {rs} kg/m3 (voids flooded): " + ", ".join(row) + "  m3/t  (claim 0.28/0.74/0.86)")
for name, (rho_o, bulk) in cargo.items():
    sealed = 1000*(1 - 1.0/bulk)     # per t if voids are sealed air (bulk in t/m3)
    print(f" {name}: sealed bulk {bulk} t/m3 -> net {'weight' if sealed>0 else 'BUOYANCY'} {abs(sealed):.0f} kg per t without any snow")

print("\n== 2. 1 t pod stall check (claim 1-12 kg) ==")
for v in (0.1, 0.3):
    for CdA in (1.0, 1.3):
        F = 0.5*rho_w*CdA*v*v
        print(f" v={v} CdA={CdA}: drag {F:.1f} N -> max net buoyancy at mu=0.5: {F/0.5/9.81:.1f} kg")

print("\n== 3. 10 t fin pod 5.0 x 2.2 x 1.2 m ==")
a, b, c = 5.0, 2.2, 1.2
V = a*b*c
S = 2*(a*b + a*c + b*c)
print(f" envelope {V:.1f} m3 -> neutral total mass {V:.1f} t ; surface {S:.1f} m2")
for t in (0.08, 0.09, 0.10):
    Vin = (a-2*t)*(b-2*t)*(c-2*t)
    Vsh = V - Vin
    payload = V*1000 - rho_i*Vsh   # cargo + snow mass for neutral
    print(f" shell {t*100:.0f} cm: shell {Vsh:.2f} m3 ({Vsh*rho_i/1000:.2f} t), interior {Vin:.2f} m3, cargo+snow at neutral {payload/1000:.2f} t")
# coal fit check
t = 0.09; Vin = (a-2*t)*(b-2*t)*(c-2*t); Vsh = V - Vin
for f in (0.60, 0.65):
    Mmax = f*1350*Vin
    excess = V*1000 - (Mmax + 100*(Vin - Mmax/1350) + rho_i*Vsh)
    print(f" coal packing {f}: max coal {Mmax/1000:.2f} t; pod then {excess:.0f} kg buoyant -> needs that much ballast")
# drag
for A, lab in ((a*c, "5.0x1.2"), (a*b, "5.0x2.2")):
    Cd = 170/(0.5*rho_w*A*0.16**2)
    print(f" drag 170 N at 0.16 m/s with frontal {lab} = {A} m2 -> Cd {Cd:.2f}")
for B in (3, 9):
    print(f" friction at mu 0.5 with +{B} kg: {0.5*B*9.81:.0f} N vs drag 170 N")

print("\n== 4. Buoyancy drift from shell melt (their own 6 cm / 45 d) ==")
melt_rate = 0.06/45  # m/day
dB_per_day = (rho_w - rho_i)*S*melt_rate
print(f" shell melt {melt_rate*100:.3f} cm/day over {S:.1f} m2 -> buoyancy loss {dB_per_day:.2f} kg/day")
for B0 in (3, 9):
    print(f"  trimmed +{B0} kg -> neutral after {B0/dB_per_day:.1f} days, sinks thereafter")
for days in (45, 68):
    print(f"  after {days} d: melt {melt_rate*days*100:.1f} cm, buoyancy change {-dB_per_day*days:.0f} kg")
print(" heat flux implied by 6 cm/45 d: %.1f W/m2" % (0.06*rho_i*334e3/(45*86400)))
# sunk pod on bed
Wsub = dB_per_day*45*9.81
for mu in (0.5, 0.7):
    print(f" sunk pod at 45 d: net weight {Wsub:.0f} N, bed friction {mu*Wsub:.0f} N vs drag 170 N")
# frazil accretion the other way: 1 cm of accreted ice
print(" 1 cm of frazil/ice accreted on shell -> +%.0f kg buoyancy" % ((rho_w-rho_i)*S*0.01))

print("\n== 5. Soaking to 0 C ==")
m_cargo, cp_c = 9.5e3, 750.0
m_sh, cp_i = 3.0e3, 2050.0
for dT in (20, 30):
    Q = (m_cargo*cp_c + m_sh*cp_i)*dT
    ice = Q/334e3
    print(f" contents at -{dT} C: {Q/1e6:.0f} MJ -> {ice:.0f} kg ice frozen onto shell -> buoyancy +{ice*(rho_w-rho_i)/rho_i:.0f} kg (vs +3..9 kg trim)")
alpha = 3e-7
Lh = 0.6
print(" conduction time scale L^2/alpha = %.1f days" % (Lh**2/alpha/86400))
pods_day = 1200/10
for soak in (7, 14):
    n = pods_day*soak
    area = n*a*b
    print(f" soak {soak} d x {pods_day:.0f} pods/day = {n:.0f} pods in water, slot area {area:,.0f} m2; at 10 cm/day new ice -> {area*0.10:,.0f} m3/day ice to clear")

print("\n== 6. Transit / season ==")
for d in (41, 68):
    print(f" 700 km in {d} d = {700e3/(d*86400):.3f} m/s")
print(" 144,000 t / 1,200 t/d = %.0f launch days" % (144000/1200))
print(" pods/day = %.0f, one per %.1f min per slot pair" % (pods_day, 24*60/pods_day))

print("\n== 7. Clearance on riffles ==")
for ice in (1.2, 1.6, 2.0):
    draft = ice*rho_i/rho_w
    for pod_h in (1.2, 2.2):
        print(f" ice {ice} m (draft {draft:.2f} m) + pod {pod_h} m -> needs > {draft+pod_h:.2f} m depth at every riffle")

print("\n== 8. Losses and baseline ==")
print(" 5%% of 144 kt = %.0f t of cargo left in the river per season" % (0.05*144000))
for km in (500, 700, 1500):
    print(f" winter road at $0.118/t-km over {km} km = ${0.118*km:.0f}/t")
print(" $59-176/t over 500-1500 km -> $%.3f-%.3f per t-km" % (59/500, 176/1500))
