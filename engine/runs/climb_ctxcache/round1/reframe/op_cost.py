# Operator-side real marginal cost of a cache READ vs a RECOMPUTE, Llama-3-70B-class, BF16 KV, H100.
# All hardware/price inputs are ASSUMPTIONS (same as baseline calc.py where shared): H100 $2/h, 989 TFLOPs
# BF16 dense at 45% MFU, HBM 3.35 TB/s, DRAM $1.64 and NVMe $0.07 per 1M tokens-hour of 70B KV.
P_=70e9; L=80; D=8192; KVB=2*8*128*L*2            # 327,680 B/token (GQA 8 KV heads)
FL=989e12*0.45; GPU=2/3600; HBM_BW=3.35e12; PCIE=40e9
TIER={"HBM":2/80/3600, "DRAM":1.64/(KVB*1e6/1e9)/3600, "NVMe":0.07/(KVB*1e6/1e9)/3600}   # $/GB-s
lin=lambda n: 2*P_*n; att=lambda n,ctx: 4*L*D*n*(ctx+n/2)
def recompute(P): return (lin(P)+att(P,0))/FL*GPU
def read(P,n,gap,tier):           # extra cost caused by having P cached tokens in the context instead of none
    a=att(n,P)/FL*GPU                         # new tokens attend to cached KV (exact, unavoidable)
    res=KVB*P/1e9*gap*TIER[tier]              # keep KV during the inter-turn gap
    load=0 if tier=="HBM" else 0.0            # PCIe/NVMe load assumed overlapped layer-wise (AttentionStore-style)
    return a, res
print("tier $/GB-h:", {k:round(v*3600,5) for k,v in TIER.items()})
for P in (20_000, 50_000, 100_000):
  for n in (500, 2300):
    rc=recompute(P)
    for gap in (10, 60, 600):
      s=[]
      for t in ("HBM","DRAM","NVMe"):
        a,r=read(P,n,gap,t); s.append(f"{t}={(a+r)/rc:6.2%}")
      print(f"P={P:>7,} n={n:>5} gap={gap:>4}s  recompute=${rc:.4f}  read/recompute: "+" ".join(s)+
            f"  (attention part {att(n,P)/FL*GPU/rc:.2%})")
# PCIe load time for the prefix (to check the overlap assumption): prefill of n new tokens vs load time
for P,n in ((100_000,2300),(100_000,500)):
    print(f"P={P} n={n}: load {KVB*P/PCIE:.2f}s vs new-token prefill {(lin(n)+att(n,P))/FL:.2f}s on one GPU")
