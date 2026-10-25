"""Checks: (1) model10 with HO=1, no pairing reproduces Continuum-9 (59.8); (2) HO=8 no pairing reproduces critic2 (64/88 lanes);
(3) pairing at HO=8 over lanes."""
import sys
from multiprocessing import Pool
import model10 as c
q, e8 = c.q, c.e8
R = None
def run(a):
    name, ho, kw = a; c.HO = ho
    A = c.env(q.C128, **kw); R = e8.gpu_env(e8.rubin_prof(150), q.C128); U = e8.gpu_env(e8.ultra4_prof(150), q.C128)
    return f"{name:<34} {e8.fmt(A)} | /Rubin {e8.rat(A, R)} | /Ultra4 {e8.rat(A, U)}\n     >=1000 {c.detail(A[1000][1])}\n     >=2000 {c.detail(A[2000][1])}"
jobs = [("C9 reproduce HO1 64 lanes", 1, dict(use_pair=False)),
        ("critic HO8 64 lanes", 8, dict(use_pair=False)),
        ("critic HO8 88 lanes", 8, dict(use_pair=False, lanes=88))]
jobs += [(f"PAIR HO8 {l} lanes Gmax28", 8, dict(lanes=l)) for l in (48, 56, 64, 72, 88)]
jobs += [("PAIR HO8 64 lanes Gmax40 gmax20", 8, dict(lanes=64, Gmax=40, gmax=20))]
if __name__ == "__main__":
    with Pool(4) as p:
        for s in p.imap(run, jobs): print(s, flush=True)
