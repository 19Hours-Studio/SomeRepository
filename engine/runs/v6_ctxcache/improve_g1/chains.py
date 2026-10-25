# Idea 1 (Archetype C chain from eval_g0/c1/gate.py: bill = 0.45 fixed + 0.55 prefill;
# compute % of full prefill: blend full stack 23.2, prefix cache 83, +1 KV load; 8B = 32 layers)
L = 32; probe = 100 / L            # layer-1 full recompute = deviation probe (CacheBlend HKVD step)
eps = 0.01                          # shadow full recompute on 1% of traffic
def ratio(m, fn=0.0, blend=23.2):
    """m = share of requests the probe routes to the exact path; fn = share of true multi-source
    requests it misses (they get blended at reduced quality, cost counted as blended)."""
    exact = 83 + probe              # probe paid, then exact prefix-cache path
    b = blend + 1 + probe * 0       # probe reused as CacheBlend's own layer-1 selection
    c = m * exact + (1 - m) * b + eps * 100
    return 1 / (0.45 + 0.55 * c / 83)
print("I1 old claim (all blended, 23.2%%): %.2fx" % (1 / (0.45 + 0.55 * 24.2 / 83)))
for m in (0.1, 0.2, 0.3, 0.5):
    print("I1 routed share m=%.1f: bill ratio vs prefix caching %.2fx" % (m, ratio(m)))
import math
# break-even m for 1.5x: solve 0.45+0.55*c/83 = 1/1.5
c_need = (1/1.5 - 0.45) * 83 / 0.55
m_be = (c_need - 24.2 - 1) / ((83 + probe) - 24.2)
print("I1 max routed share for 1.5x: %.2f" % m_be)

# Idea 2 on a third-party API (Archetype B ledger: system 1k read 0.1, docs 4k, question 0.2k,
# output 0.3k at 5x; Anthropic multipliers write 1.25 read 0.1); reuse u from i2_order_sim.out
base = 1*0.1 + 4*1.0 + 0.2 + 0.3*5
for name, u in [("hash z1.05", .152), ("pop z1.05", .400), ("pop z1.2", .546), ("pop z1.5", .768)]:
    docs = 4 * (u * 0.1 + (1 - u) * 1.25)
    print("I2 API %-10s doc reuse %.3f: bill ratio vs uncached-docs best practice %.2fx"
          % (name, u, base / (base - 4 + docs)))
# break-even reuse where caching docs beats not caching them: u*0.1+(1-u)*1.25 = 1
print("I2 API break-even doc reuse %.3f" % (0.25 / 1.15))
