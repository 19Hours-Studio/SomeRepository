import json, math, sys, numpy as np
sys.path.insert(0,'.')
import sim
# trace with only central angle, report per-x outcome
d=json.load(open(sys.argv[1])); rec=np.array(d['receiver'],float)
NA=int(sys.argv[2]) if len(sys.argv)>2 else 1
sim.NA=NA
segs=[(np.array(p[i],float),np.array(p[i+1],float)) for p in d['mirrors'] for i in range(len(p)-1)]
old=sim.NX
got=[]
# reuse trace but extract got array: copy of trace
def trace(rec,mirrors,th):
    sim.THETA=th
    A = np.array([s[0] for s in segs] + [rec[0]], float); Bp = np.array([s[1] for s in segs] + [rec[1]], float)
    E=Bp-A; nseg=len(A); is_rec=np.zeros(nseg,bool); is_rec[-1]=True
    xs=-0.5+(np.arange(sim.NX)+0.5)/sim.NX; an=np.array([th])
    X,G=np.meshgrid(xs,an); P=np.stack([X.ravel(),np.full(X.size,1-1e-9)],1); D=np.stack([np.sin(G.ravel()),-np.cos(G.ravel())],1)
    alive=np.ones(len(P),bool); g=np.zeros(len(P),bool)
    for _ in range(200):
        live=np.nonzero(alive)[0]
        if not len(live): break
        sim.step(live,P,D,A,E,is_rec,alive,g)
    return xs,g
for th in [0,0.03,-0.03,0.05]:
    xs,g=trace(rec,d['mirrors'],th)
    print(th, g.mean(), ''.join('#' if v else '.' for v in g[::5]))
