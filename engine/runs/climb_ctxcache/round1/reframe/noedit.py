# Edit-free workload (edits only near the end => errata useless, check0): what batching and read price give alone.
import levers, statistics as st
def run(R, **kw):
    levers.R=R; r=[levers.session(s,edit_every=10**9,**kw) for s in range(20)]
    return st.mean(x[0] for x in r)
b=run(0.10)
for R in (0.10,0.03):
    for name,kw in (("k=1",{}),("k=1.5",dict(ks=(1,2))),("k=2",dict(k=2))):
        v=run(R,**kw); print(f"no edits R={R:.2f} {name:6} input {v:9,.0f} ({v/b-1:+.1%})")
for calls in (20,50,100):
    levers.R=0.10; a=levers.session(0,edit_every=10**9,calls=calls)[0]; c=levers.session(0,edit_every=10**9,calls=calls,ks=(1,2))[0]
    print(f"calls={calls}: k=1.5 saves {1-c/a:.1%} of input")
