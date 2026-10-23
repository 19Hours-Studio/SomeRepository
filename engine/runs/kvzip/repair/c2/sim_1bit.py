# Round 4: is 1-bit DITHERED value plane usable in broad heads (anchor's strongest regime)?
import numpy as np
exec(open("sim_dither.py").read().split("res = {}")[0])
exec(open("sim_dither2.py").read().split("for kind in")[0].split("rng = np.random.default_rng(5)")[1])
rng = np.random.default_rng(11)
T2 = 4096
for kind in ["iid", "struct", "dup"]:
    if kind == "dup":
        proto = rng.standard_normal((16, D)); V = proto[rng.integers(0, 16, T2)] + 0.02*rng.standard_normal((T2, D))
    else:
        V = make_values(kind)
    VR = V @ H.T
    R = {"RTN1": quant(VR,1)@H, "dith1": quant(VR,1,True)@H, "ctr+RTN1": center_quant(VR,1)@H,
         "ctr+dith1": center_quant(VR,1,dither=True)@H, "RTN4": quant(VR,4)@H}
    relr = {k: np.linalg.norm(r-V)/np.linalg.norm(V) for k,r in R.items()}
    line = []
    for ne in [64, 512, 2048]:
        p,_ = attn_probs(ne); E = np.sqrt((p**2).sum()); o = p@V
        line.append(f"N_eff~{ne}(E={E:.3f}): " + " ".join(f"{k}={np.linalg.norm(p@r-o)/np.sqrt(np.mean(np.sum(V**2,1))):.3f}" for k,r in R.items()))
    print(f"[{kind}] rel_rms " + " ".join(f"{k}={v:.2f}" for k,v in relr.items()))
    for l in line: print("   ", l)
print("target: abs err/|v| <= rel4*1 (single-token V4 retrieval) =", 0.10)
