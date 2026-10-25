"""Sensitivity of Continuum vs Rubin (tau 15us) at 128K context, tok/s per provisioned MW."""
import copy, model as m

def row(tag, s, tau=3e-6):
    b = m.best(m.pipe_points(s, tau))
    r = m.best(m.gpu_points(m.GPU["Rubin NVL72"], 15e-6))
    cells = []
    for x, y in zip(b, r):
        if x is None: cells.append(f"{'--':>12}")
        elif y is None: cells.append(f"{x[1]/1e6:6.1f}M/inf ")
        else: cells.append(f"{x[1]/1e6:6.1f}M/{x[1]/y[1]:3.1f}x")
    print(f"{tag:<40}" + "".join(cells))

print(f"{'variant':<40}" + "".join(f"{t:>12}" for t in m.TIERS))
base = copy.deepcopy(m.CONT)
row("base (24PF, 9.2GB, 256TB/s, 4xHBM4, 2.1kW)", base)
for tau in (2e-6, 5e-6, 8e-6, 12e-6, 20e-6):
    row(f"tau {tau*1e6:.0f} us", base, tau)
s = dict(base, hbm=216, hbmbw=15e12, P=2250); row("6 HBM4 stacks (216GB, 15TB/s, 2.25kW)", s)
s = dict(base, hbm=72, hbmbw=5e12, P=1950); row("2 HBM4 stacks (72GB, 5TB/s, 1.95kW)", s)
s = dict(base, srambw=128e12); row("SRAM bw 128 TB/s", s)
s = dict(base, F4=32e15, F8=16e15, P=2400); row("32 PF FP4, 2.4kW", s)
s = dict(base, F4=16e15, F8=8e15, P=1800); row("16 PF FP4, 1.8kW", s)
s = dict(base, P=2600); row("power 2.6 kW/pkg (+25%)", s)
s = dict(base, sram=6.9); row("SRAM 6.9 GB (3 of 4 tiers good / -25%)", s)
m.N_EXP = 768; m.W_TOTAL *= 2
row("model 2x experts (3.2T params)", base)
