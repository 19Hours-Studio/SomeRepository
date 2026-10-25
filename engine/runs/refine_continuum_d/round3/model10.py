"""Round 10 (refine_continuum_d/round3): Continuum-10 = Continuum-9 + two corrections + one mapping change.
Imports model9 / model8 (copied unchanged from round2).

  * HO: stage hand-off bytes per position in units of hid. V4 uses mHC with hc_mult = 4, so the residual that
    crosses a package boundary is 4 streams x hid; BF16 -> HO = 8 (critic2 correction 1). model9 charged HO = 1.
  * pair=True ("layer-pair groups"): a CSA layer and the following HCA layer share one group of G packages. Each
    package owns 384/G whole experts of BOTH layers, and the attention of b/G users for BOTH layers
    (user-stationary), so the mHC residual stays on-package between the two layers; only one hand-off per pair.
    Cost: experts of a layer are spread over G (not g) packages, so D(G) > D(g) and dispatch bytes rise; every
    pair package carries HBM (CSA KV) -> h in (1..4). 30 pairs + 1 unpaired HCA stage + MTP + head.
    Pair layout pipeline: L/2 stages (30 pairs, the unpaired HCA layer, MTP+head), each holding m microbatches;
    c_pair = c_CSA + c_HCA (two layers back to back on the same packages); cycle Tp = max(m c, c + 2 tau) since a
    pair stage contains two per-layer fixed latencies; throughput m b tok / Tp; speed tok / ((L/2) Tp);
    users in flight m b L/2.
  * fixed host 110 W/slot (no KV-mirror DRAM; critic2 point 2).
"""
import model9 as e9
q, e8, m = e9.q, e9.e8, e9.m
M = e9.M
HO = 8.0


def _cap(s, typ, g, users, idx_sram, kv_sram):
    in_sram = hbm = 0.0
    if kv_sram: in_sram += users * typ["kvs"] / g
    else: hbm += users * typ["kvs"] / g
    if typ["idxs"]:
        if idx_sram: in_sram += users * typ["idxs"] / g
        else: hbm += users * typ["idxs"] / g
    return in_sram, hbm


def _terms(s, typ, g, h, b, pos, imb, idx_sram, kv_sram, L):
    """per-layer (sram_time, hbm_time, compute_time, dispatch+combine link time) on g packages, EP split"""
    dense_b = m.b_dense(M)
    kv_s = kv_h = 0.0
    if kv_sram: kv_s += b * typ["kvr"] / g
    else: kv_h += b * typ["kvr"] / g
    if typ["idxs"]:
        if idx_sram: kv_s += b * typ["idxr"] / g
        else: kv_h += b * typ["idxr"] / g
    if kv_h > 0 and h == 0: return None
    lin = 2 * (M["topk"] * M["exp"] + M["dense"]) + 2 * M["head"] / L
    cL = b * pos * imb * lin / (s["F4"] * s["s"]) / m.ETA / g
    cA = b * pos * imb * (typ["f8"] / s["F8"] + typ["f4"] / s["F4"]) / m.ETA / g
    sw = (imb * m.touched(M, b * pos) * m.b_exp(M) / g + dense_b) / s["srambw"]
    sk = kv_s / s["srambw"]
    hk = kv_h / (h * e8.STACK_BW) if h else 0.0
    lnk = imb * b * pos / g * M["hid"] * 3 * e9.D(g) * (g - 1) / g / s["link"] if g > 1 else 0.0
    return sw + sk, hk, cL + cA, lnk


def single(s, typ, g, h, b, pos, L, users, idx_sram, kv_sram, imb_fixed=None):
    exp_b = M["n_exp"] * m.b_exp(M) / g
    cap = e8.FILL * s["sram"] * 1e9
    a, hb = _cap(s, typ, g, users, idx_sram, kv_sram)
    in_sram = exp_b + m.b_dense(M) + a
    if in_sram > cap or hb > 0.9 * h * e8.STACK_GB * 1e9: return None
    imb = imb_fixed or (q.IMB_G if cap - in_sram >= e8.REP * exp_b else q.IMB_C)
    if e9.IMB_EP: imb = max(imb, e9.IMB_EP)
    t = _terms(s, typ, g, h, b, pos, imb, idx_sram, kv_sram, L)
    if t is None: return None
    ho = imb * HO * b * pos / g * M["hid"] / s["link"]
    return max(t[0], t[1], t[2], t[3] + ho)


def pair(s, csa, hca, G, h, b, pos, L, users, idx_sram, hca_kv_sram, imb_fixed=None):
    exp_b = M["n_exp"] * m.b_exp(M) / G
    cap = e8.FILL * s["sram"] * 1e9
    a1, h1 = _cap(s, csa, G, users, idx_sram, False)
    a2, h2 = _cap(s, hca, G, users, False, hca_kv_sram)
    in_sram = 2 * (exp_b + m.b_dense(M)) + a1 + a2
    if in_sram > cap or h1 + h2 > 0.9 * h * e8.STACK_GB * 1e9: return None
    imb = imb_fixed or (q.IMB_G if cap - in_sram >= e8.REP * 2 * exp_b else q.IMB_C)
    if e9.IMB_EP: imb = max(imb, e9.IMB_EP)
    tc = _terms(s, csa, G, h, b, pos, imb, idx_sram, False, L)
    th = _terms(s, hca, G, h, b, pos, imb, False, hca_kv_sram, L)
    if tc is None or th is None: return None
    ho = imb * HO * b * pos / G * M["hid"] / s["link"]
    return max(tc[0], tc[1], tc[2], tc[3] + ho) + max(th[0], th[1], th[2], th[3])   # full pair-stage time


