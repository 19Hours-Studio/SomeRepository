# Round 2: add HiSparse-style LRU hot buffer (2x top-k, 87% hit, arXiv 2608.07009) to BOTH Vera offload and Continuum;
# shrink Continuum LPDDR to 4 SOCAMM2-class modules (assume ~175 GB/s each LPDDR6, 128 GB each).
NL, IDX, LAT, K = 61, 132, 656, 2048
W = 671e9*0.5625
def run(L, tps, stacks, hit, lp_bw, lp_eff, lp_cap, hot_mult=2, ndev=72, mtp=1.0):
    ic=IDX*L*NL; lc=LAT*L*NL; ib=ic*tps/mtp; gb=LAT*min(L,K)*NL*tps/mtp*1.0
    wc=W/ndev; wb=wc*tps/mtp
    hot=LAT*K*NL*hot_mult
    u=dict(hcap=(stacks*36e9*0.9-wc)/(ic+hot), hbw=(stacks*2.75e12*0.8-wb)/(ib+gb*hit),
           lbw=lp_bw*lp_eff/(gb*(1-hit)), lcap=lp_cap/lc)
    return min(u.values()), min(u,key=u.get)
L=131072
for mtp in [1.0, 1.8]:
  print(f"--- MTP tokens/step = {mtp} (indexer scan shared by draft+verify queries) ---")
  v,b=run(L,100,8,0.87,0.6e12,0.6,750e9,mtp=mtp); print(f"Rubin+Vera HiSparse: {v:6.1f}/GPU {v/8:5.1f}/stack bind={b}")
  c,b=run(L,100,4,0.87,0.7e12,0.5,512e9,mtp=mtp); print(f"Continuum-D 4 HBM4 + 4 LPDDR6 mods: {c:6.1f}/die {c/4:5.1f}/stack bind={b}")
  c0,b0=run(L,100,4,0.0,0.7e12,0.5,512e9,mtp=mtp); print(f"Continuum-D no hot buffer: {c0:6.1f}/die bind={b0}")
  # all-in-HBM Rubin (capacity bound)
  ic=IDX*L*NL; lc=LAT*L*NL; a=(8*36e9*0.9-W/72)/(ic+lc); print(f"Rubin all-HBM: {a:6.1f}/GPU {a/8:5.1f}/stack")
  # TPU Ironwood-like (8 HBM3e 24 GB, 7.37 TB/s), no large coherent host memory: all-HBM
  a2=(192e9*0.9-W/72)/(ic+lc); print(f"Ironwood all-HBM: {a2:6.1f}/chip {a2/8:5.1f}/stack")
  # Ironwood + Continuum-style LPDDR tier retrofit (keep 8 HBM3e: 0.92 TB/s/stack)
  icb=ic*100/mtp; gbb=LAT*K*NL*100/mtp
  u=dict(hcap=(192e9*0.9-W/72)/(ic+LAT*K*NL*2), hbw=(7.37e12*0.8-W/72*100/mtp)/(icb+gbb*0.87), lbw=0.7e12*0.5/(gbb*0.13), lcap=512e9/lc)
  print(f"Ironwood + LPDDR tier: {min(u.values()):6.1f}/chip bind={min(u,key=u.get)}")
# memory BOM per 128K user slot, 2026/2027 HBM price, LPDDR $10/GB; Vera CPU share counted at $0 (sunk) and at ~$2k/GPU (assumption)
for yr,h in [("2026",600),("2027",1300)]:
    v,_=run(L,100,8,0.87,0.6e12,0.6,750e9); c,_=run(L,100,4,0.87,0.7e12,0.5,512e9)
    print(yr, "Vera $/user", round((8*h+750*10)/v), "(+Vera die share)", round((8*h+750*10+2000)/v), "| Continuum $/user", round((4*h+512*10)/c))
