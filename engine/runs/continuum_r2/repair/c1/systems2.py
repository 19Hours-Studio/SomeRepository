"""Best-baseline-at-SLA table for Idea 1, LPX+VR baseline, and Idea 2 (expert-stationary stacked SRAM)."""
import math
from systems import *
from model import per_token, W_BYTES

# best GPU option at SLA >= s : operator may pick HBM-only or ESS offload and any faster step time
def best_gpu(s, ctx, sp):
    best = float('inf')
    for s2 in range(s, 401, 10):
        for f in (vr_hbm, vr_ess):
            t, _ = f(1 / s2, ctx, sp)
            best = min(best, usd_per_mtok(VR['capex'], VR['kw'], t))
    return best

# LPX + VR attention/FFN disaggregation. SRC: 256 LP30/rack, 500 MB SRAM, 1.2 PF FP8.
# EST: LPX rack $3.5M and 130 kW (no public price); AFD step floor 1.2 ms; experts FP4 need ceil(368/128)=3 racks.
LPX_RACK, LPX_KW, AFD_FLOOR = 3.5e6, 130, 1.2e-3
def lpx_vr(T, ctx, sp, n_lpx=3):
    if T < AFD_FLOOR: return 0
    rd, fl_tot, ft = per_token(ctx, sp)
    fl_att = fl_tot - 2 * 37e9
    u, _ = pool_users(T, VR['bw'], VR['cap'], VR['fl'], rd, ft, fl_att, 11e9 / 72 * 0.5, 11e9 / 72)
    return u / T * 72
def lpx_cost(t, n_lpx=3): return usd_per_mtok(VR['capex'] + n_lpx * LPX_RACK, VR['kw'] + n_lpx * LPX_KW, t)

cd = continuum_d(); cd21 = continuum_d(lp_price=21)
print("IDEA 1: $/Mtok at SLA (best GPU = min over HBM-only/ESS offload and any faster step)")
print(" SLA   ctx    sparse | best VR  | LPX+VR  | Cont-D $10 | Cont-D $21 | ratio bestVR/CD, LPX/CD")
for s in (50, 100, 200, 400, 1000):
    for ctx, sp in ((32768, False), (131072, True), (32768, True)):
        g = best_gpu(s, ctx, sp) if s <= 400 else float('inf')
        lx = min(lpx_cost(lpx_vr(1/s2, ctx, sp)) for s2 in range(s, max(s, 830) + 1, 10))
        c = usd_per_mtok(cd['capex'], cd['kw'], cd_tps(cd, 1/s, ctx, sp)[0])
        c21 = usd_per_mtok(cd21['capex'], cd21['kw'], cd_tps(cd21, 1/s, ctx, sp)[0])
        print(f" {s:4d} {ctx//1024:4d}K {str(sp):6s} | {g:7.3f}  | {lx:7.3f} | {c:9.3f}  | {c21:9.3f}  | {g/c:5.2f} {lx/c:5.2f}")

# ---- sensitivity of Continuum-D at the target point (128K DSA, 200 tok/s) ----
print("\nIDEA 1 sensitivity @128K DSA, 200 tok/s/user ($/Mtok, best VR = %.3f)" % best_gpu(200, 131072, True))
for label, kw in [("base", {}), ("LPDDR 0.7 TB/s", dict(lp_bw=0.7e12)), ("LPDDR 1.5 TB/s", dict(lp_bw=1.5e12)),
                  ("LP $21/GB", dict(lp_price=21)), ("SRAM 0.75 GB/die", dict(sram_gb=0.75)), ("LPDDR 128 GB", dict(lp_gb=128))]:
    x = continuum_d(**kw); t = cd_tps(x, 1/200, 131072, True)[0]
    print(f"  {label:18s} dies {x['n']:4d} capex ${x['capex']/1e6:.2f}M  {t:8.0f} tok/s  ${usd_per_mtok(x['capex'], x['kw'], t):.3f}")

