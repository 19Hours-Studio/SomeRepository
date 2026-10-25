# Synthetic edit replay, corrected per the check (check0/replay_fixed.py) and extended with a
# per-edit hybrid chooser: send an erratum OR rewrite in place, whichever is cheaper over the
# expected remaining horizon. Billing: new tokens each turn are 1.25x writes, cached prefix 0.1x.
import random, statistics as st
W, R = 1.25, 0.10
def session(policy, seed, turns=50, sys_tok=10_000, tool=2_000, out=300, edit_every=5,
            e=2300, pos="uniform", horizon="online"):
    rng = random.Random(seed); ctx = [sys_tok]; cached_upto = 0; cost = hit = tot = 0
    n_inplace = n_err = 0
    for t in range(turns):
        div = cached_upto
        if t and t % edit_every == 0:
            n = len(ctx)
            k = rng.randrange(1, n) if pos == "uniform" else max(1, n - 1 - int(rng.expovariate(1 / 2)))
            suffix = sum(ctx) - sum(ctx[:k])
            H = (turns - t) if horizon == "oracle" else t           # online: Lindy guess, remaining ~ elapsed
            err_cost = W * e + R * e * H
            inpl_cost = (W - R) * suffix
            choose = policy if policy != "hybrid" else ("inplace" if inpl_cost <= err_cost else "erratum")
            if choose == "inplace": div = min(div, sum(ctx[:k])); n_inplace += 1
            else: ctx.append(e); n_err += 1
        L = sum(ctx); c = min(div, L)
        cost += R * c + W * (L - c); hit += c; tot += L
        cached_upto = L; ctx.append(tool + out)
    return hit / tot, cost, sum(ctx), n_inplace, n_err
def avg(pol, **kw):
    r = [session(pol, s, **kw) for s in range(200)]
    return [st.mean(x[i] for x in r) for i in range(5)]
print("e = erratum tokens (2300 = full re-send of the 2,300-token entry; 410 = diff-style erratum, 0.177 x 2300 from diffstat.out)")
for pos in ("uniform", "recent"):
    for e in (2300, 410):
        a = avg("inplace", pos=pos); b = avg("erratum", pos=pos, e=e)
        h = avg("hybrid", pos=pos, e=e); ho = avg("hybrid", pos=pos, e=e, horizon="oracle")
        print(f"pos={pos:7} e={e:4}: inplace {a[1]:,.0f} | erratum {b[1]:,.0f} ({1-b[1]/a[1]:+.1%}) | "
              f"hybrid-online {h[1]:,.0f} ({1-h[1]/a[1]:+.1%}, vs erratum {1-h[1]/b[1]:+.1%}; {h[3]:.1f} rewrites/{h[4]:.1f} errata) | "
              f"hybrid-oracle {ho[1]:,.0f} ({1-ho[1]/a[1]:+.1%})")
print("no-edit floor (hit rate, cost):", [round(x, 4) for x in avg("inplace", edit_every=10**9)[:2]])
print("break-even turns (incremental rewrite cost (W-R)(N-p)):")
for N, p, e in [(100_000, 50_000, 500), (100_000, 90_000, 2_000)]:
    print(f"  N={N} p={p} e={e}: {((W-R)*(N-p) - W*e)/(R*e):.0f}")
