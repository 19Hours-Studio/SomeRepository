# Idea 4 on a consistent basis: HBM rental ($2/h/80GB) vs DRAM rental ($0.005/GB-h), plus recompute (discard) option.
import replay2 as R
for gap in (5, 30, 120):
    out = {}
    for tier, rate in (("HBM", 2 / 80 / 3600), ("DRAMrent", 0.005 / 3600), ("DRAMcapex", 4 / (3 * 8760 * 3600))):
        R.DRAM_GBS = rate; out[tier] = sum(R.avg("errata", seeds=20, gap_s=gap)["own"])
    R.DRAM_GBS = 0
    disc = R.avg("inplace", seeds=20, edit_every=1, gap_s=gap)  # not used: discard-all proxy below
    print(f"gap {gap:3d}s HBM ${out['HBM']:.3f} DRAM-rental ${out['DRAMrent']:.3f} ({out['HBM']/out['DRAMrent']:.2f}x)"
          f" DRAM-capex ${out['DRAMcapex']:.3f} ({out['HBM']/out['DRAMcapex']:.2f}x)")
# discard-and-recompute every turn (InferCept 'discard'): prefill of full context each turn
R.DRAM_GBS = 0
tot = 0
for t in range(50):
    L = 10_000 + t * 2300 + (t // 5) * 200
    tot += R.own_cost(L, 0, 0, 300, 0)[0] + R.own_cost(L, 0, 0, 300, 0)[1]
print(f"discard+recompute every turn: ${tot:.3f}/session")
