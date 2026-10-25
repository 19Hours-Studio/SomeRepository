# Idea 4 re-check: recompute cost incl. attention FLOPs; DRAM/NVMe on a capex basis; NVMe load time.
L, d, gpu_hr, eff = 80, 8192, 2.0, 0.45*989e12
b = 2*80*8*128*2  # bytes/token Llama-3-70B BF16
lin = 2*70e9
for ctx in (0, 32_000, 100_000):
    att = 4*L*d*(ctx/2)          # QK^T + AV, avg position ctx/2 over a ctx-long prefill
    usd = (lin+att)/eff*gpu_hr/3600*1e6
    print(f"prefill ctx={ctx:>7,}: ${usd:.3f}/M tok (attention adds {att/lin:.0%})")
for tier, gbh in [("DRAM cloud-rental 0.005", 0.005), ("DRAM capex $4/GB over 3y", 4/(3*8760)),
                  ("NVMe cloud 0.0002", 0.0002), ("NVMe capex $0.08/GB over 3y", 0.08/(3*8760))]:
    store = gbh*b*1e6/1e9
    for rc in (0.175, 0.337):
        print(f"{tier:28s} ${store:.4f}/M-tok-h ; break-even reuse interval at recompute ${rc}: {rc/store:.2f} h")
for bw in (7e9, 25e9, 50e9):
    print(f"load 100k-tok 70B BF16 ({b*1e5/1e9:.1f} GB) at {bw/1e9:.0f} GB/s: {b*1e5/bw:.1f} s")
print(f"recompute 100k tok on 1 H100 (linear only): {1e5*lin/eff:.0f} s; on 8 H100: {1e5*lin/eff/8:.1f} s")
print("Gemini 2.5 Pro explicit cache storage $4.50/M-tok-h vs input $1.25/M -> 3.6x input price per hour")
