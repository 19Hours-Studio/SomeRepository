"""Kill-test measurements for ideas 2-4 (synthetic weights; HF download blocked by proxy)."""
import numpy as np
from scipy.stats import norm
rng = np.random.default_rng(0)

def kmeans1d(x, k, iters=60):
    c = np.quantile(x, (np.arange(k) + 0.5) / k)
    for _ in range(iters):
        idx = np.abs(x[:, None] - c[None]).argmin(1)
        for j in range(k):
            m = idx == j
            if m.any(): c[j] = x[m].mean()
    return c[np.abs(x[:, None] - c[None]).argmin(1)]

# --- known-answer check: Lloyd-Max 16-level Gaussian MSE = 0.009497 (Max 1960)
g = rng.standard_normal(200000)
print("check Lloyd-Max16 Gaussian MSE", np.mean((kmeans1d(g, 16) - g) ** 2), "expected 0.009497")

# FP formats
def fp_grid(e, m, bias):
    vals = [0.0]
    for E in range(0, 2 ** e):
        for M in range(2 ** m):
            v = (M / 2 ** m) * 2.0 ** (1 - bias) if E == 0 else (1 + M / 2 ** m) * 2.0 ** (E - bias)
            vals.append(v)
    v = np.unique(np.array(vals)); return np.concatenate([-v[::-1], v])
E2M1 = fp_grid(2, 1, 1)                       # max 6
E4M3 = fp_grid(4, 3, 7); E4M3 = E4M3[np.abs(E4M3) <= 448]
def q_grid(x, grid): return grid[np.abs(x[..., None] - grid).argmin(-1)]
def fp8_tensor(w):  # per-output-channel scale FP8 e4m3
    s = np.abs(w).max(1, keepdims=True) / 448; return q_grid(w / s, E4M3) * s
def nvfp4(w, B=16):  # NVFP4: 16-elem blocks, E4M3 scale
    r = w.reshape(-1, B); s = np.abs(r).max(1, keepdims=True) / 6
    s = q_grid(s / s.max(), E4M3[E4M3 > 0]) * s.max()  # scale itself in FP8 (relative)
    return (q_grid(r / s, E2M1) * s).reshape(w.shape)
def cb_group(w, k=16, G=128):  # Idea 2: k-entry codebook per channel group of G (with absmax normalisation)
    r = w.reshape(-1, G); out = np.empty_like(r)
    for i in range(r.shape[0]):
        out[i] = kmeans1d(r[i], k, 25)
    return out.reshape(w.shape)
def cb_layer(w, k):  # Idea 3: one codebook per layer
    return kmeans1d(w.ravel(), k, 40).reshape(w.shape)
def sqnr(w, q): return 10 * np.log10(np.sum(w ** 2) / np.sum((w - q) ** 2))

# synthetic LLM-like weight: Student-t(5) entries, lognormal per-input-channel scale (outlier channels)
O, I = 256, 1024
W = rng.standard_t(5, (O, I)) * np.exp(0.6 * rng.standard_normal(I))[None] * 0.02
res = {"FP8 e4m3/ch": sqnr(W, fp8_tensor(W)), "NVFP4": sqnr(W, nvfp4(W)),
       "CB16/group128 (idea2)": sqnr(W, cb_group(W, 16, 128)), "CB8/group128 (idea2)": sqnr(W, cb_group(W, 8, 128)),
       "CB16/layer (idea3, 4b)": sqnr(W, cb_layer(W, 16)), "CB64/layer (idea3, 6b)": sqnr(W, cb_layer(W, 64))}
for k, v in res.items(): print(f"SQNR {k:26s} {v:6.2f} dB")
for k in ["CB16/group128 (idea2)", "CB16/layer (idea3, 4b)", "CB64/layer (idea3, 6b)"]:
    print(f"MSE ratio FP8/{k}: {10 ** ((res['FP8 e4m3/ch'] - res[k]) / -10):.3f}   NVFP4/{k}: {10 ** ((res['NVFP4'] - res[k]) / -10):.3f}")

# --- Idea 4: does ABFT checksum residual track the true quantisation error of a tile?
print("\nIdea 4: ABFT residual vs true tile error")
T = 128; ntile = 400; tr, rr = [], []
for t in range(ntile):
    A = rng.standard_normal((T, T)) * np.exp(rng.standard_normal() * 0.5)
    Bw = rng.standard_t(rng.choice([2.5,4,8,30]), (T, T)) * 0.02 * np.exp(rng.standard_normal() * 0.5)
    C = A @ Bw; Cq = A @ nvfp4(Bw)
    check = A @ Bw.sum(1)                     # high-precision row checksum A.(B.1)
    resid = Cq.sum(1) - check                 # residual seen by hardware
    tr.append(np.linalg.norm(Cq - C) / np.linalg.norm(C)); rr.append(np.linalg.norm(resid) / np.linalg.norm(check))
tr, rr = np.array(tr), np.array(rr)
# known-answer: exact computation -> residual ~ fp64 roundoff
A = rng.standard_normal((T, T)); Bw = rng.standard_normal((T, T))
print("check exact residual", np.abs((A @ Bw).sum(1) - A @ Bw.sum(1)).max())
print("corr(log resid, log true err) =", np.corrcoef(np.log(rr), np.log(tr))[0, 1])
# per-tile decision quality: fraction of tiles whose true error rank-tercile is predicted by residual
thr_t, thr_r = np.median(tr), np.median(rr)
print("decision agreement above/below median:", np.mean((tr > thr_t) == (rr > thr_r)))
# relative error is ~constant for a given format; what varies is whether residual separates bad tiles
print("true rel err range", tr.min(), tr.max(), " resid range", rr.min(), rr.max())
