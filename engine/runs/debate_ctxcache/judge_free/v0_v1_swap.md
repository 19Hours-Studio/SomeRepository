I checked both answers. **A is clearly better.** It is a corrected revision of B: it keeps the same four ideas and fixes real errors that I confirmed by running the code.

**What I checked**
- **B's replay (`vs_ctxcache/baseline/calc.py:14-30`) never charges for new content.** Each turn's 2,000-token tool output plus the 300-token reply is appended after `div = sum(ctx)` is taken. On the next turn those tokens count as cached even though they were never written. That bug produces B's headline figures: 99.75% hit rate and −40% cost.
- **B's ski-rental rule never fires.** The "erratum" and "erratum+ski" runs give the same 364,600 units, so the compaction rule B names its idea after adds nothing.
- **B's hash-order sorting has a real flaw.** When a new document arrives, sorting by hash places it somewhere in the middle and breaks the cache from there. A shows that first-seen order fixes this: 1,000 tokens rewritten per request instead of 6,003.
- **B compares only against a weak baseline**, an agent that rewrites edited content in place. A also compares against an agent that already appends updates. Against that baseline the honest client-side gain is about −3% to −11%, not −40%. A says so openly. That matters for the asker, who might otherwise expect a big saving from a practice they may already follow.
- **A's numbers reproduce exactly** when I re-ran `replay2.py`: −35.8% against in-place editing and −11.0% against appending, with a 100% hit rate on re-sent tokens. A's long-session runs, at equal retained history, show span delete/replace saving −24.5% / −25.8% against appending.
- **Quality and honest limits:**
  - B calls the appended-correction approach "exact KV" with no measured downside. A cites published evidence (PI-LLM) that leaving stale text next to its correction hurts the model more as corrections pile up. It proposes a cap on corrections per segment and gives a testable sample-size plan.
  - A corrects B's 47.5% agent-memory figure: that loss belongs to CacheBlend, while AgentKVShift loses 5.9%.
  - A adds prior art B missed (llama.cpp `--cache-reuse`, Gemini storage pricing).
  - A states plainly that brand-new content caps the total hit rate at about 96%.

**Where B holds up:** both answers share the same core ideas, and B is shorter and lists sources. Its basic storage and recompute arithmetic is fine. Neither answer tested output quality on a real model.

WINNER: A
MARGIN: clearly
WHY: I re-ran both scripts. B's replay never bills new tool output as a cache write, which inflates its 99.75% hit rate and −40% saving, and its ski-rental rule never fires. A fixes both, reproduces exactly, adds the baseline that matters (an agent that already appends updates, where the gain is only 3–11%) and corrects B's hash-order flaw. A also adds published evidence of quality loss from stale text, so its claims are more trustworthy and more useful to the asker.