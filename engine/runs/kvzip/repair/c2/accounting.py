# Bit accounting, gate thresholds, requests served per GPU, runtime overhead. Exact arithmetic.
import numpy as np
rel = {2: 0.50, 3: 0.215, 4: 0.10}          # rotated min-max rel RMS, measured in sim_dither*.py (matches FACT 3 ~0.097 for 4b)
safety = 1.5                                  # bound measured within ~20% (sim_round3 b); 1.5x margin
thr = {b: rel[4] / (rel[b] * safety) for b in (2, 3)}
print("gate E_h thresholds:", {b: round(t, 3) for b, t in thr.items()},
      "=> N_eff_q >=", {b: round(1 / t**2, 1) for b, t in thr.items()})
OV = 32 / 128                                 # FP16 scale+zero (or scale+channel-mean) per 128 values = 0.25 bit
ctx = 32768; fp16_tok = 4 + 128               # 4 sinks + 128 recent kept FP16
side = fp16_tok * 16 / ctx                    # bits/value amortised
print(f"FP16 sinks+recent at {ctx}: {side:.3f} bit/value")
scen = {"S_cons": (0.5, 0.2, 0.3), "S_mid": (0.3, 0.2, 0.5), "S_opt": (0.2, 0.1, 0.7)}  # share of KV heads: E_h>thr3, thr2<E_h<=thr3, E_h<=thr2
def idea1(f4, f3, f2):   # keys always K4; values gated 4/3/2 with dither
    K = 4 + OV; V = f4 * (4 + OV) + f3 * (3 + OV) + f2 * (2 + OV); return (K + V) / 2 + side
def idea2(f4, f3, f2):   # joint K/V: K4V4 / K4V3 / K3V2, block-centred, no 1-bit, no K2
    return f4 * (4 + OV) + f3 * (3.5 + OV) + f2 * (2.5 + OV) + side
base = {"FP16": 16, "FP8 (vLLM)": 8 + 0.0, "NVFP4 KV (FP8 scale/16)": 4.5, "uniform K4V4 g128": 4 + OV + side,
        "KVTuner Llama 3.25b(+0.25 meta)": 3.5, "KVTuner Qwen 4.0b(+0.25)": 4.25, "Kitty ~2-bit (8x claimed)": 2.0}
rows = {**base}
for s, f in scen.items(): rows[f"Idea1 {s}"] = idea1(*f); rows[f"Idea2 {s}"] = idea2(*f)
# Requests served: Llama-3.1-8B on H100-80GB, 32k context, memory-bound decode
HBM, W, BW = 80e9, 16.06e9, 3.35e12
kv_vals_tok = 32 * 8 * 128 * 2                # values per token (K+V)
free = HBM - W - 6e9                          # 6 GB activations/workspace
print(f"\n{'scheme':36s} {'bits':>5} {'xFP16':>6} {'max seqs':>8} {'tok/s@max':>9} {'GB KV/seq':>9}")
for k, b in rows.items():
    per_seq = kv_vals_tok * ctx * b / 8
    B = int(free // per_seq)
    step = (W + B * per_seq) / BW              # seconds per decode step (bandwidth bound)
    print(f"{k:36s} {b:5.2f} {16/b:6.2f} {B:8d} {B/step:9.0f} {per_seq/1e9:9.2f}")
# Runtime: dither regeneration (hash, ~6 int ops -> 32 random bits -> 4 x 8-bit dither) on V elements only
vals = 32 * 8 * 128 * ctx                     # V elements per seq per step
int_ops = vals * (6 / 4 + 1)                  # hash + subtract
INT32 = 33.5e12                                # H100 SXM non-tensor INT32 ops/s (NVIDIA whitepaper)
mem = vals * 2 * idea1(*scen["S_mid"]) / 8 / BW
print(f"\ndither ALU {int_ops/INT32*1e3:.3f} ms vs KV memory time {mem*1e3:.3f} ms per seq-step "
      f"({int_ops/INT32/mem*100:.0f}% if NOT overlapped; memory-bound kernel hides most)")
# Prefill: sum p^2 accumulation = 1 mul + 1 FMA per score, vs QK^T+PV = 4*d FLOP on tensor cores
d = 128; print(f"sum p^2 extra per score: 2 FLOP CUDA-core vs {4*d} tensor FLOP; vs ~5 softmax ops already -> +~40% softmax ALU,"
               " FA3 softmax ~ 1/4..1/3 of attn time if not overlapped -> <=+10% attn; restricted to last 1k prompt queries: ~0")
