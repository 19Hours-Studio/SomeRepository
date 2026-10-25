# Idea 1: TCO per decode token, Rubin NVL72 vs bandwidth-sized part (same 22 TB/s => same tok/s when BW-bound)
sh=dict(pkg=.45,rack=.20,fac=.12,energy=.09,ops=.03,other=.11)   # ledger archetype A
rubin=55e3; hbm_gb=16.0  # DigiTimes ~$2/Gb (siliconanalysts tracker); idea uses 18.4
# BOM-level savings: 96 GB HBM, ~half compute silicon (~$1.5k on N3 2x reticle), smaller CoWoS (~$0.5k)
bom_save=96*hbm_gb+1500+500
# case a: vendor price falls only by BOM saving; case b: price scales with BOM (Rubin BOM ~ $10k est)
rubin_bom=288*hbm_gb+3000+1500+1000
for name,pk in [("BOM-only",bom_save/rubin),("const-margin",bom_save/rubin_bom)]:
    p=1-0.5*0.0  # power 1.64->1.34
    new=sh['pkg']*(1-pk)+sh['rack']*0.9+sh['fac']*(1.34/1.64)+sh['energy']*(1.34/1.64)+sh['ops']+sh['other']
    print(name,"pkg cut %.2f"%pk,"RATIO %.3f"%(1/new))
req=1-1/1.2; nonpkg=sh['rack']*0.1+(sh['fac']+sh['energy'])*(1-1.34/1.64)
print("pkg cut required for 1.2x: %.3f"%((req-nonpkg)/sh['pkg']))
# capacity check 128K, 300 tok/s
print("KV GB needed", 22e12/300/1e9, "+7.6 =",22e12/300/1e9+7.6, "vs 192 ->",192/(22e12/300/1e9+7.6))
# Idea 2: bandwidth density vs measured Alibaba (1.38 TB/s over 602 mm2)
need=27.6e12/4/400; meas=1.38e12/602.22
print("Idea2 GB/s/mm2 need %.1f meas %.2f margin %.3f"%(need/1e9,meas/1e9,meas/need))
# sanity: capacity per chiplet
print("GB/chiplet",64e6*400*2/8/1e9)
# Idea2 decode bytes/token, Kimi-K2-like: 384 experts top-8, 61 layers, FP8 MLA 656 B/tok/layer, 8K ctx
import math
kv_user=656*61*8192/1e9
W=500.0; expert_frac=0.95  # FP4 weights GB; ~95% in experts
users=300/kv_user; mb=users/32
touched=1-(1-8/384)**mb
bytes_tok_c=(W*(1-expert_frac)+W*expert_frac*touched)/mb + kv_user
tpkW_c=32*27.6e12/(bytes_tok_c*1e9)/(32*0.6)
# Rubin: 288 GB, 22 TB/s, 72 GPUs, ~2.3 kW; batch limited by capacity
kv_rack=72*288-550; users_r=kv_rack/kv_user
bytes_tok_r=550/users_r+kv_user
tpkW_r=72*22e12/(bytes_tok_r*1e9)/(72*2.3)
print("kv/user %.2f GB; cont users %d mb %.1f touched %.2f bytes/tok %.2f GB tok/s/kW %.0f"%(kv_user,users,mb,touched,bytes_tok_c,tpkW_c))
print("rubin users %d bytes/tok %.3f tok/s/kW %.0f  RATIO %.3f"%(users_r,bytes_tok_r,tpkW_r,tpkW_c/tpkW_r))
