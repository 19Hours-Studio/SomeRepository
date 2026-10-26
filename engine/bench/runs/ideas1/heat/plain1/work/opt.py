import sys, numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spl
N,KH,SINK=101,200.0,5; n=N; idx=np.arange(n*n).reshape(n,n); c0=(n-SINK)//2
NF=int(0.10*n*n)
hi,hj=idx[:,:-1].ravel(),idx[:,1:].ravel(); vi,vj=idx[:-1,:].ravel(),idx[1:,:].ravel()
I=np.concatenate([hi,vi]); J=np.concatenate([hj,vj]); s=idx[0,c0:c0+SINK]
def solve(k):
    kf=k.ravel(); a,b=kf[I],kf[J]; g=2*a*b/(a+b)
    diag=np.zeros(n*n); np.add.at(diag,I,g); np.add.at(diag,J,g); diag[s]+=2*kf[s]
    A=sp.csc_matrix((np.concatenate([-g,-g,diag]),(np.concatenate([I,J,np.arange(n*n)]),np.concatenate([J,I,np.arange(n*n)]))),shape=(n*n,n*n))
    lu=spl.splu(A); T=lu.solve(np.ones(n*n)); return T,lu,a,b
def grad(k,P):
    T,lu,a,b=solve(k); Tm=T.max(); r=T/Tm
    Jv=Tm*np.mean(r**P)**(1/P)
    dJdT=np.mean(r**P)**(1/P-1)*r**(P-1)/(n*n)
    lam=lu.solve(dJdT)
    dg=-(lam[I]-lam[J])*(T[I]-T[J])
    ga=dg*2*b*b/(a+b)**2; gb=dg*2*a*a/(a+b)**2
    dk=np.zeros(n*n); np.add.at(dk,I,ga); np.add.at(dk,J,gb)
    dk[s]+=-lam[s]*T[s]*2
    return Jv,Tm,dk.reshape(n,n)
yy,xx=np.mgrid[0:n,0:n]
def filt(x,R):
    from scipy.ndimage import uniform_filter
    return uniform_filter(x,size=2*R+1,mode='nearest') if R>0 else x
rho=np.full((n,n),0.1)
for p,P,R,it in [(1,8,2,60),(2,12,2,60),(3,16,1,80),(3,30,1,80),(4,30,0,80)]:
    for t in range(it):
        k=1+(KH-1)*rho**p
        Jv,Tm,dk=grad(k,P)
        dc=dk*(KH-1)*p*rho**(p-1)
        dc=filt(dc,R)
        dc=np.minimum(dc,-1e-12)
        l1,l2=1e-12,1e12; mv=0.1
        while l2/l1>1+1e-6:
            lm=np.sqrt(l1*l2)
            new=np.clip(rho*np.sqrt(-dc/lm),np.maximum(0.001,rho-mv),np.minimum(1,rho+mv))
            if new.mean()>0.1: l1=lm
            else: l2=lm
        rho=new
    print(p,P,R,Tm,flush=True)
np.save('work/rho.npy',rho)
# threshold
order=np.argsort(-rho.ravel()); d=np.zeros(n*n,bool); d[order[:NF]]=True; d=d.reshape(n,n)
T,_,_,_=solve(1+(KH-1)*d); print('binary Tmax',T.max())
np.save('work/d.npy',d)
open('design.txt','w').write('\n'.join(''.join('1' if c else '0' for c in row) for row in d)+'\n')
