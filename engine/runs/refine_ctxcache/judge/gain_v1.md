# Verdict: no demonstrated gain over best current practice

The answer's headline compares against a strawman baseline. Against an honest best-practice baseline, what remains is a small synthetic hit-rate difference that comes from prior-art techniques and has no quality test.

## What checks out

I re-derived the arithmetic, and it is sound:

- **§B cost split.** Over 50 turns, reads come to about 332k token-equivalents (0.1 × Σ(10k + 2.3k·(t−1))). Writes come to about 156k (1.25 × 125k). Output comes to about 75k (15k × 5). That gives 59% / 28% / 13%, as stated.
- **Ski-rental break-even.** (1.15·50k − 625)/50 = 1,138 turns, and (11.5k − 2.5k)/200 = 45 turns. Both are correct.
- **Idea 4 numbers.**
  - Llama-3-70B KV is 80 × 8 × 128 × 2 × 2 B ≈ 320 KB per token.
  - Recompute costs about $0.175 per 1M tokens: 140 GFLOP per token on 445 effective TFLOPS at $2/h.
  - HBM break-even is about 1.3 min: 320 GB per 1M tokens at about $8/h.
  - One NVMe drive at about 6.7 GB/s loads about 21k tokens/s.
  - All consistent. This is useful analysis, but it is a cost model, not a gain.

## What is unfair or unsupported in its own comparison

1. **The Idea 1 headline (47% → 96.6%) uses the wrong baseline.**
   - "Typical authoring order" is not best practice.
   - Manus already prescribes a stable prefix, append-only context, deterministic serialization, and re-stating the volatile todo list at the end of the context.
   - Anthropic's guidance already says to put stable content first.
   - So the fair baseline is the "volatile tail" row at **94.7%**, not 47%.
   - The only remaining step is 94.7% → 96.6%, and it comes from errata for document changes. That is the same append-only principle, and Manus already says to leave corrections in place rather than edit.
2. **Smith's rule is compared against random layouts.** The miss rate drops from 29.7% to 11.1%, but the baseline is random order rather than the "stable-first" heuristic. On the answer's own agent layout, Smith's rule alone gives 68.4%, which is worse than the prior-art volatile-tail layout.
3. **The 96.6% is optimistic.**
   - It treats errata as near-zero misses. For a changed document, the erratum can be as large as the document.
   - It ignores that errata keep adding read volume.
   - Quality is untested. Stale text is left sitting next to its correction.
4. **RAG popularity ordering (52–58% → 60–76%) is weakly supported.**
   - It comes from a synthetic Zipf replay, not real logs.
   - It moves documents away from relevance order, a known quality risk ("lost in the middle"), and that risk was not tested.
   - Prior art on reordering for prefix sharing (e.g., relational and LLM query-reordering work, RAGCache) was not ruled out.
5. **Idea 2's "12.5× cheaper" uses the wrong comparison.**
   - The fair alternative to splicing is to keep the tool result and read it at 0.1×, not to rewrite the suffix at 1.25×.
   - The real saving is only the deleted tokens' reads, so it is at most the 0.71× input bill.
   - Even that requires a provider to offer the operation and bill it as a hit.
   - It is approximate and has no quality measurement.
   - The answer itself concedes that Leyline already implements splicing with RoPE re-anchoring.
6. **Idea 3 contributes no measurements of its own.** CacheBlend, EPIC, APE, and AgentKVShift supply all of its numbers. The proposed additions, a deviation gate and two-tier pricing, are neither implemented nor measured.
7. **The TTL rule and the compaction rule are small.** The TTL rule is direct arithmetic from Anthropic's published pricing. The compaction rule rarely binds, as the answer itself admits, because context limits trigger compaction first.

## Net

- **Against an honest best-practice baseline, the exact client-side gain is at most 94.7% → 96.6% token hit rate.** In price terms, input cost per token drops from about 0.161 to 0.139, roughly 1.16×.
  - This figure is synthetic.
  - It rests on optimistic accounting of the errata.
  - It comes from a prior-art principle.
  - It has no quality validation.
- **The serving-side ideas add no measured gain.** They are either prior art (splicing, segment reuse) or untested additions (the gate and the pricing).

The answer is honest about its limits and its arithmetic is correct. But it does not establish a real improvement over current best practice.

HONEST GAIN: none