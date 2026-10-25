from common import *
import numpy as np, itertools, statistics as st
from math import exp, factorial
# ---------- (1) Risk pooling under long grey-import lead time ----------
# Critical part type: demand lambda per site per year; lead time L years; base-stock S. Fill = P(D_L <= S-1) approx (Poisson).
def poisson_cdf(k,mu): 
    return sum(exp(-mu)*mu**i/factorial(i) for i in range(0,int(k)+1)) if k>=0 else 0.0
def stock_for_fill(mu, fill):
    S=0
    while poisson_cdf(S-1,mu) < fill: S+=1
    return S
print("Pooling: stock units needed for 95% no-wait probability per failure (Poisson), 6 Norilsk mines")
for lam,L in ((2,0.25),(2,0.75),(4,0.75),(1,1.0)):
    sep = 6*stock_for_fill(lam*L,0.95); pool = stock_for_fill(6*lam*L,0.95)
    print(f" lam {lam}/site/yr, lead {L*12:.0f} mo: separate {sep} units, pooled {pool} -> pooled needs {pool/sep:.0%}")
# With the same stock budget, which fill rate does pooling give?
lam,L=2,0.75; budget=6*stock_for_fill(lam*L,0.80)
print(f" fixed budget {budget} units (80% fill each site separately) -> pooled fill {poisson_cdf(budget-1,6*lam*L):.1%}")

# ---------- (2) Lost Ni-eq ranking: rich vs disseminated ore fleets ----------
# Rich (massive) Talnakh ore grades: ASSUMED ~3% Ni, 4% Cu, 8 g/t PGM (no source in ledger); cuprous/dissem = F1 Talnakh avg
rich = dict(Ni=3.0,Cu=4.0,Pd=5.4,Pt=1.4)
rec = dict(Ni=0.85,Cu=0.92,PGM=0.85)
v_rich = sum(value_per_t(rich,P,rec).values())*0.8
v_tal  = sum(value_per_t(ORES['Talnakh_proven(F1)'],P,rec).values())*0.8
v_n1   = sum(value_per_t(ORES['Norilsk1_dissem(F2)'],P,dict(Ni=.71,Cu=.8,PGM=.75)).values())*0.8
print(f"\nRecovered payable value per t ore: rich {v_rich:.0f}$, Talnakh avg {v_tal:.0f}$, Norilsk-1 {v_n1:.0f}$ -> rich/N1 = {v_rich/v_n1:.1f}x")
# LHD: 14 t bucket class, ~ 120 t/h effective (assumed); lost hour value
for nm,v in (('rich',v_rich),('Talnakh avg',v_tal),('N1',v_n1)):
    print(f"  LHD-hour (120 t/h) lost on {nm:11s} = {120*v:8,.0f} $  = {120*v/P['Ni']:.2f} t Ni-eq")

# ---------- (3) Programme economics vs capacity stage ----------
# Nornickel 2023 dip attributed to equipment switch (F64). Assumed lost output 2-5% of group Ni-eq (789 kt).
grp=789e3
def prog(avail_pts, rich_share_mined, mine_bound, cost_bn_yr, de_rating):
    """avail_pts: fleet availability gain (pp) on targeted fleets (base ~75%); mine_bound: fraction of time mine (not plant) binds.
       de_rating: domestic-part MTBF / OEM MTBF (affects net gain)"""
    base_av=0.75
    rel = avail_pts/100/base_av                       # relative fleet-hours gained
    # net of extra swaps from shorter-life parts: share of downtime from targeted parts ~40%; more failures by 1/de_rating
    penalty = 0.40*(1/de_rating-1)*(1-base_av)/base_av
    net = max(rel - penalty,0)
    # ranking by lost Ni-eq: rich-ore fleets carry rich_share of value
    dq = grp*net*mine_bound*(1.0 if rich_share_mined else 0.5)  # targeting priority: on value-weighted fleets gain applies to the value share
    cost = cost_bn_yr*1e9/FX + 1500*dq + 6.5e3*0.0
    return dq, cost/dq if dq>0 else float('inf')
print("\nProgramme: added Ni-eq and cost per added t (opex-only programme, downstream 1500$/t)")
for pts,mb,c,dr in ((3,0.6,3,0.7),(5,0.6,3,0.7),(3,0.4,5,0.5),(5,0.8,3,0.9),(2,0.4,5,0.6)):
    dq,cpt=prog(pts,True,mb,c,dr)
    print(f" +{pts}pp avail, mine binds {mb:.0%}, cost {c} bnRUB/yr, domestic MTBF {dr:.0%}: +{dq/1e3:5.1f} kt Ni-eq/yr ({dq/grp:.1%}), {cpt:6,.0f} $/t added")
# Capacity-stage comparator: Talnakh 2017 47 bn RUB (2017 RUB) -> +2.6 Mtpa; inflate x1.6 to 2026 + sanctions +40-70% (F57)
for esc in (1.4,1.7):
    capex = 47*1.6*esc*1e9/FX
    dq = 2.6e6*v_tal/P['Ni']
    ann = capex*(0.12/(1-1.12**-20))
    print(f" Brownfield capacity stage (Talnakh-2017 analog, x{esc}): +{dq/1e3:.0f} kt Ni-eq/yr, capex {capex/1e9:.1f} bn$, capex charge {ann/dq:,.0f} $/t + opex ore 45$/t ({45*2.6e6/dq:,.0f}$/t) + downstream 1500 -> {(ann+45*2.6e6)/dq+1500:,.0f} $/t")
