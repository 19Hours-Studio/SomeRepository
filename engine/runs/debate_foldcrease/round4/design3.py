"""Round-2 lever study: smoothed teardrop with free neck curvature (geometry re-solved to close the fold),
baseline panel 30 um (R=5.5 mm keeps glass at ~500 MPa), tension up to 3000 N/m, glass anelastic set phi_g.
Neck: ramp Lr1 from 1/R to -1/Rn, plateau Ln, ramp Lr2 back to 0; unknowns bulb plateau Lb2 and Rn."""
import numpy as np, math
from scipy.optimize import fsolve
from design2 import open_shape, shares, ARC
def half(R, Rn, Lr1, Lr2, Lb2, Ln, m=6000):
    S=[0,Lb2,Lb2+Lr1,Lb2+Lr1+Ln,Lb2+Lr1+Ln+Lr2]; K=[1/R,1/R,-1/Rn,-1/Rn,0]
    s=np.linspace(0,S[-1],m); k=np.interp(s,S,K)
    psi=np.concatenate([[0],np.cumsum((k[1:]+k[:-1])/2*np.diff(s))])
    x=np.concatenate([[0],np.cumsum(np.cos((psi[1:]+psi[:-1])/2)*np.diff(s))])
    return s,k,psi,x
def solve(R, Lr1, Lr2, Ln=0.0, g=0.4e-3):
    def F(v):
        Lb2,Rn=abs(v[0]),abs(v[1]); s,k,psi,x=half(R,Rn,Lr1,Lr2,Lb2,Ln); return [psi[-1]-math.pi/2,(x[-1]-g/2)/R]
    for gs in [(R*a,R*b) for a in (0.3,0.6,1.0,1.5,2.0) for b in (1.0,1.6,2.5,4.0,6.0)]:
        sol,info,ier,msg=fsolve(F,gs,full_output=True)
        if ier==1 and max(abs(np.array(F(sol))))<1e-7:
            Lb2,Rn=abs(sol[0]),abs(sol[1]); s,k,psi,x=half(R,Rn,Lr1,Lr2,Lb2,Ln)
            return dict(Lb2=Lb2,Rn=Rn,half=s[-1],zone=2*s[-1],width=2*x.max(),
                        s=np.concatenate([-s[::-1],s[1:]]),k=np.concatenate([k[::-1],k[1:]]))
    return None
def run(tp,R,geo,phis,phig,T,tg=20e-6,margin=3e-3):
    Dt,Dg,Dp,Da,zt=shares(tp,tg)
    eff=(Dp*phis[0]+Da*phis[1]+Dg*phig)/Dt
    return open_shape(eff*geo["k"],geo["s"],geo["half"]+margin,T,Dt,N=8001)
if __name__=="__main__":
    tp,R=30e-6,5.5e-3; Dt,Dg,Dp,Da,zt=shares(tp)
    print(f"Baseline: 20 UTG/3/30 panel/3/20 UTG = {zt*1e6:.0f} um, R={R*1e3} mm -> bulb glass stress {72e9*zt/2/R/1e6:.0f} MPa")
    designs=[(0,0,7e-3),(5e-3,5e-3,0),(10e-3,10e-3,0),(15e-3,15e-3,0),(20e-3,20e-3,0),(20e-3,30e-3,0)]
    cases=[((0.05,0.02),0),((0.2,0.1),0),((0.2,0.1),1e-3),((0.2,0.1),3e-3),((0.5,0.3),0),((0.5,0.3),3e-3)]
    for Lr1,Lr2,Ln in designs:
        g=solve(R,max(Lr1,1e-6),max(Lr2,1e-6),Ln)
        if g is None: print(f"\nramps {Lr1*1e3:.0f}/{Lr2*1e3:.0f} mm: no closed fold"); continue
        print(f"\nramps {Lr1*1e3:.0f}/{Lr2*1e3:.0f} mm, neck plateau {Ln*1e3:.0f} mm: Rn={g['Rn']*1e3:.1f} mm (user-face neck stress {72e9*zt/2/g['Rn']/1e6:.0f} MPa), zone {g['zone']*1e3:.0f} mm, bulb width {g['width']*1e3:.1f} mm")
        for phis,phig in cases:
            o=[]
            for T in (0,1000,2000,3000):
                d,sl,cv=run(tp,R,g,phis,phig,T); o.append(f"T={T:4d}: {d*1e6:6.2f} um/{sl*1e3:6.3f} mrad/{2*sl*0.85*ARC:5.0f}\"")
            print(f"  phi {phis[0]:.2f}/{phis[1]:.2f} g {phig:.0e} | "+" | ".join(o))
