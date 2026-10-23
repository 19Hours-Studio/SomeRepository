import numpy as np, itertools
rng=np.random.default_rng(1)
# --- groupwise scalar quantizers on rotated (Gaussian) data, group=128 values
def rtn(x,bits,asym=True,dither=False):
    g=x.reshape(-1,128)
    if asym:
        lo,hi=g.min(1,keepdims=True),g.max(1,keepdims=True); L=2**bits-1
        s=(hi-lo)/L; u=rng.uniform(-.5,.5,g.shape) if dither else 0
        q=np.clip(np.round((g-lo)/s+u),0,L)-u; return (q*s+lo).ravel()
    else:  # symmetric absmax, 2^bits levels at +-(k+.5)s
        L=2**bits; s=np.abs(g).max(1,keepdims=True)/(L/2)
        u=rng.uniform(-.5,.5,g.shape) if dither else 0
        q=np.clip(np.floor(g/s+u),-L/2,L/2-1)+.5-u; return (q*s).ravel()
x=rng.standard_normal(128*4000)
m=lambda y:np.mean((x-y)**2)
quarot3=m(rtn(x,3,True)); kivi2=m(rtn(x,2,True))
idea2K=m(rtn(x,3,False)); idea2V=m(rtn(x,2,False,dither=True)); idea2Vnod=m(rtn(x,2,False))
print(f"QuaRot-style 3b asym g128 MSE {quarot3:.4f}; 2b asym g128 {kivi2:.4f}")
print(f"Idea2 K 3b sym g128 {idea2K:.4f}; V 2b sym subtractive-dither {idea2V:.4f} (no dither {idea2Vnod:.4f})")
# E8 codebooks: 2b = 2^16 lowest-norm E8+1/4 ; 1b residual = 2^8 lowest-norm E8 points
pts=np.array([v for v in itertools.product(range(-3,4),repeat=8) if sum(v)%2==0],float)
B=pts+0.5; E8=np.vstack([pts,B[(B.sum(1)%2==0)&(np.abs(B)<=3.5).all(1)]])
C2=(E8+0.25); C2=C2[np.argsort((C2**2).sum(1))][:65536]
C1=E8[np.argsort((E8**2).sum(1))][:256]
def vq(X,C,s):
    out=np.empty_like(X); cn=(C**2).sum(1)
    for i in range(0,len(X),500):
        xs=X[i:i+500]/s; out[i:i+500]=C[(cn[None]-2*xs@C.T).argmin(1)]*s
    return out
X=rng.standard_normal((5000,8))
q2=vq(X,C2,0.95); e2=np.mean((X-q2)**2)
R=X-q2; best=min((np.mean((R-vq(R,C1,s))**2),s) for s in np.linspace(0.3,1.0,15))
print(f"E8P 2b MSE {e2:.4f}; E8P+1b E8 residual (3b) MSE {best[0]:.4f} (scale {best[1]:.3f})")
k1,v1=best[0],e2
print(f"Idea1 K/V MSE {k1:.4f}/{v1:.4f} vs QuaRot-3b {quarot3:.4f}/{quarot3:.4f}  (QuaRot-3b lost 6.7 AIME pts)")
print(f"Idea2 K/V MSE {idea2K:.4f}/{idea2V:.4f}; V noise / 3b-RTN noise = {idea2V/quarot3:.2f} -> N_eff needed for parity")
# check 'averaging' claim: rel. output error of sum p_i v_i vs N_eff, iid zero-mean V
for neff in [1,2,4,16]:
    T=64; p=np.zeros(T); p[:neff]=1/neff
    V=rng.standard_normal((20000,T)); Vq=rtn(V.ravel()[:len(V.ravel())//128*128],2,False,True).reshape(V.shape)
    o=V@p; oq=Vq@p; print(f"  N_eff={neff:2d} relative output err^2 {np.mean((o-oq)**2)/np.mean(o**2):.3f}")
