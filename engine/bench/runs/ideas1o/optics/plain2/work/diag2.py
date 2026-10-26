import sys, math, numpy as np
sys.path.insert(0,'..'); import sim
def trace_info(rec, mirrors, NX=400, NA=9):
    segs=[];owner=[]
    for k,p in enumerate(mirrors):
        for i in range(len(p)-1): segs.append((p[i],p[i+1])); owner.append(k)
    owner=np.array(owner+[-1])
    A=np.array([q[0] for q in segs]+[rec[0]],float); Bp=np.array([q[1] for q in segs]+[rec[1]],float)
    E=Bp-A; n=len(A); is_rec=np.zeros(n,bool); is_rec[-1]=True
    xs=-0.5+(np.arange(NX)+0.5)/NX; an=-sim.THETA+(np.arange(NA)+0.5)/NA*2*sim.THETA
    X,G=np.meshgrid(xs,an); P=np.stack([X.ravel(),np.full(X.size,1-1e-9)],1); D=np.stack([np.sin(G.ravel()),-np.cos(G.ravel())],1)
    alive=np.ones(len(P),bool); got=np.zeros(len(P),bool)
    hits=[[] for _ in range(len(P))]
    for _ in range(50):
        live=np.nonzero(alive)[0]
        if not len(live): break
        p,d=P[live],D[live]
        den=d[:,None,0]*E[None,:,1]-d[:,None,1]*E[None,:,0]; q=A[None]-p[:,None]
        with np.errstate(all='ignore'):
            t=(q[...,0]*E[None,:,1]-q[...,1]*E[None,:,0])/den; u=(q[...,0]*d[:,None,1]-q[...,1]*d[:,None,0])/den
        ok=(np.abs(den)>1e-14)&(t>1e-9)&(u>=0)&(u<=1); t=np.where(ok,t,np.inf); j=t.argmin(1)
        for r,jj in zip(live,j):
            if np.isfinite(t[list(live).index(r) if False else 0,0]) or True: pass
        tm=t[np.arange(len(live)),j]
        for ii,r in enumerate(live):
            if np.isfinite(tm[ii]): hits[r].append(owner[j[ii]])
        sim.step(live,P,D,A,E,is_rec,alive,got)
    return xs,an,got.reshape(NA,NX),hits
