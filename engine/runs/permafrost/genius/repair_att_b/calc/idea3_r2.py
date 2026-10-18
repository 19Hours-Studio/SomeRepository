exec(open('/home/user/SomeRepository/engine/runs/permafrost/genius/repair_att_b/calc/idea3.py').read().split('print("=== R1: cutting')[0])
rho_insitu=1.25
def lhv(W,A_dry=0.12,Qdaf=27.0): return (1-A_dry)*Qdaf*(1-W)-2.44*W
def dredge_cost(demand=10000,haul_km=200,frt=3.0,mob=6e6,share=1,day=0.6e6,P=40,rec=0.8,unload=450,screen=150,lic_expl=30e6,years=15,env=2e6):
    hours=demand/(rec*rho_insitu*P); days=hours/20+3
    return (mob/share+day*days+env)/demand + lic_expl/(years*demand) + haul_km*frt + unload + screen
def micro(demand=10000,SR=4,cs=85*1.5*1.5,mine=350,capex=60e6,years=15,haul_km=200,frt=3.0,unload=450):
    return SR*cs+mine+capex/(years*demand)+haul_km*frt+unload
kd=lhv(0.32)/4.1868; kp=lhv(0.30)/4.1868   # Mcal/kg -> per t: Gcal/t
print(f"dredged+screened coal {kd*1000:.0f} kcal/kg ; bank-pit coal {kp*1000:.0f} kcal/kg")
for demand in (5000,10000):
    for share in (1,4):
        cd=dredge_cost(demand,share=share)
        for SR in (4,15,25):
            cm=micro(demand,SR)
            print(f" demand {demand} t, mob shared by {share}: dredge {cd:,.0f} rub/t = {cd/kd:,.0f} rub/Gcal | bank micro-pit SR {SR}: {cm:,.0f} rub/t = {cm/kp:,.0f} rub/Gcal -> ratio {cm/kp/(cd/kd):.1f}x | vs northern-delivery 15k rub/t ({15000/5.3:,.0f} rub/Gcal) {15000/5.3/(cd/kd):.1f}x")
