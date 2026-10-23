# Round 2: compare decorrelation fixes on structured values: subtractive dither (Idea 1) vs
# per-block channel-mean centering (Idea 2 fix); and check the sqrt(sum p^2) scaling rule.
import numpy as np
from scipy.linalg import hadamard
exec(open("sim_dither.py").read().split("res = {}")[0])  # reuse helpers
rng = np.random.default_rng(5)

def center_quant(x, bits, blk=128, dither=False):
    out = np.empty_like(x)
    for s in range(0, len(x), blk):
        m = x[s:s+blk].mean(0).astype(np.float16).astype(float)   # FP16 channel mean per 128-token block
        out[s:s+blk] = quant(x[s:s+blk] - m, bits, dither, seed=s) + m
    return out

for kind in ["struct", "iid"]:
    V = make_values(kind); VR = V @ H.T
    R = {"rot+RTN2": quant(VR,2)@H, "rot+dith2": quant(VR,2,True)@H,
         "rot+ctr+RTN2": center_quant(VR,2)@H, "rot+ctr+dith2": center_quant(VR,2,dither=True)@H,
         "rot+dith3": quant(VR,3,True)@H, "rot+ctr+RTN3": center_quant(VR,3)@H,
         "rot+RTN4": quant(VR,4)@H}
    print(f"\n== {kind}: per-element rel RMS", {k: round(float(np.linalg.norm(r-V)/np.linalg.norm(V)),3) for k,r in R.items()})
    print("metric A = |err|/|o - mean(V)| (selective signal);  E=sqrt(sum p^2)")
    print(f"{'N_eff':>7} {'E':>6} " + " ".join(f"{k:>13}" for k in R))
    for ne in [1.5, 4, 16, 64, 256, 1024]:
        acc = {k: [] for k in R}; Es=[]
        for rep in range(6):
            p, nea = attn_probs(ne); o = p@V; sig = max(np.linalg.norm(o-V.mean(0)), 0.05*np.linalg.norm(o))
            Es.append(np.sqrt((p**2).sum()))
            for k,r in R.items(): acc[k].append(np.linalg.norm(p@r-o)/sig)
        print(f"{nea:7.1f} {np.mean(Es):6.3f} " + " ".join(f"{np.mean(v):13.3f}" for v in acc.values()))
