"""Decode roofline + latency model for DeepSeek-V4-Pro-class serving (128K context).

Every number here is an input assumption or a vendor figure; see SPECS comments.
Usage: python3 model.py [context_tokens]
"""
import math, sys

CTX = int(sys.argv[1]) if len(sys.argv) > 1 else 131072

# ---------------- workload: DeepSeek-V4-Pro-like (public config + paper) -------------
LAYERS, N_EXP, TOPK = 61, 384, 6
EXPERT_PARAMS = 3 * 7168 * 3072                 # 66M per routed expert
DENSE_PARAMS_LAYER = 0.35e9 + EXPERT_PARAMS     # attention (est.) + shared expert
HEAD_PARAMS = 129280 * 7168                     # LM head, read once per token
B_EXP = EXPERT_PARAMS * 4.5 / 8                 # NVFP4: 4b + E4M3 scale per 16
B_DENSE_LAYER = DENSE_PARAMS_LAYER * 8.25 / 8   # attention/shared kept at FP8
B_HEAD = HEAD_PARAMS * 4.5 / 8
N_CSA, N_HCA = 30, 31                           # assumption: ~even split
ENTRY = 448 + 64 * 2                            # FP8 latent + BF16 RoPE dims = 576 B
TOPK_ATT, WIN, M_CSA, M_HCA = 1024, 128, 4, 128
IDX_B, IDX_FLOP = 128 * 0.5, 64 * 128 * 2       # FP4 indexer key / FLOPs per entry
FLOP_PER_ENTRY = 128 * 2 * (512 + 512)          # QK + AV over 128 heads


def kv_store(L):        # bytes per user resident in memory
    csa = L / M_CSA * (ENTRY + IDX_B) + WIN * ENTRY
    hca = L / M_HCA * ENTRY + WIN * ENTRY
    return N_CSA * csa + N_HCA * hca


def kv_read(L):         # bytes read per decode step per user
    csa = (TOPK_ATT + WIN) * ENTRY + L / M_CSA * IDX_B
    hca = (L / M_HCA + WIN) * ENTRY
    return N_CSA * csa + N_HCA * hca


def attn_flops(L):
    csa = (TOPK_ATT + WIN) * FLOP_PER_ENTRY + L / M_CSA * IDX_FLOP
    hca = (L / M_HCA + WIN) * FLOP_PER_ENTRY
    return N_CSA * csa + N_HCA * hca


LIN_FLOPS = 2 * (TOPK * EXPERT_PARAMS * LAYERS + DENSE_PARAMS_LAYER * LAYERS + HEAD_PARAMS)
W_TOTAL = LAYERS * (N_EXP * B_EXP + B_DENSE_LAYER) + B_HEAD


def touched(b):         # expected distinct experts hit by b tokens in one layer
    return N_EXP * (1 - (1 - TOPK / N_EXP) ** b)


# ---------------- systems ----------------------------------------------------------
# F4/F8 dense FLOP/s; HBM GB, TB/s; SRAM GB, TB/s; P = provisioned W per chip slot
# (rack power / chips); tau = fixed per-layer latency (comm + sync + launch), seconds.
ETA = 0.6  # achieved fraction of dense peak compute, same for everyone
GPU = {
    "GB300 NVL72": dict(N=72, F4=15e15, F8=5e15, hbm=288, hbmbw=8e12, P=135e3 / 72),
    "Rubin NVL72": dict(N=72, F4=35e15, F8=17.5e15, hbm=288, hbmbw=22e12, P=220e3 / 72),
    "Ironwood x128": dict(N=128, F4=4.6e15, F8=4.6e15, hbm=192, hbmbw=7.37e12, P=1200),
    "TPU 8i x128": dict(N=128, F4=10.1e15, F8=5e15, hbm=288, hbmbw=8.6e12, P=1300),
    "MI455X x72": dict(N=72, F4=40e15 * 0.7, F8=14e15, hbm=432, hbmbw=19.6e12, P=230e3 / 72),
}
CONT = dict(F4=24e15, F8=12e15, sram=9.2, srambw=256e12, hbm=144, hbmbw=10e12, P=2100)
LP30 = dict(sram=0.5, srambw=150e12, F4=1.2e15, F8=1.2e15, P=625)
WSE = dict(sram=44, srambw=43.2e15, F4=62e15, F8=62e15, P=43e3)  # FP16-class, no FP4


