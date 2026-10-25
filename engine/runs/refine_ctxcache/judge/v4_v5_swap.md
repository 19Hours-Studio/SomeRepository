Both answers propose the same four ideas: cache-stable layout, KV splicing, a gated segment cache, and retention pricing. The difference is how solid the evidence behind their numbers is.

**Answer A** replays 42 real SWE-agent sessions and corrects several numbers that B relies on:
- **Clearing saving.** Clearing old tool results saves 0.79×, not 0.43×. Real observations are about 159 tokens, not 2,000.
- **Baseline.** The fair baseline is the 97% hit rate that real agent traffic already gets. B's 47% "authoring order" figure is a strawman.
- **Rolling masking.** The published rolling observation masking costs 2.01× once prompt caching is in place. Applying it in batches brings that to 0.90×, while still showing at least as much context as the rolling window does.
- **Period rule.** The square-root (EOQ) clearing period predicts 9 steps, and the real-trace replay's best is also 9.
- **Server-side cost.** A roofline model shows that most of the remaining GPU cost is decode-time reads of the KV cache, not misses.

A also admits that its "novel" rules are textbook results (exchange argument, EOQ, ski rental). It explains the breakpoint placement needed to make batched clearing work on Anthropic. It says plainly that 0.2–0.4× is out of reach on typical sessions.

**Answer B** is more readable in places and gives more detail on the layout tricks. However, it claims a 0.43× bill from a synthetic model, bases its hit-rate gains on a strawman baseline, and presents known results as new. Someone acting on B would expect savings that A's real-trace replay shows do not materialise.

WINNER: A
MARGIN: clearly
WHY: A tests its claims against real agent traces and corrects the inflated synthetic figures that B relies on (0.43× becomes 0.79×; the 47% baseline becomes 97%). It also finds a concrete, actionable result: rolling masking doubles the bill under caching, and batching fixes it. It is more honest about prior art and about what cannot be achieved, so acting on A gives realistic expectations and better decisions.