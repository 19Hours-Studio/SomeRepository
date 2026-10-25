"""W-tier clock omega as a per-deployment setting: 1M and 128K envelopes per omega (g <= 14). Usage: python3 om1m.py > om1m.txt"""
from multiprocessing import Pool
import model9 as e9
q, e8 = e9.q, e9.e8
def run(a):
    ctx, o = a
    A = e9.env(ctx, **dict(e9.BASE, omega=o)); R = e8.gpu_env(e8.rubin_prof(150), ctx)
    return f"{ctx//1024}K omega {o}: C9 {e8.fmt(A)} ratio {e8.rat(A, R)} | >=1000 {e9.detail(A[1000][1])}"
if __name__ == "__main__":
    with Pool(2) as p:
        for s in p.imap(run, [(c, o) for c in (q.C1M, q.C128) for o in (1.0, 0.85, 0.7, 0.5, 0.4)]): print(s, flush=True)
