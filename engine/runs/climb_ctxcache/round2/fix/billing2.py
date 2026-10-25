# Round 2 billing probes on the same 200 real SWE-agent traces (reuses traces.py from round 1).
# (a) Anthropic breakpoint model: cache entries exist only at breakpoint positions written by earlier
#     requests; each breakpoint looks back at most 20 blocks for an entry. "1bp" = breakpoint at the end
#     of each request only; "2bp" = also a stable breakpoint after the last placeholder plus one at the
#     first edited position (4 breakpoints in all). Shows the fix check1 asked for and what it restores.
# (b) Fair client-side comparison: every policy family (SWE-agent polling, fixed batch, horizon, DP)
#     swept over its knob, reported as cost vs mean prompt, plus context-matched pairs.
# (c) Own-stack compute accounting (prefill FLOPs, Llama-3-70B shape) instead of API prices, including
#     the RoPE re-rotation of downstream keys that a splice needs.
# Usage: python3 -I billing2.py data/traces.jsonl
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import traces as T
W, R = T.PRICES["anthropic"]

def polling_seq(tr, ntok, P, keep):  # SWE-agent LastNObservations(n=keep, polling=P), as in check1
    seq = []
    for a in T.requests(tr):
        obs = [i for i in range(a) if T.is_obs(tr, i)]
        m = max(0, len(obs) - keep); m = (m // P) * P
        seq.append(T.ctx(tr, ntok, a, set(obs[:m])))
    return seq

def old(tr, a, keep):
    obs = [i for i in range(a) if T.is_obs(tr, i)]
    return set(obs[:-keep]) if len(obs) > keep else set()

def batch_seq(tr, ntok, theta, keep):
    seq = []; el = set()
    for a in T.requests(tr):
        e = old(tr, a, keep) - el
        if e and sum(ntok[i] for i in e) >= theta: el |= e
        seq.append(T.ctx(tr, ntok, a, el))
    return seq

def horizon_seq(tr, ntok, keep, w=W, r=R):  # round-1 rule.py rule, keep as a parameter
    seq = []; el = set()
    for j, a in enumerate(T.requests(tr)):
        e = old(tr, a, keep) - el
        if e:
            S = sum(ntok[i] for i in e); f = min(e)
            X = sum(ntok[i] for i in range(f, a) if i not in e) + T.PH * len(e)
            if r * S * max(j, 1) >= (w - r) * X: el |= e
        seq.append(T.ctx(tr, ntok, a, el))
    return seq

def opt_cost(tr, ntok, keep):
    k0 = T.KEEP; T.KEEP = keep
    try: return T.offline_opt(tr, ntok, W, R)
    finally: T.KEEP = k0

def bp_bill(seq, blocks, two, maxlb=20):
    """Anthropic-style billing with explicit breakpoints. entries = prefixes (tuples of segment keys)
    written at breakpoints of earlier requests. A breakpoint at segment boundary b finds the longest
    entry among boundaries b, b-1, ... within maxlb blocks. Unmatched tokens are written at W."""
    entries = set(); cost = 0.0; prevkeys = []
    for s in seq:
        keys = [k for k, _ in s]; cum = [0]
        for _, t in s: cum.append(cum[-1] + t)
        bps = [1, len(s)]                                   # tools breakpoint + end of request
        if two:
            # (i) a stable breakpoint just after the last placeholder (where the next clear will start), so an
            # entry exists there; (ii) when the client edited the prompt, a breakpoint at the first edited
            # position, which hits that entry however far back it is. 4 breakpoints = Anthropic's maximum.
            ph = [i for i, k in enumerate(keys) if isinstance(k, tuple) and k[0] == "ph"]
            bps.append(ph[-1] + 1 if ph else 1)
            f = next((i for i, (x, y) in enumerate(zip(prevkeys, keys)) if x != y), None)
            if f is not None and f >= 1: bps.append(f)
        hit = 0
        for b in bps:
            nb = 0; i = b
            while i >= 1 and nb <= maxlb:
                if tuple(keys[:i]) in entries: hit = max(hit, cum[i]); break
                nb += blocks.get(keys[i - 1], 1); i -= 1
        cost += R * hit + W * (cum[-1] - hit)
        for b in bps: entries.add(tuple(keys[:b]))
        prevkeys = keys
    return cost

# Llama-3-70B prefill compute per token: 2*N_params + attention 4*n_layers*d_model*context (QK^T and AV).
NP, NL, DM, DKV = 70.6e9, 80, 8192, 1024
KVB = 2 * NL * DKV * 2          # bytes of K+V per token, BF16
PEAK, MFU, HBM, HBMU = 989e12, 0.45, 3.35e12, 0.7   # H100 dense BF16, assumed utilisation; HBM bandwidth
def flops(seq, splice=False, outs=None, acc=None, key=None, refresh=0):
    """Own-stack compute: every token not served from KV is prefilled; a splice also re-rotates the K of
    downstream cached tokens (about 6 flops per K element per layer, counted, though it is memory-bound)."""
    tot = 0.0; prev = []; nspl = 0
    for s in seq:
        L = sum(t for _, t in s)
        if splice:
            pk = set(k for k, _ in prev); miss = sum(t for k, t in s if k not in pk)
            # downstream cached tokens after the first changed position get re-rotated
            first = next((i for i, (x, y) in enumerate(zip(prev, s)) if x != y), min(len(prev), len(s)))
            rot = sum(t for k, t in s[first:] if k in pk)
            if refresh and first < len(prev):          # this request spliced
                nspl += 1
                if nspl % refresh == 0:   # bounded staleness: re-prefill everything after the first placeholder
                    ph = next((i for i, (k, _) in enumerate(s) if isinstance(k, tuple) and k[0] == "ph"), len(s))
                    miss = L - sum(t for _, t in s[:ph]); rot = 0
            tot += rot * NL * DKV * 6
        else:
            miss = L - T.lcp(prev, s)
        ctx0 = L - miss
        tot += miss * 2 * NP + 4 * NL * DM * (miss * ctx0 + miss * miss / 2)
        if outs is not None:   # decode: each output token reads the whole context's KV once (BF16, 320 KB/token)
            o = outs.pop(0); acc[key + ":kvread"] = acc.get(key + ":kvread", 0) + o * (L + o / 2) * KVB
            acc[key + ":ctxtok"] = acc.get(key + ":ctxtok", 0) + L
        prev = s
    return tot

def main(path):
    Tr = T.load(path); acc = {}
    def add(k, v): acc[k] = acc.get(k, 0) + v
    for tr in Tr:
        ntok = [T.tok(s) for s in tr["text"]]; A = T.requests(tr)
        blocks = {"tools": 1}
        for i, r in enumerate(tr["role"]): blocks[(i, 0)] = 2 if r == "assistant" else 1
        add("req", len(A))
        fam = {"append": T.policy_seq(tr, ntok, "append", W, R), "sliding": T.policy_seq(tr, ntok, "sliding", W, R)}
        for keep in (3, 5, 7, 10):
            for P in (5, 10, 20): fam[f"polling{P}/keep{keep}"] = polling_seq(tr, ntok, P, keep)
            for th in (3000, 5000, 10000): fam[f"batch{th//1000}k/keep{keep}"] = batch_seq(tr, ntok, th, keep)
            fam[f"horizon/keep{keep}"] = horizon_seq(tr, ntok, keep)
            add(f"opt/keep{keep}:c", opt_cost(tr, ntok, keep))
        for k, s in fam.items():
            c, h, t = T.bill(s, W, R); add(k + ":c", c); add(k + ":t", t); add(k + ":h", h)
        for k in ("append", "sliding", "polling10/keep5", "batch5k/keep5", "horizon/keep5"):
            add(k + ":1bp", bp_bill(fam[k], blocks, False)); add(k + ":2bp", bp_bill(fam[k], blocks, True))
        outs = [ntok[a] for a in A]
        for k in ("append", "sliding", "polling10/keep5", "batch5k/keep5", "horizon/keep5"):
            add(k + ":fl", flops(fam[k], outs=list(outs), acc=acc, key=k))
        add("sliding+splice:fl", flops(fam["sliding"], splice=True, outs=list(outs), acc=acc, key="sliding+splice"))
        add("polling10/keep5+splice:fl", flops(fam["polling10/keep5"], splice=True, outs=list(outs), acc=acc, key="polling10/keep5+splice"))
        for K in (4, 8):
            add(f"sliding+splice/refresh{K}:fl", flops(fam["sliding"], splice=True, outs=list(outs), acc=acc, key=f"sliding+splice/refresh{K}", refresh=K))
    ap, sl, n = acc["append:c"], acc["sliding:c"], acc["req"]
    print(f"traces={len(Tr)} requests={n}")
    print("\n(a) Anthropic breakpoint model (20-block lookback). Cost vs exact-LCP billing of the same policy:")
    for k in ("append", "sliding", "polling10/keep5", "batch5k/keep5", "horizon/keep5"):
        e = acc[k + ":c"]; b1 = acc[k + ":1bp"]; b2 = acc[k + ":2bp"]
        print(f"  {k:17s} exact {e:12,.0f} | 1bp {b1:12,.0f} ({b1/e-1:+.1%}, vs append-1bp {b1/acc['append:1bp']-1:+.1%})"
              f" | 2bp {b2:12,.0f} ({b2/e-1:+.1%}, vs append-2bp {b2/acc['append:2bp']-1:+.1%})")
    print("\n(b) Cost vs context, Anthropic prices, exact-LCP billing (2bp makes this achievable, see (a)):")
    print(f"  {'policy':20s} {'vs append':>9s} {'vs sliding':>10s} {'mean prompt':>11s} {'tok hit':>7s}")
    rows = []
    for k in [k[:-2] for k in acc if k.endswith(":c")]:
        c = acc[k + ":c"]; t = acc.get(k + ":t"); h = acc.get(k + ":h")
        rows.append((t / n if t else float("nan"), k, c, h / t if t else float("nan")))
    for mp, k, c, hr in sorted(rows, key=lambda r: (r[0] != r[0], r[0])):
        print(f"  {k:20s} {c/ap-1:+9.1%} {c/sl-1:+10.1%} {mp:11,.0f} {hr:7.3f}")
    print("\n(c) Own stack, Llama-3-70B shape, BF16 KV, H100 (989 TFLOP/s at 45% MFU, 3.35 TB/s at 70%), all 200 traces.")
    print("    prefill = compute for every token not served from KV (+ splice key re-rotation); decode KV = bytes of")
    print("    context KV read per output token (weight reads are the same for every policy and left out).")
    print(f"  {'policy':24s} {'prefill EFLOP':>13s} {'vs app':>7s} {'decode KV PB':>12s} {'vs app':>7s} {'GPU-h':>7s} {'vs app':>7s} {'KV-resident':>11s}")
    def gh(k): return (acc[k+':fl'] / (PEAK * MFU) + acc[k+':kvread'] / (HBM * HBMU)) / 3600
    for k in ("append", "sliding", "sliding+splice", "sliding+splice/refresh4", "sliding+splice/refresh8", "polling10/keep5", "polling10/keep5+splice", "batch5k/keep5", "horizon/keep5"):
        f, kv = acc[k+':fl'], acc[k+':kvread']
        print(f"  {k:24s} {f/1e18:13.2f} {f/acc['append:fl']-1:+7.1%} {kv/1e15:12.2f} {kv/acc['append:kvread']-1:+7.1%} {gh(k):7.2f} {gh(k)/gh('append')-1:+7.1%} {acc[k+':ctxtok']/acc['append:ctxtok']:10.2f}x")
main(sys.argv[1])
