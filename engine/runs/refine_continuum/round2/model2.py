"""Round-2 decode/prefill roofline + latency model, DeepSeek-V4-Pro-class MoE.

Changes vs round1/model.py: fine batch grid; CS-4 at 25 PF dense (250 PF is sparse);
MTP (1 draft, p=0.8 acceptance) available for every system; Continuum pipeline-fill derate;
prefill blending; GB300 calibration against InferenceMAX 8K/1K; equal-tau GPU rows.
Usage: python3 model2.py [context] [mtp 0|1]
"""
import math, sys

CTX = int(sys.argv[1]) if len(sys.argv) > 1 else 131072
MTP = int(sys.argv[2]) if len(sys.argv) > 2 else 0
P_ACC = 0.8                                   # draft acceptance (assumption)
POS = 1 + MTP                                 # positions computed per user per step
TOK = 1 + MTP * P_ACC                         # accepted tokens per user per step

LAYERS, N_EXP, TOPK = 61, 384, 6
EXPERT_PARAMS = 3 * 7168 * 3072
DENSE_PARAMS_LAYER = 0.35e9 + EXPERT_PARAMS
HEAD_PARAMS = 129280 * 7168
B_EXP = EXPERT_PARAMS * 4.5 / 8
B_DENSE_LAYER = DENSE_PARAMS_LAYER * 8.25 / 8
B_HEAD = HEAD_PARAMS * 4.5 / 8
N_CSA, N_HCA = 30, 31
ENTRY = 448 + 64 * 2
TOPK_ATT, WIN, M_CSA, M_HCA = 1024, 128, 4, 128
IDX_B, IDX_FLOP = 128 * 0.5, 64 * 128 * 2
FLOP_PER_ENTRY = 128 * 2 * (512 + 512)


def kv_store(L):
    return N_CSA * (L / M_CSA * (ENTRY + IDX_B) + WIN * ENTRY) + N_HCA * (L / M_HCA * ENTRY + WIN * ENTRY)


def kv_read(L):
    return N_CSA * ((TOPK_ATT + WIN) * ENTRY + L / M_CSA * IDX_B) + N_HCA * ((L / M_HCA + WIN) * ENTRY)


def attn_flops(L):
    return N_CSA * ((TOPK_ATT + WIN) * FLOP_PER_ENTRY + L / M_CSA * IDX_FLOP) + \
        N_HCA * ((L / M_HCA + WIN) * FLOP_PER_ENTRY)


LIN_FLOPS = 2 * (TOPK * EXPERT_PARAMS * LAYERS + DENSE_PARAMS_LAYER * LAYERS + HEAD_PARAMS)
W_TOTAL = LAYERS * (N_EXP * B_EXP + B_DENSE_LAYER) + B_HEAD


def touched(n_tok):
    return N_EXP * (1 - (1 - TOPK / N_EXP) ** n_tok)


def pre_flops(L_ctx):
    """Prefill FLOPs per prompt token at average causal position L_ctx/2 (CSA/HCA prefill)."""
    return LIN_FLOPS + attn_flops(L_ctx / 2)


ETA = 0.6
DERATE = 0.85  # same system derate for all: GPU EP imbalance/stragglers, pipeline fill/bubbles
# P = provisioned W per accelerator slot = rack (or pod) power / accelerators, incl. host,
# switches, NICs, power conversion. Continuum: 1.8 kW TDP + 0.3 kW host/switch/conversion share.
SYS = {
    "GB300 NVL72": dict(N=72, F4=15e15, F8=5e15, hbm=288, hbmbw=8e12, P=135e3 / 72),
    "Rubin NVL72": dict(N=72, F4=35e15, F8=17.5e15, hbm=288, hbmbw=22e12, P=220e3 / 72),
    "Rubin (50PF dense)": dict(N=72, F4=50e15, F8=17.5e15, hbm=288, hbmbw=22e12, P=220e3 / 72),
    "MI455X x72": dict(N=72, F4=28e15, F8=14e15, hbm=432, hbmbw=19.6e12, P=230e3 / 72),
    "TPU 8i x128": dict(N=128, F4=10.1e15, F8=5.05e15, hbm=288, hbmbw=8.6e12, P=1300),
    "Ironwood x128": dict(N=128, F4=4.6e15, F8=4.6e15, hbm=192, hbmbw=7.37e12, P=1200),
}
CONT = dict(F4=24e15, F8=12e15, sram=9.2, srambw=256e12, hbm=144, hbmbw=10e12, P=2100)
LP30 = dict(sram=0.5, srambw=150e12, F4=1.2e15, F8=1.2e15, P=625)
WSE = dict(sram=44, srambw=43.2e15, F4=25e15, F8=25e15, P=43e3)
BGRID = sorted(set([int(round(1.15 ** k)) for k in range(0, 85)]))


def gpu_points(s, tau, ctx=CTX):
    out = []
    for t in (1, 2, 4, 8):
        for B in BGRID:
            N = s["N"]
            w_chip = LAYERS * N_EXP * B_EXP / N + (LAYERS * B_DENSE_LAYER + B_HEAD) / t
            if w_chip + B * t / N * kv_store(ctx) > 0.9 * s["hbm"] * 1e9:
                continue
            mem = (LAYERS * touched(B * POS) * B_EXP / N + (LAYERS * B_DENSE_LAYER + B_HEAD) / t
                   + B * t / N * kv_read(ctx))
            comp = B * POS / N * (LIN_FLOPS / s["F4"] + attn_flops(ctx) / s["F8"]) / ETA
            step = max(mem / s["hbmbw"], comp) + LAYERS * tau
            out.append((TOK / step, DERATE * B * TOK / step / (N * s["P"]) * 1e6, B, t))
    return out


