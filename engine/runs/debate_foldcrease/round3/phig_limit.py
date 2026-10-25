"""phi_g that the round-3 nominal hardware tolerates before the worst feature exceeds 0.024 mrad; and phi_g=1e-2 row."""
import sys; sys.dont_write_bytecode=True
from budget3 import budget, base3
from scipy.optimize import brentq
for name,H in (("R3 nominal",base3),("R3 nominal, R=7 35/10, tongue 50",dict(base3,R=7e-3,Lr1=35e-3,Lr2=10e-3,Lt=50e-3))):
    f=lambda pg: budget(dict(H,phig=pg))['total']-0.024e-3
    pg=brentq(f,0,3e-2); o=budget(dict(H,phig=1e-2))
    print(f"{name}: worst feature reaches 0.024 mrad at phi_g = {pg:.2e}; at phi_g 1e-2: interior {o['interior']*1e3:.4f}, clamp {o['clamp']*1e3:.4f} mrad, depth {o['depth']*1e6:.2f} um")
