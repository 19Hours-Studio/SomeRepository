# Idea 4: night-sky lithium freeze cascade - repair rounds
import numpy as np, math
sigma=5.67e-8
# R1: anchor as stated (sub-eutectic CaCl2): best regime = refrigeration-assisted, Arctic air as sink
for Tair in (-40,-45):
    Tp=-55; Tc=Tair+5
    cop=0.45*(Tp+273.15)/((Tc+273.15)-(Tp+273.15))
    q=290e3   # J/kg brine: ice + CaCl2.6H2O near eutectic composition
    kwh=q/cop/3.6e6
    for Li_ppm in (294,600):
        brine=188/(Li_ppm*1e-6*0.7)/1000   # t brine per t LCE, 70% capture
        print(f"sub-eutectic w/ heat pump, air {Tair}: COP {cop:.1f}, {kwh*1000:.1f} kWh/t brine, Li {Li_ppm} mg/kg -> {brine:.0f} t brine/t LCE, {kwh*brine*1000/1e3:.1f} MWh/t LCE -> ${kwh*brine*1000*0.05:,.0f}-{kwh*brine*1000*0.10:,.0f} power only")
# residual liquor still ~27-30 wt% CaCl2 -> DLE still needed; CaCl2-saturated brine above eutectic: hexahydrate crystallisation only
x=(0.35-0.31)/(0.507-0.31); print(f"35%->31% CaCl2 by hexahydrate crystallisation removes {x*100:.0f}% mass -> Li x{1/(1-x):.2f}")
# R2: niche, Ca-free eluate. RO first (osmotic limit), then freezing replaces MVR
for Li in (2.2,6,8,10):
    c=Li/6.94  # M LiCl
    pi=2*0.93*c*0.08314*278
    print(f"LiCl at {Li} g/L Li: osmotic {pi:.0f} bar")
Li_RO=6.0; Li_target=25.0
V0=188/Li_RO; Vf=188/Li_target
print(f"water to remove after RO ({Li_RO}->{Li_target} g/L): {V0-Vf:.1f} m3/t LCE (vs 188-626 m3 from raw eluate)")
# LiCl freezing points (approx CRC): wt% -> C
tab=[(0,0),(2,-1.7),(4,-3.6),(6,-5.8),(8,-8.3),(10,-11.1),(12,-14.4),(14,-18.1),(16,-22.4),(18,-27.3),(20,-33.0)]
def Tf(Li):  # g/L Li -> wt% LiCl approx (density ~1.05-1.1)
    w=Li*42.39/6.94/ (1000*1.07)*100
    return float(np.interp(w,[a for a,b in tab],[b for a,b in tab])), w
for Li in (6,14,25):
    t,w=Tf(Li); print(f"  {Li} g/L Li = {w:.1f} wt% LiCl, freezes at {t:.1f} C")
# spray-freeze cascade with drainage + fractional melt (Alberta field data: >50% impurities leave with unfrozen water; ~90% of salts in first ~19-30% of melt)
def stage(V,C,frz=0.75,drain_share=0.55,early_melt=0.25,early_share=0.90):
    Li=V*C
    Vd=V*(1-frz); Ld=Li*drain_share
    Vi=V*frz; Li_ice=Li-Ld
    Vm=Vi*early_melt; Lm=Li_ice*early_share
    return (Vd,Ld/Vd),(Vm,Lm/Vm),(Vi-Vm,(Li_ice-Lm)/(Vi-Vm))
