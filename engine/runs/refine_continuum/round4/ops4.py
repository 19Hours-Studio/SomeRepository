"""Operating points behind the central case (128K, p=0.8). Usage: python3 ops4.py > ops4.txt"""
import model4 as m
for t in (200, 1000):
    c = m.envelope(lambda k: m.pipe_points(m.CONT, 10e-6, 131072, k, 0.8, gmin=3), (t,))[t]
    v, k, u, q = c; d = q[4]; pos, tok, L = m.spec(k, 0.8)
    print(f">={t} Continuum k={k} b={q[2]} users/microbatch, {L*q[2]:,} users/pod, {u:,.0f} tok/s/user, "
          f"{v*2450:,.0f} tok/s/pkg | stage us: " + ", ".join(f"{a} {x*1e6:.1f}" for a, x in d.items() if a != 'g')
          + f" | positions/expert-slice ~{q[2]*pos*6/384:.1f}")
    for n in ("Rubin35", "Rubin50"):
        r = m.envelope(lambda k: m.gpu_points(m.SYS[n], 20e-6, 131072, k, 0.8), (t,))[t]
        v, k, u, q = r; d = q[4]
        print(f">={t} {n} k={k} B={q[2]:,} t={q[3]}, {u:,.0f} tok/s/user, {v*m.SYS[n]['P']:,.0f} tok/s/GPU | step ms: "
              + ", ".join(f"{a} {x*1e3:.2f}" for a, x in d.items()) + f" (incl. {62*20e-3:.2f} ms tau)")
pos, tok, L = m.spec(2, 0.8)
print(f"FLOP inflation (k+1)/E[acc]: k=1 {2/m.spec(1,0.8)[1]:.2f}, k=2 {3/m.spec(2,0.8)[1]:.2f}, k=3 {4/m.spec(3,0.8)[1]:.2f}, k=4 {5/m.spec(4,0.8)[1]:.2f}")
print(f"KV/user @128K {m.kv_store(131072)/1e9:.3f} GB, KV read/step {m.kv_read(131072)/1e6:.0f} MB, attn {m.attn_flops(131072)/1e9:.1f} GF, lin {m.lin_flops(62)/1e9:.0f} GF")
