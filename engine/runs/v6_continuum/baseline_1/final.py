"""Final comparison across attention types. Same 1T/32B MoE FFN; attention variants:
 MLA  : dense MLA (Kimi-K2/DeepSeek-V3 style), 576 vals/tok/layer, ~242 FLOP/value
 DSA  : MLA + DeepSeek-V3.2-style top-2048 sparse attention w/ FP8 lightning indexer (128-d key, 64 idx heads)
 GQA  : 8 KV heads x128 x(K,V) = 2048 vals/tok/layer, 64 q heads -> 16 FLOP/value
All memory-tier/energy constants as in roofline.py (EST unless FACT)."""
import math, roofline as R
GB=1e9
chips = {
 "Rubin":     dict(cf=288, bf=22,    tf="hbm",  f4=50,  f8=16,  kw=1.8, lat=3.0),
 "Ironwood":  dict(cf=192, bf=7.37,  tf="hbm",  f4=4.6, f8=4.6, kw=1.0, lat=4.0),
 "WSE-3":     dict(cf=44,  bf=21000, tf="sram", f4=12.5,f8=12.5,kw=23,  lat=8.0),
 "Groq LP30": dict(cf=0.5, bf=150,   tf="sram", f4=1.2, f8=1.2, kw=0.5, lat=1.0),
 "Continuum": dict(cf=160, bf=64,    tf="stack",f4=40,  f8=20,  kw=2.0, lat=3.0),
}
def step(c, B, L, att, n):
    w_read=(R.P_ALWAYS+R.MOE_LAYERS*R.unique_experts(B)*R.P_EXPERT)*R.BITS/8
    w_tot=R.P_TOTAL*R.BITS/8
    if att=="GQA":   vals=2048; kv_store=B*L*R.LAYERS*vals*R.BITS/8; kv_read=kv_store; fl_att=B*R.LAYERS*L*64*128*2*2; idx=0
    else:
        vals=576; kv_store=B*L*R.LAYERS*vals*R.BITS/8
        if att=="MLA": kv_read=kv_store; fl_att=B*R.LAYERS*L*64*1088*2; idx=0
        else:
            k=min(L,2048); idx_bytes=B*L*R.LAYERS*128*1.0
            kv_store+=idx_bytes; kv_read=B*k*R.LAYERS*vals*R.BITS/8+idx_bytes
            fl_att=B*R.LAYERS*k*64*1088*2; idx=B*R.LAYERS*L*64*128*2
    if (w_tot+kv_store)*1.1 > n*c["cf"]*GB: return None
    read=w_read+kv_read
    t_mem=read/(n*c["bf"]*1e12)
    t_cmp=B*2*32e9/(n*c["f4"]*1e15*.7)+(fl_att+idx)/(n*c["f8"]*1e15*.7)
    t=max(t_mem,t_cmp)+(2*R.MOE_LAYERS*c["lat"]*1e-6 if n>1 else 0)
    e=read*8*R.PJ_BIT[c["tf"]]*1e-12+B*2*32e9*R.PJ_FLOP_FP4*1e-12+(fl_att+idx)*R.PJ_FLOP_FP8*1e-12+.25*n*c["kw"]*1e3*t
    return dict(u=1/t, kw=B/t/(n*c["kw"]), j=B/e, bd="mem" if t_mem>t_cmp else "cmp")
NS=[1,2,3,4,6,8,12,16,24,32,48,64,96,128,192,256,384,512,768,1024,1536,2048,3072,4096]
lines=[]
for att in ("GQA","MLA","DSA"):
  for L in (8192,131072):
    lines.append(f"\n[{att}, context {L}] best tok/s per kW-TDP at SLO (tok/J, bound, n, B)")
    for name,c in chips.items():
      cells=[]
      for slo in (100,400,1000):
        best=None
        for n in NS:
          for B in [2**i for i in range(15)]:
            r=step(c,B,L,att,n)
            if r and r["u"]>=slo and (best is None or r["kw"]>best[0]["kw"]): best=(r,n,B)
        cells.append(f"{best[0]['kw']:6.0f} ({best[0]['j']:.1f},{best[0]['bd']},{best[1]},{best[2]})" if best else "      -")
      lines.append(f"{name:10s} | "+" | ".join(cells))
print("\n".join(lines))
