"""Critic check: V4 uses mHC (hc_mult=4): the residual crossing each pipeline-stage boundary is 4 x hid, not 1 x hid.
HO = hand-off bytes per position in units of hid (model9 uses 1 = one stream at 1 B/elt).
4 = 4 streams FP8 (aggressive), 8 = 4 streams BF16 (normal), 16 = FP32.
Also lets Continuum buy back link lanes (2.25 W/lane/dir, model9's own cost rule)."""
import sys
from multiprocessing import Pool
import model9 as e9
q, e8, m = e9.q, e9.e8, e9.m
M = e9.M
_orig = e9.stage
HO = 1.0
def stage(s, typ, g, h, b, pos, L, users, idx_sram, kv_sram, split="ep", two_phase=False, imb_fixed=None):
    r = _orig(s, typ, g, h, b, pos, L, users, idx_sram, kv_sram, split, two_phase, imb_fixed)
    if r is None or HO == 1.0: return r
    # recompute link term with HO hand-off and take the max again (non-two-phase path)
    exp_b = M["n_exp"] * m.b_exp(M) / g
    room_imb = None
    # imbalance: re-derive exactly as model9
    dense_b = m.b_dense(M); sram_cap = e8.FILL * s["sram"] * 1e9; in_sram = exp_b + dense_b
    if kv_sram: in_sram += users * typ["kvs"] / g
    if typ["idxs"] and idx_sram: in_sram += users * typ["idxs"] / g
    imb = imb_fixed or (q.IMB_G if sram_cap - in_sram >= e8.REP * exp_b else q.IMB_C)
    if e9.IMB_EP: imb = max(imb, e9.IMB_EP)
    lnk = imb * b * pos / g * M["hid"] * (HO + 3 * e9.D(g) * (g - 1) / g) / s["link"] if g > 1 else HO * b * pos * M["hid"] / s["link"]
    return max(r, lnk)
e9.stage = stage
def run(a):
    global HO
    ho, lanes, gmax = a; HO = ho
    A = e9.env(q.C128, **dict(e9.BASE, lanes=lanes, gmax=gmax))
    R = e8.gpu_env(e8.rubin_prof(150), q.C128)
    return f"HO {ho:>4} lanes {lanes:>3} gmax {gmax}: C9 {e8.fmt(A)} ratio {e8.rat(A, R)} | >=1000 {e9.detail(A[1000][1])}"
if __name__ == "__main__":
    jobs = [(1, 64, 14), (4, 64, 14), (8, 64, 14), (16, 64, 14), (8, 96, 14), (8, 128, 14), (8, 96, 20), (8, 128, 20), (16, 128, 14)]
    with Pool(4) as p:
        for s in p.imap(run, jobs): print(s, flush=True)
