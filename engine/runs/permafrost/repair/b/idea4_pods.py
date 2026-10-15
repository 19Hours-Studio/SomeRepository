"""IDEA 4 - Snow-buoyed ice-shell ore pods. Anchor: crushed ore + dry snow sealed in an ice shell, floated against the
underside of winter river ice and carried by the under-ice current to a downstream recovery slot (no vessel, no return).
Sources: under-ice currents Lena delta 0.05-0.25 m/s (Bykovskaya 0.20-0.25, main 0.12-0.18, Olenekskaya 0.05-0.11);
ice-ice friction near 0 C rises with hold time/slow sliding (sintering; Schulson; JAP 2004 crossover ~0.01 m/s),
sphere-on-ice friction ~0.5 near melting at slow speed (AMOLF PRX 2021); Russian truck rate 69.6 rub/truck-km 2024
(Monopoliya), Manitoba study: winter-road freight +60% vs all-weather road."""
import math
rw=1000.; ri=917.
def pod(ore_t, rho_ore, snow_rho=200., shell=0.08, snow_m3=None, B_target=None):
    """returns snow volume needed for net buoyancy B_target (kg), pod volume, mass"""
    Vore=ore_t*1000/rho_ore            # solid ore volume; voids between crushed ore filled by snow
    # shell of ice around a cube-ish pod; iterate
    Vs=0.5
    for _ in range(50):
        Vin=Vore+Vs; side=Vin**(1/3); Vsh=(side+2*shell)**3-Vin
        M=ore_t*1000+Vs*snow_rho+Vsh*ri
        V=Vin+Vsh
        B=rw*V-M
        Vs+= (B_target-B)/ (rw-snow_rho)   # adding snow volume adds (rw - snow_rho) buoyancy per m3
    return Vs,V,M,B,side+2*shell
print("=== R1: snow needed per tonne of ore (net buoyancy +1% of mass) ===")
for name,rho in (("coal",1350),("kimberlite/rock ore",2700),("Pb-Zn sulphide ore",3600)):
    Vs,V,M,B,s=pod(1.0,rho,B_target=15.)
    print(f"{name:22s}: snow {Vs:.2f} m3/t ore (dry snow 200 kg/m3), pod {V:.2f} m3, mass {M:.0f} kg, side {s:.2f} m")

print("\n=== R1: does a pod slide along the ice ceiling? drag vs friction ===")
def drag(U,A,Cd): return 0.5*rw*Cd*A*U*U
for U in (0.1,0.2,0.3):
    for shape,A,Cd in (("cube 1 t ore (rock)",1.25,1.05),("fin 1t: 2.4x1.0x0.55 broadside",2.4,1.2)):
        D=drag(U,A,Cd)
        for mu in (0.05,0.5):
            Bmax=D/(mu*9.81)
            print(f"U={U} {shape:30s} drag {D:5.1f} N, mu={mu}: max net buoyancy {Bmax:6.1f} kg")
print("-> original (buoyancy margin ~ tens-hundreds kg, static contact, mu~0.5 near melting): pods stop and freeze in.")

print("\n=== R2: trim precision achievable in the launch slot ===")
# snow density scatter +-10% on 1 m3 => +-20 kg; trim by floating in slot and adding/removing ore/snow until freeboard ~0
# measurable: a 1.0 m2 waterplane top moves 1 mm per 1 kg -> trim to +-3 kg with a ruler
print("density scatter of packed snow +-10% x 1 m3 x 200 kg/m3 = +-20 kg; slot trim (waterplane 1 m2 -> 1 mm per kg) gets +-3 kg")
print("fin pod at U>=0.2 m/s tolerates B<=~10 kg even at mu=0.5 -> trim to +3..+8 kg keeps it sliding")

print("\n=== R2: freeze-in when stopped; melt in transit ===")
for hi,Ts in ((1.0,-30),(1.8,-30)):
    q=2.2*(0-Ts)/hi; growth=q/(ri*334e3)*86400*100
    print(f"ice {hi} m, surface {Ts} C: basal growth {growth:.1f} cm/day -> a stopped pod is frozen in within hours-days")
