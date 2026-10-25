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

