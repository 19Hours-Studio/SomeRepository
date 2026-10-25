I ranked **C1 first, but it's close.** Both answers are solid, their numbers hold up, and neither is very new. C1 wins because it actually tackles the four cases the asker named and measures the quality cost of its approximate method. C2 mostly argues that those cases aren't where the money is.

**What I checked**
- **C1.** I went through the outputs of its billing, quality and cost scripts and compared each headline claim with them. They match:
  - Clearing old tool outputs saves 23–26% of billed input against append-only (the policy the traced agent actually ran). This holds on Anthropic only if extra cache breakpoints are placed; with a single breakpoint at the end it can cost up to 19% more.
  - Its splice (cutting old tool outputs straight out of the stored attention cache on your own serving stack) gives 33–42% fewer GPU-hours.
  - The splice's quality loss (KL 0.006–0.013, top-1 agreement about 98%) is about the same as keeping one more tool output in the prompt. The exact-match sanity checks pass.
- **C2.** I re-ran its copy-speculation script (guessing upcoming output tokens by copying earlier text, then checking them in one pass), and the output was identical: 1.82 and 1.99 tokens per pass. I also read its GPU-time model. It is reasonable: batch of 32, and compute and memory time are added rather than overlapped, which is conservative.
- **Web check of C2's OpenAI claims.** The 24-hour retention option really is the same price as the default. Cache writes being billed from GPT-5.6 on is in Azure's docs. Its "30-minute minimum TTL" isn't backed by any source I found.

**Weaknesses of C1**
- Most of its client-side saving is existing practice. SWE-agent's `polling` setting already gets −23.2%; C1's best setting is only about 3.6% cheaper than that.
- The splice is close to Leyline and llama.cpp's existing cache-editing calls.
- The quality evidence comes from a 135M-parameter model on prompts of about 1.5k tokens.
- It cites an `idea4.out` that isn't in its folder (a copy exists in round 1). It also calls the splice "Idea 3" in one place and "Idea 2" in another.

**Strengths and weaknesses of C2**
- Its best contribution is evidence from 269k real production requests: inside sessions, prompts changed in the middle cost 0% of input, and reuse outside the prefix is only 1–7% of input. That is a useful finding for the asker.
- But its main saving, copy-speculation for 21–34% less GPU time, is well-known prior art (prompt lookup decoding, already built into vLLM). It cuts decode cost rather than making changed prefixes reusable.
- By its own account, its other levers (keeping the reply's cache for the next turn, retention chosen by cost) cover none of the four cases. The one idea that does (Idea 5) has no quality measurement.

Sources:
- [OpenAI prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)
- [Azure prompt caching](https://learn.microsoft.com/en-my/Azure/foundry/openai/how-to/prompt-caching)
- [DEV Community: OpenAI 24h cache](https://dev.to/jangwook_kim_e31e7291ad98/openais-24h-prompt-cache-we-measured-the-real-discount-2c0n)

RANKING: C1 > C2
WHY: I re-ran C2's copy-speculation script (identical output), read its GPU model, checked C1's stored billing, splice-quality and cost outputs against its claims, and checked the OpenAI retention claims on the web. Both hold up and both are mostly prior art. C1 deals directly with the asker's cases (mid-prompt deletion and edits on the API and on an own stack), measures the splice's quality against full recompute and is frank that its client-side gain matches SWE-agent `polling`. C2's main lever is standard prompt-lookup speculation that doesn't touch non-prefix caching, and its one approach covering the asker's cases has no quality measurement. Its production evidence that the non-prefix prize is small is valuable, but it reframes the question more than it answers it.