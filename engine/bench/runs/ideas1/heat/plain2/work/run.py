import numpy as np, sys
sys.path.insert(0,'work'); from topo import *
from scipy.ndimage import convolve
VF=1020/(n*n); P=int(sys.argv[1]) if len(sys.argv)>1 else 8; R=float(sys.argv[2]) if len(sys.argv)>2 else 1.5
rho=np.full((n,n),VF)
r=int(np.ceil(R)); yy,xx=np.mgrid[-r:r+1,-r:r+1]; H=np.maximum(0,R-np.sqrt(xx**2+yy**2))
def filt(x): return convolve(x,H,mode='nearest')/convolve(np.ones_like(x),H,mode='nearest')
it=0; bestb=1e9
for pen in [1,2,3,4,5,6,8]:
  for k_ in range(60):
    xf=filt(rho)
    k=1+(KH-1)*xf**pen
    J_,Tm,dk=grad(k,P)
    dr=filt(dk*(KH-1)*pen*np.maximum(xf,1e-6)**(pen-1))
    dr=np.minimum(dr,-1e-12)
    l1,l2=1e-12,1e12; m=0.1
    while l2/l1>1+1e-6:
        lm=np.sqrt(l1*l2); new=np.clip(rho*np.sqrt(-dr/lm),np.maximum(0,rho-m),np.minimum(1,rho+m))
        if filt(new).mean()>VF: l1=lm
        else: l2=lm
    ch=abs(new-rho).max(); rho=new; it+=1
  # binarize report
  xf=filt(rho); o=np.argsort(-xf.ravel()); d=np.zeros(n*n,bool); d[o[:1020]]=True
  vb=evalk(1+(KH-1)*d.reshape(n,n)); print(pen,J_,Tm,'binary',vb,flush=True)
  if vb<bestb:
    bestb=vb; open('/home/user/SomeRepository/engine/bench/runs/ideas1/heat/plain2/work/bin_%d_%s.txt'%(P,R),'w').write('\n'.join(''.join('1' if c else '0' for c in row) for row in d.reshape(n,n))+'\n')
np.save('/home/user/SomeRepository/engine/bench/runs/ideas1/heat/plain2/work/rho_%d_%s.npy'%(P,R),filt(rho))
