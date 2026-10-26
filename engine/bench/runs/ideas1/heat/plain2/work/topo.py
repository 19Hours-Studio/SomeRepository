import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spl, sys
N,KH,SINK=101,200.0,5; n=N; idx=np.arange(n*n).reshape(n,n); c0=(n-SINK)//2
hi,hj=idx[:,:-1].ravel(),idx[:,1:].ravel(); vi,vj=idx[:-1,:].ravel(),idx[1:,:].ravel()
I=np.concatenate([hi,vi]); J=np.concatenate([hj,vj]); s=idx[0,c0:c0+SINK].ravel()
def solve(k, rhs_extra=None):
    kf=k.ravel(); a,b=kf[I],kf[J]; g=2*a*b/(a+b)
    diag=np.zeros(n*n); np.add.at(diag,I,g); np.add.at(diag,J,g); diag[s]+=2*kf[s]
    A=sp.csr_matrix((np.concatenate([-g,-g,diag]),(np.concatenate([I,J,np.arange(n*n)]),np.concatenate([J,I,np.arange(n*n)]))),shape=(n*n,n*n)).tocsc()
    lu=spl.splu(A); return lu,a,b
def evalk(k):
    lu,a,b=solve(k); return lu.solve(np.ones(n*n)).max()
def grad(k,P):
    lu,a,b=solve(k); T=lu.solve(np.ones(n*n))
    Tm=T.max(); w=(T/Tm)**P; J_=Tm*(w.mean())**(1/P)
    dJdT=J_/ (w.sum()) * w/T  # d/dT of (mean T^P)^(1/P)
    lam=lu.solve(dJdT)
    dT=(T[I]-T[J])*(lam[I]-lam[J])
    dga=2*b*b/(a+b)**2; dgb=2*a*a/(a+b)**2
    dk=np.zeros(n*n); np.add.at(dk,I,-dga*dT); np.add.at(dk,J,-dgb*dT)
    dk[s]+=-2*T[s]*lam[s]
    return J_,T.max(),dk.reshape(n,n)
