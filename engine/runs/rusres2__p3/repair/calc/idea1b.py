from common import *
import itertools, statistics as st
REC_NOF = dict(Ni=0.71, Cu=0.80, PGM=0.75)   # Ni: AR2020; Cu/PGM assumed
REC_TOF = dict(Ni=0.85, Cu=0.92, PGM=0.85)   # Ni: AR2020 83-88%; Cu/PGM assumed
PAY=0.80
def crf(r,n): return r/(1-(1+r)**-n)
def nieq(ore,rec,mt,p=P): return nieq_t(sum(value_per_t(ORES[ore],p,rec).values()))*mt*1e6*PAY
# opex assumptions USD/t ore (mine+mill) and USD/t Ni-eq downstream; group check: 5.1bn$/789kt => ~6.5k$/t Ni-eq all-in cash
OPEX_ORE = {'Talnakh_proven(F1)':45., 'Norilsk1_dissem(F2)':35., 'Maslovskoye(F7)':45.}
OPEX_DOWN = 1500.

def route(name, flows, capex_bn, life=20, r=0.12, p=P, fx=FX):
    """flows: list of (ore, rec, Mtpa). capex_bn: PV RUB bn. returns kt Ni-eq/yr and full $/t Ni-eq"""
    q = sum(nieq(o,rc,m,p) for o,rc,m in flows)
    opex = sum(OPEX_ORE[o]*m*1e6 for o,rc,m in flows) + OPEX_DOWN*q
    cap = capex_bn*1e9/fx*crf(r,life)
    return q, (opex+cap)/q, cap/(opex+cap)

def scenario(cap_tof3=100, uf=0.5, life_ext=25, newconc_9=90, defer=8, n1_mine=30, p=P, fx=FX, verbose=False):
    rec_m = {k: REC_NOF[k]+uf*(REC_TOF[k]-REC_NOF[k]) for k in REC_NOF}
    T='Talnakh_proven(F1)'; N='Norilsk1_dissem(F2)'
    # Incremental flows vs today (today: 5 Mtpa Talnakh at NOF, ~3 Mtpa N1 at NOF)
    uplift = nieq(T,rec_m,5)-nieq(T,REC_NOF,5)
    inc_alone = [(T,rec_m,2.8)]                       # TOF-3 alone: +2.8 Mtpa new Talnakh ore, moved ore gains uplift
    inc_refill= [(N,REC_NOF,4.0),(T,rec_m,2.8)]      # + Norilsk-1 refill of freed NOF (to 7 Mtpa, F360)
    # capex PV (RUB bn)
    defer_pv = newconc_9*(1-1/(1+0.12)**defer)       # PV saved by deferring 9 Mtpa first section of new dissem concentrator
    c_alone = cap_tof3
    c_pair  = cap_tof3 + life_ext + n1_mine
    c_plan  = cap_tof3 + newconc_9 + n1_mine         # Nornickel 2021 plan: new 9 Mtpa section now, NOF retired
    out={}
    for nm,fl,c in (('TOF-3 alone',inc_alone,c_alone),('Pair (refill NOF)',inc_refill,c_pair),('Plan (new conc now)',inc_refill,c_plan),
                    ('Pair, new conc after defer',inc_refill,c_pair+newconc_9-defer_pv)):
        q,cost,cs = route(nm,fl,c,p=p,fx=fx); q+=uplift
        q2,cost2,_ = route(nm,fl,c,p=p,fx=fx)
        # recompute cost incl uplift tonnes (uplift has ~zero extra opex except downstream)
        tot = cost2*q2 + OPEX_DOWN*uplift
        out[nm]=(q, tot/q, c)
        if verbose: print(f" {nm:28s} +{q/1e3:5.1f} kt Ni-eq/yr  capex {c:5.0f} bnRUB  incr full cost {tot/q:6,.0f} $/t Ni-eq  capex/annual t {c*1e9/q/1e3:5.0f}k RUB")
    return out

print("BASE (Ni 16k, Pd 1300, Pt 1800 $; 85 RUB/$; 12% real, 20 y)")
o=scenario(verbose=True)
print("\nGroup full cost ~10,260 $/t Ni-eq (base.py)")
print("\nSensitivity over TOF-3 capex 70-130, uplift 0.25-0.75, life-ext 15-60, new 9Mtpa section 60-130, N1 mine 20-45, prices base/hi:")
R=[];A=[]
for c,uf,le,nc,nm,p in itertools.product([70,100,130],[.25,.5,.75],[15,25,40,60],[60,90,130],[20,30,45],[P,P_hi]):
    o=scenario(c,uf,le,nc,8,nm,p)
    R.append(o['Pair (refill NOF)'][1]/o['Plan (new conc now)'][1]); A.append(o['Pair (refill NOF)'][1]/o['TOF-3 alone'][1])
print(f" pair/plan incr full cost: min {min(R):.2f} med {st.median(R):.2f} max {max(R):.2f}")
print(f" pair/alone incr full cost: min {min(A):.2f} med {st.median(A):.2f} max {max(A):.2f}")
# break-even life-extension cost where pair = plan
for le in range(10,200,5):
    o=scenario(life_ext=le)
    if o['Pair (refill NOF)'][1]>=o['Plan (new conc now)'][1]: print(f" break-even NOF life-ext capex = {le} bn RUB (= new 9 Mtpa section capex 90)"); break
