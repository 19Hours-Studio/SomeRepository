"""Round 9 (refine_continuum_d/round2): Continuum-9 = Continuum-8 + expert-parallel stage split + W-tier bandwidth
provisioned to need + fewer link lanes. Imports model8 (copied unchanged from round1) and through it model7/model5.

New here (Continuum only; the GPU side is model8 unchanged):
  * split="ep": inside a stage of g packages each package owns 384/g whole experts and b/g users' attention.
    Bytes received per package per position: (hid/g) stage hand-off + 3*hid*D(g)*(g-1)/g^2 dispatch (1 B/elt) and
    BF16 combine (2 B/elt), D(g) = g(1-(1-1/g)^6) distinct packages hit by a token's 6 experts; x imbalance.
    split="tp" is round 8 (expert intermediate dim split, every package sees every position).
    EP imbalance also scales the weight-read time (hot packages read more experts).
  * W-tier provisioned bandwidth omega x 512 TB/s at f0. Provisioned W-tier power = S_static (not scaled by clock,
    retention/periphery leakage, base 100 W) + (614 - S_static) * omega (dynamic, scales with clock as before).
  * link lanes: 64 / 48 / 32 per direction (1.8 / 1.35 / 0.9 TB/s raw, 144 / 108 / 72 W).
  * gmax raised to 20 (deployment unit grows; reported).
  * spares: hot spares at full slot power (factor 1/(1+sp)) or cold spares (idle 5% of slot power).
"""
import math
import model8 as e8
q, m = e8.q, e8.m
M = e8.M
S_STATIC = 100.0
IMB_EP = None      # None -> replica rule (1.07 if room else 1.12); else fixed EP imbalance


def design_profiles(h, omega=1.0, lanes=64, labels=None, s_static=None, wt_dyn=1.0):
    s_static = S_STATIC if s_static is None else s_static
    base = dict(e8.C8, srambw=512e12 * omega, link=1.8e12 * 0.85 * lanes / 64)
    parts = dict(e8.C8_PARTS, wt_w=(614 - s_static) * omega * wt_dyn, other_w=e8.STACK_W * h + 144 * lanes / 64 + s_static)
    pr = q.cont_prof(base, parts)
    return {l: (s, f) for l, s, f in pr if labels is None or l in labels}


def D(g, k=6): return g * (1 - (1 - 1 / g) ** k)


def stage(s, typ, g, h, b, pos, L, users, idx_sram, kv_sram, split="ep", two_phase=False, imb_fixed=None):
    exp_b = M["n_exp"] * m.b_exp(M) / g
    dense_b = m.b_dense(M)
    sram_cap = e8.FILL * s["sram"] * 1e9
    in_sram = exp_b + dense_b
    hbm_store = kv_rd_sram = kv_rd_hbm = 0.0
    if kv_sram:
        in_sram += users * typ["kvs"] / g; kv_rd_sram += b * typ["kvr"] / g
    else:
        hbm_store += users * typ["kvs"] / g; kv_rd_hbm += b * typ["kvr"] / g
    if typ["idxs"]:
        if idx_sram:
            in_sram += users * typ["idxs"] / g; kv_rd_sram += b * typ["idxr"] / g
        else:
            hbm_store += users * typ["idxs"] / g; kv_rd_hbm += b * typ["idxr"] / g
    if in_sram > sram_cap or hbm_store > 0.9 * h * e8.STACK_GB * 1e9: return None
    if kv_rd_hbm > 0 and h == 0: return None
    room = sram_cap - in_sram >= e8.REP * exp_b
    imb = imb_fixed or (q.IMB_G if room else q.IMB_C)
    if split == "ep" and IMB_EP: imb = max(imb, IMB_EP)
    lin = 2 * (M["topk"] * M["exp"] + M["dense"]) + 2 * M["head"] / L
    cL = b * pos * imb * lin / (s["F4"] * s["s"]) / m.ETA / g
    cA = b * pos * imb * (typ["f8"] / s["F8"] + typ["f4"] / s["F4"]) / m.ETA / g
    if split == "ep":
        sw = (imb * m.touched(M, b * pos) * m.b_exp(M) / g + dense_b) / s["srambw"]
        lnk = imb * b * pos / g * M["hid"] * (1 + 3 * D(g) * (g - 1) / g) / s["link"] if g > 1 else b * pos * M["hid"] / s["link"]
    else:
        sw = (m.touched(M, b * pos) * m.b_exp(M) / g + dense_b) / s["srambw"]
        lnk = b * pos * (M["hid"] * (g - 1) / g + 2 * M["hid"]) / s["link"]
    sk = kv_rd_sram / s["srambw"]
    hk = kv_rd_hbm / (h * e8.STACK_BW) if h else 0.0
    if two_phase:
        return max(max(sw, cL) + max(sk + hk, cA), lnk)
    return max(sw + sk, hk, cL + cA, lnk)


