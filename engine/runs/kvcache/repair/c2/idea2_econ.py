"""Idea 2 economics: admission threshold implied by the anchor score in $ terms, and SSD endurance load."""
gpu = {"H100 8B": (2.5, 4.0e14), "H800/H200 DSv3": (3.0, 4.0e14)}   # $/GPU-h, effective prefill FLOP/s (assumptions)
models = {"H100 8B": (16e9, 65536), "H800/H200 DSv3": (74e9, 70272)}   # linear FLOP/token, bytes/token
ssd_usd_tb, dwpd, years = 160.0, 1.0, 5                               # PM9A3-class retail ~$163/TB, 1 DWPD
usd_per_byte_written = ssd_usd_tb / 1e12 / (dwpd * 365 * years)
print(f"SSD wear cost: ${usd_per_byte_written*1e12:.3f} per TB written")
for k in models:
    usd_h, eff = gpu[k]; lin, bpt = models[k]
    usd_flop = usd_h / 3600 / eff
    thr = usd_per_byte_written / usd_flop          # FLOP/byte needed per unit reuse prob
    dens0 = lin / bpt                              # FLOP/byte of a shallow block (attention adds more)
    print(f"{k}: $/FLOP {usd_flop:.2e}; break-even P(reuse) for shallow block = {thr/dens0:.3f}")
# endurance load, DeepSeek-like prefill node: 73.7k input tok/s/node (DeepSeek day-6), 56.3% hit (CloudMatrix paper)
tok_new = 73.7e3 * (1 - 0.563)
for name, bpt in [("DSv3 MLA BF16", 70272), ("Llama-8B FP8", 65536), ("Llama-70B BF16", 327680)]:
    gbs = tok_new * bpt / 1e9; tb_day = gbs * 86400 / 1e3
    drives_1dwpd = tb_day / 7.68
    print(f"{name}: write-all {gbs:.2f} GB/s = {tb_day:.0f} TB/day -> {drives_1dwpd:.0f} x 7.68TB 1-DWPD drives of endurance per node"
          f"; wear ${tb_day*usd_per_byte_written*1e12:.1f}/day vs 8-GPU node ${8*3*24:.0f}/day")
