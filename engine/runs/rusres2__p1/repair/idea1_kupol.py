# Idea 1: Kupol hub toll-milling -- winter-road satellite ore to Kupol mill on Kupol's own diesel
import numpy as np
OZ=31.1035; USD_RUB=85.0
AU=4000.0          # $/oz, Oct-2026 assumption (sensitivity 3000-4500)
def crf(r,n): return r/(1-(1+r)**-n)

# ---- winter-road haul cost, bottom-up, $/t-km (payload) ----
def haul_cost_tkm(L_km, payload=40, v=25, load_h=3, season_d=90,
                  fuel_L_km=0.45, fuel_usd_L=1.3, truck_usd=180e3, truck_life=5, r=0.15,
                  driver_usd_season=47e3, maint_tkm=0.02, road_rub_km=1.0e6, season_t=300e3):
    trip_h = 2*L_km/v + load_h
    trips = season_d*24*0.85/trip_h                 # 85% availability
    tkm_truck = trips*payload*L_km
    fuel = 2*fuel_L_km*fuel_usd_L/payload           # round trip, empty back
    capital = truck_usd*crf(r,truck_life)/tkm_truck # truck works only on the season
    driver = driver_usd_season/tkm_truck
    road = road_rub_km*L_km/USD_RUB/(season_t*L_km)
    return fuel+capital+driver+maint_tkm+road, trips, trip_h
for L in (100,160,300):
    c,tr,h=haul_cost_tkm(L); print(f"L={L} km  haul ${c:.3f}/t-km  -> ${c*L+6:.0f}/t incl $6 rehandle; trips/truck/season {tr:.0f}")

# ---- per-oz comparison: hub haul vs stand-alone satellite mill ----
def per_oz(g, L, tpa, rec_hub=0.92, rec_sat=0.90, sort=None):
    c,_,_=haul_cost_tkm(L, season_t=tpa)
    mass=1.0; au_keep=1.0
    if sort: mass,au_keep=sort        # fraction of mass hauled, fraction of Au kept
    haul = (c*L+6)*mass + (2.5 if sort else 0)   # $/t ROM; sorting $2.5/t ROM
    oz_hub = g*au_keep*rec_hub/OZ
    return haul/oz_hub, oz_hub
# stand-alone: Kekura DFS capex $229m (2018) for 0.8 Mt/y; escalate +50% (sanctions/inflation, FACT 57 range 40-70%);
# share avoided by toll milling (mill, TSF, power plant, part of camp) ~60%
cap_sat = 229e6*1.5*0.60
for tpa in (0.3e6,0.5e6,0.8e6):
    for g in (4,5,7.5,10):
        h_oz,oz_t = per_oz(g,160,tpa)
        oz_y_sat = tpa*g*0.90/OZ
        cap_scaled = cap_sat*(tpa/0.8e6)**0.6
        avoid = cap_scaled*crf(0.15,10)/oz_y_sat
        # stand-alone opex premium: small mill own G&A, power plant O&M ~ $8/t (diseconomy) vs hub marginal
        avoid += 8/(g*0.9/OZ)
        print(f"tpa {tpa/1e6:.1f} Mt g {g:4.1f}  haul ${h_oz:5.0f}/oz  avoided ${avoid:5.0f}/oz  net hub gain ${avoid-h_oz:5.0f}/oz")
# with satellite XRT sorting (domestic RADOS): 35% mass reject, 93% Au kept (ASSUMPTION, deciding unknown)
print("--- with sorting 0.65 mass / 0.93 Au ---")
for g in (3,4,5,7.5):
    h,_=per_oz(g,160,0.5e6,sort=(0.65,0.93))
    h0,_=per_oz(g,160,0.5e6)
    print(f"g {g}: haul/oz unsorted ${h0:.0f}  sorted ${h:.0f}  (lost Au value ${(1-0.93)*AU:.0f}/oz-equiv on ROM)")

# ---- breakeven grade where haul/oz = avoided/oz at 0.5 Mt/y, 160 km & 300 km
from scipy.optimize import brentq
def gain(g,L,tpa=0.5e6):
    h,_=per_oz(g,L,tpa); oz_y=tpa*g*0.9/OZ
    return cap_sat*(tpa/0.8e6)**0.6*crf(0.15,10)/oz_y + 8/(g*0.9/OZ) - h
for L in (100,160,300):
    print(f"L {L} km: haul/oz = avoided/oz at any grade? gain@5g/t ${gain(5,L):.0f}/oz, @10 ${gain(10,L):.0f}/oz")

# ---- winter-road throughput check ----
for tpa in (0.3e6,0.5e6,0.8e6):
    for days in (90,75):
        loads=tpa/40; print(f"{tpa/1e6} Mt in {days} d: {loads:.0f} loads, {loads/days:.0f}/day (TCWR record 10,922 loads/season, ~168/day over 65 d)")
# fleet for 0.5 Mt at 160 km, 75 days
c,tr,h=haul_cost_tkm(160,season_d=75); print("fleet for 0.5 Mt/75 d:", 0.5e6/40/tr)
# ---- full cost per oz delivered (toll route) vs Kupol-style standalone
def full_cost(g, tpa, L, route):
    oz = tpa*g*(0.92 if route=='hub' else 0.90)/OZ
    mine = 45*tpa   # $45/t ore underground/open-pit mix remote
    if route=='hub':
        mill = 30*tpa  # toll fee at Kupol marginal cost incl diesel power ~30 kWh/t at $0.35/kWh = $10.5/t
        haul = (haul_cost_tkm(L,season_t=tpa)[0]*L+6)*tpa
        cap = 60e6*(tpa/0.5e6)**0.6*crf(0.15,10)   # mine dev + road + stockpile pads
        years=2
    else:
        mill = 38*tpa; haul=0
        cap = (60e6*(tpa/0.5e6)**0.6 + cap_sat*(tpa/0.8e6)**0.6)*crf(0.15,10)
        years=4
    return (mine+mill+haul+cap)/oz + 0.06*AU, years   # 6% MET+royalty
for g in (5,7.5):
    for r in ('hub','standalone'):
        c,y=full_cost(g,0.5e6,160,r); print(f"g {g} {r:10s}: full ${c:.0f}/oz, decision->first gold ~{y} y")
