import sys
sys.path.insert(0, "/home/user/SomeRepository/engine/runs/refine_continuum_d/round3")
import model10 as c
q, e8, m = c.q, c.e8, c.m
for ctx in (q.C128, q.C1M):
    R = e8.gpu_env(e8.rubin_prof(150), ctx)
    for t in q.T:
        eff, lab, e = R[t]; pt = e[3]
        d = pt[4]
        print(f"{ctx//1024}K >={t}: {eff:.1f} tok/s/W {lab} k={e[1]} spd={pt[0]:.0f} B={pt[2]} (t,m)={pt[3]} mem={d['mem']*1e6:.0f}us comp={d['comp']*1e6:.0f}us link={d['link']*1e6:.0f}us c={d['c']*1e6:.2f} T={d['T']*1e6:.2f}")
    s = [x for l, x, f in e8.rubin_prof(150) if l == R[1000][1]][0]
    print("  slot P at chosen label", round(s["P"]), "kv_store MB/user", round(m.kv_store(m.V4, ctx)/1e6))
