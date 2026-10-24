"""Roofline / energy / cost model for the two Continuum repairs.
All inputs labelled: [S]=sourced (see NOTES.md), [E]=own estimate/assumption.
Run: python3 model.py
"""
import math

# ---------------- workload: DeepSeek-V3-class MLA MoE (public config) ----------------
P_TOT = 671e9          # [S] total params
P_ACT = 37e9           # [S] active params / token
LAYERS = 61            # [S]
MOE_LAYERS = 58        # [S] (first 3 dense)
KV_ELEM_TOK = (512 + 64) * LAYERS   # [S] MLA latent+rope elements / token
HEADS = 128            # [S]
BITS_W = 4.5           # [S] NVFP4 incl. block scales (FACT 3 / NVFP4 spec)

def kv_bytes(ctx, bits=8):           # bytes per user
    return KV_ELEM_TOK * ctx * bits / 8

def attn_flops_tok(ctx):             # absorbed MLA decode: q.K (576) + attn.V (512), per head
    return 2 * HEADS * (576 + 512) * ctx * LAYERS

W_BYTES = P_TOT * BITS_W / 8
FL_DENSE = 2 * P_ACT

# ---------------- baselines ----------------
RUBIN = dict(hbm_bw=22e12, hbm_cap=288e9, fp8=16e15,  # [S] 22 TB/s, 288 GB (Register); FP8 dense [E]
             pkg=72, rack_price=7.8e6, rack_kw=190)    # price [S] Morgan Stanley via digitalcitizen; kW [E] 130-230
HBM_PJ_B = 3.44                                         # [S] FACT 6 (5.74 alt)
LPDDR_PJ_B = 3.6                                        # [S] FACT 5 (Vera subsystem)
SRAM_PJ_B = 0.15                                        # [E] local SRAM read incl. short wire, N3
FP8_PJ_FLOP = 0.25                                      # [E] ~B200 1kW/4.5PF FP8 at full power

def p(*a): print(*a)

# =====================================================================================
# IDEA 1  Continuum-D : weights resident in 2D SRAM over N dies, KV in per-die LPDDR
# =====================================================================================
p("=" * 30, "IDEA 1  Continuum-D", "=" * 30)
SRAM_MIB_MM2 = 31.8      # [S] FACT 9 N3E bitcell density
ARRAY_EFF = 0.70         # [E] macro periphery/redundancy overhead
WAFER_N3 = 19.5e3        # [S] siliconanalysts N3 avg 2026 (17-22k)
D0 = 0.10                # [E] defects/cm^2 mature N3
LP_TBps_DIE = 1.0e12     # [E] ~Vera-class (1.2 TB/s, FACT 5) per die
LP_GB_DIE = 32           # [E]
LP_USD_GB = 10           # [S] FACT 1 (7.8-21)

def dies_per_wafer(a_mm2, d=300):
    return math.pi * (d / 2) ** 2 / a_mm2 - math.pi * d / math.sqrt(2 * a_mm2)

def sram_area_mm2(gb):
    bits = gb * 8e9
    return bits / (SRAM_MIB_MM2 * 2**20) / ARRAY_EFF

for gb_die in (1.0, 1.25):
    n = math.ceil(W_BYTES * 1.10 / (gb_die * 1e9))   # 10% headroom (dense layers replicated, spares)
    p(f"\nSRAM/die {gb_die} GB -> dies needed {n}, SRAM area {sram_area_mm2(gb_die):.0f} mm2")

GB_DIE = 1.25
N1 = math.ceil(W_BYTES * 1.10 / (GB_DIE * 1e9))
A_SRAM = sram_area_mm2(GB_DIE)
A_DIE = 800
A_LOGIC = A_DIE - A_SRAM - 110          # 110 mm2 [E] LPDDR PHY + SerDes + misc
TF_MM2 = 16e15 / 1600 / 1e12            # [E] Rubin-like FP8 density ~10 TF/mm2 incl. overhead
p(f"Design: {N1} dies x {A_DIE} mm2, SRAM {A_SRAM:.0f} mm2, logic {A_LOGIC:.0f} mm2 -> FP8 {A_LOGIC*TF_MM2*0.5:.0f} TF (50% of logic as tensor)")

