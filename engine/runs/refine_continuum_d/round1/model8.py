"""Round 8 (refine_continuum_d/round1): per-layer-type pipeline stages for Continuum, plus symmetric fixes.

Imports round7/model7.py and round6/model5.py unchanged. New here:
  * Stage model: each V4 layer type (30 CSA, 31 HCA, 1 MTP) gets its own package count g; the pipeline runs at
    its slowest stage (critic correction A). npk = 30 gC + 31 gH + gM + 1.
  * Heterogeneous packages (Continuum-8): same C-dies and W-tier everywhere; HBM stacks per package h in {0,2,3,4}
    chosen per stage type. Options: CSA indexer keys held in the W-tier SRAM (idx_sram); HCA-layer KV (and SWA
    window) held in the W-tier SRAM (kv_sram) so HCA packages can ship with h = 0. All capacity-checked.
  * Hot-expert replication: imbalance 1.07 (GPU parity, EPLB-like) only if the stage has free SRAM for 12.5% expert
    replicas (DeepSeek EPLB uses 32 redundant of 256 = 12.5%); otherwise 1.12.
  * Optional two-phase (no weight/attention overlap) bracket, applied to Rubin too (critic correction C).
  * Rubin host trim parameter (critic correction B).
"""
import math, sys, os
R7 = "/home/user/SomeRepository/engine/runs/refine_continuum/round7"
sys.path[:0] = [R7, R7 + "/../round6"]
import model7 as q, model5 as m

M = m.V4
STACK_GB, STACK_BW, STACK_W = 48.0, 2.5e12, 80.0
REP = 0.125


def layer_types(ctx, M=M):
    E = m.entry()
    idx_r = ctx / m.M_CSA * m.IDX_B
    csa = dict(n=m.N_CSA, kvr=(m.TOPK_ATT + m.WIN) * E, idxr=idx_r, f8=(m.TOPK_ATT + m.WIN) * m.FPE,
               f4=ctx / m.M_CSA * m.IDX_FLOP, kvs=ctx / m.M_CSA * E + m.WIN * E, idxs=idx_r)
    hca = dict(n=m.N_HCA, kvr=(ctx / m.M_HCA + m.WIN) * E, idxr=0.0, f8=(ctx / m.M_HCA + m.WIN) * m.FPE, f4=0.0,
               kvs=ctx / m.M_HCA * E + m.WIN * E, idxs=0.0)
    mtp = dict(n=1, kvr=0.0, idxr=0.0, f8=0.0, f4=0.0, kvs=0.0, idxs=0.0)
    return csa, hca, mtp


def c8_profiles(base, parts, h, labels=None):
    pr = q.cont_prof(base, dict(parts, other_w=STACK_W * h + 144))
    return {l: (s, f) for l, s, f in pr if labels is None or l in labels}


def stage(s, typ, g, h, b, pos, L, users, idx_sram, kv_sram, two_phase=False, imb_fixed=None):
    """returns (c seconds, ok) for one stage of this type"""
    exp_b = M["n_exp"] * m.b_exp(M) / g
    dense_b = m.b_dense(M)
    sram_cap = 0.9 * s["sram"] * 1e9
    in_sram = exp_b + dense_b
    hbm_store = 0.0
    kv_rd_sram = kv_rd_hbm = 0.0
    if kv_sram:
        in_sram += users * (typ["kvs"]) / g; kv_rd_sram += b * typ["kvr"] / g
    else:
        hbm_store += users * typ["kvs"] / g; kv_rd_hbm += b * typ["kvr"] / g
    if typ["idxs"]:
        if idx_sram:
            in_sram += users * typ["idxs"] / g; kv_rd_sram += b * typ["idxr"] / g
        else:
            hbm_store += users * typ["idxs"] / g; kv_rd_hbm += b * typ["idxr"] / g
    if in_sram > sram_cap or hbm_store > 0.9 * h * STACK_GB * 1e9: return None
    if (kv_rd_hbm > 0) and h == 0: return None
    imb = imb_fixed or (q.IMB_G if sram_cap - in_sram >= REP * exp_b else q.IMB_C)
    lin = 2 * (M["topk"] * M["exp"] + M["dense"]) + 2 * M["head"] / L
    cL = b * pos * imb * lin / (s["F4"] * s["s"]) / m.ETA / g
    cA = b * pos * imb * (typ["f8"] / s["F8"] + typ["f4"] / s["F4"]) / m.ETA / g
    sw = (m.touched(M, b * pos) * m.b_exp(M) / g + dense_b) / s["srambw"]
    sk = kv_rd_sram / s["srambw"]
    hk = kv_rd_hbm / (h * STACK_BW) if h else 0.0
    lnk = b * pos * (M["hid"] * (g - 1) / g + 2 * M["hid"]) / s["link"]
    if two_phase:
        return max(max(sw, cL) + max(sk + hk, cA), lnk)
    return max(sw + sk, hk, cL + cA, lnk)


