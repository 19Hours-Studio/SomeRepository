"""Decode roofline for a 1T-class MLA MoE (Kimi-K2-like public config) on
Continuum vs Rubin NVL72, Ironwood, Cerebras CS-3, Groq3 LPX+Rubin (AFD).
All vendor figures from search excerpts; Continuum figures are design estimates.
Model: step = max(compute, memory) + comm_latency + comm_bw. Uniform util."""
import math

# ---- model (Kimi K2 public config: 61 layers, 384 experts top-8, d=7168, expert ffn 2048, 64 heads, MLA 512+64)
L, D, E, K, FF, H = 61, 7168, 384, 8, 2048, 64
P_EXPERT = 3 * D * FF                       # 44M per expert
P_ROUTED = P_EXPERT * E * (L - 1)           # ~1.01T
P_ACTIVE = 32e9
P_ALWAYS = P_ACTIVE - P_EXPERT * K * (L - 1)  # shared expert + attn + dense layer
WBITS, KVBITS = 4.25, 4.5                   # MXFP4/NVFP4 weights, NVFP4 KV (~4.5b)
KV_ELEMS = 576                              # MLA latent+rope per token per layer
W_TOTAL = (P_ALWAYS + P_ROUTED) * WBITS / 8

def wbytes(B):
    frac = 1 - (1 - K / E) ** B
    return (P_ALWAYS + P_ROUTED * frac) * WBITS / 8

def kv_bytes_user(ctx, sparse):
    if not sparse:
        return ctx * L * KV_ELEMS * KVBITS / 8
    # DSA-like: top-2048 latent reads + FP4 128-d indexer keys over full ctx
    return 2048 * L * KV_ELEMS * KVBITS / 8 + ctx * L * 128 * KVBITS / 8

def flops_user(ctx, sparse):
    ffn = 2 * P_ACTIVE
    n = 2048 if sparse else ctx
    attn = 2 * H * (KV_ELEMS + 512) * n * L
    idx = 2 * 64 * 128 * ctx * L if sparse else 0
    return ffn, attn + idx

COMM_BYTES_TOK = L * D * K * (1 + 2)        # FP8 dispatch + BF16 combine

# ---- systems: N chips, fp4/fp8 dense PF, HBM TB/s & GB, SRAM TB/s & GB, power kW all-in per chip,
# per-all-to-all latency us, scale-up TB/s per chip (uni), weights_in_sram
SYS = {
 "Rubin NVL72 (22TB/s)": dict(N=72, fp4=35, fp8=17.5, hbm=22, hbm_gb=288, sram=0, sram_gb=0, kw=220/72, lat=8, link=1.8, wsram=False),
 "Rubin NVL72 (13TB/s)": dict(N=72, fp4=35, fp8=17.5, hbm=13, hbm_gb=288, sram=0, sram_gb=0, kw=220/72, lat=8, link=1.8, wsram=False),
 "Ironwood x128":        dict(N=128, fp4=4.614, fp8=4.614, hbm=7.38, hbm_gb=192, sram=0, sram_gb=0, kw=1.1, lat=10, link=0.6, wsram=False),
 "Cerebras CS-3 x14":    dict(N=14, fp4=25, fp8=25, hbm=0, hbm_gb=0, sram=21000, sram_gb=44, kw=23, lat=5, link=1.5, wsram=True, kv_in_sram=True),
 "Continuum x144":       dict(N=144, fp4=30, fp8=15, hbm=22, hbm_gb=288, sram=300, sram_gb=4, kw=2.3*1.25, lat=1.5, link=1.8, wsram=True),
 "Continuum x144 lat4us": dict(N=144, fp4=30, fp8=15, hbm=22, hbm_gb=288, sram=300, sram_gb=4, kw=2.3*1.25, lat=4, link=1.8, wsram=True),
 "Continuum x144 HBM13":  dict(N=144, fp4=30, fp8=15, hbm=13, hbm_gb=288, sram=300, sram_gb=4, kw=2.3*1.25, lat=1.5, link=1.8, wsram=True),
 # AFD: 1280 LP30 (weights, 150TB/s, 1.23PF FP8, ASSUMED 0.8kW all-in) + NVL72 for KV/attn; modelled as one pool, lat 4us (cross-rack hop)
 "LPX x5 + NVL72 (AFD)":  dict(N=72, fp4=35+1280/72*1.23, fp8=17.5+1280/72*1.23, hbm=22, hbm_gb=288, sram=1280/72*150, sram_gb=1280/72*0.512, kw=(220+1280*0.8)/72, lat=4, link=1.8, wsram=True),
}
# Cerebras: 12.5 PF dense FP16 (The Register) -> assume 2x for FP8-class; 23 kW system.
# Ironwood ~1.1 kW/chip from "9216 chips ~10 MW". Continuum lat 1.5us is an ASSUMPTION (needs network sim).

