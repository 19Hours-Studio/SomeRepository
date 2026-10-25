"""Round-3 lever scan: unequal ramps (bulb->neck Lr1, neck->flat Lr2), bulb radius R, tension T.
Crease = material-set term only (20/10 polymer set, phi_g 0 / 1e-3 / 3e-3), 30 um panel, 1 min after worst hold."""
import numpy as np, math, sys
sys.dont_write_bytecode=True
from design2 import shares, open_shape
from design3 import solve
tp=30e-6; Dt,Dg,Dp,Da,zt=shares(tp)
def crease(g,phig,T,ps=0.2,pa=0.1,margin=6e-3):
    eff=(Dp*ps+Da*pa+Dg*phig)/Dt
    return open_shape(eff*g["k"],g["s"],g["half"]+margin,T,Dt,N=8001)
if __name__=="__main__":
    print(f"stack {zt*1e6:.0f} um, D={Dt:.3e}")
    for R in (5.5e-3,7e-3):
        for Lr1,Lr2 in ((15e-3,15e-3),(15e-3,5e-3),(20e-3,5e-3),(25e-3,5e-3),(25e-3,8e-3),(30e-3,6e-3)):
            g=solve(R,Lr1,Lr2)
            if g is None: print(f"R{R*1e3} {Lr1*1e3:.0f}/{Lr2*1e3:.0f}: none"); continue
            k1=(1/R+1/g['Rn'])/Lr1; k2=(1/g['Rn'])/Lr2
            o=[]
            for T in (3000,4000):
                for pg in (0,1e-3,3e-3):
                    d,sl,cv=crease(g,pg,T); o.append(f"T{T} g{pg:.0e} {d*1e6:.2f}/{sl*1e3:.4f}")
            print(f"R{R*1e3:.1f} ramps {Lr1*1e3:.0f}/{Lr2*1e3:.0f}: Rn {g['Rn']*1e3:.1f} zone {g['zone']*1e3:.0f} width {g['width']*1e3:.1f} kp1 {k1:.0f} kp2 {k2:.0f} neck-face {72e9*zt/2/g['Rn']/1e6:.0f} MPa | "+" | ".join(o))
