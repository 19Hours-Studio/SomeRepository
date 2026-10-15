# Idea 2: Freeze-Engine Vitriol Winning - repair rounds
import math, numpy as np
from math import erf, sqrt
# ---------- R1: hydrate-free working fluid: n-butane (Antoine, NIST: log10 P[bar]=4.35576-1175.581/(T-2.071), 195-273 K)
def p_nbutane(Tc):
    T=Tc+273.15; return 10**(4.35576-1175.581/(T-2.071))
for Tc in (-2,-5,-10,-20,-30,-40):
    print(f"n-butane vp {Tc:>4} C: {p_nbutane(Tc):.3f} bar")
# turbine exhaust volume flow, 122.5 MW reject, latent ~385 kJ/kg near -30 C
mdot=127e6/385e3; Tcond=-25; rho=p_nbutane(Tcond)*1e5*0.05812/(8.314*(Tcond+273.15))
print(f"butane flow {mdot:.0f} kg/s, exhaust density {rho:.2f} kg/m3 at {Tcond} C, volumetric {mdot/rho:.0f} m3/s")
# ---------- liquor path: freezing point of H2SO4 solution (CRC freezing-point depression table, wt% -> K)
acid_tab=[(0,0),(1,0.42),(2,0.86),(3,1.31),(4,1.80),(5,2.29),(6,2.81),(8,3.95),(10,5.23),(12,6.69),(14,8.36),(16,10.29),(18,12.48),(20,14.97),(22,17.8),(24,21.0),(26,24.6),(28,28.8),(30,33.5)]
def dT_acid(w):
    xs=[a for a,b in acid_tab]; ys=[b for a,b in acid_tab]; return float(np.interp(w,xs,ys))
def path(a0_wt, Cu0, Cu_sat, rec_target):
    # water to keep liquid so Cu left = (1-rec)*Cu0 ; Cu_sat in g Cu / kg water
    w_left = (1-rec_target)*Cu0/Cu_sat       # kg water left per kg feed water
    CF = 1/w_left
    f = np.linspace(0,1-w_left,400)          # fraction of water frozen
    acid = a0_wt/(1-f)                        # approx wt% (dilute)
    Tf = -np.array([dT_acid(min(a,30)) for a in acid]) - np.where(Cu0/(1-f)>=Cu_sat,1.6,0.6*np.minimum(1,Cu0/(1-f)/Cu_sat))
    return CF, f, Tf, acid[-1]
Cu0=2.5  # g Cu per kg water (2.5 g/L)
for Cu_sat in (57,30):    # 57 = pure water 0 C (14.3 g CuSO4/100 g); 30 = assumed common-ion salting-out by acid (unmeasured at 0 C)
  for rec in (0.8,0.9):
    CF,f,Tf,afin=path(0.25,Cu0,Cu_sat,rec)
    ice=(1-1/CF)/ (Cu0*rec/1000)
    print(f"Cu_sat {Cu_sat} g/kg, rec {rec}: CF {CF:.0f}, final acid {afin:.1f} wt%, final Tf {Tf[-1]:.1f} C, ice-weighted mean Tf {np.mean(Tf):.1f} C, ice {ice:.0f} kg/kg Cu")
# ---------- engine: work per kg ice = eta_rel*Carnot*L ; source = Tf-3 ; sink = Tair + dTair + 4
L_ice=334e3; eta_rel=0.32
def work_per_kg(Tair, Tf_arr, dTair):
    Ts=Tf_arr-3+273.15; Tk=Tair+dTair+4+273.15
    w=np.where(Ts>Tk, eta_rel*(1-Tk/Ts)*L_ice, 0.0)
    return float(np.mean(w))
# fan power per kg ice: air flow for reject heat; dp scales with face velocity; base 100 Pa at dTair 8 K (reviewer range)
def fan_per_kg(dTair, dp_base=100, eta_f=0.65):
    rho_air=1.45; cp=1005
    V=L_ice/(rho_air*cp*dTair)          # m3 air per kg ice
    dp=dp_base*(8/dTair)**1.0 if False else dp_base   # fixed coil dp, ACC area scales instead
    return V*dp/eta_f
CF,f,Tf,afin=path(0.25,Cu0,30,0.8)
print("\nNet work per kg ice (kJ) vs air temp and air-side rise (fans 100 Pa)")
for Tair in (-25,-30,-35,-40,-45):
    row=[]
    for dTair in (6,10,15,20):
        row.append(f"dT{dTair}: {(work_per_kg(Tair,Tf,dTair)-fan_per_kg(dTair))/1e3:5.1f}")
    print(f" Tair {Tair}: "+"  ".join(row))
# natural-draft option: draft = g*H*(rho_out-rho_in); needs >= 60 Pa for low-velocity coils
for Tair,dTair,H in ((-35,10,80),(-35,15,60),(-25,10,80)):
    rho_o=101325*0.02897/(8.314*(Tair+273.15)); rho_i=101325*0.02897/(8.314*(Tair+dTair+273.15))
    print(f"natural draft Tair {Tair}, dT {dTair}, H {H} m: {9.81*H*(rho_o-rho_i):.0f} Pa")
