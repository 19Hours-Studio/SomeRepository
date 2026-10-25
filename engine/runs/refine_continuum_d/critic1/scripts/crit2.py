"""(1) Ultra 2-die at 192 GB (8-high HBM4, per SemiAnalysis-sourced reports) vs answer's 512 GB.
(2) Silicon per token including HBM DRAM + base dies (assumption: ~120 mm2 per DRAM die and per base die)."""
import sys; sys.path.insert(0, "/home/user/SomeRepository/engine/runs/refine_continuum_d/round1")
import model8 as e8
q, m = e8.q, e8.m
L = ("0.55V wt", "0.60V wt", "0.55V")
for ctx in (q.C128, q.C1M):
    A = e8.c8_env(e8.C8, e8.C8_PARTS, ctx, labels=L)
    for hbm in (512, 192):
        base = dict(q.RUBIN, hbm=hbm, P=q.RUBIN["P"] + 100 - 150, P_maxq=q.RUBIN["P_maxq"] + 100 - 150)
        U = e8.gpu_env(q.profiles(base, comp_w=1720, leak_w=150, other_w=0, rack_share=0.83), ctx)
        print(f"{ctx//1024}K C8 / Ultra-2die {hbm} GB: {e8.rat(A, U)}   (Ultra {e8.fmt(U)})")
# silicon incl. DRAM (per-package figures from supply8.txt)
die = 1.20  # cm2 per HBM DRAM or base die (assumption)
for t, tc, tr, st in ((200, 128824, 76472, 1.71), (1000, 128824, 57126, 1.71), (2000, 109474, 29981, 1.07)):
    c8 = 30 + 60 + st * 17 * die; rb = 16.5 + 8 * 13 * die
    print(f">={t}: silicon cm2/pkg C8 {c8:.0f} (logic+SRAM 90, DRAM {st*17*die:.0f}) Rubin {rb:.0f} (logic 16.5, DRAM {8*13*die:.0f})"
          f" -> per-token C8/Rubin incl DRAM {(c8/tc)/(rb/tr):.2f}; excl DRAM {(90/tc)/(16.5/tr):.2f}")
