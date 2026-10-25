"""Critic3 adjusted base: +130 W switch plane (oversell fix) with leakage at Rubin's W/mm2 and HBM4 at 50 W/stack (undersell fixes);
omega chosen per tier from {0.5, 0.6, 0.7} (runtime clock). Also: zero-skip Continuum-only on top of the adjusted base, and
activity-proportional W-tier dynamic power (x0.62)."""
import sys
sys.path.insert(0, "/home/user/SomeRepository/engine/runs/refine_continuum_d/round3")
from multiprocessing import Pool
import model10 as c
q, e8 = c.q, c.e8
ADJ = dict(parts_over={"fixed": 240 / 110, "leak_w": 0.56})
CASES = {"switch only (+130 W)": dict(parts_over={"fixed": 240 / 110}),
         "adjusted (switch+leak parity+HBM 50 W)": dict(ADJ, _stack=50.0),
         "adjusted + zero-skip lost (Continuum only)": dict(ADJ, _stack=50.0, base_over={"s": 1 / 1.43}),
         "adjusted + activity W-tier (x0.62)": dict(ADJ, _stack=50.0, wt_dyn=0.62)}
def run(a):
    name, ctx, om = a; kw = dict(CASES[name]); e8.STACK_W = kw.pop("_stack", 80.0)
    return name, ctx, om, c.env(ctx, omega=om, lanes=72, **kw)
if __name__ == "__main__":
    jobs = [(n, x, om) for n in CASES for x in (q.C128, q.C1M) for om in (0.5, 0.6, 0.7)]
    R = {x: e8.gpu_env(e8.rubin_prof(150), x) for x in (q.C128, q.C1M)}; U = {x: e8.gpu_env(e8.ultra4_prof(150), x) for x in (q.C128, q.C1M)}
    best = {}
    with Pool(3) as p:
        for name, ctx, om, A in p.imap(run, jobs):
            print(f"{ctx//1024:>5}K {name:<44} omega {om}: {e8.fmt(A)} /Rubin {e8.rat(A, R[ctx])} /Ultra4 {e8.rat(A, U[ctx])}", flush=True)
            b = best.setdefault((name, ctx), {})
            for t in q.T:
                if t in A and (t not in b or A[t][0] > b[t][0]): b[t] = A[t]
    for (name, ctx), b in best.items():
        print(f"BEST-OMEGA {ctx//1024:>5}K {name:<44} {e8.fmt(b)} /Rubin {e8.rat(b, R[ctx])} /Ultra4 {e8.rat(b, U[ctx])}", flush=True)
