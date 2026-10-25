# Robustness of replay.py results (Anthropic 5-min prices): per-trace spread, bootstrap CI over traces,
# placeholder/back-reference size, minimum run length, and the largest raw prompt (context-window check).
import os, sys, random, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import replay as rp
T = rp.T
def tot(pol, d, ts=T): return [rp.run(t, pol, d)["cost"] for t in ts]
raw, roll = tot("raw", False), tot("roll", False)
bd, bm, rd = tot("batch", True), tot("batch", False), tot("raw", True)
per = [1 - b / r for b, r in zip(bd, raw)]
print(f"batch+delta vs raw per trace: median {st.median(per):+.1%}, worse than raw on {sum(p < 0 for p in per)}/{len(per)} traces, "
      f"min {min(per):+.1%} max {max(per):+.1%}")
rng = random.Random(0); bs = []
for _ in range(2000):
    ix = [rng.randrange(len(T)) for _ in T]
    bs.append(1 - sum(bd[i] for i in ix) / sum(raw[i] for i in ix))
bs.sort(); print(f"bootstrap 95% CI of pooled saving vs raw: [{bs[50]:+.1%}, {bs[1949]:+.1%}]")
for k in (8, 16, 32, 64):
    s = [t for t in T if len(rp.prep(t)[1]) >= k]
    if s:
        a = sum(rp.run(t, "raw", False)["cost"] for t in s); b = sum(rp.run(t, "batch", True)["cost"] for t in s)
        print(f"  traces with >= {k:2d} calls (n={len(s):2d}): saving vs raw {1-b/a:+.1%}")
for ph, mr in ((12, 3), (30, 3), (30, 6), (12, 10)):
    rp.PH, rp.MINRUN = ph, mr
    a = sum(tot("raw", False)); b = sum(tot("batch", True)); c = sum(tot("raw", True)); r5 = sum(tot("roll", False))
    print(f"PH={ph} MINRUN={mr}: raw+delta {1-c/a:+.1%}, batch+delta {1-b/a:+.1%} vs raw; roll-5 {1-r5/a:+.1%} vs raw")
rp.PH, rp.MINRUN = 12, 3
mx = max(max(sum(t["msgs"][j]["chars"] for j in range(i)) / rp.prep(t)[4] for i in rp.prep(t)[1]) for t in T)
print(f"largest raw-append prompt: {mx/1e3:.0f}k tokens (Claude 3.5 Sonnet window 200k)")
