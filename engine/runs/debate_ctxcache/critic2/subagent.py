# Live-context lever: delegate exploration calls to a sub-agent with a fresh context (shared, cached system prompt),
# parent receives only an S-token summary. Append-only everywhere (all re-sent tokens hit), anth5m prices.
W, Rd = 1.25, 0.10
def session(calls=50, block=5, deleg=0, S=500, sys=10_000, tool=2300, task=300):
    # parent: per block, (block-deleg) own calls + (1 delegation round-trip appending task+S if deleg)
    c, L = W * sys, sys; reads = 0
    nb = calls // block
    for _ in range(nb):
        parent_steps = [tool] * (block - deleg) + ([task + S] if deleg else [])
        for a in parent_steps: c += Rd * L + W * a; L += a
        if deleg:                          # sub-agent: sys read from cache, then deleg calls + final summary
            l = sys
            for a in [task] + [tool] * deleg:
                c += Rd * l + W * a; l += a
            c += Rd * l + W * S            # summary generation request (output ~ billed as write of S here)
    return c, L
b, Lb = session()
print(f"no delegation: {b:,.0f} units, final parent ctx {Lb:,}")
for d, S in ((2, 300), (4, 500), (4, 1000), (4, 2000)):
    x, L = session(deleg=d, S=S)
    print(f"delegate {d}/5 calls, summary {S}: {x:,.0f} ({x/b-1:+.1%}), final parent ctx {L:,}")
for calls in (100, 200):
    b, _ = session(calls=calls); x, _ = session(calls=calls, deleg=4, S=500)
    print(f"{calls} calls, no window: delegate 4/5 S=500 {x/b-1:+.1%}")
