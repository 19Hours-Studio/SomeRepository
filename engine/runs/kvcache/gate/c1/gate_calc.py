# Exact arithmetic for the gate. Inputs: Llama-3.1-8B config (32 layers, 8 KV heads, head_dim 128, hidden 4096, ~8.0e9 params),
# H100 SXM HBM 3.35 TB/s, ~500 TFLOP/s effective (ledger assumption), PCIe Gen5 x16 ~50 GB/s pinned H2D (64 GB/s theoretical), NVMe Gen4 ~7 GB/s.
import math, random
L,KVH,HD,H,P=32,8,128,4096,8.0e9
bpt_bf16=L*KVH*HD*2*2; bpt_fp8=bpt_bf16//2
print("bytes/token bf16",bpt_bf16,"fp8",bpt_fp8)
HBM,FLOPS,PCIE,NVME=3.35e12,500e12,50e9,7e9
# ---- Idea 1: per-step fetch budget, batch-bound decode at long context (weights amortised away)
keep=0.30
rmax=keep/(1-keep)*PCIE/HBM
print(f"Idea1: max fraction of offloaded KV fetchable per step without stalling (KV-bound) = {rmax*100:.2f}%")
S=128*1024
w=16e9/HBM; kv_res=keep*S*bpt_fp8/HBM; step=w+kv_res
off=(1-keep)*S*bpt_fp8
print(f"  single 128K request: step {step*1e3:.2f} ms, offloaded {off/1e9:.2f} GB, fetchable/step {PCIE*step/1e9:.3f} GB = {PCIE*step/off*100:.2f}%")
# ShadowKV: sparse budget 1.56% of context fetched per step (values only, i.e. half of KV) -> fraction of offloaded
need=0.0156*0.5/(1-keep)
print(f"  ShadowKV-like need (1.56% budget, V-only) as fraction of offloaded = {need*100:.2f}% -> margin {rmax/need:.2f}")
need_full=0.0156/(1-keep)
print(f"  Quest-like need (1.56% budget, K+V) = {need_full*100:.2f}% -> margin {rmax/need_full:.2f}")
# ---- Idea 2: load vs prefill for 20K
S2=20000
fl=2*P*S2 + L*4*H*S2**2/2
tp=fl/FLOPS; kvb=S2*bpt_bf16
print(f"Idea2: 20K prefill {fl/1e12:.0f} TFLOP -> {tp:.2f}s; KV {kvb/1e9:.2f} GB; PCIe load {kvb/PCIE:.3f}s (margin {tp/(kvb/PCIE):.1f}); NVMe load {kvb/NVME:.3f}s (margin {tp/(kvb/NVME):.1f})")
def cost(h,lt=kvb/PCIE): return 1-0.66*h*(1-lt/tp)
for h_gpu,h_tier in [(0.34,0.55)]:
    print(f"  Mooncake hit 34%->55%: tiered vs GPU-only {cost(h_gpu)/cost(h_tier):.2f}x ; tiered vs no reuse {1/cost(h_tier):.2f}x ; GPU-only vs none {1/cost(h_gpu):.2f}x")
print(f"  hit rate needed for 1.5x vs no reuse: {(1-1/1.5)/(0.66*(1-kvb/PCIE/tp)):.2f}; for 2.4x: {(1-1/2.4)/(0.66*(1-kvb/PCIE/tp)):.2f}")
# GPU capacity: 80GB - 16GB weights - ~6GB act -> contexts held
print(f"  GPU KV pool ~58GB holds {58e9/kvb:.0f} x 20K contexts; 1 TB DRAM holds {1e12/kvb:.0f}")
# ---- Idea 3: 30-min budget, RULER-128K samples, minimum detectable paired delta
sec_per=28*128/129  # ~prefill-dominated GPU-s per 128K sample (ledger: 28 s per 128K+1K request)
n_cfg=int(1800/sec_per/2)
print(f"Idea3: 30 min -> {n_cfg} RULER-128K samples per config")
def mdd(n,p=0.9,disc=None):
    # paired binary: sd of difference ~ sqrt(discordant rate / n); discordant rate approx 2p(1-p) if independent errors
    d=disc if disc else 2*p*(1-p)
    return 1.96*math.sqrt(d/n)  # 95% half-width ignoring delta^2
# check once on known case by simulation: n=1000, p=0.9 independent errors
random.seed(0); n=1000; diffs=[]
for _ in range(2000):
    a=sum(random.random()<0.9 for _ in range(n)); b=sum(random.random()<0.9 for _ in range(n)); diffs.append((a-b)/n)
sd=(sum(x*x for x in diffs)/len(diffs))**0.5
print(f"  check: sim sd {sd:.4f} vs formula {math.sqrt(0.18/n):.4f}")
print(f"  95% half-width at n={n_cfg}: {mdd(n_cfg)*100:.1f} pts; n needed for 2-pt resolution: {math.ceil(0.18*(1.96/0.02)**2)}")
# ---- Idea 4: gain on models where FP8 fails (baseline BF16 KV), fraction f of layers kept BF16
for f in (0.1,0.25,0.5):
    kvr=(1+f)/2
    # archetype A shares recomputed for BF16 KV: decode KV read 25% at FP8 -> 50/125 of a cost-1.25 system
    base=1.25; new=1.25-0.5*(1-kvr)
    print(f"Idea4: f={f}: KV bytes x{1/kvr:.2f}; archetype-A cost ratio vs BF16 KV {base/new:.2f}")
print("Idea3/4 vs blanket FP8 on models where FP8 is safe: ratio <=1.0 (gating only adds BF16 layers)")
