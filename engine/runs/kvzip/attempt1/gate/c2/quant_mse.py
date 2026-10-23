import numpy as np, itertools
rng=np.random.default_rng(0)
N=200000
x=rng.standard_normal(N)
def lloyd(bits,x,it=200):
    L=2**bits; c=np.quantile(x,(np.arange(L)+0.5)/L)
    for _ in range(it):
        b=(c[1:]+c[:-1])/2; idx=np.searchsorted(b,x); c=np.array([x[idx==i].mean() for i in range(L)])
    b=(c[1:]+c[:-1])/2; return np.mean((x-c[np.searchsorted(b,x)])**2)
lm2,lm3=lloyd(2,x),lloyd(3,x)
print("Lloyd-Max Gaussian MSE 2b %.4f (known 0.1175) 3b %.4f (known 0.03454)"%(lm2,lm3))
print("Shannon D(R) bound 2b %.4f  -> ratio vs LM3 %.2f"%(2**-4,2**-4/lm3))
# E8P-like codebook: 2^16 lowest-norm points of E8 + 1/4 shift
pts=[]
r=range(-3,4)
for v in itertools.product(r,repeat=8):
    if sum(v)%2==0: pts.append(v)
A=np.array(pts,float)
B=A+0.5; B=B[(np.abs(B)<=3.5).all(1)]
H=np.vstack([A,B]); H=H[((H.sum(1))%2==0)]  # E8 = D8 u D8+1/2 (sum even)
H=H+0.25
H=H[np.argsort((H**2).sum(1))][:65536]
print("codebook size",len(H))
X=rng.standard_normal((6000,8))
best=None
Ht=H.T; hn=(H**2).sum(1)
for s in np.linspace(0.6,1.4,17):
    err=0
    for i in range(0,len(X),500):
        xs=X[i:i+500]/s
        d=hn[None,:]-2*xs@Ht
        q=H[d.argmin(1)]*s
        err+=((X[i:i+500]-q)**2).sum()
    m=err/X.size
    if best is None or m<best[0]: best=(m,s)
print("E8-ball 2^16 (16 bits/8 dims=2b) Gaussian MSE %.4f at scale %.3f (QuIP#-reported E8P 0.089)"%best)
print("ratio E8 2b / LM 3b = %.2f (idea 3 requires <=1.3)"%(best[0]/lm3))
