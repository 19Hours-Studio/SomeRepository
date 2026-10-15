"""Idea 3 - freeze-and-float boulder pond. Binding quantities: ice buoyancy per m2 vs stone + frozen-gravel load,
ice growth after contact (freeze-in of gravel), breakout of embedded boulders, capacity per m2, cost per m3 boulder.
Sources: ice growth h = a*sqrt(FDD) (Stefan/Ashton; a~2.0-2.7 cm/(C d)^0.5 for snow-covered lakes, Michel 1971);
natural precedents: Reimnitz et al. 1987 (anchor ice rafts seabed sediment), High-Arctic lake diamicts rafted when
meltwater lifts ice (Sedimentology 2000), Lake Hoare floating boulders (Allen et al.)."""
import math, numpy as np
rw, ri, rs = 1000, 917, 2650
# FDD by date for an upper-Kolyma/Bilibino-type site (monthly mean air T)
months = ["Oct","Nov","Dec","Jan","Feb","Mar","Apr","May"]
Tm = [-12, -27, -33, -35, -32, -24, -12, -1]   # typical Bilibino/Seymchan-like normals
days = [31, 30, 31, 31, 28, 31, 30, 31]
a = 2.4
cum = 0; hist = []
for m, T, d in zip(months, Tm, days):
    for i in range(d):
        cum += max(-T, 0) if not (m == "Oct" and i < 15) else 0
        hist.append((m, i+1, cum, a*math.sqrt(cum)/100))
FDD = cum
hmax = a*math.sqrt(FDD)/100
print(f"FDD {FDD:.0f} C d -> natural ice {hmax:.2f} m (a=2.4); a=2.0..2.7 -> {2.0*math.sqrt(FDD)/100:.2f}..{2.7*math.sqrt(FDD)/100:.2f} m")

def lift(h_ice, gravel_frozen=0.0, phi=0.35):
    """net lift capacity, m3 of stone per m2, after carrying a frozen gravel layer stuck under the floe"""
    B = (rw-ri)*h_ice                                   # kg/m2 net buoyancy of ice
    Wg = gravel_frozen*((1-phi)*(rs-rw) - phi*(rw-ri))  # submerged weight of frozen gravel
    return (B-Wg)/(rs-rw), B, Wg
for h in (1.7, 3.2):
    v, B, _ = lift(h)
    print(f"ice {h} m: buoyancy {B:.0f} kg/m2 -> lifts {v:.3f} m3 stone/m2 (no gravel stuck)")

# freeze-in of gravel after ice touches the bed: Stefan into saturated gravel (porosity 0.35)
def freeze_in(FDD_after, h0, phi=0.35):
    # ice-equivalent growth continues; latent per m of gravel = phi*ri*L vs ri*L -> gravel front moves 1/phi faster,
    # conductivity of frozen gravel ~2.5 vs ice 2.2 (ignored, conservative)
    h_tot_ice_eq = math.sqrt(h0**2 + (a/100)**2*FDD_after)
    return (h_tot_ice_eq - h0)/phi
print("\nfreeze-in under the floe if it grounds early (natural timing, 'reaches boulder tops in March'):")
for start in ("Mar", "Apr", "late Apr"):
    if start == "Mar": idx = [i for i, x in enumerate(hist) if x[0] == "Mar" and x[1] == 15][0]
    elif start == "Apr": idx = [i for i, x in enumerate(hist) if x[0] == "Apr" and x[1] == 1][0]
    else: idx = [i for i, x in enumerate(hist) if x[0] == "Apr" and x[1] == 25][0]
    F0 = hist[idx][2]; h0 = a*math.sqrt(F0)/100
    g = freeze_in(FDD-F0, h0)
    for h_ice in (1.7, 3.2):
        v, B, Wg = lift(h_ice, g)
        print(f" contact {start:8s}: residual FDD {FDD-F0:4.0f} -> frozen gravel {g*100:5.1f} cm; ice {h_ice} m: B {B:.0f} vs gravel {Wg:.0f} kg/m2 -> net stone {v:+.3f} m3/m2 {'FLOATS' if v>0 else 'STAYS GROUNDED'}")

