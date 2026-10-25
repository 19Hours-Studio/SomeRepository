# Round-4 replay of the REAL traces (441 mini-SWE-agent v2.4.2 + gemini-3-5-flash, 19,514 requests).
# A. corrected append-only headline: back-references only for runs of >=3 / >=5 re-shown lines (critic3 #2), strict
#    batching scaled by its hand-checked precision (critic3 #1), and the output-kept sensitivity (critic3 "undersold").
# B. NEW regime on real token streams: a real context-mutating harness policy, SWE-agent's LastNObservations
#    (classic n=5, polling=1; its docs say it "breaks prompt caching"), vs its own polling workaround, vs append-only,
#    vs provider-side replace_span (elision billed as a hit + 32 boundary tokens recomputed per hole).
# Prices in units of base input: read 0.1, 5m write 1.25, output 5 (Anthropic).
# Usage: python3 -I trace5.py <trajs_dir>
import sys, glob, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import trace4 as T
R, W, O = T.R, T.W, T.O
F = sorted(glob.glob(sys.argv[1] + "/*.json")); TR = [T.load(f) for f in F]
base = sum(T.cost(t) for t, _ in TR); nreq = sum(len(t) for t, _ in TR)

def dup_runs(steps, kmin):                      # critic3 check3.py rule: only runs of >= kmin re-shown lines count
    shown = set(); saved = {}
    for j, s in enumerate(steps):
        lines = s["obs"].split("\n"); toks = [len(l) / 3.6 + 0.5 for l in lines]; net = 0; i = 0
        flags = [len(l.strip()) >= 20 and l in shown for l in lines]
        while i < len(lines):
            if flags[i]:
                k = i
                while k < len(lines) and flags[k]: k += 1
                if k - i >= kmin: net += max(0, sum(toks[i:k]) - 12)
                i = k
            else: i += 1
        for l in lines:
            if len(l.strip()) >= 20: shown.add(l)
        if net > 0 and j + 1 < len(steps): saved[j + 1] = int(net)
    return saved

print("== A. append-only agent: corrected headline ==")
drops = [T.groups(t, task, 4, False, True) for t, task in TR]
b_only = sum(T.cost(t, d) for (t, _), d in zip(TR, drops)) / base - 1
for kmin in (3, 5):
    sv = [dup_runs(t, kmin) for t, _ in TR]
    br = sum(T.cost(t, saved_tok=s) for (t, _), s in zip(TR, sv)) / base - 1
    for keep in (1.0, 0.75):
        comb = sum(T.cost([dict(x, out=x["out"] * keep) if j in d else x for j, x in enumerate(t)], d, s)
                   for (t, _), d, s in zip(TR, drops, sv)) / base - 1
        bat = comb - br                      # batching part on top of back-references
        print(f"backrefs runs>={kmin}: {br:+.1%}; + strict cap-4 batching keeping {keep:.0%} of merged output: {comb:+.1%};"
              f" batching part scaled by precision 0.77..0.90 -> {br + 0.77*bat:+.1%} .. {br + 0.90*bat:+.1%}")
print(f"(batching alone, 100% output kept: {b_only:+.1%})")

print("\n== B. real token streams under a context-MUTATING policy (SWE-agent LastNObservations) ==")
def segs_of(t):
    n = len(t)
    obs = [min(len(s["obs"]) / 3.6 + 0.5, max(t[i + 1]["L"] - s["L"], 0)) if i + 1 < n else 0 for i, s in enumerate(t)]
    oth = [max(t[i + 1]["L"] - s["L"], 0) - obs[i] if i + 1 < n else 0 for i, s in enumerate(t)]
    return obs, oth
