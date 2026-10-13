# Germany 2012-2017 daily data (OPSD via jenfly/opsd). Build a 100% wind+solar system,
# normalise each source by its trailing-365d mean (removes capacity growth), scale so that
# annual VRE = OVER * consumption. Study the residual deficit time series.
import csv, statistics as st
rows=[r for r in csv.DictReader(open('data/opsd_germany_daily.csv')) if r['Wind'] and r['Solar'] and r['Consumption']]
D=[r['Date'] for r in rows]; L=[float(r['Consumption']) for r in rows]
W=[float(r['Wind']) for r in rows]; S=[float(r['Solar']) for r in rows]
def norm(x):
    out=[];
    for i in range(len(x)):
        lo=max(0,i-182); hi=min(len(x),i+183)
        out.append(x[i]/ (sum(x[lo:hi])/(hi-lo)))
    return out
Wn,Sn=norm(W),norm(S)
Lm=st.mean(L)
def run(OVER=1.3, fw=0.65, quiet=False):
    G=[OVER*Lm*(fw*w+(1-fw)*s) for w,s in zip(Wn,Sn)]
    R=[g-l for g,l in zip(G,L)]           # GWh/day, + surplus
    deficit=[max(0,-x) for x in R]; surplus=[max(0,x) for x in R]
    n_years=len(R)/365.25
    Edef=sum(deficit)/n_years             # GWh/yr delivered by storage (perfect efficiency)
    Pmax=max(deficit)/24                  # GW daily-mean peak
    H_full=Edef/Pmax                      # full-load hours of a converter sized to daily peak
    if not quiet:
        print(f"OVER={OVER} wind share={fw}: deficit energy {Edef/1000:.1f} TWh/yr ({Edef/sum(L)*n_years*100:.1f}% of load),"
              f" surplus {sum(surplus)/n_years/1000:.1f} TWh/yr, peak daily-mean deficit {Pmax:.1f} GW"
              f" (mean load {Lm/24:.1f} GW), converter full-load hours {H_full:.0f} h/yr")
    return R
R=run(1.3); run(1.5); run(1.2)
# Two-tier: LDES converter capped at P_cap (GW), a medium buffer (days of energy) covers the rest.
# Medium buffer is recharged by LDES converter (when deficit<P_cap) or by surplus.
def two_tier(R, P_cap, Ebuf):
    buf=Ebuf; worst=0; ld=0; unmet=0
    for x in R:
        need=max(0,-x)            # GWh/day
        ldes=min(P_cap*24, need + (Ebuf-buf))  # LDES runs flat-out to cover need and refill buffer
        if x>0:  # surplus refills buffer first
            refill=min(x, Ebuf-buf); buf+=refill
            ldes=min(P_cap*24, Ebuf-buf) if buf<Ebuf else 0
        buf += ldes - need
        if buf<0: unmet+= -buf; buf=0
        buf=min(buf,Ebuf); ld+=ldes
    return ld, unmet
n_years=len(R)/365.25
Pmax=max(max(0,-x) for x in R)/24
print("\nTwo-tier sizing (OVER=1.3): LDES converter cap vs buffer energy needed for zero unmet")
for frac in (1.0,0.7,0.5,0.4,0.3,0.25,0.2):
    P=frac*Pmax
    lo,hi=0,20000
    for _ in range(40):
        mid=(lo+hi)/2
        if two_tier(R,P,mid)[1]>1e-6: lo=mid
        else: hi=mid
    ld,_=two_tier(R,P,hi)
    print(f"  LDES conv {P:5.1f} GW ({frac:.2f} of peak): buffer {hi/1000:5.2f} TWh = {hi/(Lm):4.2f} days of mean load,"
          f" LDES full-load hours {ld/n_years/P:5.0f} h/yr")
