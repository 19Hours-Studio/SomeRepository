"""Fraction of NVFP4 (E2M1, 16-value blocks, scale = blockmax/6) codes that quantize to zero, synthetic weights.
Usage: python3 zeros5.py > zeros5.txt"""
import numpy as np
rng = np.random.default_rng(1)
for name, x in (("gaussian", rng.standard_normal((1 << 20, 16))), ("laplace", rng.laplace(size=(1 << 20, 16))),
                ("student-t3", rng.standard_t(3, size=(1 << 20, 16)))):
    sc = np.abs(x).max(1, keepdims=True) / 6
    z = (np.abs(x / sc) < 0.25).mean()
    print(f"{name:<11} zero codes {z:.3f} -> weight-only zero-skip speedup <= {1/(1-z):.2f}x")
