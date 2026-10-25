"""Critic3: asymmetric / untested sensitivities on Continuum-10 base (72 lanes, omega 0.7), ratios vs Rubin trimmed 150 W and Ultra4."""
import sys
sys.path.insert(0, "/home/user/SomeRepository/engine/runs/refine_continuum_d/round3")
from multiprocessing import Pool
import model10 as c, model9 as e9
q, e8 = c.q, c.e8
B = dict(omega=0.7, lanes=72)

def rubin(ctx, s=1.43, leak=150, ultra=False):
    if ultra:
        return e8.gpu_env(e8.ultra4_prof(150), ctx) if s == 1.43 else e8.gpu_env([(l, dict(x, s=s), f) for l, x, f in e8.ultra4_prof(150)], ctx)
    old = q.RUBIN_PROF
    q.RUBIN_PROF = lambda: q.profiles(q.RUBIN, comp_w=1720, leak_w=leak, other_w=0, rack_share=0.83)
    try: return e8.gpu_env(e8.rubin_prof(150, s=s), ctx)
    finally: q.RUBIN_PROF = old

CASES = {
 "base": (dict(), dict()),
 "zero-skip 1.0 Continuum only": (dict(base_over={"s": 1 / 1.43}), dict()),
 "zero-skip 1.0 both": (dict(base_over={"s": 1 / 1.43}), dict(s=1.0)),
 "switch plane +130 W/slot (fixed 110->240)": (dict(parts_over={"fixed": 240 / 110}), dict()),
 "Continuum leakage at Rubin W/mm2 (x0.56)": (dict(parts_over={"leak_w": 0.56}), dict()),
 "Rubin leakage at Continuum W/mm2 (150->277 W)": (dict(), dict(leak=277)),
 "SRAM density V-cache-like (18.4->13.5 GB)": (dict(base_over={"sram": 13.5 / 18.4}), dict()),
 "HBM 50 W/stack (Continuum only)": (dict(_stack=50.0), dict()),
 "omega 0.6": (dict(omega=0.6), dict()),
 "omega 0.5": (dict(omega=0.5), dict()),
}

def run(a):
    name, ctx = a
    kw, rk = CASES[name]; kw = dict(B, **kw)
    e8.STACK_W = kw.pop("_stack", 80.0)
    A = c.env(ctx, **kw); R = rubin(ctx, **rk); U = rubin(ctx, s=rk.get("s", 1.43), ultra=True)
    return f"{ctx//1024:>5}K {name:<46} C10 {e8.fmt(A)} | /Rubin {e8.rat(A, R)} | /Ultra4 {e8.rat(A, U)}  [>=1000 {A[1000][1]['npk']} pkgs]"

if __name__ == "__main__":
    jobs = [(n, x) for n in CASES for x in (q.C128, q.C1M)]
    with Pool(2) as p:
        for s in p.imap(run, jobs): print(s, flush=True)
