=== REVIEW ===
IDEA 1: Storage-priced retention, not token-priced hits
DEFECT | MAJOR | It adds nothing for the question's actual cases (middle edits, insertions, changed tool outputs, reordering): those tokens are not stored KV at all, so keeping KV longer cannot turn them into hits. | Every break-even in the text applies only to exact-prefix entries. The hit rate on non-identical prefixes is unchanged.
DEFECT | MAJOR | The recompute cost leaves out attention FLOPs, which double the cost of long prefixes, so every break-even is about 2x too short. | 4·80·8192·(C/2)/1.4e11 = 1.2x the linear FLOPs at a 128k prefix. That gives $0.385/M instead of $0.175/M, so DRAM breaks even at about 14 min (not 6.6) and NVMe at about 5.5 h (not 2.5).
DEFECT | MAJOR | Pricing reuse only against recompute GPU-dollars leaves out time-to-first-token (TTFT): recomputing a 128k prefix takes about 40–90 s on one H100, so no operator would make this trade on cost alone. | 128k / 3,179 tok/s = 40 s for the linear part alone, about 88 s with attention. Loading from NVMe takes 42 GB / 7 GB/s ≈ 6 s.
DEFECT | MAJOR | "MLA cuts 4.6x" compares a 70B GQA model with a different model, DeepSeek-V3 (671B MoE). Converting an existing model to MLA (TransMLA, MHA2MLA) needs fine-tuning, which the constraint forbids. | 327,680 / 70,272 B/token = 4.66 reproduces, but only by switching models.
DEFECT | MINOR | The rule is labelled ski-rental, but it is an expected-value rule (expected reuses × cost). It has no worst-case 2x guarantee. | Definition as stated in the text.
DEFECT | MINOR | The "only 1.2x over GPU-only" figure for prior art is unsourced and is being used as a straw baseline. | No source given. Mooncake and LMCache report several-fold gains on their own workloads.
SURVIVES | $0.175/M recompute (linear part), 320 KB/token, $8.19/M·h in HBM, DRAM/NVMe ratio 22.9x, and the 6.6 min / 2.5 h break-evens all reproduce under the stated inputs.
RATIO | 1.1 | Own stack only: cost-aware eviction against LRU tiering in LMCache/Mooncake changes only marginal-tier decisions. Hosted-API users get 1.0.
KNOWN | yes | Gemini explicit caching already bills storage per token-hour (about $4.50/M·h for 2.5 Pro, ~$1 for Flash; ai.google.dev pricing, via https://discuss.ai.google.dev/t/gemini-2-5-pro-context-cache-pricing-per-request-vs-cumulative-token-counting/92919). Marconi (MLSys'25) uses FLOP-saved-per-byte eviction (https://arxiv.org/pdf/2411.19379). Anthropic's 1-hour TTL at 2x write is a priced-retention tier.
NEW FACT | Gemini explicit caching needs at least 32,768 tokens and defaults to a 1 h TTL | https://fast.io/resources/gemini-context-caching/

IDEA 2: Cost-optimal patch folding
DEFECT | MAJOR | The forced fold on a second edit to the same key cancels the ski-rental "≤2x optimal" guarantee. A frequently edited section near the front triggers a full rewrite on every second edit. | 15 edits to §1 of a 120k document mean about 7 forced folds × 150k = 1.05M units, against about 15×(small patch) for patch-only. The competitive ratio is unbounded.
DEFECT | MAJOR | The baseline is inline rewriting of the document. Competent agent practice already appends changes (Edit-tool diffs, file re-reads, mutable state at the tail). | Against that practice the gain is roughly the fold-timing difference, about 1.0–1.15x, not 1.5–2.7x.
DEFECT | MINOR | "96.4% hit = every reusable token" defines the hit rate as the ceiling of its own model, so it is circular. | As stated.
DEFECT | MINOR | No inter-turn gap distribution is sourced, yet the gain falls to 1.2–1.4x at 30% of gaps above the TTL. Human document sessions often have gaps longer than 5 min. | No measured data cited.
SURVIVES | The 1.5–2.7x against inline rewriting is plausible: my rough check gives 1.9x (25k) and 3.0–3.3x (120k) with uniform edit positions.
RATIO | 1.1 | Against an append-patch or re-read agent, not inline rewriting.
KNOWN | partly | Manus "keep the prefix stable, append-only context" (manus.im blog, Context Engineering for AI Agents). Claude Code's Edit/Read pattern.

IDEA 3: Popularity-first exact-prefix document ordering
DEFECT | MAJOR | The reuse figures assume a cache that is warm without limit, not a 5-minute TTL. Inside a TTL window, reuse falls below the 0.217 break-even at modest traffic. | My replay (100k chunks, top-5): Zipf 1.05 reuse is 0.155 / 0.253 / 0.336 at 10 / 100 / 1,000 requests per window. That gives doc-token ratios of 0.93 / 1.04 / 1.15x, against the claimed 0.400 and 1.17x.
DEFECT | MAJOR | The Zipf exponents are not tied to measured RAG skew. Measured traces imply lower skew, and there the method loses money. | Cache-Craft: top 5% of chunks serve 40–60% of requests (https://arxiv.org/pdf/2502.15734). Zipf 1.05 puts 77% in the top 3%. At Zipf 0.85 (51% in the top 3%) reuse is 0.048–0.181, below 0.217 even at 1,000 requests per window.
DEFECT | MAJOR | The baseline ignores implicit-cache APIs with no write premium (OpenAI, Gemini implicit). There even hash order gains, so "uncached documents" is not best practice everywhere. | With a 90% read discount and no premium, popularity vs hash = (1−0.9·0.152)/(1−0.9·0.40) = 1.35x. Under that pricing the base practice already beats 1.0x.
DEFECT | MAJOR | The 1,024-token minimum is outdated for current models. Short chunk prefixes at depth 2–3 cannot be cached. | Opus 4.5 and Haiku 4.5 need 4,096 tokens per checkpoint (Bedrock docs, LiteLLM table: https://docs.litellm.ai/docs/completion/prompt_caching.md).
DEFECT | MINOR | Popularity order moves the most relevant document away from first position (the "lost in the middle" effect), and the test has no sample size. | Detecting a 2-point EM change at about 10% discordant pairs needs n ≈ 2,000 paired questions (z≈2.8).
SURVIVES | Break-even 0.217 = (1.25−1)/1.15 reproduces. Hash order 0.95x reproduces (0.93 per doc token). The per-request ratios are consistent with dilution by non-document tokens.
RATIO | 1.05 | Average over realistic traffic with the 5-minute TTL and measured skew. It is below 1.0 at low traffic, where you must fall back to uncached.
KNOWN | partly | CacheWeaver-style trie ordering. RAGCache knowledge tree (https://arxiv.org/pdf/2404.12457).

IDEA 4: Context-length-gated turn collapsing
DEFECT | FATAL | The 2.02x gate-only figure exceeds the hard ceiling for k=3 at a 75% read share. | Ceiling = 1/(0.25+0.75/3) = 2.00x. 2.02x needs 67.3% of reads removed, more than the 2/3 maximum, even with every turn folded and no early stops.
DEFECT | MAJOR | Folding only read-only or idempotent tools caps the gain well below what the text claims. | If 60% of late turns are foldable: 1/(0.25+0.75·(1−0.6·2/3)) = 1.43x, not 2.02x. Each early stop lowers it further.
DEFECT | MAJOR | It does not raise the cache hit rate on any of the four change cases. It reduces turn count, a different lever, and the task-success cost of acting on fewer observations is not measured. | No success-rate data. Script-writing output is billed at 5x the input price and is left out.
DEFECT | MAJOR | The baseline omits shipped programmatic tool calling, which already keeps intermediate tool results out of context. | Anthropic Programmatic Tool Calling, about 37% token reduction on multi-tool tasks, GA Feb 2026 (https://www.anthropic.com/engineering/advanced-tool-use).
SURVIVES | The direction holds: gating on C×0.1×p correctly prices late turns as the expensive ones.
RATIO | 1.1 | Against an agent that already uses programmatic tool calling and filtering.
KNOWN | yes | CodeAct, and Anthropic "code execution with MCP" and Programmatic Tool Calling.

IDEA 5: Popularity order with second-sighting cache writes
DEFECT | MAJOR | It inherits Idea 3's skew problem. At measured RAG skew (about Zipf 0.85), reuse within the window stays below the 1h-TTL break-even, so the gain is about 1.0x rather than 1.06x. | 1h-TTL break-even r > (2−1)/1.9 = 0.526. Replay reuse at Zipf 0.85 is ≤0.18.
DEFECT | MAJOR | Four breakpoints at document depths 2–5 leave none for the system prompt. Anthropic only finds entries that earlier requests wrote, so every request whose first documents are new misses the system prompt too. | Lookback finds only prior breakpoint positions. Either the system prompt is billed in full on misses, or depth 5 must be given up (3 document breakpoints).
DEFECT | MINOR | "Client-only, stateless" is not true at organisation scale. The seen-hash list must be shared across all workers (for example in Redis), or each worker sees 1/W of the traffic. | With W=10 workers, effective traffic per list is 10x lower, so the result moves toward the low-traffic 1.06x end.
DEFECT | MINOR | The 4,096-token minimum (Opus 4.5 / Haiku 4.5) blocks shallow breakpoints, as in Idea 3. | LiteLLM / Bedrock tables.
SURVIVES | "Never loses" holds by construction when first sightings are billed at 1.0x and when hit rates are measured within the TTL window.
RATIO | 1.1 | Within the TTL window, at mid traffic and Zipf ≈1.0, against uncached documents.
KNOWN | partly | TinyLFU / "cache on second hit" admission in CDNs, and Marconi's admission forecasting (https://arxiv.org/pdf/2411.19379).

IDEA 6: Floating depth-1 override ledger
DEFECT | MAJOR | The baseline puts 8k of mutable state at the front and rewrites it inline. Every caching guide says to put dynamic state at the end, and against that practice the ledger costs the same. | Tail state: 142k×0.1 + 8k×1.0 = 22.2k units ≈ the ledger's 24.5k ($0.0735 at $3/M). Ratio ≈1.0, not 4.6.
DEFECT | MINOR | The 10% fold cap is set where the ledger already doubles per-turn input cost. | 15k ledger at 1.0x equals the 150k read at 0.1x.
DEFECT | MINOR | "Patch-chain depth 3–7" is unsourced. | No citation.
SURVIVES | $0.336 inline and $0.0735 ledger reproduce within about 10% under $3/M pricing (101k + outputs vs 15k + ledger).
RATIO | 1.0 | Against mutable state appended at the tail.
KNOWN | yes | Claude Code re-injects todo/state as trailing `<system-reminder>` blocks. Manus "recitation" of todo.md at the end of context.

IDEA 7: Append-only errata with ski-rental compaction
DEFECT | MAJOR | The baseline (editing earlier tool outputs in place) is a straw man. Real agents already append re-reads and never edit earlier results, so the 40% is against a practice almost no one uses. | My replay reproduces about −45% (528k → 290k) only against the in-place baseline. Against append re-read the ratio is 1.0.
DEFECT | MAJOR | "Reordering becomes an exact prefix match" by hash order contradicts Idea 3's own replay. Hash order gives 0.152–0.503 reuse, and 0.95x with cache_control. | Idea 3's figures.
DEFECT | MAJOR | Stale text plus errata grows the context, which raises the read cost and context-rot risk the method ignores. Compaction is "window-driven" only. | 10 errata × 2k over 50 turns = +20k tokens, +20% on a 100k context. That is never compacted on cost grounds (T* = 50–1,238 turns).
DEFECT | MINOR | "KV matches full recomputation exactly" is true only for a different prompt (stale text plus correction), not the intended one. | Definitional.
DEFECT | MINOR | The quality test has no sample size. A SWE-bench A/B needs about 500+ paired tasks to resolve 3 points. | 500-task Verified set, binomial SE ≈2.2 points.
SURVIVES | T* = 1,237.5 and 50 turns reproduce. The −40% billed input reproduces in direction and magnitude against the in-place baseline.
RATIO | 1.0 | Against append-and-re-read agents.
KNOWN | yes | Manus "append-only context, deterministic serialization" (manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus).

IDEA 8: Hole-punch deletes via block-table edits
DEFECT | MAJOR | The position-gap variant runs past the trained context window in long sessions. | Clears of at least 20k on a 100–120k trigger: positions pass 200k after about 4–5 clears, while live context stays at about 120k.
DEFECT | MAJOR | Post-hole blocks are keyed by hash chains that include the deleted tokens. Other requests cannot reuse them, and blocks shared through refcounts cannot be freed. | vLLM's prefix-cache block hash depends on all earlier tokens. The "zero extra memory, freed to pool" claim fails whenever a block is shared.
DEFECT | MAJOR | Residual information from the deleted span defeats the main reason for clearing (stale or wrong context). The quality risk is unmeasured. | No KL or top-1 data. llama.cpp context shift is known to degrade quality.
DEFECT | MINOR | It refers to "an erratum from Idea 1", but errata are Idea 7. Blocks are 16 tokens, so a deletion boundary mid-block needs a partial recompute. | Text as written.
SURVIVES | 1.25/0.1 = 12.5x per suffix token. Anthropic context editing does invalidate the cache from the cleared point (https://platform.claude.com/docs/en/build-with-claude/context-editing).
RATIO | 1.3 | Clears are amortised by clear_at_least: about 5 rewrites × 1.15 × 80k = 460k saved out of about 1.6M per 100-turn session, before any quality cost.
KNOWN | partly | llama.cpp context shift, StreamingLLM/H2O/SnapKV. Anthropic's clear_at_least exists to amortise exactly this invalidation.
NEW FACT | Anthropic documents that tool-result clearing invalidates cached prefixes and recommends clear_at_least to make the rewrite worthwhile | https://platform.claude.com/docs/en/build-with-claude/context-editing

IDEA 9: Segment cache with boundary recompute
DEFECT | MAJOR | Saving prefill compute (3–7x) is not the same as saving whole-request cost. Decode, question tokens and recompute attention over the full context remain. | RAG with 6k input / 300 output at a 1:5 price weighting: 7.5k → about 3.25k units ≈ 2.3x against no cache, and about 1.7x against exact prefix caching that already hits shared prefixes.
DEFECT | MAJOR | A "KV per segment computed after the shared prefix" store multiplies with distinct system prompts or tenants. | Storage = segments × prompts × 320 KB/token. 10 system prompts × 1M segment tokens = 3.3 TB in BF16.
DEFECT | MINOR | The deviation gate duplicates CacheBlend's own layer-wise selection, and every fallback lowers the claimed 85–94%. | No gate trigger rate given.
DEFECT | MINOR | It does not run on hosted APIs at all, so it does not help the third-party-API case. | Own stack only.
SURVIVES | 320 KB and 69 KB/token, 6.6 s per 1M tokens (≈49.6 GB/s PCIe Gen5), EPIC 32/512 = 6.25%, and CacheBlend's 15% recompute with 2.2–3.3x TTFT all reproduce.
RATIO | 1.7 | Whole-request cost against exact prefix caching on a RAG workload with moderate reuse.
KNOWN | yes | CacheBlend (LMCache), EPIC, APE, and Cache-Craft (https://arxiv.org/pdf/2502.15734).
NEW FACT | Measured RAG skew: top 5% of chunks serve 60% of requests (Sys-X, MuSiQue) and 40% (2WikiMQA). Separately, 3.1–31.4% of documents serve 50% of queries across SQuAD, HotpotQA and TriviaQA. | https://arxiv.org/pdf/2502.15734 ; https://arxiv.org/pdf/2504.11765