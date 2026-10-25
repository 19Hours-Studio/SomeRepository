**A is better.** A and B are the same document, word for word, except for the headline client-side numbers. A's numbers come from the code in `round8/`. B's numbers have been inflated and nothing in the code supports them.

**What I did**
- **Diffed the files.** `A.md` is byte-identical to the run's own `round8/answer.md`. `B.md` differs on only six lines, and every one is a client-side savings figure made larger.
- **Re-ran `calc.py`** (section R). It reproduces A exactly:
  - References at MINRUN 8 / 4 / 2: 0.897× / 0.881× / 0.873× of the bill, with a 97.1% hit rate.
  - The references remove 18.1% of the final context.
  - The prior-art whole-file stub gives 0.993×.
  - References + batched clearing gives 0.720× at keep 10 and 0.625× at keep 3.
- **Checked the saved `calc8_out.txt`** (section V). It shows "references alone x0.881; references + batch up to 3 read-only calls x0.816". That matches A.
- **B's figures appear nowhere in the outputs:** 0.643×, 0.597×, 0.526×, 0.456×, and "41.5% / 52% / 43.4%" of tokens repeated.
- **B also contradicts itself.** For the self-hosted runner it keeps A's 0.884×, even though that number comes from the same reference rewrite.

**What A's real gain is worth.** It is solid but modest, and A says so honestly:
- **Client side (API users):** about a 12% lower bill with no information dropped (0.881×). The best prior art, the whole-file re-read stub, gives only 0.993× on the same traces. Batching read-only calls brings it to 0.816×, but that is an upper bound and changes how the agent behaves.
- **Self-hosted runner:** about 0.884× against a strong baseline (prefix caching, FP8 KV cache and the best setting of vLLM's official suffix decoding). The 0.53–0.6× figures need long contexts and approximate sparse attention, and that approach's quality on agent tasks hasn't been tested.
- **Hit rate:** A correctly points out that plain prefix caching already hits 97% on these traces. So the hit rate isn't the real lever.
- **Limits:** A states that reordered RAG documents can only be reused approximately.

The margin is large because B's version of the main result is overstated about threefold and isn't backed by its own files. Someone acting on B would expect a 36% saving and get about 12%.

My re-run output is in `/tmp/claude-0/-home-user-SomeRepository-engine-runs-freejudge-planted-free/86b61a25-826d-5e99-8ce4-43b0688ac74a/scratchpad/calc_rerun.txt`.

WINNER: A
HOW MUCH BETTER: Clearly better. It is the same answer, but B's headline client-side savings are inflated about threefold (0.643× instead of 0.881×, and 43% instead of 18% of context repeated). They don't reproduce, and they contradict B's own runner figures. A's numbers reproduce exactly.
REAL GAIN A: For API clients, the line-run references cut the bill to about 0.88× (versus 0.993× for the best prior art, Claude Code's re-read stub) with no information lost; batching read-only calls brings it to about 0.82× at best. Self-hosted, about 0.88× of GPU time against the tuned prefix caching + FP8 + suffix decoding baseline. Larger gains need approximate sparse attention at long context, and their quality hasn't been tested.
REAL GAIN B: The same method as A, so really the same roughly 0.88× (about 12%) gain. B's claimed 0.64× / 0.60× / 0.46× figures are not supported by the code.