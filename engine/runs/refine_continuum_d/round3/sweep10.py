"""Continuum-10 lane sweep (pair layout allowed, HO = 8) at 128K and 1M. Usage: python3 sweep10.py > sweep10.txt"""
from multiprocessing import Pool
import model10 as c
q, e8 = c.q, c.e8
def run(a):
    ctx, l, om = a
    A = c.env(ctx, lanes=l, omega=om); R = e8.gpu_env(e8.rubin_prof(150), ctx); U = e8.gpu_env(e8.ultra4_prof(150), ctx)
    return (f"{ctx//1024:>5}K lanes {l} omega {om}: C10 {e8.fmt(A)} | /Rubin {e8.rat(A, R)} | /Ultra4 {e8.rat(A, U)}\n"
            + "".join(f"     >={t} {c.detail(A[t][1])}\n" for t in (200, 1000, 2000)))
if __name__ == "__main__":
    jobs = [(q.C128, l, 0.7) for l in (56, 64, 72, 80)] + [(q.C128, 64, 1.0), (q.C128, 72, 0.6)] + [(q.C1M, l, 1.0) for l in (64, 72)]
    with Pool(4) as p:
        for s in p.imap(run, jobs): print(s, flush=True)
