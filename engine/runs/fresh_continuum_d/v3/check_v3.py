"""Independent perturbations of Continuum-10 (model10) vs Rubin, 128K, at the answer's base design (omega 0.7, 72 lanes).
Cases: base; Continuum-only zero-skip s=1 (Rubin keeps vendor 50 PF); CSA KV-read union for draft positions
(each query position picks its own top-1024; extra positions add a fraction u of new entries), applied to BOTH systems."""
import sys, time
sys.path.insert(0, "/home/user/SomeRepository/engine/runs/refine_continuum_d/round3")
from multiprocessing import Pool
import model10 as c
q, e8, m = c.q, c.e8, c.m
POS = [1]
_spec = m.spec
def spec(M, k, p):
    r = _spec(M, k, p); POS[0] = r[0]; return r
m.spec = spec
U = [0.0]
_kvread = m.kv_read
def kv_read(M, L):
    E = m.entry()
    return _kvread(M, L) + U[0] * (POS[0] - 1) * m.N_CSA * m.TOPK_ATT * E
m.kv_read = kv_read
_terms = c._terms
def terms(s, typ, g, h, b, pos, imb, idx_sram, kv_sram, L):
    if typ["idxs"] and U[0]:
        typ = dict(typ, kvr=typ["kvr"] + U[0] * (pos - 1) * m.TOPK_ATT * m.entry())
    return _terms(s, typ, g, h, b, pos, imb, idx_sram, kv_sram, L)
c._terms = terms

def run(a):
    name, u, kw = a; U[0] = u
    t0 = time.time()
    A = c.env(q.C128, omega=0.7, lanes=72, **kw)
    R = e8.gpu_env(e8.rubin_prof(150), q.C128)
    return f"{name:<44} C {e8.fmt(A)} | Rubin {e8.fmt(R)} | ratio {e8.rat(A, R)}  ({time.time()-t0:.0f}s)\n   >=1000 {c.detail(A[1000][1])}"
jobs = [("base", 0.0, {}),
        ("Continuum zero-skip s=1 only", 0.0, dict(base_over={"s": 1 / 1.43})),
        ("CSA KV union u=0.5, both", 0.5, {}),
        ("CSA KV union u=1.0, both", 1.0, {}),
        ("s=1 Continuum + same node + u=0.5", 0.5, dict(base_over={"s": 1 / 1.43}, parts_over={"comp_w": 1.25}))]
if __name__ == "__main__":
    with Pool(5) as p:
        for s in p.imap(run, jobs): print(s, flush=True)
