"""Gate arithmetic for 4 KV-cache ideas. Synthetic data only (HF blocked): quantizer error on
Hadamard-rotated Gaussian channels (the idealised post-rotation case) + exact bit / bandwidth arithmetic."""
import numpy as np
from scipy.linalg import hadamard

rng = np.random.default_rng(0)
D, N = 128, 20000

def q_uniform(x, bits, g):
    """asymmetric min-max per group of g along last axis, returns reconstruction"""
    s = x.reshape(-1, g)
    lo, hi = s.min(1, keepdims=True), s.max(1, keepdims=True)
    L = 2**bits - 1
    sc = (hi - lo) / L
    c = np.clip(np.round((s - lo) / sc), 0, L)
    return (c * sc + lo).reshape(x.shape), c.reshape(x.shape), lo, sc

def bitplane_top2(x, g):
    """4-bit codes, read only top 2 planes, reconstruct at bin centre"""
    _, c, lo, sc = q_uniform(x, 4, g)
    s = c.reshape(-1, g)
    top = np.floor(s / 4) * 4 + 1.5
    return (top * sc + lo).reshape(x.shape)

E2M1 = np.array([0, .5, 1, 1.5, 2, 3, 4, 6])
def q_nvfp4(x):
    s = x.reshape(-1, 16)
    amax = np.abs(s).max(1, keepdims=True)
    sc = amax / 6.0  # (FP8 rounding of scale ignored -> slightly optimistic for NVFP4)
    v = np.abs(s) / sc
    idx = np.abs(v[..., None] - E2M1).argmin(-1)
    return (np.sign(s) * E2M1[idx] * sc).reshape(x.shape)

def rel(x, xh):
    return np.sqrt(((x - xh)**2).mean() / (x**2).mean())

# --- known-answer checks
u = rng.uniform(-1, 1, (N, D))
xh, *_ = q_uniform(u, 4, 128)
print("CHECK uniform data 4b g128 relMSE %.5f  theory ~ (2/15)^2/12/(1/3)=%.5f" % (((u-xh)**2).mean()/(u**2).mean(), (2/15)**2/12/(1/3)))

# --- Gaussian with outlier channels, then Hadamard rotation (QuaRot/TurboQuant-style)
x = rng.standard_normal((N, D)) * np.where(np.arange(D) < 4, 10.0, 1.0)  # 4 outlier channels like keys
H = hadamard(D) / np.sqrt(D)
xr = x @ H
res = {}
for name, f in [("2b g32", lambda a: q_uniform(a, 2, 32)[0]), ("2b g128", lambda a: q_uniform(a, 2, 128)[0]),
                ("4b g32", lambda a: q_uniform(a, 4, 32)[0]), ("4b g128", lambda a: q_uniform(a, 4, 128)[0]),
                ("bitplane top2 of 4b g32", lambda a: bitplane_top2(a, 32)),
                ("1b g128", lambda a: q_uniform(a, 1, 128)[0]), ("NVFP4", q_nvfp4)]:
    res[name] = rel(xr, f(xr))
    print("rotated  %-26s rel-RMS err %.3f" % (name, res[name]))
print("unrotated 2b g128 rel-RMS err %.3f" % rel(x, q_uniform(x, 2, 128)[0]))

# --- IDEA 1: tail-mass tolerance as written: m_tail * e_value <= 1e-3
e2 = res["bitplane top2 of 4b g32"]
m_req = 1e-3 / e2
print("\nIDEA1 required tail mass <= %.4f  (coverage >= %.2f%%)" % (m_req, 100*(1-m_req)))
# bits: 4-bit codes + scale/zero; read = 2 planes + scales + 2% * 2 low planes + window
print("IDEA1 read bits/value (32k ctx): %.3f" % (2.5 + 0.02*2 + (68/32768)*2))

# --- IDEA 2: residual traffic over PCIe
def fetch(layers, kvh, k=256, d=128): return layers*kvh*k*2*d*2/8  # K+V, 2-bit residual
f70, f8 = fetch(80, 8), fetch(32, 8)
print("\nIDEA2 70B fetch/req/step %.1f MB ; 8B %.1f MB" % (f70/1e6, f8/1e6))
pcie = 45e9  # PCIe5 x16 64 GB/s raw, ~0.7 efficiency for 64-B scattered TLPs (assumption)
for nm, f, L, B in [("A 70B TP8 b8 (per GPU)", f70/8*8, 80, 8), ("B 8B b10", f8*10, 32, 10)]:
    t = f/pcie + L*10e-6   # + per-layer dependent round trip/top-k ~10us (assumption)
    print("IDEA2 %s: PCIe bytes %.1f MB -> %.2f ms/step incl %d serial layer hops" % (nm, f/1e6, t*1e3, L))

# --- IDEA 4: bit budget feasibility. group-128 FP16 scale+zero = 0.25 b/value overhead (favourable)
ov = 0.25
lo_, mid, hi_ = (2+1)/2+ov, (3+2)/2+ov, 4+ov
f_hi_max = (2.1 - lo_) / (hi_ - lo_)
print("\nIDEA4 bits: K2V1 %.2f K3V2 %.2f K4V4 %.2f ; max K4V4 head fraction at 2.1b avg = %.3f" % (lo_, mid, hi_, f_hi_max))
print("IDEA4 avg bits if 50%% heads K4V4 (DuoAttention GQA) rest K2V1: %.2f" % (0.5*hi_+0.5*lo_))

# --- CHAIN on archetype B (ledger shares at FP16 KV, batch 10): KV 50, W 36, kern 5, prefill 1, other 8
def cost(kv_bits, kv_mult=1.0, extra=0.0, store_bits=None, cap=False):
    kv = 50*kv_bits/16*kv_mult
    w = 36.0
    if cap:  # capacity-aware: batch limited by 56 GB free HBM, KV/req 4.3 GB at FP16 end
        b = min(56/(4.3*(store_bits or kv_bits)/16), 64)
        w = 36*10/b
    return kv + w + 5 + 1 + 8 + extra
unit_ms = (21.5e9/3.35e12)*1e3/50   # 1 ledger unit in ms of step time (FP16 KV avg read)
pcie_units = (f8*10/pcie + 32*10e-6)*1e3/unit_ms
for cap in (False, True):
    base = cost(4.5, store_bits=4.5, cap=cap)
    rows = {"I1": cost(2.58, store_bits=4.5, cap=cap), "I2": cost(2.25, extra=pcie_units*(1 if not cap else 1), store_bits=2.25, cap=cap),
            "I3": cost(2.2, 1.125, store_bits=4.3, cap=cap), "I4": cost(2.1, store_bits=2.1, cap=cap)}
    print("\nCHAIN B cap=%s NVFP4=%.1f units; " % (cap, base) + " ".join("%s %.1f (RATIO %.2f)" % (k, v, base/v) for k, v in rows.items()))
print("note: I2 cap=True keeps PCIe at batch-10 size (optimistic for I2)")
