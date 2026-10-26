import numpy as np, sys
sys.path.insert(0,'/home/user/SomeRepository/engine/bench/runs/ideas1/heat/plain2/work'); from topo import *
from scipy.ndimage import binary_dilation
src,out=sys.argv[1],sys.argv[2]; P=float(sys.argv[3]); rng=np.random.default_rng(int(sys.argv[4])); TL=float(sys.argv[5])
import time; t0=time.time()
d=np.array([[c=='1' for c in l.strip()] for l in open(src) if l.strip()])
def K(d): return 1+(KH-1)*d
def ev(d):
    lu,_,_=solve(K(d)); T=lu.solve(np.ones(n*n)); m=T.max(); return m*np.mean((T/m)**P)**(1/P), m
J,best=ev(d); bestd=d.copy(); print('start',J,best,flush=True); it=0
while time.time()-t0<TL:
    _,_,dk=grad(K(d),P)
    cand_add=binary_dilation(d)&~d
    add_s=np.where(cand_add,-dk,-np.inf).ravel(); rem_s=np.where(d,-dk,np.inf).ravel()
    A=np.argsort(-add_s)[:80]; R=np.argsort(rem_s)[:80]
    ok=False
    for t in range(30):
        a=A[min(int(rng.exponential(10)),79)]; r=R[min(int(rng.exponential(10)),79)]
        d2=d.copy().ravel(); d2[a]=True; d2[r]=False; d2=d2.reshape(n,n)
        j,m=ev(d2)
        if j<J: J=j; d=d2; ok=True
        if m<best: best=m; bestd=d2.copy(); open(out,'w').write('\n'.join(''.join('1' if c else '0' for c in row) for row in bestd)+'\n')
        if ok: break
    it+=1
    if it%20==0: print(it,J,best,flush=True)
print('final',best)
