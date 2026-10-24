# Beam-column crease model: minimise  int D/2 (w''-k_r)^2 + T/2 w'^2  with clamped ends at the
# edges of the free bend zone and unilateral support plate (w>=0, plate below; + = up toward viewer).
import numpy as np
from scipy.optimize import lsq_linear
from strain import stack

EI = lambda t,E: E*1e9*(t*1e-6)**3/12
D_lam = sum(EI(t,E) for n,t,E,c in stack)          # decoupled layers (soft OCA)
def teardrop_profile(R, n=1200, neck_angle=np.radians(35), neck_ratio=3.0, flat=4.0):
    """curvature (1/m) along arclength (m): neck(-) | tip(+) of total angle pi+2*neck | neck(-)"""
    Rn=neck_ratio*R
    Ltip=(np.pi+2*neck_angle)*R; Lneck=neck_angle*Rn
    L=Ltip+2*Lneck+2*flat
    x=np.linspace(0,L,n)*1e-3
    k=np.zeros(n); s=x*1e3
    a=flat; b=a+Lneck; c=b+Ltip; d=c+Lneck
    k[(s>=a)&(s<b)]=-1/(Rn*1e-3); k[(s>=b)&(s<c)]=1/(R*1e-3); k[(s>=c)&(s<d)]=-1/(Rn*1e-3)
    return x,k
def solve(x,kr,T,D=D_lam,contact=True):
    n=len(x); h=x[1]-x[0]
    D2=(np.eye(n,k=-1)-2*np.eye(n)+np.eye(n,k=1))[1:-1]/h**2
    D1=(np.eye(n,k=1)-np.eye(n))[:-1]/h
    A=np.vstack([np.sqrt(D*h)*D2, np.sqrt(max(T,0)*h)*D1]); b=np.concatenate([np.sqrt(D*h)*kr[1:-1], np.zeros(n-1)])
    lb=np.zeros(n) if contact else -np.inf*np.ones(n); ub=np.inf*np.ones(n)
    lb[[0,1,-2,-1]]=-1e-15; ub[[0,1,-2,-1]]=1e-15     # clamped: w=0,w'=0
    r=lsq_linear(A,b,bounds=(lb,ub),method='bvls' if n<400 else 'trf',lsmr_tol='auto',max_iter=5000)
    w=r.x; sl=np.gradient(w,x); cu=np.gradient(sl,x)
    return w, sl, cu
def metrics(x,w,sl,cu):
    return dict(depth_um=(w.max()-w.min())*1e6, slope_mrad=np.abs(sl).max()*1e3, curv_inv_m=np.abs(cu).max())
def residual_kr(R, phi, eps_c, k_oca_frac=0.0):
    """laminate residual curvature fraction c = k_res/k_fold from per-layer set above threshold eps_c"""
    num=0
    for n,t,E,creeps in stack:
        if not creeps or E<0.01: continue
        eps=t*1e-3/(2*R)
        k_i=phi*max(0,eps-eps_c)/(t*1e-6/2)       # residual curvature of layer i, 1/m
        num+=EI(t,E)*k_i
    c=(num/D_lam)/(1/(R*1e-3))
    return c+k_oca_frac
if __name__=="__main__":
    print(f"D_lam (decoupled) = {D_lam:.3e} N m ; fully-bonded figure used by kill test 6.6e-4")
    # verification: no contact, T=0 vs closed-form for simple tip-only profile? check linear scaling + FD convergence
    for n in [300,600,1200]:
        x,k=teardrop_profile(3.0,n=n); w,s,c=solve(x,0.05*k,0,contact=False)
        print("n",n,metrics(x,w,s,c))
