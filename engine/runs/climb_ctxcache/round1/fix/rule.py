# Price-derived online clearing rule ("horizon rule") on the same 200 real traces, plus a check that
# every batch/horizon schedule shows the model a superset of what the sliding window shows.
# Clear the stale old observations S at request j iff  R * S * H  >=  (W - R) * X,
# where X = tokens that must be re-written after the first cleared position and H = expected remaining
# requests (online guess H = j, requests so far; "oracle" uses the true remaining count).
# Usage: python3 -I rule.py data/traces.jsonl
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import traces as T
def horizon_seq(tr, ntok, W, R, oracle=False):
    A = T.requests(tr); seq = []; el = set(); els = []
    for j, a in enumerate(A):
        elig = T.old_obs(tr, a) - el
        if elig:
            S = sum(ntok[i] for i in elig); f = min(elig)
            X = sum(ntok[i] for i in range(f, a) if i not in elig) + T.PH * len(elig)
            H = (len(A) - j) if oracle else max(j, 1)
            if R * S * H >= (W - R) * X: el |= elig
        seq.append(T.ctx(tr, ntok, a, el)); els.append(set(el))
    return seq, els
tot = {}; viol = 0; nreq = 0
for tr in T.load(sys.argv[1]):
    ntok = [T.tok(s) for s in tr["text"]]
    for pn, (W, R) in T.PRICES.items():
        for k, seq in [("append", T.policy_seq(tr, ntok, "append", W, R)),
                       ("sliding", T.policy_seq(tr, ntok, "sliding", W, R)),
                       ("batch5k", T.policy_seq(tr, ntok, "batch", W, R, 5000)),
                       ("horizon", horizon_seq(tr, ntok, W, R)[0]),
                       ("horizon-oracle", horizon_seq(tr, ntok, W, R, True)[0])]:
            c, h, t = T.bill(seq, W, R)
            for q, v in (("c", c), ("h", h), ("t", t)): tot[(pn, k, q)] = tot.get((pn, k, q), 0) + v
        tot[(pn, "opt", "c")] = tot.get((pn, "opt", "c"), 0) + T.offline_opt(tr, ntok, W, R)
        # superset check: elided(horizon) and elided(batch) must be subsets of elided(sliding) at every request
        A = T.requests(tr); _, els = horizon_seq(tr, ntok, W, R)
        for j, a in enumerate(A):
            nreq += 1
            if not els[j] <= T.old_obs(tr, a): viol += 1
for pn in T.PRICES:
    sl = tot[(pn, "sliding", "c")]; ap = tot[(pn, "append", "c")]
    print(f"== {pn}")
    for k in ("append", "sliding", "batch5k", "horizon", "horizon-oracle", "opt"):
        c = tot[(pn, k, "c")]
        hr = f"token hit={tot[(pn,k,'h')]/tot[(pn,k,'t')]:.3f} (token-weighted)  mean prompt={tot[(pn,k,'t')]/(nreq/2):,.0f}" if (pn, k, "h") in tot else ""
        print(f"  {k:15s} {c:13,.0f}  vs sliding {c/sl-1:+.1%}  vs append {c/ap-1:+.1%}  {hr}")
print(f"superset check: {viol} violations in {nreq} requests (0 = model never sees less than under the sliding window)")
