"""Gate arithmetic + quantizer error measurements for the 4 KV-cache ideas.
Synthetic data only (Gaussian / heavy-tailed, Hadamard-rotated); real KV tensors unavailable (HF blocked)."""
import numpy as np
from scipy.linalg import hadamard
rng = np.random.default_rng(0)

# ---------- Lloyd-Max codebooks (known-answer check: MSE 0.3634 / 0.1175 / 0.03454 for 1/2/3 bits) ----------
def lloyd_max(bits, n=2_000_000, it=200):
    x = rng.standard_normal(n)
    L = 2**bits
    c = np.quantile(x, (np.arange(L) + 0.5) / L)
    for _ in range(it):
        t = (c[1:] + c[:-1]) / 2
        idx = np.searchsorted(t, x)
        c = np.array([x[idx == i].mean() for i in range(L)])
    t = (c[1:] + c[:-1]) / 2
    return c, np.mean((x - c[np.searchsorted(t, x)])**2)
CB = {}
for b in (1, 2, 3):
    c, mse = lloyd_max(b)
    CB[b] = c
    print(f"Lloyd-Max {b}-bit Gaussian MSE = {mse:.4f}  (known: {[0.3634,0.1175,0.03454][b-1]})")

def e4m3(s):  # round positive scale to FP8 E4M3
    s = np.maximum(s, 2**-9)
    e = np.floor(np.log2(s)); m = np.round(s / 2**e * 8) / 8
    return m * 2**e

def q_lm(x, bits, g):  # fixed Gaussian codebook, FP8 RMS scale per group
    xg = x.reshape(-1, g); s = e4m3(np.sqrt((xg**2).mean(1, keepdims=True)))
    c = CB[bits]; t = (c[1:] + c[:-1]) / 2
    return (c[np.searchsorted(t, xg / s)] * s).reshape(x.shape)

FP4 = np.array([0, .5, 1, 1.5, 2, 3, 4, 6])
def q_nvfp4(x):  # E2M1 values, E4M3 absmax scale per 16
    xg = x.reshape(-1, 16); s = e4m3(np.abs(xg).max(1, keepdims=True) / 6)
    y = np.abs(xg) / s; grid = FP4
    q = grid[np.abs(y[..., None] - grid).argmin(-1)]
    return (np.sign(xg) * q * s).reshape(x.shape)

def q_uniform(x, bits, g, keep_planes=None):  # asym min-max, FP16 scale/zero; optional bit-plane truncation
    xg = x.reshape(-1, g); lo = xg.min(1, keepdims=True); hi = xg.max(1, keepdims=True)
    L = 2**bits - 1; s = (hi - lo) / L
    code = np.clip(np.round((xg - lo) / s), 0, L).astype(int)
    if keep_planes is not None:  # keep top planes, reconstruct at bucket midpoint
        drop = bits - keep_planes
        code = (code >> drop << drop) + (2**drop - 1) / 2
    return (code * s + lo).reshape(x.shape)

def rel_err(x, xh):
    return np.sqrt(np.mean((x - xh)**2) / np.mean(x**2))

d = 128; N = 4096
H = hadamard(d) / np.sqrt(d)
# synthetic "keys": per-channel scale outliers (a few channels 10x) -> rotate
chs = np.ones(d); chs[rng.choice(d, 4, replace=False)] = 10
K = (rng.standard_normal((N, d)) * chs) @ H
V = rng.standard_normal((N, d)) @ H
print("\nRelative RMS error (rotated synthetic K / V):")
rows = [("3-bit LM fixed codebook, FP8 RMS scale /64 (Idea4, 3.125b)", lambda x: q_lm(x, 3, 64)),
        ("NVFP4 E2M1 + E4M3 /16 (4.5b)", q_nvfp4),
        ("4-bit uniform /32 FP16 s+z (5.0b)", lambda x: q_uniform(x, 4, 32)),
        ("top-2 planes of 4-bit uniform /32 (Idea2/3 coarse)", lambda x: q_uniform(x, 4, 32, keep_planes=2)),
        ("2-bit uniform /32 (KIVI-like)", lambda x: q_uniform(x, 2, 32)),
        ("1-bit LM /64 FP8 scale (Idea1 V1)", lambda x: q_lm(x, 1, 64)),
        ("2-bit LM /64 FP8 scale", lambda x: q_lm(x, 2, 64))]
