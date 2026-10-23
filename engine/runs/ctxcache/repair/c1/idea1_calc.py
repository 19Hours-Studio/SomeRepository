"""Idea 1: audit-calibrated (closed-loop) chunk KV fusion. Cost per request served.
Sources: FACT6 (70B KV 320 KiB/tok FP16 -> 160 KiB FP8), H100 SXM spec (989 TF BF16 / 1979 TF FP8 dense, 3.35 TB/s),
CacheBlend 2405.16444 (15% default; Musique F1 0.35->0.15 at full reuse), AgentKVShift 2607.21604 (10% budget ~full quality;
CacheBlend -47.5% at 10%), ContextPilot 2511.03475 (exact-prefix reorder+dedup: hit 34-60%, F1 64.15->64.68)."""
import math
L,KVH,HD=80,8,128; P=70e9
kv_fp8=L*KVH*HD*2*1            # bytes/token FP8 K+V
print("KV FP8 KiB/token", kv_fp8/1024)
# GPU-ms per token (8xH100 node, FP8)
mfu=0.5; flops_gpu=1979e12*mfu
pre_ms=2*P/flops_gpu*1e3        # GPU-ms per prefill token (linear part)
B=64; ctx=7300; hbm=3.35e12*8
step=(P*1+B*ctx*kv_fp8)/hbm     # s per decode step, node
dec_ms=step/B*8*1e3             # GPU-ms per output token
print(f"prefill {pre_ms:.3f} GPU-ms/tok, decode {dec_ms:.3f} GPU-ms/tok, ratio {dec_ms/pre_ms:.1f}")
gpu_h=2.5                        # $/H100-hour (cloud mid 2026, assumption)
usd=lambda gms: gms/3.6e6*gpu_h
S,D,Q,O=1000,6000,100,200        # sys prompt, doc tokens (6 chunks x1000), query, output
read_ms=0.02*pre_ms              # cost to place cached token (attention + load), assumption ~2% of prefill
def cost(prefill_tok, reused_tok, out=O):
    return prefill_tok*pre_ms + reused_tok*read_ms + out*dec_ms
base={}
base['full recompute']=cost(S+D+Q,0)
base['exact prefix (sys only)']=cost(D+Q,S)
for h in (0.34,0.60):
    base[f'ContextPilot reorder h={h}']=cost(D*(1-h)+Q,S+D*h)
for r in (0.15,0.20):
    base[f'CacheBlend open-loop r={r}']=cost(r*D+Q,S+D*(1-r))
base['AgentKVShift r=0.10']=cost(0.10*D+Q,S+0.9*D)
def idea(r,a=0.02,h=0.0):
    fused=cost(r*D*(1-h)+Q,S+D*h+D*(1-h)*(1-r))
    audit_extra=cost(r*D*(1-h)+Q+O,0,out=0)   # shadow fused prefill + teacher-forced scoring of gold answer
    full=cost(D*(1-h)+Q,S+D*h)
    return (1-a)*fused + a*(full+audit_extra)
rows=list(base.items())
for r in (0.05,0.10,0.15,0.30):
    rows.append((f'IDEA closed-loop r*={r} a=2%',idea(r)))
    rows.append((f'IDEA + ContextPilot h=0.34 r*={r}',idea(r,h=0.34)))
ref=base['exact prefix (sys only)']; best_exact=base['ContextPilot reorder h=0.34']
print(f"{'scheme':40s} GPU-ms/req  $/1k req  x vs prefix  x vs CtxPilot34")
for k,v in rows:
    print(f"{k:40s} {v:9.1f}  {usd(v)*1000:8.4f}  {ref/v:6.2f}  {best_exact/v:6.2f}")
# prefill-only ratio (input term)
print("input-term ratio r=0.10 vs prefix:", (D+Q)/(0.1*D+Q+S*0.02))
# --- audit statistics: zero-failure bound n = ln(delta)/ln(1-eps)
for eps in (0.01,0.02,0.05):
    n=math.log(0.05)/math.log(1-eps)
    print(f"answer-flip budget {eps:.0%}: audits needed {n:.0f}; at a=2% -> {n/0.02:,.0f} requests per calibration window")
# detect a jump in flip rate 1%->5% (one-sided binomial, alpha .05 power .8)
from math import sqrt
p0,p1=0.01,0.05; za,zb=1.645,0.84
n=((za*sqrt(p0*(1-p0))+zb*sqrt(p1*(1-p1)))/(p1-p0))**2
print(f"detect flip rate 1%->5%: n={n:.0f} audits")
# --- consistency: SSD / DRAM bandwidth vs compute throughput
for r in (0.05,0.10,0.15):
    gpu_ms_req=(r*D+Q)*pre_ms+O*dec_ms
    req_s=8*1000/gpu_ms_req
    load_GBs=req_s*D*(1-r)*kv_fp8/1e9
    print(f"r={r}: node serves {req_s:.1f} req/s -> needs {load_GBs:.1f} GB/s KV load (PCIe5 x16 ~50 GB/s/GPU, 1 NVMe ~7-14 GB/s)")
# --- storage economics: hot-set admission
chunk_GB=1000*kv_fp8/1e9
save_usd=usd(1000*0.9*pre_ms)
for tier,usd_gb_mo in (('NVMe',0.10),('DRAM',3.0)):
    per_h=chunk_GB*usd_gb_mo/730
    print(f"{tier}: 1k-token chunk {chunk_GB:.3f} GB costs ${per_h:.2e}/h; saving per reuse ${save_usd:.2e} -> break-even {per_h/save_usd:.3f} reuses/h")
