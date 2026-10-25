import time, model9 as e9
q=e9.q
t=time.time()
A=e9.env(q.C128, split="tp", gmax=14, s_static=0, labels=("0.55V wt",))
print("repro C8:", e9.e8.fmt(A), time.time()-t); print(e9.detail(A[1000][1]))
for sp,o,l,ss in (("tp",1,64,100),("ep",1,64,100),("ep",0.75,48,100),("ep",0.6,48,100),("ep",0.5,32,100)):
    t=time.time(); A=e9.env(q.C128, split=sp, omega=o, lanes=l, s_static=ss, labels=("0.55V wt",))
    print(sp,o,l,ss, e9.e8.fmt(A), f"{time.time()-t:.0f}s"); print("  ",e9.detail(A[1000][1])); print("  ",e9.detail(A[2000][1]))
