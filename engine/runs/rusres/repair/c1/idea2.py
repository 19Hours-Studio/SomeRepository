import math
def crf(r,n): return r*(1+r)**n/((1+r)**n-1)
r=0.12; g=9.81
Q=8e6                    # t/y extra ore for Talnakh concentrator 10->18 Mtpa (FACT 349)
H=1000.0                 # m lift (assumed mid-depth disseminated/cupriferous levels; Oktyabrsky rich ore >1.7 km FACT 6)
hours=330*20
tph=Q/hours; print("design flow t/h",round(tph), "-> design 1600 t/h")
# --- belt physics: flights with steel-cord belt
Qd=1600; v=4.0; m_load=Qd/3.6/v          # kg/m
for ST,W in ((3150,1.4),(5000,1.4)):
    Tmax=ST*W*1000/7.0                      # N, safety factor 7
    f=0.025; m_belt=60; m_idl=25
    for ang in (14.0,9.5):
        th=math.radians(ang)
        # tension per m of slope: lift + friction
        per_m=g*(m_load*math.sin(th)+f*math.cos(th)*(m_load+2*m_belt+m_idl))
        Lflight=Tmax/per_m; Hflight=Lflight*math.sin(th)
        L=H/math.sin(th)
        print(f"ST{ST} {ang}deg: flight lift {Hflight:.0f} m, decline length {L/1000:.1f} km, flights {math.ceil(H/Hflight)}")
P_lift=Qd/3.6*g*H/0.85/1e6; print("belt lift power MW",round(P_lift,1))
E_t=g*H/0.85/3.6e6*1000; print("belt kWh/t",round(E_t,2),"; skip hoist ~",round(g*H/0.80/3.6e6*1000,2))
# --- development time
shaft_depth=2100; shaft_rates=(150,322)   # m/yr Nornickel AR2017 (152 m vent shaft, 322 m skip-cage shaft in 2017)
for s in shaft_rates: print(f"shaft sinking {s} m/y -> {shaft_depth/s:.1f} y + ~1.5 y equipping")
for name,L,rate in (("D&B 14deg",H/math.sin(math.radians(14)),150),("D&B 14deg 2 headings",H/math.sin(math.radians(14))/2,150),("TBM 9.5deg",H/math.sin(math.radians(9.5)),300)):
    print(f"{name}: {L/1000:.1f} km at {rate} m/mo -> {L/rate/12:.1f} y + 1 y belt install")
# --- capex
KZT=470; nurk=5.9e9/KZT; print("Nurkazgan crusher+844m cascade $M",round(nurk/1e6,1),"=> $/m incl crusher",round(nurk/844))
def decl_capex(L, exc_per_m):
    return L*exc_per_m + L*6000 + 3*25e6     # excavation + belt installed $6k/m + 3 level crusher stations $25M each
L14=H/math.sin(math.radians(14))
dec_lo=decl_capex(L14,8000); dec_hi=decl_capex(L14,14000)*1.3
shaft_lo=shaft_depth*40000+60e6; shaft_hi=shaft_depth*70000+90e6   # shaft+hoist; plus LHD/rail to shaft same in both? shaft also needs crushing/loading pockets
shaft_lo+=2*15e6; shaft_hi+=2*20e6
print(f"decline+belt capex ${dec_lo/1e6:.0f}-{dec_hi/1e6:.0f}M ; new shaft+hoist ${shaft_lo/1e6:.0f}-{shaft_hi/1e6:.0f}M")
# --- opex per t ore (difference items only)
elec=0.04  # $/kWh Norilsk own gas/hydro power assumption
def opex_belt(): return E_t*elec*1.1 + 0.35 + 0.25   # energy, belt/idler maint ~$0.35/t, crusher ~$0.25/t
def opex_shaft(): return g*H/0.80/3.6e6*1000*elec + 0.45 + 0.25  # hoist maint+crew higher
# truck ramp (strawman-check, only for completeness, 1:7 ramp)
ramp=H*7.1; cyc=ramp/1000/10+ramp/1000/18+0.2; truck_tpd=45/cyc*20*0.75
ntr=Q/330/truck_tpd; kw=405*ntr
air=kw*0.06; DD=4900   # K*d below +2C (FACT 345 FDD 4415 + margin)
heat=air*1.25*1.005*DD*86400/3.6e9  # MWh_th... (kJ->kWh: /3600) -> J? compute in GWh
heat_GWh=air*1.25*1005*DD*86400/3.6e12
print(f"truck-ramp: {ntr:.0f} trucks, {kw/1000:.1f} MW diesel, air {air:.0f} m3/s, winter air heating {heat_GWh:.0f} GWh_th/y")
diesel_L=kw*0.6*6600*0.25; truck_opex=(diesel_L*0.9+ntr*4.5*60000+ntr*1.2e6/6+ntr*250000+heat_GWh*1e6*0.02)/Q
print(f"truck-ramp opex {truck_opex:.2f} $/t (diesel {diesel_L/1e6:.0f} ML/y)")
life=25
for name,cap,op in (("decline belt lo",dec_lo,opex_belt()),("decline belt hi",dec_hi,opex_belt()),("shaft lo",shaft_lo,opex_shaft()),("shaft hi",shaft_hi,opex_shaft())):
    print(f"{name:16s} capital {cap*crf(r,life)/Q:.2f} $/t + opex {op:.2f} = {cap*crf(r,life)/Q+op:.2f} $/t ore")
# --- per unit product: disseminated ore value
ni=0.30;cu=0.40;pgm=4.5
val=ni/100*15500*0.75+cu/100*9500*0.8+pgm/31.1035*1100*0.75
print("recovered value $/t ore",round(val), "-> t ore per t Ni-eq", round(15500/val))
full_cost_ore=75  # $/t all-in mine+mill+smelt share assumption for disseminated ore
print("full cost per t Ni-eq ~", round(full_cost_ore*15500/val))
# --- value of time: concentrator 18 Mtpa ready 2030-31; decision 2027
margin=val-full_cost_ore
for shaft_y in (7.0,10.0,14.0):
    dec_y=3.5
    gap=max(0,(2027+shaft_y)-max(2027+dec_y,2031))
    # concentrator capital idle: Talnakh upgrade 1.8bn RUB per mtpa (FACT 59) ~ $22M/mtpa at 82 RUB/$
    conc_idle=8*22e6*r*gap
    print(f"shaft {shaft_y}y: ore late by {gap:.1f} y vs belt; lost margin {margin*Q*gap/1e9:.2f} $bn undiscounted; idle concentrator carry {conc_idle/1e6:.0f} $M")
# whole-chain ratio over the life incl. ramp: annualised cost per t Ni-eq in first 10 years
