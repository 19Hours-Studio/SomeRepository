import numpy as np
rng=np.random.default_rng(1)
C=100000;R=200000
def run(s):
    w=1/np.arange(1,C+1)**s; w/=w.sum()
    cdf=np.cumsum(w)
    d=np.searchsorted(cdf,rng.random((R,8)))
    docs=[]
    for r in d:
        u=list(dict.fromkeys(r.tolist()))[:5]
        while len(u)<5: u.append(int(rng.integers(C)))  # rare
        docs.append(tuple(sorted(u)))
    out={}
    for N in (10,100,1000):
        hit=np.zeros(5);cnt=0;last=[{} for _ in range(5)]
        # frac of tokens with path hit = sum_k hit_k /5 per depth
        for i,u in enumerate(docs):
            for k in range(5):
                p=u[:k+1]
                j=last[k].get(p)
                if i>5000 and j is not None and i-j<=N: hit[k]+=1
                last[k][p]=i
            if i>5000: cnt+=1
        out[N]=hit/cnt
    return out
for s in (1.05,1.2,1.5):
    o=run(s)
    for N,h in o.items(): print(s,N,np.round(h,3),"doc-token reuse",round(h.mean(),3))
