"""Critic round-2 checks. Imports author code read-only (sys.path), writes nothing outside critic2."""
import sys, math, numpy as np
sys.path.insert(0,"../round2"); sys.path.insert(0,"../round1")
sys.dont_write_bytecode=True
from design2 import shares, open_shape
from design3 import solve, half
from scipy.linalg import solve_banded
tp,R=30e-6,5.5e-3; Dt,Dg,Dp,Da,zt=shares(tp)
print(f"0. D={Dt:.4e}  glass {Dg/Dt*100:.2f}%  panel {Dp/Dt*100:.3f}%  adh {Da/Dt*100:.3f}%  l=sqrt(D/T) @3000 = {math.sqrt(Dt/3000)*1e3:.2f} mm")
g=solve(R,15e-3,15e-3)
print(f"1. 15/15 geometry: Rn={g['Rn']*1e3:.2f} zone {g['zone']*1e3:.1f} width {g['width']*1e3:.2f} mm")
# analytic quasi-static estimate
for ps,pa,pg in ((0.2,0.1,0),(0.05,0.02,0),(0.2,0.1,1e-3)):
    S=Dp*ps+Da*pa+Dg*pg; dk=1/R+1/g['Rn']; kp=dk/15e-3
    for T in (1000,3000):
        d,sl,cv=open_shape(S/Dt*g['k'],g['s'],g['half']+3e-3,T,Dt,N=8001)
        print(f"   phi {ps}/{pa} g{pg:.0e} T={T}: analytic {S*dk/T*1e6:.3f} um {S*kp/T*1e3:.4f} mrad | numeric {d*1e6:.3f} um {sl*1e3:.4f} mrad, peak curvature {cv:.4f} 1/m = {2*cv*1e3:.1f} mdpt (reflective power)")
# 2. folded geometry: lateral excursion vs distance from spine
s,k,psi,x=half(R,g['Rn'],15e-3,15e-3,g['Lb2'],0.0)
y=np.concatenate([[0],np.cumsum(np.sin((psi[1:]+psi[:-1])/2)*np.diff(s))])
print("2. folded shape (per half): depth into the half body (x - g/2) vs distance from spine tip y")
for yy in (2,5,10,15,20,25,30):
    i=np.argmin(abs(y-yy*1e-3)); print(f"   y={yy:2d} mm: cavity depth {(x[i]-0.2e-3)*1e3:5.2f} mm")
print(f"   total y-extent of curved zone {y[-1]*1e3:.1f} mm; min x along curve {x[50:].min()*1e3:.3f} mm (must stay >= g/2=0.2)")
# robustness of geometry branch: neighbouring ramps
for L in (13e-3,14e-3,15e-3,16e-3,17e-3):
    gg=solve(R,L,L); print(f"   ramps {L*1e3:.0f}: " + ("none" if gg is None else f"Rn {gg['Rn']*1e3:.1f} zone {gg['zone']*1e3:.0f} width {gg['width']*1e3:.1f}"))
# 3. boundary terms the model omits: clamp angle mismatch, height step, pressure
a=g['half']+3e-3; N=8001; X=np.linspace(-a,a,N); dx=X[1]-X[0]
def solveth(T,rhs,thL=0,thR=0):
    n=N-2; ab=np.zeros((3,n)); ab[0,1:]=Dt/dx**2; ab[1,:]=-2*Dt/dx**2-T; ab[2,:-1]=Dt/dx**2
    r=rhs[1:-1].copy(); r[0]-=Dt/dx**2*thL; r[-1]-=Dt/dx**2*thR
    return np.concatenate([[thL],solve_banded((1,1),ab,r),[thR]])
T=3000
print(f"3a. wing angle mismatch delta (each wing tilted delta/2, T={T}); kink = slope change vs wing within ~l of the clamp")
for dl in (1e-3,0.1e-3,0.05e-3):
    th=solveth(T,np.zeros(N),-dl/2,dl/2); mid=th[N//2]
    print(f"   delta {dl*1e3:.2f} mrad ({math.degrees(dl):.4f} deg): slope change at clamp {abs(th[-1]-mid)*1e3:.4f} mrad over {math.sqrt(Dt/T)*1e3:.2f} mm")
print(f"3b. height step dh between wings (parallel): chord slope dh/(2a); kink at each clamp = dh/(2a)")
for dh in (1e-6,2e-6,5e-6,20e-6): print(f"   dh {dh*1e6:4.0f} um -> kink {dh/(2*a)*1e3:.4f} mrad")
print("3c. pressure difference across the free span (q=dP), worst slope and deflection")
for dP in (1,10,50,340):
    th=solveth(T,dP*X); w=np.concatenate([[0],np.cumsum((th[1:]+th[:-1])/2)*dx])
    print(f"   dP {dP:4d} Pa: slope {abs(th).max()*1e3:.4f} mrad, deflection {(w.max()-w.min())*1e6:.2f} um")
P0,T0=101.3e3,298
print(f"   sealed cavity, +1 K: dP={P0/T0:.0f} Pa ; vented cavity with time constant tau, heating 10 K/10 min: dP ~ P0*(dT/dt)/T0*tau = {P0*(10/600)/T0:.1f} Pa per s of tau")
# 3d. eccentric frame load -> bowing of each half
F=3000*0.15
for e,EI in ((1e-3,40.0),(2e-3,40.0),(2e-3,20.0)):
    M=F*e; L=0.072; print(f"3d. frame compression {F:.0f} N, eccentricity {e*1e3:.0f} mm, half EI {EI:.0f} N m^2: wing end slope {M/EI*L*1e3:.2f} mrad; +-20% thermal -> +-{0.2*M/EI*L*1e3:.2f} mrad")
# 4. lever: R vs depth at fixed polymer set (Rn,ramps fixed as 15/15 solve) and glass stress
print("4. lever: bulb radius (15/15 ramps re-solved), 20/10 set, phi_g 0 and 1e-3, T=3000")
for RR in (4.5e-3,5.5e-3,7e-3,9e-3):
    gg=solve(RR,15e-3,15e-3)
    if gg is None: print(f"   R {RR*1e3}: no solution"); continue
    out=[]
    for pg in (0,1e-3):
        S=(Dp*0.2+Da*0.1+Dg*pg)*(R/RR)  # polymer/glass set strain ~ proportional to folded strain (linear set), so eff set curvature ~ phi*kappa as before
        d,sl,cv=open_shape(S/Dt*gg['k']*(RR/R),gg['s'],gg['half']+3e-3,3000,Dt,N=8001)
        out.append(f"phi_g {pg:.0e}: {d*1e6:.2f} um/{sl*1e3:.4f} mrad")
    print(f"   R {RR*1e3:.1f} mm: glass {72e9*zt/2/RR/1e6:.0f} MPa, Rn {gg['Rn']*1e3:.1f}, zone {gg['zone']*1e3:.0f}, width {gg['width']*1e3:.1f} | "+" | ".join(out))
# 5. finger 1N contact on backstop frequency; membrane stiffness
print(f"5. membrane estimate 1 N -> {1/(2*math.pi*3000)*math.log(0.038/4e-3)*1e6:.0f} um (author 119)")
