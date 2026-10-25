"""Blend decode with prefill: 2K new prefill tokens per 1K output (agentic turn, 128K cached prefix)."""
import model as m
PRE = 2.0 * (m.LIN_FLOPS + m.attn_flops(m.CTX))   # prefill FLOPs per output token (2 new in / 1 out)
def pre_rate(F4, P, eta=0.6): return F4 * eta / P / PRE * 1e6
for name, dec, F4, P in [("Rubin tau15", m.best(m.gpu_points(m.GPU["Rubin NVL72"], 15e-6)), 35e15, 220e3/72),
                         ("Continuum tau3", m.best(m.pipe_points(m.CONT, 3e-6)), 24e15, 2100)]:
    pr = pre_rate(F4, P)
    print(name, f"prefill-only {pr/1e6:.1f}M out-tok/s/MW;", " ".join(
        f"{t}:{(1/(1/d[1]+1/pr))/1e6:.1f}M" if d else f"{t}:--" for t, d in zip(m.TIERS, dec)))
