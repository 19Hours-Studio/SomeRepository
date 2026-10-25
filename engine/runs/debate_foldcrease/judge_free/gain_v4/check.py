"""Independent checks on answer.md v4 (floating tensioned display)."""
import math, sys
sys.path.insert(0, "../../round4"); sys.dont_write_bytecode = True
import numpy as np
from design2 import shares
from float4 import crease
Dt, Dg, Dp, Da, zt = shares(30e-6)
print(f"D {Dt:.3e}; glass {Dg/Dt:.4f} panel {Dp/Dt:.4f} adh {Da/Dt:.4f}")
eff0 = (Dp*0.2 + Da*0.1)/Dt
print(f"effective polymer set fraction phi_eff = {eff0:.2e}")
# 1. analytic scaling: theta ~ (D/T) * kappa_r'  over ramp L
R, L2, T = 5.5e-3, 12e-3, 4000
print(f"analytic slope estimate ~ {Dt/T*eff0/(R*L2)*1e3:.4f} mrad (code 0.0066 smooth profile)")
# 2. sensitivity: what dominates? crease vs phi_g, and phi_g needed to reach Duo-new bound 1.75 mrad
for pg in (0, 1e-3, 1e-2, 3e-2, 0.1):
    g, sl, d, *_ = crease(5.5e-3, 28e-3, 12e-3, 4000, pg)
    print(f"  phi_g {pg:.0e}: slope {sl*1e3:.4f} mrad depth {d*1e6:.2f} um")
# 3. tension off (spring failure) -> what is the shape? use tiny T
g, sl, d, *_ = crease(5.5e-3, 28e-3, 12e-3, 1e-3, 1e-3)
print(f"T~0, phi_g 1e-3: slope {sl*1e3:.2f} mrad, depth {d*1e6:.0f} um")
# 4. glass stresses folded at R=5.5 (stack symmetric, neutral plane at mid)
E = 72e9
for z, lab in ((38e-6, "outer face bottom UTG"), (35e-6, "DOL bottom of outer face"), (28e-6, "core of bottom UTG"), (21e-6, "inner DOL edge")):
    print(f"  folded R5.5 bending stress at z={z*1e6:.0f} um ({lab}): {E*z/R/1e6:.0f} MPa")
print(f"  core tension in tensile-side UTG while folded ~ {E*28e-6/R/1e6+150:.0f} MPa (bending + CT 150)")
# critical flaw at that core stress, K_IC 0.75
for s in (244e6, 517e6):
    a = (0.75e6/(1.12*s))**2/math.pi; print(f"  critical flaw at {s/1e6:.0f} MPa: {a*1e6:.2f} um")
# 5. what tension-only buys vs T=0 with same set (ratio)
for pg in (1e-3,):
    _, s0, *_ = crease(5.5e-3, 28e-3, 12e-3, 1e-3, pg); _, s1, *_ = crease(5.5e-3, 28e-3, 12e-3, 4000, pg)
    print(f"  tension gain factor at phi_g {pg}: {s0/s1:.0f}x")
