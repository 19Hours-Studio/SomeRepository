"""Final comparison table, calibration, energy and prefill blend for Continuum (design B, g=3)."""
import sys, importlib
def load(ctx, mtp):
    sys.argv = ['x', str(ctx), str(mtp)]
    import model2 as m; importlib.reload(m); return m

def table(ctx, mtp):
    m = load(ctx, mtp)
    C = dict(m.CONT, F4=32e15, F8=16e15, P=2450)
    rows = [("Rubin NVL72 tau15", m.gpu_points(m.SYS['Rubin NVL72'], 15e-6)),
            ("Rubin NVL72 tau8", m.gpu_points(m.SYS['Rubin NVL72'], 8e-6)),
            ("Rubin 50PF-dense tau8", m.gpu_points(m.SYS['Rubin (50PF dense)'], 8e-6)),
            ("MI455X tau15", m.gpu_points(m.SYS['MI455X x72'], 15e-6)),
            ("MI455X tau8", m.gpu_points(m.SYS['MI455X x72'], 8e-6)),
            ("TPU 8i tau15", m.gpu_points(m.SYS['TPU 8i x128'], 15e-6)),
            ("TPU 8i tau8", m.gpu_points(m.SYS['TPU 8i x128'], 8e-6)),
            ("Ironwood tau15", m.gpu_points(m.SYS['Ironwood x128'], 15e-6)),
            ("Rubin+LPX tau4", m.afd_points(4e-6)),
            ("CS-4 tau3", m.pipe_points(m.WSE, 3e-6, True)),
            ("Continuum g3 tau8", m.pipe_points(C, 8e-6, gmin=3)),
            ("Continuum g3 tau5", m.pipe_points(C, 5e-6, gmin=3)),
            ("Continuum g2 tau5", m.pipe_points(C, 5e-6, gmin=2))]
    print(f"\n== ctx {ctx:,} MTP={mtp}: output tok/s per provisioned MW (M) at >= tok/s/user ==")
    print(f"{'system':<24}" + "".join(f"{t:>7}" for t in m.TIERS) + "    max")
    res = {}
    for n, pts in rows:
        b = m.best(pts); res[n] = b
        print(f"{n:<24}" + "".join(f"{x[1]/1e6:7.1f}" if x else f"{'--':>7}" for x in b) + f"  {max(p[0] for p in pts):5,.0f}")
    return m, res, C

for ctx in (8192, 131072, 1048576):
    for mtp in (0, 1):
        m, res, C = table(ctx, mtp)

# ---- calibration: GB300 at 8K/1K, MTP on, prefill (8 prompt tokens per output) on same fleet
m = load(8192, 1)
s = m.SYS['GB300 NVL72']
pre = m.prefill_rate(s['F4'], s['F8'], s['P'], 8192)
print("\n== calibration GB300 NVL72, 8K in / 1K out, MTP ==")
for tau in (40e-6, 25e-6, 15e-6):
    for tier, x in zip(m.TIERS, m.best(m.gpu_points(s, tau))):
        if x and tier in (50, 100, 200):
            out = m.blend(x[1], pre, 8.0)
            print(f" tau {tau*1e6:.0f}us tier>={tier}: decode-only {x[1]*s['P']/1e6:,.0f} out-tok/s/GPU; with prefill "
                  f"{out*s['P']/1e6:,.0f} out-tok/s/GPU = {9*out*s['P']/1e6:,.0f} total(in+out)/GPU")
print(" measured (InferenceX, interpolated): ~7.5-9.4k tok/s/GPU at ~50 tok/s/user")

# ---- 128K agentic blend: 2K new prompt tokens per 1K output (cached 128K prefix)
m, res, C = table(131072, 1)
print("\n== 128K MTP, blended with 2 prefill tokens per output token ==")
pr = {"Rubin NVL72 tau15": m.prefill_rate(35e15, 17.5e15, 220e3/72, 131072),
      "Rubin NVL72 tau8": m.prefill_rate(35e15, 17.5e15, 220e3/72, 131072),
      "Rubin 50PF-dense tau8": m.prefill_rate(50e15, 17.5e15, 220e3/72, 131072),
      "MI455X tau15": m.prefill_rate(28e15, 14e15, 230e3/72, 131072),
      "TPU 8i tau15": m.prefill_rate(10.1e15, 5.05e15, 1300, 131072),
      "Continuum g3 tau5": m.prefill_rate(32e15, 16e15, 2450, 131072),
      "Continuum g3 tau8": m.prefill_rate(32e15, 16e15, 2450, 131072)}
for n, p in pr.items():
    print(f"{n:<24} prefill {p/1e6:5.1f}M prompt-tok/s/MW; blended: " + " ".join(
        f"{t}:{m.blend(x[1], p, 2.0)/1e6:.1f}M" if x else f"{t}:--" for t, x in zip(m.TIERS, res[n])))

# ---- operating points + activity energy at 128K MTP
PJ = dict(sram=0.15e-12, hbm=3.5e-12, link=5e-12, fp4=0.04e-12, fp8=0.08e-12)
def eflops(): return m.POS / m.TOK * (m.LIN_FLOPS * PJ['fp4'] + m.attn_flops(m.CTX) * PJ['fp8'])
print("\n== operating points and activity energy, 128K, MTP ==")
for tier in (200, 1000):
    i = m.TIERS.index(tier)
    u, mw, b, N = res["Continuum g3 tau5"][i]
    tps = mw * N * C['P'] / 1e6
    w = m.LAYERS * (m.touched(b * m.POS) * m.B_EXP + m.B_DENSE_LAYER) / (b * m.TOK)
    e = dict(sram=w * 8 * PJ['sram'], hbm=m.kv_read(m.CTX) / m.TOK * 8 * PJ['hbm'], flops=eflops(),
             link=m.LAYERS * 7168 * 2 * 8 * PJ['link'] * 2 / m.TOK * m.POS, static=N * 450 / tps)
    tot = sum(e.values())
    print(f" Continuum tier>={tier}: {u:.0f} tok/s/user, b={b}, users {61*b:,}, pkgs {N}, {tps/N:,.0f} tok/s/pkg, "
          f"{mw/1e6:.1f}M/MW; {tot*1e3:.1f} mJ/tok ({1/tot:.0f} tok/J) " + ", ".join(f"{k} {v*1e3:.1f}" for k, v in e.items()))
    for n in ("Rubin NVL72 tau15", "Rubin NVL72 tau8"):
        x = res[n][i]
        if not x: print(f" {n} tier>={tier}: unreachable"); continue
        u, mw, B, t = x; N = 72; P = 220e3 / 72; tps = mw * N * P / 1e6
        byts = (m.LAYERS * m.touched(B * m.POS) * m.B_EXP + N / t * (m.LAYERS * m.B_DENSE_LAYER + m.B_HEAD) + B * t * m.kv_read(m.CTX)) / (B * m.TOK)
        e = dict(hbm=byts * 8 * PJ['hbm'], flops=eflops(), link=m.LAYERS * m.TOPK * 7168 * 3 * 8 * PJ['link'] / m.TOK * m.POS, static=N * 1000 / tps)
        tot = sum(e.values())
        print(f" {n} tier>={tier}: {u:.0f} tok/s/user, B={B:,}, attn-TP {t}, {tps/N:,.0f} tok/s/GPU, {mw/1e6:.1f}M/MW; "
              f"{tot*1e3:.1f} mJ/tok ({1/tot:.0f} tok/J) " + ", ".join(f"{k} {v*1e3:.1f}" for k, v in e.items()))
