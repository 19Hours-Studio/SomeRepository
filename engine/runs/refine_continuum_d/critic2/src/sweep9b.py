"""Continuum-9 design sweep, part 2 (lower omega, more lanes). Usage: python3 sweep9b.py > sweep9b.txt"""
import model9 as e9
q = e9.q
R = e9.e8.gpu_env(e9.e8.rubin_prof(150), q.C128)
for o in (0.7, 0.6, 0.5, 0.4):
    for l in (64, 80, 96):
        A = e9.env(q.C128, omega=o, lanes=l)
        print(f"omega {o:.2f} lanes {l}: {e9.e8.fmt(A)} | ratio {e9.e8.rat(A, R)} | >=1000: {e9.detail(A[1000][1])}", flush=True)
for gm in (14, 10):
    A = e9.env(q.C128, omega=0.7, lanes=64, gmax=gm)
    print(f"omega 0.70 lanes 64 gmax {gm}: {e9.e8.fmt(A)} | ratio {e9.e8.rat(A, R)} | >=1000: {e9.detail(A[1000][1])}", flush=True)
