The measured gain over best current practice is a cost cut of about **4%**, from back-references, and no one has tested whether it hurts output quality. The answer's headline figure for an already append-only agent is −12%. That figure needs batched tool calls that the model in these traces never made, even though it was asked to.

**Reproduction.** I reran `round3/trace4.py` on the downloaded data: 441 real mini-SWE-agent trajectories and the one Claude Opus 4.6 trajectory. The output is byte-for-byte identical to `trace4.out`. The real-trace numbers are real, not invented.

**What each claim is worth:**
- **The ~100% hit target is already met.** On the real traces the baseline sends an unchanged, growing prompt and uses ordinary prefix caching, and it hits 99.4% of re-sent tokens. The answer says so itself. The only open lever is cost, not hit rate.
- **Batching (−5.7% to −8.8%) is mostly not achievable as described.**
  - Parallel tool calls already exist in the APIs and the agent tools, so this is prior art.
  - The harness prompt in these trajectories already says "You can make MULTIPLE tool calls in a single response when the commands are independent", with an example. Even so, all 19,514 responses contain exactly one tool call.
  - The answer's client-side fix ("prompted or enforced") has therefore already been tried in this exact setup and saved nothing. Forcing the model to batch is not specified, and its effect on quality is untested. The batching figure is an upper bound, not an expected saving.
- **Back-references (−3.7%) are the one new measured saving.** They replace lines the agent already showed with a short pointer. The counting rule is conservative. The answer does not cite the closest prior art: observation masking, which hides old tool outputs and cut cost by about 50% against a raw agent on SWE-bench Verified ([Lindenbauer et al. 2025](https://arxiv.org/abs/2508.21433)).
- **Errata (−32.6%) comes from synthetic sessions.** Its baseline edits the prompt in place, which existing guidance already warns against (Manus). Against a fairer baseline that re-shows the whole file, the saving is −9.6%, still synthetic.
- **First-seen document order (−36% to −44%) is synthetic and does not compare like with like.** The final context is 1.8–2.5x larger, so the model sees more documents, including stale ones.
- **Weaker items:**
  - Provider-side deletion and replacement of spans is a simulation only, and saves nothing on the real traces.
  - The selective 1-hour cache-lifetime trick depends on provider behaviour nobody has checked.
  - The operator savings (swapping cache to DRAM between requests, FP8 KV) are prior art.
- **No effect on output quality was measured anywhere.** Every quality section only proposes tests.

The answer is honest about its limits and withdraws its earlier inflated claims. But compared with an agent that already keeps its prompt append-only and uses prefix caching, its supported gain is small.

I wrote these notes to `gain_check.md` in the current folder.

Sources:
- [The Complexity Trap (arXiv 2508.21433)](https://arxiv.org/abs/2508.21433)
- [NeurIPS 2025 listing](https://neurips.cc/virtual/2025/131688)

HONEST GAIN: about −4% of total cost (back-references on real append-only traces, output quality untested); the claimed −12% needs batching that this model did not do even when the prompt asked for it