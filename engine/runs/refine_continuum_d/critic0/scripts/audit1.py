"""Critic audit 1: decisive-number checks on round-7 model (imports round7/model7 unchanged)."""
import sys, math, itertools
R7 = "/home/user/SomeRepository/engine/runs/refine_continuum/round7"
sys.path[:0] = [R7, R7 + "/../round6"]
import model7 as q, model5 as m, run7 as r7
C = q.C128
def c7(parts=None, base=None, ctx=C, gs=(1,2,3,4,6), **kw):
    return q.pipe_env(q.cont_prof(base or q.C7T, parts or q.C7T_PARTS), ctx, gs=gs, **kw)
def rub(ctx=C, prof=None): return q.gpu_env(prof or q.RUBIN_PROF(), ctx)
A, R = c7(), rub()
print("base C7/Rubin", q.ratio(A, R))

# 1. KV per request, users, HBM capacity
print(f"kv_store 128K = {m.kv_store(m.V4, C)/1e9:.3f} GB/user ; 1M = {m.kv_store(m.V4, q.C1M)/1e9:.3f} GB")

# 2. per-GB HBM rather than per-stack
for t in (200, 1000, 2000):
    v, lab, pt = A[t]; v2, lab2, _ = R[t]
    Pc = [x for a, x, f in q.cont_prof(q.C7T, q.C7T_PARTS) if a == lab.split(" g")[0]][0]["P"]
    Pr = [x for a, x, f in q.RUBIN_PROF() if a == lab2][0]["P"]
    print(f">={t}: per stack {v*Pc/4/(v2*Pr/8):.2f}x ; per GB HBM {v*Pc/192/(v2*Pr/288):.2f}x")

# 3. imbalance parity (hot-expert replication with 87% SRAM free at g=6)
print("C7 imb 1.07  ", q.ratio(c7(base=dict(q.C7T, imb=1.07)), R))

# 4. Rubin with host/NIC/switch overhead trimmed like C7 (subtract X W from every Rubin profile slot)
for X in (150, 250, 350):
    prof = [(a, dict(s, P=s["P"] - X), f) for a, s, f in q.RUBIN_PROF()]
    print(f"Rubin slot -{X} W     ", q.ratio(A, rub(prof=prof)))

# 5. adverse pairs on Continuum (claim: >=1000 survives pairs)
adv = {"node": dict(parts=dict(q.C7T_PARTS, comp_w=3300)),
       "eta.5": dict(base=dict(q.C7T, F4=q.C7T['F4']*5/6, F8=q.C7T['F8']*5/6)),
       "leak2": dict(parts=dict(q.C7T_PARTS, leak_w=1000)),
       "wt.30": dict(parts=dict(q.C7T_PARTS, wt_w=1228)),
       "imb1.25": dict(base=dict(q.C7T, imb=1.25))}
def merge(a, b):
    base = dict(q.C7T); parts = dict(q.C7T_PARTS)
    for d in (a, b):
        if "base" in d:
            for k in ("F4", "F8", "imb"):
                if d["base"][k] != q.C7T[k]: base[k] = d["base"][k]
        if "parts" in d:
            for k, v in d["parts"].items():
                if v != q.C7T_PARTS[k]: parts[k] = v
    return base, parts
for (n1, d1), (n2, d2) in itertools.combinations(adv.items(), 2):
    b, p = merge(d1, d2)
    print(f"pair {n1:>7}+{n2:<8}", q.ratio(c7(parts=p, base=b), R))
b, p = merge(adv["node"], adv["eta.5"]); b2, p2 = merge((dict(base=b, parts=p)), adv["leak2"])
print("triple node+eta.5+leak2   ", q.ratio(c7(parts=p2, base=b2), R))