def gpu_points(s, tau):
    out = []
    for t in (1, 2, 4, 8):
        for B in [2 ** k for k in range(4, 17)]:
            N = s["N"]
            w_chip = LAYERS * N_EXP * B_EXP / N + (LAYERS * B_DENSE_LAYER + B_HEAD) / t
            users_chip = B * t / N
            if w_chip + users_chip * kv_store(CTX) > 0.9 * s["hbm"] * 1e9:
                continue
            mem = (LAYERS * touched(B) * B_EXP / N + (LAYERS * B_DENSE_LAYER + B_HEAD) / t
                   + users_chip * kv_read(CTX))
            comp = B / N * (LIN_FLOPS / s["F4"] + attn_flops(CTX) / s["F8"]) / ETA
            step = max(mem / s["hbmbw"], comp) + LAYERS * tau
            out.append((1 / step, B / step / (N * s["P"]) * 1e6, B, t))
    return out


def pipe_points(s, tau, kv_in_sram=False, hbm=True):
    """Weights stationary in SRAM, one pipeline stage per layer, microbatch b per stage."""
    out = []
    lay_b = N_EXP * B_EXP + B_DENSE_LAYER
    for b in [2 ** k for k in range(0, 12)]:
        users = LAYERS * b
        kv_layer = users * kv_store(CTX) / LAYERS
        need = lay_b + (kv_layer if kv_in_sram else 0)
        g = need / (0.9 * s["sram"] * 1e9)
        if not kv_in_sram:
            g = max(math.ceil(g), 1)
            if kv_layer > 0.9 * g * s["hbm"] * 1e9:
                continue
        sram_t = (touched(b) * B_EXP + B_DENSE_LAYER) / (g * s["srambw"])
        kvbw = s["srambw"] if kv_in_sram else s["hbmbw"]
        kv_t = b * kv_read(CTX) / LAYERS / (g * kvbw)
        comp = b * (LIN_FLOPS / s["F4"] + attn_flops(CTX) / s["F8"]) / LAYERS / g / ETA
        stage = (max(sram_t + kv_t, comp) if kv_in_sram else max(sram_t, kv_t, comp)) + tau
        N = LAYERS * g + 1
        out.append((1 / (LAYERS * stage), b / stage / (N * s["P"]) * 1e6, b, round(N)))
    return out


def afd_points(tau):
    """Vera Rubin NVL72 (attention + KV, one layer per GPU) + Groq-3 LPX (experts)."""
    out = []
    r = GPU["Rubin NVL72"]
    g = math.ceil(N_EXP * B_EXP / (0.9 * LP30["sram"] * 1e9))
    for b in [2 ** k for k in range(0, 12)]:
        users = LAYERS * b
        if users * kv_store(CTX) / LAYERS > 0.9 * r["hbm"] * 1e9:
            continue
        att = max((B_DENSE_LAYER + b * kv_read(CTX) / LAYERS) / r["hbmbw"],
                  b * attn_flops(CTX) / LAYERS / r["F8"] / ETA)
        ffn = max(touched(b) * B_EXP / (g * LP30["srambw"]),
                  b * 2 * TOPK * EXPERT_PARAMS / (g * LP30["F8"] * ETA))
        stage = max(att, ffn) + tau
        P = 72 * r["P"] + LAYERS * g * LP30["P"]
        out.append((1 / (LAYERS * stage), b / stage / P * 1e6, b, LAYERS * g))
    return out


TIERS = (50, 100, 200, 400, 1000, 2000)


def best(points):
    res = []
    for tier in TIERS:
        ok = [p for p in points if p[0] >= tier]
        res.append(max(ok, key=lambda p: p[1]) if ok else None)
    return res


def fmt(name, pts):
    cells = []
    for p in best(pts):
        cells.append(f"{p[1]:>9,.0f}" if p else f"{'--':>9}")
    mx = max(p[0] for p in pts) if pts else 0
    print(f"{name:<34}" + "".join(cells) + f"   max {mx:,.0f}")


if __name__ == "__main__":
    print(f"context {CTX:,}: weights {W_TOTAL/1e9:.0f} GB, KV/user {kv_store(CTX)/1e9:.2f} GB, "
          f"KV read/step {kv_read(CTX)/1e6:.0f} MB, attn {attn_flops(CTX)/1e9:.0f} GF, "
          f"linear {LIN_FLOPS/1e9:.0f} GF per token")
    print("tok/s per provisioned MW at >= tok/s/user tier")
    print(f"{'system (per-layer tau)':<34}" + "".join(f"{t:>9}" for t in TIERS))
    for name, s in GPU.items():
        for tau in (40e-6, 15e-6):
            fmt(f"{name} ({tau*1e6:.0f}us)", gpu_points(s, tau))
    for tau in (8e-6, 4e-6):
        fmt(f"Rubin+LPX AFD ({tau*1e6:.0f}us)", afd_points(tau))
    for tau in (6e-6, 3e-6):
        fmt(f"CS-4 wafers ({tau*1e6:.0f}us)", pipe_points(WSE, tau, kv_in_sram=True))
    for tau in (12e-6, 8e-6, 5e-6, 3e-6, 2e-6):
        fmt(f"Continuum ({tau*1e6:.0f}us)", pipe_points(CONT, tau))
