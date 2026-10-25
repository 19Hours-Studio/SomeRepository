"""GB300 calibration vs InferenceX DSv4-Pro FP4 8K/1K (compare page, 'per chip', read as input+output -> /9 = output).
Blend: every output token also costs 8 prefill tokens (8K in / 1K out) on the same GPUs, compute-bound prefill.
Usage: python3 calib4.py > calib4.txt"""
import model4 as m
s = m.SYS["GB300"]
pre = 1 / ((m.lin_flops(61) / s["F4"] + m.attn_flops(4096) / s["F8"]) / m.ETA)   # prompt tok/s per GPU
print(f"GB300 prefill model: {pre:,.0f} prompt tok/s/GPU -> {pre/8:,.0f} output-equivalent tok/s/GPU at 8:1")
meas = {55: 110889 / 9, 81: 69409 / 9, 106: 32541 / 9}
print("measured output tok/s/GPU (total/9):", {k: round(v) for k, v in meas.items()})
for ks, lab in (((1,), "k=1"), (range(4), "k<=3")):
    for tau in (8, 20, 40, 70, 100, 150):
        cells = []
        for tier, mv in meas.items():
            e = m.envelope(lambda k: m.gpu_points(s, tau * 1e-6, 8192, k, 0.8), (tier,), ks=ks)
            if tier not in e: cells.append(f"{tier}: --"); continue
            dec = e[tier][0] * s["P"]
            bl = 1 / (1 / dec + 8 / pre)
            cells.append(f"{tier}: {bl:7,.0f} ({bl/mv:4.2f}x)")
        print(f"{lab:<5} tau {tau:>3}us  " + "   ".join(cells))