def system1(ctx, kv_bits, tps_user):
    kvb_die = kv_bytes(ctx, kv_bits) / N1        # KV share per die per user (layers pipelined)
    thr_mem = LP_TBps_DIE / kvb_die              # tok/s system (every token visits every die)
    fl_die = (attn_flops_tok(ctx) + FL_DENSE) / N1
    thr_cmp = A_LOGIC * TF_MM2 * 0.5e12 * 0.6 / fl_die   # 60% MFU [E]
    hop = 0.7e-6                                  # [E] die-die hop latency (Groq-like C2C)
    # per-token latency = N1 stages x (stage compute + hop); stage compute <= what interactivity allows
    stage_budget = 1 / tps_user / N1 - hop
    thr = min(thr_mem, thr_cmp) if stage_budget > 0 else 0
    users = thr / tps_user
    kv_cap_users = LP_GB_DIE * 1e9 / kvb_die
    return thr, thr_mem, thr_cmp, users, kv_cap_users, stage_budget

die_good = WAFER_N3 / (dies_per_wafer(A_DIE) * (0.30 + 0.70 * math.exp(-D0 * A_DIE / 100 * 0.45)))
# SRAM (~45% of die) is repairable; logic yield Poisson on remaining fraction; 0.30 floor = harvest [E]
die_usd = die_good + 250                  # [E] std flip-chip package + test (no CoWoS)
board_usd = 600                          # [E] board share, PMIC, cooling
lp_usd = LP_GB_DIE * LP_USD_GB
net_usd = 400                            # [E] SerDes optics/cables share
unit = die_usd + board_usd + lp_usd + net_usd
capex1 = N1 * unit * 1.25                # 25% chassis/integration [E]
P_DIE_W = 350                            # [E] see energy check below
p(f"Good-die cost ${die_good:.0f}; per-node ${unit:.0f}; system capex ${capex1/1e6:.2f}M; power {N1*P_DIE_W/1e3:.0f} kW")

def rubin(ctx, kv_bits, tps_user, a2a_us):
    """NVL72 wide-EP decode: step = weights_share + B*KV over HBM, + comm latency per token."""
    w_share = W_BYTES / RUBIN['pkg']
    t_step = 1 / tps_user
    t_comm = 2 * MOE_LAYERS * a2a_us * 1e-6
    t_mem = t_step - t_comm - w_share / RUBIN['hbm_bw']
    if t_mem <= 0:
        return 0, 0
    B = t_mem * RUBIN['hbm_bw'] / kv_bytes(ctx, kv_bits)
    B = min(B, (RUBIN['hbm_cap'] - w_share) / kv_bytes(ctx, kv_bits))
    # compute check
    fl = B * (attn_flops_tok(ctx) + FL_DENSE)
    B = min(B, RUBIN['fp8'] * 0.6 * t_step / (attn_flops_tok(ctx) + FL_DENSE))
    return B * tps_user * RUBIN['pkg'], B

p("\nctx  kvbits tok/s/user | C-D thr  (mem,cmp)  users  kvcap | Rubin thr(a2a 10us) (a2a 30us) | $/Mtok C-D  Rubin10")
HOURS = 4 * 365 * 24 * 0.7    # 4-yr life, 70% util [E]
for ctx in (8192, 32768, 131072):
    for kvb in (8, 4.5):
        for tps in (50, 200, 1000):
            thr, tm, tc, u, kc, sb = system1(ctx, kvb, tps)
            r10, _ = rubin(ctx, kvb, tps, 10)
            r30, _ = rubin(ctx, kvb, tps, 30)
            def usd_mtok(capex, kw, th):
                if th <= 0: return float('inf')
                opex = kw * HOURS * 0.10 * 1.3  # $0.10/kWh, PUE 1.3 [E]
                return (capex + opex) / (th * HOURS * 3600) * 1e6
            c1 = usd_mtok(capex1, N1 * P_DIE_W / 1e3, thr)
            cr = usd_mtok(RUBIN['rack_price'], RUBIN['rack_kw'], r10)
            p(f"{ctx:6d} {kvb:4.1f} {tps:5d} | {thr/1e3:7.0f}k ({tm/1e3:.0f}k,{tc/1e3:.0f}k) {u:7.0f} {kc:7.0f} | {r10/1e3:7.0f}k {r30/1e3:7.0f}k | {c1:6.3f} {cr:6.3f}")

