"""Round 8 additions (run: python3 -I calc8.py; stdlib only; ~1 min). Same 42 sessions and the same bill and roofline
models as calc.py sections P-S (functions copied here so this file runs on its own).

T. Fair speculative baseline: vLLM's own suffix-decoding drafter (official Arctic Inference code, traces/c4/spec8b.py)
   and vLLM ngram, each at its best swept setting for each concurrency; the round-7 'capped' drafter is re-scored
   against it. (traces/c4/spec8.py is my own re-implementation; it under-performs the official code and is shown only
   to document that.)
U. Sparse decode attention (Quest-style top-k pages, training-free): the lever on cached-context KV reads that is
   still unused, by concurrency, alone and composed with speculation and references; HBM capacity limit on concurrency.
V. Fewer requests instead of fewer tokens: bound on batching consecutive read-only tool calls (parallel tool use).
"""
import json, os

W5, R, OUT, TOOLS = 1.25, 0.10, 5.0, 1_500
HERE = os.path.dirname(os.path.abspath(__file__))
C4 = os.path.join(HERE, "traces", "c4")
D2 = json.load(open(os.path.join(C4, "steps2.json")))
for f in ("spec8.json", "spec8b.json"):
    SD = json.load(open(os.path.join(C4, f)))
    for k, v in D2.items():
        assert len(SD[k]) == len(v["steps"])
        for s, r in zip(v["steps"], SD[k]):
            assert s["out"] == r["out"]; s.update({kk: vv for kk, vv in r.items() if kk != "out"})
SX = sorted(k for k in D2[next(iter(D2))]["steps"][0] if k.startswith("sx_"))
def section(t): print("\n" + "=" * 8, t)

# ---- copied from calc.py (P/Q): bill replay and roofline
def replay2(S, hook=None, drop=()):
    prev, reads, writes, outs = None, 0.0, 0.0, 0.0
    for i, s in enumerate(S):
        blocks = [("t", TOOLS)] + [(m[2], m[1]) for m in s["m"]]
        tot = sum(b[1] for b in blocks); l = 0
        if prev:
            while l < min(len(prev), len(blocks)) and prev[l][0] == blocks[l][0]: l += 1
        hit = sum(b[1] for b in blocks[:l]) if prev else 0
        outs += OUT * s["out"]
        if i in drop: continue   # request never sent: its new tokens are written by the next sent request
        reads += R * hit; writes += W5 * (tot - hit)
        if hook: hook(i, s, hit, tot)
        prev = blocks
    return reads, writes, outs
PF, BW, WB, ATT = 0.45 * 8 * 989e12, 0.70 * 8 * 3.35e12, 70e9, 4 * 80 * 8192
XSHARED = 0
KVB = 163_840                     # FP8 KV, Llama-3-70B geometry (80 layers x 8 KV heads x 128 x 2 x 1 B)
def decoded_credit(S, orig):
    cr = [0]
    for i in range(1, len(S)):
        a, b = S[i - 1]["m"], S[i]["m"]
        if len(b) > len(a) and [m[2] for m in b[:len(a)]] == [m[2] for m in a]:
            cr.append(sum(m[1] for m, o in zip(b[len(a):], orig[i]["m"][len(a):]) if m[3] in ("thought", "args") and m[1] == o[1]))
        else: cr.append(0)
    return cr
def kv_read(C, k, sparse, B=32):
    """tokens of KV read per sequence by one verify pass of k+1 queries at context C. sparse = None (dense) or
    (budget, union): Quest-style top-k pages in 78 of 80 layers (first 2 dense, as in Quest), page metadata = min/max
    key per 16-token page = 1/16 of the KV; union = 'shared' (the k+1 queries pick the same pages) or 'indep'.
    A prefix of XSHARED tokens common to all B sequences is read once per batch (cascade attention, vLLM V1 /
    FlashInfer), i.e. XSHARED/B per sequence -- part of the baseline; sparse selection then applies to the rest."""
    xs = min(XSHARED, C); own = C - xs
    if not sparse: return own + xs / B
    bud, un = sparse
    sel = min(own, bud * (1 if un == "shared" else k + 1))
    return xs / B + (2 * own + 78 * (sel + own / 16)) / 80
def pre_attn(n, h, psparse):
    """attention FLOPs of n new tokens over h cached + themselves (causal). psparse = budget: each 64-query block
    attends the union of its top pages, <= budget cached tokens, in 78 of 80 layers; page scoring adds
    (n/64) x (h/16) x 2 key-vector dots (negligible); new tokens attend each other densely."""
    if not psparse: return ATT * n * (h + n / 2)
    return ATT * n * ((2 * h + 78 * min(h, psparse)) / 80 + n / 2) + ATT / 2 * (n / 64) * (h / 16) * 2
