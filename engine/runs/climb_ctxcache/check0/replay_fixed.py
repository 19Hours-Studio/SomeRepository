# Re-check of calc.py section 1b. Fixes: (a) tokens appended last turn (tool result + assistant output)
# are NEW input this turn -> cache write, not a read (calc.py counted them as hits);
# (b) erratum size sweep (calc.py uses 1000 tok errata to replace a 2300 tok entry);
# (c) edit-position distribution; (d) ski-rental with correct incremental rewrite cost.
import random, statistics as st
W, R = 1.25, 0.10
def session(policy, seed, turns=50, sys_tok=10_000, tool=2_000, out=300, edit_every=5,
            edit_tok=1_000, fix_new=True, pos="uniform", ski=False):
    rng = random.Random(seed); ctx=[sys_tok]; cached_upto=0; cost=hit=tot=0; debt=0.0; errata=[]
    for t in range(turns):
        L_prev = sum(ctx)
        div = cached_upto if fix_new else L_prev
        if t and t % edit_every == 0:
            n=len(ctx)
            k = rng.randrange(1,n) if pos=="uniform" else max(1, n-1-int(rng.expovariate(1/2)))  # recent: mean 2 entries back
            if policy=="inplace":
                div=min(div,sum(ctx[:k]))
            else:
                ctx.append(edit_tok); debt+=R*edit_tok
                if ski and debt >= (W-R)*(sum(ctx)-sum(ctx[:k])):
                    div=min(div,sum(ctx[:k])); debt=0
        L=sum(ctx); c=min(div,L)
        cost+=R*c+W*(L-c); hit+=c; tot+=L
        cached_upto=L          # whole request is cached after this turn
        ctx.append(tool+out)
    return hit/tot, cost
def avg(pol, **kw):
    r=[session(pol,s,**kw) for s in range(200)]
    return st.mean(x[0] for x in r), st.mean(x[1] for x in r)
print("seed0 reproduce (bug kept):", session("inplace",0,fix_new=False), session("erratum",0,fix_new=False))
for fix in (False, True):
  for pos in ("uniform","recent"):
    for e in (1000, 2300):
        a=avg("inplace",fix_new=fix,pos=pos); b=avg("erratum",fix_new=fix,pos=pos,edit_tok=e)
        print(f"fix_new={fix!s:5} pos={pos:7} e={e}: inplace hit={a[0]:.4f} cost={a[1]:,.0f} | erratum hit={b[0]:.4f} cost={b[1]:,.0f} | saving={1-b[1]/a[1]:.1%}")
# floor: no edits at all (pure append) under fixed billing
print("no-edit floor:", avg("inplace",edit_every=10**9))
# edit frequency sweep, fixed billing, uniform, e=2300
for ee in (1,2,5,10):
    a=avg("inplace",edit_every=ee); b=avg("erratum",edit_every=ee,edit_tok=2300)
    print(f"edit_every={ee}: saving={1-b[1]/a[1]:.1%}  ctx growth erratum vs inplace=+{(50//ee)*2300} tok")
