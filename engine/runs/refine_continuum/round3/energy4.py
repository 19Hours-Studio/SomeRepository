"""Activity energy per output token at the best-k operating point, 128K, p=0.8, tau 8us. Also tok/s per HBM stack.
Usage: python3 energy4.py > energy4.txt"""
import envelope3 as e
PJ = dict(sram=0.15e-12, hbm=3.5e-12, link=5e-12, fp4=0.04e-12, fp8=0.08e-12)
def best_op(kind, tier, p=0.8, tau=8e-6):
    top = None
    for k in e.KS:
        m = e.load(131072, k, p)
        if kind == 'C':
            pts = m.pipe_points(dict(m.CONT, F4=32e15, F8=16e15, P=2450), tau, gmin=3)
        else:
            pts = m.gpu_points(m.SYS['Rubin NVL72' if kind == 'R35' else 'Rubin (50PF dense)'], tau)
        ok = [x for x in pts if x[0] >= tier]
        if ok:
            x = max(ok, key=lambda q: q[1])
            if not top or x[1] > top[1][1]: top = (k, x, m)
    return top
for tier in (200, 1000):
    for kind, P, stacks, static in (('C', 2450, 4, 450), ('R35', 220e3 / 72, 8, 1000), ('R50', 220e3 / 72, 8, 1000)):
        k, (u, mw, b, x4), _ = best_op(kind, tier); m = e.load(131072, k, 0.8)
        fl = m.POS / m.TOK * (m.LIN_FLOPS * PJ['fp4'] + m.attn_flops(131072) * PJ['fp8'])
        if kind == 'C':
            N = x4; tps = mw * N * P / 1e6
            w = m.LAYERS * (m.touched(b * m.POS) * m.B_EXP + m.B_DENSE_LAYER) / (b * m.TOK) * 8 * PJ['sram']
            link = m.LAYERS * 7168 * 2 * 8 * PJ['link'] * 2 * m.POS / m.TOK
        else:
            N = 72; t = x4; tps = mw * N * P / 1e6
            w = (m.LAYERS * m.touched(b * m.POS) * m.B_EXP + N / t * (m.LAYERS * m.B_DENSE_LAYER + m.B_HEAD)) / (b * m.TOK) * 8 * PJ['hbm']
            link = m.LAYERS * 7168 * 2 * 8 * PJ['link'] * 2 * m.POS / m.TOK
        kv = m.kv_read(131072) / m.TOK * 8 * PJ['hbm']
        st = N * static / tps
        tot = w + kv + fl + link + st
        print(f"tier>={tier} {kind:<4} k={k} b={b} {u:,.0f} tok/s/user {mw/1e6:.1f}M/MW {tps/N:,.0f} tok/s/pkg "
              f"{tps/N/stacks/1e3:.1f}k tok/s/stack | mJ/tok: weights {w*1e3:.1f} KV {kv*1e3:.1f} FLOPs {fl*1e3:.1f} "
              f"links {link*1e3:.1f} static {st*1e3:.1f} = {tot*1e3:.1f} ({1/tot:.0f} tok/J)")