# ---------- R2: climate. hourly T ~ Normal(monthly mean, sd); Nov..Mar
sites={"Udachny":[-29.8,-36.0,-39.4,-35.2,-24.3],"Chara(Udokan)":[-21.0,-31.1,-31.8,-26.3,-16.2]}
hrs=[720,744,744,672,744]
rng=np.random.default_rng(1)
def season_samples(means,sd):
    return np.concatenate([rng.normal(m,sd,h) for m,h in zip(means,hrs)])
ice_per_kgCu=(1-1/CF)/(Cu0*0.8/1000)
EW=2.0   # kWh/kg Cu (typical EW 1.9-2.2)
print(f"\nice per kg Cu (Cu_sat 30, 80%): {ice_per_kgCu:.0f}")
for s,means in sites.items():
  for sd in (5,8):
    T=np.sort(season_samples(means,sd))
    for Nh in (1500,2500,3600):   # run freezer only in the coldest Nh hours (capacity = ice/Nh)
        Tsel=T[:Nh]
        # best dTair per hour
        wk=[max(work_per_kg(t,Tf,d)-fan_per_kg(d) for d in (6,8,10,12,15,20)) for t in Tsel[::10]]
        wavg=np.mean(wk)  # J/kg ice
        kwh=wavg*ice_per_kgCu/3.6e6
        print(f" {s:14s} sd{sd} coldest {Nh} h (mean {Tsel.mean():.1f} C): net {wavg/1e3:.1f} kJ/kg ice -> {kwh:.2f} kWh/kg Cu = {kwh/EW*100:.0f}% of EW")
# ---------- R3: economics per t Cu at 10 kt/yr ; capex reviewer/idea $63M at 4.94 Mt ice/yr ; scale with ice
CRF=0.147  # 12%, 15 yr
cap_per_t_ice_yr=63e6/4.94e6
for grade in (2.5,5,10):
    ice=(1-1/CF)/(grade*0.8/1000) if grade==2.5 else ice_per_kgCu*2.5/grade
    capex=cap_per_t_ice_yr*ice*1e4*0.7**(0) # $ for 10 kt Cu
    capex_nowash=capex*0.65   # no wash column needed: entrained liquor goes back to heap (assumption: wash column ~35% of freeze plant)
    for price in (0.06,0.30):
        kwh=1.0*2.5/grade   # mid net kWh/kg Cu at Udachny-like scaled by grade (from above ~0.8-1.2 at 2.5 g/L)
        credit=kwh*price*1000
        cost=(capex_nowash*CRF/1e4 + 0.03*capex_nowash/1e4) - credit
        print(f"grade {grade} g/L: ice {ice:.0f} kg/kg, capex(no wash) ${capex_nowash/1e6:.0f}M, power credit ${credit:.0f}/t at ${price}/kWh -> freeze step net ${cost:.0f}/t Cu")
# baseline SX step alone (what the freeze step replaces): capex 40% of SX-EW 3000-7400 $/t/yr (USGS 1991 $1500-3700 x2 escalation) + opex 60-120 $/t
for c in (3000,7400):
    print(f"SX step baseline: ${0.4*c*CRF+60:.0f}-{0.4*c*CRF+120:.0f}/t Cu (SX-EW capex {c}/t/yr)")
# Mg limit: mother liquor bled -> max Mg in feed without MgSO4 crystallising
for CFv in (CF,114):
    print(f"Mg feed limit if mother liquor fully bled at CF {CFv:.0f}: {44/CFv:.2f} g/L ; Cu lost to bleed unless cemented: {Cu0*0.2:.2f} g/L-feed eq.")
# pond: liquor stored per 10 kt Cu
print(f"stored liquor per 10 kt Cu at 2.5/5/10 g/L: {1e7/2.5/0.8/1e6:.1f}/{1e7/5/0.8/1e6:.1f}/{1e7/10/0.8/1e6:.1f} Mm3")
# ---------- R4: natural-draft dry tower (no fan power), 60-80 m (Heller-type), dTair 10-15 K
print("\nNatural-draft condenser (no fans):")
for s,means in sites.items():
    T=np.sort(season_samples(means,6.5))
    for Nh in (1500,2500,3600):
        Tsel=T[:Nh]
        wk=[max(work_per_kg(t,Tf,d) for d in (10,12,15)) for t in Tsel[::10]]
        kwh=np.mean(wk)*ice_per_kgCu/3.6e6
        print(f" {s:14s} sd6.5 coldest {Nh} h (mean {Tsel.mean():.1f} C): {np.mean(wk)/1e3:.1f} kJ/kg ice -> {kwh:.2f} kWh/kg Cu = {kwh/EW*100:.0f}% of EW")
# whole-route cost vs best practice at an off-grid site (diesel $0.30/kWh) and at Udokan grid ($0.06)
for site,kwh,price in (("off-grid Udachny-like",0.9,0.30),("Udokan grid",0.25,0.06)):
    freeze=(41e6*(CRF+0.03))/1e4 - kwh*price*1000
    EWcost=2.0*price*1000+250       # power + EW capex/opex ~ $250/t
    sx_lo,sx_hi=236,555
    print(f"{site}: freeze route {freeze+EWcost:.0f} $/t Cu vs SX-EW {sx_lo+EWcost:.0f}-{sx_hi+EWcost:.0f} -> ratio {(sx_lo+EWcost)/(freeze+EWcost):.2f}-{(sx_hi+EWcost)/(freeze+EWcost):.2f}")
