from common import *
import itertools, statistics as st
grp=789e3            # group Ni-eq kt (base.py)
FULL=10260           # $/t Ni-eq group full cost (base.py)
def model(A0=0.72, W=0.35, fill0=0.80, fill1=0.99, lt0=9, lt1=3, d=0.7, crit_share=0.5, mttr_ratio=1.0,
          value_share=0.60, fleet_share=0.35, mine_bound=0.6, cost_bn=3.0):
    """A0: current mechanical availability of underground fleet; W: share of downtime spent waiting for parts.
    Pooling raises fill fill0->fill1 (computed in idea2.py: same stock budget 80%->99.5%).
    Reverse-engineered parts cut lead time lt0->lt1 months for crit_share of waits; but last d x OEM life
    -> failure events of those parts x 1/d. Programme targets fleets carrying value_share of Ni-eq with fleet_share of machines."""
    down=1-A0; wait=down*W; repair=down*(1-W)
    # waiting time ~ (1-fill)*lead time
    wait1 = wait*((1-fill1)/(1-fill0))*( (crit_share*lt1+(1-crit_share)*lt0)/lt0 )
    # but a stockout-free system still has logistics wait floor ~10% of original
    wait1 = max(wait1, 0.10*wait)
    repair1 = repair*(1 + crit_share*0.4*(1/d-1)*mttr_ratio)   # 40% of repair events are on the targeted part families
    A1 = 1-(wait1+repair1)
    dA = A1-A0
    dq = grp*value_share*(dA/A0)*mine_bound
    cost = cost_bn*1e9/FX*fleet_share/0.35 + 1500*dq
    return dA, dq, (cost/dq if dq>0 else float('inf'))
dA,dq,c=model()
print(f"BASE: availability +{dA*100:.1f} pp, +{dq/1e3:.1f} kt Ni-eq/yr ({dq/grp:.1%} of group), {c:,.0f} $/t added Ni-eq")
# group full-cost effect: fixed costs spread
print(f" group full cost/t Ni-eq: {FULL:,.0f} -> {(FULL*grp + c*dq)/(grp+dq):,.0f}  ({((FULL*grp + c*dq)/(grp+dq))/FULL-1:+.1%})")
# break-even domestic life ratio d (dA = 0)
for d in [x/100 for x in range(20,101,2)]:
    if model(d=d)[0]>0: print(f" break-even domestic/OEM part life d = {d:.2f}"); break
# untargeted (rank by machine-hours not by Ni-eq): same programme spread on all fleets -> value_share=fleet_share
dA2,dq2,c2=model(value_share=0.35)
print(f" untargeted (value share = fleet share 35%): +{dq2/1e3:.1f} kt, {c2:,.0f} $/t  -> targeting gain x{dq/dq2:.2f}")
R=[]
for A0,W,d,mb,cb,vs in itertools.product([.65,.72,.80],[.2,.35,.5],[.5,.7,.9],[.4,.6,.85],[2,3,6],[.45,.6,.7]):
    a,q,cc=model(A0=A0,W=W,d=d,mine_bound=mb,cost_bn=cb,value_share=vs); R.append((cc,q,a))
cs=[r[0] for r in R if r[1]>0]; qs=[r[1] for r in R]
print(f" sensitivity: positive in {len(cs)}/{len(R)}; $/t added: p10 {st.quantiles(cs,n=10)[0]:,.0f} median {st.median(cs):,.0f} p90 {st.quantiles(cs,n=10)[-1]:,.0f}; added kt median {st.median(qs)/1e3:.1f}, max {max(qs)/1e3:.1f}")
print(" comparators: brownfield stage 7,300-8,100 $/t added (idea2.py); TOF-3 alone 6,660 $/t; group average full cost 10,260 $/t")
