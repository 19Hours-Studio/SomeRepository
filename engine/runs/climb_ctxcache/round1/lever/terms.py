# Decomposes the billed input of replay.py policies (Anthropic 5-min: write 1.25x, read 0.1x) into
# (a) reads of the static per-task prefix (system + demo trajectory + issue), (b) reads of the growing history,
# (c) first-time writes of new content, (d) re-writes caused by mask-induced cache breaks.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import replay as rp
W, R = 1.25, 0.10
def decomp(tr, policy, delta):
    m, calls, obs, roll, c = rp.prep(tr)
    P = sum(x["chars"] for x in m[:obs[0]]) / c                  # static prefix: everything before 1st observation
    sysd = sum(x["chars"] for x in m[:obs[0]] if x["role"] == "system" or x["demo"]) / c
    r = rp.run(tr, policy, delta)
    reads = R * r["hit"] * r["tok"]; writes = r["cost"] - reads
    pre_reads = R * P * (len(calls) - 1)                         # call 0 writes it, every later call reads it
    full = {j: m[j]["chars"] / c for j in range(len(m))}
    dsz = rp.delta_tokens(m, c, lambda k: set(range(k)))[0] if delta else {}
    first = W * sum(dsz.get(j, full[j]) for j in range(calls[-1]))   # every segment written once (upper bound on floor)
    return dict(cost=r["cost"], pre=pre_reads, hist=reads - pre_reads, first=first, rew=writes - first, P=P, sysd=sysd,
                calls=len(calls))
for name, pol, d in [("raw append", "raw", False), ("raw + delta", "raw", True), ("batch + delta", "batch", True)]:
    D = [decomp(t, pol, d) for t in rp.T]; C = sum(x["cost"] for x in D)
    s = lambda k: sum(x[k] for x in D)
    print(f"{name:14s} total={C/1e6:5.2f}M | prefix reads {s('pre')/1e6:4.2f}M ({s('pre')/C:5.1%}) | history reads "
          f"{s('hist')/1e6:4.2f}M ({s('hist')/C:5.1%}) | first writes {s('first')/1e6:4.2f}M ({s('first')/C:5.1%}) | "
          f"re-writes {s('rew')/1e6:5.2f}M ({s('rew')/C:5.1%})")
D = [decomp(t, "raw", False) for t in rp.T]
print(f"static prefix per task: mean {sum(x['P'] for x in D)/len(D):,.0f} tok, of which system+demo (identical across tasks) "
      f"{sum(x['sysd'] for x in D)/len(D):,.0f} tok; calls/task mean {sum(x['calls'] for x in D)/len(D):.1f}")
