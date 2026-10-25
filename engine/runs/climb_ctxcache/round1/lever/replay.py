# Replay of 63 real SWE-agent (Claude 3.5 Sonnet, SWE-bench Verified) trajectories under prefix-cache billing.
# Each API call's prompt = all history messages before that assistant turn; a request hits the cache for the
# longest prefix of segments identical to the previous request (agent turns are seconds apart, so a 5-min TTL holds).
# Billed input units per call = R*hit + W*(len - hit). Tokens = chars / c, with c calibrated per trace so that
# SWE-agent's actual policy (last-5-observation masking) reproduces the recorded model_stats.tokens_sent exactly.
import json, os, sys, statistics as st
from functools import lru_cache
HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, "traces.json")))
PH = 12          # tokens of a placeholder such as "Old output omitted (57 lines)." / "(lines 40-139 unchanged, see view #7)"
KEEP = 5         # SWE-agent's LastNObservations window
MINRUN = 3       # shortest run of known lines replaced by a back-reference
THRESH = 10_000  # "thresh" policy: fixed clear_at_least-style trigger (tokens freed), as in Anthropic context editing

def prep(tr):
    m = tr["msgs"]
    calls = [i for i, x in enumerate(m) if x["role"] == "assistant" and not x["demo"]]
    users = [i for i, x in enumerate(m) if x["role"] == "user" and not x["demo"]]
    obs = users[1:]                                  # first non-demo user message is the issue: never masked
    # per-call roll-5 masked set (what SWE-agent sent)
    def roll(i): o = [j for j in obs if j < i]; return frozenset(o[:-KEEP])
    mchars = sum(sum(40 if j in roll(i) else m[j]["chars"] for j in range(i)) for i in calls)
    c = mchars / tr["stats"]["tokens_sent"]
    return m, calls, obs, roll, c

def delta_tokens(m, c, visible):
    """Token size of each file view when runs of >=MINRUN lines already shown (same path, same content, constant
    line offset) in an earlier *visible* view are replaced by a PH-token back-reference. Returns (size, refs)."""
    size, refs = {}, {}
    for k, x in enumerate(m):
        if "lines" not in x or x["demo"]: continue
        prev = [j for j in range(k) if j in visible(k) and m[j].get("path") == x["path"] and not m[j]["demo"]]
        idx = {j: {h: n for n, h, _ in m[j]["lines"]} for j in prev}
        byln = {j: {n: h for n, h, _ in m[j]["lines"]} for j in prev}
        L = x["lines"]; covered = [None] * len(L); i = 0
        while i < len(L):
            best = (0, None)
            for j in prev:
                if L[i][1] in idx[j]:
                    off = L[i][0] - idx[j][L[i][1]]; r = 0
                    while i + r < len(L) and byln[j].get(L[i + r][0] - off) == L[i + r][1]: r += 1
                    if r > best[0]: best = (r, j)
            if best[0] >= MINRUN:
                for q in range(i, i + best[0]): covered[q] = best[1]
                i += best[0]
            else: i += 1
        runs = sum(1 for q in range(len(L)) if covered[q] is not None and (q == 0 or covered[q - 1] != covered[q]))
        saved = sum(L[q][2] for q in range(len(L)) if covered[q] is not None)
        size[k] = (x["chars"] - saved) / c + PH * runs
        refs[k] = {covered[q] for q in range(len(L)) if covered[q] is not None}
    return size, refs

def run(tr, policy, delta=False, W=1.25, R=0.10, mask_at=None):
    m, calls, obs, roll, c = prep(tr)
    full = {j: m[j]["chars"] / c for j in range(len(m))}
    vis_all = lambda k: set(range(k))
    if delta: dsz, refs = delta_tokens(m, c, vis_all)
    else: dsz, refs = {}, {}
    size = lambda j: dsz.get(j, full[j])
    def close(X, upto):            # never mask an observation still referenced by an unmasked later view
        X = set(X)
        while True:
            keep = {r for k in range(upto) if k not in X for r in refs.get(k, ())} & X
            if not keep: return frozenset(X)
            X -= keep
    prev_ids, prev_len = [], 0.0
    cost = hit = tot = vis = 0.0; S = frozenset(); rent = 0.0; nmask = 0
    for ci, i in enumerate(calls):
        if policy == "raw": S = frozenset()
        elif policy in ("roll", "splice"): S = close(roll(i), i)
        elif policy in ("batch", "sched", "thresh"):
            E = close(roll(i), i) - S
            if E:
                cand = S | E
                ids = [(j, j in cand) for j in range(i)]
                p = next(q for q in range(len(ids)) if q >= len(prev_ids) or ids[q] != prev_ids[q])
                cached_after = sum((PH if mk else size(j)) for j, mk in ids[p:len(prev_ids)])
                buy = (W - R) * cached_after   # suffix that turns from a read into a re-write
                if policy == "batch":
                    rent += R * sum(size(j) - PH for j in E)
                    go = rent >= buy
                elif policy == "thresh": go = sum(size(j) - PH for j in E) >= THRESH
                else: go = ci in mask_at
                if go: S = cand; rent = 0.0; nmask += 1
        ids = [(j, j in S) for j in range(i)]
        lens = [(PH if mk else size(j)) for j, mk in ids]
        L = sum(lens); h = 0.0
        if policy == "splice":        # own stack: masked spans' KV blocks dropped in place (Idea 2), rest reused
            ps = set(prev_ids); h = sum(l for a, l in zip(ids, lens) if a in ps)
        else:
            for q, (a, b) in enumerate(zip(ids, prev_ids)):
                if a != b: break
                h += lens[q]
        cost += R * h + W * (L - h); hit += h; tot += L
        vis += sum(size(j) for j in obs if j < i and j not in S)
        prev_ids = ids
    return dict(cost=cost, hit=hit / tot, tok=tot, calls=len(calls), vis=vis, nmask=nmask)

