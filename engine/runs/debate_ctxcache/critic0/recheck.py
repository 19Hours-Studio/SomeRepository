# Re-check of baseline calc.py replay. Fixes: (a) tokens appended since the last request
# (new tool output + previous assistant output, and the system prompt on turn 0) are cache
# WRITES, not reads; (b) erratum size is a parameter (a changed tool output usually has to be
# restated in full = 2000); (c) erratum "rent" accrues every turn it is re-read, so ski-rental
# can actually fire; (d) a fair baseline "append-reread" = what agents already do.
import random
P = dict(w=1.25, r=0.10)
def session(policy, seed=0, turns=50, sys_tok=10_000, tool=2_000, out=300, edit_every=5,
            edit_tok=1_000, fixed=False, p=P, window=None):
    rng = random.Random(seed); ctx = [sys_tok]; prev_len = 0 if fixed else sys_tok
    cost = hit = tot = 0; errata = []  # list of (k, size)
    rewrites = 0
    for t in range(turns):
        div = prev_len
        if t and t % edit_every == 0:
            k = rng.randrange(1, len(ctx))
            if policy == "inplace":
                div = min(div, sum(ctx[:k]))
            else:
                ctx.append(edit_tok); errata.append((k, edit_tok))
        if policy == "erratum+ski" and errata:
            # rent paid so far per erratum vs buy = (w - r) * suffix from earliest stale segment
            rent = sum(p["r"] * s for _, s in errata) * 1  # per-turn rent
            ski_debt = getattr(session, "_d", 0) + rent; session._d = ski_debt
            kmin = min(k for k, _ in errata)
            buy = (p["w"] - p["r"]) * (sum(ctx) - sum(ctx[:kmin]))
            if ski_debt >= buy:
                for _k, s in errata: ctx.remove(s) if s in ctx[-len(errata)-1:] else None
                errata = []; session._d = 0; div = min(div, sum(ctx[:kmin])); rewrites += 1
        L = sum(ctx); cached = min(div, L)
        if not fixed: cached = min(div, L)  # original: div included tokens never sent before
        cost += p["r"] * cached + p["w"] * (L - cached); hit += cached; tot += L
        ctx.append(tool + out); prev_len = L if fixed else sum(ctx)
    session._d = 0
    return hit / tot, cost, L, rewrites

print("policy           fixed  edit_tok  hit     cost       final_ctx  rewrites")
for fixed in (False, True):
    for et in (1000, 2000):
        for pol in ("inplace", "erratum", "erratum+ski"):
            h, c, L, rw = session(pol, fixed=fixed, edit_tok=et)
            print(f"{pol:15s} {str(fixed):6s} {et:6d}  {h:.4f}  {c:9,.0f}  {L:8,d}  {rw}")
# cost in "units": what fraction of billed input is the unavoidable new-token write?
h, c, L, _ = session("inplace", fixed=True)
new = 10_000 + 49 * 2300
print(f"\nunavoidable writes alone (fixed): {1.25*new:,.0f} units")
# seed sensitivity of the -X% claim
import statistics
for et in (1000, 2000):
    d = []
    for s in range(200):
        a = session("inplace", seed=s, fixed=True, edit_tok=et)[1]
        b = session("erratum", seed=s, fixed=True, edit_tok=et)[1]
        d.append(1 - b / a)
    print(f"edit_tok={et}: erratum saving vs inplace over 200 seeds: mean {statistics.mean(d):.3f} "
          f"min {min(d):.3f} max {max(d):.3f}")
# long session: does ski-rental ever fire / context growth
for turns in (50, 200, 500):
    for pol in ("inplace", "erratum", "erratum+ski"):
        h, c, L, rw = session(pol, fixed=True, edit_tok=2000, turns=turns)
        print(f"turns={turns:4d} {pol:12s} hit={h:.4f} cost={c:12,.0f} final_ctx={L:9,d} rewrites={rw}")
