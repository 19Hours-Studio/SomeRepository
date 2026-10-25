"""Round-5 decode model. Extends round4/model4.py.

Changes vs model4 (all applied to every system unless stated):
  * model config is a dict (DeepSeek-V4-Pro and DeepSeek-R1), so the GPU model can be checked against
    the MLPerf v6.1 Vera Rubin / GB300 DeepSeek-R1 Interactive results;
  * V4 lightning-indexer scores run at the FP4 rate (V4 report: indexer attention computed in FP4);
  * microbatch interleaving m = 1..4 for every system: per-layer cycle T = max(m*c, c + tau), where c is the
    per-microbatch resource time (weights are re-read for each microbatch: from HBM on GPUs, from SRAM on
    pipelines). m = 1 reproduces model4. GPUs get this as two-batch overlap (SGLang/DeepSeek TBO);
  * zero-skip factor s on FP4 linear FLOPs for systems that have it (Rubin's "adaptive compression"; Continuum-5
    adds an offline-compressed equivalent). s=1.43 reproduces Rubin's 50 PF; s=1 is Rubin's 35 PF dense;
  * Rubin Max-Q power profile (190 kW rack, perf factor q); power per slot is a parameter for all.
"""
import math

V4 = dict(name="DSv4-Pro", L0=61, moe_layers=61, n_exp=384, topk=6, exp=3 * 7168 * 3072,
          dense=0.35e9 + 3 * 7168 * 3072, extra_dense=0, head=129280 * 7168, hid=7168, kind="v4")
R1 = dict(name="DSR1", L0=61, moe_layers=58, n_exp=256, topk=8, exp=3 * 7168 * 2048,
          dense=0.18e9 + 3 * 7168 * 2048, extra_dense=3 * (3 * 7168 * 18432 - 3 * 7168 * 2048),
          head=129280 * 7168, hid=7168, kind="mla")
# V4 attention constants (round 4)
N_CSA, N_HCA, ENTRY, TOPK_ATT, WIN, M_CSA, M_HCA = 30, 31, 448 + 64 * 2, 1024, 128, 4, 128
IDX_B, IDX_FLOP, FPE = 128 * 0.5, 64 * 128 * 2, 128 * 2 * (512 + 512)
MLA_B, MLA_FPE = 576 + 8, 128 * 2 * (576 + 512)
ETA, DERATE = 0.6, 0.85
OPT = dict(idx_fp4=True, kv_fp4=False)   # global switches (round-4 reproduction: idx_fp4=False)


def spec(M, k, p):
    return 1 + k, sum(p ** i for i in range(k + 1)), M["L0"] + (1 if k else 0)


def entry():
    return 448 * 4.5 / 8 + 64 * 2 if OPT["kv_fp4"] else ENTRY


def kv_store(M, L):
    ENTRY = entry()
    if M["kind"] == "mla":
        return M["L0"] * L * MLA_B
    return N_CSA * (L / M_CSA * (ENTRY + IDX_B) + WIN * ENTRY) + N_HCA * (L / M_HCA * ENTRY + WIN * ENTRY)


def kv_read(M, L):
    ENTRY = entry()
    if M["kind"] == "mla":
        return M["L0"] * L * MLA_B
    return N_CSA * ((TOPK_ATT + WIN) * ENTRY + L / M_CSA * IDX_B) + N_HCA * ((L / M_HCA + WIN) * ENTRY)


def attn_flops(M, L):
    """(FP8 flops, FP4 flops) per position"""
    if M["kind"] == "mla":
        return M["L0"] * L * MLA_FPE, 0.0
    f8 = N_CSA * (TOPK_ATT + WIN) * FPE + N_HCA * (L / M_HCA + WIN) * FPE
    if not OPT["idx_fp4"]:
        return f8 + N_CSA * L / M_CSA * IDX_FLOP, 0.0
    return f8, N_CSA * L / M_CSA * IDX_FLOP


def lin_flops(M, layers):
    return 2 * (M["topk"] * M["exp"] * M["moe_layers"] + M["dense"] * layers + M["extra_dense"] + M["head"]
                + (M["topk"] * M["exp"] if layers > M["L0"] else 0))


def touched(M, n_tok):
    return M["n_exp"] * (1 - (1 - M["topk"] / M["n_exp"]) ** n_tok)


def b_exp(M): return M["exp"] * 4.5 / 8
def b_dense(M): return M["dense"] * 8.25 / 8
def a2a(M): return M["topk"] * (M["hid"] + 2 * M["hid"])


SYS = {
    "GB300": dict(N=72, F4=15e15, F8=5e15, hbm=288, hbmbw=8e12, link=0.9e12, P=135e3 / 72, s=1.0),
    "Rubin": dict(N=72, F4=35e15, F8=17.5e15, hbm=288, hbmbw=22e12, link=1.8e12, P=220e3 / 72, s=1.0),
    "MI455X": dict(N=72, F4=28e15, F8=14e15, hbm=432, hbmbw=19.6e12, link=1.8e12, P=230e3 / 72, s=1.0),
    "TPU8i": dict(N=128, F4=10.1e15, F8=5.05e15, hbm=288, hbmbw=8.6e12, link=1.2e12, P=1300, s=1.0),
    "Ironwood": dict(N=128, F4=4.6e15, F8=4.6e15, hbm=192, hbmbw=7.37e12, link=0.6e12, P=1200, s=1.0),
}


def rubin(s=1.0, maxq=False, q=0.92):
    r = dict(SYS["Rubin"], s=s)
    if maxq:  # Max-Q: 190 kW rack, clocks lower -> compute x q (HBM unchanged)
        r.update(F4=r["F4"] * q, F8=r["F8"] * q, P=190e3 / 72)
    return r


