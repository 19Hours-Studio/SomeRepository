=== REVIEW ===
IDEA 1: Popularity-first exact-prefix document ordering
DEFECT | MAJOR | The 1.17–1.78x figures come from a cache that never expires. With real 5-minute TTL traffic the reuse falls below the 0.217 break-even at low request rates, so the idea loses money there. | My replay (100k chunks, top-5, independent Zipf, popularity order) with only the last 10 requests inside the TTL gives reuse of 0.155 at Zipf 1.05, so the doc bill is 1.25·0.845+0.1·0.155 = 1.07, i.e. 0.93x. Idea 4's own "old always-write rule 0.88x" confirms the same loss.
DEFECT | MAJOR | The minimum cacheable length is assumed to be 1,024 tokens. Current Opus 4.5/4.6 and Haiku 4.5 require 4,096, and Sonnet 4.6 requires 2,048. With 256–512-token chunks, depth-1 and depth-2 document breakpoints cannot be cached unless the system prompt is already ≥3k tokens. | OpenRouter prompt-caching docs list per-model minimums of 4096/2048/1024. This is a secondary source; Anthropic's own docs page did not show these models.
DEFECT | MAJOR | All reuse figures assume independent Zipf draws per document. Real top-k sets are correlated by query topic, so the popularity counter and the trie-greedy order can diverge. The claim that the counter matches CacheWeaver is therefore only shown on a workload where the two orders are nearly the same by construction. | My replay gives 0.436/0.583/0.807 with an unbounded cache, against the claimed 0.400/0.546/0.768. Same order of magnitude, but no real retrieval trace was used.
DEFECT | MINOR | Since February 2026 the cache is isolated per workspace, not per organisation. Traffic split across dev, staging and prod workspaces divides the rate that the TTL math depends on. | Several third-party 2026 caching guides report this; I found no primary Anthropic source.
DEFECT | MINOR | Detecting the expected 1–3 F1 point quality shift from reordering needs a paired test with roughly n≥2,000 questions per arm to get ±1 point, and the idea gives no sample size. | Binomial SE at p≈0.5 with n=2,000 is about 1.1 points.
SURVIVES | Break-even reuse 0.217 (1.25−1.15r<1) is correct. Exact-prefix hits give KV identical to full recompute. Runs client-side.
RATIO | 1.15 | ~0.93x at ≤10 req/5 min, up to 1.2–1.8x at high traffic, against caching the system prompt only and sending documents uncached.
KNOWN | partly | CacheWeaver (arXiv 2606.19667) does cache-aware evidence reordering; RAGCache (arXiv 2404.12457) uses a document-order knowledge tree with PGDSF eviction.
NEW FACT | Model-specific minimum cacheable lengths of 4,096/2,048 tokens | https://openrouter.ai/docs/prompt-caching

IDEA 2: Context-length-gated turn collapsing
DEFECT | MAJOR | It does not address the question. It cuts the number of turns, but does nothing for hits on prefixes that differ in the middle, by insertion, by tool output or by reordering. | No change case is covered.
DEFECT | MAJOR | "Observation masking 0.83x" is a model result, and a measurement contradicts it. The measured masking result is about 2x cheaper than the raw agent at equal or better solve rate. That makes masking the best-practice baseline, and against it this idea is about 1.0–1.2x. | Lindenbauer et al., "The Complexity Trap" (arXiv 2508.21433): masking 52% cheaper than raw on SWE-bench Verified with Qwen3-Coder 480B.
DEFECT | MAJOR | Quality impact is not tested. Folding k=3 steps removes the model's ability to react to intermediate results. A single failed task that has to be re-run costs a whole session, and a ~10% drop in solve rate would erase about 20% of the gain. | No solve-rate test is proposed.
DEFECT | MINOR | The 150-turn "gate alone 2.02x" exceeds the bound implied by its own inputs. With reads at 75% of cost and at most 3x fewer reads, the ceiling is 1/(0.25+0.25) = 2.00x, and early turns are not folded at all. | Computed 2.0 upper bound.
DEFECT | MINOR | The scripts are output tokens at 5x the input price (Sonnet $15 vs $3 per M), and this is not counted. | Anthropic price ratio.
SURVIVES | The CodeAct comparison is about right: a 30% turn cut with reads at 75% of cost gives 1.29x (the idea states 1.20x).
RATIO | 1.1 | Against observation masking, which is the measured best practice.
KNOWN | partly | CodeAct (Wang et al. 2024) packs multiple actions into code; Anthropic's "programmatic tool calling" filters tool output inside code.

