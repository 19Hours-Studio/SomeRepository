#!/usr/bin/env python3
"""Continuum vs. 2026 accelerators: decode roofline + energy + capacity model.

Step time per decode step (one token for each of B concurrent users):
  t = max(t_mem, t_compute) + layers * t_floor
where t_floor is a per-layer latency floor (sync, all-to-all, kernel overhead).
Everything marked ASSUME is a design assumption or estimate, not a measurement.
"""
import math

# ---------------- models (public architecture parameters) ----------------
MODELS = {
    # DeepSeek-V3-class MoE + MLA: 671B total, 37B active, 61 layers, 256 routed experts top-8.
    "DSv3-671B": dict(total=671e9, active=37e9, dense=17e9, experts=256, topk=8, layers=61,
                      kv_vals_per_tok=(512 + 64) * 61,            # MLA latent + rope key, shared by heads
                      attn_flop_per_ctx=128 * (512 + 64 + 512) * 2 * 61),  # absorbed MLA, 128 heads
    # Llama-3.3-70B dense GQA: 80 layers, 8 KV heads x 128, 64 Q heads.
    "Llama-70B": dict(total=70.6e9, active=70.6e9, dense=70.6e9, experts=1, topk=1, layers=80,
                      kv_vals_per_tok=2 * 8 * 128 * 80,
                      attn_flop_per_ctx=64 * 128 * 2 * 2 * 80),
}
W_BITS = 4.5    # NVFP4/MXFP4 weights incl. block scales
KV_BITS = 4.5   # NVFP4 KV (given in task notes)

# ---------------- systems ----------------
# cap/bw per chip (package). w_in: where weights live. e_*: pJ/bit or pJ/FLOP (ASSUME, see notes).
# floor_us: per-layer latency floor (ASSUME; GPU calibrated to InferenceMAX GB200 curve falling off
# ~100-120 tok/s/user; dataflow calibrated to Cerebras ~2,300-2,700 tok/s/user).
HBM_PJ = 4.0     # ASSUME HBM4 incl. PHY+controller (HBM3 ~5-7, HBM4E ~3.5-5 per secondary table)
SYS = {
    "Rubin NVL72": dict(n=72, sram=0.0, sram_bw=0, hbm=288, hbm_bw=22e12, stacks=8,
                        fp4=50e15, fp8=17.5e15, watt=2300 * 1.25, floor_us=100, w_in="hbm",
                        e_w=HBM_PJ, area=1600),
    "Rubin NVL72 (opt. SW)": dict(n=72, sram=0.0, sram_bw=0, hbm=288, hbm_bw=22e12, stacks=8,
                        fp4=50e15, fp8=17.5e15, watt=2300 * 1.25, floor_us=25, w_in="hbm",
                        e_w=HBM_PJ, area=1600),
    "Ironwood x64": dict(n=64, sram=0.0, sram_bw=0, hbm=192, hbm_bw=7.37e12, stacks=8,
                         fp4=4.6e15, fp8=4.6e15, watt=1000 * 1.25, floor_us=40, w_in="hbm",
                         e_w=HBM_PJ, area=1400),
    "Groq3 LPU": dict(n=None, sram=0.5, sram_bw=150e12, hbm=0, hbm_bw=0, stacks=0,
                      fp4=1.23e15, fp8=1.23e15, watt=600, floor_us=10, w_in="sram",
                      e_w=0.4, area=700),
    "Cerebras WSE-3": dict(n=None, sram=44, sram_bw=21e15, hbm=0, hbm_bw=0, stacks=0,
                           fp4=15e15, fp8=15e15, watt=23000, floor_us=10, w_in="sram",
                           e_w=0.4, area=46225),
    # Continuum package (this proposal, all ASSUME): 2 N2 compute dies (~800 mm2) each on a
    # 2-high stack of N5-class SRAM base dies -> 4 x ~2.6 GB = ~10 GB weights SRAM, 6 HBM4 for KV.
    "Continuum x64": dict(n=64, sram=10.0, sram_bw=128e12, hbm=216, hbm_bw=15e12, stacks=6,
                          fp4=30e15, fp8=15e15, watt=1800 * 1.25, floor_us=6, w_in="sram",
                          e_w=0.3, area=1600 + 3200 * 0.4),  # N5 SRAM area weighted 0.4 vs N2
}
E_FP4, E_FP8 = 0.05, 0.10   # pJ/FLOP chip-level ASSUME (B200 ~0.22 pJ/FLOP FP8 all-in at TDP)
E_LINK = 5.0                # pJ/bit scale-up SerDes+switch ASSUME
UTIL_C, UTIL_M = 0.6, 0.8
STATIC_FRAC = 0.3           # share of package power burned regardless of work ASSUME


