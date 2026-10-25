"""Round-7 additions on top of round6/model5.py (imported unchanged).

  * One voltage/frequency law for every system (alpha-power law, V0 = 0.75 V, Vt = 0.30 V, alpha = 1.3):
    f/f0 = ((V-Vt)/(V0-Vt))**alpha * V0/V ; dynamic energy per op ~ (V/V0)**2 ; leakage power ~ V/V0.
    Vendor Max-P / Max-Q points are kept exactly as before (Max-Q compute x0.92, 29% compute-power saving,
    rack sees 0.83 of chip saving); deeper points (0.65, 0.60, 0.55 V) come from the law, for all systems.
  * Fixed per-layer latency splits into a clock-independent part (collectives, 7 us) and a part that scales
    with 1/f (3 us at f0): tau(f) = 7 + 3/f us. Applied to all systems.
  * Pipeline SRAM bandwidth can be clocked down with the compute clock (W-tier power ~ bandwidth used).
  * Groq LP30 has no FP4 (SemiAnalysis/More Than Moore): expert weights held at FP8 in the AFD baseline.
"""
import math, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "round6"))
import model5 as m

m.OPT["dense_rep"] = True
V0, VT, ALPHA = 0.75, 0.30, 1.3
VMENU = (0.75, 0.65, 0.60, 0.55)
T = (200, 500, 1000, 1500, 2000)
C128, C1M = 131072, 1048576
IMB_G, IMB_C = 1.07, 1.12


def fr(V): return ((V - VT) / (V0 - VT)) ** ALPHA * V0 / V
def er(V): return (V / V0) ** 2
def tau_f(f): return (7 + 3 / f) * 1e-6


SHARE = 1.146   # slot saving per W of chip saving, the SAME for every system (conversion/cooling scale with load).
                # Round 6 used 0.83 for Rubin (from 2.3->1.8 kW chip vs 220->190 kW rack) but 1.146 for Continuum.


def profiles(base, comp_w, leak_w, other_w, conv=0.146, fixed=0.0, wt_w=0.0, vendor_maxq=True, rack_share=None):
    """Return list of (label, sys-dict, f) operating profiles, one law for all systems.
    chip(V) = comp_w*f*e + leak_w*V/V0 + wt_w*ws + other_w ; slot(V) = slot(V0) - SHARE*(chip(V0) - chip(V)).
    For Continuum slot(V0) = chip(V0)*(1+conv) + fixed; for GPUs slot(V0) is the vendor rack figure per slot.
    Vendor Max-Q (compute x0.92) is kept for GPUs as published (190 kW rack) and mirrored for Continuum."""
    out = []
    chip0 = comp_w + leak_w + wt_w + other_w
    P0 = base["P"] if rack_share is not None else chip0 * (1 + conv) + fixed
    for V in VMENU:
        f, e = fr(V), er(V)
        for wtrack in ((False, True) if wt_w else (False,)):
            ws = f if wtrack else 1.0
            chip = comp_w * f * e + leak_w * V / V0 + wt_w * ws + other_w
            P = P0 - SHARE * (chip0 - chip)
            s = dict(base, F4=base["F4"] * f, F8=base["F8"] * f, P=P)
            if wtrack and "srambw" in s: s["srambw"] = base["srambw"] * ws
            out.append((f"{V:.2f}V{' wt' if wtrack else ''}", s, f))
    if vendor_maxq:
        f = 0.92
        P = base["P_maxq"] if rack_share is not None else P0 - 0.83 * (0.29 * comp_w + 0.10 * leak_w)
        out.append(("MaxQ", dict(base, F4=base["F4"] * f, F8=base["F8"] * f, P=P), f))
    return out


# ---- systems -----------------------------------------------------------------------------------------------
RUBIN = dict(m.SYS["Rubin"], s=1.43, imb=IMB_G, P=220e3 / 72, P_maxq=190e3 / 72)
RUBIN_PROF = lambda: profiles(RUBIN, comp_w=1720, leak_w=150, other_w=0, rack_share=0.83)


def ultra(P_slot, clock=1.0):
    """Rubin Ultra (provisional): 144 pkgs, 100 PF FP4 'with compression' (70 dense) at full clock."""
    return dict(N=144, F4=70e15 * clock, F8=35e15 * clock, hbm=768, hbmbw=32e12, link=3.6e12, P=P_slot,
                P_maxq=P_slot, s=1.43, imb=IMB_G)