# energy per token, Idea 1 vs Rubin, 32K FP8 KV, 200 tok/s/user
ctx = 32768
e_w_sram = P_ACT * BITS_W * SRAM_PJ_B * 1e-12
e_kv_lp = kv_bytes(ctx, 8) * 8 * LPDDR_PJ_B * 1e-12
e_cmp = (attn_flops_tok(ctx) + FL_DENSE) * FP8_PJ_FLOP * 1e-12
e_link = 7168 * 1 * N1 * 8 * 1.5e-12   # activation (7168 FP8) hop per die, 1.5 pJ/b SerDes-short [E]
_, B = rubin(ctx, 8, 200, 10)
e_w_hbm = W_BYTES / RUBIN['pkg'] * 8 * HBM_PJ_B * 1e-12 / max(B, 1)
e_kv_hbm = kv_bytes(ctx, 8) * 8 * HBM_PJ_B * 1e-12
p(f"\nEnergy/token @32K FP8: C-D  weights {e_w_sram*1e3:.1f} mJ  KV(LPDDR) {e_kv_lp*1e3:.1f}  compute {e_cmp*1e3:.0f}  links {e_link*1e3:.2f}  total {(e_w_sram+e_kv_lp+e_cmp+e_link)*1e3:.0f} mJ")
p(f"                       Rubin weights {e_w_hbm*1e3:.2f} mJ (B={B:.0f}) KV(HBM) {e_kv_hbm*1e3:.1f}  compute {e_cmp*1e3:.0f}  total {(e_w_hbm+e_kv_hbm+e_cmp)*1e3:.0f} mJ")
thr32, *_ = system1(32768, 8, 200)
p(f"Power check: C-D at 32K/200tps dissipates {(e_w_sram+e_kv_lp+e_cmp+e_link)*thr32/N1:.0f} W/die dynamic (budget {P_DIE_W} W incl leakage/IO)")

# reliability
FIT_NODE = 2000   # [E] failures / 1e9 h per node (die+LPDDR+board+links)
mtbf = 1e9 / (FIT_NODE * N1)
p(f"Instance MTBF with {N1} nodes at {FIT_NODE} FIT: {mtbf:.0f} h; reload 1.25 GB over 100 Gb/s: {1.25e9*8/100e9:.2f} s")

# =====================================================================================
# IDEA 2  Expert-stationary stacked SRAM (Rubin-class package + SRAM under compute)
# =====================================================================================
p("\n" + "=" * 30, "IDEA 2  Expert-stationary stacked SRAM", "=" * 30)
VC_MB_MM2_N7 = 64 / 36            # [S] FACT 4 (V-Cache gen2, N7-class bitcell 0.027 um2)
VC_MB_MM2_N5 = VC_MB_MM2_N7 * 0.027 / 0.021   # scale to N5/N3 HD bitcell [S FACT 9]
for layers in (4,):
    for dies in (1, 2):
        cap = dies * layers * 750 * VC_MB_MM2_N5 / 1e3
        p(f"{dies} compute die(s) x {layers} SRAM layers x 750 mm2 @ {VC_MB_MM2_N5:.2f} MB/mm2 = {cap:.1f} GB/pkg; rack(72) {cap*72:.0f} GB")
