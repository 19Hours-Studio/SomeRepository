import numpy as np, hashlib
# Replay: 100k chunks, top-5 distinct Zipf draws (same generator as eval_g1/c1/pop_order_ttl.py).
# Measures doc-token reuse for exact prefix with hash-canonical vs popularity order, and chunk-level KV hit (for blending).
rng=np.random.default_rng(1); C=100_000; K=5; N=100_000
def draws(s):
    p=1/np.arange(1,C+1)**s; p/=p.sum(); raw=rng.choice(C,size=(N,16),p=p); out=[]
    for row in raw:
        u=list(dict.fromkeys(row.tolist()))[:K]
        while len(u)<K:
            u=list(dict.fromkeys(u+[int(rng.choice(C,p=p))]))
        out.append(u)
    return out
H=lambda x:hashlib.md5(str(x).encode()).hexdigest()
def replay(R,W,order):
    last={};lc={};reuse=0;ch=0
    for t,u in enumerate(R):
        o=sorted(u,key=H) if order=='hash' else sorted(u)
        m=0
        for k in range(1,K+1):
            key=tuple(o[:k])
            if key in last and t-last[key]<=W and m==k-1: m=k
            last[key]=t
        for c in u:
            if c in lc and t-lc[c]<=W: ch+=1
            lc[c]=t
        reuse+=m
    return reuse/(N*K), ch/(N*K)
# known-answer check: identical requests -> reuse ~1
same=[[1,2,3,4,5]]*1000; print('check identical',replay(same,10**9,'pop')[0]*1000/999)
for s in (1.05,1.2,1.5):
    R=draws(s)
    for W in (10**9,1000):
        rh,_=replay(R,W,'hash'); rp,hc=replay(R,W,'pop')
        print(f"s={s} W={W} hash={rh:.3f} pop={rp:.3f} chunkhit={hc:.3f}")
