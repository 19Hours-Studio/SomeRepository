=== CALIBRATION ===

P | 1 | 20% | Has the fewest broken numbers: the 40-turn figure of 1.48× reproduces at about 1.42×. It is mostly prior art, though (Programmatic Tool Calling, CodeAct, parallel calls), so it gains only about 1.1× over best practice. It only lowers cost and does nothing for middle edits or reordering.

P | 3 | 15% | Placing the ledger after the breakpoint is sound, and folding after TTL expiry costs nothing. But the depth-1 claim is false in agent loops, the headline $ figures don't reproduce, and it gains only about 1.0–1.3× over tail-state or patch-chain practice.

P | 2 | 10% | The ski-rental "≤2× OPT" guarantee is broken, because the buy price keeps growing (about 3.2× OPT and unbounded). It scores 0.95× against an append-only patch chain, and the 2.66× figure can't be reached on OpenAI pricing.

P | 4 | 10% | This is the only candidate that targets middle edits and reordering, but it has an unanswered FATAL defect: the audit can't certify ≤2% flips within the stated window. Once audit cost is included it is about 1.0× CacheBlend, and it can't run on hosted APIs.

P | none | 45% | No candidate gets close to 100% hit rate on reordered or mid-edited prefixes on hosted APIs. All the price gains shrink to about 1.0–1.1× against real best practice. The best answer is probably a combination: client-side canonical ordering, append-only edits and tail-placed state, plus CacheBlend-class reuse on your own serving stack.

WEAKEST LINK: Idea 1 assumes most calls after the threshold are foldable, and that the gain survives against the true baseline. With only 50% of calls foldable, the gain drops to 1.18–1.50×. Programmatic Tool Calling plus parallel calls already captures most of the folding and filtering.

FLIP TEST: Replay real long agent traces (40 and 150 turns) under three setups: Programmatic Tool Calling plus parallel calls, the same plus Idea 1's context-length gate, and Idea 3's ledger. | If the gate adds less than 1.05× cost reduction over Programmatic Tool Calling, or if fewer than 40% of post-threshold calls are read-only or idempotent, Idea 1 falls below Idea 3 or below "none". If Idea 3 beats tail-placed state by more than 1.3× without hurting accuracy on the latest values, Idea 3 leads.

UNKNOWN: Even if Idea 1 is right, it leaves the core question open. No candidate shows how to get close to 100% cache hits for reordered documents or changed middle tool outputs on hosted APIs without provider-side approximate KV reuse. None has measured the quality cost of such reuse on models of 70B or larger.