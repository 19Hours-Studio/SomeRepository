"""Does the GPU model reproduce the measured fall of per-GPU throughput with interactivity?
InferenceX (interpolated): GB300 NVL72 V4-Pro 8k/1k FP4: 2,209 tok/s/GPU @93 tok/s/user, 750 @133.
                           GB300 NVL72 R1 1k/1k FP4: 10,008 @88, 1,967 @162, 232 @235.
Shape test only (ratios between interactivity points), so the input/output token-counting ambiguity cancels."""
import sys; sys.path.insert(0, "/home/user/SomeRepository/engine/runs/refine_continuum_d/round1")
import model8 as e8
q, m = e8.q, e8.m
GB300 = dict(m.SYS["GB300"], P=1.0, s=1.0, imb=q.IMB_G)
def best(M, ctx, floor, ks=range(4), p=0.8):
    bb = 0
    for k in ks:
        for pt in m.gpu_points(GB300, 10e-6, ctx, k, p, M=M):
            if pt[0] >= floor: bb = max(bb, pt[1] / m.DERATE)
    return bb
for M, ctx, pts in ((m.V4, 8704, ((93, 2209), (133, 750))), (m.R1, 1536, ((88, 10008), (162, 1967), (235, 232)))):
    print(M["name"], f"ctx {ctx}")
    base = None
    for ks, lab in ((range(1), "no MTP"), (range(4), "MTP k<=3")):
        row = []
        for fl, meas in pts:
            v = best(M, ctx, fl, ks); row.append((fl, meas, v))
        r0 = row[0]
        print(f"  {lab:<9}" + "  ".join(f"@{fl}: model {v:9,.0f} meas {meas:6,} meas/model {meas/v:.3f} (rel {meas/v/(r0[1]/r0[2]):.2f})" for fl, meas, v in row))
    mx = max(pt[0] for k in range(8) for pt in m.gpu_points(GB300, 10e-6, ctx, k, 0.8, M=M))
    print(f"  model max tok/s/user on GB300: {mx:,.0f}")
