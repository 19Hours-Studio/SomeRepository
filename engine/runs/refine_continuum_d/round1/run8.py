"""Lever ladder for Continuum-8 vs Rubin (as shipped and with symmetric host trim). Usage: python3 run8.py > run8.txt"""
import model8 as e8
q = e8.q
L = ("0.55V wt", "0.60V wt", "0.65V wt", "0.55V", "0.60V")
H = " " * 52 + " ".join(f"{t:>6}" for t in q.T)
for ctx in (q.C128, q.C1M):
    R0 = e8.gpu_env(e8.rubin_prof(0), ctx); R150 = e8.gpu_env(e8.rubin_prof(150), ctx); R250 = e8.gpu_env(e8.rubin_prof(250), ctx)
    print(f"\n== {ctx//1024}K p=0.8"); print(H)
    print(f"{'Rubin as shipped':<52}" + e8.fmt(R0)); print(f"{'Rubin host-trimmed 150 W (symmetric rule)':<52}" + e8.fmt(R150))
    ladder = [
        ("1 per-layer stages, uniform 4-HBM pkgs, imb 1.12", dict(hs_csa=(4,), hs_hca=(4,), idx_opts=(False,), hca_sram_opts=(False,), imb_fixed=1.12)),
        ("2 + hot-expert replicas (imb 1.07 if room)", dict(hs_csa=(4,), hs_hca=(4,), idx_opts=(False,), hca_sram_opts=(False,))),
        ("3 + HCA KV in W-tier, HCA pkgs without HBM", dict(hs_csa=(4,), hs_hca=(0, 4), idx_opts=(False,))),
        ("4 + CSA indexer keys in W-tier", dict(hs_csa=(4,), hs_hca=(0, 4))),
        ("5 + CSA HBM stacks 2/3/4 (= Continuum-8)", dict()),
    ]
    for lab, kw in ladder:
        A = e8.c8_env(e8.C8, e8.C8_PARTS, ctx, labels=L, **kw)
        print(f"{lab:<52}" + e8.fmt(A) + "   max %.0f" % A["max"])
        print(f"{'   / Rubin shipped | / trimmed150 | / trimmed250':<52}" + e8.rat(A, R0) + " |" + e8.rat(A, R150) + " |" + e8.rat(A, R250))
    for t in q.T:
        d = A[t][1]
        print(f"   >={t}: {d['lab']} k{d['k']} m{d['m']} b{d['b']} CSA(g,h,idx,kv)={d['C']} HCA={d['H']} MTP={d['Mt']} pkgs {d['npk']} "
              f"stacks {d['stacks']} users {d['users']:,} {d['spd']:,.0f} tok/s/user T {d['T']*1e6:.1f} us stage c(us)="
              + "/".join(f"{x*1e6:.1f}" for x in d['c']) + f" avg slot {d['W']/d['npk']:.0f} W")
