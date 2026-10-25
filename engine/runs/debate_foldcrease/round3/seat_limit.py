"""Seat repeatability (1 sigma per contact, 3-sigma used) at which the nominal round-3 clamp line reaches 0.024 mrad;
also with phi_g 1e-3 and with a 50 mm tongue; and bow eccentricity limit."""
import sys; sys.dont_write_bytecode=True
from budget3 import budget, base3
from scipy.optimize import brentq
for name,H in (("nominal",base3),("phi_g 1e-3",dict(base3,phig=1e-3)),("tongue 50 mm",dict(base3,Lt=50e-3))):
    s=brentq(lambda v: budget(dict(H,seat_sigma=v))['total']-0.024e-3,1e-9,2e-6)
    e=brentq(lambda v: budget(dict(H,e=v))['total']-0.024e-3,1e-6,2e-3)
    print(f"{name}: seat sigma limit {s*1e6:.3f} um (3 sigma {3*s*1e6:.2f} um); load-path eccentricity limit {e*1e3:.3f} mm (EI 10, dF 2.5%)")
