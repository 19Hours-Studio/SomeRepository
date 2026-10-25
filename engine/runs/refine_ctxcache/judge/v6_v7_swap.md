A is clearly better: it fixes B's overstated baselines and adds the only client-side saving that keeps every piece of context.

**What A adds over B**
- **A new client-side method that drops nothing.** "Reference, don't repeat" replaces repeated line runs in tool traffic with pointers. On the same traces it cuts the bill to 0.881×.
  - A checks it against the closest prior art, Claude Code's whole-file dedup, which emulates to only 0.993×.
  - It also explains why matching on content avoids that feature's known stale-read bugs.
  - B's API-side savings all come from dropping content.
- **A fairer competitor baseline.** A sweeps Anthropic's context editing fully.
  - It finds a better provider setting (0.868×).
  - It admits that at keep 1 the provider tool already matches client-side batching, so client work adds nothing there.
  - B tested a narrower sweep and stopped at 0.874×.
- **A corrected runner model.** A fixes B's error of counting re-prefill of decoded tokens (prefill share 39% → 32%).
- **Stronger speculation baselines.**
  - B compares speculation only against no speculation and calls it the gain "over current best practice."
  - A compares against vLLM's default `ngram` drafter (0.77× gain) and against MTP-equipped runners (~0.80×).
  - B's headline 0.66× therefore overstates the gain for anyone already using prompt lookup.

**What A and B share**
Both carry the same layout, splice, segment-cache and retention ideas, so A loses nothing relative to B.

WINNER: A
MARGIN: clearly
WHY: A keeps all of B's content and adds a new client-side technique (line-run references) that saves money without dropping any context. It compares this against real prior art. A also corrects B's overstated claims: the incomplete provider-baseline sweep, the inflated prefill share, and speculation measured only against no speculation. Someone acting on A gets more honest gain estimates and one extra, low-risk lever B lacks.