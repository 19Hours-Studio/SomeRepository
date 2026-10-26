import sys, math, numpy as np
sys.path.insert(0,'..')
import sim
s=math.sin(math.radians(3))
def trace(rec, mirrors, NX=200, NA=15, ret=False):
    segs=[(p[i],p[i+1]) for p in mirrors for i in range(len(p)-1)]
    A=np.array([q[0] for q in segs]+[rec[0]],float); Bp=np.array([q[1] for q in segs]+[rec[1]],float)
    E=Bp-A; n=len(A); is_rec=np.zeros(n,bool); is_rec[-1]=True
    xs=-0.5+(np.arange(NX)+0.5)/NX; an=-sim.THETA+(np.arange(NA)+0.5)/NA*2*sim.THETA
    X,G=np.meshgrid(xs,an); P=np.stack([X.ravel(),np.full(X.size,1-1e-9)],1); D=np.stack([np.sin(G.ravel()),-np.cos(G.ravel())],1)
    alive=np.ones(len(P),bool); got=np.zeros(len(P),bool)
    ch=max(1,3_000_000//n)
    for _ in range(200):
        live=np.nonzero(alive)[0]
        if not len(live): break
        for c0 in range(0,len(live),ch): sim.step(live[c0:c0+ch],P,D,A,E,is_rec,alive,got)
    if ret: return got.reshape(NA,NX)
    return got.mean()
def score(d, **k):
    w=np.linalg.norm(np.subtract(d['receiver'][1],d['receiver'][0]))
    eta=trace(d['receiver'],d['mirrors'],**k); return eta, eta/w*s
