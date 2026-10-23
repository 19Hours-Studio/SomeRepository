import statistics as st, math
from model2 import run
# share-cap sweep for floating ledger in C and E
for cap in (0.02, 0.05, 0.10, 0.20):
    c = st.mean(run(doc=25_000, turns=10, edits=3, patch=500, mode="ledger", share_cap=cap, seed=s)[0] for s in range(300))
    e = st.mean(run(doc=150_000, turns=40, edits=20, patch=200, pos_hi=8000, mode="ledger", share_cap=cap, seed=s)[0] for s in range(300))
    print(f"cap {cap:.2f}: C ledger ${c:.4f}  E ledger ${e:.4f}")
# idea2 depth cap sweep in D and E
for dc in (1, 2, 3, 99):
    d = st.mean(run(doc=120_000, turns=30, edits=15, patch=300, mode="idea2", depth_cap=dc, seed=s)[0] for s in range(300))
    e = st.mean(run(doc=150_000, turns=40, edits=20, patch=200, pos_hi=8000, mode="idea2", depth_cap=dc, seed=s)[0] for s in range(300))
    print(f"depth cap {dc}: D idea2 ${d:.4f}  E idea2 ${e:.4f}")
# token-weighted cache hit rate, D scenario, inline vs patched (analytic: reread tokens / total input)
doc, turns, sysp, q, ans = 120_000, 30, 3000, 60, 400
# patched: every turn only q + prev answer + patch are new
tot = sum(sysp + doc + t*(q+ans) + q for t in range(turns))
new = sysp + doc + q + sum(q + ans for t in range(1, turns)) + 15*300
print(f"D patched hit rate = {1-new/tot:.4f}  (new-token floor = {new/tot:.4f})")
# inline: mean edit at doc/2 -> recompute ~doc/2+hist per edit
new_in = new - 15*300 + sum(doc/2 + t*(q+ans) for t in range(1, turns, 2))
print(f"D inline hit rate ~ {1-new_in/tot:.4f}")
# paired-eval sample size (McNemar), detect 3-pt drop, discordance 8% / 15%, alpha .05 two-sided, power .8
za, zb = 1.96, 0.8416
for pd in (0.08, 0.15):
    d = 0.03
    n = ((za*math.sqrt(pd) + zb*math.sqrt(pd - d*d)) / d) ** 2
    print(f"McNemar n for 3-pt drop at discordance {pd}: {math.ceil(n)} paired questions")
