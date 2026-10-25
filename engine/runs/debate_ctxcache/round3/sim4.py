# Round-3 synthetic checks, all with OUTPUT TOKENS PRICED (critic2 point 1). Imports round-2 sim3 unchanged.
# Out = 300 generated tokens per tool call at 5x (Anthropic) or 8x (OpenAI) base input.
import sim3 as S, statistics as st, random, inspect

def priced(pol, om=5, calls=50, **kw):
    return S.avg(pol, calls=calls, **kw)["api"] + calls * 300 * om

print("== 1. errata / batching, output priced ==")
for om in (5, 8):
    i, a, e = (priced(p, om) for p in ("inplace", "append_full", "errata"))
    print(f"out {om}x: errata vs inplace {e/i-1:+.1%}, vs append_full {e/a-1:+.1%}")
    for q2 in (0.15, 0.23, 0.3, 0.5):
        x = priced("errata", om, q2=q2)
        print(f"   measured-range batching q2={q2:.2f}: {x/e-1:+.1%} vs errata sequential")
print("   early mutable state (memory/todo block near top) handled by errata: see round2 sim3 (-53.6% unpriced)")

print("\n== 2. span ops: cost vs mean live context (critic2 method), 200 calls, output priced 5x ==")
src = inspect.getsource(S.session).replace('api += p["r"] * cached', 'LL.append(L); api += p["r"] * cached')
ns = dict(S.__dict__); exec(src.replace("def session(", "def session_i(LL, "), ns)
def mean_ctx(pol, seeds=20, **kw):
    out = []
    for s in range(seeds):
        LL = []; r = ns["session_i"](LL, pol, seed=s, calls=200, window=200_000, **kw); out.append((r["api"], st.mean(LL)))
    return st.mean(a for a, _ in out) + 200 * 300 * 5, st.mean(l for _, l in out)
grid = ((60_000, 15_000), (60_000, 40_000), (120_000, 60_000), (195_000, 100_000), (195_000, 140_000), (195_000, 170_000), (195_000, 185_000))
E = [mean_ctx("errata", trigger=t, target=g) + (t, g) for t, g in grid]
P = [mean_ctx("patch", trigger=t, target=g) + (t, g) for t, g in grid]
for c, m, t, g in E: print(f"errata {t//1000}k->{g//1000}k cost {c:11,.0f} mean ctx {m:9,.0f} cost/ctx {c/m:5.1f}")
for c, m, t, g in P: print(f"patch  {t//1000}k->{g//1000}k cost {c:11,.0f} mean ctx {m:9,.0f} cost/ctx {c/m:5.1f}")
# client's efficient frontier: lower convex hull of errata (cost, mean ctx); a client wanting >= m context picks the cheapest
# errata setting with mean ctx >= m.
def client_best(m): return min((c, mm) for c, mm, _, _ in E if mm >= m * 0.995) if any(mm >= m * 0.995 for _, mm, _, _ in E) else None
for c, m, t, g in P:
    b = client_best(m)
    print(f"patch {g//1000}k (mean {m:,.0f}): {c:,.0f}; cheapest errata with >= that context {b[0]:,.0f} (mean {b[1]:,.0f})"
          f" -> {c/b[0]-1:+.1%}" if b else f"patch {g//1000}k: no errata point with that context")
# vs errata's most cost-efficient setting (min cost/ctx), patch at >= that context
eff = min(E, key=lambda r: r[0] / r[1]); print(f"errata most efficient: {eff[2]//1000}k->{eff[3]//1000}k cost/ctx {eff[0]/eff[1]:.1f}")
for c, m, t, g in P:
    if m >= eff[1] * 0.99: print(f"   patch {g//1000}k mean {m:,.0f} cost {c:,.0f}: {c/eff[0]-1:+.1%} cost for {m/eff[1]-1:+.1%} context vs errata@{eff[3]//1000}k")

print("\n== 3. delegation, output priced, WITH edits (errata) in both arms ==")
W, Rd, O = 1.25, 0.10, 5.0
def deleg(calls=50, block=5, d=0, Ssum=500, sys=10_000, tool=2000, out=300, task=300, edit_every=5, diff=200):
    c, L = W * sys, sys; n = 0
    for _ in range(calls // block):
        own = block - d
        for k in range(own):
            n += 1; add = tool + out + (diff if n % edit_every == 0 else 0)
            c += Rd * L + W * add + O * out; L += add
        if d:
            c += Rd * L + W * task + O * task; L += task            # parent writes the task (generated)
            l = sys
            for k in range(d):
                n += 1; add = tool + out + (diff if n % edit_every == 0 else 0)
                c += Rd * l + W * add + O * out; l += add
            c += Rd * l + O * Ssum                                    # sub-agent generates the summary
            c += Rd * L + W * Ssum; L += Ssum                         # summary enters parent as new input
    return c, L
b, Lb = deleg()
for d, s in ((2, 300), (4, 500), (4, 2000)):
    x, L = deleg(d=d, Ssum=s); print(f"delegate {d}/5, summary {s}: {x/b-1:+.1%}, final parent ctx {L:,} vs {Lb:,}")

print("\n== 4. RAG/multi-turn document order: relevance-ranked (real default) vs canonical hash vs first-seen ==")
def rag(order, turns=30, k=10, size=800, pool=60, drift=0.3, sys=2000, q=200, out=300, seed=0):
    rng = random.Random(seed); rel = {d: rng.random() for d in range(pool)}; ctx_prev = []; c = 0.0; seen = []
    for t in range(turns):
        for d in rel: rel[d] = (1 - drift) * rel[d] + drift * rng.random()     # relevance drifts with each query
        top = sorted(rel, key=rel.get, reverse=True)[:k]
        if order == "relevance": docs = top
        elif order == "hash": docs = sorted(top, key=lambda d: hash((d, 7)) % 997)
        else:                                                                   # first-seen, append-only union
            for d in top:
                if d not in seen: seen.append(d)
            docs = list(seen)
        blocks = [("sys", sys)] + [(("doc", d), size) for d in docs] + [("rank", 5 * k if order == "first" else 0)] \
                 + [(("turn", j), q + out) for j in range(t)] + [(("q", t), q)]
        hit = 0
        for a, b in zip(blocks, ctx_prev):
            if a != b: break
            hit += a[1]
        L = sum(b for _, b in blocks); c += Rd * hit + W * (L - hit) + O * out; ctx_prev = blocks
    return c, L
for drift in (0.1, 0.3):
    r = {o: rag(o, drift=drift) for o in ("relevance", "hash", "first")}
    print(f"drift {drift}: " + "  ".join(f"{o} {v[0]:,.0f} (final ctx {v[1]:,})" for o, v in r.items())
          + f" -> first-seen {r['first'][0]/r['relevance'][0]-1:+.1%} vs relevance, {r['first'][0]/r['hash'][0]-1:+.1%} vs hash")
