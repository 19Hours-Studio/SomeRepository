import sys
sys.path.insert(0, "/home/user/SomeRepository/engine/runs/refine_continuum_d/round1")
import model8 as e8
q = e8.q
L = ("0.55V wt", "0.60V wt", "0.65V wt", "0.55V", "0.60V")
ctx = q.C128
R = e8.gpu_env(e8.rubin_prof(150), ctx)
SN = dict(e8.C8_PARTS, comp_w=3300)
for lab, base, parts in [("SRAM 13.8GB (18 Mb/mm2)", dict(e8.C8, sram=13.8), e8.C8_PARTS),
                         ("SRAM 13.8GB + same node", dict(e8.C8, sram=13.8), SN),
                         ("SRAM 13.8GB + same node + eta0.5", dict(e8.C8, sram=13.8, F4=e8.C8["F4"]*5/6, F8=e8.C8["F8"]*5/6), SN)]:
    A = e8.c8_env(base, parts, ctx, labels=L)
    print(f"{lab:<36}", e8.fmt(A), "|", e8.rat(A, R))
    d = A[1000][1]; print("   >=1000:", d['C'], d['H'], d['npk'], d['stacks'], round(d['spd']))