# ================= IDEA 2 =================
print("\nIDEA 2: expert-stationary stacked SRAM")
MB_MM2_VC = 64 / 36                      # SRC AMD V-Cache, N7
MB_MM2 = MB_MM2_VC * 0.027 / 0.021       # EST scale by bitcell N7 HD 0.027 -> N5/N3E 0.021 um^2 (FACT 9)
DIE_MM2 = 800
def stack_gb(layers, dies): return layers * dies * DIE_MM2 * MB_MM2 / 1e3
K2_EXP = 384 * 60 * 3 * 7168 * 2048 * B_FP4  # Kimi K2 routed experts FP4 (SRC config: 384 exp, 61 layers/1 dense, ff 2048)
V3_EXP = P_EXPERTS * B_FP4
for layers in (2, 3, 4):
    g = stack_gb(layers, 144)
    print(f"  {layers}-high x 144 dies: {g:.0f} GB/rack ({g/72:.1f}/GPU); margin V3 {g/(V3_EXP/1e9):.2f}  K2 {g/(K2_EXP/1e9):.2f}")
print(f"  (original claim: 64 chips x4 x800mm2 at {MB_MM2_VC:.2f} MB/mm2 = {stack_gb(4,64)*MB_MM2_VC/MB_MM2:.0f} GB)")

# rack scale gain: weight-read time per step saved = W/(N*BW*eff)
for name, W, N in (("V3 rack EP72", W_BYTES, 72), ("K2 rack EP72", 1.04e12 * B_FP4, 72)):
    t_w = W / N / (22e12 * BW_EFF)
    print(f"  {name}: weight read/step {t_w*1e3:.2f} ms -> gain at 2.5 ms step {2.5e-3/(2.5e-3 - t_w):.2f}x, at 5 ms {5e-3/(5e-3-t_w):.2f}x")

# node scale: gpt-oss-120b on 8 GPUs (SRC model card: 116.8B total, 5.1B active, 36 layers, 128 exp top-4,
# 64 q heads, 8 kv heads x 64, alternating 128-token sliding window). MXFP4 checkpoint ~ 63 GB.
OSS_W, OSS_ACT, OSS_L = 63e9, 5.1e9, 36
def oss_tok(ctx):
    full = OSS_L // 2; kvb = 2 * 8 * 64 * 1   # FP8 K+V bytes/token/layer
    rd = kvb * (full * ctx + full * min(ctx, 128)); fl = 2 * OSS_ACT + 2 * 2 * 64 * 64 * (full * ctx + full * 128)
    return rd, fl, rd
NODE = dict(n=8, bw=22e12, cap=288e9, fl=17.5e15)
NODE_CAPEX, NODE_KW = 7.8e6 / 72 * 8 * 1.1, 190 / 72 * 8       # EST pro-rata Rubin node
SRAM_ADD = 16 * 4 * (15e3 / 65 / 0.85 + 100)                   # EST 16 dies x 4 layers, N5 wafer $15k, +$100 bond/KGD
FLOOR_BASE_NODE = OSS_L * 15e-6                                # EST per-layer kernel + intra-node all-to-all
print(f"  node SRAM: {stack_gb(4,16):.0f} GB vs gpt-oss {OSS_W/1e9:.0f} GB (margin {stack_gb(4,16)/(OSS_W/1e9):.2f}); SRAM add ${SRAM_ADD/1e3:.0f}k on ${NODE_CAPEX/1e6:.2f}M")
print("   SLA  ctx | base tok/s $/Mtok | stacked tok/s $/Mtok | gain")
for s in (200, 500, 800, 1000, 1500):
    T = 1 / s
    for ctx in (8192, 32768):
        rd, fl, ft = oss_tok(ctx)
        t_w = OSS_W / 8 / (22e12 * BW_EFF)
        ub = pool_users(T, NODE['bw'], NODE['cap'], NODE['fl'], rd, ft, fl, OSS_W / 8, OSS_W / 8)[0] if T > FLOOR_BASE_NODE + t_w else 0
        us = pool_users(T, NODE['bw'], NODE['cap'], NODE['fl'], rd, ft, fl)[0] if T > FLOOR_BASE_NODE else 0
        tb, ts = ub / T * 8, us / T * 8
        cb, cs = usd_per_mtok(NODE_CAPEX, NODE_KW, tb), usd_per_mtok(NODE_CAPEX + SRAM_ADD, NODE_KW * 1.06, ts)
        print(f"  {s:5d} {ctx//1024:3d}K | {tb:9.0f} {cb:7.3f} | {ts:9.0f} {cs:7.3f} | {cb/cs if cs < 1e9 else 0:.2f}")
