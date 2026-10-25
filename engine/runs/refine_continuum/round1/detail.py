"""Operating points, activity-based energy (J/token) and sensitivity for model.py."""
import model as m

PJ = dict(sram=0.15e-12, hbm=3.5e-12, link=5e-12, fp4=0.04e-12, fp8=0.08e-12)

def e_flops(): return m.LIN_FLOPS*PJ["fp4"] + m.attn_flops(m.CTX)*PJ["fp8"]

def e_cont(b, N, tps_total, p_static=450, pj=PJ):
    w = m.LAYERS*(m.touched(b)*m.B_EXP + m.B_DENSE_LAYER)/b
    sram = w*8*pj["sram"]; hbm = m.kv_read(m.CTX)*8*pj["hbm"]
    link = m.LAYERS*7168*2*8*pj["link"]*1.5   # stage hop + intra-pair exchange
    stat = N*p_static/tps_total
    return dict(sram=sram, hbm=hbm, flops=e_flops(), link=link, static=stat)

def e_gpu(B, t, N, tps_total, p_static=1000):
    byts = (m.LAYERS*m.touched(B)*m.B_EXP + N/t*(m.LAYERS*m.B_DENSE_LAYER+m.B_HEAD) + B*t*m.kv_read(m.CTX))/B
    link = m.LAYERS*m.TOPK*(7168 + 7168*2)*8*PJ["link"]
    return dict(hbm=byts*8*PJ["hbm"], flops=e_flops(), link=link, static=N*p_static/tps_total)

def show(tag, d):
    tot = sum(d.values())
    print(f"  {tag}: {tot*1e3:6.1f} mJ/tok -> {1/tot:5.1f} tok/J  [" + ", ".join(f"{k} {v*1e3:.1f}" for k,v in d.items()) + "]")

for tier in (50, 200, 400, 1000):
    print(f"--- tier >= {tier} tok/s/user, ctx {m.CTX}")
    pts = m.pipe_points(m.CONT, 3e-6)
    p = [x for x in pts if x[0] >= tier]
    if p:
        u, mw, b, N = max(p, key=lambda x: x[1])
        tps = mw*N*m.CONT["P"]/1e6
        print(f" Continuum tau3: {u:.0f} tok/s/user, b={b}, users={61*b}, N={N}, {tps/N:,.0f} tok/s/pkg, {mw/1e6:.1f}M tok/s/MW")
        show("energy", e_cont(b, N, tps))
    for tau in (15e-6,):
        s = m.GPU["Rubin NVL72"]
        p = [x for x in m.gpu_points(s, tau) if x[0] >= tier]
        if p:
            u, mw, B, t = max(p, key=lambda x: x[1]); tps = mw*72*s["P"]/1e6
            print(f" Rubin tau15: {u:.0f} tok/s/user, B={B}, TP-attn={t}, {tps/72:,.0f} tok/s/GPU, {mw/1e6:.1f}M tok/s/MW")
            show("energy", e_gpu(B, t, 72, tps))
