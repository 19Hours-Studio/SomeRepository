"""Idea 1 budget: reversible KVzip-style eviction with CPU backing, recall per TURN vs per STEP.
Exact config arithmetic; hardware numbers are datasheet/literature (see NOTES)."""
KIB = 1024
# Llama-3.1-8B: 32 layers, 8 KV heads, head_dim 128 -> FP8 K+V = 32*8*128*2*1 B
bpt = 32 * 8 * 128 * 2 * 1                  # 65536 B/token (FP8)
W = 16.06e9                                  # BF16 weights
HBM, HBM_BW = 80e9, 3.35e12                  # H100 SXM
reserve = 8e9                                # activations / CUDA graphs / fragmentation (assumption)
PCIE = 25e9                                  # effective H2D, PCIe4 x16-class (FACT 8); H100 PCIe5 ~2x
GPU_HR = 2.5                                 # $/h H100 (assumption, market range 2-3.5)
T_OUT = 343                                  # mean output tokens/turn, Mooncake conversation trace (computed)
rho, r_turn, meta = 0.30, 0.10, 0.7 / 64 * 2 / 2   # resident, recalled per turn, min/max-key page summaries (64-tok pages, K only)

def decode(L, frac_resident, frac_read, extra_pcie_per_step_per_user=0.0):
    per_user = frac_resident * L * bpt
    B = int((HBM - W - reserve) // per_user)
    t_hbm = (W + B * frac_read * L * bpt) / HBM_BW
    t_pcie = B * extra_pcie_per_step_per_user / PCIE
    t = max(t_hbm, t_pcie)                   # transfers overlap compute; the slower one binds
    return B, t, B / t, t_pcie / t_hbm

print("L      design                          B   step_ms  tok/s   pcie/hbm  $/1M out tok   x vs FP8-full")
for L in (32_000, 128_000):
    base = decode(L, 1.0, 1.0)
    rows = {
        "FP8 full (vLLM flag)": base,
        "KVzip 30% permanent": decode(L, rho, rho),
        # per-step Quest recall of 10% of context every decode step (killed design)
        "per-STEP recall 10%": decode(L, rho + r_turn + meta, rho + r_turn, r_turn * L * bpt),
        # per-TURN recall: 10% of context fetched once per turn, amortised over T_OUT steps
        "per-TURN recall 10%": decode(L, rho + r_turn + meta, rho + r_turn, r_turn * L * bpt / T_OUT),
        "per-TURN 10% + 0.5%/step valve": decode(L, rho + r_turn + 0.005 * 8 + meta, rho + r_turn,
                                                r_turn * L * bpt / T_OUT + 0.005 * L * bpt),
    }
    for k, (B, t, tps, pr) in rows.items():
        usd = GPU_HR / 3600 / tps * 1e6
        print(f"{L//1000:>3}K  {k:31s} {B:3d}  {t*1e3:6.1f}  {tps:6.0f}  {pr:7.2f}   {usd:7.3f}       {tps/base[2]:.2f}")
# turn-start latency: reload of resident+recall set for a session coming back from CPU (multi-turn)
for L in (32_000, 128_000):
    full = L * bpt / PCIE; ours = (rho + r_turn) * L * bpt / PCIE
    print(f"TTFT reload from CPU at {L//1000}K: full FP8 {full*1e3:.0f} ms vs resident+recall {ours*1e3:.0f} ms")
# CPU DRAM capacity check: sessions held in host RAM (full FP8 copy) on a 2 TB host, 8 GPUs
for L in (32_000, 128_000):
    print(f"host 2TB / {L//1000}K-token FP8 session = {2e12/(L*bpt):.0f} sessions per node")

# ---- Round 3: include prefill + residency-scoring cost per request (GPU-seconds/request) ----
EFF = 4.0e14                       # effective prefill FLOP/s on H100 (~40% of 989 dense BF16; assumption)
NEW = 0.63 * 12035                 # uncached tokens/request: Mooncake conv trace, infinite cache (computed)
def prefill_s(L, n):               # n new tokens appended at the end of an L-token context
    p0 = L - n
    att = 4 * 32 * 4096 * (n * p0 + n * n / 2)
    return (n * 16e9 + att) / EFF
print("\nGPU-s/request incl. prefill (L=32K):  s = scoring cost as multiple of prefill of new tokens")
L = 32_000
pf = prefill_s(L, NEW)
B0, t0, _, _ = decode(L, 1.0, 1.0)
base = pf + T_OUT * t0 / B0
print(f"FP8 full: prefill {pf:.3f}s + decode {T_OUT*t0/B0:.3f}s = {base:.3f}s  ${GPU_HR/3600*base*1000:.3f}/1k req")
B1, t1, _, _ = decode(L, rho + r_turn + meta, rho + r_turn, r_turn * L * bpt / T_OUT)
for s, name in [(2.0, "KVzip full reconstruction (~2x?)"), (1.0, "KVzip ~1x"), (0.1, "observation-window score"), (0.0, "head-level static score")]:
    tot = pf * (1 + s) + T_OUT * t1 / B1
    print(f"per-TURN, {name:34s}: {tot:.3f}s  cost ratio vs FP8 full {tot/base:.2f}")
# break-even scoring overhead
s_be = (base - pf - T_OUT * t1 / B1) / pf
print(f"break-even scoring overhead = {s_be:.2f} x prefill")
# decode-heavy regime: new tokens per turn small (chat follow-ups with cached prefix, e.g. 500 new tok)
for n in (500, 2000):
    pf2 = prefill_s(L, n); b2 = pf2 + T_OUT * t0 / B0
    for s in (0.1, 1.0):
        o2 = pf2 * (1 + s) + T_OUT * t1 / B1
        print(f"new={n} tok/turn, s={s}: FP8 {b2:.3f}s vs ours {o2:.3f}s -> ratio {o2/b2:.2f}")
# PCIe valve headroom and short-output break-even
B, t, _, _ = decode(L, rho + r_turn + meta, rho + r_turn)
vmax = (PCIE * t - B * r_turn * L * bpt / T_OUT) / (B * L * bpt)
print(f"valve max fraction/step within PCIe = {vmax*100:.2f}%  ; per-turn recall stalls if T_OUT < {B*r_turn*L*bpt/(PCIE*t):.0f} tokens")
