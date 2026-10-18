"""IDEA 4 rounds 2-3: regime where anchor is strongest - warm ice-rich permafrost (foundations 20-25% of capex,
F4 says 20-50% of structure cost), cheap barge hulls ($3,000/t, K), yard pre-commissioning, short life + re-float/re-use."""
def run(fnd_share, hull_cost_per_t, f_float, resid, life, label, capex=500.0, hulls=5, light=2000):
    lab, eq, bulks, ind = 0.30, 0.33, 0.17, 0.10
    eq_ = eq - (fnd_share - 0.10)/2; bulks_ = bulks - (fnd_share - 0.10)/2   # keep total = 1
    s = dict(eq=eq_, bulks=bulks_, lab=lab, fnd=fnd_share, ind=ind)
    hull = hulls*(light*hull_cost_per_t/1e6 + 2.0) + 3.0 + 8.0
    flo = capex*(s['eq']+s['bulks'] + s['lab']*((1-f_float)+f_float*0.4) + s['fnd']*(1-f_float) + s['ind']*0.9) + hull
    mod = capex*(s['eq']+s['bulks'] + s['lab']*(0.4+0.6*0.45) + s['fnd'] + s['ind']*0.95 + 0.03)
    r = 0.12; crf = r/(1-(1+r)**-life)
    cf = (flo - resid*0.6*flo/(1+r)**life)*crf; cm = mod*crf
    k = 0.415/0.585; opex = cm/k
    print(f"{label:58s} capex float {flo:4.0f} vs modular {mod:4.0f} ({100*(1-flo/mod):+.0f}%), delivered ratio {(cf+opex)/(cm+opex):.3f}")
run(0.10, 5000, 0.6, 0.0, 15, "R1 base (cold permafrost, $5k/t hull, no re-use)")
run(0.10, 3000, 0.7, 0.0, 15, "R2 cheap barge hull, 70% floats")
run(0.20, 3000, 0.7, 0.0, 15, "R3 warm ice-rich ground, foundations 20%")
run(0.25, 3000, 0.7, 0.45, 7, "R4 + 7-yr deposit, re-float & re-use (45% residual)")
run(0.25, 3000, 0.8, 0.55, 5, "R5 5-yr deposit, 80% floats, 55% residual")
