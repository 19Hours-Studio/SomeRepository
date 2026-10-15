import numpy as np
def cascade(N, k, a, feed=1.0):
    # stages 1..N ; forward fraction a goes to i+1 (N -> concentrate), back (1-a) to i-1 (1 -> tailings)
    # unknown stage feeds x_i ; x_i = feed*delta(i,k) + a*x_{i-1} + (1-a)*x_{i+1}
    A = np.zeros((N,N)); b = np.zeros(N)
    for i in range(N):
        A[i,i] = 1.0
        if i-1 >= 0: A[i,i-1] -= a
        if i+1 < N: A[i,i+1] -= (1-a)
    b[k-1] = feed
    x = np.linalg.solve(A,b)
    conc = a*x[-1]; tail=(1-a)*x[0]
    return x, conc, tail
g_ore = 1.2; g_sp = 8.03  # Li2O % in ore and in pure spodumene
fv = g_ore/g_sp  # mass fraction of spodumene in ore
fw = 1-fv
print("spodumene mass fraction in ore", round(fv,4))
best=[]
for N in range(3,13):
    for k in range(1,N+1):
        xv, cv, tv = cascade(N,k,0.85,fv)
        xw, cw, tw = cascade(N,k,0.45,fw)
        rec = cv/fv; mass = cv+cw; grade = cv*g_sp/mass
        circ = (xv.sum()+xw.sum())  # total stage throughput / fresh feed
        best.append((N,k,rec,grade,mass,circ))
for r in best:
    if r[0]==9:
        print("N=%d feed@%d rec=%.3f grade=%.2f%% mass=%.3f stage-throughput/feed=%.2f"%r)
# find closest to 82% / 6.1%
cand = sorted(best, key=lambda r: (r[2]-0.82)**2*100+(r[3]-6.1)**2)
print("closest:", ["N=%d k=%d rec=%.3f grade=%.2f mass=%.3f circ=%.2f"%c for c in cand[:5]])
# simple non-recycled series of 9 stages
rv=0.85**9; rw=0.45**9
print("9 stages in series, no recycle: rec=%.4f grade=%.2f"%(rv, rv*fv*g_sp/(rv*fv+rw*fw)))
print("--- sensitivity of 9-stage cascade (feed at stage 1) to per-stage split")
for a,b in ((0.85,0.45),(0.85,0.55),(0.80,0.50),(0.75,0.55),(0.70,0.50),(0.85,0.65)):
    xv,cv,tv=cascade(9,1,a,fv); xw,cw,tw=cascade(9,1,b,fw)
    print("valuable fwd %.2f waste fwd %.2f: rec %.3f grade %.2f%% Li2O mass %.3f throughput %.1fx"%(a,b,cv/fv,cv*g_sp/(cv+cw),cv+cw,xv.sum()+xw.sum()))
