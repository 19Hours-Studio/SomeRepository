"""Hand check of Continuum-10 pair-stage terms at the 128K >=1000 point and the 1M point (64 lanes, omega 0.7 / 1.0)."""
import model10 as c
q, e8, m, e9 = c.q, c.e8, c.m, c.e9
M = c.M
def show(ctx, omega, G, h, b, k, mm, idx, kv):
    csa, hca, mtp = e8.layer_types(ctx)
    s = e9.design_profiles(h, omega, 64, ("0.55V wt",))["0.55V wt"][0]
    pos, tok, L = m.spec(M, k, 0.8); S = L - 30; users = mm * b * S
    exp_b = M["n_exp"] * m.b_exp(M) / G
    a1, h1 = c._cap(s, csa, G, users, idx, False); a2, h2 = c._cap(s, hca, G, users, False, kv)
    print(f"{ctx//1024}K G={G} h={h} b={b} k={k} m={mm} users={users:,}  slot P={s['P']:.0f} W  F4={s['F4']/1e15:.1f} PF srambw={s['srambw']/1e12:.0f} TB/s link={s['link']/1e12:.2f} TB/s")
    print(f"  SRAM: experts 2x{exp_b/1e9:.2f} + dense 2x{m.b_dense(M)/1e9:.2f} + {a1/1e9:.2f} idx + {a2/1e9:.2f} HCA-KV = {(2*exp_b+2*m.b_dense(M)+a1+a2)/1e9:.2f} of cap {0.9*s['sram']:.2f} GB")
    print(f"  HBM: {(h1+h2)/1e9:.1f} of cap {0.9*h*48:.1f} GB; D(G)={e9.D(G):.2f}")
    for nm, typ, i_, k_ in (("CSA", csa, idx, False), ("HCA", hca, False, kv)):
        t = c._terms(s, typ, G, h, b, pos, 1.07, i_, k_, L)
        print(f"  {nm}: sram {t[0]*1e6:.2f} us  hbm {t[1]*1e6:.2f}  compute {t[2]*1e6:.2f}  dispatch/combine {t[3]*1e6:.2f}")
    ho = 1.07 * 8 * b * pos / G * M["hid"] / s["link"]
    cp = c.pair(s, csa, hca, G, h, b, pos, L, users, idx, kv)
    tau = q.tau_f(0.635) if False else q.tau_f(e9.design_profiles(0, omega, 64, ("0.55V wt",))["0.55V wt"][1])
    T = max(mm * cp, cp + 2 * tau)
    print(f"  hand-off {ho*1e6:.2f} us; c_pair {cp*1e6:.2f} us; tau {tau*1e6:.2f}; T = max({mm}x c, c+2tau) = {T*1e6:.1f} us; speed {tok/(S*T):,.0f} tok/s/user")
show(c.q.C128, 0.7, 8, 2, 539, 1, 2, True, False)
show(c.q.C1M, 1.0, 27, 3, 233, 2, 3, True, False)
