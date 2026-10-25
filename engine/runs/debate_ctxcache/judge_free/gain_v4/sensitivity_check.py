import sys, io, contextlib
sys.path.insert(0, "/home/user/SomeRepository/engine/runs/debate_ctxcache/round4")
sys.argv=[sys.argv[0], sys.argv[1]]
with contextlib.redirect_stdout(io.StringIO()):
    import trace5 as T, rag5 as G
TR=T.TR; A=sum(T.run(t,None,1)[0] for t,_ in TR)
P20=sum(T.run(t,5,20)[0] for t,_ in TR)
for k in (0,32,128,512,2000):
    c=sum(T.run(t,5,1,"span",k=k)[0] for t,_ in TR)
    print(f"span n=5 k={k}: vs append {c/A-1:+.1%}  vs poll20 {c/P20-1:+.1%}")
# output share & what share of append-only bill is reads
out=sum(T.O*s["out"] for t,_ in TR for s in t); print("output share", out/A)
# RAG sensitivity
for pool,k,drift in ((60,10,0.1),(60,10,0.3),(200,10,0.3),(60,10,0.6),(1000,10,0.3)):
    r={l:G.rag(l,drift=drift,pool=pool,k=k)[0] for l in ("sysctx","tail","tail_span")}
    c12=G.rag("tail_cap",drift=drift,pool=pool,cap=12)[0]
    print(pool,k,drift,{l:f"{v/r['tail']-1:+.1%}" for l,v in r.items()}, "cap12 vs tail", f"{c12/r['tail']-1:+.1%}",
          "span kb=256 vs tail", f"{G.rag('tail_span',drift=drift,pool=pool,kb=256)[0]/r['tail']-1:+.1%}")
