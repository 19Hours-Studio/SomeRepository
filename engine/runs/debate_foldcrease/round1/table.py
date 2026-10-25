"""Honest-gain table: same set assumptions, sandwich (this round) vs critic's coupled model of round-0 Idea 1."""
import sys,math; sys.path.insert(0,'.')
from sandwich import stack,teardrop,depth
import critic_oca_coupled2 as C
D,zt,zna=stack(); Dt=sum(d for _,d,*_ in D)
shp=sum(d for n,d,*_ in D if n=="panel")/Dt; sha=sum(d for n,d,*_ in D if n=="adh")/Dt
for R,Rn in ((5e-3,8e-3),(4e-3,6e-3)):
    s,k,al,Lz=teardrop(R,Rn)
    print(f"\nSandwich 20/3/22/3/20, R={R*1e3:.0f} Rn={Rn*1e3:.0f} (zone {Lz*1e3:.0f} mm, clamp margin 3 mm)")
    for pp,pa in ((0.05,0.02),(0.10,0.05),(0.20,0.10),(0.50,0.30)):
        row=[]
        for T in (0,500,1000):
            d,sl=depth((shp*pp+sha*pa)*k,s,Lz/2+3e-3,T=T,Dt=Dt); row.append(f"T={T:4d}: {d*1e6:6.2f} um/{sl*1e3:5.2f} mrad")
        print(f"  phi_panel {pp:.2f} phi_adh {pa:.2f} | "+" | ".join(row))
print("\nRound-0 Idea 1 (critic coupled model, soft OCA, bonded Ti), R=4 mm")
for G,phi in ((1e4,0.05),(1e5,0.05),(1e4,0.10),(1e5,0.10)):
    print(f"  G={G:.0e} phi={phi:.2f} | "+" | ".join(f"T={T:4d}: {C.solve(G=G,phi=phi,T=T)['depth']*1e6:6.2f} um" for T in (0,500,1000)))
