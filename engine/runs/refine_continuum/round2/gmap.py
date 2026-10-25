"""Packages per layer (g) for Continuum-B, MTP on: tok/s/MW at tiers, max tok/s/user, pod size."""
import sys
for ctx in (8192, 131072, 1048576):
    sys.argv = ['x', str(ctx), '1']
    import importlib, model2 as m; importlib.reload(m)
    B = dict(m.CONT, F4=32e15, F8=16e15, P=2450)
    R = m.best(m.gpu_points(m.SYS['Rubin NVL72'], 8e-6))
    for tau in (5e-6, 8e-6):
        for g in (2, 3, 4):
            pts = m.pipe_points(B, tau, gmin=g)
            b = m.best(pts)
            cells = " ".join(f"{x[1]/1e6:5.1f}({x[1]/r[1]:.2f})" if x and r else (f"{x[1]/1e6:5.1f}(inf) " if x else "   --       ") for x, r in zip(b, R))
            print(f"ctx {ctx:>7} tau {tau*1e6:.0f} g={g} pkgs {61*g+1:>3} kW {(61*g+1+5)*2.45:4.0f}: {cells}  max {max(p[0] for p in pts):,.0f}")