def opt_schedule(tr, delta=False, W=1.25, R=0.10):
    """Exact offline optimum over *when* to apply masking, where a mask at call k applies every observation
    eligible under roll-5 at k (same action space as the ski-rental rule). Cost after a mask at call j depends
    only on S_j, so f(j) = min(never again, min_k seg(j,k) + f(k)) is an exact O(K^2) DP."""
    m, calls, obs, roll, c = prep(tr); K = len(calls)
    full = {j: m[j]["chars"] / c for j in range(len(m))}
    dsz, refs = delta_tokens(m, c, lambda k: set(range(k))) if delta else ({}, {})
    size = lambda j: dsz.get(j, full[j])
    def close(X, upto):
        X = set(X)
        while True:
            keep = {r for k in range(upto) if k not in X for r in refs.get(k, ())} & X
            if not keep: return frozenset(X)
            X -= keep
    Sk = [close(roll(i), i) for i in calls]
    def ids(q, S): return [(j, j in S) for j in range(calls[q])]
    def cc(q, S, Sp):                       # cost of call q with mask S, previous call sent with mask Sp
        a = ids(q, S); b = ids(q - 1, Sp) if q else []
        lens = [(PH if mk else size(j)) for j, mk in a]; h = 0.0
        for t, (x, y) in enumerate(zip(a, b)):
            if x != y: break
            h += lens[t]
        return R * h + W * (sum(lens) - h)
    f = {}
    for j in range(K - 1, -2, -1):          # j = -1: no mask yet (S = empty)
        S = Sk[j] if j >= 0 else frozenset()
        run_ = [cc(q, S, S) for q in range(j + 1, K)]
        best = sum(run_); acc = 0.0
        for k in range(j + 1, K):
            if Sk[k] != S: best = min(best, acc + cc(k, Sk[k], S) + f[k])
            acc += run_[k - j - 1]
        f[j] = best
    return f[-1]

if __name__ == "__main__":
    PR = {"anthropic_5m": (1.25, 0.10), "openai_auto": (1.00, 0.10), "anthropic_1h": (2.00, 0.10)}
    cs = [prep(t)[4] for t in T]
    print(f"traces={len(T)} calls={sum(len(prep(t)[1]) for t in T)} chars/token calibrated median={st.median(cs):.2f} "
          f"IQR=({st.quantiles(cs, n=4)[0]:.2f},{st.quantiles(cs, n=4)[2]:.2f})")
    for pname, (W, R) in PR.items():
        res = {}
        for name, pol, d in [("raw append", "raw", False), ("roll-5 mask (SWE-agent)", "roll", False),
                             ("batch mask (ski-rental)", "batch", False),
                             ("roll-5 + KV splice (own stack)", "splice", False), ("raw + delta views", "raw", True),
                             ("roll-5 + delta", "roll", True), ("batch + delta", "batch", True)]:
            rr = [run(t, pol, d, W, R) for t in T]
            res[name] = rr
        base = sum(r["cost"] for r in res["roll-5 mask (SWE-agent)"])
        raw = sum(r["cost"] for r in res["raw append"])
        print(f"\n[{pname}: write {W}x, read {R}x]   cost units summed over traces; savings vs roll-5 and vs raw")
        for name, rr in res.items():
            C = sum(r["cost"] for r in rr); H = sum(r["hit"] * r["tok"] for r in rr) / sum(r["tok"] for r in rr)
            V = sum(r["vis"] for r in rr) / sum(r["vis"] for r in res["raw append"])
            print(f"  {name:30s} cost={C/1e6:7.2f}M  token-hit={H:6.1%}  tokens_sent={sum(r['tok'] for r in rr)/1e6:6.2f}M "
                  f" vs roll5={1-C/base:+6.1%}  vs raw={1-C/raw:+6.1%}  obs-visible={V:5.1%}  masks/trace={st.mean(r['nmask'] for r in rr):.1f}")
        if pname == "anthropic_5m":
            # read/write split of the cost for raw append and the best policy
            for name in ("raw append", "batch + delta"):
                rr = res[name]; Rd = sum(R * r["hit"] * r["tok"] for r in rr); C = sum(r["cost"] for r in rr)
                print(f"  split {name}: reads {Rd/C:.1%} of billed input, writes {1-Rd/C:.1%}")
            out = sum(t["stats"]["tokens_received"] for t in T)
            print(f"  output tokens: {out/1e3:.0f}k = {5*out/raw:.1%} of raw-append input cost at 5x output price")
            sub = T
            ob = sum(opt_schedule(t, False) for t in sub); bb = sum(run(t, "batch", False)["cost"] for t in sub)
            print(f"  ski-rental vs offline-best schedule (exact DP, all traces): {bb/ob:.3f}x")
