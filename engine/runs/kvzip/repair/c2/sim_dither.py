# Idea 1: does subtractive dither on the VALUE plane help, and in which regime?
# Output error of attention o = sum_i p_i v_i under per-token group-128 min-max quantization.
import numpy as np
rng = np.random.default_rng(0)
D, T = 128, 4096
from scipy.linalg import hadamard
H = hadamard(D) / np.sqrt(D)

def make_values(kind):
    if kind == "iid":
        return rng.standard_normal((T, D))
    # structured: per-channel mean (coherent across tokens) + smaller per-token variation,
    # 2 outlier channels (x8) -- typical "value has channel offsets, small token deltas"
    mu = rng.standard_normal(D) * 1.0
    sc = np.ones(D); sc[[3, 77]] = 8.0
    delta = rng.standard_normal((T, D)) * 0.35
    return (mu + delta) * sc

def quant(x, bits, dither=False, seed=1):
    L = 2 ** bits
    lo = x.min(1, keepdims=True); hi = x.max(1, keepdims=True)
    lo = lo.astype(np.float16).astype(float); hi = hi.astype(np.float16).astype(float)
    d = (hi - lo) / (L - 1)
    if dither:
        u = np.random.default_rng(seed).uniform(-0.5, 0.5, x.shape)  # regenerated from seed at decode
        q = np.clip(np.round((x - lo) / d + u), 0, L - 1)
        return (q - u) * d + lo
    q = np.clip(np.round((x - lo) / d), 0, L - 1)
    return q * d + lo

def attn_probs(neff_target):
    # logits with one "needle" plus gaussian background; tune temperature to hit N_eff
    z = rng.standard_normal(T)
    best = None
    for beta in np.logspace(-2, 2, 400):
        p = np.exp(beta * z - (beta * z).max()); p /= p.sum()
        ne = 1 / (p ** 2).sum()
        if best is None or abs(np.log(ne / neff_target)) < abs(np.log(best[1] / neff_target)):
            best = (p, ne)
    return best

res = {}
for kind in ["iid", "struct"]:
    V = make_values(kind)
    VR = V @ H.T
    recon = {
        "RTN2": quant(V, 2), "dith2": quant(V, 2, True),
        "rot+RTN2": quant(VR, 2) @ H, "rot+dith2": quant(VR, 2, True) @ H,
        "RTN3": quant(V, 3), "rot+dith3": quant(VR, 3, True) @ H,
        "RTN4": quant(V, 4), "rot+RTN4": quant(VR, 4) @ H,
    }
    print(f"\n== values: {kind} ==  per-element rel RMS:",
          {k: round(float(np.linalg.norm(r - V) / np.linalg.norm(V)), 3) for k, r in recon.items()})
    print("mean error (bias):", {k: float(f"{(r - V).mean():.1e}") for k, r in recon.items()})
    print(f"{'N_eff':>7} " + " ".join(f"{k:>10}" for k in recon))
    for ne in [1.5, 4, 16, 64, 256, 1024]:
        errs = {k: [] for k in recon}
        for rep in range(6):
            p, nea = attn_probs(ne)
            o = p @ V
            # signal = the part of the output that depends on WHICH tokens are attended
            sig = np.linalg.norm(o - V.mean(0)) + 1e-9
            for k, r in recon.items():
                errs[k].append(np.linalg.norm(p @ r - o) / max(sig, 0.05 * np.linalg.norm(o)))
        print(f"{nea:7.1f} " + " ".join(f"{np.mean(v):10.3f}" for v in errs.values()))
