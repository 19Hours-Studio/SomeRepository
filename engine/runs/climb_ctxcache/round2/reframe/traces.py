# Replay of 200 real SWE-agent trajectories (Claude Sonnet 4, SWE-bench Verified, public S3 bucket;
# fetched by fetch_traces.py) under different context-management policies, billed with exact
# prefix-cache rules. Request j = all messages before assistant turn j (as the agent sent them).
# Billing per request: R * (longest common prefix with the previous request) + W * (rest).
# Tokens ~ chars/3.5 (no tokenizer download possible here); a 2,500-token tool-schema prefix is added.
# Usage: python3 -I traces.py data/traces.jsonl
import json, sys, os, difflib, re, statistics as st

CH = 3.5; TOOLS = 2500; KEEP = int(os.environ.get("KEEP", 5)); PH = 12      # placeholder "Old environment output: (N lines omitted)"
PRICES = {"anthropic": (1.25, 0.10), "openai": (1.00, 0.10)}
OUT_PRICE = 5.0                                 # Claude Sonnet 4 output $15 vs input $3 per M

def tok(s): return max(1, round(len(s) / CH))

def load(path):
    T = []
    for l in open(path):
        t = json.loads(l); m = t["msgs"]
        T.append({"id": t["id"], "role": [x["role"] for x in m], "text": [x["text"] for x in m]})
    return T

def requests(tr):  # indices a where an assistant message starts; request = msgs[:a]
    return [a for a, r in enumerate(tr["role"]) if r == "assistant"]

def is_obs(tr, i): return i >= 2 and tr["role"][i] in ("tool", "user")

def ctx(tr, ntok, a, elided):  # list of (key, tokens) segments; key identifies exact content
    segs = [("tools", TOOLS)]
    for i in range(a):
        if i in elided: segs.append((("ph", i), PH))
        else: segs.append(((i, 0), ntok[i]))
    return segs

def lcp(s1, s2):
    n = 0
    for x, y in zip(s1, s2):
        if x != y: break
        n += x[1]
    return n

def bill(seq, W, R):  # seq = list of contexts (segment lists), one per request
    cost = hit = tot = 0; prev = []
    for s in seq:
        L = sum(t for _, t in s); c = lcp(prev, s)
        cost += R * c + W * (L - c); hit += c; tot += L; prev = s
    return cost, hit, tot

def old_obs(tr, a):  # observations that are outside the last-KEEP window at request a
    obs = [i for i in range(a) if is_obs(tr, i)]
    return set(obs[:-KEEP]) if len(obs) > KEEP else set()

def policy_seq(tr, ntok, pol, W, R, theta=None):
    A = requests(tr); seq = []; elided = set(); debt = 0.0
    for a in A:
        eligible = old_obs(tr, a) - elided
        if pol == "sliding": elided |= eligible
        elif pol == "batch" and sum(ntok[i] for i in eligible) >= theta: elided |= eligible
        elif pol == "ski" and eligible:
            # rent: each request pays R per stale token; buy: rewrite suffix from first eligible obs
            debt += R * sum(ntok[i] for i in eligible)
            first = min(eligible)
            buy = (W - R) * (TOOLS + sum(ntok[i] for i in range(first, a)))
            if debt >= buy: elided |= eligible; debt = 0.0
        seq.append(ctx(tr, ntok, a, elided))
    return seq

def offline_opt(tr, ntok, W, R):
    # DP over clearing times. A clear at request j elides all eligible-old observations at j.
    A = requests(tr); n = len(A)
    def el(c): return set() if c < 0 else old_obs(tr, A[c])
    memo = {}
    def C(j, c):  # context at request j with last clear at request index c (c=-1: none)
        k = (j, c)
        if k not in memo: memo[k] = ctx(tr, ntok, A[j], el(c))
        return memo[k]
    def L(s): return sum(t for _, t in s)
    best = {-1: W * L(C(0, -1))}                     # state: last clear index -> min cost so far
    for j in range(1, n):
        nb = {}
        for c, v in best.items():
            for c2 in (c, j):
                s0, s1 = C(j - 1, c), C(j, c2); h = lcp(s0, s1)
                x = v + R * h + W * (L(s1) - h)
                if x < nb.get(c2, 1e30): nb[c2] = x
        best = nb
        for k in [k for k in memo if k[0] < j - 1]: del memo[k]
    return min(best.values())

VIEW = re.compile(r"Here's the result of running `cat -n` on (\S+?):\r?\n")
def delta_views(tr):
    # Client-side delta tool outputs: when the agent re-views a file already shown (full view) in
    # context, send a unified diff against the last shown version (or "unchanged") instead.
    text = list(tr["text"]); last = {}; nre = nchg = 0
    for i, s in enumerate(text):
        if not is_obs(tr, i): continue
        m = VIEW.search(s)
        if not m: continue
        p = m.group(1); body = s[m.end():]
        if p in last:
            nre += 1
            old = last[p].splitlines(); new = body.splitlines()
            if old == new: text[i] = f"[{p}: unchanged since your last view]"
            else:
                d = list(difflib.unified_diff(old, new, lineterm="", n=1))
                cand = f"[{p}: diff vs your last view]\n" + "\n".join(d[2:]); nchg += 1
                if len(cand) < len(s): text[i] = cand
        last[p] = body
    return text, nre, nchg

