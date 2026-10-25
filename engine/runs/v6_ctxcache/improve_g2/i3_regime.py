# Idea 3 fix: per-session TTL switch priced from the return hazard. Per turn, input cost in units of k tokens.
# Anthropic multipliers: 5m write 1.25, 1h write 2.0 (premium 0.75 on every written token), read 0.1.
# s = share of turns arriving after a 5-60 min gap; P = cached prefix, n = tokens written per turn.
# Ping chain: avg 1.5 pings per returning gap + 0.5 wasted ping per return (hazard threshold 0.08).
# Trace check (improve_g1/i3_ttl_replay.out, Mooncake FAST25): f = 0.11/0.09, blanket 1h = 0.73x, ceiling 1.07-1.10x.
def strategies(P, n, s):
    hit, miss = 0.1 * P + 1.25 * n, 1.25 * (P + n)
    plain = (1 - s) * hit + s * miss
    h1 = hit + 0.75 * n                      # every write pays the 1h premium; gaps <= 60 min all hit
    ping = hit + s * 2.0 * 0.1 * P
    return plain, h1, ping
print("rule: use 1h TTL when s > s* = 0.75n / (1.15P)")
for P, n in ((100, 2), (100, 10), (20, 10), (8, 4)):
    sstar = 0.75 * n / (1.25 * (P + n) - 0.1 * P - 1.25 * n)
    for s in (0.0, 0.02, 0.1, 0.3):
        pl, h1, pg = strategies(P, n, s)
        best = min(pl, h1, pg)
        print("P=%3dk n=%2dk s=%.2f: plain %.1f | 1h %.1f | ping %.1f | adaptive vs plain %.2fx, vs blanket-1h %.2fx  (s*=%.3f)"
              % (P, n, s, pl, h1, pg, pl / best, h1 / best, sstar))
