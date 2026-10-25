=== REVIEW ===
IDEA 1: Storage-priced retention, not token-priced hits
DEFECT | FATAL | This does nothing about the asked problem: it only changes how long exact-prefix KV is kept, so a middle edit, insertion, changed tool output or reordering still misses from the first differing token. | The mechanism has no step that matches non-identical prefixes; the hit rate on edited prefixes stays what plain prefix caching gives.
DEFECT | MAJOR | Its central "new" step, pricing retention by storage per token-hour, is already a shipped product. | Gemini explicit context caching bills storage separately at about $4.50 per 1M tokens per hour on Pro models, and has a 32,768-token minimum (ai.google.dev forum, fast.io). Anthropic sells a 1h TTL at 2x write.
DEFECT | MAJOR | The $0.175/1M recompute figure counts only the 2·P linear FLOPs and leaves out attention, which roughly doubles the per-token cost at long context. That moves every break-even point. | Causal attention at 100k context is about 4·80·8192·50k = 1.31e11 FLOP per token, 0.94x the 1.4e11 linear part, so recompute is about $0.34/1M. That shifts the DRAM break-even from about 6.6 min to about 13 min, and NVMe from 2.5 h to about 4.8 h.
DEFECT | MAJOR | The cost basis is recompute GPU-dollars only. It ignores time-to-first-token (TTFT), which is a main reason to keep KV in fast tiers, and it ignores the bandwidth needed to read KV back from NVMe. | Reading 327.7 GB (1M tokens of 70B BF16 KV) at 7 GB/s per drive takes 47 s. An 8xH100 node recomputes the same 1M tokens in 39 s. So NVMe-default retention is slower than recompute unless the node has 2 or more drives per node striped.
DEFECT | MINOR | The rule as written, "keep while expected reuses × recompute > storage × time", is an expected-value threshold, not ski-rental. It carries no competitive guarantee and needs a reuse forecast. | Definitional.
DEFECT | MINOR | The ~4.6x MLA figure compares KV per token across different models. DeepSeek-V3 has 37B active parameters versus 70B dense, so its recompute cost per token also falls about 1.9x, and the break-even reuse interval improves only about 2.5x, not 4.6x. | 327,680 / 70,272 B = 4.66, but 4.66 × (37/70) ≈ 2.5.
SURVIVES | These reproduce: $0.175/1M (linear-only), 320 KB/token, $8.19 HBM-hour, 69 KB/token for MLA, 6.6 min DRAM and 2.5 h NVMe break-evens, DRAM/NVMe ≈ 23x.
RATIO | 1.1 | Against tiered LRU caching (LMCache/Mooncake), per-prefix cost eviction only trims storage spend. Hit rate on edited prefixes is unchanged.
KNOWN | yes | Gemini context-cache storage pricing; CachedAttention/AttentionStore (USENIX ATC'24) cost-tiered KV storage; Mooncake; LMCache.
NEW FACT | Gemini explicit caching charges about $4.50/1M tokens/hour of storage on Pro models, plus a reduced per-use cached-input rate. Flash rates were conflicting and I could not confirm them. | https://discuss.ai.google.dev/t/gemini-2-5-pro-context-cache-pricing-per-request-vs-cumulative-token-counting/92919 ; https://fast.io/resources/gemini-context-caching/

IDEA 2: Floating depth-1 override ledger
DEFECT | FATAL | The 4.6x is measured against a straw man: mutable state placed at the front and rewritten inline. The standard practice is to put mutable state after the last cache breakpoint, and it costs the same as the ledger or less, without the stale copy. | My recompute at $3/M: inline $0.304/request, ledger $0.069, state-at-end $0.0666. Ledger vs best practice ≈ 0.97x.
DEFECT | MAJOR | The stale 8k original stays in the cached prefix forever, and each key has an override after it. So the model reads two conflicting values on every turn. "Depth 1" still means every key is interfered with on every turn, and that is never measured. | 20 edits across 8k of state means most keys always carry a conflict. No quality test is proposed, although the brief requires one.
DEFECT | MAJOR | Dropping the ledger from history shifts the positions of the assistant reply and tool results that came after it. In a multi-call agent turn the ledger must stay in place across tool calls, or each reply is re-written at 1.25x. | Acknowledged only as "plus reply tokens". With 40 calls this is up to 40 suffix re-writes, and their size is not stated.
DEFECT | MINOR | The 2.6–4.6x range and "within 4–8% of the patch chain" come from an unpublished model with unstated prices, output tokens and edit positions. | I could reproduce $0.0735 vs $0.336 only to within about 10%, and only by assuming $3/M input with no output cost.
SURVIVES | The arithmetic shape holds: one ledger at 1.0x on top of a 0.1x cached read is cheap when edits are frequent.
RATIO | 1.0 | Against "mutable state at the end of the prompt" ($0.0666 vs $0.069).
KNOWN | yes | Manus re-writes todo.md at the end of context every step (Manus, "Context Engineering for AI Agents"). Anthropic's caching docs say to put static content first and dynamic content last.

IDEA 3: Segment cache with boundary recompute
DEFECT | MAJOR | It does not exist on hosted APIs. No provider offers position-independent segment reuse, so for a third-party-API user the gain is zero. | The idea itself says "own stack or provider-side".
DEFECT | MAJOR | "Prefill compute falls 3–7x" is the ceiling for prefill only. Decode, the per-segment KV load and the full-compute selection pass are untouched, so whole-request cost falls much less. | Recomputing 15% gives at most 6.7x on prefill. CacheBlend's own whole-request figures are TTFT 2.2–3.3x and throughput 2.8–5x.
DEFECT | MAJOR | The layer-1 deviation fallback gate has no evidence that layer-1 KV deviation predicts answer error. A gate tuned on single-hop RAG may not fire on the multi-hop and agent-memory cases where the idea itself admits a gap. | No calibration data is given. Fusion-RAG and AgentKVShift are unverified (NEW), so I cannot size the gap.
DEFECT | MINOR | A cached segment's KV is only valid for the exact shared prefix it was computed after (APE), and for one model and checkpoint. Storage therefore scales with segments × distinct system prompts, not just with unique segments. | At 320 KB/token, a 1M-token corpus is 327 GB per system-prompt variant.
DEFECT | MINOR | The proposed quality test has no sample size or equivalence margin. | Detecting a 1-point F1 drop on MuSiQue needs about 1,000+ paired items at α=0.05. Only about 200 items are typically used in LongBench subsets.
SURVIVES | These hold: CacheBlend's 15% recompute and 2.2–3.3x TTFT, EPIC's up-to-8x TTFT, 320 KB and 69 KB per token, and about 6.6 s per 1M tokens over PCIe at 50 GB/s.
RATIO | 2.5 | Prefill-dominated RAG on your own stack vs exact prefix caching (which gets about 0 hits on new chunk combinations); 1.0 on hosted APIs.
KNOWN | yes | CacheBlend (EuroSys'25), shipped in LMCache with vLLM; EPIC (ICML'25); APE (ICLR'25). The only addition is the gate.

IDEA 4: Cost-optimal patch folding
DEFECT | MAJOR | The best current practice is not inline rewriting but appended diffs/patches, which coding agents already use. Against those, the only addition is the fold timing, worth a few percent. | Idea 2 itself puts the patch chain within 4–8% of its cost, so this rule vs the chain ≈ 1.05x.
DEFECT | MAJOR | The ski-rental 2x bound is proved for a single buy against fixed rent. Here the buy price changes as patches arrive (earliest patched position), forced folds on a repeated key break the rule, and TTL expiry destroys the cache write, so the 2x claim is not established for this policy. | Forced folds alone can make cost depend on edit pattern without bound: one key edited each turn forces a fold of the suffix every turn.
DEFECT | MINOR | The ratios swing with unstated output-token and edit-position assumptions. | My sim of 25k doc, 10 questions, 3 mid-document edits: 1.72x input-only, 1.54x with 400-token answers at 5x price.
DEFECT | MINOR | There is no quality test, yet residual stale text plus a patch per section is the main risk. | The brief requires one.
SURVIVES | Folding for free on a request that misses anyway is correct. 1.5–2.7x vs inline rewriting is plausible.
RATIO | 1.05 | Against the appended-patch chain that coding agents already use.
KNOWN | partly | Diff-based edits in Aider and Claude Code; break-even rule as in classic ski-rental caching.

IDEA 5: Context-length-gated turn collapsing
DEFECT | MAJOR | The gate prices the observation at the cached-read cost, which is tiny next to the value of observing in a task worth dollars. So the rational gate almost never fires, and when it does it trades success rate for cents. | At C=30k and $3/M, one read is 30k × 0.1 × $3/M = $0.009. A 0.5% success drop on a $2 task costs $0.01.
DEFECT | MAJOR | There is no quality metric or test, and folding steps without observing is exactly what lowers agent success. | The brief requires a quality comparison. The early-stop check is unvalidated.
DEFECT | MAJOR | Filtering tool outputs inside code and batching calls is already shipped, so the 2.0–2.4x is not new. The fair baseline is that practice, not a plain loop. | Anthropic's "Code execution with MCP" post (Nov 2025) reports 150k→2k tokens (98.7%). Programmatic Tool Calling reports about 37% fewer tokens; Cloudflare has "Code Mode".
DEFECT | MINOR | Scripts are output tokens at about 5x the input price, and this cost is not counted. | 300 extra script tokens per collapsed turn = 1,500 input-token equivalents, about 50% of a 30k cached read.
DEFECT | MINOR | It does not touch the asked cases: middle edits, insertions and reordering. | Scope.
SURVIVES | Reads making up about 75% of cost in a 150-turn cached session is plausible (my estimate: about 73%).
RATIO | 1.1 | Against code-execution/programmatic-tool-calling agents that already filter outputs.
KNOWN | yes | CodeAct (ICML'24); Anthropic code execution with MCP and Programmatic Tool Calling; Cloudflare Code Mode.
NEW FACT | Anthropic reports 150,000→2,000 tokens (98.7%) from code execution with on-demand tool loading (single example workflow). | https://www.anthropic.com/engineering/code-execution-with-mcp

IDEA 6: Hole-punch deletes via block-table edits
DEFECT | MAJOR | The output now depends on whether the cache survived. The hole-punched KV state cannot be rebuilt from the token sequence, so after eviction, or on another replica, recomputation gives a different state and different behavior. This breaks reproducibility and the "billed as a hit" semantics. | A hit and a miss of the same request produce different next-token distributions; the size of the difference is unmeasured.
DEFECT | MAJOR | It is a security showstopper for the most important reason to delete. Prompt injections or secrets in a removed tool result stay encoded in the KV of every later token. | The mechanism text itself says later tokens "still carry information" from the deleted span. No mitigation is given.
DEFECT | MAJOR | 12.5x applies only to the one-time suffix rewrite at each deletion event, not to session cost. | Suffix 1.25x→0.1x saves 1.15 × suffix once per clear. For one clear of a 50k suffix per 20 turns of 100k reads, the session saving is about 1.2–1.3x.
DEFECT | MINOR | The prior-art attributions are wrong: PyramidKV is per-layer KV budget allocation, not position gaps. H2O keeps original positions; StreamingLLM re-indexes positions within the cache. | PyramidKV paper (2024).
DEFECT | MINOR | Paged blocks hold 16 tokens in vLLM, so spans that do not align with block edges need partial-block copies. "Zero extra memory" is approximate. | vLLM block_size default 16.
SURVIVES | Zero recompute for the remaining blocks, freed memory, and a sound proposed test (KL divergence and top-1 agreement).
RATIO | 1.2 | Session-level saving from avoiding one suffix rewrite per clear, own stack only.
KNOWN | partly | llama.cpp `llama_kv_cache_seq_rm` and `seq_add` (context shift) delete spans and shift positions. KV eviction: StreamingLLM, H2O, SnapKV.

IDEA 7: Append-only errata with ski-rental compaction
DEFECT | MAJOR | The replay's 99.75% hit rate cannot match its own 365k billed units. Each of the 50 turns appends at least 2k new uncached tokens. | 100k new tokens at 1.25 = 125k units, leaving 240k for reads = 2.4M tokens, so hit ≤ 2.4M/2.5M = 96%. Conversely, 99.75% at 365k units implies only 8.9k missed tokens in total.
DEFECT | MAJOR | The baseline "edit earlier tool output in place" is not current practice. Normal agent loops already append new tool results, and Manus prescribes append-only context, so the −40% is against a straw man. | Manus blog: append-only context, deterministic serialization, KV-cache hit rate as the key metric.
DEFECT | MAJOR | Hash-sorted document order covers reordering only for the same set. Inserting or swapping one document breaks everything after its sorted slot, and the sort removes relevance ordering that RAG quality depends on. | With a random hash slot, inserting 1 document into n loses on average 50% of the document tokens. The lost-in-the-middle effect is a known quality cost of order changes.
DEFECT | MINOR | "KV matches full recomputation exactly" is true only for the erratum-augmented prompt, which is not the edited prompt. The quality question stays fully open and no test was run. | Stated by the idea itself.
SURVIVES | T* = 1,237.5 and 50 turns reproduce. For realistic session lengths the erratum is cheaper than a rewrite on cost alone.
RATIO | 1.05 | Against append-only agent loops with sorted JSON, which competent operators already run.
KNOWN | yes | Manus "Context Engineering for AI Agents: Lessons from Building Manus" (append-only, stable serialization). The compaction rule is the only increment.
NEW FACT | Manus calls KV-cache hit rate the single most important production metric for agents and re-writes todo.md at the end of context. The todo.md detail comes from secondary write-ups only. | https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus ; https://agentic-ai.readthedocs.io/en/latest/ContextEngineering/manus/

Sources:
- [Gemini 2.5 Pro cache pricing forum](https://discuss.ai.google.dev/t/gemini-2-5-pro-context-cache-pricing-per-request-vs-cumulative-token-counting/92919)
- [fast.io Gemini context caching](https://fast.io/resources/gemini-context-caching/)
- [Anthropic: Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [jiangren.com.au MCP code execution chapter](https://jiangren.com.au/en/learn/ai-engineer/mcp-code-execution)
- [Manus context engineering blog](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- [agentic-ai Manus summary](https://agentic-ai.readthedocs.io/en/latest/ContextEngineering/manus/)