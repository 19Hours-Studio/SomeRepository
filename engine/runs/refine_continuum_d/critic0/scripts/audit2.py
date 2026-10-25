"""Critic audit 2: (a) calibration composition, (b) site-level dilution by GPU prefill,
(c) two-phase overlap bracket applied to BOTH systems (weights-phase and attention-phase serialise within a microbatch)."""
import sys, math
R7 = "/home/user/SomeRepository/engine/runs/refine_continuum/round7"
sys.path[:0] = [R7, R7 + "/../round6"]
import model7 as q, model5 as m
C = q.C128
# (a) calib7: share of GPU-time that is prefill
GB = dict(m.SYS["GB300"], imb=q.IMB_G, s=1.0)
pre = m.comp_time(m.V4, GB, 1, 61, 4096); dec = 1 / 62772
print(f"calib: per output token, decode {dec:.3e} s, prefill 8x{pre:.3e}={8*pre:.3e} s -> prefill share {8*pre/(8*pre+dec):.0%} of GPU time")

# (b) prefill energy per fresh prompt token on Rubin (compute-bound, eta 0.6, s=1.43, mean ctx 64K), best PF/kW profile
best = None
for lab, s, f in q.RUBIN_PROF():
    s = dict(s, s=1.43)
    J = m.comp_time(m.V4, s, 1, 61, C // 2) * s["P"] / m.DERATE
    best = min(best or (9, ""), (J, lab))
Jp = best[0]; print(f"Rubin prefill {Jp*1e3:.1f} mJ per fresh prompt token at 128K ({best[1]})")
A = q.pipe_env(q.cont_prof(q.C7T, q.C7T_PARTS), C, gs=(1,2,3,4,6)); R = q.gpu_env(q.RUBIN_PROF(), C)
print("fresh prompt tok per output tok -> site-level C7/Rubin ratio at >=200 / >=1000 / >=2000")
for r in (0, 0.5, 1, 2, 4, 8, 16, 75):
    out = []
    for t in (200, 1000, 2000):
        jc, jr = 1 / A[t][0], 1 / R[t][0]
        out.append((jr + r * Jp) / (jc + r * Jp))
    print(f"  r={r:<4} " + " ".join(f"{x:5.2f}" for x in out))

# (c) two-phase overlap bracket
def gpu2(s, tau, ctx, k, p, M=m.V4, ms=m.MS):
    pos, tok, L = m.spec(M, k, p); N, out = s["N"], []
    f8, f4a = m.attn_flops(M, ctx)
    for t in (1, 2, 4, 8):
        wb = L * M["n_exp"] * m.b_exp(M) / N + (L * m.b_dense(M) + M["head"] * 4.5 / 8) / t
        for mm in ms:
            for Bm in m.BGRID:
                B = Bm * mm
                if wb + B * t / N * m.kv_store(M, ctx) > 0.9 * s["hbm"] * 1e9: break
                n = Bm * pos / N
                memW = (L * m.touched(M, Bm * pos) * m.b_exp(M) / N + (L * m.b_dense(M) + M["head"] * 4.5 / 8) / t) / s["hbmbw"]
                memK = Bm * t / N * m.kv_read(M, ctx) / s["hbmbw"]
                cL = n * s["imb"] * m.lin_flops(M, L) / (s["F4"] * s["s"]) / m.ETA
                cA = n * s["imb"] * (f8 / s["F8"] + f4a / s["F4"]) / m.ETA
                lnk = n * L * m.a2a(M) * (N - 1) / N / s["link"]
                c = max(max(memW, cL) + max(memK, cA), lnk) / L
                T = max(mm * c, c + tau)
                out.append((tok / (L * T), m.DERATE * B * tok / (L * T) / (N * s["P"]), B, (t, mm), {}))
    return out
def pipe2(s, tau, ctx, k, p, M=m.V4, gmin=1, ms=m.MS):
    pos, tok, L = m.spec(M, k, p); lay_b = M["n_exp"] * m.b_exp(M) + m.b_dense(M); out = []
    f8, f4a = m.attn_flops(M, ctx)
    for mm in ms:
        for b in m.BGRID:
            g = max(math.ceil(lay_b / (0.9 * s["sram"] * 1e9)), gmin)
            if mm * b * m.kv_store(M, ctx) > 0.9 * g * s["hbm"] * 1e9: break
            sram_t = (m.touched(M, b * pos) * m.b_exp(M) / g + m.b_dense(M)) / s["srambw"]
            kv_t = b * m.kv_read(M, ctx) / L / (g * s["hbmbw"])
            n = b * pos / L / g
            cL = n * s["imb"] * m.lin_flops(M, L) / (s["F4"] * s["s"]) / m.ETA
            cA = n * s["imb"] * (f8 / s["F8"] + f4a / s["F4"]) / m.ETA
            lnk = b * pos * (M["hid"] * (g - 1) / g + 2 * M["hid"]) / s["link"]
            c = max(max(sram_t, cL) + max(kv_t, cA), lnk)
            T = max(mm * c, c + tau)
            out.append((tok / (L * T), m.DERATE * mm * b * tok / T / ((L * g + 1) * s["P"]), b, (L * g + 1, mm), {}))
    return out
og, op = m.gpu_points, m.pipe_points
m.gpu_points, m.pipe_points = gpu2, pipe2
for ctx in (C, q.C1M):
    A2 = q.pipe_env(q.cont_prof(q.C7T, q.C7T_PARTS), ctx, gs=(1,2,3,4,6)); R2 = q.gpu_env(q.RUBIN_PROF(), ctx)
    print(f"two-phase {ctx//1024}K: C7 {q.vals(A2)}\n            Rubin {q.vals(R2)}\n            ratio {q.ratio(A2, R2)}")
m.gpu_points, m.pipe_points = og, op
