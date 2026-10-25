"""Activity energy per accepted output token at the run5 §F operating points (V4-Pro, 128K, p=0.8, equal tau).
pJ/FLOP FP4: Continuum (N2) 0.040, Rubin (N3P) 0.050; FP8 = 2x; zero-skip removes s-1 of FP4 linear work energy
at 50% of the saving (control overhead). SRAM 0.15, HBM4 3.5, links 5 pJ/bit. Static/leakage excluded.
Usage: python3 energy5.py > energy5.txt"""
import model5 as m, run5 as r
M, C = m.V4, r.C128
def energy(kind, B_mu, k, pj4):
    pos, tok, L = m.spec(M, k, 0.8)
    f8, f4a = m.attn_flops(M, C)
    lin = m.lin_flops(M, L)
    e_c = pos * (lin * pj4 * (1 - 0.5 * (1 - 1 / 1.43)) + f8 * 2 * pj4 + f4a * pj4) / tok
    wbytes = L * (m.touched(M, B_mu * pos) * m.b_exp(M) + m.b_dense(M))
    if kind == "gpu":
        e_w = wbytes * 8 * 3.5e-12 / (B_mu * tok)
        e_kv = m.kv_read(M, C) * 8 * 3.5e-12 / tok
        e_l = pos * L * m.a2a(M) * 71 / 72 * 8 * 5e-12 / tok
    else:
        e_w = wbytes * 8 * 0.15e-12 / (B_mu * tok)
        e_kv = m.kv_read(M, C) * 8 * 3.5e-12 / tok
        e_l = pos * L * (M["hid"] * 2 / 3 + 2 * M["hid"]) * 8 * 5e-12 / tok
    return e_c * 1e3, e_w * 1e3, e_kv * 1e3, e_l * 1e3
for t in (200, 1000, 1500):
    c = r.cont(r.CONT5); q = c[t][3]
    g = r.rub(1.43, 10e-6); qg = g[t][3]
    ec = energy("cont", q[2], c[t][1], 0.04e-12)
    eg = energy("gpu", qg[2] // qg[3][1], g[t][1], 0.05e-12)
    print(f">={t}: Continuum-5 k={c[t][1]} compute {ec[0]:.2f} weights {ec[1]:.2f} KV {ec[2]:.2f} link {ec[3]:.2f} = {sum(ec):.2f} mJ/token"
          f" | Rubin k={g[t][1]} compute {eg[0]:.2f} weights {eg[1]:.2f} KV {eg[2]:.2f} link {eg[3]:.2f} = {sum(eg):.2f} mJ | ratio {sum(eg)/sum(ec):.2f}")
