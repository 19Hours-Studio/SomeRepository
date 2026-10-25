"""Round 7: extreme Ultra bound (vendor 600 kW at 100 PF AND the undervolt law on top), supply arithmetic.
Usage: python3 run7e.py > run7e.txt"""
import model7 as q, model5 as m, run7 as r7
for ctx in (q.C128, q.C1M):
    A = q.pipe_env(q.cont_prof(q.C7T, q.C7T_PARTS), ctx, gs=(1, 2, 3, 4, 6))
    U = q.gpu_env(q.profiles(dict(q.ultra(600e3 / 144), P_maxq=600e3 / 144), comp_w=3440 * 4167 / 5690, leak_w=300 * 4167 / 5690,
                             other_w=0, rack_share=1, vendor_maxq=False), ctx)
    print(f"{ctx//1024}K C7 / Ultra(vendor 600 kW @100 PF + undervolt law): {q.ratio(A, U)}   Ultra picks {[U[t][1] for t in q.T]}")
# supply per GW at the >=200 point, 128K
good_per_wafer = 46          # 750 mm2 on 300 mm: ~72 candidates, ~65% good with tile harvesting
for name, slotW, cdies, stacks, cm2 in (("C6 (MaxQ, round 6)", 2443, 2, 3, 15), ("C7T (0.55 V)", 2542, 4, 4, 30)):
    pk = 1e9 / slotW
    wafers = pk * cdies / good_per_wafer
    print(f"{name}: {pk/1e3:,.0f}k packages/GW, {pk*cdies/1e6:.2f}M C-dies, {wafers/1e3:.0f}k C-die wafers, "
          f"{2*wafers/1e3:.0f}k SoIC bonding passes (2 tiers per C-die) = {2*wafers/15e3:.1f}-{2*wafers/10e3:.1f} months of 10-15k wpm; "
          f"{pk*stacks/1e6:.2f}M HBM stacks/GW; {pk*cm2/1e6:.1f}M cm2 leading-edge logic/GW")
pk = 1e9 / 1981
print(f"Rubin (0.60 V slot 1981 W): {pk/1e3:,.0f}k GPUs/GW, {pk*8/1e6:.2f}M HBM stacks/GW, {pk*16.5/1e6:.1f}M cm2 N3P logic/GW")
