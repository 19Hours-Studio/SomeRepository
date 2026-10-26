import sys, numpy as np
exec(open('opt.py').read().split('yy,xx')[0])
from scipy.ndimage import binary_dilation
d=np.load(sys.argv[1]); out=sys.argv[2]
def tm(d): return solve(1+(KH-1)*d)[0].max()
best=tm(d); print('start',best,flush=True)
rng=np.random.default_rng(int(sys.argv[3]) if len(sys.argv)>3 else 0)
for rnd in range(400):
    k=1+(KH-1)*d
    _,_,dk=grad(k,200)  # dJ/dk, negative = adding helps
    gain_add=-dk*(KH-1); 
    front=binary_dilation(d)&~d
    add=np.flatnonzero((front).ravel()); add=add[np.argsort(-gain_add.ravel()[add])][:30]
    rem=np.flatnonzero(d.ravel()); rem=rem[np.argsort(-dk.ravel()[rem])][:30]  # least useful
    improved=False
    pairs=[(a,r) for a in add[:12] for r in rem[:12]]; rng.shuffle(pairs)
    for a,r in pairs[:40]:
        dd=d.copy().ravel(); dd[a]=True; dd[r]=False; dd=dd.reshape(n,n)
        v=tm(dd)
        if v<best-1e-9:
            best=v; d=dd; improved=True; break
    if not improved: print('stuck',rnd); break
    if rnd%10==0: print(rnd,best,flush=True); np.save(out,d)
np.save(out,d); print('final',best)
