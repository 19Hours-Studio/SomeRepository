"""NVFP4 KV cache on all systems (C8 vs Rubin trimmed 150 W). Usage: python3 fp4kv8.py ctx > fp4kv8_<ctx>.txt"""
import sys, model8 as e8
q, m = e8.q, e8.m
m.OPT["kv_fp4"] = True
ctx = int(sys.argv[1])
A = e8.c8_env(e8.C8, e8.C8_PARTS, ctx, labels=("0.55V wt", "0.60V wt", "0.65V wt", "0.55V", "0.60V"))
R = e8.gpu_env(e8.rubin_prof(150), ctx)
print(f"{ctx//1024}K NVFP4 KV on both: C8 {e8.fmt(A)} | Rubin {e8.fmt(R)} | ratio {e8.rat(A, R)}")
