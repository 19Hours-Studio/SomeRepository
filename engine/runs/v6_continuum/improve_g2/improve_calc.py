"""improve_g2: recompute the deciding number for each of the three answers.

Sourced inputs (see evidence.md / ceilings.md unless stated):
  AMD V-Cache 64 MB on ~36 mm2 N7 -> 14.2 Mb/mm2 (FACT 1)
  A100: 624 TOPS INT8 dense, 826 mm2, TSMC N7 (Nvidia A100 datasheet/whitepaper) -> 0.755 TOPS/mm2 whole die
  Llama-3.3-70B: 80 layers, d=8192, 64 q heads, 8 KV heads x128, 70.6B params (Meta config)
  NVFP4 ~4.5 bit/value for weights and KV (user notes)
  Groq $0.79/Mtok, Cerebras $0.60-1.20/Mtok list for Llama-3.3-70B (FACT 17)
  CS-3 ~$3.2M, 44 GB SRAM -> ~$57-73k/GB (FACT 2/11)
  Hybrid-bonded logic-to-DRAM 64 Mb/mm2 measured (FACT 14, ISSCC 2022)
  SeDRAM 135 GB/s/Gb @0.66 pJ/b (VLSI 2023), 34 GB/s/Gb @0.88 pJ/b (IEDM 2020) (FACT 8)
  Rubin 288 GB HBM4, 22 TB/s, ~2.3 kW TDP analyst (FACT 12); HBM3E 3.44-5.74 pJ/b (FACT 13)
  MiniMax-M2 KV: 62 layers x 8 KV heads x 128 -> 71 KB/token at NVFP4 (FACT 10, gate g1_rf2#2)
  Rubin GPU ~$55k, rack ~$7.8M, HBM4 ~$382k/rack (~$18/GB) (Morgan Stanley via digitalcitizen.life / wccftech)
  TSMC 4nm ~$18-20k/wafer (Morgan Stanley via guru3d); N6 taken as $12k (assumption, below 4nm)
Everything else is marked ASSUMPTION.
"""
import math

def hdr(s): print("\n" + "=" * 8 + " " + s + " " + "=" * 8)

# ---------------------------------------------------------------- IDEA 1
hdr("IDEA 1: N6 SRAM-chiplet packages, package = tensor-parallel stage")
L, D, NQ, NKV, HD, PARAMS = 80, 8192, 64, 8, 128, 70.6e9
BITS = 4.5
W_GB = PARAMS * BITS / 8 / 1e9
kv_tok = 2 * L * NKV * HD * BITS / 8                     # bytes/token
CTX = 8192
kv_user = kv_tok * CTX / 1e9                              # GB/user
F_tok = 2 * PARAMS + 4 * L * CTX * NQ * HD                # FLOP/token at 8K
print(f"weights {W_GB:.1f} GB, KV {kv_tok/1e3:.1f} KB/tok -> {kv_user:.3f} GB/user @8K, {F_tok/1e9:.0f} GFLOP/tok")

SRAM_DENS = 64 * 8 / 36          # Mb/mm2, measured V-Cache (FACT 1)
DIE, SRAM_MM2, LOGIC_MM2 = 100, 70, 30
die_MB = SRAM_MM2 * SRAM_DENS / 8
TOPS_MM2 = 624 / 826             # A100 whole-die INT8 dense on N7 (FP8 assumed same cost)
die_TF = LOGIC_MM2 * TOPS_MM2
print(f"die: {die_MB:.0f} MB SRAM, {die_TF:.1f} TF FP8 (density {SRAM_DENS:.1f} Mb/mm2 measured, not 17.5)")
DIES_PKG = 32

# cost inputs
WAFER = 12000.0                  # ASSUMPTION N6
gross = math.pi * 150**2 / DIE - math.pi * 300 / math.sqrt(2 * DIE)
yld = math.exp(-0.1 * LOGIC_MM2 / 100) * 0.98            # D0=0.1/cm2 on logic, SRAM repaired (ASSUMPTION)
die_cost = WAFER / (gross * yld) + 3                     # +$3 test
PKG_OVH = 7500.0                 # ASSUMPTION substrate, assembly, board, VRMs per 32-die package
W_DIE = 25.0                     # ASSUMPTION W/die (compute ~8, SRAM read ~2, leakage ~12, IO ~2)
HRS = 4 * 8766
PUE, KWH = 1.3, 0.08
FAC_PER_W = 12.0 / (12 * 8766)   # $12/W facility over 12 yr, per W-hour (ASSUMPTION)

