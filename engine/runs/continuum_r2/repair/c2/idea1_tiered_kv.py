# Idea 1: indexer-in-HBM, MLA latent in LPDDR, hardware top-k gather. DeepSeek-V3.2 (DSA).
# Sources: 656 B/token latent, FlashMLA README / vLLM DSA blog; 132 B indexer key (128 FP8 + fp32 scale), Tensor Economics via aiwiki;
# 61 layers, 64 indexer heads, top-k 2048 (DeepSeek-V3.2 report); Rubin 288 GB / 8 HBM4 / 22 TB/s; Vera 1.5 TB LPDDR5X @1.2 TB/s, C2C 1.8 TB/s
# HBM4 12-Hi ~$550-600 (2026) / ~$1300 (2027) per 36 GB (TrendForce via Silicon Analysts); LPDDR ~$10/GB (TrendForce/wccftech)
# HBM3E 3.44 pJ/b (arXiv 2602.18568); LPDDR5X subsystem ~3.6 pJ/b (Vera)
NL, IDX, LAT, K = 61, 132, 656, 2048
W_FP4 = 671e9*0.5625                      # NVFP4 weights incl. 1 scale/16 = 377 GB
def per_user(L, tps=100):
    idx_cap = IDX*L*NL; lat_cap = LAT*L*NL
    idx_bw = idx_cap*tps; gat_bw = LAT*min(L,K)*NL*tps
    return idx_cap, lat_cap, idx_bw, gat_bw
def users_baselineA(L, stacks=8, cap=36e9, bw=2.75e12, ndev=72, tps=100, eff=0.8):
    ic, lc, ib, gb = per_user(L, tps)
    wcap = W_FP4/ndev; wbw = wcap*tps            # each device streams its weight shard every step
    u_cap = (stacks*cap*0.9 - wcap)/(ic+lc)
    u_bw = (stacks*bw*eff - wbw)/(ib+gb)
    return min(u_cap,u_bw), u_cap, u_bw
def users_vera(L, hit, stacks=8, ndev=72, tps=100, lp_bw_per_gpu=0.6e12, lp_eff=0.6, lp_cap_per_gpu=750e9):
    ic, lc, ib, gb = per_user(L, tps)
    wcap = W_FP4/ndev; wbw = wcap*tps
    hot = 0.10*lc*0 + LAT*K*NL*4                 # hot buffer: ~4x the top-k working set kept in HBM (assumption)
    u_hcap = (stacks*36e9*0.9 - wcap)/(ic+hot)
    u_hbw = (stacks*2.75e12*0.8 - wbw)/(ib + gb*hit)  # hits served from HBM
    u_lbw = lp_bw_per_gpu*lp_eff/(gb*(1-hit)+1e-9)
    u_lcap = lp_cap_per_gpu/lc
    return min(u_hcap,u_hbw,u_lbw,u_lcap), dict(hcap=u_hcap,hbw=u_hbw,lbw=u_lbw,lcap=u_lcap)
def users_continuum(L, stacks=4, lp_peak=1.5e12, lp_eff=0.6, lp_cap=512e9, ndev=72, tps=100):
    ic, lc, ib, gb = per_user(L, tps)
    wcap = W_FP4/ndev; wbw = wcap*tps
    u = dict(hcap=(stacks*36e9*0.9 - wcap)/ic, hbw=(stacks*2.75e12*0.8 - wbw)/ib,
             lbw=lp_peak*lp_eff/gb, lcap=lp_cap/lc)
    return min(u.values()), u
print("per-user @128K,100 tok/s: idx %.2f GB, latent %.2f GB, idx scan %.0f GB/s, gather %.1f GB/s"%tuple(x/1e9 for x in per_user(131072)))
ic,lc,ib,gb=per_user(131072)
print("HBM bytes/step today (FlashMLA sparse) %.3f GB vs Continuum %.3f GB -> ratio %.2f"%((ic+LAT*K*NL)/1e9, ic/1e9, (ic+LAT*K*NL)/ic))
print("dense MLA bytes/step %.2f GB"%(lc/1e9))
print("indexer BW/capacity demand = %.0f /s ; HBM4 stack BW/cap = %.0f /s"%(ib/ic, 2.75e12/36e9))
print()
for L in [8192, 32768, 131072, 524288]:
    a = users_baselineA(L); c, cu = users_continuum(L)
    print(f"L={L:>6}: Rubin-8stack users={a[0]:6.1f} (cap {a[1]:.0f}, bw {a[2]:.0f}) -> /stack {a[0]/8:5.1f} | "
          f"Continuum-4stack users={c:6.1f} {({k:round(v) for k,v in cu.items()})} -> /stack {c/4:5.1f} | ratio/stack {c/4/(a[0]/8):.2f}")
print()
L=131072
for hit in [0,0.5,0.7,0.8,0.9]:
    v,d = users_vera(L,hit); print(f"Vera-offload (ESS-like) hit={hit}: users/GPU={v:6.1f} /stack={v/8:5.1f}", {k:round(x) for k,x in d.items()})
# LPDDR gather efficiency sensitivity
print()
for eff in [0.3,0.4,0.5,0.6,0.8]:
    c,cu = users_continuum(L, lp_eff=eff); print(f"LPDDR gather eff {eff}: Continuum users {c:.1f}, binding {min(cu,key=cu.get)}")
# memory BOM per 128K user-slot
print()
for yr, hbm in [("2026",600),("2027",1300)]:
    a = users_baselineA(L)[0]; c,_ = users_continuum(L)
    bomA = 8*hbm; bomC = 4*hbm + 512*10
    v,_ = users_vera(L,0.8); bomV = 8*hbm + 750*10   # half a Vera's LPDDR per GPU
    print(f"{yr}: $/user-slot memory BOM: Rubin {bomA/a:6.0f}  Vera-offload(h=.8) {bomV/v:6.0f}  Continuum {bomC/c:6.0f}  -> A/C {bomA/a/(bomC/c):.2f}, V/C {bomV/v/(bomC/c):.2f}")
# energy per token (memory only), pJ/bit: HBM 3.44, LPDDR 3.6 + 0.5 PHY/D2D
eA = (ic+LAT*K*NL)*8*3.44e-12; eC = ic*8*3.44e-12 + LAT*K*NL*8*4.1e-12
print(f"\nmemory energy/token/user @128K: today {eA*1e3:.1f} mJ, Continuum {eC*1e3:.1f} mJ (ratio {eA/eC:.2f})")
# LPDDR6 random 656-B gather timing per 12-bit subchannel (14.4 Gb/s, ~19.2 GB/s data); tRC ~60 ns assumed (LPDDR5-class)
sub_bw=19.2e9; t_xfer=656/sub_bw; tRC=60e-9; banks=16
print(f"656B on one subchannel: {t_xfer*1e9:.0f} ns transfer; banks needed in flight to hide tRC: {tRC/t_xfer:.1f} of {banks}")
# critical path: per-layer gather latency budget at 100 tok/s
print(f"per-layer time budget {10e-3/NL*1e6:.0f} us; per-user per-layer gather {LAT*K/1e6:.2f} MB")
