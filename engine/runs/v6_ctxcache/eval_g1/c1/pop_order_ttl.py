import numpy as np, sys
# Popularity-first ordering replay with TTL: entry alive if touched within last W requests (W = requests per 5 min).
# bp: set of doc-count positions where a cache breakpoint is placed (Anthropic: <=4 breakpoints; writes only at breakpoints).
rng=np.random.default_rng(0)
C=100_000; K=5; NREQ=int(sys.argv[1]) if len(sys.argv)>1 else 200_000
def draws(s):
    p=1/np.arange(1,C+1)**s; p/=p.sum()
    out=[]
    raw=rng.choice(C,size=(NREQ,12),p=p)
    for row in raw:
        u=list(dict.fromkeys(row.tolist()))[:K]
        while len(u)<K: u.append(int(rng.choice(C,p=p))); u=list(dict.fromkeys(u))
        out.append(u)
    return out
def replay(reqs,W,bp):
    last={}; reuse=0
    for t,u in enumerate(reqs):
        o=sorted(u)  # id = popularity rank (Zipf rank) -> descending popularity, the counter's limit
        m=0
        for k in range(1,K+1):
            key=tuple(o[:k])
            if k in bp:
                if key in last and t-last[key]<=W: m=k
                last[key]=t
        reuse+=m
    return reuse/(len(reqs)*K)
cost=lambda r:(4*(0.1*r+1.25*(1-r))+1.8)
for s in (1.05,1.2,1.5):
    R=draws(s)
    res=[]
    for W in (10**9,100_000,10_000,1_000,100,10):
        for name,bp in (('all',{1,2,3,4,5}),('4bp',{2,3,4,5})):
            r=replay(R,W,bp); res.append((W,name,round(r,3),round(5.8/cost(r),3)))
    print(s,res,flush=True)
