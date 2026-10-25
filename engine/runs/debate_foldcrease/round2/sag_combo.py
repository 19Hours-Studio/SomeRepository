"""Crease + face-up gravity sag, superposed (linear), worst-case sign: max_x |theta_c|+|theta_s|.
Sag: D theta'' - T theta = q x, theta(+-a)=0 (clamped). 30 um panel, R5.5, 15/15 mm ramps."""
import numpy as np
from scipy.linalg import solve_banded
from design2 import shares
from design3 import solve
tp,R=30e-6,5.5e-3; Dt,Dg,Dp,Da,zt=shares(tp); g=solve(R,15e-3,15e-3); a=g["half"]+3e-3
q=(2500*40e-6+1400*36e-6)*9.81; N=8001; x=np.linspace(-a,a,N); dx=x[1]-x[0]
def th(T,rhs):
    n=N-2; ab=np.zeros((3,n)); ab[0,1:]=Dt/dx**2; ab[1,:]=-2*Dt/dx**2-T; ab[2,:-1]=Dt/dx**2
    return np.concatenate([[0],solve_banded((1,1),ab,rhs[1:-1]),[0]])
for phis,phig in (((0.05,0.02),0),((0.2,0.1),0),((0.2,0.1),6e-4),((0.2,0.1),1e-3)):
    eff=(Dp*phis[0]+Da*phis[1]+Dg*phig)/Dt; kr=np.interp(x,g["s"],eff*g["k"],left=0,right=0)
    for T in (2000,3000,4000):
        tc=th(T,Dt*np.gradient(kr,dx)); ts=th(T,q*x)
        print(f"phi {phis} phi_g {phig:.0e} T={T}: crease {abs(tc).max()*1e3:.4f}, sag {abs(ts).max()*1e3:.4f}, worst sum {(abs(tc)+abs(ts)).max()*1e3:.4f} mrad")