def step(s, B, ctx, sparse, util=0.6):
    ffn, attn = flops_user(ctx, sparse)
    t_comp = B * (ffn / (s["fp4"] * 1e15) + attn / (s["fp8"] * 1e15)) / (s["N"] * util)
    kvb = B * kv_bytes_user(ctx, sparse)
    wb = wbytes(B)
    if s.get("kv_in_sram"):
        t_mem = (wb + kvb) / (s["N"] * s["sram"] * 1e12)
    elif s["wsram"]:
        t_mem = max(wb / (s["N"] * s["sram"] * 1e12), kvb / (s["N"] * s["hbm"] * 1e12))
    else:
        t_mem = (wb + kvb) / (s["N"] * s["hbm"] * 1e12)
    t_comm = 2 * L * s["lat"] * 1e-6 + B * COMM_BYTES_TOK / (s["N"] * s["link"] * 1e12)
    return max(t_comp, t_mem) + t_comm, (t_comp, t_mem, t_comm)

def bmax(s, ctx, sparse):
    if s.get("kv_in_sram"):
        free = s["N"] * s["sram_gb"] * 1e9 * 0.95 - W_TOTAL
    elif s["wsram"]:
        free = s["N"] * s["hbm_gb"] * 1e9 * 0.9
    else:
        free = s["N"] * s["hbm_gb"] * 1e9 * 0.9 - W_TOTAL
    return max(0, int(free / (ctx * L * KV_ELEMS * KVBITS / 8)))

def best_at_slo(s, ctx, sparse, slo):
    best = (0, 0, None)
    for B in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]:
        if B > bmax(s, ctx, sparse): break
        t, parts = step(s, B, ctx, sparse)
        if 1 / t >= slo and B / t > best[0]:
            best = (B / t, B, parts)
    return best

print(f"Weights total {W_TOTAL/1e9:.0f} GB; KV/user 128K dense {kv_bytes_user(131072,False)/1e9:.2f} GB, "
      f"sparse {kv_bytes_user(131072,True)/1e9:.2f} GB; FLOP/user-tok 128K dense {sum(flops_user(131072,False))/1e12:.2f} T")
for ctx, sparse in [(8192, False), (131072, False), (131072, True)]:
    print(f"\n=== ctx={ctx} sparse={sparse} ===")
    for name, s in SYS.items():
        t1, p1 = step(s, 1, ctx, sparse)
        mw = s["N"] * s["kw"] / 1000
        row = f"{name:22s} B1={1/t1:6.0f} tok/s/user | Bmax={bmax(s,ctx,sparse):6d} |"
        for slo in (100, 300, 1000):
            thr, B, parts = best_at_slo(s, ctx, sparse, slo)
            row += f" @{slo}: {thr/mw/1e6:6.2f} Mtok/s/MW (B={B})"
        print(row, f"| {mw*1000:.0f} kW")

# energy sanity: per-package power split for Continuum at full tilt
print("\nContinuum package power check (estimates):")
sram_w = 300e12 * 8 * 0.12e-12; hbm_w = 22e12 * 8 * 3.0e-12
comp_w = 15e15 / 2 * 0.12e-12   # FP8 MAC/s * 0.12 pJ/MAC datapath (Rubin all-in calib: ~2kW/8.75e15 MAC/s = 0.23 pJ)
print(f" SRAM 300TB/s@0.12pJ/b={sram_w:.0f} W, HBM 22TB/s@3pJ/b={hbm_w:.0f} W, compute FP8 15PF@0.12pJ/MAC={comp_w:.0f} W, "
      f"sum={sram_w+hbm_w+comp_w:.0f} W + SerDes/IO ~250 W")
# SRAM capacity / bond arithmetic
die_mm2, mb_per_mm2, eff = 800, 30, 0.75
print(f" SRAM die {die_mm2}mm2 @{mb_per_mm2}Mb/mm2*{eff} = {die_mm2*mb_per_mm2*eff/8/1000:.2f} GB")
sig = 14000 * 40  # signals/mm2 F2F * 40mm2 of signal area
print(f" F2F bonds {sig/1e3:.0f}k @3Gb/s = {sig*3e9/8/1e12:.0f} TB/s per die")
print(f" packages to hold weights in SRAM: {W_TOTAL/4e9:.0f} (Continuum 4GB), {W_TOTAL/0.512e9:.0f} LP30 (512MB), {W_TOTAL/44e9:.1f} WSE-3")
