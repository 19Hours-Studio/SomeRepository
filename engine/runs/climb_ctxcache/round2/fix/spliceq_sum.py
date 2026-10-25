# Summarise spliceq.py output: per mode, mean over eval points of KL(full||mode), top-1 agreement and
# delta-NLL of the real next message, with a 95% bootstrap CI over traces; and by number of accumulated splices.
# Usage: python3 -I spliceq_sum.py out/spliceq.*.jsonl
import sys, json, random, statistics as st
rows = [json.loads(l) for f in sys.argv[1:] for l in open(f) if l.startswith("{")]
ids = sorted({r["id"] for r in rows}); modes = ["splice", "noshift", "keep+1", "noise"]
print(f"traces={len(ids)} eval points={len(rows)} mean ctx={st.mean(r['ctx'] for r in rows):,.0f} tokens "
      f"mean scored tokens/point={st.mean(r['tgt'] for r in rows):.0f} mean splices so far={st.mean(r['clears'] for r in rows):.1f} "
      f"max splices={max(r['clears'] for r in rows)}")
rng = random.Random(0); by = {i: [r for r in rows if r["id"] == i] for i in ids}
def ci(mode, met):
    v = []
    for _ in range(2000):
        pts = [r for i in (rng.choice(ids) for _ in ids) for r in by[i]]
        v.append(st.mean(r[mode][met] for r in pts))
    v.sort(); return v[50], v[1949]
print(f"\n{'mode':8s} {'KL nats/tok':>12s} {'95% CI':>20s} {'median':>8s} {'top-1 agree':>11s} {'dNLL':>8s} {'95% CI':>18s}")
for m in modes:
    if m == "noise":
        z = [r[m] for r in rows if m in r]
        print(f"noise    max |KL| {max(abs(x['kl']) for x in z):.1e}, min top-1 {min(x['top1'] for x in z):.4f}, max |dNLL| {max(abs(x['dnll']) for x in z):.1e} over {len(z)} points"); continue
    kl = [r[m]["kl"] for r in rows]; a, b = ci(m, "kl"); c, d = ci(m, "dnll")
    print(f"{m:8s} {st.mean(kl):12.5f} {a:9.5f}..{b:9.5f} {st.median(kl):8.5f} {st.mean(r[m]['top1'] for r in rows):11.4f} "
          f"{st.mean(r[m]['dnll'] for r in rows):+8.4f} {c:+8.4f}..{d:+8.4f}")
w = sum(r["splice"]["kl"] < r["keep+1"]["kl"] for r in rows)
print(f"\nsplice KL below keep+1 KL at {w}/{len(rows)} eval points; mean ratio splice/keep+1 = "
      f"{st.mean(r['splice']['kl'] for r in rows)/st.mean(r['keep+1']['kl'] for r in rows):.2f}")
print("\nby accumulated splices (splice mode):")
for lo, hi in ((1, 2), (3, 5), (6, 10), (11, 99)):
    g = [r for r in rows if lo <= r["clears"] <= hi]
    if g: print(f"  {lo:2d}-{hi:2d}: n={len(g):3d}  KL={st.mean(r['splice']['kl'] for r in g):.5f}  noshift KL={st.mean(r['noshift']['kl'] for r in g):.5f}"
                f"  keep+1 KL={st.mean(r['keep+1']['kl'] for r in g):.5f}  top1={st.mean(r['splice']['top1'] for r in g):.4f}  dNLL={st.mean(r['splice']['dnll'] for r in g):+.4f}")
