# Summarise splicelong.py: by accumulated splices; splice vs full-recompute, and both vs append-only.
import sys, json, statistics as st, random
rows = [json.loads(l) for f in sys.argv[1:] for l in open(f) if l.startswith("{")]
ids = sorted({r["id"] for r in rows}); by = {i: [r for r in rows if r["id"] == i] for i in ids}
print(f"traces={len(ids)} points={len(rows)} mean ctx={st.mean(r['ctx'] for r in rows):.0f} max splices={max(r['clears'] for r in rows)}")
def ci(f, sel):
    rng = random.Random(0); v = []
    for _ in range(2000):
        p = [r for i in (rng.choice(ids) for _ in ids) for r in by[i] if sel(r)]
        if p: v.append(st.mean(f(r) for r in p))
    v.sort(); return v[int(.025*len(v))], v[int(.975*len(v))]
for lo, hi in ((1, 4), (5, 12), (13, 20), (21, 99), (1, 99)):
    g = [r for r in rows if lo <= r["clears"] <= hi]
    if not g: continue
    ga = [r for r in g if "s_vs_app" in r]
    sel = lambda r, lo=lo, hi=hi: lo <= r["clears"] <= hi
    a, b = ci(lambda r: r["s_vs_full"]["kl"], sel)
    s = (f"splices {lo:2d}-{hi:2d}: n={len(g):3d} KL(full||splice)={st.mean(r['s_vs_full']['kl'] for r in g):.4f} [{a:.4f},{b:.4f}]"
         f" top1={st.mean(r['s_vs_full']['top1'] for r in g):.3f} dNLL(splice-full)={st.mean(r['dnll_s_full'] for r in g):+.4f}")
    if ga:
        s += (f" | n_app={len(ga)} KL(app||splice)={st.mean(r['s_vs_app']['kl'] for r in ga):.4f}"
              f" KL(app||exactclear)={st.mean(r['f_vs_app']['kl'] for r in ga):.4f}"
              f" splice closer at {sum(r['s_vs_app']['kl'] < r['f_vs_app']['kl'] for r in ga)}/{len(ga)}"
              f" dNLL vs app: splice {st.mean(r['dnll_s_app'] for r in ga):+.4f} clear {st.mean(r['dnll_f_app'] for r in ga):+.4f}")
    print(s)
