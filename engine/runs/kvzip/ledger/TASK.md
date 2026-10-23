# Task: the value ledger - where the cost actually goes today

QUESTION the ledger serves: Which architecture for compressing the LLM KV cache (the stored attention keys and values) is best if it has to be much more aggressive than FP8, which is 8 bits per value or about 2× smaller than FP16/BF16? It has to work as a drop-in replacement for the cache storage format in an existing pretrained transformer model, with no retraining, fine-tuning or architecture change, and with almost no loss of quality. The cache may be compressed along any axis: numeric precision, the number of stored tokens, channels or heads, redundancy across layers, or entropy coding. The asker calls this a "super-zip" for the KV cache. The answer should be a concrete architecture, covering what is stored, how it is encoded and decoded, and how attention reads it. It should also give the expected compression ratio and quality loss on standard long-context and reasoning benchmarks, and say what runtime cost the design adds.
A good answer: 
- It gives a specific, implementable design. Naming a family of methods is not enough.
- It states the effective bits per value or the compression ratio vs FP16, counting all metadata (scales, zero-points, indices, codebooks).
- Quality loss is stated against the FP16 cache on named benchmarks and models, for example LongBench, RULER, needle-in-a-haystack, GSM8K or MATH-style reasoning, and perplexity. "Almost no loss" is given a number, for example ≤1% relative drop.
- It is checked against the failure modes below: outlier channels in keys, RoPE, attention sinks, GQA/MLA models, long contexts, multi-turn or multi-query reuse, and reasoning-model chains of thought.
- It estimates decode and prefill latency and throughput, including dequantization or decompression cost and compatibility with FlashAttention-style fused kernels.
- It shows how it beats or complements the current state of the art (see CONTEXT), and says what is new.
- It names a cheap experiment that could falsify it.
Constraints: 
- No training, fine-tuning or distillation of the base model. The asker said "without retraining". Whether a one-time offline calibration pass on a small data sample counts is UNCLEAR.
- It must apply to any ready-made model by changing the cache storage format only.
- Compression must be far beyond FP8. This is stated as "much stronger" with no numeric target.
- Quality must drop almost not at all.

You are a cost researcher. Build the ledger that tells inventors WHERE THE COST IS today, with sourced numbers, for the
3-5 archetypes (a concrete use case + the way a competent practitioner does it today, best current practice) most
relevant to the question. "Cost" is what the question asks to reduce or improve - money, energy, memory, time,
bandwidth, error - per unit of the final product or service. Tools: WebSearch (WebFetch does not reach hosts here; use
excerpts) and Bash with python3. At most 15 searches. Write files only in the current directory; do not commit.

For each archetype give: best current practice in one line; the cost per unit of final product or service; the cost
split in % that sums to 100 across 4-8 terms natural to this domain (for physical goods use exactly: energy | labour |
inbound logistics | outbound logistics | processing | capital | other), always ending with "other" = the part that no
answer to this question could change (for goods: taxes, royalties, fees, margins); the largest term.

Final answer (text only), exactly this shape, at most 700 words:
=== LEDGER ===
ARCHETYPE A: <best practice> | cost <number unit per unit of product or service> | <price or target, if any>
SHARES: <term> x% | <term> y% | ... | other t%
LARGEST: <term> - a 10x cut of it removes <p>% of the cost
(same for B, C, ...)
SOURCES: short list of URLs.
