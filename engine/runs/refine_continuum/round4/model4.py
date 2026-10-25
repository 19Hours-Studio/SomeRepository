"""Round-4 decode model (DeepSeek-V4-Pro-class MoE). Self-contained rewrite of round3/model3.py.

Changes vs model3:
  * functions take (ctx, k, p) explicitly instead of reloading the module per argv;
  * GPU/TPU expert-parallel all-to-all bandwidth term (dispatch FP8 + combine BF16), assumed
    perfectly overlapped: step = max(HBM, compute, scale-up link) + layers * tau;
  * Continuum link-bandwidth term per stage (all-gather FP8 + reduce-scatter BF16 + next-stage hop);
  * per-system tau (exposed per-layer latency) so measured-implied values can be used;
  * drafter = one MoE-layer-equivalent block drafter (DSpark/DFlash-style, all k drafts in one pass).
"""
import math

LAYERS0, N_EXP, TOPK, HID = 61, 384, 6, 7168
EXPERT_PARAMS = 3 * HID * 3072
DENSE_PARAMS_LAYER = 0.35e9 + EXPERT_PARAMS          # attention + shared expert
HEAD_PARAMS = 129280 * HID
B_EXP = EXPERT_PARAMS * 4.5 / 8                      # NVFP4
B_DENSE_LAYER = DENSE_PARAMS_LAYER * 8.25 / 8        # FP8 + scales
B_HEAD = HEAD_PARAMS * 4.5 / 8
N_CSA, N_HCA = 30, 31
ENTRY = 448 + 64 * 2                                 # FP8 latent + BF16 RoPE dims
TOPK_ATT, WIN, M_CSA, M_HCA = 1024, 128, 4, 128
IDX_B, IDX_FLOP = 128 * 0.5, 64 * 128 * 2
FLOP_PER_ENTRY = 128 * 2 * (512 + 512)
ETA, DERATE = 0.6, 0.85


def spec(k, p):
    """positions verified per user per step, expected accepted tokens, layer count incl. drafter"""
    return 1 + k, sum(p ** i for i in range(k + 1)), LAYERS0 + (1 if k else 0)


def kv_store(L):
    return N_CSA * (L / M_CSA * (ENTRY + IDX_B) + WIN * ENTRY) + N_HCA * (L / M_HCA * ENTRY + WIN * ENTRY)


def kv_read(L):
    return N_CSA * ((TOPK_ATT + WIN) * ENTRY + L / M_CSA * IDX_B) + N_HCA * ((L / M_HCA + WIN) * ENTRY)


def attn_flops(L):
    return N_CSA * ((TOPK_ATT + WIN) * FLOP_PER_ENTRY + L / M_CSA * IDX_FLOP) + N_HCA * ((L / M_HCA + WIN) * FLOP_PER_ENTRY)


def lin_flops(layers):
    return 2 * (TOPK * EXPERT_PARAMS * layers + DENSE_PARAMS_LAYER * layers + HEAD_PARAMS)


def touched(n_tok):
    return N_EXP * (1 - (1 - TOPK / N_EXP) ** n_tok)


A2A_BYTES = TOPK * (HID + 2 * HID)  # per token per MoE layer, leaving one GPU: FP8 dispatch + BF16 combine

# P = provisioned W per accelerator slot (rack power / accelerators: host, switches, NICs, conversion)
# link = scale-up bandwidth per direction (B/s)
SYS = {
    "GB300": dict(N=72, F4=15e15, F8=5e15, hbm=288, hbmbw=8e12, link=0.9e12, P=135e3 / 72),
    "Rubin35": dict(N=72, F4=35e15, F8=17.5e15, hbm=288, hbmbw=22e12, link=1.8e12, P=220e3 / 72),
    "Rubin50": dict(N=72, F4=50e15, F8=17.5e15, hbm=288, hbmbw=22e12, link=1.8e12, P=220e3 / 72),
    "MI455X": dict(N=72, F4=28e15, F8=14e15, hbm=432, hbmbw=19.6e12, link=1.8e12, P=230e3 / 72),
    "TPU8i": dict(N=128, F4=10.1e15, F8=5.05e15, hbm=288, hbmbw=8.6e12, link=1.2e12, P=1300),
    "Ironwood": dict(N=128, F4=4.6e15, F8=4.6e15, hbm=192, hbmbw=7.37e12, link=0.6e12, P=1200),
}
CONT = dict(F4=32e15, F8=16e15, sram=9.2, srambw=256e12, hbm=144, hbmbw=10e12, link=1.8e12 * 0.85, P=2450)
LP30 = dict(sram=0.5, srambw=150e12, F4=1.2e15, F8=1.2e15, P=625)
WSE = dict(sram=44, srambw=43.2e15, F4=25e15, F8=25e15, P=43e3)
BGRID = sorted(set([int(round(1.15 ** i)) for i in range(0, 85)]))


