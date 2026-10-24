"""Idea 3: measure escalation rate of 3-bit tiles under a cheap provable error bound.

Tile = dot products of length K (one MMA reduction tile). 3-bit symmetric integer quant
(levels -3..3) with a per-tile absmax scale for A rows and B columns. Cheap hardware bound
per output: sum_k |a_k| db + |b_k| da + da*db  (da, db = half-steps), which is a valid
worst-case bound. Budget = the same-style provable bound for NVFP4 (E2M1, block 16,
per-block scale) and for FP8 E4M3, i.e. like-for-like "provable" accuracy targets.
Escalate if bound_3bit > budget.
"""
import numpy as np

rng = np.random.default_rng(0)
FP4 = np.array([0, 0.5, 1, 1.5, 2, 3, 4, 6])


def q_int3(x):
    s = np.abs(x).max(axis=-1, keepdims=True) / 3.0
    q = np.clip(np.round(x / s), -3, 3) * s
    return q, s / 2.0  # value, half-step (per element bound)


def q_fp4_block(x, blk=16):
    sh = x.shape
    xb = x.reshape(*sh[:-1], -1, blk)
    s = np.abs(xb).max(axis=-1, keepdims=True) / 6.0
    s[s == 0] = 1
    m = np.abs(xb) / s
    idx = np.abs(m[..., None] - FP4).argmin(-1)
    v = FP4[idx]
    # half-ulp at that grid point (element-wise bound)
    ulp = np.where(v < 2, 0.5, np.where(v < 4, 1.0, 2.0))
    q = np.sign(xb) * v * s
    return q.reshape(sh), (ulp / 2 * s).reshape(sh)


def q_fp8(x):
    # E4M3 with per-tensor scale: 3 mantissa bits -> half-ulp = |x| * 2^-4 (relative)
    e = np.floor(np.log2(np.abs(x) + 1e-30))
    ulp = 2.0 ** (e - 3)
    q = np.round(x / ulp) * ulp
    return q, ulp / 2


def bound(a, da, b, db):
    return (np.abs(a) * db + np.abs(b) * da + da * db).sum(-1)


def run(dist, K=128, n=20000):
    if dist == "gauss":
        A = rng.standard_normal((n, K)); B = rng.standard_normal((n, K))
    else:  # heavy-tailed activations (student-t df=3), gaussian weights
        A = rng.standard_t(3, (n, K)); B = rng.standard_normal((n, K))
    exact = (A * B).sum(-1)
    out = {}
    for name, f in [("int3", q_int3), ("nvfp4", q_fp4_block), ("fp8", q_fp8)]:
        qa, da = f(A); qb, db = f(B)
        err = np.abs((qa * qb).sum(-1) - exact)
        bd = bound(qa, np.broadcast_to(da, A.shape), qb, np.broadcast_to(db, B.shape))
        assert np.all(err <= bd * (1 + 1e-9) + 1e-9), name  # bound must be valid
        out[name] = (err, bd)
    e3, b3 = out["int3"]
    res = {}
    for tgt in ["nvfp4", "fp8"]:
        eb = out[tgt][1]
        res[tgt] = dict(esc_vs_bound=(b3 > eb).mean(),
                        esc_vs_bound_x4=(b3 > 4 * eb).mean(),
                        median_bound_ratio=np.median(b3 / eb))
    res["rms_err"] = {k: float(np.sqrt((v[0] ** 2).mean())) for k, v in out.items()}
    return res


# Known-answer check: uniform rounding error with step h has variance h^2/12
x = rng.uniform(-1, 1, 10**6); h = 0.1
print("check var ratio (expect 1.0):", np.var(np.round(x / h) * h - x) / (h * h / 12))
for d in ["gauss", "heavy"]:
    print(d, run(d))
