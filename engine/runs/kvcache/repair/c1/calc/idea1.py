# Idea 1: exact-prefix tiered KV reuse. All inputs sourced in NOTES.md.
import math
GB=1e9
# Llama-3.1-8B config: 32 layers, 8 KV heads, head_dim 128
L,H,D=32,8,128
kv_tok=L*H*D*2*2            # BF16 K+V bytes/token
print("KV bytes/token BF16", kv_tok)
# H100-80GB node (DGX H100: 2 TB DRAM, 8x3.84 TB NVMe, 8 GPUs)
hbm_free=80*0.9-16-4        # GB for KV after weights(16)+activations(4)
dram=2000/8*0.8             # GB/GPU usable for tier
nvme=8*3.84e3/8*0.9         # GB/GPU
cap={k:v*GB/kv_tok for k,v in dict(gpu=hbm_free,cpu=dram,nvme=nvme).items()}
for k,v in cap.items(): print(f"capacity {k}: {v/1e6:.2f} M tokens")
# Mooncake conversation hit-rate curve (FACT 11): tokens->hit
pts=[(16e3,.033),(4e6,.185),(16e6,.342)]; ceil=.374
def hit(c):
    if c<=pts[0][0]: return pts[0][1]
    for (x0,y0),(x1,y1) in zip(pts,pts[1:]):
        if c<=x1: return y0+(y1-y0)*math.log(c/x0)/math.log(x1/x0)
    return min(ceil, pts[-1][1]+(ceil-pts[-1][1])*min(1,math.log(c/16e6)/math.log(4)))
# NOTE: trace is cluster-level; per-GPU capacity is a scale assumption -> also show x8 (node-shared tier)
def scen(name,c): print(f"  {name:28s} cap {c/1e6:7.2f}M tok  hit {hit(c):.3f}")
print("Per-GPU private tier:")
g=cap['gpu']; c=g+cap['cpu']; n=c+cap['nvme']
for nm,cc in [("GPU-only APC",g),("GPU+CPU (LMCache/Offload)",c),("GPU+CPU lossless x1.32",g+1.32*cap['cpu']),("GPU+CPU+NVMe",n)]: scen(nm,cc)
print("Node-shared tier (8 GPUs pool CPU/NVMe):")
for nm,cc in [("GPU-only APC",g),("GPU+CPU",g+8*cap['cpu']),("GPU+CPU lossless x1.32",g+8*1.32*cap['cpu']),("GPU+CPU+NVMe",g+8*(cap['cpu']+cap['nvme']))]: scen(nm,cc)

# Per-request GPU time, Mooncake trace averages: input 7590, output 182 (Mooncake paper)
def flops_prefill(n):   # 2*params*n + attention 4*L*d_model*n^2/2 (causal)
    return 2*8.0e9*n + 2*L*4096*n*n
eff=500e12                  # effective BF16 FLOP/s on H100 (FACT 8 assumption)
n_in,n_out=7590,182
t_pre=flops_prefill(n_in)/eff
# decode: memory bound, batch B=64, step=(W + B*ctx*kv)/BW
BW=3.35e12*0.8; B=64; W=16e9
ctx=n_in+n_out/2
t_step=(W+B*ctx*kv_tok)/BW
t_dec=n_out*t_step/B
print(f"\nprefill {t_pre*1e3:.0f} ms GPU, decode share {t_dec*1e3:.0f} ms GPU-equiv/request; prefill frac {t_pre/(t_pre+t_dec):.2f}")
# load costs per tier (bytes for the hit portion), overlapped layer-wise -> only residual counted
pcie=25e9; nvme_bw=6.5e9*4   # 8 drives / 8 GPUs, but RAID across node: assume 4 drives' worth reachable
def req_time(h, tier_bw):
    hit_tok=h*n_in; miss=n_in-hit_tok
    load=hit_tok*kv_tok/tier_bw
    pre=flops_prefill(miss)/eff   # approx (miss attends to hits too; conservative-ish)
    pre+= 2*L*4096*miss*hit_tok*2/eff
    return max(load,0)*0.1 + pre + t_dec   # 90% of load overlapped with compute (FACT 9 layer-pipelining)
base=req_time(hit(g),1e30)
print("cost per request relative to GPU-only APC (per-GPU / node-shared):")
for nm,(c1,c2,bw) in {"GPU+CPU":(g+cap['cpu'],g+8*cap['cpu'],pcie),
                       "GPU+CPU lossless1.32":(g+1.32*cap['cpu'],g+8*1.32*cap['cpu'],pcie*1.32),
                       "GPU+CPU+NVMe":(n,g+8*(cap['cpu']+cap['nvme']),nvme_bw)}.items():
    print(f"  {nm:22s} {base/req_time(hit(c1),bw):.3f}x   {base/req_time(hit(c2),bw):.3f}x")
nohit=req_time(0,1e30); print(f"GPU-only APC vs no caching: {nohit/base:.3f}x")

# High-reuse regime: agentic/multi-turn, per-turn context 60K, reuse of prior turns ~95% if still cached
print("\nAgentic regime: S concurrent sessions x 60K ctx, think time between turns evicts GPU copy")
n_ctx=60000; out=500
for S in [4,16,64,256]:
    ws=S*n_ctx
    h_gpu=0.95*min(1,cap['gpu']/ws)   # LRU on uniform round-robin: ~all-or-nothing; use fractional optimistic
    h_cpu=0.95*min(1,(cap['gpu']+8*cap['cpu'])/ws)
    def t(h):
        hit_tok=h*n_ctx; miss=n_ctx-hit_tok
        pre=(2*8e9*miss+2*L*4096*(miss*miss+2*miss*hit_tok))/eff
        load=hit_tok*kv_tok/pcie
        dec=out*(W+B*n_ctx*kv_tok)/BW/B
        return pre+0.1*load+dec, load
    tg,_=t(h_gpu); tc,ld=t(h_cpu)
    print(f"  S={S:4d} ws {ws/1e6:6.2f}M tok hit gpu {h_gpu:.2f} cpu {h_cpu:.2f}  gain {tg/tc:.2f}x  load {ld*1e3:.0f} ms vs full prefill {(2*8e9*n_ctx+2*L*4096*n_ctx**2)/eff*1e3:.0f} ms")
# $ per 1M requests (Mooncake avg) H100 $2.5/h; DRAM cost amortized $4/GB / 4y
gpu_h=2.5
for nm,tt,extra in [("no cache",nohit,0),("GPU APC",base,0),("+CPU tier",req_time(hit(g+8*cap['cpu']),pcie),dram*4/(4*8760))]:
    print(f"$ per 1M req {nm:10s}: {(tt*1e6/3600)*(gpu_h+extra):8.1f}")
# batch-invariant mode penalty (SGLang 34%, LLM-42 56%) against bitwise claim
for pen in [0.34,0.56]: print(f"bitwise mode throughput penalty {pen:.0%} -> needs gain >{1/(1-pen):.2f}x to break even")
