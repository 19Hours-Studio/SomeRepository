"""Critic3: speculative-decoding assumption. Base uses geometric acceptance p=0.8 up to k=6 (GPU envelope allows k=7).
Cases: same k cap 0..6 for both; k<=2 for both (single MTP module chained once); p=0.7 both."""
import sys
sys.path.insert(0, "/home/user/SomeRepository/engine/runs/refine_continuum_d/round3")
from multiprocessing import Pool
import model10 as c
q, e8, m = c.q, c.e8, c.m
_env = m.envelope
def run(a):
    name, ctx, kmax, p = a
    m.envelope = lambda fn, tiers, ks=range(8): _env(fn, tiers, ks=range(kmax + 1))
    A = c.env(ctx, p=p, omega=0.7, lanes=72, ks=range(kmax + 1))
    R = e8.gpu_env(e8.rubin_prof(150), ctx, p=p); U = e8.gpu_env(e8.ultra4_prof(150), ctx, p=p)
    return f"{ctx//1024:>5}K {name:<28} C10 {e8.fmt(A)} | Rubin {e8.fmt(R)} | /Rubin {e8.rat(A, R)} | /Ultra4 {e8.rat(A, U)}"
if __name__ == "__main__":
    jobs = [("k<=6 both, p=0.8", q.C128, 6, 0.8), ("k<=2 both, p=0.8", q.C128, 2, 0.8), ("k<=6 both, p=0.7", q.C128, 6, 0.7),
            ("k<=2 both, p=0.8", q.C1M, 2, 0.8)]
    with Pool(2) as p:
        for s in p.imap(run, jobs): print(s, flush=True)
