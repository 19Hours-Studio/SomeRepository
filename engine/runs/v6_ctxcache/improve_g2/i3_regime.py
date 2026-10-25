# Idea 3 fix: restrict to the regime where post-expiry rewrites exist, and choose per gap among
# {let expire, 5m ping chain, 1h TTL}. Anthropic multipliers: 5m write 1.25, 1h write 2.0, read 0.1.
# Measured on Mooncake FAST25 traces (improve_g1/i3_ttl_replay.out): f = 0.114 / 0.089, ceiling 1.096x / 1.069x.
import math
P, n = 100.0, 2.0          # k tokens: cached prefix, new tokens per turn (long agent session)
def turn_cost(g, action):
    if action == 'expire':   return 1.25 * (P + n) if g > 5 else 0.1 * P + 1.25 * n
    if action == 'ping':     return 0.1 * P * max(0, math.ceil(g / 5) - 1) + 0.1 * P + 1.25 * n
    if action == '1h':       return 0.75 * P * (1/12) * 0 + (0.1 * P + 2.0 * n if g <= 60 else 2.0 * (P + n))
for g in (4, 8, 12, 20, 40, 55):
    c = {a: turn_cost(g, a) for a in ('expire', 'ping', '1h')}
    best = min(c, key=c.get)
    print("gap %2d min: expire %.1f ping %.1f 1h %.1f -> best %s, %.2fx vs plain 5m"
          % (g, c['expire'], c['ping'], c['1h'], best, c['expire'] / c[best]))
# 1h TTL premium: 0.75 x (tokens written) once; ping chain costs 0.1P per 5 min -> ping cheaper while
# ceil(g/5)-1 pings * 0.1P < 0.75 * n_written ... with whole prefix written once at 1h: 0.75P => 7.5 pings (~40 min)
print("ping vs 1h crossover when the whole prefix must be re-written at 1h: %.1f pings ~ %.0f min" % (0.75 / 0.1, 5 * (0.75 / 0.1 + 1)))
# Session input bill vs share s of turns that come back after a 5-60 min gap (avg 1.5 pings each),
# plus waste of 0.5 ping per return on sessions that do not come back (hazard threshold 0.08).
hit = 0.1 * P + 1.25 * n; miss = 1.25 * (P + n)
for s in (0.05, 0.1, 0.2, 0.3, 0.5):
    plain = (1 - s) * hit + s * miss
    rule = hit + s * (1.5 + 0.5) * 0.1 * P
    print("share of post-gap turns s=%.2f: input bill ratio %.2fx" % (s, plain / rule))
for target in (1.5, 3.0):
    # plain/rule = target -> solve for s
    s = (target * hit - hit) / (miss - hit - target * 2.0 * 0.1 * P)
    print("s needed for %.1fx on input: %.3f" % (target, s))