dT=0.01; h=500
print(f"transit melt at water +{dT} C: {h*dT/(ri*334e3)*86400*45*100:.1f} cm of shell in 45 days (shell 8 cm OK); pods pre-soaked to 0 C so they don't accrete ice")

print("\n=== R3: route, speed, throughput ===")
for L in (300,700,1500):
    for U in (0.15,0.25):
        print(f"route {L} km at mean pod speed {U*0.8:.2f} m/s (0.8 x mean): {L*1000/(U*0.8)/86400:.0f} days")
pods_per_hr=12; t_per_pod=1.0
season=120
print(f"one slot crew at {pods_per_hr} pods/h x 20 h x {season} d x {t_per_pod} t = {pods_per_hr*20*season*t_per_pod/1000:.0f} kt/season")

print("\n=== COST per tonne ore delivered ===")
rub=95.
truck_tkm=69.6/20/rub           # $/t-km ordinary road, full 20 t
winter=truck_tkm*1.6*2          # winter-road premium (Manitoba +60%) and empty backhaul
print(f"ordinary truck {truck_tkm:.3f} $/t-km; winter road with empty return {winter:.3f} $/t-km")
labour=2*14*120          # two slots x 14 people x $120/day
equip=2*1500             # loaders, crane, ice saw/bubbler per day (fuel+ownership)
snow_ore=0.0             # snow free
daily_t=pods_per_hr*20*t_per_pod
pod_cost=(labour+equip)/daily_t
loss=0.05
print(f"pod handling both ends: ${pod_cost:.1f}/t (+{loss*100:.0f}% lost pods)")
for L in (300,700,1500):
    tr=winter*L; pc=pod_cost/(1-loss)
    print(f"  {L} km: winter road ${tr:.0f}/t vs pods ${pc:.0f}/t -> {tr/pc:.1f}x ; vs summer barge (~$0.025/t-km) ${0.025*L:.0f}/t")

print("\n=== R4: scale pods to 10 t ore (fin 5.0 x 2.2 x 1.2 m), crane-handled; coal vs rock ===")
for name,rho in (("coal",1350),("rock ore",2700)):
    Vs,V,M,B,s=pod(10.0,rho,B_target=10.)
    print(f"{name}: snow {Vs:.1f} m3 per 10 t, pod volume {V:.1f} m3, mass {M/1000:.1f} t")
A=5.0*2.2; Cd=1.2
for U in (0.15,0.2,0.3):
    D=drag(U,A,Cd); print(f"  U={U}: drag {D:.0f} N -> sliding tolerated for net buoyancy <= {D/(0.5*9.81):.0f} kg at mu=0.5, {D/(0.1*9.81):.0f} kg at mu=0.1; slot trim +-10 kg on 11 m2 waterplane")
pods_hr=6; t=10.
daily=pods_hr*20*t
labour=2*14*120; equip=2*2500
pc=(labour+equip)/daily/(1-0.05)
print(f"throughput {daily:.0f} t/day -> {daily*120/1000:.0f} kt per 120-day season; handling ${pc:.1f}/t incl. 5% loss")
for L in (500,1000,1500):
    tr=winter*L
    print(f"  {L} km: winter road ${tr:.0f}/t vs pods ${pc:.1f}/t -> {tr/pc:.1f}x ; summer barge ~${0.025*L:.0f}/t ({0.025*L/pc:.1f}x)")

print("\n=== R5: pass-under criterion for ice-underside roughness / keels: pod dives under an obstacle if drag > B*g ===")
for U in (0.15,0.2,0.3):
    D=drag(U*0.8,A,Cd)   # 0.8: near-ice layer is slower than section mean
    print(f"  section mean {U} m/s (pod sees {U*0.8:.2f}): drag {D:.0f} N -> trim B < {D/9.81:.0f} kg (dive angle >45 deg); trim by crane load cell holding the pod submerged (+-3 kg on ~130 N) -> {'OK' if D/9.81>8 else 'too tight'}")
print("  -> design rule: trim each 10 t pod to +3..+9 kg (load-cell, in the slot) net buoyancy; route only where section-mean under-ice velocity >= 0.2 m/s")
print("  (Lena delta measured 0.05-0.25 m/s: only the fastest channels qualify; regulated rivers below HPPs (Kolyma, Yenisei, Vilyuy) carry larger winter flows)")
