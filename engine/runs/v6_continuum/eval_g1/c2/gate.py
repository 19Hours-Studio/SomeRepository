# known-answer check: V-Cache density 64 MB (512 Mb) / 36 mm^2
print("vcache Mb/mm2", 512/36)
W=545e9; bw=22e12; hbm=288e9; L=61; kvb=656  # Kimi-K2/DeepSeek-class MLA, FP8 KV (FACT 6)
for n_rubin in (72,):
  for ctx in (8192,131072):
    for tps in (300,100):
      step=1/tps; per_gpu_bytes=bw*step
      wshard=W/n_rubin; kv_user=L*kvb*ctx
      w_share=wshard/per_gpu_bytes
      users_bw=(per_gpu_bytes-wshard)/kv_user; users_cap=(hbm-wshard)/kv_user
      users_sram=per_gpu_bytes/kv_user
      gain=min(users_sram,hbm/kv_user)/min(users_bw,users_cap)
      print(ctx,tps,"weight share %.3f"%w_share,"users bw %.0f cap %.0f"%(users_bw,users_cap),"per-pkg gain %.3f"%gain)
# idea packages: SRAM per package
for tsv in (1.0,0.9):
  gb=2*800*14.2e6/8*tsv/1e9; print("SRAM GB/pkg",round(gb,2),"pkgs",W/1e9/gb)
