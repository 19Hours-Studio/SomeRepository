import numpy as np
rng=np.random.default_rng(0)
N=100000
for s in (1.05,1.2,1.5):
    p=1/np.arange(1,N+1)**s;p/=p.sum()
    for W in (10,100,1000):
        R=20000
        # top-5 sample w/o replacement via Gumbel; popularity order = by index
        g=np.log(p)[None,:]  # too big; use sampling by rejection
        reqs=[]
        for _ in range(R):
            d=set()
            while len(d)<5: d.add(int(rng.choice(N,p=None) if False else 0))
            break
        # fast: sample with replacement dedupe
        draws=rng.choice(N,size=(R,12),p=p)
        paths=[]
        for r in draws:
            u=sorted(set(r.tolist()))[:5]; paths.append(tuple(u))
        out=[]
        for depth in (1,3,5):
            seen={};hit=0
            for i,pt in enumerate(paths):
                k=pt[:depth]
                if k in seen and i-seen[k]<=W: hit+=1
                seen[k]=i
            out.append(round(hit/R,3))
        print(s,W,"path reuse by depth1/3/5",out)
