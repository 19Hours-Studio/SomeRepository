import math
rho, g = 1900.0, 9.81   # frozen overburden bulk density [E]
# --- R1: break span. cantilever: sigma = 3 rho g D^2 / H ; fixed-fixed roof span B: sigma = rho g B^2 /(2H)
# frozen sand/gravel tensile: short-term ~1-1.5 MPa (idea's 0.5-1.5), long-term ~0.2-0.4 MPa at -2..-5C [E: Tsytovich; creep ~1/4-1/8]
print("niche depth D (cantilever) / roof span B (fixed) needed to break, m")
for H in (4,6,8,12):
    row=[]
    for s in (0.2,0.5,1.0):
        D = math.sqrt(s*1e6*H/(3*rho*g)); B = math.sqrt(2*s*1e6*H/(rho*g)); row.append(f"s={s}:D={D:4.1f},B={B:4.1f}")
    print(f"  H={H:2d} m  "+"  ".join(row))
# --- R1 geometry check (face toppling): fallen slab rubble per m face
H, D, hp = 6.0, 8.0, 2.0
rubble = 1.3*H*D
print(f"face toppling: rubble {rubble:.0f} m3 per m of face lands on the floor in front of the next niche -> next niche blocked; "
      f"thawing it by water = hydraulic stripping (known, and water-heat {H*D*70/21:.0f} m3 water/m face)")
# --- thermal: ablation-limited niche advance E = h dT / L_eff
ice_vol = 0.30   # volumetric ice content of frozen pay gravel [E 0.2-0.4]
L_eff = ice_vol*917*334e3 + 2.2e6*3   # J/m3 incl. warming from -3C
for U,dT,label in ((1.0,8,"creek-flow 1 m/s, 8C"),(1.0,4,"creek 1 m/s, 4C"),(5.0,8,"low-pressure monitor jet 5 m/s, 8C")):
    Re = U*1.0/1.8e-6; Nu = 0.023*Re**0.8*13**0.4; h = Nu*0.57/1.0
    if U>2: h *= 2.0   # impingement enhancement [E]
    E = h*dT/L_eff
    print(f"  {label:36s}: h={h:5.0f} W/m2K -> {E*86400:5.1f} m/day theoretical (field rates 0.15-5 m/day [S: Yamal 15-20 cm/d; Bylot scarps up to 5 m/d])")
# water heat budget per m3 of pay
for dT_used in (3,5,8):
    print(f"  water needed if it cools by {dT_used} K: {L_eff/(4.186e6*dT_used):.1f} m3 per m3 pay")
# --- R2 repaired geometry: retreat drifts off a trench, roof drops 2 m in place (no outward topple)
trench_w, panel = 12.0, 60.0   # trench stripped conventionally; drifts 60 m long each side [E]
strip_frac = trench_w/(trench_w+2*panel)
print(f"R2 drift-and-drop: conventional stripping only for trench = {strip_frac*100:.0f}% of overburden")
# bulking check: 2 m void, broken roof bulks 1.1-1.3 -> roof just settles; surface subsides ~2 m
print(f"  void {hp} m vs roof H={H} m: settled roof fills void after bulking of {(H+hp)/H:.2f}; surface subsidence ~{hp:.1f} m")
# --- cost per g, grade 0.5 g/m3 sands, pay 2 m, overburden 6 m (strip ratio 3)
price=9600; grade=0.5
# baseline A: dozer stripping after natural layered thaw (80-120 rub/m3), wash 250, other 250 [E]
# baseline B: drill-blast/ripping frozen overburden 200-300 rub/m3
for name, sc, rec in (("A layered thaw + dozer", 100, 0.88), ("B rip/blast frozen + dozer", 250, 0.88)):
    c=(3*sc+250+250)/(grade*rec); print(f"baseline {name}: {c:,.0f} rub/g")
# drift-and-drop: trench stripping (strip_frac*3 m3/m3 at 100), water 6 m3/m3 pumped at 0.5 MPa + hydroelevator,
# remote monitors, sluice same 250, other 250, recovery loss from bedrock left under caved roof
fuel_MJ = (6*0.5 + 2.0)/0.6/0.35   # MJ diesel per m3 pay
fuel_rub = fuel_MJ/36*90
for rec in (0.70,0.80):
    c=(strip_frac*3*100 + fuel_rub + 120 + 250 + 250)/(grade*rec)   # 120 = pumps/monitors/remote ops capital+labour [E]
    print(f"drift-and-drop rec {rec}: fuel {fuel_rub:.0f} rub/m3 -> {c:,.0f} rub/g")
# deep-overburden regime H=10 m (strip ratio 5)
for name, sc in (("A",100),("B",250)):
    print(f"  H=10 baseline {name}: {(5*sc+500)/(grade*0.88):,.0f} rub/g", end="")
print(f"  | drift-and-drop H=10 rec0.75: {(strip_frac*5*100+fuel_rub+120+500)/(grade*0.75):,.0f} rub/g")
# underground placer mining (known for H>~10-15 m) [E]: 1,500-3,000 rub/m3 sands
print(f"  underground placer baseline (1500-3000 rub/m3): {1500/(grade*0.85):,.0f}-{3000/(grade*0.85):,.0f} rub/g")
