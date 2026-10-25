"""Feynman proxy (speculative bound, no public spec): 4-die Ultra architecture with compute energy x0.66
(N3P -> A16: x0.8 for N2 [own assumption] x 0.82 for A16 vs N2P [TSMC claims 15-20% lower power]),
and optionally custom HBM with +50% bandwidth at the same power. Compared with Continuum-10 (N2) and with
Continuum-10 ported to A16 (compute energy x0.82)."""
from multiprocessing import Pool
import model10 as c
q, e8 = c.q, c.e8
def fprof(bw=1.0, trim=150):
    u = dict(q.ultra(5690 - trim), P_maxq=5690 - trim); u["hbmbw"] *= bw
    # compute energy x0.66: comp_w 3440 -> 2270 W, slot reduced by SHARE x saving at every V point
    sav = 3440 * 0.34
    pr = q.profiles(dict(u, P=u["P"] - 1.146 * sav, P_maxq=u["P_maxq"] - 1.146 * sav), comp_w=3440 * 0.66, leak_w=300,
                    other_w=0, rack_share=0.83, vendor_maxq=False)
    return pr
def run(a):
    ctx, nm = a
    if nm == "C10":
        A = c.env(ctx, omega=0.7, lanes=72)
    else:
        A = c.env(ctx, omega=0.7, lanes=72, parts_over={"comp_w": 0.82})
    F1 = e8.gpu_env(fprof(1.0), ctx); F2 = e8.gpu_env(fprof(1.5), ctx)
    return f"{ctx//1024:>5}K {nm:<14} {e8.fmt(A)} | /Feynman-proxy {e8.rat(A, F1)} | /Feynman-proxy+cHBM1.5 {e8.rat(A, F2)}"
if __name__ == "__main__":
    with Pool(2) as p:
        for s in p.imap(run, [(x, n) for x in (q.C128, q.C1M) for n in ("C10", "C10 on A16")]): print(s, flush=True)
