# Improve_g1 arithmetic for the 3 leading Continuum answers. Inputs tagged S=sourced, E=estimate.
import math

# ---------- shared anchors ----------
VC_DENS = 512 / 36            # S: AMD V-Cache 64 MB in 36 mm^2 (N7) -> Mb/mm^2 (FACT 1)
assert abs(VC_DENS - 14.22) < 0.01

# ================= IDEA 1: N6 SRAM-chiplet pipeline =================
# Fix: size to measured 14.2 Mb/mm^2 on the SRAM fraction only, leave logic area explicit,
# and drop capacity need by using NVFP4 (4.5 b) weights + KV, the current Blackwell/Rubin practice.
P70 = 70e9
L, KVH, HD = 80, 8, 128                         # S: Llama-3-70B config (80 layers, 8 KV heads, 128 dim)
users, ctx = 31, 8192                            # same operating point as the gate check
bits = 4.5                                       # S: NVFP4 ~4.5 b/value (user notes)
w_old = P70 * 1.0                                # FP8 weights (original answer)
kv_old = 2 * L * KVH * HD * 1.0 * ctx * users    # FP8 KV
w_new = P70 * bits / 8
kv_new = 2 * L * KVH * HD * bits / 8 * ctx * users
need_old, need_new = (w_old + kv_old) / 1e9, (w_new + kv_new) / 1e9
die_mm2, sram_mm2, logic_mm2 = 100, 80, 20       # E: 80/20 split per die
mb_die = sram_mm2 * VC_DENS / 8                  # MB per die at measured density
dies = math.ceil(need_new * 1e3 / mb_die / 32) * 32
pkgs = dies // 32
# silicon cost (gate check inputs): $10k N6 wafer (E, scaled from N3/N4 reports), 640 gross, 90% yield
die_cost = 10_000 / (640 * 0.9)
pkg_over = 7_500                                 # E: gate-check bottom-up per-package overhead
sys_cost = dies * die_cost + pkgs * pkg_over
markup = 2.0                                     # E: vendor gross-margin markup (as in the gate's stress case)
sys_price = sys_cost * markup
cap_gb = dies * mb_die / 1e3
# compute check: 1000 tok/s/user, ~2 FLOP/param + attention at 8K (2*2*L*ctx*heads*hd, 64 q-heads)
attn = 2 * 2 * L * ctx * 64 * HD
flop_tok = 2 * P70 + attn
need_pf = users * 1000 * flop_tok / 1e15
# E: N7 A100 312 TF dense FP16 on 826 mm^2 -> 0.38 TF/mm^2; FP8 = 2x
fp8_tf_die = logic_mm2 * 312 / 826 * 2
have_pf = dies * fp8_tf_die / 1e3
# $/Mtok: 4-yr straight-line capex + energy (E: 25 W/die incl. links, PUE 1.3, $0.08/kWh)
toks = users * 1000
yr = 3600 * 24 * 365
power_kw = dies * 25 / 1e3 * 1.3
energy_per_s = power_kw * 0.08 / 3600
capex_per_s = sys_price / (4 * yr)
usd_mtok = (capex_per_s + energy_per_s) / toks * 1e6
allow_gbcost = 1500 * 112 / cap_gb                # $/GB allowed at the original $/system budget
print("[I1] need GB old (FP8) %.1f  new (NVFP4) %.1f" % (need_old, need_new))
print("[I1] MB/die at 14.2 Mb/mm2 on 80 mm2 = %.0f; dies %d; pkgs %d; capacity %.1f GB" % (mb_die, dies, pkgs, cap_gb))
print("[I1] compute need %.2f PF FP8, have %.2f PF -> margin %.2f" % (need_pf, have_pf, have_pf / need_pf))
print("[I1] cost at build %.0f k$, with %.0fx markup %.0f k$ -> %.0f $/GB; allowed %.0f $/GB at original budget"
      % (sys_cost / 1e3, markup, sys_price / 1e3, sys_price / cap_gb, allow_gbcost))
print("[I1] power %.1f kW; $/Mtok %.3f at 1000 tok/s/user (GB300 ~0.07 at ~50 tok/s, gate-check figure)" % (power_kw, usd_mtok))
print("[I1] margin on $/system vs original 168k$ budget: %.2f" % (1500 * 112 / sys_price))

# ================= IDEA 2: hybrid-bonded DRAM-on-logic =================
# Fix: halve the DRAM areal density demand (0.10 Gb/mm^2, ~half commodity, leaving room for 2048 IO/Gb
# periphery and power TSVs) -> 80 GB/pkg at the same 64 TB/s; take energy from the measured SeDRAM figures.
area = 4 * 400                                   # mm^2 per DRAM layer (4 chiplets)
for dens, hi in ((0.20, 4), (0.10, 4)):
    gb = dens * area * hi / 8
    print("[I2] density %.2f Gb/mm2 x %d-high -> %.0f GB; need %.0f GB/s/Gb (SeDRAM measured 135)"
          % (dens, hi, gb, 64e3 / (gb * 8)))
