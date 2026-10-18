# IDEA 3: channel-talik seam dredging (CSD cuts coal seam in place in the unfrozen channel talik)
print("=== R1: cutting rate P = eta*Pc/(k*UCS)  (specific energy ~ k*UCS, k~1 MJ/m3 per MPa; CSD mech. limit ~50 MPa IADC) ===")
for Pc in (75,150,300):
    for ucs in (2,5,7,15):
        P=0.6*Pc*1e3/(1.0*ucs*1e6)*3600
        print(f" cutter {Pc} kW, coal UCS {ucs} MPa -> {P:.0f} m3/h in situ")
# pump limit: 300 mm discharge, 4 m/s, Cv 0.12
import math
Qp=math.pi*0.15**2*4*0.12*3600
print(f" pump solids limit (300 mm, 4 m/s, Cv 0.12) = {Qp:.0f} m3/h")
print("=== R1: time to cut a village cluster's year ===")
rho_insitu=1.25  # t/m3 brown coal in situ
for demand in (5000,10000,20000):
    for P in (20,60):
        rec=0.8  # spillage + overflow fines loss
        h=demand/(rec*rho_insitu*P)
        print(f" {demand} t/yr at {P} m3/h, recovery {rec}: {h:.0f} h = {h/20:.1f} days (20 h/d)")
print("=== R2: quality of dredged coal (as-received) ===")
# brown coal: dry ash-free GCV ~ 27 MJ/kg (lignite/sub-bit typical), ash 12% dry
def lhv(W,A_dry=0.12,Qdaf=27.0):
    dry=(1-A_dry)*Qdaf
    return dry*(1-W)-2.44*W
for W in (0.25,0.32,0.40,0.45):
    print(f" total moisture {W:.0%}: LHV {lhv(W):.1f} MJ/kg = {lhv(W)/4.1868*1000:.0f} kcal/kg")
print("=== R3: cost per tonne and per Gcal delivered ===")
def dredge_cost(demand=10000,haul_km=300,frt=3.0,mob=6e6,day=0.6e6,P=40,rec=0.8,unload=450,lic=1.5e6,env=2e6):
    hours=demand/(rec*rho_insitu*P); days=hours/20+3
    c=(mob+day*days+lic+env)/demand + haul_km*frt + unload
    return c,days
hard_kcal=5300   # hard coal assumed for northern-delivery (Zyryanka/Dzhebariki type), assumption
for demand in (5000,10000,20000):
    for haul in (100,300):
        c,d=dredge_cost(demand,haul)
        W=0.40; kcal=lhv(W)/4.1868*1000
        print(f" dredge: {demand} t, haul {haul} km: {c:,.0f} rub/t ({d:.0f} dredge-days); per Gcal {c/(kcal/1000):,.0f} rub (at {kcal:.0f} kcal/kg)")
for p in (3500,10000,25000):
    print(f" northern-delivery hard coal {p} rub/t (Tkach 2020 range 3.5-25k): per Gcal {p/(hard_kcal/1000):,.0f} rub")
# micro-strip pit on the bank (best local alternative): stripping SR m3/t, bulldozer 85*1.5 rub/m3, ripping frozen x1.5, capex amortised
def micro(demand=10000,SR=4,cs=85*1.5*1.5,mine=350,capex=60e6,years=15,haul_km=300,frt=3.0,unload=450,road=0):
    return SR*cs+mine+capex/(years*demand)+haul_km*frt+unload+road
for demand in (5000,10000,20000):
    for SR in (3,6):
        c=micro(demand,SR); kcal=lhv(0.32)/4.1868*1000
        print(f" micro-pit: {demand} t SR {SR}: {c:,.0f} rub/t, per Gcal {c/(kcal/1000):,.0f}")
