# Idea 1: triaged thermosyphon retrofit - cooling margin by site and cost per unit delivered
import numpy as np
days=np.array([31,28,31,30,31,30,31,31,30,31,30,31])
# monthly mean air T, approx 1991-2020 normals (pogodaiklimat / WMO tables; rounded, ASSUMED +/-1 K)
sites={
 'Norilsk':  [-26.0,-25.3,-21.1,-14.1,-5.4,6.4,15.3,11.4,4.0,-8.6,-20.0,-23.6],
 'Udachny/Mirny':[-36.5,-33.0,-23.5,-11.0,1.5,12.0,16.5,12.5,4.0,-9.0,-26.5,-34.0],
 'Pevek':    [-25.5,-26.0,-24.5,-17.0,-5.0,3.5,8.5,6.5,1.5,-8.5,-17.0,-23.0],
 'Salekhard':[-23.0,-22.1,-15.5,-9.0,-1.7,8.5,15.0,11.4,5.4,-3.3,-13.6,-19.7],
 'Nadym':    [-21.7,-20.0,-12.3,-6.0,0.4,10.0,16.4,12.6,5.9,-3.2,-13.6,-18.6],
 'Fairbanks (TAPS)':[-21.9,-18.9,-11.9,-1.1,9.3,15.4,16.9,13.9,7.6,-3.4,-15.4,-19.4],
 'Beiluhe (QTR)':[-14.5,-12.0,-7.5,-3.0,1.5,5.0,7.5,7.0,3.5,-3.0,-10.0,-13.5],
}
R=0.12      # K/W total thermosyphon+ground resistance, single 57-mm unit, ~10 m evaporator (Russian TMD-type; ASSUMED range 0.08-0.2)
dTstart=1.0 # K start-up difference
Tg=-3.0     # ground at evaporator, target state (deg C)
# annual heat load per unit: building leak 3 W/m2 over 9 m2 (one unit per pile at 3 m grid) + lateral climate gain
q_build=3*9   # W, continuous
q_lat=15      # W, lateral/basal heat gain into the cooled block in a warming climate (ASSUMED)
load_GJ=(q_build+q_lat)*8760*3600/1e9
def extr(T,warm=0.0):
    T=np.array(T)+warm
    dT=np.clip(Tg-dTstart-T,0,None)
    return (dT*days*86400/R).sum()/1e9, (np.clip(-T,0,None)*days).sum()
print(f"annual heat load per unit = {load_GJ:.2f} GJ")
print(f"{'site':18s} FDD  E_now GJ  margin  | +2.5K winter (2050) E  margin")
res={}
for s,T in sites.items():
    e,fdd=extr(T); e2,_=extr(T,2.5)
    res[s]=(fdd,e/load_GJ,e2/load_GJ)
    print(f"{s:18s} {fdd:5.0f} {e:6.2f} {e/load_GJ:6.2f}   | {e2:6.2f} {e2/load_GJ:6.2f}")
# Cooling to restore capacity: one-off cooling of 3x3x12 m block by 2 K, apparent heat cap incl. unfrozen water (saline loam) 5 MJ/m3K
oneoff=3*3*12*2*5/1e3
print(f"one-off cool-down per unit {oneoff:.2f} GJ -> years at Norilsk surplus:",
      round(oneoff/(extr(sites['Norilsk'])[0]-load_GJ),2))
# ---- cost per unit delivered
rub=85.0
Ni_eq=13.76e9/15500      # t Ni-eq/yr, revenue / Ni price (F241)
full_cost=5.1e9+3.0e9    # cash cost 2024 (F62) + capex (F61)
print(f"full cost per t Ni-eq = {full_cost/Ni_eq:,.0f} $")
crf=lambda i,n: i*(1+i)**n/((1+i)**n-1)
for unit_rub in (0.3e6,0.6e6,1.0e6):          # installed drilled unit, retrofit (hardware from 10k RUB, drilling dominates; ASSUMED)
  for nstruct in (30,50):
    units=nstruct*170                          # 3000 m2 footprint / 9 m2 per pile * 0.5 (one unit per 2 piles)
    capex=units*unit_rub/rub
    ann=capex*crf(0.14,25)+0.02*capex          # +2%/yr inspection, NCG checks every 3 yr
    print(f"unit {unit_rub/1e6:.1f}M RUB, {nstruct} structures: capex ${capex/1e6:5.0f}M, annual ${ann/1e6:5.1f}M = {100*ann/full_cost:.2f}% of full cost, ${ann/Ni_eq:4.1f}/t Ni-eq")
# Baselines per structure (3000 m2, 333 piles)
piles=333
base={'triaged retrofit (170 units x 0.6M)':170*0.6e6,
      'blanket retrofit all monitored (cost x 165/50)':170*0.6e6*165/50/50*50/165*3.3,  # per structure same, but 3.3x structures
      'underpinning: new piles to bedrock (2M RUB/pile, ASSUMED)':piles*2.0e6,
      'rebuild structure (~60k RUB/m2 industrial, ASSUMED)':3000*60e3}
for k,v in base.items(): print(f"{k:60s} {v/1e6:8.0f} M RUB/structure")
# Expected avoided losses (thaw-attributable share)
ambarnaya=146e9/rub     # F262 court award
for f,share in ((1/20,0.3),(1/10,0.5)):
    print(f"event freq {f:.2f}/yr, thaw share {share}: expected loss ${ambarnaya*f*share/1e6:.0f}M/yr (fine only)")
outage=13.76e9*0.4*30/365*0.48   # 30-d outage of a concentrator carrying ~40% of Ni-eq, lost EBITDA margin
print(f"30-day concentrator outage lost margin ${outage/1e6:.0f}M")