# Continuum-5 package: as round 4, slot power re-derived with Rubin's methodology (see answer §3.1)
CONT = dict(F4=32e15, F8=16e15, sram=9.2, srambw=256e12, hbm=144, hbmbw=10e12, link=1.8e12 * 0.85, P=2800, s=1.0)
LP30 = dict(sram=0.5, srambw=150e12, F4=1.2e15, F8=1.2e15, P=625)
WSE = dict(sram=44, srambw=43.2e15, F4=25e15, F8=25e15, P=43e3, s=1.0)
BGRID = sorted(set([int(round(1.15 ** i)) for i in range(0, 85)]))
MS = (1, 2, 3, 4)


def comp_time(M, s, n_pos, layers, ctx, frac=1.0):
    f8, f4a = attn_flops(M, ctx)
    return n_pos * frac * s.get("imb", 1.0) * (lin_flops(M, layers) / (s["F4"] * s.get("s", 1.0)) + f8 / s["F8"] + f4a / s["F4"]) / ETA


def gpu_points(s, tau, ctx, k, p, M=V4, ms=MS):
    pos, tok, L = spec(M, k, p)
    N, out = s["N"], []
    for t in (1, 2, 4, 8):
        wb = L * M["n_exp"] * b_exp(M) / N + (L * b_dense(M) + M["head"] * 4.5 / 8) / t
        for m in ms:
            for Bm in BGRID:
                B = Bm * m
                if wb + B * t / N * kv_store(M, ctx) > 0.9 * s["hbm"] * 1e9:
                    break
                mem = (L * touched(M, Bm * pos) * b_exp(M) / N + (L * b_dense(M) + M["head"] * 4.5 / 8) / t
                       + Bm * t / N * kv_read(M, ctx)) / s["hbmbw"]
                comp = comp_time(M, s, Bm * pos / N, L, ctx)
                lnk = Bm * pos / N * L * a2a(M) * (N - 1) / N / s["link"]
                c = max(mem, comp, lnk) / L
                T = max(m * c, c + tau)
                out.append((tok / (L * T), DERATE * B * tok / (L * T) / (N * s["P"]), B, (t, m),
                            dict(mem=mem, comp=comp, link=lnk, T=T, c=c)))
    return out


def pipe_points(s, tau, ctx, k, p, M=V4, kv_in_sram=False, gmin=1, ms=MS):
    pos, tok, L = spec(M, k, p)
    lay_b = M["n_exp"] * b_exp(M) + b_dense(M)
    out = []
    for m in ms:
        for b in BGRID:
            kv_all = m * b * kv_store(M, ctx)
            if kv_in_sram:
                g = (lay_b + kv_all) / (0.9 * s["sram"] * 1e9)
            else:
                g = max(math.ceil(lay_b / (0.9 * s["sram"] * 1e9)), gmin)
                if kv_all > 0.9 * g * s["hbm"] * 1e9:
                    break
            sram_t = (touched(M, b * pos) * b_exp(M) + b_dense(M)) / (g * s["srambw"])
            kv_t = b * kv_read(M, ctx) / L / (g * (s["srambw"] if kv_in_sram else s["hbmbw"]))
            comp = comp_time(M, s, b * pos, L, ctx) / L / g
            lnk = b * pos * (M["hid"] * (g - 1) / g + 2 * M["hid"]) / s["link"] if "link" in s else 0
            c = max(sram_t + kv_t, comp) if kv_in_sram else max(sram_t, kv_t, comp, lnk)
            T = max(m * c, c + tau)
            Npk = L * g + 1
            out.append((tok / (L * T), DERATE * m * b * tok / T / (Npk * s["P"]), b, (Npk, m),
                        dict(sram=sram_t, kv=kv_t, comp=comp, link=lnk, T=T, c=c, g=g, users=m * b * L)))
    return out


def afd_points(tau, ctx, k, p, M=V4, r=None, ms=MS):
    """Rubin NVL72 (attention, KV) + LPX (experts in SRAM), static pipeline per layer"""
    r = r or rubin()
    pos, tok, L = spec(M, k, p)
    g = math.ceil(M["n_exp"] * b_exp(M) / (0.9 * LP30["sram"] * 1e9))
    out = []
    for m in ms:
        for b in BGRID:
            if m * b * kv_store(M, ctx) > 0.9 * 72 * r["hbm"] * 1e9 / L:
                break
            f8, f4a = attn_flops(M, ctx)
            att = max((b_dense(M) + b * kv_read(M, ctx) / L) / (72 * r["hbmbw"] / L),
                      b * pos * (f8 / r["F8"] + f4a / r["F4"]) / L / (72 / L) / ETA)
            ffn = max(touched(M, b * pos) * b_exp(M) / (g * LP30["srambw"]),
                      b * pos * 2 * M["topk"] * M["exp"] / (g * LP30["F8"] * ETA))
            c = max(att, ffn)
            T = max(m * c, c + tau)
            P = 72 * r["P"] + L * g * LP30["P"]
            out.append((tok / (L * T), DERATE * m * b * tok / T / P, b, (L * g, m), {}))
    return out


def envelope(fn, tiers, ks=range(8)):
    res = {}
    for k in ks:
        pts = fn(k)
        for t in tiers:
            ok = [q for q in pts if q[0] >= t]
            if ok:
                q = max(ok, key=lambda q: q[1])
                if t not in res or q[1] > res[t][0]:
                    res[t] = (q[1], k, q[0], q)
        if pts:
            res["max"] = max(res.get("max", 0), max(q[0] for q in pts))
    return res
