import math
print("== sanity: B200 FP8 ridge 4.5e15/8e12 =", 4.5e15/8e12, "FLOP/B (known ~562)")
# GEMM intensity check: square 8192 FP8
n=8192; print("GEMM 8192^3 FP8 intensity", 2*n**3/(3*n*n), "(known 2n/3=5461)")

print("\n== IDEA 1: HBM base-die attention ==")
# RPU paper (arXiv 2602.18568) modeled HBM3e: total 3.44 pJ/b; I/O 0.25 pJ/b; TSV 0.148/layer; act 0.18
tot=3.44; io=0.25; host_phy=0.25  # assume symmetric host-side PHY
saved=io+host_phy
print("energy saved by skipping PHY/interposer: %.2f of %.2f pJ/b = %.0f%%"%(saved,tot,100*saved/tot))
req=3.9-1.5; print("idea requires saving %.1f pJ/b; MARGIN=%.2f"%(req,saved/req))
# GQA intensity: group g=8, FP8 KV -> 2g FLOP/B
print("GQA g=8 FP8 intensity", 2*8, "FLOP/B")
# chain archetype C: HBM 50% of decode energy, KV ~60% of HBM bytes at 16K (est), saved fraction
kv_share=0.5*0.6; f=saved/tot
print("chain: energy/token ratio = %.3f"%(1/(1-kv_share*f)))

print("\n== IDEA 2: SRAM weights + LPDDR KV ==")
sram_mbmm2=31.8  # Mib/mm2 N3E (WikiChip/Tom's)
print("1 GiB SRAM area at N3E: %.0f mm2"%(8192/sram_mbmm2))
# MLA KV per token DeepSeek-V3: (512+64)*61 layers, FP8
kv_tok=(512+64)*61; print("MLA KV/token FP8 %.1f KB; 32K user %.2f GB (BF16 %.2f)"%(kv_tok/1e3,kv_tok*32768/1e9,2*kv_tok*32768/1e9))
ai_mla=(2*128*576+2*128*512)/576; print("MLA absorbed decode intensity ~%.0f FLOP/B"%ai_mla)
dies=340; bw=1e12; eff=0.7; ctx=8.5e3; tps_user=100
kv_user=kv_tok*ctx
users=dies*bw*eff/(kv_user*tps_user); Y=users*tps_user
print("users@%dtok/s, ctx %.1fK: %.0f ; throughput %.0f tok/s"%(tps_user,ctx/1e3,users,Y))
att_tf=ai_mla*bw*eff/1e12; moe_tf=Y*2*37e9/dies/1e12
print("per-die FP8 compute need: attention %.0f TF + MoE %.0f TF"%(att_tf,moe_tf))
# die cost
wafer=20000; area=800; d=300
gross=math.pi*(d/2)**2/area - math.pi*d/math.sqrt(2*area)
y=0.75; die=wafer/(gross*y)
print("gross dies/wafer %.0f, die cost @%.0f%% yield $%.0f"%(gross,y*100,die))
lp_gb=16; lp_price=145.9/12  # $/GB Q2-2026 LPDDR5X contract (Utmel)
pkg=150; system=1500
per=die+lp_gb*lp_price+pkg+system; tot2=per*dies
print("LPDDR $/GB %.1f; per-die all-in $%.0f; 340 dies $%.2fM; MARGIN vs $1.5M = %.2f"%(lp_price,per,tot2/1e6,1.5e6/tot2))
# NVL72 reference: ledger $0.04-0.08/Mtok owned TCO; assume owned TCO $1.4/GPU-hr
X=72*1.4/(0.06e-6*3600); print("NVL72 implied throughput %.0f tok/s"%X)
nvl_bom=72*6400+600e3  # GPU BOM (Epoch) + est rest-of-rack BOM
hw=(tot2/nvl_bom)/(Y/X); pw=(dies*350/132e3)/(Y/X)
cost=55*hw+35*pw+10
print("hw cost/throughput %.2f, power/throughput %.2f -> RATIO %.2f"%(hw,pw,100/cost))
# 32K context case
users32=dies*bw*eff/(kv_tok*32768*tps_user); print("32K ctx users %.0f thr %.0f"%(users32,users32*tps_user))

print("\n== IDEA 3: memory-light prefill die ==")
# Rubin CPX-like: 30 PF NVFP4, assume LPDDR 1 TB/s -> ridge for FP4 weights
ridge=30e15/1e12; print("ridge FP4 die w/ 1TB/s LPDDR: %.0f FLOP/B (idea assumes 300)"%ridge)
# MoE expert intensity at FP4 weights (0.5B/param): 4*tokens_per_expert
need_tpe=ridge/4; print("tokens/expert needed %.0f -> global tokens per step %.0f (top8/256)"%(need_tpe,need_tpe*256/8))
print("MARGIN on stated 300 FLOP/B rule = %.3f (300/ridge means rule underestimates)"%(300/ridge))
# chain: prefill share p of fleet, prefill die cost per FLOP k x cheaper
for p in (0.3,0.5):
  for k in (2,3):
    print(" p=%.1f k=%d RATIO %.2f"%(p,k,1/(1-p+p/k)))

print("\n== IDEA 4: HBM-lean training ==")
alpha=math.log(4.5)/math.log(16); ret=0.5**alpha
print("power-law alpha %.2f (arXiv 2506.15006 16x BW->4.5x); half-BW throughput retention %.2f"%(alpha,ret))
print("MARGIN retention/0.85 = %.2f"%(ret/0.85))
# chain archetype B: hardware 44 (BOM ~18% of price; HBM 45% of BOM), net 13, staff 33, energy 4, other 6
bom_frac=6400/35000; hbm=0.45; sram_add=0.05
chip_cost=1-bom_frac*(hbm/2-sram_add)
for r in (ret,0.85):
  c=44*chip_cost/r+13/r+33+4/r+6/r
  print(" retention %.2f: chip cost x%.3f -> RATIO %.2f"%(r,chip_cost,100/c))
