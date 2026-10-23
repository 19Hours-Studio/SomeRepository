# E8 lattice fixed-rate codebook vs scalar quantizers on unit Gaussian (post-Hadamard proxy).
import numpy as np, itertools
rng=np.random.default_rng(0)
def e8_points(rmax2):
    # E8 = D8 U (D8+1/2). enumerate norms^2 <= rmax2
    pts=[]
    r=int(np.ceil(np.sqrt(rmax2)))+1
    rngv=np.arange(-r,r+1)
    # integer part: coords in D8 (sum even)


    # use recursive enumeration with pruning
    def rec(prefix,s2,half):
        if len(prefix)==8:
            v=np.array(prefix)
            if half or (round(v.sum())%2==0):
                if not half or (round(v.sum())%2==0): pts.append(v.copy())
            return
        vals=(rngv+0.5) if half else rngv
        for x in vals:
            if s2+x*x<=rmax2+1e-9: rec(prefix+[x],s2+x*x,half)
    rec([],0,False); rec([],0,True)
    return np.array(pts,dtype=np.float32)
P10=e8_points(12.0); print("E8 pts <=12:",len(P10))


def ball(N):
    Q=P10[np.argsort((P10**2).sum(1),kind='stable')][:N]; return Q
def vq_mse(C,X,iters=0):
    # nearest neighbour, scale-optimised
    best=None
    for s in np.linspace(0.3,1.6,27):
        Cs=C*s; err=0
        for i in range(0,len(X),2000):
            x=X[i:i+2000]; d=(x**2).sum(1)[:,None]-2*x@Cs.T+(Cs**2).sum(1)[None]
            err+=d.min(1).clip(0).sum()
        m=err/X.size
        if best is None or m<best[0]: best=(m,s)
    return best
X=rng.standard_normal((4000,8)).astype(np.float32)
res={}
m2,s2=vq_mse(ball(65536),X); res['E8ball 2b (2^16)']=m2
# 3 bit: 2-bit E8 + 1-bit residual E8 (256 pts) RVQ ; 4 bit: 2b+2b RVQ
C=ball(65536)*s2
def nn(C,x):
    out=np.empty_like(x)
    for i in range(0,len(x),2000):
        xx=x[i:i+2000]; d=-2*xx@C.T+(C**2).sum(1)[None]; out[i:i+2000]=C[d.argmin(1)]
    return out
R=X-nn(C,X)
m3,_=vq_mse(ball(256),R/np.sqrt((R**2).mean())); m3*= (R**2).mean(); res['E8 RVQ 3b (2b+1b)']=m3
m4,_=vq_mse(ball(65536),R/np.sqrt((R**2).mean())); m4*=(R**2).mean(); res['E8 RVQ 4b (2b+2b)']=m4
# scalar Lloyd-Max
def lloyd(b,n=200000):
    x=np.sort(rng.standard_normal(n)); L=2**b; c=np.quantile(x,(np.arange(L)+0.5)/L)
    for _ in range(200):
        e=(c[1:]+c[:-1])/2; idx=np.searchsorted(e,x); c=np.array([x[idx==j].mean() for j in range(L)])
    e=(c[1:]+c[:-1])/2; idx=np.searchsorted(e,x); return ((x-c[idx])**2).mean()
for b in (2,3,4): res[f'scalar Lloyd-Max {b}b (no scale)']=lloyd(b)
# per-group absmax uniform INT-b with fp16 scale per 128 (KIVI-like asymmetric min/max)
def intg(b,g):
    x=rng.standard_normal((20000,g)); mn=x.min(1,keepdims=True); mx=x.max(1,keepdims=True)
    s=(mx-mn)/(2**b-1); q=np.round((x-mn)/s)*s+mn; return ((x-q)**2).mean()
for b in (2,3,4): res[f'INT{b} asym g128 (+0.25b meta)']=intg(b,128)
# NVFP4: E2M1 values, block 16, FP8 E4M3 scale (approx scale exact)
fp4=np.array([0,0.5,1,1.5,2,3,4,6]); fp4=np.concatenate([-fp4[::-1],fp4])
x=rng.standard_normal((20000,16)); s=np.abs(x).max(1,keepdims=True)/6
q=fp4[np.abs((x/s)[...,None]-fp4).argmin(-1)]*s; res['NVFP4 (4.5b)']=((x-q)**2).mean()
for b in (2,3,4): res[f'Shannon D(R) {b}b']=2**(-2*b)
for k,v in res.items(): print(f"{k:34s} MSE={v:.4f} relRMS={np.sqrt(v):.3f} SNR={-10*np.log10(v):.2f} dB")
