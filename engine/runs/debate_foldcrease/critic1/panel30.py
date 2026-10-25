"""Sandwich with 30 um panel at R for 490 MPa glass stress, T=1000, low and mid set, step and 5 mm ramp."""
import sys, numpy as np; sys.path.insert(0,'../round1')
from sandwich import stack, teardrop, depth, E_g
D,zt,_=stack(tp=30e-6); Dt=sum(d for _,d,*_ in D)
Dp=sum(d for n,d,*_ in D if n=="panel"); Da=sum(d for n,d,*_ in D if n=="adh")
R=E_g*zt/2/490e6; s,k,_,Lz=teardrop(R,1.6*R); a=Lz/2+3e-3
n=int(5e-3/(s[1]-s[0])); kr=np.convolve(k,np.ones(n)/n,mode='same')
for pp,pa in ((0.05,0.02),(0.2,0.1)):
    eff=(pp*Dp+pa*Da)/Dt
    for nm,kk in (("step",k),("5mm ramp",kr)):
        d,sl=depth(eff*kk,s,a,T=1000,Dt=Dt); print(f"tp=30 R={R*1e3:.2f} phi {pp}/{pa} {nm}: {d*1e6:.2f} um / {sl*1e3:.3f} mrad")
