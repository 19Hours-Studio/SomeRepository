# A's calc.py session() with one fix: tokens appended since the last request are billed as writes.
import random
def session(policy, seed=0, turns=50, sys_tok=10_000, tool=2_000, out=300, edit_every=5, edit_tok=1_000, w=1.25, r=0.10):
    rng=random.Random(seed); ctx=[sys_tok]; cost=hit=tot=0; prev=0
    for t in range(turns):
        div=prev  # only what was in the previous request is cached
        if t and t%edit_every==0:
            k=rng.randrange(1,len(ctx))
            if policy=="inplace": div=min(div,sum(ctx[:k]))
            else: ctx.append(edit_tok)
        L=sum(ctx); c=min(div,L); cost+=r*c+w*(L-c); hit+=c; tot+=L; prev=L
        ctx.append(tool+out)
    return hit/tot,cost
import statistics as st
for p in ("inplace","erratum"):
    rs=[session(p,seed=s) for s in range(200)]
    print(p, f"hit={st.mean(x[0] for x in rs):.4f} cost={st.mean(x[1] for x in rs):,.0f}")