IDEA 3: Append-only errata with ski-rental compaction
DEFECT | MAJOR | The 99.75% hit rate cannot be a token hit rate that includes new tokens. 50 turns × 2k new tool-output tokens are unavoidable misses, which puts the ceiling at about 97.2%. | The billed 365k units imply ~3.55M input tokens, and 100k/3.55M = 2.8% minimum miss.
DEFECT | MAJOR | It claims near-100% hits on reordering via content-hash ordering. The idea set's own replay shows hash order reuses only 0.152–0.503 and loses money with caching (0.95x). | Idea 1's own figures.
DEFECT | MAJOR | The baseline is in-place editing. Manus-style append-only context is already the competent practice, so the gain against best practice is only the compaction rule. Since T* says compaction almost never pays, that rule adds about 1.0x. | T* = 1,238 turns reproduces; compaction is driven by the context window.
DEFECT | MAJOR | It is not quality-tested. Stale text and correction coexist, and proactive interference (PI-LLM) degrades retrieval of the latest value. The errata also make the context grow without bound. | The idea itself says the test was not run.
DEFECT | MINOR | The 2x ski-rental bound assumes a fixed buy cost. Here the rewrite cost 1.25(N−p) grows every turn, and a TTL expiry makes the rewrite free, so the bound as stated does not apply. | Formula inspection.
SURVIVES | T* formula, 1,237.5 and 50 turns, and −39.6% billed reproduce. The KV is exact.
RATIO | 1.1 | Against append-only practice; 1.65x only against in-place editing.
KNOWN | yes | Manus, "Context Engineering for AI Agents" (append-only, deterministic serialization).

IDEA 4: Popularity order with second-sighting cache writes
DEFECT | MAJOR | It inherits Idea 1's independent-Zipf workload and the 2,048/4,096-token minimums, so the "never loses" claim is unvalidated on real query-correlated traffic and on newer models. | OpenRouter minimum-length table; no real trace.
DEFECT | MINOR | The 1-hour TTL at 2x only beats 5 minutes if reuse is above 0.526 per written depth. That holds only because second-sighting filters writes, and it is sensitive to the seen-list window. | 2(1−r)+0.1r<1 ⇒ r>0.526.
DEFECT | MINOR | On OpenAI and Gemini implicit caching there is no write fee, so second-sighting is pointless there and the advantage is specific to Anthropic. | OpenAI automatic caching has no write premium.
SURVIVES | My replay reproduces the trend and range: doc-only ratios of 1.12–1.38 (Zipf 1.05), 1.23–1.66 (Zipf 1.2) and 1.55–2.47 (Zipf 1.5) across 10–1,000 req/5 min, and it never loses below 1.0x.
RATIO | 1.25 | Replay after diluting with system-prompt and question tokens, at mid traffic and Zipf 1.05–1.2.
KNOWN | partly | CacheWeaver (arXiv 2606.19667) for the ordering; the CDN cache-on-second-hit rule (Maggs & Sitaraman) and TinyLFU for admission.

