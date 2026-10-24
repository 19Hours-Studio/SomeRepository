"""System-level decode roofline + $/Mtok for Idea 1 (Continuum-D) and Idea 2 (expert-stationary stack).
Same derates for every system: BW_EFF of peak bandwidth, FL_EFF of peak FLOPs."""
import math
from model import per_token, W_BYTES, P_EXPERTS, B_FP4, L, MOE_L, p_exp, N_EXP

BW_EFF, FL_EFF = 0.6, 0.45          # EST, applied to all systems
YEARS, UTIL = 4, 0.7                # EST amortisation, fleet utilisation
KWH, PUE = 0.08, 1.25               # EST $/kWh, facility overhead

def usd_per_mtok(capex, kw, tps):
    if tps <= 0: return float('inf')
    per_s = capex / (YEARS * 365 * 86400) + kw * PUE * KWH / 3600
    return per_s / (tps * UTIL) * 1e6

def pool_users(T, bw, cap, flops, rd, ft, fl, w_read=0.0, w_res=0.0):
    """users one memory pool / compute unit can serve at step time T"""
    u_bw = (bw * BW_EFF * T - w_read) / rd
    u_cap = (cap - w_res) / ft
    u_fl = flops * FL_EFF * T / fl
    return max(0.0, min(u_bw, u_cap, u_fl)), (u_bw, u_cap, u_fl)

# ---------- Rubin NVL72 (SRC: 288 GB, 22 TB/s HBM4/GPU; $7.8M Morgan Stanley; EST FP8 dense 17.5 PF, ~190 kW) ----------
VR = dict(n=72, bw=22e12, cap=288e9, fl=17.5e15, capex=7.8e6, kw=190)
GPU_FLOOR = 2.5e-3   # EST: wide-EP decode step floor (116 all-to-alls + kernels), i.e. <=400 tok/s/user

def vr_hbm(T, ctx, sparse):
    if T < GPU_FLOOR: return 0, None
    rd, fl, ft = per_token(ctx, sparse)
    wsh = W_BYTES / VR['n']
    u, lim = pool_users(T, VR['bw'], VR['cap'], VR['fl'], rd, ft, fl, wsh, wsh)
    return u / T * VR['n'], lim

# GPU + ESS-style offload (FACT 22): latent cache in Vera LPDDR5X (1.5 TB, 1.2 TB/s per Vera, 1 Vera per 2 GPUs, SRC FACT 5),
# indexer keys stay in HBM; a fraction REUSE of top-k latents per step is already resident in HBM (EST).
REUSE = 0.5
def vr_ess(T, ctx, sparse):
    if T < GPU_FLOOR or not sparse: return vr_hbm(T, ctx, sparse)
    rd, fl, ft = per_token(ctx, sparse)
    from model import KV_MLA, KV_IDX, TOPK_TOK
    idx_rd = L * ctx * KV_IDX; lat_rd = L * min(ctx, TOPK_TOK) * KV_MLA
    idx_ft = L * ctx * KV_IDX; lat_ft = L * ctx * KV_MLA
    wsh = W_BYTES / VR['n']
    u_hbm = (VR['bw'] * BW_EFF * T - wsh) / (idx_rd + lat_rd * REUSE)
    u_hcap = (VR['cap'] - wsh) / (idx_ft + 3 * min(ctx, TOPK_TOK) * L * KV_MLA)  # indexer + hot latent working set
    u_lp = 0.6e12 * BW_EFF * T / (lat_rd * (1 - REUSE))
    u_lcap = 0.75e12 / lat_ft
    u_fl = VR['fl'] * FL_EFF * T / fl
    u = max(0, min(u_hbm, u_hcap, u_lp, u_lcap, u_fl))
    return u / T * VR['n'], (u_hbm, u_hcap, u_lp, u_lcap, u_fl)

