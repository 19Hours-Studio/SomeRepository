# Exact cost arithmetic for the ideas. Prices as multiples of base input price (Anthropic: read 0.1, write5m 1.25, write1h 2.0).
import random
R, W5, W1 = 0.1, 1.25, 2.0
N = 100_000  # cached context tokens

print("== 1. API cost of one mid-context edit (edit e=200 tok at uniform position) ==")
e = 200
inplace = sum(p*R + (N-p+e)*W5 for p in range(0, N, 100)) / (N/100)
erratum = N*R + (e+30)*W5   # append erratum (+30 tok framing)
cached_turn = N*R
print(f"in-place edit turn  : {inplace/1e3:8.1f}k units ({inplace/cached_turn:.2f}x a fully cached turn)")
print(f"erratum-append turn : {erratum/1e3:8.1f}k units ({erratum/cached_turn:.2f}x)")
print(f"saving per edit event: {inplace/erratum:.2f}x")

print("\n== 2. Ski-rental rebase vs always-erratum vs always-inplace (simulation) ==")
def sim(policy, turns=200, p_edit=0.2, seed=0):
    rnd = random.Random(seed); cost = 0; extra = 0; earliest = N; acc = 0
    for t in range(turns):
        cost += N*R + extra*R + 500*W5      # read + new user/tool tokens appended
        if rnd.random() < p_edit:
            p = rnd.randrange(N)
            if policy == "inplace":
                cost += (N-p)*(W5-R)
            else:
                extra += e+30; cost += (e+30)*W5; earliest = min(earliest, p)
        acc += extra*R
        if policy == "ski" and extra and acc >= (N-earliest)*(W5-R):
            cost += (N-earliest)*(W5-R); extra = 0; acc = 0; earliest = N
    return cost
base = sim("inplace")
for pol in ["inplace", "erratum", "ski"]:
    c = sim(pol); print(f"{pol:8s}: {c/1e6:7.2f}M units  ({base/c:.2f}x cheaper than in-place)")
ideal = 200*(N*R+500*W5)
print(f"lower bound (no edits ever): {ideal/1e6:.2f}M")

print("\n== 3. TTL: keepalive pings (5-min TTL) vs 1-h write ==")
for gap in [4, 10, 20, 30, 40, 50, 59]:
    pings = gap // 5 if gap % 5 else gap//5 - 0   # one ping per <5 min window before return
    pings = max(0, (gap-1)//4)                     # ping every 4 min to be safe
    k = pings*R*N; h = (W1-W5)*N; miss = (W5-R)*N
    print(f"gap {gap:2d} min: keepalive {k/1e3:6.1f}k  | 1h-TTL extra {h/1e3:5.1f}k | let-expire re-write {miss/1e3:6.1f}k")

print("\n== 4. Own-stack compute: tokens recomputed per edit (uniform position) ==")
for name, frac in [("prefix cache only", 1.0), ("CacheBlend 15%", .15), ("edit-local repair 5%", .05), ("edit-local repair 2%", .02)]:
    print(f"{name:22s}: recompute {0.5*frac*100:5.1f}% of context -> {1/(0.5*frac):5.1f}x less prefill than full, {1/frac:4.1f}x less than prefix caching")

print("\n== 5. Storage ==")
kv = 80*8*128*2*2   # Llama-3-70B BF16 bytes/token
idx = 4*8*3         # 4 sampled layers x top-8 source blocks x 3 B (block id 2B + uint8 mass)
print(f"KV/token {kv/1024:.0f} KiB; dependency index {idx} B/token = {idx/kv*100:.3f}% overhead")
print(f"100k-token context KV: {kv*N/2**30:.1f} GiB BF16")
# FLOPs: linear vs attention per recomputed token for 70B
lin = 2*70e9; att_per_ctx = 4*80*8192
print(f"attention FLOPs equal linear FLOPs at ctx = {lin/att_per_ctx/1e3:.0f}k tokens")
