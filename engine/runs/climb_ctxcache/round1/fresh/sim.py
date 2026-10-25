# Cost-scheduled observation masking vs append-only / errata / in-place edits.
# Billing: each turn the whole context is sent; the longest prefix identical to the previous
# request is billed at R (cache read), the rest at W (base price or cache write).
# Output tokens are not counted (the same for all policies only if masking does not change behaviour).
import json, math, random, statistics as st, sys, itertools

PRICES = {"anthropic": (1.25, 0.10), "openai": (1.00, 0.10)}
STUB = 15          # "Old environment output: (N lines omitted)" ~ 15 tokens

class Ctx:
    _ids = itertools.count()
    def __init__(s, prompt):
        s.seg = [[next(s._ids), prompt, False, False]]     # id, tokens, is_obs, masked
        s.prev = []
    def add(s, tok, obs):
        s.seg.append([next(s._ids), tok, obs, False])
    def total(s): return sum(x[1] for x in s.seg)
    def bill(s, W, R):
        hit = 0
        for i, x in enumerate(s.seg):
            if i < len(s.prev) and s.prev[i] == x[0]: hit += x[1]
            else: break
        tot = s.total(); s.prev = [x[0] for x in s.seg]
        return hit, tot, R*hit + W*(tot-hit)
    def unmasked_obs(s): return [i for i, x in enumerate(s.seg) if x[2] and not x[3]]
    def mask_all_but(s, n):
        idx = s.unmasked_obs()
        for i in idx[:max(0, len(idx)-n)]:
            x = s.seg[i]; x[0] = next(s._ids); x[1] = min(x[1], STUB); x[3] = True
    def stale(s, n):                         # observations a mask now would elide
        idx = s.unmasked_obs(); return idx[:max(0, len(idx)-n)]

def run(steps, prompt, policy, W, R, n=5, K=1, edits=None, trigger=100_000, keep=3, at_least=20_000):
    """steps: list of (assistant_tok, obs_tok). edits: dict turn->(entry_frac, erratum_tok, mode)."""
    c = Ctx(prompt); acc = 0.0; H = T = C = 0; peak = 0
    for t, (a, o) in enumerate(steps):
        if edits and t in edits:
            frac, e, mode = edits[t]
            k = 1 + int(frac*(len(c.seg)-1))
            if mode == "inplace": c.seg[k][0] = next(c._ids)
            else: c.add(e, True)                               # erratum, maskable like a tool result
        # ---- masking decision before sending ----
        if policy == "poll":
            if len(c.unmasked_obs()) > n + K - 1: c.mask_all_but(n)
        elif policy == "balance":                              # ski-rental: rent (stale reads) until = buy (rewrite)
            st_ = c.stale(n)
            if st_:
                acc += R*sum(c.seg[i][1]-STUB for i in st_)
                ss = set(st_)                                   # tokens re-written if we mask now,
                suffix = sum(STUB if i in ss else c.seg[i][1]   # excluding the last turn's new tokens
                             for i in range(st_[0], len(c.seg)-2))  # (those are a write anyway)
                if acc >= (W-R)*suffix: c.mask_all_but(n); acc = 0.0
        elif policy == "clear_tool_uses":                      # Anthropic-style trigger/keep/clear_at_least
            if c.total() > trigger:
                gain = sum(c.seg[i][1]-STUB for i in c.stale(keep))
                if gain >= at_least: c.mask_all_but(keep)
        h, tot, cost = c.bill(W, R); H += h; T += tot; C += cost; peak = max(peak, tot)
        c.add(a, False); c.add(o, True)
    return dict(hit=H/T, sent=T, cost=C, peak=peak)

def eoq_K(steps, n, W, R):
    """Closed form: K* = sqrt(2 (W-R) * window_tokens / (R * (obs - stub)))  (economic order quantity)."""
    a = st.mean(x[0] for x in steps); o = st.mean(x[1] for x in steps)
    return max(1, round(math.sqrt(2*(W-R)*n*(a+o)/(R*max(1, o-STUB)))))