# ---------- Continuum-D (Idea 1) ----------
def die_cost(area=800, wafer=19500, d0=0.07, logic_mm2=330, pkg=150, test=60):
    dpw = math.pi * 150**2 / area - math.pi * 300 / math.sqrt(2 * area)
    y = math.exp(-d0 * logic_mm2 / 100) * 0.97           # SRAM portion repairable
    return wafer / (dpw * y) + pkg + test, dpw, y

SRAM_MIB_MM2 = 31.8 * 0.55     # SRC bitcell density (FACT 9) x EST 55% macro efficiency (V-Cache shows 38% incl. TSVs)
def continuum_d(lp_price=10, lp_gb=64, lp_bw=1.0e12, die_fl=0.51e15, sram_gb=1.0):
    exp_per_die = int(sram_gb * 1e9 * 0.9 // (p_exp * B_FP4))            # 10% for attention weights + buffers
    dies_per_stage = math.ceil(N_EXP / exp_per_die)
    spares = 1
    n = MOE_L * (dies_per_stage + spares) + 3 + 2                         # + dense layers + embed/head
    c_die, dpw, y = die_cost()
    board = 1200                                                          # EST board, VRM, share of chassis/NIC/host
    capex = n * (c_die + lp_gb * lp_price + board) + 150e3                # EST + hosts/switches for prefill hand-off
    kw = n * 0.30 * 1.15                                                  # EST 300 W/die incl. LPDDR, 15% overhead
    sram_mm2 = sram_gb * 1e9 * 8 / 2**20 / SRAM_MIB_MM2
    return dict(n=n, active=n - MOE_L * spares, dps=dies_per_stage, exp_per_die=exp_per_die, c_die=c_die,
                capex=capex, kw=kw, bw=lp_bw, cap=lp_gb * 1e9, fl=die_fl, sram_mm2=sram_mm2, dpw=dpw, y=y)
CD_FLOOR = 61 * 6e-6 + 0.1e-3   # EST: 61 stages x (2 C2C hops ~1us + ~4us compute) + 0.1 ms sampling

def cd_tps(cd, T, ctx, sparse):
    if T < CD_FLOOR: return 0, None
    rd, fl, ft = per_token(ctx, sparse)
    u, lim = pool_users(T, cd['bw'], cd['cap'], cd['fl'], rd, ft, fl)   # weights never touch LPDDR
    return u / T * cd['active'], lim

if __name__ == "__main__":
    cd = continuum_d()
    print(f"Continuum-D: {cd['n']} dies ({cd['dps']}+1 per MoE stage, {cd['exp_per_die']} experts/die), die ${cd['c_die']:.0f} "
          f"(dpw {cd['dpw']:.0f}, yield {cd['y']:.2f}), SRAM 1 GB = {cd['sram_mm2']:.0f} mm2, capex ${cd['capex']/1e6:.2f}M, {cd['kw']:.0f} kW")
    print("\n tok/s/user  ctx  sparse |  VR-HBM tok/s  $/Mtok | VR+ESS tok/s  $/Mtok | Cont-D tok/s  $/Mtok (LP $10) $/Mtok (LP $21)")
    cd21 = continuum_d(lp_price=21)
    for s in (50, 100, 200, 400, 1000):
        T = 1 / s
        for ctx, sp in ((32768, False), (131072, True), (32768, True)):
            a, _ = vr_hbm(T, ctx, sp); b, _ = vr_ess(T, ctx, sp); c, lim = cd_tps(cd, T, ctx, sp); c21, _ = cd_tps(cd21, T, ctx, sp)
            print(f" {s:5d} {ctx//1024:5d}K {str(sp):6s} | {a:10.0f} {usd_per_mtok(VR['capex'],VR['kw'],a):7.3f} | "
                  f"{b:10.0f} {usd_per_mtok(VR['capex'],VR['kw'],b):7.3f} | {c:10.0f} {usd_per_mtok(cd['capex'],cd['kw'],c):7.3f} "
                  f"{usd_per_mtok(cd21['capex'],cd21['kw'],c21):7.3f}  lim(bw,cap,fl)={tuple(round(x,1) for x in lim) if lim else None}")
