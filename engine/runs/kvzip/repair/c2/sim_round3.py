# Round 3: (a) duplicate-content regime where centering cannot remove coherence but dither can;
# (b) the absolute-error bound err ~ rel_rms(b) * E_h, E_h = sqrt(sum_{quantized} p^2), sinks/recent excluded.
import numpy as np
exec(open("sim_dither.py").read().split("res = {}")[0])
exec(open("sim_dither2.py").read().split("for kind in")[0].split("rng = np.random.default_rng(5)")[1])
rng = np.random.default_rng(9)
# (a) 4096 tokens drawn from 64 distinct value vectors (repeated phrases / code / CoT loops) + tiny noise
proto = rng.standard_normal((64, D)); ids = rng.integers(0, 64, T)
V = proto[ids] + 0.02*rng.standard_normal((T, D)); VR = V @ H.T
R = {"rot+RTN2": quant(VR,2)@H, "rot+ctr+RTN2": center_quant(VR,2)@H, "rot+dith2": quant(VR,2,True)@H,
     "rot+ctr+RTN4": center_quant(VR,4)@H, "rot+dith3": quant(VR,3,True)@H}
print("(a) duplicates: head attends uniformly to all n copies of one phrase; abs err / |v|")
for n_target in [1, 8, 64]:
    k = 0; idx = np.where(ids == k)[0][:n_target]
    p = np.zeros(T); p[idx] = 1/len(idx); o = p@V
    print(f"  N_eff={len(idx):3d} " + " ".join(f"{kk}={np.linalg.norm(p@r-o)/np.linalg.norm(o):.3f}" for kk,r in R.items()))
# (b) bound check on iid values: abs error/|v| vs rel_rms*E_h
V = rng.standard_normal((T, D)); VR = V@H.T
for b in [2,3,4]:
    r = quant(VR,b,True)@H; rel = np.linalg.norm(r-V)/np.linalg.norm(V)
    out=[]
    for ne in [1.5,16,256]:
        p,_ = attn_probs(ne); E=np.sqrt((p**2).sum())
        out.append(f"E={E:.3f}: meas={np.linalg.norm(p@r-p@V)/np.sqrt(D):.3f} pred={rel*E:.3f}")
    print(f"(b) dith{b} rel_rms={rel:.3f}  " + " | ".join(out))
