# Re-run of A's 50-turn replay (calc.py 1b), changing only one thing: tokens appended
# since the previous request are billed as cache writes, not as hits.
import random
def session(policy, fix, seed=0, turns=50, sys_tok=10_000, tool=2_000, out=300, edit_every=5, edit_tok=1_000, w=1.25, r=0.10):
    rng = random.Random(seed); ctx = [sys_tok]; prev_len = 0; cost = hit = tot = 0
    for t in range(turns):
        div = prev_len if fix else sum(ctx)
        if t and t % edit_every == 0:
            k = rng.randrange(1, len(ctx))
            if policy == "inplace": div = min(div, sum(ctx[:k]))
            else: ctx.append(edit_tok)
        L = sum(ctx); c = min(div, L)
        cost += r*c + w*(L-c); hit += c; tot += L
        prev_len = L; ctx.append(tool+out)
    return hit/tot, cost
for fix in (False, True):
    for et in (1000, 2300):
        a = session("inplace", fix, edit_tok=et); b = session("erratum", fix, edit_tok=et)
        print(f"fix={fix} erratum={et}: inplace hit={a[0]:.4f} cost={a[1]:,.0f} | errata hit={b[0]:.4f} cost={b[1]:,.0f} | saving={1-b[1]/a[1]:.1%}")
