import fan, diag2, numpy as np, collections
d=fan.build()
xs,an,g,hits=diag2.trace_info(d['receiver'],d['mirrors'],NX=400,NA=9)
NX=400
# per first-mirror stats: count, success
st=collections.defaultdict(lambda:[0,0]); paths=collections.Counter()
for r,h in enumerate(hits):
    f=h[0] if h else None; st[f][0]+=1; st[f][1]+=g.ravel()[r]
    if not g.ravel()[r] and xs[r%NX]>0: paths[tuple(h[:4])]+=1
nm=len(d['mirrors'])//2
for k in sorted(st, key=lambda z: (z is None, z if z is not None else 0)):
    if k is None or k<nm: print(k, st[k])
print(paths.most_common(25))
