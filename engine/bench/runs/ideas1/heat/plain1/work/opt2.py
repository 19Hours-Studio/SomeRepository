import sys, numpy as np
exec(open('opt.py').read().split('yy,xx')[0])
from scipy.ndimage import uniform_filter, gaussian_filter
def run(sched, seed=0, sym=True):
    rng=np.random.default_rng(seed)
    rho=np.full((n,n),0.1)+ (0.02*rng.standard_normal((n,n)) if seed else 0); rho=np.clip(rho,0.001,1)
    for p,P,R,it in sched:
        for t in range(it):
            k=1+(KH-1)*rho**p
            Jv,Tm,dk=grad(k,P)
            dc=dk*(KH-1)*p*rho**(p-1)
            if R>0: dc=gaussian_filter(dc*rho,R,mode='nearest')/np.maximum(rho,1e-3)
            if sym: dc=(dc+dc[:,::-1])/2
            dc=np.minimum(dc,-1e-14)
            l1,l2=1e-14,1e14; mv=0.05
            while l2/l1>1+1e-7:
                lm=np.sqrt(l1*l2)
                new=np.clip(rho*np.sqrt(-dc/lm),np.maximum(0.001,rho-mv),np.minimum(1,rho+mv))
                if new.mean()>0.1: l1=lm
                else: l2=lm
            rho=new
    order=np.argsort(-rho.ravel()); d=np.zeros(n*n,bool); d[order[:NF]]=True; d=d.reshape(n,n)
    T,_,_,_=solve(1+(KH-1)*d); return T.max(),d,rho
scheds={
 'A':[(1,8,1.5,100),(2,12,1.0,100),(3,20,0.7,100),(4,30,0.5,100),(5,40,0,100)],
 'B':[(1,10,1.0,150),(1.5,15,0.8,100),(2.5,25,0.6,100),(3.5,40,0.4,100),(5,60,0,100)],
 'C':[(2,8,1.0,150),(3,16,0.7,150),(4,30,0.5,100),(5,50,0,100)],
 'D':[(1,16,0.6,150),(2,20,0.5,150),(3,30,0.4,100),(5,60,0,100)],
}
key=sys.argv[1]
tm,d,rho=run(scheds[key])
print(key,tm,flush=True); np.save(f'd_{key}.npy',d)
