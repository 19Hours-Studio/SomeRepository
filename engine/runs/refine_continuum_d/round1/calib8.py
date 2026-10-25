"""Decode-only calibration of the GPU model (critic point D).
Measured decode-pool points (DeepSeek-R1/V3, 2K-token inputs, GB200 NVL72, SGLang PD + wide EP):
  LMSYS Part II (Sep 2025): 13,386 output tok/s per decode GPU (FP8 attention, NVFP4 MoE)
  LMSYS Part I  (Jun 2025):  7,583 (FP8 MoE, BF16 attn)          vLLM WideEP (Feb 2026): 10.1k decode TPGS (2K/2K, 8 GPUs)
Model: model5.gpu_points with GB200 specs, R1 config, no MTP, max throughput over batch (no speed floor), DERATE removed.
Usage: python3 calib8.py > calib8.txt"""
import model8 as e8
q, m = e8.q, e8.m
GB200 = dict(N=72, F4=10e15, F8=5e15, hbm=186, hbmbw=8e12, link=0.9e12, P=1.0, s=1.0, imb=q.IMB_G)
for N, ctx, lab, meas in ((72, 2100, "LMSYS II, EP72-class, NVFP4 MoE", 13386), (48, 2100, "LMSYS II, EP48", 13386),
                          (8, 3000, "vLLM 2K/2K, 8 decode GPUs", 10100)):
    for tau in (10e-6, 30e-6):
        s = dict(GB200, N=N)
        pts = m.gpu_points(s, tau, ctx, 0, 0.8, M=m.R1)
        best = max(pts, key=lambda x: x[1])
        out = best[1] / m.DERATE          # output tok/s per GPU (P=1)
        print(f"{lab:<34} tau {tau*1e6:3.0f} us: model {out:8,.0f} tok/s/GPU at {best[0]:5.0f} tok/s/user, B={best[2]}"
              f" (t,m)={best[3]} -> measured/model = {meas/out:.2f}")
# FP8-MoE variant of Part I (weights 8.25 bits): compare 7,583
old = m.b_exp; m.b_exp = lambda M: M["exp"] * 8.25 / 8
s = dict(GB200, F4=5e15)  # FP8 MoE: linear at FP8 rate
pts = m.gpu_points(s, 10e-6, 2100, 0, 0.8, M=m.R1); b = max(pts, key=lambda x: x[1]); m.b_exp = old
print(f"{'LMSYS I, FP8 MoE, EP72':<34} tau  10 us: model {b[1]/m.DERATE:8,.0f} -> measured/model = {7583/(b[1]/m.DERATE):.2f}")
