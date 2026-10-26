# binary local search: swap moves guided by sensitivity, exact eval
import numpy as np, sys
sys.path.insert(0,'/home/user/SomeRepository/engine/bench/runs/ideas1/heat/plain2/work'); from topo import *
from scipy.ndimage import binary_dilation
src,out=sys.argv[1],sys.argv[2]; iters=int(sys.argv[3]); rng=np.random.default_rng(int(sys.argv[4]) if len(sys.argv)>4 else 0)
if src.endswith('.npy'):
    xf=np.load(src); o=np.argsort(-xf.ravel()); d=np.zeros(n*n,bool); d[o[:1020]]=True; d=d.reshape(n,n)
else:
    d=np.array([[c=='1' for c in l.strip()] for l in open(src) if l.strip()])
def K(d): return 1+(KH-1)*d
best=evalk(K(d)); print('start',best,flush=True)
for it in range(iters):
    J_,Tm,dk=grad(K(d),64)
    # gain of adding: -dk (at k=1, linearized scaled), loss of removing
    cand_add=binary_dilation(d)&~d
    add_s=np.where(cand_add,-dk,-np.inf).ravel(); rem_s=np.where(d,-dk,np.inf).ravel()
    A=np.argsort(-add_s)[:30]; R=np.argsort(rem_s)[:30]
    improved=False
    for t in range(40):
        a=A[min(int(rng.exponential(6)),29)]; r=R[min(int(rng.exponential(6)),29)]
        d2=d.copy(); ai,aj=divmod(a,n); ri,rj=divmod(r,n); d2[ai,aj]=d2[ai,n-1-aj]=True; d2[ri,rj]=d2[ri,n-1-rj]=False
        if d2.sum()>1020: continue
        v=evalk(K(d2))
        if v<best-1e-9: best=v; d=d2; improved=True; break
    if it%10==0: print(it,best,flush=True)
    if not improved: print('stuck',it,best)
    open(out,'w').write('\n'.join(''.join('1' if c else '0' for c in row) for row in d)+'\n')
print('final',best)
