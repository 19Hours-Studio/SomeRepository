"""Collective-latency lever, Continuum-10 base: fixed part 7 -> 4 -> 2 us, Continuum only vs both systems (128K)."""
from multiprocessing import Pool
import model10 as c
q, e8 = c.q, c.e8
def run(a):
    cc, both = a
    tf = lambda f, x=cc: (x + 3 / f) * 1e-6
    A = c.env(q.C128, omega=0.7, lanes=72, tau_fn=tf)
    old = q.tau_f
    if both: q.tau_f = tf
    try: R = e8.gpu_env(e8.rubin_prof(150), q.C128); U = e8.gpu_env(e8.ultra4_prof(150), q.C128)
    finally: q.tau_f = old
    return f"collectives {cc} us, {'both systems' if both else 'Continuum only'}: C10 {e8.fmt(A)} /Rubin {e8.rat(A, R)} /Ultra4 {e8.rat(A, U)} (Rubin {e8.fmt(R)})"
if __name__ == "__main__":
    with Pool(2) as p:
        for s in p.imap(run, [(7, False), (4, False), (4, True), (2, True)]): print(s, flush=True)
