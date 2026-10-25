"""Decode roofline + energy model for Continuum vs 2026 reference chips.

Workload: Kimi-K2-class MoE (1.04T total, ~32B active, 61 layers, MLA kv 512+64,
64 heads, 384 routed experts top-8). Weights and KV stored at 4.5 bits/value
(NVFP4-style incl. block scales). All chips get the same storage format so the
comparison isolates the hardware.

FACT = vendor/spec figure (see NOTES); EST = our assumption, flagged.
"""
import math

GB = 1e9
BITS = 4.5
LAYERS, MOE_LAYERS = 61, 60
EXPERTS, TOPK = 384, 8
P_EXPERT = 3 * 7168 * 2048            # params per routed expert per layer
P_ALWAYS = 32e9 - TOPK * MOE_LAYERS * P_EXPERT   # attn + shared expert + embed (~11B)
P_TOTAL = P_ALWAYS + MOE_LAYERS * EXPERTS * P_EXPERT
KV_VALS_PER_TOK = LAYERS * (512 + 64)
HEADS = 64

# energy per op (EST, literature-typical; need Accelergy/silicon to confirm)
PJ_FLOP_FP4, PJ_FLOP_FP8 = 0.045, 0.08   # all-in datapath+local regfile, 3-4nm-class
PJ_BIT = {"hbm": 3.0, "stack": 0.8, "sram": 0.25, "gddr": 6.0}
# hbm: HBM3E/HBM4 incl. PHY ~2.5-3.5 (EST); stack: hybrid-bonded DRAM 0.66-0.88 (arXiv 2604.08044)
# sram: large distributed on-die SRAM incl. wire ~0.1-0.4 (EST)

chips = {
    # name: cap_fast_GB, bw_fast_TBs, tier_fast, cap_slow, bw_slow, tier_slow, PF_fp4, PF_fp8, tdp_kW, a2a_us
    "Rubin (GPU)":    dict(cf=288, bf=22, tf="hbm", cs=0, bs=0, ts="hbm", f4=50, f8=16, kw=1.8, lat=3.0),  # f8,kW EST
    "Ironwood (TPU)": dict(cf=192, bf=7.37, tf="hbm", cs=0, bs=0, ts="hbm", f4=4.6, f8=4.6, kw=1.0, lat=4.0),  # kW EST
    "WSE-3 (wafer)":  dict(cf=44, bf=21000, tf="sram", cs=0, bs=0, ts="hbm", f4=12.5, f8=12.5, kw=23, lat=8.0),  # inter-wafer
    "Groq LP30":      dict(cf=0.5, bf=150, tf="sram", cs=0, bs=0, ts="hbm", f4=1.2, f8=1.2, kw=0.5, lat=1.0),  # bf,kW EST
    "Continuum":      dict(cf=80, bf=64, tf="stack", cs=192, bs=10, ts="hbm", f4=32, f8=16, kw=2.2, lat=3.0),  # all EST
}

def unique_experts(b):
    return EXPERTS * (1 - (1 - TOPK / EXPERTS) ** b)

def step(chip, B, L, n_force=None, kv_bits=None):
    c = chips[chip]
    w_bytes_read = (P_ALWAYS + MOE_LAYERS * unique_experts(B) * P_EXPERT) * BITS / 8
    kv_bytes = B * L * KV_VALS_PER_TOK * BITS / 8
    w_total = P_TOTAL * BITS / 8
    cap_needed = (w_total + kv_bytes) * 1.1          # 10% activations/headroom
    cap_chip = c["cf"] + c["cs"]
    n = max(1, math.ceil(cap_needed / (cap_chip * GB)))
    if n_force:
        if n_force < n: return None
        n = n_force
    read = w_bytes_read + kv_bytes
    # tier placement: hot bytes go to fast tier up to its capacity, rest slow tier
    fast_cap = n * c["cf"] * GB
    if c["cs"] == 0:
        t_mem, b_fast, b_slow = read / (n * c["bf"] * 1e12), read, 0
    else:
        bf, bs = n * c["bf"] * 1e12, n * c["bs"] * 1e12
        b_fast = min(fast_cap / 1.1, read * bf / (bf + bs))
        b_slow = read - b_fast
        t_mem = max(b_fast / bf, b_slow / bs)
    flops_lin = B * 2 * 32e9                              # FP4 weights x FP8 act -> FP4 path
    flops_att = B * LAYERS * L * HEADS * (576 + 512) * 2  # MLA absorbed, FP8
    t_cmp = flops_lin / (n * c["f4"] * 1e15 * 0.7) + flops_att / (n * c["f8"] * 1e15 * 0.7)
    t_comm = 2 * MOE_LAYERS * c["lat"] * 1e-6 if n > 1 else 0
    t = max(t_mem, t_cmp) + t_comm
    e_mem = (b_fast * PJ_BIT[c["tf"]] + b_slow * PJ_BIT[c["ts"]]) * 8e-12
    e_cmp = flops_lin * PJ_FLOP_FP4 * 1e-12 + flops_att * PJ_FLOP_FP8 * 1e-12
    e_static = 0.25 * n * c["kw"] * 1e3 * t               # EST 25% TDP leakage/fabric/idle
    e = e_mem + e_cmp + e_static
    return dict(n=n, tps_user=1 / t, tps=B / t, tok_per_J=B / e, bound="mem" if t_mem > t_cmp else "cmp",
                tps_per_kW_tdp=B / t / (n * c["kw"]))

def slo_sweep(L, slos=(50, 100, 200, 400, 800, 1600)):
    print(f"\n=== best tok/s per kW(TDP) meeting tok/s/user SLO, context {L} (n,B free) ===")
    print(f"{'chip':16s}" + "".join(f"{s:>14d}" for s in slos))
    for ch in chips:
        row = []
        for slo in slos:
            best = None
            for n in sorted(set([int(x) for x in [1,2,3,4,5,6,8,10,12,16,20,24,32,48,64,96,128,192,256,384,512,768,1024,1536,2048,3072,4096]])):
                for B in [1,2,4,8,16,32,64,128,256,512,1024,2048,4096]:
                    r = step(ch, B, L, n_force=n)
                    if r and r["tps_user"] >= slo and (best is None or r["tps_per_kW_tdp"] > best[0]):
                        best = (r["tps_per_kW_tdp"], n, B, r["tok_per_J"])
            row.append(f"{best[0]:7.0f}({best[1]},{best[2]})" if best else f"{'-':>14s}")
        print(f"{ch:16s}" + "".join(f"{x:>14s}" for x in row))

def max_speed(L):
    print(f"\n=== max tok/s/user (B=1, any n) and its tok/s/kW, context {L} ===")
    for ch in chips:
        best = max((step(ch, 1, L, n_force=n) or {"tps_user": 0}, n) for n in [1,2,3,4,6,8,16,32,64,128,256,1024,2048,4096] for _ in [0]) if False else None
        rs = [(step(ch, 1, L, n_force=n), n) for n in [1,2,3,4,6,8,16,32,64,128,256,1024,2048,4096]]
        rs = [(r, n) for r, n in rs if r]
        r, n = max(rs, key=lambda x: x[0]["tps_user"])
        print(f"{ch:16s} {r['tps_user']:7.0f} tok/s/user on {n} chips ({r['bound']})")

if __name__ == "__main__":
    for L in (8192, 131072):
        slo_sweep(L)
        max_speed(L)