def idea1(B, eta=0.7, tau=1e-6, hop=2e-6, markup=2.0, util=0.6, rate_floor=1000):
    need_GB = (W_GB + B * kv_user) * 1.05
    dies = math.ceil(need_GB * 1e3 / die_MB)
    S = math.ceil(dies / DIES_PKG); dies = S * DIES_PKG
    P_pkg = DIES_PKG * die_TF * 1e12 * eta
    M = max(1, B // 2)                                   # micro-batches of 2 users
    m = B / M
    t_comp = m * F_tok / S / P_pkg
    t_coll = 2 * (L / S) * tau + hop                     # 2 all-reduces/layer inside package + 1 hop
    t_stage = t_comp + t_coll
    T = max(M, S) * t_stage                              # round trip of one user's token
    rate = 1 / T
    capex = S * (DIES_PKG * die_cost + PKG_OVH) * markup
    capex *= 1 / 0.75                                    # host/network/rack = 25% of silicon (archetype C 60:15)
    kw = dies * W_DIE / 1e3 * 1.15                       # +15% host/network power
    per_hr = capex / HRS + kw * PUE * KWH + kw * 1e3 * PUE * FAC_PER_W
    per_hr *= 1 / (1 - 0.09)                             # ops 3% + other 6%
    tps = B * min(rate, rate_floor) * util
    usd_mtok = per_hr / (tps * 3600) * 1e6
    sram_GB = dies * die_MB / 1e3
    return dict(B=B, S=S, dies=dies, rate=rate, capex=capex, kw=kw, usd=usd_mtok,
                usd_per_GB=capex / sram_GB, t_comp=t_comp * 1e6, t_coll=t_coll * 1e6, M=M)

print(f"die cost ${die_cost:.1f} (gross {gross:.0f}, yield {yld:.2f})")
print(" B  pkgs dies  tok/s/user  $capex   kW   $/GB   $/Mtok@60%util")
for B in (16, 24, 32, 40, 48):
    r = idea1(B)
    print(f"{B:3d} {r['S']:4d} {r['dies']:5d} {r['rate']:9.0f} {r['capex']/1e3:7.0f}k {r['kw']:5.1f} {r['usd_per_GB']:6.0f} {r['usd']:.4f}")
base = idea1(32)
print(f"chosen B=32: t_comp {base['t_comp']:.1f} us + t_coll {base['t_coll']:.1f} us per stage, M={base['M']}")
# old layer-serial check: if every stage only had P_total/S at batch 1 with 80 stages
print("sensitivity (B=32): rate, $/Mtok")
for eta, tau, mk, u in [(0.5, 1e-6, 2, .6), (0.7, 2e-6, 2, .6), (0.5, 2e-6, 3, .6), (0.7, 1e-6, 2, .4), (0.5, 2e-6, 3, .4)]:
    r = idea1(32, eta=eta, tau=tau, markup=mk, util=u)
    print(f"  eta={eta} tau={tau*1e6:.0f}us markup={mk} util={u}: {r['rate']:.0f} tok/s/user, ${r['usd']:.3f}/Mtok")
print("package overhead sensitivity (B=32, eta .7, tau 1us, markup 2, util .6):")
for ovh in (1500, 3000, 7500):
    PKG_OVH = ovh
    r = idea1(32)
    print(f"  pkg overhead ${ovh}: capex ${r['capex']/1e3:.0f}k, ${r['usd_per_GB']:.0f}/GB, ${r['usd']:.3f}/Mtok")
PKG_OVH = 7500.0
cs_per_GB = 3.2e6 / 44
print(f"capex/GB SRAM: Continuum ${base['usd_per_GB']:.0f} vs CS-3 ${cs_per_GB:.0f} -> {cs_per_GB/base['usd_per_GB']:.0f}x")
print(f"vs list price Groq $0.79: {0.79/base['usd']:.1f}x, Cerebras $0.60: {0.60/base['usd']:.1f}x (list includes their margin)")

# ---------------------------------------------------------------- IDEA 2 and 3 shared decode model
W_MOE = 1e12 * BITS / 8 / 1e9       # GB, 1T total params
ACT = 32e9
KV_M2 = 62 * 8 * 128 * 2 * BITS / 8 # bytes/token, MiniMax-M2-shaped GQA
NQ_M2 = 48 * 128                    # MiniMax-M2 q width (48 heads x 128) ASSUMPTION from config
E_FLOP = 0.15e-12                   # J/FLOP FP8 incl. operand delivery, N3/N2 (ASSUMPTION)

def decode(C, BW, Pf, e_mem, idle, link_W, r, ctx, N, eta=0.6, ivr=1.0):
    w = W_MOE / N
    kv = KV_M2 * ctx / 1e9
    f = 2 * ACT + 4 * 62 * ctx * NQ_M2
    B_cap = (C * 0.95 - w) / kv
    B_bw = (BW / 1e9 / r - w) / kv
    B_cmp = Pf * eta / (r * f)
    B = max(0.0, min(B_cap, B_bw, B_cmp))
    tps = B * r
    bytes_s = min(BW, (w + B * kv) * 1e9 * r)
    p = idle + link_W + bytes_s * 8 * e_mem + ivr * tps * f * E_FLOP
    lim = ["cap", "bw", "cmp"][[B_cap, B_bw, B_cmp].index(min(B_cap, B_bw, B_cmp))]
    return tps, p, lim

# ---------------------------------------------------------------- IDEA 2
hdr("IDEA 2: DRAM-on-logic sized to measured 64 Mb/mm2, 1.8 V IVR feed")
CHIP, NCH, LAYERS = 400, 4, 4
P_LOGIC = 1300.0                   # W logic budget used to size power TSVs (decode never exceeds it, see below)
for vin in (0.75, 1.8):
    I = P_LOGIC / vin / NCH / (0.9 if vin > 1 else 1)
    tsv = I / 10e-3                # 10 mA per power TSV (ASSUMPTION, EM-limited)
    area = tsv * (30e-3) ** 2      # 30 um pitch
    print(f"Vin {vin} V: {I:.0f} A/chiplet, {tsv/1e3:.0f}k TSVs, {area:.1f} mm2 = {area/CHIP*100:.1f}% of layer")
TSV_OVH = 0.06                     # 1.8 V case ~4% + keep-out
gb = NCH * CHIP * LAYERS * 0.064 * (1 - TSV_OVH)           # Gb
C2 = gb / 8
for gbps_gb in (135, 110):
    print(f"capacity {C2:.1f} GB ({gb:.0f} Gb); BW at {gbps_gb} GB/s/Gb = {gb*gbps_gb/1e3:.1f} TB/s")
BW2 = 44e12                         # chosen: 44 TB/s -> needs 117 GB/s/Gb (margin vs 135 measured below)
need_bwgb = BW2 / 1e9 / gb
print(f"chosen BW 44 TB/s needs {need_bwgb:.0f} GB/s/Gb vs 135 measured -> margin {135/need_bwgb:.2f}; density margin 0.064/0.064 = 1.00")
CONT = dict(C=C2, BW=BW2, Pf=20e15, idle=400, link_W=3.6e12 * 8 * 5e-12, ivr=1 / 0.9)
RUB = dict(C=288, BW=22e12, Pf=17.5e15, idle=500, link_W=3.6e12 * 8 * 5e-12, ivr=1.0)
print("ctx   r   N | Rubin tok/s/kW (3.44/5.74 pJ) | Cont tok/s/kW (0.88/1.5 pJ) | gain range | Cont W | limits")
gains = []
for ctx in (8192, 131072):
    for r in (100, 400, 1000):
        for N in (72, 144):
            rl, pl, _ = decode(e_mem=3.44e-12, r=r, ctx=ctx, N=N, **RUB)
            rh, ph, lr = decode(e_mem=5.74e-12, r=r, ctx=ctx, N=N, **RUB)
            cl, qpl, lc = decode(e_mem=0.88e-12, r=r, ctx=ctx, N=N, **CONT)
            ch, qph, _ = decode(e_mem=1.5e-12, r=r, ctx=ctx, N=N, **CONT)
            r_lo, r_hi = rl / pl * 1e3, rh / ph * 1e3
            c_lo, c_hi = cl / qpl * 1e3, ch / qph * 1e3
            g_min = c_hi / r_lo; g_max = c_lo / r_hi
            gains += [g_min, g_max]
            print(f"{ctx//1024:4d}K {r:4d} {N:3d} | {r_lo:6.0f} / {r_hi:6.0f} | {c_lo:6.0f} / {c_hi:6.0f} | {g_min:.2f}-{g_max:.2f}x | {qpl:5.0f} | R:{lr} C:{lc}")
            per_pkg = cl / rl
            print(f"            tokens/s per package Cont/Rubin = {per_pkg:.2f}")
print(f"balanced per-user rate where 48 GB stops binding: BW/C = {BW2/1e9/C2:.0f} tok/s/user (Rubin: {22e3/288:.0f})")

# ---------------------------------------------------------------- IDEA 3
hdr("IDEA 3: bandwidth-sized decode part (HBM4 8-high, 1.2 TB/s scale-up), cost per token")
RUBIN_PRICE = 55e3
RACK = 7.8e6
OTHER_PER_GPU = (RACK - 72 * RUBIN_PRICE) / 72      # Vera, NVLink switches, NICs, power shelves, LPDDR
NVL_SHARE = 0.4                                     # ASSUMPTION: share of OTHER that scales with scale-up BW
HBM_GB = 382e3 / (72 * 288)                         # $/GB
print(f"HBM4 ${HBM_GB:.1f}/GB; other-rack per GPU ${OTHER_PER_GPU/1e3:.1f}k")
# decode part: same 8 stacks / 22 TB/s, 8-high 24 GB stacks -> 192 GB; logic cut to ~5 PF FP8
C3 = 192
hbm_save = (288 - C3) * HBM_GB
LOGIC_SAVE_BOM = 700.0                               # ASSUMPTION: 2x~450 mm2 N3 dies instead of 2 reticle dies
def tco_hr(pkg_price, other, kw):
    capex = pkg_price + other
    return (capex / HRS + kw * PUE * KWH + kw * 1e3 * PUE * FAC_PER_W) / (1 - 0.11)
for ctx in (8192, 131072):
    for r in (100, 300):
        tr, pr, lr = decode(e_mem=3.44e-12, r=r, ctx=ctx, N=72, **RUB)
        dp = dict(C=C3, BW=22e12, Pf=5e15, idle=300, link_W=1.2e12 * 8 * 5e-12, ivr=1.0)
        td, pd, ld = decode(e_mem=3.44e-12, r=r, ctx=ctx, N=72, **dp)
        out = []
        for view, price in (("pass-through", RUBIN_PRICE - hbm_save - LOGIC_SAVE_BOM),
                            ("price~BOM", RUBIN_PRICE * (1 - (hbm_save + LOGIC_SAVE_BOM) / 10.2e3 * 0.5))):
            other_d = OTHER_PER_GPU * (1 - NVL_SHARE * (1 - 1.2 / 3.6))
            # rack power: GPU + 30% for CPU/switch/NIC
            cr = tco_hr(RUBIN_PRICE, OTHER_PER_GPU, pr / 1e3 * 1.3) / tr
            cd = tco_hr(price, other_d, pd / 1e3 * 1.3) / td
            out.append(cr / cd)
        print(f"{ctx//1024:4d}K r={r:3d}: Rubin {tr:6.0f} tok/s {pr:5.0f} W ({lr}) | decode part {td:6.0f} tok/s {pd:5.0f} W ({ld}) | cost/token gain {out[0]:.2f}x (pass-through) {out[1]:.2f}x (price~BOM/2)")
e_share = lambda p: p * 1.3 * PUE * KWH
print(f"energy share of Rubin TCO/hr at decode power: {e_share(1.84)/tco_hr(RUBIN_PRICE, OTHER_PER_GPU, 1.84*1.3)*100:.1f}%")
print(f"HBM bits per TB/s: decode part {C3/22:.1f} GB vs Rubin {288/22:.1f} GB -> {288/C3:.2f}x more decode packages per HBM wafer")