IDEA 5: Segment cache with boundary recompute
DEFECT | MAJOR | It does not apply to third-party API users, which is the asker's stated setting (hosted APIs). | Requires your own stack or a provider.
DEFECT | MAJOR | Storage is not costed at scale. One KV copy per unique segment for a 100k-chunk × 512-token corpus on a 70B model is about 16.8 TB. That forces NVMe or DRAM tiers, and Idea 6 says those cost more than recompute unless a segment is reused at least every ~2.5 h. | 5.12e7 tok × 327,680 B = 16.8 TB.
DEFECT | MAJOR | "3–7x prefill compute against exact prefix caching" counts all non-prefix tokens as misses. But prefix caching already serves the system prompt, and CacheBlend's measured end-to-end TTFT gain is 2.2–3.3x. Whole-chain GPU cost, with decode included, falls much less. | CacheBlend paper (EuroSys'25).
DEFECT | MINOR | The layer-1 deviation gate threshold is uncalibrated, and the proposed tests (2WikiMQA, MuSiQue) are the same ones CacheBlend already ran, so the test adds little. Fusion-RAG and AgentKVShift are NEW and unverified. | CacheBlend evaluation suite.
SURVIVES | 320 KiB/token for Llama-3-70B, 68.6 KiB/token for DeepSeek-V3 MLA (4.66x), and the 6.6 s PCIe load per 1M tokens at 50 GB/s all reproduce. Loading is about 48x faster than the ~315 s recompute.
RATIO | 1.5 | Own-stack GPU cost per RAG request after decode and storage.
KNOWN | yes | CacheBlend in LMCache/vLLM, EPIC (ICML'25), APE, TurboRAG.

IDEA 6: Storage-priced retention, not token-priced hits
DEFECT | MAJOR | Storage-priced retention is already sold. Gemini explicit caching bills storage per token-hour, and RAGCache's PGDSF and AttentionStore are cost-aware tiered eviction, so the "addition" is not new. | Gemini cache storage $1.00 (Flash) to $4.50 (Pro) per M tokens per hour, from third-party pricing guides; arXiv 2404.12457.
DEFECT | MAJOR | It does not raise hit rates on non-identical prefixes at all. It only reprices retention of exact prefixes. | No change case is covered.
DEFECT | MINOR | "MLA cuts 4.6x" mixes models. DeepSeek-V3 recompute is also cheaper (37B active, about $0.092/M), so the break-even interval moves less than 4.6x. | Computed.
DEFECT | MINOR | "About 1.2x for tiered caching" is an unsourced number from an earlier run. Mooncake reports far larger capacity gains on real traces. | Mooncake (FAST'25).
SURVIVES | $0.175/M recompute, $8.2/M-h in HBM, the DRAM break-even interval of 6.6 min and the NVMe break-even of 2.5 h all reproduce.
RATIO | 1.05 | Eviction-policy refinement over existing tiered caches.
KNOWN | yes | Gemini context-cache storage pricing; RAGCache PGDSF; AttentionStore (ATC'24).

IDEA 7: Hole-punch deletes via block-table edits
DEFECT | MAJOR | After the hole, the KV no longer corresponds to any token string. It cannot be keyed in a prefix or radix cache, cannot be shared across requests, and cannot be rebuilt after eviction without full recompute. The 100% hit rate therefore holds only within a sticky session. | Mechanism; prefix caches are keyed by token hash.
DEFECT | MAJOR | Deletions are usually done to remove distraction and context rot, but the residual information in later tokens keeps part of the deleted span's influence. Clearing becomes cheaper but partly ineffective, and that is untested. | No downstream task test; KL and top-1 agreement are not task success.
DEFECT | MINOR | "Pair with an erratum from Idea 1" is a wrong cross-reference (errata are Idea 3). PyramidKV is a layer-budget method, not position-gap continuation. HERMES and KV Packet are NEW and unverified. | Text.
DEFECT | MINOR | Spans that are not aligned to 16-token blocks need copy-on-write of the boundary blocks, so "zero extra memory" does not hold exactly. | vLLM block size 16.
SURVIVES | The 1.25/0.1 = 12.5x suffix ratio is correct. Anthropic context editing really does invalidate the cache, and its docs advise `clear_at_least` for that reason.
RATIO | 1.2 | Per-session saving, given deletions are periodic and reads dominate.
KNOWN | partly | llama.cpp context shift; StreamingLLM position re-indexing; Anthropic context editing (docs.claude.com).

IDEA 8: Cost-optimal patch folding
DEFECT | MAJOR | The baseline is inline rewriting, a strawman. The competent practice is appended patches (Idea 3 and Manus), and against that the gain is only fold timing, about 1.0–1.05x. | Idea 9 itself reports "within 4–8%" of the coding-agent patch chain.
DEFECT | MAJOR | It has no quality test, even though the design depends on the model applying section patches correctly at a distance. | None stated.
DEFECT | MINOR | The 96.4% hit rate is redefined as "every reusable token" and excludes new tokens, so it is not comparable with the question's hit rate. | Text.
DEFECT | MINOR | The TTL sensitivity (30% of gaps longer than 5 min, giving 1.2–1.4x) is assumed. Human copilot think-times often exceed 5 min, and the 1-hour TTL costs 2x per write. | Not sourced.
SURVIVES | A rough recomputation of the 25k/10-question/3-edit case gives about 1.5–1.75x against inline, consistent with the stated 1.52x.
RATIO | 1.05 | Against appended-patch practice.
KNOWN | yes | Manus append-only; ski-rental is textbook.

IDEA 9: Floating depth-1 override ledger
DEFECT | MAJOR | 4.6x is measured against keeping mutable state at the front and rewriting it inline, which is a strawman. Standard practice is to put mutable state at the end, as Claude Code's to-do and system reminders do, and that gives the same ~$0.069. | Computed: inline $0.304 vs ledger $0.069 input at $3/M. A tail-state baseline is equal, so the ratio is ~1.0.
DEFECT | MAJOR | Dropping the ledger from history every turn leaves earlier assistant replies citing state that is no longer visible. The depth-1 interference benefit is asserted, not tested. | No test proposed.
DEFECT | MINOR | "Within 6% of the no-edit floor" holds only if the ledger averages ~1.5k tokens. With the full 8k state edited, input cost is $0.069 against a $0.045 floor, i.e. +53% on input. | Computed.
SURVIVES | Inline $0.30 + output ≈ $0.336, and ledger ≈ $0.069–0.0735, reproduce at $3/M.
RATIO | 1.0 | Against mutable state at the tail.
KNOWN | yes | Manus guidance on keeping the prefix stable; Claude Code places system-reminder and to-do state at the tail.

Sources:
- [Anthropic prompt caching docs](https://docs.claude.com/en/docs/build-with-claude/prompt-caching)
- [OpenRouter prompt caching](https://openrouter.ai/docs/prompt-caching)
- [The Complexity Trap (arXiv 2508.21433)](https://arxiv.org/abs/2508.21433)
- [CacheWeaver (arXiv 2606.19667)](https://arxiv.org/pdf/2606.19667)
- [RAGCache (arXiv 2404.12457)](https://arxiv.org/pdf/2404.12457)
- [Anthropic context editing](https://docs.claude.com/en/docs/build-with-claude/context-editing)
- [Gemini context caching pricing (third-party)](https://fast.io/resources/gemini-context-caching/)
- [Workspace cache isolation report (third-party)](https://dev.to/alexcloudstar/prompt-caching-in-2026-anthropic-vs-openai-vs-gemini-for-production-apps-433i)