def run(path):
    T = load(path); agg = {}
    def add(k, v): agg.setdefault(k, []).append(v)
    for tr in T:
        ntok = [tok(s) for s in tr["text"]]
        A = requests(tr)
        out_tok = sum(ntok[a] for a in A)
        for pn, (W, R) in PRICES.items():
            base = bill(policy_seq(tr, ntok, "append", W, R), W, R)
            add((pn, "append", "cost"), base[0]); add((pn, "append", "hit"), base[1] / base[2])
            add((pn, "append", "ctx"), base[2] / len(A)); add((pn, "nocache"), W * 0 + base[2])
            add((pn, "out"), OUT_PRICE * out_tok)
            for pol, th in [("sliding", None), ("batch", 5_000), ("batch", 10_000), ("batch", 20_000), ("batch", 30_000), ("ski", None)]:
                c, h, t = bill(policy_seq(tr, ntok, pol, W, R, th), W, R)
                k = pol if th is None else f"batch{th//1000}k"
                add((pn, k, "cost"), c); add((pn, k, "hit"), h / t); add((pn, k, "ctx"), t / len(A))
                # server-side splice (hole-punch / Leyline-style): only placeholders + new tokens are written
                if pol == "sliding":
                    seq = policy_seq(tr, ntok, pol, W, R); cs = 0; prevkeys = set()
                    for s in seq:
                        new = sum(t for key, t in s if key not in prevkeys); Ls = sum(t for _, t in s)
                        cs += R * (Ls - new) + W * new; prevkeys = {key for key, _ in s}
                    add((pn, "sliding+splice", "cost"), cs)
            add((pn, "opt", "cost"), offline_opt(tr, ntok, W, R))
            # delta re-views on top of append-only
            dt, nre, nchg = delta_views(tr); ntd = [tok(s) for s in dt]
            c, h, t = bill(policy_seq({"role": tr["role"], "text": dt}, ntd, "append", W, R), W, R)
            add((pn, "delta", "cost"), c); add((pn, "delta", "hit"), h / t); add((pn, "delta", "ctx"), t / len(A))
            c2, h2, t2 = bill(policy_seq({"role": tr["role"], "text": dt}, ntd, "ski", W, R), W, R)
            add((pn, "delta+ski", "cost"), c2); add((pn, "delta+ski", "ctx"), t2 / len(A))
            if pn == "anthropic": add(("re",), nre); add(("chg",), nchg); add(("req",), len(A))
    S = lambda k: sum(agg[k])
    print(f"traces={len(T)}  requests/trace mean={st.mean(agg[('req',)]):.1f}  file re-views/trace={st.mean(agg[('re',)]):.1f} "
          f"(changed {st.mean(agg[('chg',)]):.1f})")
    for pn in PRICES:
        b = S((pn, "append", "cost"))
        print(f"\n== {pn} (write {PRICES[pn][0]}x, read {PRICES[pn][1]}x); totals over all traces, base-input units ==")
        print(f"no cache (all input at 1.0x): {S((pn,'nocache')):,.0f}   output tokens at {OUT_PRICE}x: {S((pn,'out')):,.0f}")
        for k in ["append", "sliding", "sliding+splice", "batch5k", "batch10k", "batch20k", "batch30k", "ski", "opt", "delta", "delta+ski"]:
            c = S((pn, k, "cost"))
            hit = f"tok-hit={st.mean(agg[(pn,k,'hit')]):.3f}" if (pn, k, "hit") in agg else " " * 13
            cx = f"mean ctx={st.mean(agg[(pn,k,'ctx')]):,.0f}" if (pn, k, "ctx") in agg else ""
            print(f"{k:15s} cost={c:14,.0f}  vs append {c/b-1:+.1%}  vs sliding {c/S((pn,'sliding','cost'))-1:+.1%}  {hit} {cx}")
    # share of reads in append-only cost
    W, R = PRICES["anthropic"]; rd = 0
    for tr in T:
        ntok = [tok(s) for s in tr["text"]]; c, h, t = bill(policy_seq(tr, ntok, "append", W, R), W, R); rd += R * h
    print(f"\nanthropic append-only: reads are {rd/S(('anthropic','append','cost')):.1%} of billed input; "
          f"input is {S(('anthropic','append','cost'))/(S(('anthropic','append','cost'))+S(('anthropic','out'))):.1%} of input+output bill")

if __name__ == "__main__":
    run(sys.argv[1])
