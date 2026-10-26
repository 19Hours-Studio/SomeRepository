import sys, numpy as np
exec(open('opt.py').read().split('yy,xx')[0])
from scipy.ndimage import binary_dilation
d=np.load(sys.argv[1]); out=sys.argv[2]
def tm(d): return solve(1+(KH-1)*d)[0].max()
best=tm(d); print('start',best,flush=True)
def orb(c):
    i,j=divmod(c,n); return {c, i*n+(n-1-j)}
W=12
for rnd in range(3000):
    _,_,dk=grad(1+(KH-1)*d,300)
    dks=(dk+dk[:,::-1])/2
    front=binary_dilation(d)&~d
    add=np.flatnonzero(front.ravel()); add=add[np.argsort(dks.ravel()[add])]
    rem=np.flatnonzero(d.ravel()); rem=rem[np.argsort(-dks.ravel()[rem])]
    def uniq(L):
        seen=set(); r=[]
        for c in L:
            o=frozenset(orb(c))
            if o not in seen: seen.add(o); r.append(o)
        return r
    A=uniq(add)[:W]; R=uniq(rem)[:W]
    improved=False
    for a in A:
        for r in R:
            if len(a)!=len(r): continue
            dd=d.copy().ravel(); dd[list(a)]=True; dd[list(r)]=False
            if dd.sum()>NF: continue
            v=tm(dd.reshape(n,n))
            if v<best-1e-9: best=v; d=dd.reshape(n,n); improved=True; break
        if improved: break
    if not improved:
        if W<40: W*=2; print('widen',W,flush=True); continue
        print('stuck',rnd); break
    if rnd%10==0: print(rnd,best,flush=True); np.save(out,d)
np.save(out,d); print('final',best)
