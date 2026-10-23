# Agentic regime with HBM-limited decode batch, plus FP8-KV-on-GPU alternative and shadow-audit cost
L=32; kv=131072; W=16e9; BW=3.35e12*0.8; eff=500e12; pcie=25e9
hbm=52e9; dram_node=8*200e9
def pf(miss,hit): return (2*8e9*miss+2*L*4096*(miss*miss+2*miss*hit))/eff
for n_ctx,out in [(30000,400),(60000,500)]:
  print(f"ctx {n_ctx}, out {out}")
  for S in [8,32,128,512]:
    ws=S*n_ctx*kv
    for nm,kvb,gcap,tier in [("APC BF16",kv,hbm,0),("APC FP8-KV",kv/2,hbm,0),("APC+CPU tier",kv,hbm,dram_node/8*8)]:
        B=max(1,min(64,int(hbm*0.5/(n_ctx*kvb))))      # half HBM for running batch, half for cached prefixes
        cache_cap=hbm*0.5+tier
        h=0.95*min(1,cache_cap/(S*n_ctx*kvb))
        hit=h*n_ctx; miss=n_ctx-hit
        t_pre=pf(miss,hit); load=(hit*kvb/pcie if tier else 0)
        t_dec=out*(W+B*n_ctx*kvb)/BW/B
        t=t_pre+0.1*load+t_dec
        print(f"  S={S:4d} {nm:13s} B={B:2d} hit={h:.2f} GPU-s/req={t:.3f}")
# shadow audit: recompute fraction a of hits from scratch and compare logits
for a in [0.01,0.001]: print(f"audit {a:.1%} of hits -> extra cost ~{a*3.8/ (3.8*0.05+1.0):.2%} per request (60K ctx)")
