# Check1 probes on the answer's 200 real traces, reusing the answer's traces.py billing.
# Usage: python3 -I probe.py ../../round1/fix/data/traces.jsonl
import sys, os, random; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import traces as T
W, R = T.PRICES["anthropic"]

def horizon_seq(tr, ntok):  # copied from the answer's rule.py (online H = j)
    A = T.requests(tr); seq = []; el = set()
    for j, a in enumerate(A):
        elig = T.old_obs(tr, a) - el
        if elig:
            S = sum(ntok[i] for i in elig); f = min(elig)
            X = sum(ntok[i] for i in range(f, a) if i not in elig) + T.PH * len(elig)
            if R * S * max(j, 1) >= (W - R) * X: el |= elig
        seq.append(T.ctx(tr, ntok, a, el))
    return seq

def polling_seq(tr, ntok, P):
    # SWE-agent LastNObservations(n=KEEP, polling=P): elision boundary advances only every P steps,
    # so the model keeps between KEEP and KEEP+P-1 recent observations.
    A = T.requests(tr); seq = []
    for a in A:
        obs = [i for i in range(a) if T.is_obs(tr, i)]
        m = max(0, len(obs) - T.KEEP); m = (m // P) * P
        seq.append(T.ctx(tr, ntok, a, set(obs[:m])))
    return seq

def selective_seq(tr, ntok, minsz, theta):
    # batch-clear only stale observations of >= minsz tokens (subset of sliding's set -> superset context)
    A = T.requests(tr); seq = []; el = set()
    for a in A:
        elig = {i for i in T.old_obs(tr, a) - el if ntok[i] >= minsz}
        if sum(ntok[i] for i in elig) >= theta: el |= elig
        seq.append(T.ctx(tr, ntok, a, el))
    return seq

def lookback_bill(seq, blocks, maxlb=20):
    # Anthropic: breakpoint only at the end of each request (+ tools). A hit at an earlier block
    # boundary is found only within ~20 blocks before the breakpoint; else fall back to tools prefix.
    cost = 0; prev = []
    for s in seq:
        L = sum(t for _, t in s); c = T.lcp(prev, s)
        # index of first differing segment
        k = 0
        for x, y in zip(prev, s):
            if x != y: break
            k += 1
        nblk_after = sum(blocks.get(key, 1) for key, _ in s[k:])
        if prev and k < len(prev) and nblk_after > maxlb: c = T.TOOLS
        cost += R * c + W * (L - c); prev = s
    return cost

def main(path):
    Tr = T.load(path); rows = {}
    def add(k, tr_i, v): rows.setdefault(k, [0.0] * len(Tr))[tr_i] = v
    for n, tr in enumerate(Tr):
        ntok = [T.tok(s) for s in tr["text"]]
        seqs = {"append": T.policy_seq(tr, ntok, "append", W, R),
                "sliding": T.policy_seq(tr, ntok, "sliding", W, R),
                "batch5k": T.policy_seq(tr, ntok, "batch", W, R, 5000),
                "horizon": horizon_seq(tr, ntok)}
        for P in (5, 10, 20): seqs[f"polling{P}"] = polling_seq(tr, ntok, P)
        for ms in (500, 1000, 2000):
            for th in (3000, 5000, 10000): seqs[f"sel{ms}_{th//1000}k"] = selective_seq(tr, ntok, ms, th)
        blocks = {("tools"): 1}
        for i, r in enumerate(tr["role"]): blocks[(i, 0)] = 2 if r == "assistant" else 1
        for k, s in seqs.items():
            c, h, t = T.bill(s, W, R); add(k, n, c); add(k + ":t", n, t); add(k + ":req", n, len(s))
            if k in ("append", "sliding", "batch5k", "horizon", "polling10", "sel1000_5k"):
                add(k + ":lb20", n, lookback_bill(s, blocks))
    S = lambda k: sum(rows[k])
    sl, ap = S("sliding"), S("append"); nreq = S("append:req")
    print("policy           cost        vs sliding  vs append  mean prompt   (Anthropic prices)")
    for k in [k for k in rows if ":" not in k]:
        print(f"{k:14s} {S(k):13,.0f}  {S(k)/sl-1:+7.1%}  {S(k)/ap-1:+7.1%}  {S(k+':t')/nreq:9,.0f}")
    print("\nopt (answer's DP) for reference: 33,347,648")
    print("\nWith Anthropic ~20-block lookback, one breakpoint at the end (no extra breakpoint at the clear point):")
    for k in ("append", "sliding", "batch5k", "horizon", "polling10", "sel1000_5k"):
        c = S(k + ":lb20"); print(f"  {k:12s} {c:13,.0f}  vs exact-LCP {c/S(k)-1:+.1%}  vs sliding(lb20) {c/S('sliding:lb20')-1:+.1%}")
    # bootstrap CI over traces for horizon/batch vs sliding and vs append
    rng = random.Random(1); N = len(Tr)
    for k in ("horizon", "batch5k", "polling10", "sel1000_5k"):
        for base in ("sliding", "append"):
            v = []
            for _ in range(2000):
                idx = [rng.randrange(N) for _ in range(N)]
                v.append(sum(rows[k][i] for i in idx) / sum(rows[base][i] for i in idx) - 1)
            v.sort(); print(f"bootstrap 95% CI {k} vs {base}: {v[50]:+.1%} .. {v[1949]:+.1%}")
main(sys.argv[1])
