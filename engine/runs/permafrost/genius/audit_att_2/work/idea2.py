import math
print("=== IDEA 2: Channel-talik seam dredging ===")
# 1. throughput and days
for q in (46,65):
    d100=10000/(q*24)
    print(f"{q} t/h: 10 kt needs {d100:.1f} days at 100% util; util implied by 8 d {d100/8:.0%}, by 25 d {d100/25:.0%}")
# density: in-situ lignite 1.15-1.3 t/m3
for rho in (1.15,1.25,1.3):
    print(f"46-65 m3/h bank x {rho} = {46*rho:.0f}-{65*rho:.0f} t/h (text says 46-65 t/h)")
# 2. implied specific energy of cutting
for q in (46,65):
    se=150*3.6/q  # MJ/m3 (kW*3600 s / m3/h /1000)
    print(f"150 kW / {q} m3/h = SE {se:.1f} MJ/m3 = {se/3.6:.2f} kWh/m3; UCS 5-7 MPa => SE/UCS = {se/7:.2f}-{se/5:.2f}")
# 3. Kovin benchmark: 4,400,863 t commercial coal in 66,056 h; cutter 750 kW, total 10,090 kW
kov=4400863/66056
print(f"Kovin I average = {kov:.1f} t/h; per cutter kW = {kov/750:.3f} t/h/kW; scaled to 150 kW = {kov/750*150:.1f} t/h; per total kW {kov/10090*1000:.1f} t/h per MW")
for q in (kov/750*150,):
    print(f"  at {q:.1f} t/h, 10 kt = {10000/q/24:.0f} days at 100% util, {10000/q/24/0.6:.0f} at 60%")
# 4. season: 4 bends x 8-25 days (+3 d transit each) vs June-July (61 d) and effective ice-free window
for per in (8,25):
    need=4*per+4*3
    print(f"4 bends at {per} d + transit = {need} d vs June-July 61 d; bends that fit in 61 d: {61//(per+3)}; in 45 d (ice-free mid-June..July): {45//(per+3)}")
# 5. rub/Gcal
for c in (2700,3400,4300):
    print(f"{c} rub/t / 3.67 Gcal/t = {c/3.67:.0f} rub/Gcal")
print("baseline 15000/2830 =", 15000/2830, "Gcal/t (i.e. kcal/kg x1000)")
print("ratio full range:", 2830/(4300/3.67), 2830/(2700/3.67), " claimed 730-930:", 2830/930, 2830/730)
# boiler efficiency penalty: lignite 32% moisture vs hard coal 5300 kcal/kg in same small boiler
for eta_c,eta_l in ((0.65,0.58),(0.60,0.50)):
    r_lo=2830/eta_c/(1170/eta_l); r_hi=2830/eta_c/(730/eta_l)
    print(f"useful-heat basis eta_hard={eta_c} eta_lig={eta_l}: ratio {r_lo:.2f}-{r_hi:.2f}")
# 6. LHV check (Mendeleev-type): GCVdaf, ash Ad, moisture W
for gcv_daf in (6300,6800,7200):
    for Ad in (0.08,0.15):
        W=0.32; Aar=Ad*(1-W); comb=1-W-Aar; Hdaf=0.05
        gcv=gcv_daf*comb; lhv=gcv-600*(W+9*Hdaf*comb)
        print(f"GCVdaf {gcv_daf} Ad {Ad:.2f}: LHV_ar at W=32% = {lhv:.0f} kcal/kg")
# 7. strip ratio meaning: 15-25 m3/t with seam thickness m and density 1.25
for m in (1.5,3,5):
    print(f"seam {m} m: overburden height for 15-25 m3/t = {15*m*1.25:.0f}-{25*m*1.25:.0f} m")
