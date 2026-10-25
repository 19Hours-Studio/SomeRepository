# Synthetic agent session with CORRECTED billing (check0/replay_fixed.py): new tokens = 1.25x write,
# cached prefix = 0.1x read every request, output = 5x (Anthropic Sonnet-style ratios).
# Same workload as check0: 10k system prompt, 50 tool calls, 2000-tok tool result + 300-tok assistant
# output per call, an earlier entry (uniform position) changes every 5th call.
# Levers: errata (append-only), k-way turn batching (k tool calls issued in parallel per request),
# digest side-calls (tool result read once in a short side request; main thread keeps a d-token digest).
import random, statistics as st
W, R, O, U = 1.25, 0.10, 5.0, 1.0
def session(seed, policy="inplace", k=1, digest=None, calls=50, sys_tok=10_000, tool=2_000, out=300,
            edit_every=5, e_tok=1_000, side_prefix=10_000, ks=None):
    # ks: optional cycle of batch sizes, e.g. (1,2) = 1.5 calls/request on average
    rng=random.Random(seed); ctx=[sys_tok]; cached=0; inp=outp=0.0; hit=tot=0; c=0
    q=0
    while c < calls:
        if ks: k=ks[q % len(ks)]; q+=1
        div=cached
        for j in range(k):                       # edits that fall inside this batch of calls
            if c+j and (c+j) % edit_every == 0 and c+j < calls:
                n=len(ctx); kk=rng.randrange(1,n)
                if policy=="inplace": div=min(div, sum(ctx[:kk]))
                else: ctx.append(e_tok)
        L=sum(ctx); h=min(div,L); inp+=R*h+W*(L-h); hit+=h; tot+=L; cached=L
        nb=min(k, calls-c)
        outp+=O*out*nb                            # assistant output (tool calls) for this request
        for j in range(nb):
            if digest:                            # side call: short shared prefix (cached) + raw tool result, read once
                inp+=R*side_prefix+U*tool; outp+=O*digest
                ctx.append(digest+out)
            else: ctx.append(tool+out)
        c+=nb
    final=sum(ctx)
    return inp, outp, hit/tot, final
def avg(**kw):
    r=[session(s,**kw) for s in range(200)]
    return [st.mean(x[i] for x in r) for i in range(4)]
if __name__=="__main__":
    base=avg()
    rows=[("in-place edits, 1 call/request (current practice)",{}),
          ("errata (diff, 1000 tok)",dict(policy="erratum")),
          ("errata (full, 2300 tok)",dict(policy="erratum",e_tok=2300)),
          ("no edits at all (floor for any hit-rate scheme)",dict(edit_every=10**9)),
          ("errata + 2 calls/request",dict(policy="erratum",k=2)),
          ("errata + 3 calls/request",dict(policy="erratum",k=3)),
          ("errata + digest 300 tok",dict(policy="erratum",digest=300)),
          ("errata + digest 300 + 2 calls/request",dict(policy="erratum",digest=300,k=2)),
          ("errata(full) + digest 300 + 2 calls/request",dict(policy="erratum",e_tok=2300,digest=300,k=2))]
    bi,bo=base[0],base[1]
    print(f"{'policy':48} {'input':>9} {'output':>8} {'in+out':>9} {'d_input':>8} {'d_total':>8} {'tok_hit':>7} {'final_ctx':>9}")
    for name,kw in rows:
        i,o,hr,f=avg(**kw)
        print(f"{name:48} {i:9,.0f} {o:8,.0f} {i+o:9,.0f} {i/bi-1:8.1%} {(i+o)/(bi+bo)-1:8.1%} {hr:7.3f} {f:9,.0f}")
