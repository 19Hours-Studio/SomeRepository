# Summarise spliceq*.jsonl: per variant, KL to exact recompute of the same prompt, top-1 agreement,
# and NLL of the agent's real next action; the clearing effect itself (append-only vs sliding);
# the bf16 chunking floor. 95% CIs by bootstrap over traces.
# Usage: python3 -I analyze.py spliceq_s0.jsonl [spliceq_s1.jsonl ...]
import sys, json, random, statistics as st
R = [json.loads(l) for p in sys.argv[1:] for l in open(p)]
ids = sorted({r["id"] for r in R}); V = [k for k in ("S0", "SG", "S16", "S128") if k in R[0]]
def boot(f, n=2000):
    rnd = random.Random(0); xs = []
    for _ in range(n):
        s = [r for t in (rnd.choice(ids) for _ in ids) for r in R if r["id"] == t]
        xs.append(f(s))
    xs.sort(); return xs[int(0.025 * n)], xs[int(0.975 * n)]
def m(rs, g): return st.mean(g(r) for r in rs)
print(f"traces={len(ids)}  eval points={len(R)}  sliding prompt mean={m(R, lambda r: r['sliding_len']):,.0f} tok  "
      f"append prompt mean={m(R, lambda r: r['append_len']):,.0f} tok  cleared observations per point mean={m(R, lambda r: r['n_cleared']):.1f}")
fl = [r["floor"] for r in R if "floor" in r]
print(f"bf16 floor (same exact prompt, 2-chunk vs 1-chunk prefill; n={len(fl)}): KL={st.mean(x['kl'] for x in fl):.4f}  top1={st.mean(x['top1'] for x in fl):.3f}")
print(f"\n{'variant (vs exact sliding prompt)':38s} {'mean KL':>8s} {'95% CI':>17s} {'median':>7s} {'top-1':>6s} {'dNLL act':>9s} {'95% CI':>17s}")
rows = [("clearing itself: append-only prompt", "app")] + [(f"splice {v}", v) for v in V]
for name, k in rows:
    kl = lambda rs, k=k: m(rs, lambda r: r[k]["kl"]); dn = lambda rs, k=k: m(rs, lambda r: r[k]["nll"] - r["ref"]["nll"])
    a, b = boot(kl); c, d = boot(dn)
    print(f"{name:38s} {kl(R):8.4f} [{a:.4f},{b:.4f}] {st.median(r[k]['kl'] for r in R):7.4f} {m(R, lambda r: r[k]['top1']):6.3f} "
          f"{dn(R):+9.4f} [{c:+.4f},{d:+.4f}]")
print("\nKL vs number of accumulated splices (S0 / S128 / clearing effect):")
for lo, hi in ((1, 2), (3, 4), (5, 8), (9, 99)):
    rs = [r for r in R if lo <= r["n_cleared"] <= hi]
    if rs: print(f"  {lo}-{hi:<3d} n={len(rs):3d}  S0={m(rs, lambda r: r['S0']['kl']):.4f}  S128={m(rs, lambda r: r['S128']['kl']):.4f}  app={m(rs, lambda r: r['app']['kl']):.4f}")
print("\nratio splice-error / clearing-effect (mean KL):", {v: round(m(R, lambda r: r[v]['kl']) / m(R, lambda r: r['app']['kl']), 3) for v in V})
print("distance to the full-context (append-only) answer, mean KL(app || x): exact sliding",
      round(m(R, lambda r: r['ref_vs_app']['kl']), 4), {v: round(m(R, lambda r: r[v]['kl_vs_app']), 4) for v in V})
print("NLL of real action (nats/token): exact sliding", round(m(R, lambda r: r['ref']['nll']), 4), " append-only", round(m(R, lambda r: r['app']['nll']), 4))
print("extra tokens recomputed by repair, per eval point (S128-S0 work):", round(m(R, lambda r: r['S128']['work'] - r['S0']['work']), 1),
      " vs exact-rewrite suffix work not tracked here (see ownstack.out)")
