"""Critic sensitivities not in sens8: worst pairs/triple, W-tier density, imbalance parity, Rubin point detail."""
import sys; sys.path.insert(0, "/home/user/SomeRepository/engine/runs/refine_continuum_d/round1")
import model8 as e8
q, m = e8.q, e8.m
L = ("0.55V wt", "0.60V wt", "0.65V wt", "0.55V", "0.60V")
ctx = int(sys.argv[1]) if len(sys.argv) > 1 else q.C128
def C(base=e8.C8, parts=e8.C8_PARTS, **kw): return e8.c8_env(base, parts, ctx, labels=L, **kw)
R = e8.gpu_env(e8.rubin_prof(150), ctx)
for t in (200, 1000, 2000):
    v = R[t]; print(f"Rubin >={t}: {v[0]:.1f} tok/s/W prof {v[1]} k={v[2][1]} spd={v[2][2]:.0f} B={v[2][3][2]} (t,m)={v[2][3][3]} {dict((a,round(b*1e6,1)) for a,b in v[2][3][4].items() if a!='T')}")
eta5 = dict(e8.C8, F4=e8.C8["F4"] * 5 / 6, F8=e8.C8["F8"] * 5 / 6)
wt30 = dict(e8.C8_PARTS, wt_w=1228)
rows = [("base", C()),
        ("pair W-tier 0.30 + eta 0.5", C(base=eta5, parts=wt30)),
        ("pair W-tier 0.30 + same node", C(parts=dict(wt30, comp_w=3300))),
        ("pair W-tier 0.30 + leakage x2", C(parts=dict(wt30, leak_w=1000))),
        ("triple same node + eta 0.5 + W-tier 0.30", C(base=eta5, parts=dict(wt30, comp_w=3300))),
        ("W-tier 14.7 GB (20 Mb/mm2)", C(base=dict(e8.C8, sram=14.7))),
        ("W-tier 11.8 GB (16 Mb/mm2, V-Cache-class)", C(base=dict(e8.C8, sram=11.8))),
        ("imbalance 1.00 (intermediate split; undersell test)", C(imb_fixed=1.0)),
        ]
print(f"\n{ctx//1024}K  C8 / Rubin trimmed 150 W" + " " * 20 + " ".join(f"{t:>6}" for t in q.T))
for lab, A in rows:
    d = A[1000][1]
    print(f"{lab:<52}" + e8.rat(A, R) + f"   C8 {e8.fmt(A)} | >=1000: npk {d['npk']} C={d['C']} H={d['H']} k{d['k']} b{d['b']}")
