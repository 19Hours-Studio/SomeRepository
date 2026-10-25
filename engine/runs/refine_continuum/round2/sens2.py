"""Continuum design variants vs Rubin, MTP on, 128K (or argv[1]) context. Ratio = Continuum / Rubin(35PF, tau as labelled)."""
import sys
ctx = int(sys.argv[1]) if len(sys.argv) > 1 else 131072
sys.argv = ['x', str(ctx), '1']
import model2 as m
R = m.SYS['Rubin NVL72']; R50 = m.SYS['Rubin (50PF dense)']
refs = {'R15': m.best(m.gpu_points(R, 15e-6)), 'R8': m.best(m.gpu_points(R, 8e-6)), 'R50@8': m.best(m.gpu_points(R50, 8e-6))}
def row(tag, s, tau=5e-6):
    b = m.best(m.pipe_points(s, tau))
    out = f"{tag:<44}"
    for i, x in enumerate(b):
        if x is None: out += f"{'--':>22}"; continue
        rs = "/".join(f"{x[1]/refs[k][i][1]:.2f}" if refs[k][i] else "inf" for k in refs)
        out += f"{x[1]/1e6:6.1f}M {rs:>15}"
    print(out)
print("ratios vs Rubin35@15us / Rubin35@8us / Rubin50dense@8us; tiers", m.TIERS)
base = dict(m.CONT)
row("A: 24PF, 2.1kW, tau5", base)
B = dict(base, F4=32e15, F8=16e15, P=2450)
row("B: 32PF, 2.45kW, tau5", B)
for t in (3e-6, 8e-6, 12e-6, 20e-6): row(f"B tau {t*1e6:.0f}us", B, t)
row("B + 4x48GB HBM4 16-hi (192GB)", dict(B, hbm=192, P=2500))
row("B + 6x36GB (216GB, 15TB/s)", dict(B, hbm=216, hbmbw=15e12, P=2650))
row("B, SRAM bw 128 TB/s", dict(B, srambw=128e12))
row("B, SRAM bw 512 TB/s (+300W)", dict(B, srambw=512e12, P=2750))
row("B, slot power 3.0 kW (+22%)", dict(B, P=3000))
row("B, compute eff 0.45 (vs 0.6 for GPUs)", dict(B, F4=24e15, F8=12e15))
row("B, 3 of 4 tiers good (6.9GB)", dict(B, sram=6.9))