CAP2 = 2 * 4 * 750 * VC_MB_MM2_N5 / 1e3 * 72
for name, P in (("DeepSeek-V3 671B", 671e9), ("Kimi-K2 1.04T", 1.04e12)):
    p(f"  {name} @NVFP4 {P*BITS_W/8/1e9:.0f} GB -> margin {CAP2/(P*BITS_W/8/1e9):.2f}")

# SRAM die cost
WAFER_N5 = 16e3   # [E] siliconanalysts range
sram_die = WAFER_N5 / (dies_per_wafer(750) * 0.85)   # SRAM-only die w/ redundancy [E 85%]
bond_yield = 0.97 ** 8          # [E] per hybrid-bond step, 8 bonds/pkg
add_pkg = (8 * sram_die + 8 * 150) / bond_yield     # $150/bond step [E]
p(f"SRAM die ${sram_die:.0f}; added cost/pkg ${add_pkg:.0f}; rack +${add_pkg*72/1e3:.0f}k ; $/GB {add_pkg/(CAP2/72):.0f}")

def stack_rack(ctx, kv_bits, tps_user, a2a_us, weights_in_sram, hop_us=0.0):
    w_share = W_BYTES / 72
    t_step = 1 / tps_user
    t_comm = 2 * MOE_LAYERS * a2a_us * 1e-6 + 2 * LAYERS * hop_us * 1e-6
    t_w = 0 if weights_in_sram else w_share / RUBIN['hbm_bw']
    t_mem = t_step - t_comm - t_w
    if t_mem <= 0:
        return 0
    cap = RUBIN['hbm_cap'] - (0 if weights_in_sram else w_share)
    B = min(t_mem * RUBIN['hbm_bw'] / kv_bytes(ctx, kv_bits), cap / kv_bytes(ctx, kv_bits),
            RUBIN['fp8'] * 0.6 * t_step / (attn_flops_tok(ctx) + FL_DENSE))
    return B * tps_user * 72

p("\nctx kv tps a2a | Rubin wideEP | Rubin+LPX AFD(+1us hop) | Stacked | gain vs Rubin, vs AFD")
for ctx in (8192, 32768):
    for tps in (100, 300, 600, 1000):
        for a2a in (5, 15):
            r = stack_rack(ctx, 4.5, tps, a2a, False)
            afd = stack_rack(ctx, 4.5, tps, a2a, True, hop_us=1.0)
            s = stack_rack(ctx, 4.5, tps, a2a, True)
            g = lambda a, b: (a / b) if b > 0 else float('inf')
            p(f"{ctx:6d} 4.5 {tps:5d} {a2a:3d} | {r/1e3:8.0f}k | {afd/1e3:8.0f}k | {s/1e3:8.0f}k | {g(s,r):5.2f}x {g(s,afd):5.2f}x")

# thermal: compute die on top (Zen5 X3D orientation), SRAM below; heat from SRAM layers
SRAM_LEAK_PW_B = (7.5, 37)   # [E] pW/bit HD SRAM at 70-85C
bits = CAP2 / 72 * 8e9
p(f"\nSRAM leakage/pkg: {bits*SRAM_LEAK_PW_B[0]*1e-12:.1f}-{bits*SRAM_LEAK_PW_B[1]*1e-12:.1f} W")
rd_W = 2.0e12 * 8 * 0.1e-12 * 1   # 2 TB/s average expert read at 0.1 pJ/b through bond
p(f"SRAM read power at 2 TB/s avg: {rd_W:.1f} W ; heat must cross compute die (top) -> path dT small")
# Power density through SRAM stack: compute die ~ 1800W/2 dies/750mm2
p(f"Compute power density ~{1800/2/750:.2f} W/mm2 (Rubin-class) -> power delivered through 4 SRAM layers of TSVs")

