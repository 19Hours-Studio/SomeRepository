# Corrected overlap (load exposed when miss-compute is short) + consistency checks
L=32; kv=131072; W=16e9; BW=3.35e12*0.8; eff=500e12; pcie=25e9; hbm=52e9
def pf(miss,hit): return (2*8e9*miss+2*L*4096*(miss*miss+2*miss*hit))/eff
for n_ctx,out,B in [(30000,400,6),(60000,500,3)]:
    t_dec=out*(W+B*n_ctx*kv)/BW/B
    full=pf(n_ctx,0)+t_dec
    hit=0.95*n_ctx; miss=n_ctx-hit
    load=hit*kv/pcie; pre=pf(miss,hit)
    tier=max(load,pre)+t_dec            # layer-pipelined: wall = max(load, compute)
    apc_gpu=pf(n_ctx*0.9,n_ctx*0.1)+t_dec   # S>=32: GPU-only hit ~0.05-0.2
    print(f"ctx {n_ctx}: load {load:.3f}s vs miss-prefill {pre:.3f}s (exposed), full prefill {pf(n_ctx,0):.2f}s; "
          f"GPU-s/req tier {tier:.2f} vs GPU-APC(hit .1) {apc_gpu:.2f} -> {apc_gpu/tier:.2f}x; audit 1%: +{0.01*pf(n_ctx,0)/tier:.2%}")
    # PCIe utilisation per GPU over operating time
    print(f"   avg PCIe use {load/tier*1:.0%} of time at 25 GB/s; avg rate {hit*kv/tier/1e9:.1f} GB/s")
    # NVMe write endurance if every new block spills to NVMe (1 DWPD, 3.84 TB drive per GPU)
    new_bytes=(n_ctx-hit)*kv          # new tokens per turn written
    w_day=new_bytes/tier*86400
    print(f"   NVMe writes {w_day/1e12:.1f} TB/day/GPU = {w_day/3.84e12:.1f} DWPD (limit 1.0 read-intensive)")
    print(f"   with second-hit admission (assume 30% blocks re-hit after DRAM eviction): {0.3*w_day/3.84e12:.2f} DWPD")
# DRAM bandwidth node: 8 GPUs x avg rate vs ~600 GB/s (2-socket DDR5)
