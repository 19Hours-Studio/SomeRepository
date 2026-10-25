"""Critic: does a shorter fixed per-layer latency (static point-to-point fabric) buy anything? HO=8, 88 lanes."""
from multiprocessing import Pool
import handoff as H
e9, e8, q = H.e9, H.e8, H.q
def run(c):
    H.HO = 8.0
    A = e9.env(q.C128, **dict(e9.BASE, lanes=88), tau_fn=lambda f, c=c: (c + 3 / f) * 1e-6)
    R = e8.gpu_env(e8.rubin_prof(150), q.C128)
    return f"collectives {c} us (Continuum only), HO8, 88 lanes: /Rubin {e8.rat(A, R)}"
if __name__ == "__main__":
    with Pool(3) as p:
        for s in p.imap(run, (7, 4, 2)): print(s, flush=True)
