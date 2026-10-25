The answer shows no real gain over current best practice. Its only measured result, a 40% lower input bill, is measured against a baseline that best practice already avoids. The parts that are actually new show no gain, or were never tested.

**What I checked:** I reran `baseline/calc.py`, and every number in the answer reproduces exactly (cache-hit rate 92.9% → 99.75%, billed input 604k → 365k units, the KV sizes and the cost per million tokens). I then wrote `replay_check.py`, which reruns the same replay against a fair baseline and varies its settings, and searched for prior art. The full write-up is in `verdict.md`.

**Idea 1 (append corrections at the end, with a rule for when to rewrite):**
- **The −40% is measured against a weak baseline.** It compares appending corrections at the end with editing earlier content in place. In-place editing is the documented mistake. Manus's guidance already says to keep the context append-only, keep the prefix stable and serialize deterministically, and normal agent loops already add a re-read file as a new tool result at the end. So appending is current practice, not a new gain.
- **The new part never helps.** The only new element is the ski-rental rule for when to rewrite. In my sweeps (50 or 200 turns, an edit every 2 or 5 turns, corrections of 1,000 or 2,300 tokens) it triggered zero times, so the results with and without it are identical. It triggered only with an edit on every turn for 200 turns, and then the cost went slightly up (9,885,645 vs 9,880,355 units).
- **The −40% depends on the random seed.** Across 200 seeds the saving ranges from 24% to 56%.
- **Sorting documents by hash only helps a pure reorder.** It makes a reordered but otherwise identical document set an exact match. An inserted document lands at a random position, so on average about half the document block is recomputed. Dropping the relevance order is also an untested risk to answer quality.
- **The quality risk is untested.** Nothing checks whether stale text sitting next to its correction confuses the model.

**Idea 2 (deleting a span from the cache without recomputing):**
- This is the mechanism llama.cpp already uses to shift its context, which the answer itself cites.
- The "12.5x cheaper" figure is just the ratio of Anthropic's two prices (1.25 / 0.10), not a measurement.
- The output differs from full recomputation, and that quality effect is not measured.

**Idea 3 (caching each document separately and recomputing a few tokens):**
- This is CacheBlend / EPIC / LMCache, and every number comes from those papers.
- A newer paper, [AgentKVShift](https://neurips.cc/virtual/2026/poster/155404) (NeurIPS 2026), reports near full-recomputation quality while refreshing only 10–30% of the cache. That is comparable or better prior art.
- The "deviation gate" the answer adds is untested.

**Idea 4 (pricing the cache by storage time rather than per token):**
- The arithmetic is correct, but two things are missing. At 100k-token contexts, attention roughly doubles the recompute cost. Loading a 100k-token 70B context from an SSD at about 7 GB/s takes about 4.7 s, not the PCIe speed the answer assumes.
- Gemini's explicit context caching already charges for storage per token-hour (reported at about [$4.50 per million tokens per hour](https://verdent.ai/guides/gemini-3-1-pro-pricing) for Pro). Tiered, cost-aware storage already exists in AttentionStore, Mooncake and LMCache. Nothing here is measured.

**The cases the answer says cannot reach about 100%** (middle insertions and substitutions without quality loss) are stated honestly. But none of its ideas improves those cases beyond existing work.

Sources:
- [Manus: Context Engineering for AI Agents](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- [Manus context engineering summary](https://agentic-ai.readthedocs.io/en/latest/ContextEngineering/manus/)
- [Anthropic context editing docs](https://docs.claude.com/en/docs/build-with-claude/context-editing)
- [AgentKVShift (arXiv)](https://arxiv.org/pdf/2607.21604)
- [AgentKVShift (NeurIPS 2026)](https://neurips.cc/virtual/2026/poster/155404)
- [Gemini 3.1 Pro pricing](https://verdent.ai/guides/gemini-3-1-pro-pricing)
- [Gemini context caching](https://fast.io/resources/gemini-context-caching/)
- [Google forum: context caching pricing](https://discuss.google.dev/t/peculiar-pricing-of-context-caching-and-potential-plans-for-prefix-caching-support/194137)

HONEST GAIN: none