def env(ctx, p=0.8, labels=("0.55V wt", "0.60V wt"), omega=1.0, lanes=64, split="ep", hs_csa=(2, 3, 4), hs_hca=(0, 2, 4),
        idx_opts=(False, True), hca_sram_opts=(False, True), gmax=20, two_phase=False, imb_fixed=None, tiers=q.T,
        ks=range(7), tau_fn=None, s_static=None, spares=0.0, spare_mode="hot", parts_over=None, base_over=None, wt_dyn=1.0):
    """best tok/s/W per tier for one Continuum-9 design point. parts_over/base_over: dict of multiplicative
    overrides used by sensitivities, e.g. {'comp_w': 1.25}."""
    tau_fn = tau_fn or q.tau_f
    csa, hca, mtp = e8.layer_types(ctx)
    profs = {}
    for h in set(hs_csa) | set(hs_hca) | {0, 4}:
        old_b, old_p = dict(e8.C8), dict(e8.C8_PARTS)
        for k_, v in (base_over or {}).items(): e8.C8[k_] = old_b[k_] * v
        for k_, v in (parts_over or {}).items(): e8.C8_PARTS[k_] = old_p[k_] * v
        try: profs[h] = design_profiles(h, omega, lanes, labels, s_static, wt_dyn)
        finally: e8.C8.clear(); e8.C8.update(old_b); e8.C8_PARTS.clear(); e8.C8_PARTS.update(old_p)
    sp = (1 + spares) if spare_mode == "hot" else (1 + 0.05 * spares)
    res, mx = {}, 0
    for lab in labels:
        tau = tau_fn(profs[0][lab][1])
        for k in ks:
            pos, tok, L = m.spec(M, k, p)
            for mm in m.MS:
                for b in m.BGRID:
                    users = mm * b * L
                    sets = []
                    for typ, hs, opts in ((csa, hs_csa, [(i, False) for i in idx_opts]),
                                          (hca, hs_hca, [(False, x) for x in hca_sram_opts]),
                                          (mtp, (0,), [(False, True)])):
                        o = []
                        if typ is mtp and k == 0:
                            sets.append([(0.0, 0.0, (0, 0, 0, 0), 0, 0)]); continue
                        for h in hs:
                            s, f = profs[h][lab]
                            for idx_s, kv_s in opts:
                                for g in range(1, gmax + 1):
                                    c = stage(s, typ, g, h, b, pos, L, users, idx_s, kv_s, split, two_phase, imb_fixed)
                                    if c is not None:
                                        o.append((c, typ["n"] * g * s["P"], (g, h, idx_s, kv_s), typ["n"] * g, typ["n"] * g * h))
                        sets.append(e8.pareto(o))
                    if not all(sets): continue
                    head_w = profs[4][lab][0]["P"]
                    for oc in sets[0]:
                        for oh in sets[1]:
                            for om in sets[2]:
                                c = max(oc[0], oh[0], om[0])
                                T = max(mm * c, c + tau)
                                W = (oc[1] + oh[1] + om[1] + head_w) * sp
                                npk = oc[3] + oh[3] + om[3] + 1
                                eff = m.DERATE * mm * b * tok / T / W
                                spd = tok / (L * T)
                                mx = max(mx, spd)
                                for t in tiers:
                                    if spd >= t and (t not in res or eff > res[t][0]):
                                        res[t] = (eff, dict(lab=lab, k=k, m=mm, b=b, C=oc[2], H=oh[2], Mt=om[2], npk=npk,
                                                            stacks=oc[4] + oh[4] + om[4] + 4, spd=spd, T=T,
                                                            c=(oc[0], oh[0], om[0]), W=W, users=users,
                                                            omega=omega, lanes=lanes))
    res["max"] = mx
    return res


BASE = dict(omega=0.7, lanes=64, gmax=14)   # Continuum-9 base design (sweep9/sweep9b)
DESIGNS = [(o, l) for o in (1.0, 0.75, 0.6, 0.5, 0.4) for l in (64, 48, 32)]


def best_design(ctx, designs=DESIGNS, **kw):
    """one silicon design must serve all tiers: return (best per-tier envelope over designs, per-design envelopes)"""
    envs = {d: env(ctx, omega=d[0], lanes=d[1], **kw) for d in designs}
    return envs


def pick(envs, d):
    return envs[d]


def detail(d):
    return (f"{d['lab']} k{d['k']} m{d['m']} b{d['b']} CSA(g,h,idx,kv)={d['C']} HCA={d['H']} MTP={d['Mt']} pkgs {d['npk']} "
            f"stacks {d['stacks']} users {d['users']:,} {d['spd']:,.0f} tok/s/user T {d['T']*1e6:.1f} us c(us)="
            + "/".join(f"{x*1e6:.1f}" for x in d['c']) + f" avg slot {d['W']/d['npk']:.0f} W")
