# Own-stack session cost (errata policy, 50 turns) when KV is parked between turns in HBM vs DRAM, by tool gap.
import replay2 as R
HBM_GBS = 2 / 80 / 3600
for gap in (5, 30, 120, 600):
    out = {}
    for tier, rate in (("HBM", HBM_GBS), ("DRAM-capex", 4 / (3 * 8760 * 3600))):
        R.DRAM_GBS = rate
        x = R.avg("errata", seeds=20, gap_s=gap); out[tier] = x["own"]
    h, d = sum(out["HBM"]), sum(out["DRAM-capex"])
    print(f"gap {gap:4d}s: HBM-pinned ${h:.3f} (hold {out['HBM'][2]:.3f})  DRAM-parked ${d:.3f}  ratio {h/d:.2f}x"
          f"  | input-side only (prefill+hold): {(out['HBM'][0]+out['HBM'][2])/(out['DRAM-capex'][0]+out['DRAM-capex'][2]):.2f}x")
