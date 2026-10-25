"""Round-1 model: bonded neutral-plane sandwich (UTG / stiff adhesive / panel / stiff adhesive / UTG).
Perfect bonding (stiff glassy adhesive, shear-lag length checked) -> composite beam, single neutral axis.
Residual curvature = sum(D_i about NA * phi_i)/D_tot * kappa_fold(s) (only viscoelastic layers set).
Fold shape: teardrop = neck arc (Rn, -alpha) + bulb (R, pi+2alpha) + neck arc; flat length = arc length.
Open state: span clamped flat (slope 0) at x=+-a (wings bonded to rigid halves); w''=kres(x)-m(+tension)."""
import numpy as np, math
E_g,E_p,E_a=72e9,6e9,3e9
def stack(tg=20e-6,ta=3e-6,tp=22e-6):
    L=[("UTG top",E_g,tg,0.0),("adh",E_a,ta,None),("panel",E_p,tp,None),("adh",E_a,ta,None),("UTG bot",E_g,tg,0.0)]
    z=0;out=[]
    for n,E,t,ph in L: out.append((n,E,t,z+t/2,ph)); z+=t
    zna=sum(E*t*zc for _,E,t,zc,_ in out)/sum(E*t for _,E,t,_,_ in out)
    D=[(n,E*t**3/12+E*t*(zc-zna)**2,E,t,zc-zna) for n,E,t,zc,_ in out]
    return D,z,zna
def teardrop(R,Rn,g=0.4e-3,n=4000):
    ca=(Rn+g/2)/(R+Rn); al=math.acos(ca)
    Ln=Rn*al; Lb=R*(math.pi+2*al); half=Ln+Lb/2
    s=np.linspace(-half,half,n); k=np.where(np.abs(s)<=Lb/2,1/R,-1/Rn)
    return s,k,al,2*Ln+Lb
def depth(kres,s,a,T=0.0,Dt=1.0,N=3001):
    x=np.linspace(-a,a,N); kr=np.interp(x,s,kres,left=0,right=0); dx=x[1]-x[0]
    if T==0:
        th=np.cumsum(kr-kr.mean())*dx                  # clamped ends: int w'' = 0
    else:  # Euler-Lagrange of int D/2(th'-kr)^2+T/2 th^2: D th''-T th = D kr', th(+-a)=0
        n=N-2; A=np.zeros((n,n)); i=np.arange(n)
        A[i,i]=-2*Dt/dx**2-T; A[i[:-1],i[:-1]+1]=Dt/dx**2; A[i[1:],i[1:]-1]=Dt/dx**2
        rhs=Dt*np.gradient(kr,dx)[1:-1]; th=np.concatenate([[0],np.linalg.solve(A,rhs),[0]])
    w=np.cumsum(th)*dx
    return w.max()-w.min(), np.abs(th).max()
if __name__=="__main__":
    for tg,ta,tp in ((20e-6,3e-6,22e-6),(25e-6,5e-6,25e-6)):
        D,zt,zna=stack(tg,ta,tp); Dt=sum(d for _,d,_,_,_ in D)
        print(f"\n=== sandwich UTG {tg*1e6:.0f}/adh {ta*1e6:.0f}/panel {tp*1e6:.0f}/adh/UTG: total {zt*1e6:.0f} um, D={Dt:.3e} N m (single 70um UTG = {E_g*70e-6**3/12:.3e})")
        c=zt/2
        for R in (4e-3,5e-3,6e-3,8e-3):
            print(f"  R={R*1e3:.0f}mm outer-fibre strain {c/R*100:.2f}%  glass stress {E_g*c/R/1e6:.0f} MPa | panel surface strain {tp/2/R*100:.2f}%  adhesive max strain {(tp/2+ta)/R*100:.2f}%")
        for n,d,E,t,zc in D: print(f"  {n:8s} D-share {d/Dt*100:6.2f}%  centroid offset {zc*1e6:6.1f} um")
    D,zt,zna=stack(); Dt=sum(d for _,d,_,_,_ in D)
    sh={n:0 for n in ("panel","adh")}
    for n,d,*_ in D:
        if n in sh: sh[n]+=d/Dt
    R,Rn=5e-3,8e-3; s,k,al,Lz=teardrop(R,Rn)
    print(f"\nTeardrop R={R*1e3}mm neck Rn={Rn*1e3}mm: alpha={math.degrees(al):.1f} deg, fold-zone length {Lz*1e3:.1f} mm, bulb inner dia {2*R*1e3:.0f} mm")
    print(f"  neck tension on user (top) surface {E_g*zt/2/Rn/1e6:.0f} MPa; bulb tension on protected inner (bottom) surface {E_g*zt/2/R/1e6:.0f} MPa")
    half=Lz/2
    print("\nResidual crease (phi = set fraction of each viscoelastic layer's folded strain)")
    for ph_p,ph_a in ((0.05,0.02),(0.10,0.05),(0.20,0.10),(0.50,0.30)):
        f=sh["panel"]*ph_p+sh["adh"]*ph_a; kres=f*k
        for marg in (0.0,1e-3,3e-3,8e-3):
            d,sl=depth(kres,s,half+marg)
            print(f"  phi_panel={ph_p:.2f} phi_adh={ph_a:.2f} eff={f*100:.3f}% clamp margin {marg*1e3:3.0f}mm: depth {d*1e6:6.3f} um slope {sl*1e3:6.3f} mrad")
    print("\nWith tension (worst row phi 0.5/0.3, margin 3 mm)")
    f=sh["panel"]*0.5+sh["adh"]*0.3
    for T in (0,250,500,1000):
        d,sl=depth(f*k,s,half+3e-3,T=T,Dt=Dt) if T>0 else depth(f*k,s,half+3e-3)
        print(f"  T={T:5d} N/m depth {d*1e6:.3f} um slope {sl*1e3:.3f} mrad")
    # adhesive shear check: transverse shear from moment gradient over neck length
    M=Dt/R; Ln=Rn*al; V=M/Ln
    Q=E_g*20e-6*(zt/2-10e-6)  # E-weighted first moment of one glass about NA
    tau=V*Q/Dt; print(f"\nStiff adhesive: M={M:.3f} N, V~M/Lneck={V:.0f} N/m, interface shear {tau/1e6:.2f} MPa, strain {tau/(E_a/2.6)*100:.2f}% (G~1.15 GPa)")
    k_ad=(E_a/2.6)/3e-6; lam=math.sqrt(E_g*20e-6/k_ad); print(f"  shear-lag length {lam*1e6:.0f} um  -> layers act as one plate beyond ~0.1 mm")
    # tension spring / thermal
    EA=2*E_g*20e-6+E_p*22e-6
    for T in (500,1000):
        print(f"tension {T} N/m: stack strain {T/EA*1e6:.0f} ue, stroke over {Lz*1e3:.0f} mm {T/EA*Lz*1e6:.1f} um, glass stress {T/EA*E_g/1e6:.1f} MPa, force over 150 mm {T*0.15:.0f} N")
    for Lf in (Lz,140e-3):
        mis=(23e-6-8.5e-6)*35*Lf; print(f"Al-vs-glass mismatch over {Lf*1e3:.0f} mm, 35 K: {mis*1e6:.0f} um -> spring rate for +-20% of 75 N: <= {15/(mis*1e3):.0f} N/mm, preload deflection {75/(15/(mis*1e3)):.2f} mm")
