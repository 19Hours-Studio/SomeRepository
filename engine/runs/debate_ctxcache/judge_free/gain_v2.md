The answer is careful and honest about what it leaves out, but almost all of its large percentages are measured against weak baselines. Against best current practice (append-only context, parallel tool calls, a sensible cache TTL, clearing old context deeply), the gain it actually supports is small. It comes from synthetic simulations only, with no quality measurement.

**What I did:** I re-ran `round2/sim3.py`, and its output matches `sim3.out` exactly. I then ran extra baselines with a short script; it's in `/tmp/claude-0/sp/chk.py` rather than the session scratchpad, which was my mistake. The per-claim table is in `gain_check.md` in this folder.

**Claim by claim, against best practice:**
- **About 100% hit rate on re-sent tokens:** no gain. Simply appending the new full version (append-only, which coding agents already do) already scores 1.0000 in the answer's own simulation. The hit-rate goal is already met today.
- **Errata, −35.8%:** this is measured against rewriting edited text in place, which is not current practice.
  - Against append-only, the −11% comes entirely from sending a 200-token diff instead of a 2,000-token output. With a 2,000-token diff the saving is +0.0%.
  - Against agents that already return short snippets (300–500 tokens), the saving is only **−0.7% to −2.0%**. Sending diffs is itself prior art.
- **Batching tool calls, −32% to −58%:** the cost effect is real (cost scales with number of requests × live context), but it isn't new.
  - Parallel tool calls are a standard provider feature, and the W&D paper already measured −35.9% on a real model.
  - The size of the gain depends on how much *extra* batching an agent can do, which nobody measured. If the baseline already pairs 50% or 70% of calls, pairing all of them gives −26% or −20%.
  - The effect on output quality was not tested.
- **TTL policy, −16% to −54%:** this is measured against letting the cache expire. The real baseline is simply choosing the provider's 1-hour TTL. Keep-alive pings beat always using the 1-hour TTL in only one case (15-minute gaps before 5% of requests): +11.1% versus +19.5%, about −7%.
- **Provider-side span operations, −17% to −55%:** these savings appear only when old context is cleared shallowly and often.
  - At deep clearing, the cheapest setting by the answer's own admission, they give +4.6% (punch) and −1.0% (patch).
  - The reused KV after a deletion is approximate, quality is untested, and it needs a provider or your own serving stack.
- **Segment cache across users:** this is prior art (CacheBlend, EPIC), and its numbers are taken from those papers.

**What it does well:** it withdraws its earlier artifacts, demotes ideas that turned out to be prior art, and states clearly which cases cannot reach about 100%: brand-new tokens, gaps longer than the TTL, exact output after edits, and cross-user reordering.

Sources:
- [Anthropic parallel tool use docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use)
- [PromptLayer: parallel tool calling](https://www.promptlayer.com/glossary/parallel-tool-calling)
- [W&D parallel tool calling (arXiv 2602.07359)](https://arxiv.org/pdf/2602.07359)

HONEST GAIN: about −1% to −2% API cost against append-only agents that already return short snippets (up to −11% only against agents that re-append full 2,000-token outputs), from client-side diff errata, synthetic and with quality untested; no gain in hit rate, and the other ideas are prior art or show about 0 at cost-optimal settings.