def pareto(opts):
    """opts: list of (c, watts, desc). keep min watts for increasing c"""
    opts.sort(key=lambda x: (x[0], x[1])); out = []; best = float("inf")
    for o in opts:
        if o[1] < best: out.append(o); best = o[1]
    return out


def c8_env(base, parts, ctx, p=0.8, labels=("0.55V wt", "0.60V wt", "0.65V wt", "0.55V", "0.60V", "0.75V"),
           hs_csa=(2, 3, 4), hs_hca=(0, 2, 4), idx_opts=(False, True), hca_sram_opts=(False, True),
           gmax=14, two_phase=False, imb_fixed=None, tiers=q.T, ks=range(8), tau_fn=None):
    tau_fn = tau_fn or q.tau_f
    csa, hca, mtp = layer_types(ctx)
    profs = {h: c8_profiles(base, parts, h, labels) for h in set(hs_csa) | set(hs_hca) | {0}}
    res = {}
    mx = 0
    for lab in labels:
        for k in ks:
            pos, tok, L = m.spec(M, k, p)
            for mm in m.MS:
                for b in m.BGRID:
                    users = mm * b * L
                    tau = tau_fn(profs[0][lab][1])
                    sets = []
                    for typ, hs, opts in ((csa, hs_csa, [(i, False) for i in idx_opts]),
                                          (hca, hs_hca, [(False, ks_) for ks_ in hca_sram_opts]),
                                          (mtp, (0,), [(False, True)])):
                        o = []
                        for h in hs:
                            s, f = profs[h][lab]
                            for idx_s, kv_s in opts:
                                for g in range(1, gmax + 1):
                                    c = stage(s, typ, g, h, b, pos, L, users, idx_s, kv_s, two_phase, imb_fixed)
                                    if c is not None:
                                        o.append((c, typ["n"] * g * s["P"], (g, h, idx_s, kv_s), typ["n"] * g, typ["n"] * g * h))
                        if typ is mtp and k == 0: o = [(0.0, 0.0, (0, 0, 0, 0), 0, 0)]
                        sets.append(pareto(o))
                    if not all(sets): continue
                    head_w = profs[4][lab][0]["P"]
                    for oc in sets[0]:
                        for oh in sets[1]:
                            for om in sets[2]:
                                c = max(oc[0], oh[0], om[0])
                                T = max(mm * c, c + tau)
                                W = oc[1] + oh[1] + om[1] + head_w
                                npk = oc[3] + oh[3] + om[3] + 1
                                stacks = oc[4] + oh[4] + om[4] + 4
                                eff = m.DERATE * mm * b * tok / T / W
                                spd = tok / (L * T)
                                mx = max(mx, spd)
                                for t in tiers:
                                    if spd >= t and (t not in res or eff > res[t][0]):
                                        res[t] = (eff, dict(lab=lab, k=k, m=mm, b=b, C=oc[2], H=oh[2], Mt=om[2], npk=npk,
                                                            stacks=stacks, spd=spd, T=T, c=(oc[0], oh[0], om[0]),
                                                            W=W, users=users))
    res["max"] = mx
    return res