# =====================================================================================
# ROUND 2 refinements
# =====================================================================================
p("\n" + "=" * 30, "ROUND 2", "=" * 30)
GM_MULT = 3.0   # [E] price = BOM x3 (~67% GM, merchant-vendor-like) so Rubin's $7.8M price is compared like-for-like
price1 = capex1 * GM_MULT
p(f"Continuum-D price at 67% GM: ${price1/1e6:.2f}M (BOM {capex1/1e6:.2f}M); LPDDR total {N1*LP_GB_DIE/1e3:.1f} TB; HBM stacks 0; CoWoS 0")

# Latency ceiling: layer-group topology (61 groups of ~5.5 dies): 2 hops per layer instead of N1 serial hops
HOP = 0.7e-6
for topo, hops in (("serial pipeline", N1), ("layer-groups (bcast+reduce)", 2 * LAYERS)):
    p(f"  {topo}: {hops} hops -> {hops*HOP*1e6:.0f} us/token hop floor -> ceiling {1/(hops*HOP):.0f} tok/s/user")

def usd_mtok(price, kw, th):
    if th <= 0: return float('inf')
    opex = kw * HOURS * 0.10 * 1.3
    return (price + opex) / (th * HOURS * 3600) * 1e6

# Cerebras CS-3: 44 GB SRAM/wafer [S], ~23 kW [S], price ~$2.5M [E, press ~2-3M]; KV in SRAM
def cerebras(ctx, kvbits, tps, n_w):
    free = n_w * 44e9 - W_BYTES
    users = max(free, 0) / kv_bytes(ctx, kvbits)
    return users * tps, n_w * 2.5e6, n_w * 23

# Rubin + LPX AFD: experts on LPUs (0.5 GB each [S]), attention/KV on Rubin. LPX rack 256 LPU [S]; price [E] $4M/rack
def afd(ctx, kvbits, tps, a2a_us, n_rubin_racks=1):
    n_lpx = math.ceil(W_BYTES * 1.1 / (256 * 0.5e9))
    th = stack_rack(ctx, kvbits, tps, a2a_us, True, hop_us=1.0) * n_rubin_racks
    return th, n_lpx * 4e6 + n_rubin_racks * RUBIN['rack_price'], n_lpx * 60 + n_rubin_racks * RUBIN['rack_kw'], n_lpx

p("\n$/Mtok (4-yr, 70% util, $0.10/kWh, PUE1.3)   ctx=32K, KV NVFP4")
p("tps/user | Continuum-D        | Rubin NVL72 wideEP(a2a5us) | Rubin+LPX AFD       | Cerebras x12 wafers")
for tps in (50, 200, 500, 1000, 2000):
    thr, *_ = system1(32768, 4.5, tps)
    if 2 * LAYERS * HOP > 1 / tps: thr = 0
    c = usd_mtok(price1, N1 * P_DIE_W / 1e3, thr)
    r = rubin(32768, 4.5, tps, 5)[0]
    cr = usd_mtok(RUBIN['rack_price'], RUBIN['rack_kw'], r)
    ta, pa, ka, nl = afd(32768, 4.5, tps, 5)
    ca = usd_mtok(pa, ka, ta)
    tc, pc, kc = cerebras(32768, 4.5, tps, 12)
    cc = usd_mtok(pc, kc, tc)
    p(f"{tps:7d} | {thr/1e3:5.0f}k  ${c:6.3f}    | {r/1e3:5.0f}k  ${cr:6.3f}           | {ta/1e3:5.0f}k ${ca:6.3f} ({nl} LPX) | {tc/1e3:5.0f}k ${cc:6.3f}")

