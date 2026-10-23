import numpy as np
rng=np.random.default_rng(0)
x=rng.standard_normal(2_000_000)
def lloyd(bits,it=200):
    n=2**bits; c=np.quantile(x,(np.arange(n)+.5)/n)
    for _ in range(it):
        b=(c[1:]+c[:-1])/2; idx=np.searchsorted(b,x)
        c=np.array([x[idx==i].mean() for i in range(n)])
    b=(c[1:]+c[:-1])/2; return np.mean((x-c[np.searchsorted(b,x)])**2)
# known answers: Lloyd-Max Gaussian 1b 0.3634, 2b 0.1175, 3b 0.03454, 4b 0.009497
lm={b:lloyd(b) for b in (1,2,3,4)}; print("LloydMax MSE",lm)
DR=lambda R:2**(-2*R)
print("Shannon D(R) 2b",DR(2),"2.125b",DR(2.125))
# Idea 2: required trellis 2-bit MSE <= 1.2 x 4-bit scalar
print("IDEA2 required MSE<=",1.2*lm[4],"; best possible at 2b (Shannon)",DR(2),
      "margin(bound)",1.2*lm[4]/DR(2),"; QTIP-class ~0.069 margin",1.2*lm[4]/0.069)
# Idea 3/4: per-token value quant, group 128, FP16 absmax scale, uniform, subtractive dither
def gq(bits,g,dither=False,zp=False):
    v=rng.standard_normal((20000,g))
    if zp: lo=v.min(1,keepdims=True); hi=v.max(1,keepdims=True)
    else: hi=np.abs(v).max(1,keepdims=True); lo=-hi
    L=2**bits-1; d=(hi-lo)/L
    u=rng.uniform(-.5,.5,v.shape) if dither else 0
    q=np.clip(np.round((v-lo)/d+u),0,L); r=(q-u)*d+lo
    e=r-v; return np.mean(e**2), np.mean(e)
for name,a in [("idea3 V 2b g128 absmax+dither",(2,128,True)),("idea3 V no dither",(2,128,False)),
               ("KIVI V 2b g32 minmax",(2,32,False,True)),("4b g16 absmax (NVFP4-like int)",(4,16,False)),
               ("idea3 K 3b g128 absmax",(3,128,False))]:
    print(name,gq(*a))
# output error of attention at effective N_eff tokens attended: var scales 1/N_eff
mse_v=gq(2,128,True)[0]; mse4=gq(4,16)[0]
for n in (1,2,4,8): print("N_eff",n,"V out rel MSE",mse_v/n,"vs 4b at N=1",mse4)
print("N_eff needed for idea3 2b V to match 4b at N_eff=1:",mse_v/mse4)
# Idea 1: key reconstruction compute in decode (RoPE after dequant => cannot fold basis into query)
d=128; flop=2*d*d; bytes_k=d*2.5/8
print("IDEA1 FLOP/byte needed",flop/bytes_k,"H100 ridge (989 TF bf16 dense /3.35TB/s)",989e12/3.35e12)
t=lambda b: b/3.35e12*1e12
kv_fp16=t(2*d*2); kv_nvfp4=t(2*d*4.5/8); kv_klt_mem=t(2*d*2.5/8); k_rec=flop/989e12*1e12
for u in (1.0,0.5,0.3):
    print(f"util {u}: KLT per token-head ps=max(mem {kv_klt_mem:.1f}, recon {k_rec/u:.1f}) vs NVFP4 {kv_nvfp4:.1f} FP8 {t(2*d):.1f} FP16 {kv_fp16:.1f}")
# AM/GM gain check: known answer
lam=np.array([4.,1.]); print("AM/GM gain bits (known 0.5*log2(2.5/2)=0.161):",0.5*np.log2(lam.mean()/np.exp(np.log(lam).mean())))
# Chain, archetype B, FP8 baseline shares: KV 50, W 36, other 14 (ledger). Best practice NVFP4 4.5b.
def cost(bits,ovh=0.0,batch_scaling=False):
    f=bits/8; kv=0.50*f*(1+ovh); w=0.36*(f if batch_scaling else 1); return kv+w+0.14
for nm,b,o in [("NVFP4",4.5,0),("idea1 2.5b",2.5,0),("idea2 2.13b +10%",2.13,0.10),("idea3 2.65b",2.65,0),("idea4 2.6b",2.6,0)]:
    print(nm,"cost",round(cost(b,o),3),"cap-limited",round(cost(b,o,True),3),
          "RATIO vs NVFP4",round(cost(4.5)/cost(b,o),2),round(cost(4.5,0,True)/cost(b,o,True),2))
