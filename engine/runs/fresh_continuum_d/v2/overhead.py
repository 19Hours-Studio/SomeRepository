"""Verifier check: how much of Continuum-9's gain comes from its per-slot overhead (fixed) and from the GPU chip/overhead split."""
import sys
sys.path.insert(0, "/home/user/SomeRepository/engine/runs/refine_continuum_d/round2")
from multiprocessing import Pool
import model9 as e9
q, e8 = e9.q, e9.e8
C = q.C128

def rubin_split(chip0):
    # same 220 kW/72 slot, but more of it is chip (voltage-scalable): chip0 = comp + 150 leak
    return [(l, dict(x, P=x["P"] - 150), f) for l, x, f in q.profiles(q.RUBIN, comp_w=chip0 - 150, leak_w=150, other_w=0, rack_share=0.83)]

def ultra_split(extra):
    return q.profiles(dict(q.ultra(5690 - 150), P_maxq=5690 - 150), comp_w=3440 + extra, leak_w=300, other_w=0,
                      rack_share=0.83, vendor_maxq=False)

def job(a):
    name, kind, v = a
    if kind == "cfix":
        A = e9.env(C, **e9.BASE, parts_over={"fixed": (110 + v) / 110})
        return name, e8.rat(A, e8.gpu_env(e8.rubin_prof(150), C)), e8.rat(A, e8.gpu_env(e8.ultra4_prof(150), C)), e8.fmt(A)
    A = e9.env(C, **e9.BASE)
    R = e8.gpu_env(rubin_split(v), C); U = e8.gpu_env(ultra_split(2 * (v - 1870)), C)
    return name, e8.rat(A, R), e8.rat(A, U), e8.fmt(R) + " | U " + e8.fmt(U)

if __name__ == "__main__":
    jobs = [("base", "cfix", 0), ("Continuum +150 W fixed/slot", "cfix", 150), ("Continuum +300 W fixed/slot", "cfix", 300),
            ("Continuum +450 W fixed/slot", "cfix", 450),
            ("GPU chip at V0 = 2,300 W (Max-P TDP), rest fixed", "gsplit", 2300)]
    with Pool(5) as p:
        for n, r, u, v in p.imap(job, jobs):
            print(f"{n:<52} vs Rubin {r} | vs Ultra4 {u} | {v}", flush=True)
