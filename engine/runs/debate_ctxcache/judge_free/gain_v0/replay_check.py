# Re-check of the IDEA 1 replay in baseline/calc.py. Same cost model (Anthropic 5m: write 1.25, read 0.10).
import random
W, R = 1.25, 0.10
def session(policy, seed=0, turns=50, sys_tok=10_000, tool=2_000, out=300, edit_every=5, err_tok=1_000):
    rng = random.Random(seed); ctx = [sys_tok]; cost = hit = tot = 0; compactions = 0; debt = 0.0
    for t in range(turns):
        div = sum(ctx)
        if t and t % edit_every == 0:
            k = rng.randrange(1, len(ctx))
            if policy == "inplace":
                div = sum(ctx[:k])
            elif policy in ("append", "append+ski"):   # append-only: erratum / fresh tool re-read at the end
                ctx.append(err_tok); debt += R * err_tok
                if policy == "append+ski" and debt >= W * (sum(ctx) - sum(ctx[:k])):
                    div = sum(ctx[:k]); debt = 0; compactions += 1
        L = sum(ctx); c = min(div, L)
        cost += R * c + W * (L - c); hit += c; tot += L
        ctx.append(tool + out)
    return hit / tot, cost, compactions
print("policy        err_tok edit_every turns | hit    cost      compactions")
for err, ee, T in [(1000,5,50),(2300,5,50),(1000,2,50),(1000,5,200),(2300,1,200)]:
    for pol in ["inplace","append","append+ski"]:
        h,c,n = session(pol, err_tok=err, edit_every=ee, turns=T)
        print(f"{pol:12s} {err:6d} {ee:6d} {T:5d} | {h:.4f} {c:10,.0f} {n}")
    print()
# Seed sensitivity of the -40% headline
import statistics
d=[1-session("append",seed=s)[1]/session("inplace",seed=s)[1] for s in range(200)]
print(f"append vs inplace saving over 200 seeds: mean {statistics.mean(d):.3f}, min {min(d):.3f}, max {max(d):.3f}")
