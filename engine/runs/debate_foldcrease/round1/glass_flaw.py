"""Glass surface flaw check: net stress at flaw depth a = bending(a) - CS*(1-a/DOL) (linear CS profile);
K = 1.12*sigma_net*sqrt(pi a). Report largest K over a in 0.05..10 um; compare K_IC~0.7, fatigue threshold ~0.3 MPa sqrt(m)."""
import numpy as np
E=72e9
def kmax(c,R,CS,DOL):
    a=np.linspace(0.05e-6,10e-6,2000); sb=E*(c-a)/R; cs=np.where(a<DOL,CS*(1-a/DOL),0)
    sn=sb-cs; K=1.12*np.clip(sn,0,None)*np.sqrt(np.pi*a); i=K.argmax(); return K[i]/1e6,a[i]*1e6,sn[i]/1e6
cases=[("sandwich bulb, protected bottom face, R=5",34e-6,5e-3),
       ("sandwich neck, user top face, Rn=8",34e-6,8e-3),
       ("sandwich bulb at R=4",34e-6,4e-3),
       ("single 30um UTG at R=1.5 (shipping-like, radius unverified)",15e-6,1.5e-3),
       ("single 30um UTG at R=2.0",15e-6,2.0e-3)]
for CS,DOL in ((450e6,6e-6),(650e6,4e-6)):
    print(f"\nCS={CS/1e6:.0f} MPa DOL={DOL*1e6:.0f} um")
    for n,c,R in cases:
        K,a,s=kmax(c,R,CS,DOL); print(f"  {n:58s} applied {E*c/R/1e6:4.0f} MPa  worst flaw {a:4.1f} um  net {s:5.0f} MPa  K={K:.2f} MPa√m")
print("\nSmallest surface-flaw depth that reaches K_th=0.3 (slow growth) / K_IC=0.7 (fracture), CT ignored")
def acrit(c,R,CS,DOL,Kt):
    a=np.linspace(0.05e-6,15e-6,6000); sb=E*(c-a)/R; cs=np.where(a<DOL,CS*(1-a/DOL),0)
    K=1.12*np.clip(sb-cs,0,None)*np.sqrt(np.pi*a); j=np.argmax(K>=Kt*1e6); return a[j]*1e6 if K[j]>=Kt*1e6 else float('nan')
for CS,DOL in ((450e6,6e-6),(650e6,4e-6),(800e6,5e-6)):
    print(f" CS={CS/1e6:.0f} DOL={DOL*1e6:.0f}: "+"; ".join(f"{n.split(',')[0][:30]}..{n.split(',')[-1]}: {acrit(c,R,CS,DOL,0.3):.1f}/{acrit(c,R,CS,DOL,0.7):.1f} um" for n,c,R in cases))
