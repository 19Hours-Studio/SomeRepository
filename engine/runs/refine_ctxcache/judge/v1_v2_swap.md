**A is clearly better.**

**Ordering rule.** This is the crux.
- **B's rule:** B uses Smith's rule (sort by λ/s).
- **A's rule:** A sorts by the odds per token, p/((1−p)·s).
- **Which is right:** When blocks change independently, swapping two neighbours shows that block a should come first exactly when p_a(1−p_b)s_b < p_b(1−p_a)s_a. That is A's rule.
- **What A adds:** A checks this by brute force over 3,000 layouts. The naive rule loses in 59% of them, by up to 17%.
- **What this means for B:** B's rule is only an approximation when change rates are small, and B presents it as the optimum.

**Reproducibility.**
- **B's scripts:** B points to `calc2.py` and `calc3.py`. According to A, these files are not in the directory.
- **A's scripts:** A rebuilt the numbers in a stdlib-only `calc.py`.
- **A's trace replay:** A adds a replay of real SWE-agent trajectories. It shows a non-obvious result: eliding old observations on the client every step costs 1.79× more than doing nothing. A server-side splice reaches 0.62×.

**Prior art and novelty.**
- **B's claims:** B claims popularity ordering for RAG as new.
- **A's correction:** A credits RAGCache, RAGBoost and CacheWeaver for it, and measures how little a greedy radix walk adds on top.
- **Mixed denominators:** B's RAG figures mix two denominators. Its 60–76% is the total hit rate and its 98% counts document occurrences. A separates total from document-only hit rates.

**Extra levers and limits in A.**
- **Cost levers:** OpenAI cache-key sharding to avoid overflow misses, and the formula for measuring the real hit rate.
- **TTL cost:** A quantifies the cost of each TTL choice.
- **Exact-reuse limit:** A states a firm bound. Only layer-0 KV survives an edit in the middle, so exact reuse saves at most about 1/L of the suffix work.

**Where they agree.** The rest is close to equal: ski-rental compaction, the segment cache with a gate, retention break-even, and the overall structure. A also adds a concrete way to calibrate the gate: shadow traffic tuned to ≥99% top-1 agreement.

WINNER: A
MARGIN: clearly
WHY: A replaces B's subtly wrong Smith's-rule ordering with the correct odds-per-token rule and backs it with a brute-force check. It adds a real-trace replay showing that client-side elision every step can raise cost while a server splice lowers it. A is more honest about prior art and keeps total and document-only hit rates apart. B points to scripts that apparently don't exist and claims popularity ordering as new when it is already published.