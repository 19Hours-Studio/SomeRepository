"""IDEA 3 - Self-sorting wave-and-ice pond. Anchor: the placer's own pond sorts it in place - sun thaw, and winter
bottom-fast ice that freezes onto the stones and is floated off in spring (ice-rafted stone removal).
Sources: USACE CEM / SPM fetch-limited wave growth (Hm0=0.0016 U^2/g (gF/U^2)^0.5, Tp=0.2857 U/g (gF/U^2)^(1/3));
linear wave theory; Ergun minimum fluidization; Stefan thaw/ice growth; Lena-delta lake ice ~2 m, summer water up to 23 C
(Russian lake summary); ice-push boulder ridges sort cobbles/boulders from 1-2 m depth (Arctic 35(2):312, 1982)."""
import math
g=9.81
def waves(U,F):
    Hm0=0.0016*U**2/g*math.sqrt(g*F/U**2); Tp=0.2857*U/g*(g*F/U**2)**(1/3); return Hm0,Tp
def wavenumber(T,h):
    w=2*math.pi/T; k=w**2/g
    for _ in range(100): k=w**2/(g*math.tanh(k*h))
    return k
print("=== R1: can pond waves winnow / jig the bed? ===")
for U,F in ((8,300),(12,500),(12,1000)):
    H,T=waves(U,F)
    for h in (0.3,0.6,1.0,1.5):
        k=wavenumber(T,h)
        ub=math.pi*H/(T*math.sinh(k*h)); pb=1000*g*H/2/math.cosh(k*h)
        print(f"U={U} F={F} m: Hs={H:.2f} m T={T:.2f} s | depth {h} m: bottom orbital u={ub:.3f} m/s, pressure pulse {pb:4.0f} Pa")
# threshold orbital velocity: fine sand 0.2 mm ~0.15 m/s, gravel 10 mm ~0.6 m/s (Komar & Miller)
# jigging needs bed dilation: min fluidization velocity of 5-20 mm gravel (Ergun, eps=0.4)
def umf(d,rho_s=2650,eps=0.4,mu=1.8e-3):
    Ar=1000*(rho_s-1000)*g*d**3/mu**2
    a=1.75/eps**3; b=150*(1-eps)/eps**3
    Re=(-b+math.sqrt(b*b+4*a*Ar))/(2*a); return Re*mu/(1000*d)
for d in (0.002,0.005,0.02):
    print(f"min fluidization velocity of {d*1000:.0f} mm gravel: {umf(d):.3f} m/s")
# wave-pumped seepage in gravel K=1e-2 m/s at 0.3 m depth gradient ~ pb*k/(rho g)
H,T=waves(12,500); k=wavenumber(T,0.6); pb=1000*g*H/2/math.cosh(k*0.6)
print(f"wave-pumped seepage ~ K*grad = {1e-2*pb*k/(1000*g):.2e} m/s  -> 2-3 orders below fluidization: NO wave jigging")

print("\n=== R1: fines export over the spillway (sediment budget) ===")
silt_kg_m2=2.0*1900*0.20   # 2 m pay, 20% <0.1 mm
for label,water_m in (("own melt+rain outflow",0.7),("creek routed through 10 ha pond, 1 m3/s x 100 d",86.0)):
    for C in (0.1,0.5):
        print(f"{label:48s} C={C} kg/m3: export {water_m*C:6.2f} kg/m2/yr vs fines {silt_kg_m2:.0f} kg/m2 -> {silt_kg_m2/(water_m*C):6.0f} years")

print("\n=== R1: thaw under the pond (Stefan) ===")
for n_ice in (0.3,0.5):
    Lv=n_ice*917*334e3
    for Tw in (10,15):
        X=math.sqrt(2*1.8*Tw*100*86400/Lv)
        print(f"ice frac {n_ice}: pond {Tw} C x 100 d -> thaw {X:.2f} m/summer")

print("\n=== R2: ice rafting capacity (buoyancy) and ice thickening ===")
def ice_growth(FDD,k=2.2,snow_free=True):
    return math.sqrt(2*k*FDD*86400/(917*334e3))*(0.7 if snow_free else 0.45)  # empirical Stefan coefficient
for FDD in (4000,5500):
    hi=ice_growth(FDD)
    for extra in (0,1.5):
        h=hi+extra
        cap=(1000-917)*h/1650   # m3 stone per m2 of floe (stone net weight 1650 kg/m3 in water)
        print(f"FDD {FDD}: natural ice {hi:.2f} m + flooded {extra} m = {h:.2f} m -> lifts {cap:.3f} m3 stone/m2/yr")
# timing: ice reaches stone tops late (March) so only stone tops + <=0.2 m of bed freeze, talik beneath stays thawed
print("\n=== R2: value - fraction of washing removed ===")
for oversize in (0.2,0.35):
    for cap in (0.1,0.18):
        yrs=2.0*oversize/cap
        print(f"oversize {oversize*100:.0f}% of 2 m pay = {2*oversize:.2f} m3/m2: {yrs:.1f} pond-years; wash volume cut to {(1-oversize)*100:.0f}% -> {1/(1-oversize):.2f}x cheaper washing")
# boulder niche: secondary breakage + dozing of >0.5 m boulders vs ice raft
print("\n=== R3 niche: boulder-rich ('valunistye') placers left unmined by dredges ===")
boulder_frac=0.12; cap=0.15
print(f"boulders {boulder_frac*100:.0f}% per m of pay -> {boulder_frac/cap:.1f} yr per m depth; floe winching: 20x20 m floe carries {cap*400:.0f} m3 of boulders")
c_blast=6.0   # $/m3 boulder: drill+blast+doze (assumption, see notes)
c_ice=(2*120*30 + 25*1.5*8*30)/(1e5*cap)  # 2 men + tractor-winch 30 days per 10 ha pond
print(f"ice-raft cost ~${c_ice:.2f}/m3 boulder (10 ha pond, 2 men + winch tractor 30 d) vs drill/blast/doze ~${c_blast}/m3 -> {c_blast/c_ice:.0f}x for that operation only")

print("\n=== R4: where would wave sorting work? (fetch needed) ===")
for F in (2000,10000,30000):
    H,T=waves(12,F); k=wavenumber(T,1.5); ub=math.pi*H/(T*math.sinh(k*1.5))
    print(f"U=12 m/s F={F/1000:.0f} km: Hs={H:.2f} m, bottom u at 1.5 m = {ub:.2f} m/s")
print("-> sorting at 1-2 m depth needs km-scale fetch = a natural lake/sea shore; that is ordinary beach-placer genesis (not novel, not a pond)")
