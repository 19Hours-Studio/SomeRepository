"""Worst pairs for Continuum-8 (round-1 design: TP split, omega 1, no separate SRAM static, g <= 14), to compare with the
check's 'worst untested pair'. Usage: python3 c8pairs.py > c8pairs.txt"""
from multiprocessing import Pool
import model9 as e9
q, e8 = e9.q, e9.e8
C8 = dict(split="tp", gmax=14, s_static=0, omega=1.0, lanes=64)
P = {"eta 0.5 + leakage x2": dict(base_over={"F4": 5/6, "F8": 5/6}, parts_over={"leak_w": 2.0}),
     "eta 0.5 + tile imb 1.25": dict(base_over={"F4": 5/6, "F8": 5/6}, imb_fixed=1.25),
     "leakage x2 + tile imb 1.25": dict(parts_over={"leak_w": 2.0}, imb_fixed=1.25),
     "W-tier 0.30 + leakage x2": dict(wt_dyn=2.0, parts_over={"leak_w": 2.0}),
     "same node + W-tier 0.30": dict(wt_dyn=2.0, parts_over={"comp_w": 1.25})}
def run(a):
    n, kw = a
    A = e9.env(q.C128, **{**C8, **kw}); R = e8.gpu_env(e8.rubin_prof(150), q.C128)
    return f"C8 {n:<32}{e8.rat(A, R)}"
if __name__ == "__main__":
    with Pool(4) as p:
        for s in p.imap(run, P.items()): print(s, flush=True)
