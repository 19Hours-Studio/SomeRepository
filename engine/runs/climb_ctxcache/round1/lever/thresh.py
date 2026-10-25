# (1) Price-derived (ski-rental) masking trigger vs the fixed "clear_at_least" thresholds of Anthropic-style context
#     editing, on the same 63 real traces, best threshold chosen in hindsight (favours the fixed rule).
# (2) Cross-task sharing of the system prompt + demo trajectory (identical in all tasks): in replay.py every trace
#     writes it at 1.25x on its first call; in a concurrent eval/fleet only the first task writes it.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import replay as rp
T = rp.T
for W, R, pn in ((1.25, 0.10, "anthropic_5m"), (1.00, 0.10, "openai_auto")):
    raw = sum(rp.run(t, "raw", False, W, R)["cost"] for t in T)
    for d in (False, True):
        ski = sum(rp.run(t, "batch", d, W, R)["cost"] for t in T)
        row = []
        for th in (2_000, 5_000, 10_000, 20_000, 40_000):
            rp.THRESH = th; row.append((th, sum(rp.run(t, "thresh", d, W, R)["cost"] for t in T)))
        best = min(row, key=lambda x: x[1])
        print(f"[{pn}] delta={d!s:5} ski-rental {1-ski/raw:+.1%} vs raw | fixed thresholds: " +
              " ".join(f"{th//1000}k:{1-c/raw:+.1%}" for th, c in row) + f" | best fixed {best[0]//1000}k; ski vs best fixed: {ski/best[1]:.3f}x")
rp.THRESH = 10_000
W, R = 1.25, 0.10
raw = sum(rp.run(t, "raw", False)["cost"] for t in T); bd = sum(rp.run(t, "batch", True)["cost"] for t in T)
sd = []
for t in T:
    m, calls, obs, roll, c = rp.prep(t)
    sd.append(sum(x["chars"] for x in m[:obs[0]] if x["role"] == "system" or x["demo"]) / c)
share = (W - R) * sum(sd[1:])          # all but the first task read the shared system+demo instead of writing it
print(f"cross-task shared system+demo ({sum(sd)/len(sd):,.0f} tok): saves {share/1e6:.2f}M units; "
      f"batch+delta+shared = {(bd-share)/1e6:.2f}M = {1-(bd-share)/raw:+.1%} vs raw ({1-(raw-share)/raw:+.1%} for raw+shared alone)")