def gpu(S, spec=None, cap=None, B=32, kvb=KVB, sparse=None, orig=None, psparse=None, onlydec=False):
    per = []; replay2(S, hook=lambda i, s, h, t: per.append((h, t, s)))
    cr = decoded_credit(S, orig or S)
    pre = dec = 0.0
    for j, ((h, t, s), c) in enumerate(zip(per, cr)):
        if j == 0: h = XSHARED       # fixed context shared by all sessions: already prefix-cached
        n = max(0, t - h - c); h = t - n
        pre += (2 * 70e9 * n + pre_attn(n, h, psparse)) / PF
        C = t
        for k, a in (s[spec] if spec else [(0, 0)] * s["out"]):
            if cap == "auto":       # round 7: largest draft that keeps the pass memory-bound
                kv = kv_read(C, k, sparse, B); mem = (WB / B + kvb * kv) / BW; ftok = (2 * 70e9 + ATT * (C if not sparse else min(C, kv + XSHARED))) / PF
                c_ = max(0, min(k, int(mem / ftok) - 1))
            else: c_ = min(k, cap) if cap is not None else k
            n_p = -(-(a + 1) // (c_ + 1)) if c_ < k else 1
            kv = kv_read(C, c_, sparse, B)
            mem = (WB / B + kvb * kv) / BW; ftok = (2 * 70e9 + ATT * (C if not sparse else min(C, kv + XSHARED))) / PF
            dec += n_p * max(mem, (c_ + 1) * ftok); C += a + 1
    return dec if onlydec else pre + dec
def agg(D_=None, **kw):
    D_ = D_ or D2
    return sum(gpu(v["steps"], orig=D2[k]["steps"], **kw) for k, v in D_.items())

# references (round 7, MINRUN=4, keep everything): rewritten sizes per message
DD = json.load(open(os.path.join(C4, "dedup4.json")))
DA = {}
for k, v in D2.items():
    st = []
    for s, r in zip(v["steps"], DD[k]):
        s2 = dict(s); s2["m"] = [[m[0], r["all"][j], m[2], m[3]] for j, m in enumerate(s["m"])]; st.append(s2)
    DA[k] = {"steps": st}

section("T. Speculation baseline at its best: vLLM suffix decoding (official code) and ngram, swept; round-7 drafter re-scored")
Tt = sum(s["out"] for v in D2.values() for s in v["steps"])
for key in ["pl", "pg", "sd_a1_p10", "sd_a4_p10"] + SX:
    P_ = sum(len(s[key]) for v in D2.values() for s in v["steps"]); K_ = sum(p[0] for v in D2.values() for s in v["steps"] for p in s[key])
    print(f"{key:<14}: {Tt/P_:.2f} tokens/pass, mean draft {K_/P_:.2f}")
print("(pl = vLLM ngram n<=4 k<=8; pg = round-7 drafter: ngram + earlier outputs; sd_* = my own suffix emulation; "
      "sx_* = official Arctic Inference SuffixDecodingCache, a=max_spec_factor, p=min_token_prob x100, k=num_speculative_tokens)")
BEST = {}
for B in (8, 32, 128):
    base = agg(B=B)
    rows = {}
    for c in (1, 2, 3, 4, 6, 8): rows[("pl", c)] = agg(B=B, spec="pl", cap=c)
    for key in SX:
        k_ = int(key.split("_k")[1])
        for c in sorted({2, 4, 8, k_}):
            if c <= k_: rows[(key, c)] = agg(B=B, spec=key, cap=c)
        rows[(key, "auto")] = agg(B=B, spec=key, cap="auto")
    r7 = agg(B=B, spec="pg", cap="auto")
    ng = min((r for r in rows if r[0] == "pl"), key=rows.get)
    sf = min((r for r in rows if r[0] != "pl" and r[1] != "auto"), key=rows.get)
    sa = min((r for r in rows if r[1] == "auto"), key=rows.get)
    bp = min(ng, sf, key=rows.get)
    BEST[B] = (bp, rows[bp], base)
    print(f"B={B:>3}: best ngram {ng} x{rows[ng]/base:.3f}; best suffix {sf} x{rows[sf]/base:.3f}; "
          f"suffix default (sx_a1_p10_k24) x{rows[('sx_a1_p10_k24', 24)]/base:.3f}")
    print(f"       round-7 drafter auto-capped x{r7/base:.3f} -> vs best practice x{r7/rows[bp]:.3f}; "
          f"official suffix + auto cap {sa} x{rows[sa]/base:.3f} -> vs best practice x{rows[sa]/rows[bp]:.3f}")

section("U. Sparse decode attention (Quest-style, training-free, approximate) on top of the best current practice")
MEANC = sum(s["out"] * sum(m[1] for m in s["m"]) for v in D2.values() for s in v["steps"]) / Tt + TOOLS
print(f"decode-weighted mean context {MEANC:,.0f} tok -> FP8 KV {MEANC*KVB/1e9:.1f} GB per sequence; "
      f"HBM for KV on 8xH100 ~ 530 GB -> at most {int(530e9/(MEANC*KVB))} resident sessions (refs: "
      f"{int(530e9/(MEANC*0.82*KVB))}; 4-bit: {int(530e9/(MEANC*KVB/2))})")
def bp_kw(B):
    (k, c), _, _ = BEST[B]
    return dict(spec=k, cap=c)
for B in (8, 32, 128):
    kw = bp_kw(B); bp = agg(B=B, **kw)
    out = [f"B={B:>3} vs best practice {kw['spec']},{kw['cap']} (x{BEST[B][1]/BEST[B][2]:.3f} of no-spec):"]
    for bud in (2048, 4096):
        for un in ("shared", "indep"):
            out.append(f"top-{bud} {un} x{agg(B=B, sparse=(bud, un), **kw)/bp:.3f}")
    print("  ".join(out))
    r = agg(D_=DA, B=B, **kw) / bp
    rs = agg(D_=DA, B=B, sparse=(4096, "indep"), **kw) / bp
    rs4 = agg(D_=DA, B=B, sparse=(4096, "indep"), kvb=KVB // 2, **kw) / bp
    print(f"       references x{r:.3f}; references + top-4096 (indep) x{rs:.3f}; + 4-bit KV x{rs4:.3f}")
# where the gain is large: per-step ratio by context length (B=32, best practice drafter), and long-context extrapolation
kw = bp_kw(32); bins = [(0, 16e3), (16e3, 32e3), (32e3, 64e3), (64e3, 1e9)]
acc = {bn: [0.0, 0.0, 0] for bn in bins}
def dec_only(s, B, sparse, **kw2):
    """decode GPU time of one step (prefill excluded: identical with and without sparse decode)"""
    C = TOOLS + sum(m[1] for m in s["m"]); d = 0.0
    for k_, a in s[kw2["spec"]]:
        c_ = min(k_, kw2["cap"]); n_p = -(-(a + 1) // (c_ + 1)) if c_ < k_ else 1
        kv = kv_read(C, c_, sparse, B); mem = (WB / B + KVB * kv) / BW; ftok = (2 * 70e9 + ATT * (C if not sparse else min(C, kv + XSHARED))) / PF
        d += n_p * max(mem, (c_ + 1) * ftok); C += a + 1
    return d
for v in D2.values():
    for s in v["steps"]:
        t = TOOLS + sum(m[1] for m in s["m"]); bn = next(b for b in bins if b[0] <= t < b[1])
        acc[bn][0] += dec_only(s, 32, None, **kw); acc[bn][1] += dec_only(s, 32, (4096, "indep"), **kw); acc[bn][2] += 1
print("decode time, top-4096 indep vs dense, B=32, by context: " + "; ".join(
      f"{int(b[0]/1e3)}-{int(b[1]/1e3) if b[1] < 1e8 else 'max'}k: x{x[1]/x[0]:.3f} ({x[2]} steps)" for b, x in acc.items()))
for C in (32e3, 128e3, 200e3):
    for B in (8, 32):
        # decode per pass, best-practice mean draft, accepted tokens/pass from the trace
        (k, c), _, _ = BEST[B]
        P_ = sum(len(s[k]) for v in D2.values() for s in v["steps"]); kbar = round(sum(min(p[0], c) for v in D2.values() for s in v["steps"] for p in s[k]) / P_)
        dn = max((WB / B + KVB * C) / BW, (kbar + 1) * (2 * 70e9 + ATT * C) / PF)
        kvs = kv_read(C, kbar, (4096, "indep"))
        sp = max((WB / B + KVB * kvs) / BW, (kbar + 1) * (2 * 70e9 + ATT * kvs) / PF)
        print(f"  context {int(C/1e3)}k, B={B}: decode pass x{sp/dn:.3f} with top-4096 (indep)")
# capacity-bound regime: demand fills HBM, so concurrency = resident sessions. GPU time per session vs best practice.
print("capacity-bound (enough demand to fill HBM): GPU time per session vs best practice at its own B_max")
bm0 = int(530e9 / (MEANC * KVB)); kw = bp_kw(128)
ref = agg(B=bm0, **kw)
for name, kw2, frac in [("best practice (FP8, best drafter)", dict(), 1.0),
                        ("+ references (exact info)", dict(D_=DA), 0.82),
                        ("+ references + top-4096 sparse", dict(D_=DA, sparse=(4096, "indep")), 0.82),
                        ("+ references + 4-bit KV", dict(D_=DA, kvb=KVB // 2), 0.41),
                        ("+ references + 4-bit + top-4096", dict(D_=DA, kvb=KVB // 2, sparse=(4096, "indep")), 0.41)]:
    bm = int(530e9 / (MEANC * KVB * frac))
    print(f"  {name:<34} B_max={bm:>3}  GPU time x{agg(B=bm, **kw, **kw2)/ref:.3f}")

section("V. Fewer requests: batch runs of consecutive read-only tool calls into one turn (upper bound, API bill)")
b0 = sum(sum(replay2(v["steps"])) for v in D2.values())
ro = sum(s["ro"] for v in D2.values() for s in v["steps"]); nst = sum(len(v["steps"]) for v in D2.values())
for maxrun in (2, 3, 100):
    tot = 0.0; dropped = 0
    for v in D2.values():
        S = v["steps"]; drop = set(); run = 0
        # step i's request carries the result of step i-1's action; if actions i-1 and i are both read-only, the
        # model could have emitted action i together with i-1, so request i is never sent
        for i in range(1, len(S)):
            if S[i]["ro"] and S[i - 1]["ro"] and run + 1 < maxrun: drop.add(i); run += 1
            else: run = 0
        dropped += len(drop); tot += sum(replay2(S, drop=drop))
    print(f"batch up to {maxrun if maxrun < 100 else 'any'} read-only calls per turn: {dropped/nst:.1%} of requests removed -> bill x{tot/b0:.3f}")
print(f"read-only actions: {ro/nst:.1%} of steps")
tot = 0.0
for k, v in DA.items():
    S = v["steps"]; drop = set(); run = 0
    for i in range(1, len(S)):
        if S[i]["ro"] and S[i - 1]["ro"] and run + 1 < 3: drop.add(i); run += 1
        else: run = 0
    tot += sum(replay2(S, drop=drop))
print(f"references (MINRUN=4) alone x{sum(sum(replay2(v['steps'])) for v in DA.values())/b0:.3f}; "
      f"references + batch up to 3 read-only calls x{tot/b0:.3f}")

section("W. Long-context agents: the same sessions with X extra tokens of fixed context in front (repo map, docs, memory)")
# concurrency is capped by resident KV: B = min(32, floor(530 GB / (mean context x KV bytes))); each variant gets its
# own capacity (references shrink context ~18%, 4-bit halves bytes). Best-practice drafter: official suffix, a=4, k=4.
kw = dict(spec="sx_a4_p10_k24", cap=4)
T0 = TOOLS
for X, shared in ((0, False), (50_000, False), (50_000, True), (100_000, False), (100_000, True), (170_000, True)):
    TOOLS = T0 + X; XSHARED = X if shared else 0
    mc = MEANC + X
    def bmax(frac):   # resident KV: the shared prefix once, each session's own part per session
        own = (mc - XSHARED) * KVB * frac; return max(1, min(32, int((530e9 - XSHARED * KVB * frac) / own)))
    b0_ = bmax(1.0); base = agg(B=b0_, **kw); pre_only = agg(B=b0_, **kw) - agg(B=b0_, **kw, onlydec=True)
    rows = [("top-4096 sparse decode", dict(B=b0_, sparse=(4096, "indep"))),
            ("references", dict(D_=DA, B=bmax(0.82))),
            ("references + sparse", dict(D_=DA, B=bmax(0.82), sparse=(4096, "indep"))),
            ("references + sparse + 4-bit", dict(D_=DA, B=bmax(0.41), sparse=(4096, "indep"), kvb=KVB // 2)),
            ("sparse decode + sparse prefill-vs-cache (8k)", dict(B=b0_, sparse=(4096, "indep"), psparse=8192)),
            ("references + both sparse", dict(D_=DA, B=bmax(0.82), sparse=(4096, "indep"), psparse=8192)),
            ("references + both sparse + 4-bit", dict(D_=DA, B=bmax(0.41), sparse=(4096, "indep"), psparse=8192, kvb=KVB // 2))]
    print(f"X={X//1000:>3}k {'shared across sessions' if shared else 'unique per session'} (mean ctx {mc/1e3:.0f}k, B={b0_}, prefill {pre_only/base:.0%} of GPU time; "
          f"best practice x{base/agg(B=b0_):.3f} of no-spec at this B):")
    print("    " + "\n    ".join(f"{name:<46} x{agg(**kw, **k2)/base:.3f}" for name, k2 in rows))
TOOLS = T0
print("done")
