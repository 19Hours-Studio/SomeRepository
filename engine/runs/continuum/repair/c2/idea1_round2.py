# Round 2: die sized at the power-density limit (~1.4 W/mm2, same as Rubin) instead of 10 PF; add facility capex.
import math
exec(open('idea1_prefill.py').read().split('# ---------------- cost')[0].split('# Repaired design')[0])
def die_cost(a,wafer=20000,D0=0.10):
    r=150; dpw=math.pi*r*r/a-math.pi*2*r/math.sqrt(2*a); y=((1-math.exp(-D0*a/100))/(D0*a/100))**2; return wafer/(dpw*y)
hrs=4*8766; elec=0.08; pue=1.25; sysov=0.35; fac_per_W=10.0; fac_hrs=10*8766
def cph(cogs,W): return cogs*(1+sysov)/hrs + W*pue/1000*elec + W*pue*fac_per_W/fac_hrs
util=0.6; fl=flop_tok(8192)
BW=1.37e12*0.8
print("PFdie  W   W/mm2  balanceT(N=8)  TTFT@2xbal(s)  $/PF  $/Mtok  vsRubin  vsCPX-HBM4  vsB200")
rub=(2*die_cost(800)+288*16+1800+600, 2000, 35e15)
cpx=(die_cost(800)+168*16+1500+500, 1840, 30e15)
b2=(2*die_cost(800,17000)+192*12.4+1200+500, 1000, 9e15)
def cpm(c,W,pf): return cph(c,W)/(pf*util/fl*3600)*1e6
for PF in (10e15,20e15,30e15):
    W=57*PF/1e15+40      # Rubin-like 57 W/PF + LPDDR ~40 W (Vera: 30-40 W for 1.2 TB/s)
    c=die_cost(800)+64*10+650
    N=8; w=W_=W
    t_w=(376e9/N)/BW; Tbal=t_w/(fl/N/(PF*util)); ttft=N*max(t_w, 2*Tbal*fl/N/(PF*util))
    r=[cpm(c,W,PF)/cpm(*x) for x in (rub,cpx,b2)]
    print(f"{PF/1e15:4.0f} {W:6.0f} {W/800:5.2f} {Tbal:10.0f} {ttft:12.2f} {c/(PF/1e15):7.0f} {cpm(c,W,PF):.5f}  {1/r[0]:.2f}x  {1/r[1]:.2f}x  {1/r[2]:.2f}x")
for n,x in (("Rubin",rub),("CPX-HBM4",cpx),("B200",b2)):
    print(f"{n:9s} $/PF {x[0]/(x[2]/1e15):.0f}  $/Mtok {cpm(*x):.5f}  HBM GB per 1k tok/s {({'Rubin':288,'CPX-HBM4':168,'B200':192}[n])/(x[2]*util/fl/1e3):.2f}")
# sensitivity: LPDDR $21/GB and HBM4 at $32/GB (Samsung ask)
c21=die_cost(800)+64*21+650; print("LPDDR $21:", round(cpm(c21,1180,20e15),5), " Rubin w/ HBM4 $32:", round(cpm(2*die_cost(800)+288*32+2400,2000,35e15),5))
# MLA-heavy long context: 128K prompts are attention-FLOP dominated -> even more compute bound
print("FLOP/token 128K:", round(flop_tok(131072)/1e9), "GF -> balance T shrinks by", round(flop_tok(131072)/fl,1),"x")
