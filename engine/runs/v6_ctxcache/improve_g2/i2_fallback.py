# Idea 2 fix: the probe's exact fallback no longer pays full relevance-order prefix caching (83% of prefill);
# flagged requests are re-sent in popularity-first order, so their exact path gets the higher exact reuse.
# Chain model from improve_g1/chains.py: bill = 0.45 fixed + 0.55 prefill; blend 23.2 + 1 KV load,
# probe = 100/32 (layer-1 of an 8B, 32-layer model), 1% shadow full recompute, prefix-cache path = 83.
# Exact-path prefill under popularity order relative to relevance order: pf from improve_g1/i2_order_sim.out
# (0.736 / 0.630 / 0.450 at Zipf 1.05 / 1.2 / 1.5; self-hosted, unbounded tree).
L = 32; probe = 100 / L; eps = 1.0
pf = {1.05: 0.736, 1.2: 0.630, 1.5: 0.450}
bill = lambda c: 0.45 + 0.55 * c / 83
def cost(m, exact):
    return m * (exact + probe) + (1 - m) * (23.2 + 1) + eps
for z, f in pf.items():
    pop_exact = 83 * f
    b_plain, b_pop = bill(83), bill(pop_exact)          # baselines: APC relevance order; APC + popularity order
    for m in (0.1, 0.25, 0.4):
        old = b_plain / bill(cost(m, 83))
        new = b_plain / bill(cost(m, pop_exact))
        vs_pop = b_pop / bill(cost(m, pop_exact))
        print("zipf %.2f m=%.2f: old %.2fx | new vs APC %.2fx | new vs APC+pop-order %.2fx" % (z, m, old, new, vs_pop))
    # largest m keeping >=1.5x vs plain APC
    c_need = (1 / 1.5 - 0.45) * 83 / 0.55
    mbe = (c_need - eps - 24.2) / (pop_exact + probe - 24.2)
    print("   max m for 1.5x vs APC: old 0.12 -> new %.2f" % mbe)
