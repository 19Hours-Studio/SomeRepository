import sys
sys.path.insert(0, "/home/user/SomeRepository/engine/runs/refine_continuum_d/round2")
from multiprocessing import Pool
import model9 as e9
q, e8 = e9.q, e9.e8
C = q.C128
def rub(slot, chip0):
    base = dict(q.RUBIN, P=slot, P_maxq=190e3 / 72)
    return [(l, dict(x, P=x["P"] - 150), f) for l, x, f in q.profiles(base, comp_w=chip0 - 150, leak_w=150, other_w=0, rack_share=0.83)]
def job(a):
    n, slot, chip = a
    A = e9.env(C, **e9.BASE); R = e8.gpu_env(rub(slot, chip), C)
    return n, e8.rat(A, R), e8.fmt(R), {t: (R[t][1]) for t in (200, 1000, 2000)}
if __name__ == "__main__":
    J = [("model as answer (3056 W slot, 1870 W chip)", 220e3/72, 1870),
         ("analyst Max-P (3194 W slot, 2300 W chip)", 230e3/72, 2300),
         ("analyst Max-Q anchor (2639 W slot, 1800 W chip)", 190e3/72, 1800)]
    with Pool(3) as p:
        for n, r, v, lab in p.imap(job, J): print(f"{n:<50} C9/Rubin {r} | Rubin tok/s/W {v} | {lab}", flush=True)