# Continuum-6 (round 6): 2 C-dies, 4 W-tiers, 3 HBM4 16-high
C6 = dict(F4=32e15, F8=16e15, sram=9.2, srambw=256e12, hbm=144, hbmbw=7.5e12, link=1.8e12 * 0.85,
          P=2780, s=1.43, imb=IMB_C)
C6_PARTS = dict(comp_w=1320, leak_w=250, wt_w=307, other_w=240 + 144, fixed=100 + 60 + 30)
# Continuum-7: 4 C-dies (N2), 8 W-tiers, 4 HBM4 16-high (10 TB/s), 128 lanes/dir
C7 = dict(F4=64e15, F8=32e15, sram=18.4, srambw=512e12, hbm=192, hbmbw=10e12, link=3.6e12 * 0.85,
          P=0, s=1.43, imb=IMB_C)
C7_PARTS = dict(comp_w=2640, leak_w=500, wt_w=614, other_w=320 + 288, fixed=100 + 100 + 30)


def cont_prof(base, parts, vendor_maxq=True):
    p0 = (parts["comp_w"] + parts["leak_w"] + parts["wt_w"] + parts["other_w"]) * 1.146 + parts["fixed"]
    b = dict(base, P=p0)
    return profiles(b, parts["comp_w"], parts["leak_w"], parts["other_w"], fixed=parts["fixed"],
                    wt_w=parts["wt_w"], vendor_maxq=vendor_maxq)


# ---- envelopes -----------------------------------------------------------------------------------------------
def best_over(cands):
    """cands: list of (label, envelope-dict). Returns {tier: (tok/s/W, label, point)}"""
    out = {}
    for lab, e in cands:
        for t in T:
            if t in e and (t not in out or e[t][0] > out[t][0]):
                out[t] = (e[t][0], lab, e[t])
        out["max"] = max(out.get("max", 0), e.get("max", 0))
    return out


def gpu_env(profs, ctx=C128, p=0.8, M=m.V4, tau_scale=True):
    c = []
    for lab, s, f in profs:
        tau = tau_f(f) if tau_scale else 10e-6
        c.append((lab, m.envelope(lambda k: m.gpu_points(s, tau, ctx, k, p, M=M), T)))
    return best_over(c)


def pipe_env(profs, ctx=C128, p=0.8, M=m.V4, gs=(3, 4, 6), tau_scale=True):
    c = []
    for lab, s, f in profs:
        tau = tau_f(f) if tau_scale else 10e-6
        for g in gs:
            c.append((f"{lab} g{g}", m.envelope(lambda k: m.pipe_points(s, tau, ctx, k, p, M=M, gmin=g), T)))
    return best_over(c)


def afd_env(ctx=C128, p=0.8, fp8_weights=True):
    if fp8_weights:
        old = m.b_exp
        m.b_exp = lambda M: M["exp"] * 8.25 / 8
    try:
        e = m.envelope(lambda k: m.afd_points(8e-6, ctx, k, p, r=dict(RUBIN)), T)
    finally:
        if fp8_weights: m.b_exp = old
    return best_over([("afd", e)])


def ratio(a, b, ts=T):
    return " ".join(f"{a[t][0]/b[t][0]:6.2f}" if t in a and t in b else f"{'cap' if t in a else '--':>6}" for t in ts)


def vals(a, ts=T):
    return " ".join(f"{a[t][0]:6.1f}" if t in a else f"{'--':>6}" for t in ts) + f"   max {a.get('max', 0):5.0f}"


# Continuum-7 primary (round 7): C7 with the over-provisioned non-compute trimmed
#  * 64 x 224G lanes per direction instead of 128 (link time at the operating points is 2.7-5.4 us of a 6-12.5 us
#    microbatch at 128 lanes, so 64 lanes still never bind; saves 144 W)
#  * one host CPU per 8 packages (50 W/slot) and one 800G NIC per package (30 W) for KV ingress from GPU prefill
#    (~0.4 Tb/s per package at the >=200 point: 29k requests/s x 0.65 GB KV at 128K over 373 packages)
C7T = dict(C7, link=1.8e12 * 0.85)
C7T_PARTS = dict(C7_PARTS, other_w=320 + 144, fixed=50 + 30 + 30)
