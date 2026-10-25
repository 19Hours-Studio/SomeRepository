"""Design sweep for Continuum-9 (EP split): W-tier provisioned fraction omega x link lanes. Usage: python3 sweep9.py > sweep9.txt"""
import model9 as e9
q = e9.q
R = e9.e8.gpu_env(e9.e8.rubin_prof(150), q.C128)
print("Rubin trimmed 150 W, 128K:", e9.e8.fmt(R))
for o in (1.0, 0.9, 0.8, 0.7):
    for l in (64, 56, 48, 40):
        A = e9.env(q.C128, omega=o, lanes=l)
        print(f"omega {o:.2f} lanes {l}: {e9.e8.fmt(A)} | ratio {e9.e8.rat(A, R)} | >=1000: {e9.detail(A[1000][1])}", flush=True)
