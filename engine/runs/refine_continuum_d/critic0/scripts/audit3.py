"""Critic audit 3: pipeline stage heterogeneity. model5.pipe_points averages KV reads and attention/indexer FLOPs over
all L layers, but a layer pipeline runs at the pace of its slowest stage. V4 has 30 CSA layers (indexer keys read in full,
L/4 x 64 B + 1152 x 576 B per user) and 31 HCA layers (1152 x 576 B at 128K). Here each layer type gets its own g, the
cycle is set by the slowest stage, and package count = 30 gC + 31 gH + gM (MTP) + 1. Same profiles, eta, imb, tau(f).
Option hca_sram: HCA-layer KV (and SWA windows) held in the idle W-tier SRAM of HCA stages (capacity-checked)."""
import sys, math
R7 = "/home/user/SomeRepository/engine/runs/refine_continuum/round7"
sys.path[:0] = [R7, R7 + "/../round6"]
import model7 as q, model5 as m
M = m.V4; E = m.entry()
def per_layer(ctx):
    csa = dict(kvr=(m.TOPK_ATT + m.WIN) * E + ctx / m.M_CSA * m.IDX_B, f8=(m.TOPK_ATT + m.WIN) * m.FPE,
               f4=ctx / m.M_CSA * m.IDX_FLOP, kvs=ctx / m.M_CSA * (E + m.IDX_B) + m.WIN * E)
    hca = dict(kvr=(ctx / m.M_HCA + m.WIN) * E, f8=(ctx / m.M_HCA + m.WIN) * m.FPE, f4=0.0,
               kvs=ctx / m.M_HCA * E + m.WIN * E)
    mtp = dict(kvr=0.0, f8=0.0, f4=0.0, kvs=0.0)
    return csa, hca, mtp
def stage(s, tau, typ, g, b, pos, L, hca_sram=False):
    lin = 2 * (M["topk"] * M["exp"] + M["dense"]) + 2 * M["head"] / L
    comp = b * pos * s["imb"] * (lin / (s["F4"] * s["s"]) + typ["f8"] / s["F8"] + typ["f4"] / s["F4"]) / m.ETA / g
    sram_b = m.touched(M, b * pos) * m.b_exp(M) / g + m.b_dense(M)
    kv = b * typ["kvr"] / g
    if hca_sram: sram_b += kv; kv_t = 0.0
    else: kv_t = kv / s["hbmbw"]
    sram = sram_b / s["srambw"]
    lnk = b * pos * (M["hid"] * (g - 1) / g + 2 * M["hid"]) / s["link"]
    return max(sram, kv_t, comp, lnk)
def env(profs, ctx, p=0.8, hca_sram=False, avg=False, hbm_free_hca=False):
    csa, hca, mtp = per_layer(ctx); res = {}
    lay_w = M["n_exp"] * m.b_exp(M) + m.b_dense(M)
    for lab, s0, f in profs:
        tau = q.tau_f(f)
        for k in range(8):
            pos, tok, L = m.spec(M, k, p)
            for mm in m.MS:
                for b in m.BGRID:
                    users_stage = mm * b  # users resident per stage (x L stages in flight)
                    best = None
                    for gC in range(1, 13):
                        if users_stage * L * csa["kvs"] > 0.9 * gC * s0["hbm"] * 1e9: continue
                        cC = stage(s0, tau, csa, gC, b, pos, L)
                        for gH in range(1, 13):
                            s = s0
                            if hca_sram:
                                if lay_w + users_stage * L * hca["kvs"] > 0.9 * gH * s0["sram"] * 1e9: continue
                            elif users_stage * L * hca["kvs"] > 0.9 * gH * s0["hbm"] * 1e9: continue
                            cH = stage(s0, tau, hca, gH, b, pos, L, hca_sram)
                            for gM in range(1, 13) if k else (0,):
                                cM = stage(s0, tau, mtp, gM, b, pos, L) if k else 0
                                c = max(cC, cH, cM)
                                T = max(mm * c, c + tau)
                                npk = 30 * gC + 31 * gH + gM + 1
                                Pavg = s0["P"]
                                if hbm_free_hca:  # HCA packages built without HBM: save 4 x 80 W x 1.146
                                    Pavg = (s0["P"] * (npk - 31 * gH) + (s0["P"] - 320 * 1.146) * 31 * gH) / npk
                                eff = m.DERATE * mm * b * tok / T / (npk * Pavg)
                                spd = tok / (L * T)
                                for t in q.T:
                                    if spd >= t and (t not in res or eff > res[t][0]):
                                        res[t] = (eff, f"{lab} k{k} m{mm} b{b} gC{gC} gH{gH} gM{gM} pk{npk}", spd)
    return res
for ctx in (q.C128, q.C1M):
    R = q.gpu_env(q.RUBIN_PROF(), ctx)
    profs = [p for p in q.cont_prof(q.C7T, q.C7T_PARTS) if p[0] in ("0.55V wt", "0.60V wt", "0.65V wt", "0.55V", "0.60V")]
    A0 = q.pipe_env(profs, ctx, gs=(1, 2, 3, 4, 6))
    print(f"== {ctx//1024}K   Rubin best: " + q.vals(R))
    print("  C7 averaged-layer model (as answer)  " + q.vals(A0) + "   ratio " + q.ratio(A0, R))
    for lab, kw in (("per-layer-type stages, uniform tool", dict()),
                    ("  + HCA KV in idle W-tier SRAM", dict(hca_sram=True)),
                    ("  + HCA packages built without HBM", dict(hca_sram=True, hbm_free_hca=True))):
        A = env(profs, ctx, **kw)
        print(f"  {lab:<37}" + " ".join(f"{A[t][0]:6.1f}" if t in A else "    --" for t in q.T) +
              "   ratio " + " ".join(f"{A[t][0]/R[t][0]:5.2f}" if t in A else "   --" for t in q.T))
        for t in (200, 1000, 2000):
            if t in A: print(f"      >={t}: {A[t][1]} {A[t][2]:,.0f} tok/s/user")