def gpu_points(s, tau, ctx, k, p, comm=True):
    pos, tok, L = spec(k, p)
    lf, af = lin_flops(L), attn_flops(ctx)
    out = []
    for t in (1, 2, 4, 8):
        for B in BGRID:
            N = s["N"]
            w_chip = L * N_EXP * B_EXP / N + (L * B_DENSE_LAYER + B_HEAD) / t
            if w_chip + B * t / N * kv_store(ctx) > 0.9 * s["hbm"] * 1e9:
                continue
            mem = (L * touched(B * pos) * B_EXP / N + (L * B_DENSE_LAYER + B_HEAD) / t + B * t / N * kv_read(ctx)) / s["hbmbw"]
            comp = B * pos / N * (lf / s["F4"] + af / s["F8"]) / ETA
            lnk = B * pos / N * L * A2A_BYTES * (N - 1) / N / s["link"] if comm else 0
            step = max(mem, comp, lnk) + L * tau
            out.append((tok / step, DERATE * B * tok / step / (N * s["P"]), B, t, dict(mem=mem, comp=comp, link=lnk, step=step)))
    return out


def pipe_points(s, tau, ctx, k, p, kv_in_sram=False, gmin=1, comm=True):
    pos, tok, L = spec(k, p)
    lf, af = lin_flops(L), attn_flops(ctx)
    lay_b = N_EXP * B_EXP + B_DENSE_LAYER
    out = []
    for b in BGRID:
        kv_layer = b * kv_store(ctx)
        need = lay_b + (kv_layer if kv_in_sram else 0)
        g = need / (0.9 * s["sram"] * 1e9)
        if not kv_in_sram:
            g = max(math.ceil(g), gmin)
            if kv_layer > 0.9 * g * s["hbm"] * 1e9:
                continue
        sram_t = (touched(b * pos) * B_EXP + B_DENSE_LAYER) / (g * s["srambw"])
        kvbw = s["srambw"] if kv_in_sram else s["hbmbw"]
        kv_t = b * kv_read(ctx) / L / (g * kvbw)
        comp = b * pos * (lf / s["F4"] + af / s["F8"]) / L / g / ETA
        lnk = b * pos * (HID * (g - 1) / g + 2 * HID) / s["link"] if (comm and "link" in s) else 0
        stage = (max(sram_t + kv_t, comp) if kv_in_sram else max(sram_t, kv_t, comp, lnk)) + tau
        N = L * g + 1
        out.append((tok / (L * stage), DERATE * b * tok / stage / (N * s["P"]), b, N,
                    dict(sram=sram_t, kv=kv_t, comp=comp, link=lnk, stage=stage, g=g)))
    return out


def afd_points(tau, ctx, k, p):
    pos, tok, L = spec(k, p)
    r = SYS["Rubin35"]
    g = math.ceil(N_EXP * B_EXP / (0.9 * LP30["sram"] * 1e9))
    out = []
    for b in BGRID:
        if b * kv_store(ctx) > 0.9 * r["hbm"] * 1e9:
            continue
        att = max((B_DENSE_LAYER + b * kv_read(ctx) / L) / r["hbmbw"], b * pos * attn_flops(ctx) / L / r["F8"] / ETA)
        ffn = max(touched(b * pos) * B_EXP / (g * LP30["srambw"]), b * pos * 2 * TOPK * EXPERT_PARAMS / (g * LP30["F8"] * ETA))
        stage = max(att, ffn) + tau
        P = 72 * r["P"] + L * g * LP30["P"]
        out.append((tok / (L * stage), DERATE * b * tok / stage / P, b, L * g, {}))
    return out


def envelope(fn, tiers, ks=range(8)):
    """best (tok/s/W, k, tok/s/user, point) at each tier over speculation depths k"""
    res = {}
    for k in ks:
        pts = fn(k)
        for t in tiers:
            ok = [q for q in pts if q[0] >= t]
            if ok:
                q = max(ok, key=lambda q: q[1])
                if t not in res or q[1] > res[t][0]:
                    res[t] = (q[1], k, q[0], q)
        mx = max(q[0] for q in pts)
        res["max"] = max(res.get("max", 0), mx)
    return res