def pipe_points(s, tau, kv_in_sram=False, ctx=CTX, gmin=1):
    out = []
    lay_b = N_EXP * B_EXP + B_DENSE_LAYER
    for b in BGRID:
        kv_layer = b * kv_store(ctx)                 # LAYERS*b users, 1/LAYERS of their KV
        need = lay_b + (kv_layer if kv_in_sram else 0)
        g = need / (0.9 * s["sram"] * 1e9)
        if not kv_in_sram:
            g = max(math.ceil(g), gmin)
            if kv_layer > 0.9 * g * s["hbm"] * 1e9:
                continue
        sram_t = (touched(b * POS) * B_EXP + B_DENSE_LAYER) / (g * s["srambw"])
        kvbw = s["srambw"] if kv_in_sram else s["hbmbw"]
        kv_t = b * kv_read(ctx) / LAYERS / (g * kvbw)
        comp = b * POS * (LIN_FLOPS / s["F4"] + attn_flops(ctx) / s["F8"]) / LAYERS / g / ETA
        stage = (max(sram_t + kv_t, comp) if kv_in_sram else max(sram_t, kv_t, comp)) + tau
        N = LAYERS * g + 1
        out.append((TOK / (LAYERS * stage), DERATE * b * TOK / stage / (N * s["P"]) * 1e6, b, round(N)))
    return out


def afd_points(tau, ctx=CTX):
    out = []
    r = SYS["Rubin NVL72"]
    g = math.ceil(N_EXP * B_EXP / (0.9 * LP30["sram"] * 1e9))
    for b in BGRID:
        if b * kv_store(ctx) > 0.9 * r["hbm"] * 1e9:
            continue
        att = max((B_DENSE_LAYER + b * kv_read(ctx) / LAYERS) / r["hbmbw"],
                  b * POS * attn_flops(ctx) / LAYERS / r["F8"] / ETA)
        ffn = max(touched(b * POS) * B_EXP / (g * LP30["srambw"]),
                  b * POS * 2 * TOPK * EXPERT_PARAMS / (g * LP30["F8"] * ETA))
        stage = max(att, ffn) + tau
        P = 72 * r["P"] + LAYERS * g * LP30["P"]
        out.append((TOK / (LAYERS * stage), DERATE * b * TOK / stage / P * 1e6, b, LAYERS * g))
    return out


TIERS = (50, 100, 200, 400, 1000, 2000)


def best(points):
    res = []
    for tier in TIERS:
        ok = [p for p in points if p[0] >= tier]
        res.append(max(ok, key=lambda p: p[1]) if ok else None)
    return res


def prefill_rate(F4, F8, P, ctx, eta=ETA):
    """Prompt tokens/s per MW, compute-bound."""
    t = (LIN_FLOPS / F4 + (attn_flops(ctx / 2)) / F8) / eta
    return 1 / t / P * 1e6


def blend(dec, pre, k):
    """Output tok/s/MW when every output token also costs k prefill tokens on the same fleet."""
    return 1 / (1 / dec + k / pre)


def systems(ctx=CTX):
    rows = []
    for name in ("GB300 NVL72", "Rubin NVL72", "Rubin (50PF dense)", "MI455X x72", "TPU 8i x128", "Ironwood x128"):
        s = SYS[name]
        for tau in (40e-6, 15e-6, 8e-6, 3e-6):
            rows.append((f"{name} ({tau*1e6:.0f}us)", gpu_points(s, tau, ctx), s))
    for tau in (8e-6, 4e-6):
        rows.append((f"Rubin+LPX AFD ({tau*1e6:.0f}us)", afd_points(tau, ctx), None))
    for tau in (6e-6, 3e-6):
        rows.append((f"CS-4 wafers ({tau*1e6:.0f}us)", pipe_points(WSE, tau, True, ctx), WSE))
    for tau in (12e-6, 8e-6, 5e-6, 3e-6):
        rows.append((f"Continuum ({tau*1e6:.0f}us)", pipe_points(CONT, tau, False, ctx), CONT))
    return rows


if __name__ == "__main__":
    print(f"ctx {CTX:,} MTP={MTP}: weights {W_TOTAL/1e9:.0f} GB, KV/user {kv_store(CTX)/1e9:.3f} GB, "
          f"KV read/step {kv_read(CTX)/1e6:.0f} MB, attn {attn_flops(CTX)/1e9:.1f} GF, linear {LIN_FLOPS/1e9:.0f} GF")
    print("decode output tok/s per provisioned MW (millions) at >= tok/s/user tier")
    print(f"{'system':<32}" + "".join(f"{t:>8}" for t in TIERS) + "     max")
    for name, pts, _ in systems():
        cells = "".join(f"{p[1]/1e6:8.1f}" if p else f"{'--':>8}" for p in best(pts))
        print(f"{name:<32}{cells}  {max(p[0] for p in pts):6,.0f}")