# Repair: drawdown-timed grounding. Keep water deep (talik stays unfrozen) until ~Apr 25, then lower the pond so the
# floating sheet settles onto boulder tops; only the last ~10-15 d of frost act.  Boulder tops protrude; ice grips them.
# Breakout of an embedded boulder (diameter D, embedded fraction e) - drained, slow buoyancy loading:
print("\nbreakout: floe area needed per boulder (ice 1.7 m and 3.2 m, 5 cm gravel stuck)")
for D in (0.5, 0.8, 1.2):
    for e in (0.3, 0.5, 0.7):
        Vb = math.pi/6*D**3
        Wb = Vb*(rs-rw)
        z = e*D
        # resistance: weight of truncated soil cone above the embedded part (45 deg spread) minus boulder part, gamma' ~ 1000 kg/m3
        r = D/2
        cone = math.pi*z/3*((r)**2 + r*(r+z) + (r+z)**2) - Vb*e
        R = max(cone, 0)*1000*0.5 if e > 0.5 else max(cone,0)*1000*0.2
        A17 = (Wb+R)/(lift(1.7, 0.05)[0]*(rs-rw))
        A32 = (Wb+R)/(lift(3.2, 0.05)[0]*(rs-rw))
        print(f" D {D} m embedded {e:.1f}: boulder {Wb:5.0f} kg + soil {R:5.0f} kg -> needs {A17:5.1f} m2 (1.7 m ice) / {A32:5.1f} m2 (3.2 m) of floe ; boulder plan area {math.pi*r*r:.2f} m2")

# capacity vs a bouldery placer: only boulders exposed in the top layer can be gripped
print("\ncapacity:")
for cover in (0.10, 0.20, 0.30):
    D = 0.8
    vol_per_m2 = cover/(math.pi*(D/2)**2)*math.pi/6*D**3
    print(f" surface boulder cover {cover:.0%} of 0.8 m boulders = {vol_per_m2:.3f} m3/m2 ; 1.7 m ice lifts {lift(1.7,0.05)[0]:.3f}, 3.2 m lifts {lift(3.2,0.05)[0]:.3f}")

# cost per m3 of boulder removed, per hectare-season
usd = 85
D375 = 159; exc = 120; tractor = 90
ha = 1e4
lifted = lift(1.7, 0.05)[0]*ha*0.8     # 80% of area effective
dike = 0.0   # pond is the dredge pond / existing dredge cut (niche)
cut_m = 2*100*(ha/(100*30))           # cut strip boundaries: 30 m x 100 m strips -> 667 m per ha
saw_h = cut_m/60                      # ice trencher 60 m/h through 1.7 m
drawdown = 1500                      # pump/ spillway operation per ha
winch = 40*tractor                   # 40 h winching strips into dump bay
spray = 0.0
c_ice = saw_h*(tractor+40) + drawdown + winch
print(f"\nice method per ha (1.7 m ice): lifts {lifted:.0f} m3; saw {saw_h:.0f} h; total ${c_ice:,.0f} -> ${c_ice/lifted:.2f}/m3 boulder")
for h_build, cost_flood in ((3.2, 0.6),):   # flood-thickened ice: pump 1.5 m of extra ice, $0.6/m3 water pumped incl. labour
    lifted2 = lift(h_build, 0.05)[0]*ha*0.8
    c2 = c_ice*1.3 + cost_flood*1.5*ha
    print(f" flood-thickened {h_build} m: lifts {lifted2:.0f} m3; ${c2:,.0f} -> ${c2/lifted2:.2f}/m3")
# Baselines: (1) excavator 30-40 t with grapple picking boulders on dry/frozen ground, 40 m3/h boulder, casting aside
b1 = exc/40
# (2) dozer push-aside of surface boulders, 60 m3/h
b2 = D375/60
# (3) drill-blast-doze for oversize >1.5 m: 6 $/m3 (idea's own number)
print(f"baselines: excavator grapple ${b1:.2f}/m3, dozer push ${b2:.2f}/m3, drill-blast-doze ~$6/m3 (only >1.5 m)")
# value case: dredge-ahead.  Dredge mining ~ $2.5/m3 vs open-pit bulldozer-sluice ~$6/m3 (NOTES).  If boulders 3% of
# volume of a 3 m pay column and must be removed (excavator from shore cannot reach under 2 m of water):
pay = 3.0; frac = 0.03
for method, cb in (("ice", c_ice/lifted), ("excavator on drained ground", b1)):
    print(f" dredge-ahead boulder clearing by {method}: adds ${cb*frac:.2f}/m3 of pay")