W = 1e12 * 4.5 / 8                                # 1T params @ 4.5 b
kvt = 8 * 128 * 2 * 4.5 / 8 * 60                  # GQA KV bytes per token-position
def tps(C, BW, N, ctx):
    kv = kvt * ctx
    B = (N * C - W) / kv
    if B <= 0: return 0, 0
    step = C / BW
    return B / step / N, 1 / step                 # tok/s per package, tok/s per user ceiling
for ctx in (8192, 131072):
    for N in (16, 32, 64):
        r, ru = tps(288e9, 22e12, N, ctx)
        c160, _ = tps(160e9, 64e12, N, ctx)
        c80, cu = tps(80e9, 64e12, max(N, 8), ctx)
        for pjb in (0.66, 0.88, 1.2):            # S: 0.66 (VLSI'23), 0.88 (IEDM'20); 1.2 = E stress
            pass
        # power: logic+IO 1.59 kW (from original 2.0 kW minus 410 W DRAM @0.8 pJ/b), DRAM at 0.88 pJ/b
        p80 = 1.59 + 64e12 * 8 * 0.88e-12 / 1e3
        print("[I2] ctx %6d N=%2d  Rubin %6.0f tok/s/kW | 160GB %6.0f | 80GB %6.0f -> 80GB/Rubin %.2fx (user ceiling %.0f tok/s)"
              % (ctx, N, r / 1.8, c160 / 2.0, c80 / p80, (c80 / p80) / (r / 1.8) if r else float('nan'), cu))
# power delivery through 4 DRAM layers: 500 W/chiplet at 0.75 V
I = 500 / 0.75
tsv_mA = 10                                       # E: conservative per-TSV DC limit
n_tsv = I / (tsv_mA / 1e3)
pitch_um = 30                                     # E: power-TSV pitch with keep-out
frac = n_tsv * (pitch_um * 1e-3) ** 2 / 400
print("[I2] %.0f A per chiplet -> %.0f power TSVs -> %.1f%% of a 400 mm2 DRAM layer at %d um pitch" % (I, n_tsv, 100 * frac, pitch_um))

# ================= IDEA 3: stacked-SRAM weights, HBM-only KV =================
# Fix: accept measured density, grow the domain; per-package throughput is set by HBM BW / KV bytes,
# so tok/s/MW is unchanged; serve only the >=300 tok/s/user tier where the gain survives capex.
Wt = 545                                          # GB weights (answer's model)
gb_pkg_raw = 2 * 800 * VC_DENS / 8 / 1e3          # 2 x 800 mm^2 base dies, whole-die density
gb_pkg = gb_pkg_raw * 0.9                         # E: 10% for power/signal TSVs to the compute die
n_min = math.ceil(Wt / gb_pkg)
n_dom = 8 * math.ceil(n_min * 1.05 / 8)           # 5% spare, rack-of-8 granularity
print("[I3] GB/pkg raw %.2f usable %.2f -> min pkgs %d, domain %d (was 144)" % (gb_pkg_raw, gb_pkg, n_min, n_dom))
# MoE all-to-all per token (E: d=7168, BF16, 8 experts, 61 layers, dispatch+combine)
a2a = 7168 * 2 * 8 * 61 * 2
tok_pkg = 18.6e6 / (1e6 / 2300)                   # answer's 18.6 Mtok/s/MW at 2.3 kW/pkg
print("[I3] per-pkg %.0f tok/s x %.1f MB a2a = %.2f TB/s scale-up (NVLink6 ~3.6 TB/s/GPU, S)" % (tok_pkg, a2a / 1e6, tok_pkg * a2a / 1e12))
# SRAM base-die silicon cost (E: $10k N7-class wafer, 64 gross 800 mm^2, 85% yield w/ redundancy)
base = 10_000 / (64 * 0.85)
print("[I3] base-die silicon $%.0f each, $%.0f per pkg" % (base, 2 * base))
for tier, g in (("8K >=100", 1.12), ("8K >=300", 1.41), ("128K >=100", 1.14), ("128K >=300", 1.58)):
    lo, hi = g / 1.15, g / 1.05                   # capex premium 15% (answer) .. 5% (E: silicon <1%, bonding+yield)
    print("[I3] %-11s per-MW %.2fx -> net cost gain %.2f-%.2fx" % (tier, g, lo, hi))
print("[I3] SRAM chips vs Groq LP30 1064: %d -> %.1fx fewer" % (n_dom * 2, 1064 / (n_dom * 2)))
