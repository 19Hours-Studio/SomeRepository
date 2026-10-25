"""Calibrate the GPU model against a measured DeepSeek-V4-Pro point (not R1):
InferenceX GB300 NVL72, FP4, 8K in / 1K out, disaggregated P/D, MTP: ~11.2-12k tok/s/GPU at ~50 tok/s/user
(PyTorch/SGLang blog, June 2026; LMSYS 'exceeds 12K'). Throughput counted both as total (in+out) and output-only.
Prefill GPUs are charged at the model's compute-bound prefill rate. Usage: python3 calib7.py > calib7.txt"""
import model7 as q, model5 as m
GB = dict(m.SYS["GB300"], imb=q.IMB_G, s=1.0)
ISL, OSL = 8192, 1024
pre_t = m.comp_time(m.V4, GB, 1, 61, ISL // 2)          # s per prompt token per GPU (compute-bound, eta 0.6)
print(f"model prefill: {1/pre_t:,.0f} prompt tok/s per GB300 GPU")
for p in (0.6, 0.7, 0.8):
    for tau in (10e-6, 30e-6, 60e-6):
        e = m.envelope(lambda k: m.gpu_points(GB, tau, ISL + OSL // 2, k, p), (50,), ks=range(4))
        dec = e[50][0] * GB["P"] / m.DERATE                # output tok/s per decode GPU (undo the 0.85 derate)
        out = 1 / (1 / dec + (ISL / OSL) * pre_t)            # output tok/s per GPU, prefill GPUs included
        print(f"p {p} tau {tau*1e6:3.0f} us: decode-only {dec:7,.0f} out tok/s/GPU; with prefill {out:6,.0f} out, "
              f"{out*(1+ISL/OSL):7,.0f} total | measured 12k = {12e3/(out*(1+ISL/OSL)):.2f} of model if total, "
              f"{12e3/out:.2f} if output-only (k={e[50][1]})")
