# Coding-gain model: bits/value needed to hit a fixed attention-logit distortion, for
# (H) global Hadamard + uniform rate [Idea1 original], (B) RoPE-band energy allocation in 8-dim groups
# [Idea1 repaired], (Kpre) pre-RoPE KLT [Idea2 original], (Kpost) post-RoPE KLT estimated on prefill,
# evaluated on later decode positions [Idea2 repaired]. Synthetic keys; real spectra unknown (Loki r90 used as anchor).
import numpy as np
rng=np.random.default_rng(1)
d=128; P=d//2
def rope_freqs(base): return base**(-np.arange(P)*2/d)
def make_cov(sig_ln, n_out, out_scale, rank, wlr, out_low=True):
    ch=np.exp(sig_ln*rng.standard_normal(d))
    # outlier pairs in low-frequency dims (high pair index) per Jin et al. 2025 massive values
    pairs=np.arange(P-12,P) if out_low else np.arange(P)
    op=rng.choice(pairs,n_out,replace=False)
    for p in op: ch[2*p]*=out_scale; ch[2*p+1]*=out_scale*0.3
    F=rng.standard_normal((d,rank))/np.sqrt(rank)
    C=wlr*F@F.T+(1-wlr)*np.eye(d); s=np.sqrt(np.diag(C)); C=C/np.outer(s,s)
    S=np.sqrt(ch)[:,None]*C*np.sqrt(ch)[None]; mu=np.zeros(d)
    for p in op: mu[2*p]=2.0*np.sqrt(ch[2*p])   # big channel mean (KIVI outlier channels)
    return S,mu
def rope(X,pos,base):
    th=np.outer(pos,rope_freqs(base)); c,s=np.cos(th),np.sin(th)
    x0,x1=X[:,0::2],X[:,1::2]; Y=np.empty_like(X); Y[:,0::2]=x0*c-x1*s; Y[:,1::2]=x0*s+x1*c; return Y
def r90(Y):
    ev=np.sort(np.linalg.eigvalsh(np.cov(Y.T)))[::-1]; return int(np.searchsorted(np.cumsum(ev)/ev.sum(),0.9)+1)
def rate(lam,w,Dt):
    # reverse water-filling for weighted MSE sum w_i*D_i = Dt ; returns avg bits/dim (Gaussian, ideal)
    a=w*lam; lo,hi=1e-12,a.max()
    for _ in range(200):
        t=np.sqrt(lo*hi); Dtot=np.minimum(t,a).sum()
        lo,hi=(t,hi) if Dtot<Dt else (lo,t)
    return np.maximum(0,0.5*np.log2(a/t)).mean()
def evaluate(base=1e6,Lp=8192,Lg=32768,rho=0.8,**kw):
    S,mu=make_cov(**kw); L=np.linalg.cholesky(S+1e-9*np.eye(d))
    pre=mu+rng.standard_normal((Lp+Lg,d))@L.T
    # queries share energy pattern with keys (corr rho on log-energies)
    qe=np.exp(rho*np.log(np.diag(S))+np.sqrt(1-rho**2)*np.log(np.diag(S)).std()*rng.standard_normal(d))
    pos=np.arange(Lp+Lg); post=rope(pre,pos,base)
    Wq=qe  # per-pre-RoPE-dim query energy; pair-symmetric after RoPE averaging
    Wq_pair=np.repeat((qe[0::2]+qe[1::2])/2,2)
    G=post[Lp:]  # decode-time keys
    out={}
    # target: weighted distortion equal to Hadamard+uniform at R0 bits; Hadamard makes coords iid var=AM
    for R0 in (2.0,3.0):
        lamH=np.full(d,np.var(G-G.mean(0),axis=0).sum()/d)
        Dt=(Wq_pair*lamH*2**(-2*R0)).sum()
        # B: 8-dim groups of 4 RoPE pairs, energies from prefill (RoPE-invariant), Hadamard inside group
        eP=(post[:Lp]-post[:Lp].mean(0))**2; e_pair=eP[:,0::2].mean(0)+eP[:,1::2].mean(0)
        g_e=np.repeat(e_pair.reshape(16,4).mean(1)/2,8); g_w=np.repeat(Wq_pair.reshape(16,8).mean(1),8)
        # actual decode distortion with prefill-estimated allocation: use actual group variance of G
        eG=(G-G.mean(0))**2; gvar=np.repeat(eG.reshape(len(G),16,8).mean((0,2)),8)
        # allocation from prefill estimate, then measure rate at which actual distortion matches Dt
        def rate_mismatch(lam_est,lam_true,w):
            # find theta via estimate, scale theta so true distortion = Dt; rate uses estimate allocation
            a_e=w*lam_est; lo,hi=1e-12,a_e.max()*10
            for _ in range(200):
                t=np.sqrt(lo*hi); b=np.maximum(0,0.5*np.log2(a_e/t)); Dtrue=(w*lam_true*2**(-2*b)).sum()
                lo,hi=(t,hi) if Dtrue<Dt else (lo,t)
            return b.mean()
        out[f'B_band8@{R0}']=rate_mismatch(g_e,gvar,g_w)
        # Kpre: oracle pre-RoPE KLT (query weighting projected)
        Cp=np.cov(pre[Lp:].T); ev,U=np.linalg.eigh(Cp); wU=(U**2*Wq[:,None]).sum(0)
        out[f'Kpre@{R0}']=rate(ev.clip(1e-12),wU,Dt)
        # Kpost: post-RoPE KLT estimated on prefill, applied to decode keys (mismatch)
        Ce=np.cov(post[:Lp].T); ev,U=np.linalg.eigh(Ce); lam_true=((G-post[:Lp].mean(0))@U).var(0)
        wU=(U**2*Wq_pair[:,None]).sum(0)
        out[f'Kpost@{R0}']=rate_mismatch(ev.clip(1e-12),lam_true,wU)
        # Kpost oracle (basis from decode keys themselves)
        Cg=np.cov(G.T); ev,U=np.linalg.eigh(Cg); wU=(U**2*Wq_pair[:,None]).sum(0)
        out[f'KpostOracle@{R0}']=rate(ev.clip(1e-12),wU,Dt)
        out[f'H@{R0}']=R0
    out['r90_pre']=r90(pre); out['r90_post']=r90(post)
    return out
cases={'mild (Loki-like)':dict(sig_ln=0.7,n_out=2,out_scale=8,rank=24,wlr=0.5),
       'strong outliers':dict(sig_ln=1.0,n_out=4,out_scale=30,rank=16,wlr=0.6),
       'flat (worst)':dict(sig_ln=0.4,n_out=0,out_scale=1,rank=8,wlr=0.2)}
for name,kw in cases.items():
    for rho in (0.0,0.8):
        o=evaluate(rho=rho,**kw)
        print(f"{name:18s} rho={rho} r90 pre/post={o['r90_pre']}/{o['r90_post']} | "+
              " ".join(f"{k}={v:.2f}" for k,v in o.items() if '@' in k))
