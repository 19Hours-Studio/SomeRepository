# Critic checks on round1/replay2.py (imported unchanged; variants monkey-patched here).
import replay2 as R, statistics, random
A = lambda pol, **kw: R.avg(pol, **kw)

print("== 1. inplace new-token double count (replay2_fix: edited segment counted new only after break) ==")
import replay2_fix as F
a, b = R.avg("inplace"), F.avg("inplace")
print(f"hit_resent {a['hit_old']:.4f} -> {b['hit_old']:.4f}; inplace no-miss floor {a['floor']:,.0f} -> {b['floor']:,.0f}; API unchanged {a['api']:,.0f}={b['api']:,.0f}")
print("\n== 2. Idea 2 increment over the best CLIENT policy (errata), sec C retention 195k->140k, 200 turns ==")
C = {p: A(p, seeds=30, turns=200, window=200_000, trigger=195_000, target=140_000)["api"] for p in ("errata", "punch", "patch", "append_full")}
for p in ("punch", "patch"): print(f"{p}: {C[p]/C['errata']-1:+.1%} vs errata  ({C[p]/C['append_full']-1:+.1%} vs append_full)")
for tgt in (100_000, 170_000):
    D = {p: A(p, seeds=20, turns=200, window=200_000, trigger=195_000, target=tgt)["api"] for p in ("append_full", "errata", "punch")}
    print(f"target {tgt//1000}k: punch {D['punch']/D['errata']-1:+.1%} vs errata, {D['punch']/D['append_full']-1:+.1%} vs append_full")

print("\n== 3. Sec B grid edge: extend triggers/targets below 150k/40k (200 turns, 20 seeds) ==")
for pol in ("append_full", "errata", "punch", "patch"):
    best = None
    for trig in (60_000, 100_000, 150_000):
        for tgt in (15_000, 25_000, 40_000):
            if tgt >= trig: continue
            v = A(pol, seeds=20, turns=200, window=200_000, trigger=trig, target=tgt)["api"]
            if best is None or v < best[0]: best = (v, trig, tgt)
    print(f"{pol:12s} best {best[0]:,.0f} at {best[1]//1000}k/{best[2]//1000}k")

print("\n== 4. Early mutable state (memory/todo block right after sys prompt): edit always hits segment 1 ==")
orig_choice = random.Random.choice
def early(self, seq): return seq[0]
random.Random.choice = early
E = {p: A(p, seeds=30)["api"] for p in ("inplace", "append_full", "errata")}
random.Random.choice = orig_choice
print(f"errata {E['errata']/E['inplace']-1:+.1%} vs inplace (uniform-position edits gave -35.8%), append_full {E['append_full']/E['inplace']-1:+.1%}")

print("\n== 5. Unused lever: fewer requests per unit of work (batch k tool calls per request; same tokens) ==")
for k in (1, 2, 4):
    v = A("errata", turns=50 // k, tool=2000 * k, out=300 * k, edit_every=max(1, 5 // k), diff=200 * k)["api"]
    print(f"{k} tool calls/request: errata API {v:,.0f} ({v/A('errata')['api']-1:+.1%} vs 1/request)")

print("\n== 6. 5-min TTL expiry: fraction f of turns idle > TTL rebill live context as write ==")
r = [R.run("errata", seed=s) for s in range(30)]
for f in (0.05, 0.2):
    # sum of read tokens per session = (api - 1.25*writes)/0.1; approximate by hit*tot: recompute tot
    v = []
    for x in r:
        tot = sum(10_000 + t * 2300 + (t // 5) * 200 for t in range(50))
        reads = x["hit"] * tot
        v.append(x["api"] + f * reads * (1.25 - 0.10))
    m = statistics.mean(v); b0 = statistics.mean(x["api"] for x in r)
    print(f"f={f:.2f}: errata API {b0:,.0f} -> {m:,.0f} ({m/b0-1:+.0%}); hit rate on re-sent tokens -> {1-f:.2f}")