V,C=V0,Li_RO
d,m,l=stage(V,C)
print(f"stage1: drain {d[0]:.1f} m3 @ {d[1]:.1f} g/L; early melt {m[0]:.1f} m3 @ {m[1]:.1f} g/L (spring, stored, recycled); late melt {l[0]:.1f} m3 @ {l[1]:.2f} g/L -> eluent/RO feed")
d2,m2,l2=stage(*d)
print(f"stage2 on drain: drain {d2[0]:.1f} m3 @ {d2[1]:.1f} g/L (product); early melt {m2[0]:.1f} @ {m2[1]:.1f}; late {l2[0]:.1f} @ {l2[1]:.2f}")
print(f"  stage2 product freezing point {Tf(d2[1])[0]:.0f} C -> needs air <= {Tf(d2[1])[0]-12:.0f} C")
# steady-state with recycle of melts to stage-1 feed: Li to product fraction per pass
Li_in=V0*Li_RO; Li_prod=d2[0]*d2[1]
print(f"per-pass Li to product {Li_prod/Li_in*100:.0f}%; rest returns in melts (no loss if melts recycled); recycle factor {Li_in/Li_prod:.2f}x stage-1 load")
# ice per t LCE with recycle
ice1=V0*0.75*Li_in/Li_prod; ice2=d[0]*0.75*Li_in/Li_prod
print(f"ice frozen per t LCE incl. recycle: {ice1+ice2:.0f} t")
# R3: costs per t LCE for the post-RO concentration step (20 kt LCE/yr)
plant=20000
water=(V0-Vf)*plant
for kwh_m3,price in ((20,0.06),(60,0.30)):
    mvr_e=kwh_m3*(V0-Vf)*price
    # MVR capex titanium ~ $1.0-1.5M per m3/h evaporation (assumption), 8000 h/yr
    cap=water/8000*np.array([1.0e6,1.5e6])
    print(f"MVR: energy ${mvr_e:.0f}/t LCE; capex ${cap[0]/1e6:.0f}-{cap[1]/1e6:.0f}M -> ${cap[0]*0.147/plant:.0f}-{cap[1]*0.147/plant:.0f}/t LCE")
ice_tot=(ice1+ice2)*plant
pump_kwh=ice_tot*1.0/1e0*0.6   # 0.6 kWh/m3 spray pumping at 15 bar
for capex in (12e6,25e6):     # snow-gun/spray system, lined ice pads, melt ponds, 0.4 Mm3 storage of RO concentrate
    opex=pump_kwh*0.30/plant + 0.03*capex/plant
    print(f"spray-freeze cascade: ice {ice_tot/1e6:.2f} Mt/yr, capex ${capex/1e6:.0f}M -> ${capex*0.147/plant+opex:.0f}/t LCE")
store=V0*plant*7/12
print(f"winter-only freezing: store RO concentrate {store/1e6:.2f} Mm3 (vs reviewer 2.2-7.3 Mm3 for raw eluate)")
# guns: heat to remove per hour at 3000 h
q=ice_tot*1000*(334e3+4.2e3*10)/(3000*3600)
print(f"heat rejection {q/1e6:.0f} MW over 3000 h; snowmaking guns ~30-100 m3/h each -> {ice_tot/3000/100:.0f}-{ice_tot/3000/30:.0f} guns")
# R4: milder product target (20 g/L) so stage 2 runs at air <= -25 C; stage-1 early melt -> stage-2 next winter; late melts -> RO feed
def run(frz2):
    d,m,l=stage(V0,Li_RO)
    V2=d[0]+m[0]; C2=(d[0]*d[1]+m[0]*m[1])/V2
    d2,m2,l2=stage(V2,C2,frz=frz2)
    prod=d2[0]*d2[1]; Li_in=V0*Li_RO
    # stage-2 early melt recycled to stage 2; late melts to RO feed (= same grade as eluate, no loss)
    frac=prod/Li_in
    ice=(V0*0.75+V2*frz2)/frac
    return C2,d2,frac,ice
for frz2 in (0.55,0.65):
    C2,d2,frac,ice=run(frz2)
    print(f"stage2 freeze {frz2}: stage-2 feed {C2:.1f} g/L, product {d2[1]:.1f} g/L (Tf {Tf(d2[1])[0]:.0f} C), Li to product per pass {frac*100:.0f}%, ice {ice:.0f} t/t LCE, late melts returned at <=1.1 g/L")