# Energy with micro-batching: at low interactivity each stage batches m tokens; dense (attn+shared) weights amortised over m
DENSE_ACT = 14e9 * 0  # placeholder
for tps in (50, 1000):
    stage_t = 1 / tps / (2 * LAYERS) * 0.5   # half of per-layer budget for compute
    thr, *_ = system1(32768, 4.5, tps)
    m = max(1, thr * stage_t / 1)            # tokens per layer-group micro-batch
    # shared (non-routed) active params ~ 37B - 8 routed experts*58 layers*44M = ~16.6B [S-derived]
    shared = 37e9 - 8 * 58 * 3 * 7168 * 2048
    e_w = (shared / m + (P_ACT - shared)) * BITS_W * SRAM_PJ_B * 1e-12
    e_kv = kv_bytes(32768, 4.5) * 8 * LPDDR_PJ_B * 1e-12
    e_c = (attn_flops_tok(32768) + FL_DENSE) * FP8_PJ_FLOP * 1e-12
    _, B = rubin(32768, 4.5, min(tps, 300), 5)
    e_r = W_BYTES / 72 * 8 * HBM_PJ_B * 1e-12 / max(B, 1) + kv_bytes(32768, 4.5) * 8 * HBM_PJ_B * 1e-12 + e_c
    p(f"tps {tps}: micro-batch m={m:.1f}; C-D J/tok {e_w+e_kv+e_c:.3f} (weights {e_w*1e3:.1f} mJ)  Rubin J/tok {e_r:.3f} -> ratio {e_r/(e_w+e_kv+e_c):.2f}")

# LPDDR shoreline check: LPDDR6 x24 @14.4 Gb/s = 38.4 GB/s measured [S SK hynix ISSCC26]
ch = 1e12 / 38.4e9
p(f"\nLPDDR6 channels/die for 1 TB/s: {ch:.0f} x24 ({ch*24:.0f} DQ); LPDDR5X-9600 equivalent bus {1e12*8/9.6e9:.0f} bits (Vera: 1024-bit, 1.2 TB/s [S])")
perim = 4 * math.sqrt(A_DIE)
p(f"Die perimeter {perim:.0f} mm; LPDDR PHY at ~0.25 mm/x24ch [E] -> {ch*1.6:.0f} mm if 1.6 mm/ch; SerDes 64x112G @ ~0.6 mm/lane [E] -> {64*0.6:.0f} mm")

# Idea 2 round 2: comm not overlapped with compute either (conservative for all)
p("\nIdea 2 sweep with compute budget = step - comm, a2a in {2,5,8} us")
def stack2(ctx, kvb, tps, a2a, w_sram, hop=0.0, hbm_bw=RUBIN['hbm_bw']):
    w_share = W_BYTES / 72
    t = 1 / tps; tc = 2 * MOE_LAYERS * a2a * 1e-6 + 2 * LAYERS * hop * 1e-6
    tw = 0 if w_sram else w_share / hbm_bw
    if t - tc - tw <= 0: return 0
    B = min((t - tc - tw) * hbm_bw / kv_bytes(ctx, kvb), (RUBIN['fp8'] * 0.6 * (t - tc)) / (attn_flops_tok(ctx) + FL_DENSE),
            (RUBIN['hbm_cap'] - (0 if w_sram else w_share)) / kv_bytes(ctx, kvb))
    return B * tps * 72
p("ctx  tps a2a | Rubin   AFD   Stacked | xRubin xAFD")
for ctx in (8192, 32768):
    for tps in (300, 600, 1000, 1500):
        for a2a in (2, 5):
            r, a, s = stack2(ctx, 4.5, tps, a2a, False), stack2(ctx, 4.5, tps, a2a, True, 1.0), stack2(ctx, 4.5, tps, a2a, True)
            f = lambda x, y: f"{x/y:5.2f}" if y > 0 else ("  inf" if x > 0 else "  n/a")
            p(f"{ctx:5d} {tps:5d} {a2a:2d} | {r/1e3:5.0f}k {a/1e3:5.0f}k {s/1e3:5.0f}k | {f(s,r)} {f(s,a)}")
# Idea 2 $ : +$308k on $7.8M rack (+4%). Break-even gain 1.04x.
p(f"Idea 2 cost ratio: rack price +{add_pkg*72*GM_MULT/RUBIN['rack_price']*100:.0f}% at 3x markup -> needs >{1+add_pkg*72*GM_MULT/RUBIN['rack_price']:.2f}x throughput to pay")
