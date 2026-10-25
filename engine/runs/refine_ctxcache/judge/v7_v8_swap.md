**Answer A is clearly better.** The two share most of their content: the references rewrite, batched clearing, cache-stable layout with errata, splicing, the segment cache and retention pricing. The difference that matters is the self-hosted runner claim.

**B's runner claim does not hold up.**
- B's headline runner result is 0.556× of GPU time, presented as exact. It rests on B's own capped suffix drafter, measured against a default stack.
- B treats the draft-length cap as a contribution.
- A replays the official Arctic Inference suffix-decoding code that vLLM imports. That code reaches 3.22 tokens per pass, against 2.46 for the home-made drafter, and comes out 1.07× better than the capped version.
- A therefore withdraws that contribution. The honest exact runner gain is about 0.88× (references only).
- Someone acting on B would expect about a 44% GPU saving from a method that underperforms an off-the-shelf vLLM config. They would also credit the saving to the wrong component.

**A's sparse-attention idea is a real addition with honest limits.**
- A adds sparse attention over the cached KV (Quest, RocketKV, HiSparse) and reports when it helps: little on short SWE-bench sessions, about 0.53–0.6× at long context.
- A notes that this gain needs sparse prefill over the cache, not just sparse decode.
- A gives a concrete quality-test plan: teacher-forced top-1 agreement and KL, binned by context length, plus a 1% shadow-recompute gate.
- A flags that no training-free result exists yet on agent tasks.
- A's batching of read-only calls is a modest extra lever and is labelled as an upper bound.

**Where B is stronger.** B gives more detail on speculation mechanics and on MTP. That detail is built on the baseline A has shown to be unfair.

WINNER: A
MARGIN: clearly
WHY: B's main self-hosted result (0.556× exact GPU time, crediting a capped custom drafter) is measured against a weak baseline. A shows the official vLLM/Arctic suffix decoder beats that drafter, so the honest exact runner gain is about 0.88×. A replaces the withdrawn claim with a properly benchmarked sparse-attention lever, says when it helps and how to test its quality, and keeps all of B's valid client-side content.