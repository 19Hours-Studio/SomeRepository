# Critic-2 checks on round2. Imports the author's sim3 (copied verbatim) and adds instrumentation.
import sim3 as S, statistics as st, random, math
base = {p: S.avg(p)["api"] for p in ("inplace", "append_full", "errata")}
print("== A. output tokens priced (300 tok/call generated; out multiple x input) ==")
for name, om in (("Anthropic 5x", 5), ("OpenAI 8x", 8)):
    O = 50 * 300 * om
    e, i, a = (base[k] + O for k in ("errata", "inplace", "append_full"))
    q2 = S.avg("errata", q2=1)["api"] + O; q4 = S.avg("errata", q4=1)["api"] + O
    a03 = S.avg("append_full", q2=0.3)["api"] + O
    print(f"{name}: O={O:,} errata vs inplace {e/i-1:+.1%} (claimed -35.8%), vs append_full {e/a-1:+.1%} (-11.0%);"
          f" pairs vs errata seq {q2/e-1:+.1%} (-36.2%), quads {q4/e-1:+.1%} (-52.7%);"
          f" pairs/quads vs append_full@q2=.3 {q2/a03-1:+.1%}/{q4/a03-1:+.1%} (-31.7/-49.4%)")
for thinking in (1000, 3000):   # reasoning tokens per request (not re-sent); proportional to requests
    O1 = 50 * (300 + thinking) * 5; e = base["errata"] + O1
    x2 = S.avg("errata", q2=1); O2 = 50 * 300 * 5 + x2["nreq"] * thinking * 5
    print(f"  with {thinking} thinking tok/request (5x): pairs vs errata seq {(x2['api']+O2)/e-1:+.1%}")

print("\n== B. span ops: cost vs MEAN live context per request (quality proxy), 200 calls, 20 seeds ==")
def instrumented(policy, **kw):
    Ls = []; orig = S.session
    # recompute mean L by re-running the loop logic cheaply: patch sum via wrapper on PR? simpler: copy-run
    return Ls
# lightweight re-implementation of mean context: wrap session by monkeypatching math.ceil is ugly; instead replay sizes
def mean_ctx(policy, seeds=20, **kw):
    import inspect
    src = inspect.getsource(S.session).replace("api += p[\"r\"] * cached", "LL.append(L); api += p[\"r\"] * cached")
    src = src.replace("def session(", "def session_i(LL, ")
    ns = dict(S.__dict__); exec(src, ns)
    out = []
    for s in range(seeds):
        LL = []; r = ns["session_i"](LL, policy, seed=s, **kw); out.append((r["api"], st.mean(LL)))
    return st.mean(a for a, _ in out), st.mean(l for _, l in out)
rows = []
for pol in ("errata", "patch", "punch"):
    for trig, tgt in ((60_000, 15_000), (60_000, 40_000), (120_000, 60_000), (195_000, 100_000), (195_000, 140_000),
                      (195_000, 170_000), (195_000, 185_000)):
        c, m = mean_ctx(pol, calls=200, window=200_000, trigger=trig, target=tgt)
        rows.append((pol, trig, tgt, c, m)); print(f"{pol:7s} {trig//1000:3d}k->{tgt//1000:3d}k cost {c:11,.0f} mean ctx {m:9,.0f}  cost/meanctx {c/m:6.1f}")
print("  frontier comparison at similar mean context:")
E = [r for r in rows if r[0] == "errata"]; P = [r for r in rows if r[0] == "patch"]
for p in P:
    # cheapest errata config with mean ctx >= patch's mean ctx  (interpolate linearly in cost vs mean ctx)
    pts = sorted((r[4], r[3]) for r in E)
    for (m0, c0), (m1, c1) in zip(pts, pts[1:]):
        if m0 <= p[4] <= m1:
            ce = c0 + (c1 - c0) * (p[4] - m0) / (m1 - m0)
            print(f"  patch {p[1]//1000}k->{p[2]//1000}k mean {p[4]:,.0f}: {p[3]:,.0f} vs errata frontier {ce:,.0f} -> {p[3]/ce-1:+.1%}")

print("\n== C. TTL: selective 1h write only on the request before a predicted idle gap ==")
# Assumes (UNTESTED) a 1h-TTL breakpoint after a 5m-cached prefix re-tags the whole prefix at 1h, paying 2x only on the new
# tokens of that request. Upper bound for a perfect gap predictor; gaps < 60 min.
for G in (15, 45):
    for f in (0.05, 0.2):
        ref = S.avg("errata", seeds=40)["api"]
        # extra = (2.0-1.25)*new tokens of the request preceding each gap; new tokens/request ~ 2300 (+200 per edit)
        x = S.avg("errata", seeds=40, idle_p=f, idle_min=G, ttl_policy="none")  # no expiry modelled
        extra = 0.75 * 2340 * f * 49
        print(f"gap {G} f={f}: selective-1h {(x['api']+extra)/ref-1:+.2%} vs no-idle reference (answer best: keepalive +11.1%, 1h-all +19.5%)")