def run(t, n_keep, poll, mode="prefix", ph=10, k=32, drop=frozenset()):
    """mode prefix: provider prefix cache (hit up to the first changed block). mode span: provider replace_span —
    an elided observation is replaced in place, billed as a hit, k boundary tokens after each new hole recomputed."""
    obs, oth = segs_of(t); upto = 0; prev = None; c = 0.0; vis = 0.0; Lsum = 0.0
    for j, s in enumerate(t):
        new_upto = max(upto, j - n_keep) if (n_keep is not None and j % poll == 0) else upto
        segs = [("p", t[0]["L"])]
        for i in range(j):
            segs.append((("a", i), oth[i])); m = i < new_upto
            segs.append((("o", i, m), ph if m else obs[i]))
        L = sum(x for _, x in segs); Lsum += L
        if mode == "prefix":
            hit = 0
            if prev:
                for a, b in zip(segs, prev):
                    if a != b: break
                    hit += a[1]
        else:                                   # span: blocks already in the cache are hits; new placeholders are written
            pk = set(key for key, _ in prev) if prev else set()
            holes = (new_upto - upto) if prev else 0
            hit = max(0.0, sum(x for key, x in segs if key in pk) - k * holes)
        if j in drop: c += O * s["out"]; Lsum -= L; continue   # merged into the previous turn: no request sent
        c += R * hit + W * (L - hit) + O * s["out"]; prev = segs; upto = new_upto
    return c, Lsum / max(1, len(t) - len(drop))
ap = [run(t, None, 1) for t, _ in TR]; A = sum(c for c, _ in ap); Lap = sum(l * len(t) for (c, l), (t, _) in zip(ap, TR)) / nreq
print(f"append-only (no elision): {A:,.0f} units (trace4 base {base:,.0f}), mean context {Lap:,.0f} tokens")
res = {}
for n_keep, poll, mode in ((5, 1, "prefix"), (5, 2, "prefix"), (5, 5, "prefix"), (5, 10, "prefix"), (5, 20, "prefix"),
                           (10, 1, "prefix"), (10, 10, "prefix"), (10, 20, "prefix"), (5, 1, "span"), (10, 1, "span"), (15, 1, "span"), (20, 1, "span"), (5, 5, "span")):
    r = [run(t, n_keep, poll, mode) for t, _ in TR]; c = sum(x for x, _ in r)
    L = sum(l * len(t) for (x, l), (t, _) in zip(r, TR)) / nreq; res[(n_keep, poll, mode)] = (c, L)
    b = res.get((n_keep, 1, "prefix"))
    print(f"LastN n={n_keep:2d} polling={poll:2d} {mode:6s}: {c:12,.0f} units  vs append-only {c/A-1:+6.1%}"
          + (f"  vs same-n polling=1 {c/b[0]-1:+6.1%}" if b else " " * 28) + f"  mean context {L:7,.0f}")

print("\nfrontier: span ops vs the cheapest client polling setting with >= the same mean context")
cl = [(c, L, k) for k, (c, L) in res.items() if k[2] == "prefix"]
for k, (c, L) in res.items():
    if k[2] != "span": continue
    ok = [x for x in cl if x[1] >= L * 0.995]
    if ok:
        b = min(ok); print(f"span n={k[0]} p={k[1]} ({c:,.0f}, ctx {L:,.0f}) vs client n={b[2][0]} p={b[2][1]} ({b[0]:,.0f}, ctx {b[1]:,.0f}): {c/b[0]-1:+.1%}")
    else: print(f"span n={k[0]}: ctx {L:,.0f} above every client polling point; vs append-only (ctx {Lap:,.0f}) {c/A-1:+.1%}")

print("\ncombined with strict cap-4 batching (all output kept; batching part to be scaled by precision 0.77..0.90)")
for n_keep, poll, mode in ((None, 1, "prefix"), (5, 20, "prefix"), (5, 1, "span"), (10, 1, "span")):
    c = sum(run(t, n_keep, poll, mode, drop=d)[0] for (t, _), d in zip(TR, drops))
    c0 = sum(run(t, n_keep, poll, mode)[0] for t, _ in TR)
    print(f"n={n_keep} p={poll} {mode}: {c/A-1:+.1%} vs append-only (without batching {c0/A-1:+.1%});"
          f" precision-scaled {(c0 + 0.77*(c-c0))/A-1:+.1%} .. {(c0 + 0.90*(c-c0))/A-1:+.1%}")