res = {}
for name, f in rows:
    rk, rv = rel_err(K, f(K)), rel_err(V, f(V)); res[name] = rv
    print(f"  {name:58s} K {rk:.3f}  V {rv:.3f}  SQNR_V {-20*np.log10(rv):5.1f} dB")

# ---------- Idea 1: head fraction arithmetic ----------
print("\nIdea 1 bit arithmetic (scale overhead o bits/value):")
for o in (0.125, 0.25, 0.5):
    a, b, c = 1.5 + o, 2.5 + o, 4.0 + o
    cmax = (2.1 - a) / (c - a)
    avg_duo = 0.5 * c + 0.5 * a
    print(f"  o={o}: K2V1={a} K3V2={b} K4V4={c}; max K4V4 head fraction for 2.1b avg = {cmax:.3f}; "
          f"avg with 50% retrieval heads (DuoAttention GQA) = {avg_duo:.2f}b -> {16/avg_duo:.2f}x")

# ---------- Idea 3 deciding quantity: tail mass * value error ----------
ev = res["top-2 planes of 4-bit uniform /32 (Idea2/3 coarse)"]
print(f"\nIdea 3: coarse value rel err {ev:.3f}; allowed coarse-only mass for 1e-3 = {1e-3/ev:.4f}")
for m in (0.05, 0.10, 0.20):
    print(f"  if coarse-only mass={m}: mass*err={m*ev:.4f} -> margin {1e-3/(m*ev):.3f}")

# ---------- Chain (Archetype B, decode-heavy CoT; NVFP4 KV = best practice) ----------
# shares at FP16 KV: KV reads 50, weight reads 36, fixed 14. Two bounds:
#  (a) batch fixed: only KV-read term scales with bits read
#  (b) capacity-limited batch: weight-read-per-request also scales with stored bits
def cost(read_b, store_b, overhead=0.0, capacity=False):
    kv = 50 * read_b / 16 * (1 + overhead)
    w = 36 * (store_b / 16 if capacity else 1)
    return kv + w + 14
base_a, base_b = cost(4.5, 4.5), cost(4.5, 4.5, capacity=True)
ideas = {"Idea1 (2.1b read/store)": (2.1, 2.1, 0.0),
         "Idea2 (2.2b read + 2%x2.15 refine, 4.3b store, +12.5% kernel)": (2.15 + 0.02*2.15, 4.3, 0.125),
         "Idea3 (2.6b read, 4.5b store)": (2.6, 4.5, 0.0),
         "Idea3 with +12.5% two-pass overhead": (2.6, 4.5, 0.125),
         "Idea4 (3.125b read/store; sinks+window FP8 negligible)": (3.125, 3.125, 0.0)}
print(f"\nChain Archetype B vs NVFP4 baseline: base(fixed batch)={base_a:.1f}, base(capacity)={base_b:.1f}")
for k, (r, s, o) in ideas.items():
    a, b = cost(r, s, o), cost(r, s, o, capacity=True)
    print(f"  {k:62s} fixed-batch RATIO {base_a/a:.2f} | capacity-limited RATIO {base_b/b:.2f}")
# PCIe check for Idea 2 host offload of refinement planes: 32k ctx, 8B model 128KB/token FP16
ref_bytes = 32768 * 128e3 * (2.15/16) * 0.02
print(f"\nIdea2 host-offload: refine bytes/request/step = {ref_bytes/1e6:.1f} MB; batch 40 over 50 GB/s PCIe = "
      f"{40*ref_bytes/50e9*1e3:.1f} ms/step vs HBM KV read at 4.5b batch 40 = {40*32768*128e3*4.5/16/3.35e12*1e3:.1f} ms")