def step(sysd, m, B, L, n):
    E, k = m["experts"], m["topk"]
    frac = 1 - (1 - k / E) ** B if E > 1 else 1.0
    w_bytes = (m["dense"] + (m["total"] - m["dense"]) * frac) * W_BITS / 8
    kv_bytes = B * L * m["kv_vals_per_tok"] * KV_BITS / 8
    lin = B * 2 * m["active"]
    att = B * L * m["attn_flop_per_ctx"]
    if sysd["w_in"] == "hbm":
        t_mem = (w_bytes + kv_bytes) / (n * sysd["hbm_bw"] * UTIL_M)
        e_mem = (w_bytes + kv_bytes) * 8 * HBM_PJ
    else:
        kv_bw = sysd["hbm_bw"] if sysd["hbm_bw"] else sysd["sram_bw"]
        kv_pj = HBM_PJ if sysd["hbm_bw"] else sysd["e_w"]
        t_mem = max(w_bytes / (n * sysd["sram_bw"] * UTIL_M), kv_bytes / (n * kv_bw * UTIL_M))
        e_mem = w_bytes * 8 * sysd["e_w"] + kv_bytes * 8 * kv_pj
    t_c = lin / (n * sysd["fp4"] * UTIL_C) + att / (n * sysd["fp8"] * UTIL_C)
    t = max(t_mem, t_c) + m["layers"] * sysd["floor_us"] * 1e-6
    # all-to-all activations: FP8 hidden (7168) x (k dispatch + k combine) per MoE layer per token
    comm_bits = B * 7168 * 2 * k * m["layers"] * 8 if E > 1 else B * 8192 * 2 * m["layers"] * 8
    e = (e_mem + lin * E_FP4 + att * E_FP8 + comm_bits * E_LINK) * 1e-12
    e += n * sysd["watt"] * STATIC_FRAC * t
    return t, e, w_bytes, kv_bytes


def chips_needed(sysd, m, B, L):
    if sysd["n"]:
        return sysd["n"]
    need = (m["total"] * W_BITS / 8 + B * L * m["kv_vals_per_tok"] * KV_BITS / 8) / 1e9
    return math.ceil(need / (sysd["sram"] * 0.9))


def fits(sysd, m, B, L, n):
    w = m["total"] * W_BITS / 8 / 1e9
    kv = B * L * m["kv_vals_per_tok"] * KV_BITS / 8 / 1e9
    if sysd["w_in"] == "hbm":
        return w + kv <= n * sysd["hbm"] * 0.9
    if sysd["hbm"]:
        return w <= n * sysd["sram"] * 0.9 and kv <= n * sysd["hbm"] * 0.9
    return w + kv <= n * sysd["sram"] * 0.9


def best_at(name, sysd, m, L, target):
    """Highest-throughput batch that still meets tok/s/user >= target."""
    best = None
    for B in [2 ** i for i in range(0, 15)]:
        n = chips_needed(sysd, m, B, L)
        if not fits(sysd, m, B, L, n):
            continue
        t, e, *_ = step(sysd, m, B, L, n)
        if 1 / t < target:
            continue
        kw = n * sysd["watt"] / 1e3
        r = dict(B=B, n=n, tps_user=1 / t, tps=B / t, tpj=B / e, tps_kw=B / t / kw,
                 tps_stack=(B / t) / max(n * sysd["stacks"], 1e-9),
                 tps_cm2=(B / t) / (n * sysd["area"] / 100))
        if best is None or r["tps_kw"] > best["tps_kw"]:  # power-normalized throughput
            best = r
    return best


if __name__ == "__main__":
    cases = [("DSv3-671B", 32768), ("DSv3-671B", 131072), ("Llama-70B", 8192)]
    for mname, L in cases:
        m = MODELS[mname]
        print(f"\n=== {mname}, context {L//1024}K, weights {W_BITS}b, KV {KV_BITS}b ===")
        kvu = L * m["kv_vals_per_tok"] * KV_BITS / 8 / 1e9
        print(f"weights {m['total']*W_BITS/8/1e9:.0f} GB; KV per user {kvu:.2f} GB; "
              f"attn intensity {m['attn_flop_per_ctx']/(m['kv_vals_per_tok']*KV_BITS/8):.0f} FLOP/B")
        for target in [50, 200, 1000]:
            print(f"  -- target >= {target} tok/s/user")
            print(f"  {'system':24s}{'chips':>6s}{'B':>6s}{'tok/s/u':>9s}{'tok/s':>10s}"
                  f"{'tok/J':>8s}{'tok/s/kW':>10s}{'tok/s/HBMstk':>13s}{'tok/s/cm2':>10s}")
            for name, s in SYS.items():
                r = best_at(name, s, m, L, target)
                if r is None:
                    print(f"  {name:24s}  infeasible")
                    continue
                stk = f"{r['tps_stack']:13.0f}" if s["stacks"] else f"{'n/a':>13s}"
                print(f"  {name:24s}{r['n']:6d}{r['B']:6d}{r['tps_user']:9.0f}{r['tps']:10.0f}"
                      f"{r['tpj']:8.2f}{r['tps_kw']:10.0f}{stk}{r['tps_cm2']:10.1f}")