def env(ctx, p=0.8, labels=("0.55V wt", "0.60V wt"), omega=0.7, lanes=64, gmax=14, Gmax=28, use_pair=True,
        hs_csa=(2, 3, 4), hs_hca=(0, 2, 4), hs_pair=(1, 2, 3, 4), imb_fixed=None, tiers=q.T, ks=range(7),
        tau_fn=None, s_static=None, spares=0.0, spare_mode="hot", parts_over=None, base_over=None, wt_dyn=1.0):
    tau_fn = tau_fn or q.tau_f
    csa, hca, mtp = e8.layer_types(ctx)
    profs = {}
    for h in set(hs_csa) | set(hs_hca) | set(hs_pair) | {0, 4}:
        old_b, old_p = dict(e8.C8), dict(e8.C8_PARTS)
        for k_, v in (base_over or {}).items(): e8.C8[k_] = old_b[k_] * v
        for k_, v in (parts_over or {}).items(): e8.C8_PARTS[k_] = old_p[k_] * v
        try: profs[h] = e9.design_profiles(h, omega, lanes, labels, s_static, wt_dyn)
        finally: e8.C8.clear(); e8.C8.update(old_b); e8.C8_PARTS.clear(); e8.C8_PARTS.update(old_p)
    sp = (1 + spares) if spare_mode == "hot" else (1 + 0.05 * spares)
    res, mx = {}, 0
    for lab in labels:
        tau = tau_fn(profs[0][lab][1])
        for k in ks:
            pos, tok, L = m.spec(M, k, p)
            for mm in m.MS:
                for b in m.BGRID:
                  for lay in (("single", "pair") if use_pair else ("single",)):
                    lpS = 1 if lay == "single" else 2
                    users = mm * b * L // lpS
                    # option A (Continuum-9 layout): 30 CSA stages + 31 HCA stages ; option B: 30 pairs + 1 HCA stage
                    def opts_single(typ, hs, ol, n):
                        o = []
                        for h in hs:
                            s, f = profs[h][lab]
                            for i_, k_ in ol:
                                for g in range(1, gmax + 1):
                                    c = single(s, typ, g, h, b, pos, L, users, i_, k_, imb_fixed)
                                    if c is not None: o.append((c, n * g * s["P"], ("S", g, h, i_, k_), n * g, n * g * h))
                        return e8.pareto(o)
                    mt = [(0.0, 0.0, (0,), 0, 0)] if k == 0 else opts_single(mtp, (0,), [(False, True)], 1)
                    layouts = []
                    if lay == "single":
                        oc = opts_single(csa, hs_csa, [(False, False), (True, False)], csa["n"])
                        oh = opts_single(hca, hs_hca, [(False, False), (False, True)], hca["n"])
                        if oc and oh: layouts.append((oc, oh))
                    else:
                        op = []
                        for h in hs_pair:
                            s, f = profs[h][lab]
                            for i_ in (False, True):
                                for kv_ in (False, True):
                                    for G in range(2, Gmax + 1):
                                        c = pair(s, csa, hca, G, h, b, pos, L, users, i_, kv_, imb_fixed)
                                        if c is not None: op.append((c, csa["n"] * G * s["P"], ("P", G, h, i_, kv_), csa["n"] * G, csa["n"] * G * h))
                        op = e8.pareto(op)
                        o1 = opts_single(hca, hs_hca, [(False, False), (False, True)], hca["n"] - csa["n"])
                        if op and o1: layouts.append((op, o1))
                    if not mt: continue
                    head_w = profs[4][lab][0]["P"]
                    for A_, B_ in layouts:
                        for oa in A_:
                            for ob in B_:
                                for om in mt:
                                    c = max(oa[0], ob[0], om[0])
                                    T = max(mm * c, c + lpS * tau)
                                    W = (oa[1] + ob[1] + om[1] + head_w) * sp
                                    npk = oa[3] + ob[3] + om[3] + 1
                                    eff = m.DERATE * mm * b * tok / T / W
                                    spd = tok / (L / lpS * T)
                                    mx = max(mx, spd)
                                    for t in tiers:
                                        if spd >= t and (t not in res or eff > res[t][0]):
                                            res[t] = (eff, dict(lab=lab, k=k, m=mm, b=b, A=oa[2], B=ob[2], Mt=om[2], npk=npk,
                                                                stacks=oa[4] + ob[4] + om[4] + 4, spd=spd, T=T,
                                                                c=(oa[0], ob[0], om[0]), W=W, users=users))
    res["max"] = mx
    return res


def detail(d):
    return (f"{d['lab']} k{d['k']} m{d['m']} b{d['b']} A={d['A']} B={d['B']} MTP={d['Mt']} pkgs {d['npk']} stacks {d['stacks']} "
            f"users {d['users']:,} {d['spd']:,.0f} tok/s/user T {d['T']*1e6:.1f} us c(us)=" + "/".join(f"{x*1e6:.1f}" for x in d['c'])
            + f" avg slot {d['W']/d['npk']:.0f} W")
