"""Fine interactivity sweep, 128K, MTP on: crossover tiers; tokens/s per HBM stack."""
import sys; sys.argv = ['x', '131072', '1']
import model2 as m
m.TIERS = (100, 300, 500, 600, 700, 800, 1000, 1500, 2000, 3000)
C = dict(m.CONT, F4=32e15, F8=16e15, P=2450)
rows = [("Rubin tau15", m.gpu_points(m.SYS['Rubin NVL72'], 15e-6), 8, 220e3/72),
        ("Rubin tau8", m.gpu_points(m.SYS['Rubin NVL72'], 8e-6), 8, 220e3/72),
        ("Rubin50 tau8", m.gpu_points(m.SYS['Rubin (50PF dense)'], 8e-6), 8, 220e3/72),
        ("MI455X tau8", m.gpu_points(m.SYS['MI455X x72'], 8e-6), 12, 230e3/72),
        ("LPX+Rubin tau4", m.afd_points(4e-6), None, None),
        ("CS-4 tau3", m.pipe_points(m.WSE, 3e-6, True), None, None),
        ("Cont g3 tau8", m.pipe_points(C, 8e-6, gmin=3), 4, 2450),
        ("Cont g3 tau5", m.pipe_points(C, 5e-6, gmin=3), 4, 2450)]
print(f"{'system':<16}" + "".join(f"{t:>7}" for t in m.TIERS))
for n, pts, st, P in rows:
    print(f"{n:<16}" + "".join(f"{x[1]/1e6:7.1f}" if x else f"{'--':>7}" for x in m.best(pts)))
print("\noutput tok/s per HBM stack (k) at tiers")
for n, pts, st, P in rows:
    if st: print(f"{n:<16}" + "".join(f"{x[1]*P/1e6/st/1e3:7.1f}" if x else f"{'--':>7}" for x in m.best(pts)))
