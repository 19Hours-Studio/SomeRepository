"""Critic: Continuum-9 with mHC hand-off HO=8 (4 streams BF16), lanes re-optimised; vs Rubin and same-date Ultra; worst pairs."""
from multiprocessing import Pool
import handoff as H
e9, e8, q = H.e9, H.e8, H.q
def run(a):
    name, ctx, kw = a; H.HO = 1.0 if name.startswith("HO1") else 8.0
    kw = dict(kw); ep = kw.pop("_ep", None); e9.IMB_EP = ep
    A = e9.env(ctx, **{**e9.BASE, **kw})
    R = e8.gpu_env(e8.rubin_prof(150), ctx); U = e8.gpu_env(e8.ultra4_prof(150), ctx)
    return f"{ctx//1024:>5}K {name:<44} C9 {e8.fmt(A)} | /Rubin {e8.rat(A, R)} | /Ultra4 {e8.rat(A, U)}"
L = lambda n: dict(lanes=n)
jobs = [(f"HO8 lanes {n}", q.C128, L(n)) for n in (72, 80, 88, 96)]
jobs += [("HO8 lanes 96 eta0.5+leak x2", q.C128, dict(lanes=96, base_over={"F4": 5/6, "F8": 5/6}, parts_over={"leak_w": 2.0})),
         ("HO8 lanes 96 eta0.5+imb1.25", q.C128, dict(lanes=96, base_over={"F4": 5/6, "F8": 5/6}, imb_fixed=1.25)),
         ("HO8 lanes 96 leak x2+imb1.25", q.C128, dict(lanes=96, parts_over={"leak_w": 2.0}, imb_fixed=1.25)),
         ("HO8 lanes 96 EP imb 1.15", q.C128, dict(lanes=96, _ep=1.15)),
         ("HO8 lanes 96 omega 1 (1M)", q.C1M, dict(lanes=96, omega=1.0)),
         ("HO1 lanes 64 omega 1 (1M, answer)", q.C1M, dict(omega=1.0))]
if __name__ == "__main__":
    with Pool(4) as p:
        for s in p.imap(run, jobs): print(s, flush=True)