# ---- GPU side ----------------------------------------------------------------------------------------------
def rubin_prof(trim=0.0, s=1.43):
    return [(l, dict(x, P=x["P"] - trim, s=s), f) for l, x, f in q.RUBIN_PROF()]


def gpu2(s, tau, ctx, k, p, M=m.V4, ms=m.MS):
    """critic's two-phase GPU model (weights phase and attention phase serialise within a microbatch)"""
    pos, tok, L = m.spec(M, k, p); N, out = s["N"], []
    f8, f4a = m.attn_flops(M, ctx)
    for t in (1, 2, 4, 8):
        wb = L * M["n_exp"] * m.b_exp(M) / N + (L * m.b_dense(M) + M["head"] * 4.5 / 8) / t
        for mm in ms:
            for Bm in m.BGRID:
                B = Bm * mm
                if wb + B * t / N * m.kv_store(M, ctx) > 0.9 * s["hbm"] * 1e9: break
                n = Bm * pos / N
                memW = (L * m.touched(M, Bm * pos) * m.b_exp(M) / N + (L * m.b_dense(M) + M["head"] * 4.5 / 8) / t) / s["hbmbw"]
                memK = Bm * t / N * m.kv_read(M, ctx) / s["hbmbw"]
                cL = n * s["imb"] * m.lin_flops(M, L) / (s["F4"] * s["s"]) / m.ETA
                cA = n * s["imb"] * (f8 / s["F8"] + f4a / s["F4"]) / m.ETA
                lnk = n * L * m.a2a(M) * (N - 1) / N / s["link"]
                c = max(max(memW, cL) + max(memK, cA), lnk) / L
                T = max(mm * c, c + tau)
                out.append((tok / (L * T), m.DERATE * B * tok / (L * T) / (N * s["P"]), B, (t, mm), {}))
    return out


def gpu_env(profs, ctx, p=0.8, two_phase=False):
    if not two_phase: return q.gpu_env(profs, ctx, p=p)
    old = m.gpu_points; m.gpu_points = gpu2
    try: return q.gpu_env(profs, ctx, p=p)
    finally: m.gpu_points = old


def ultra4_prof(trim=0.0):
    """bottom-up 4-die Ultra (round 7), 5.69 kW per package incl. ~1 kW rack overhead"""
    return q.profiles(dict(q.ultra(5690 - trim), P_maxq=5690 - trim), comp_w=3440, leak_w=300, other_w=0,
                      rack_share=0.83, vendor_maxq=False)


def ultra2_prof(trim=0.0):
    """reported 2-die Ultra (Tom's Hardware / igorsLAB / hwbusters, June 2026; unconfirmed by Nvidia):
    Rubin-class compute, 8 HBM4E stacks. Modelled as Rubin with 512 GB, 22 TB/s, +100 W for larger stacks."""
    base = dict(q.RUBIN, hbm=512, P=q.RUBIN["P"] + 100 - trim, P_maxq=q.RUBIN["P_maxq"] + 100 - trim)
    return q.profiles(base, comp_w=1720, leak_w=150, other_w=0, rack_share=0.83)


# Continuum-8 parts: same C-dies/W-tier/links as C7T; HBM per package set by c8_profiles
C8 = dict(q.C7T)
C8_PARTS = dict(q.C7T_PARTS)


def fmt(e, ts=q.T): return " ".join(f"{e[t][0]:6.1f}" if t in e else "    --" for t in ts)


def rat(a, b, ts=q.T): return " ".join(f"{a[t][0]/b[t][0]:6.2f}" if t in a and t in b else "    --" for t in ts)
