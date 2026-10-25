# Check of the answer: what gain it actually supports

## Bottom line

The only gain that survives correction is from **Idea A ("references")**. It is exact, works from the client alone, and was measured on real traces against a real prior-art baseline.

- **Bill:** 0.881× of plain prefix caching, or **0.881 / 0.993 ≈ 0.887×** of the best exact prior art the answer emulates (Claude Code's whole-file dedup). That is about **1.13× cheaper**.
- **Evidence type:** a cost-only replay of 42 SWE-agent sessions, using the legacy tokenizer.
- **Quality:** unmeasured.
- **Runner side:** the same mechanism gives about 0.884×, but that number comes from a roofline model, not a measurement.

Every larger figure is either prior art credited as new, an upper bound, approximate with no evidence on agent tasks, or a comparison against a baseline whose behaviour the answer guessed.

## What holds up

- **The framing is sound.** On agent traffic the hit rate is already 97%, so the cost lever is re-reading cached context, not raising hits. This answers the stated goal honestly.
- **The round-8 correction was done properly.** The answer replaced its own home-made drafter with the official Arctic `SuffixDecodingCache`, swept it, and withdrew the drafter claim.
- **The references number is plausible.**
  - About 18% of context is removed, and input-side cost is about 78% of the bill.
  - Before pointer overhead, that predicts roughly 0.86×.
  - The reported 0.881× fits that estimate.
  - Rewriting results on arrival keeps the history append-only, so the cache stays valid.

## Corrections

1. **Internal inconsistency in Idea A.** The answer says line-run granularity is "worth 12× the saving of whole-result stubs". Its own numbers give (1 − 0.881) / (1 − 0.993) ≈ 17×, or about 15× at MINRUN = 8. The direction stands; the multiplier is misstated.

2. **"Exact" does not mean quality-neutral.** The KV is exact for the rewritten text, but the model now sees pointers instead of content.
   - `str_replace` needs `old_str` reproduced verbatim from text that may sit behind a pointer.
   - Any extra failed edits or extra steps would eat into the 12% saving.
   - No resolve-rate result exists yet, so 0.887× is an upper bound on net savings.

3. **The baseline may be weaker than best practice.** Part of the 18% repetition comes from the harness itself: the editor echoing snippets back, and `file_text` / `old_str` payloads copying content. Existing practice such as diff-style edit formats or simply not echoing would remove some of it. The comparison is against SWE-agent's default harness plus a Claude Code-style stub, not against the best harness.

4. **Idea B (batched clearing) is compared against a guessed baseline and largely prior art.**
   - The headline ratios (0.720× vs 1.006×, 0.625× vs 0.868×) rest on stateless semantics for `clear_tool_uses` that the answer inferred from the docs and never checked. The provider at its best setting coming out *worse than no clearing* is a warning sign about that emulation.
   - Periodic, cache-friendly observation masking already exists. As I recall, SWE-agent's `LastNObservations` history processor has a polling option for exactly this purpose. That makes the fair baseline batched masking, and the increment shrinks to roughly what references add on top.
   - It also drops content, so it does not compare like-for-like with the exact methods.

5. **Idea V (batching read-only calls) is an upper bound, not a result.**
   - It assumes every consecutive pair of read-only actions is independent.
   - Parallel tool use is a standard, documented feature.
   - 0.903–0.946× (0.816× with references) is a ceiling with no quality test behind it.

6. **Idea U (sparse attention) applies existing methods, and its quality is unknown.**
   - Quest, RocketKV in TensorRT-LLM and HiSparse in SGLang are shipped prior art, so a self-hosted "best practice" can already include them.
   - All the figures are roofline estimates.
   - The answer itself says no training-free result exists on multi-turn agent tasks.
   - The large gains (0.53–0.59×) come from a hypothetical 100–170k prefix added to the traces, not from the traces themselves.
   - Those gains depend mainly on sparse prefill over the cache, which the answer calls the less mature path.
   - These are hypotheses that need the model-quality tests the answer lists.

7. **Ideas 2, 3 and 4 rest on weak evidence.**
   - Idea 3's 2.40× saving comes from a synthetic Zipf replay with no fallback and no quality gate measured.
   - Idea 2's splice quality rests on papers whose abstracts only were read.
   - Idea 4's tier thresholds use assumed prices.
   - None of them shows a supported gain over current practice.

8. **Cases that stay below ~100%.** The answer is candid here. In-place middle edits and reordering get exact hits only through layout discipline (errata, canonical order), which is already prior art (Manus, Anthropic docs, *Don't Break the Cache*). The RAG and reordering cases reach high reuse only approximately.

## Net assessment

| Approach | Status after correction |
|---|---|
| References, client side, exact | **Supported:** 0.887× of the bill vs the best exact prior art (cost replay; quality untested) |
| References, runner | Same effect, about 0.884×, modelled not measured |
| Batched clearing | Baseline semantics guessed; batching is prior art; drops content |
| Batching reads | Upper bound only |
| Sparse attention | Shipped methods; agent-task quality unknown; big numbers are hypothetical long-context cases |
| Segment cache / splice / tiering | Synthetic or literature-only |

HONEST GAIN: ~1.13x lower API bill (0.887x of the bill vs Claude Code-style whole-file dedup; 0.881x vs plain prefix caching) for agent traffic, from exact line-run references, cost-replay only with output quality untested