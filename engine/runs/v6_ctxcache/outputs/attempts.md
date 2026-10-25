=== ATTEMPTS ===

Figures below are the authors' own results unless I say otherwise. Many come from vendor blogs, and I did not verify them independently.

ATTEMPT 1: Exact-prefix caching on hosted APIs (Anthropic breakpoints, OpenAI automatic) | providers, 2024–26 | standard | WHY IT DID NOT SOLVE IT: byte-exact prefix match, so the first changed token ends reuse. Anthropic also checks only about 20 blocks back from a breakpoint. Third-party sources put OpenAI's discount at 50% with a 1,024-token minimum, and I could not confirm that from official pages. Reads cost about 0.1× and writes about 1.25× on Anthropic, per third-party sources, so the discount caps at ~90% and only on the unchanged prefix. | [Anthropic docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching), [pricing blog](https://www.tkmxai.it.com/prompt-caching-pricing)

ATTEMPT 2: Prompt discipline, meaning append-only context, stable tool order and no timestamps | Manus, 2025 | standard | WHY: it works only if nothing in the middle ever changes. A second-precision timestamp at the top voids the cache. The cached rate was $0.30 vs $3.00 per million tokens (10×), with ~50 tool calls and a 100:1 input:output ratio per task. It cannot handle reordering, insertion or edits. | [Manus](https://manus.im/en/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)

ATTEMPT 3: Self-hosted prefix reuse (vLLM block-hash, SGLang radix tree) | open source, 2023–26 | standard | WHY: vLLM chains 16-token block hashes, so a hit needs every earlier token to match. Radix matching only moves the boundary to any token. SGLang's 6.4× gain on RAG is reported to vanish when prefix order varies. Production hit rates are reported at 50–99%, depending on prompt discipline. | [Momento](https://www.gomomento.com/blog/vllms-hash-chain-and-why-prefix-caching-is-still-prefix-caching/), [Spheron](https://www.spheron.network/blog/vllm-vs-sglang-2026/)

ATTEMPT 4: KV offload to CPU, disk or network (LMCache, Dynamo, Ray) | open source and vendors | standard | WHY: it raises capacity but not matching. A hit still requires the same prefix, and each load costs bandwidth. One vendor benchmark: Qwen3-32B at ~131K tokens drops from 11 s to 1.5 s TTFT. Quantised offload raised the hit rate from 75.2% to 86.8% at a fixed memory budget, not to ~100%. | [Ray](https://docs.ray.io/en/latest/serve/llm/user-guides/kv-cache-offloading.html), [AMD](https://rocm.blogs.amd.com/software-tools-optimization/4bit-KV-LMcache/README.html)

ATTEMPT 5: KV compression and eviction (H2O, SnapKV, StreamingLLM) | academia, 2023–24 | niche | WHY: it shrinks the decode-time cache, not prefill, because the full KV must be built first. At 200k tokens, full prefill took 82.4 s and Ada-SnapKV took 88.4 s (+7.2%). Methods that do cut prefill lose accuracy at useful budgets. | [FastKV](https://arxiv.org/html/2502.01068v3)

ATTEMPT 6: Prompt Cache (modular schema, own position IDs per module) | Yale and Google, MLSys 2024 | niche | WHY: needs a prompt markup language to define modules up front. Modules are encoded without seeing each other, so cross-module attention is lost. It reports 8× (GPU) and 60× (CPU) TTFT gains. I did not see its accuracy tables. | [arXiv](https://arxiv.org/abs/2311.04934)

ATTEMPT 7: CacheBlend (reuse chunk KV at any position, recompute ~15% of tokens) | Chicago and LMCache, EuroSys '25 | niche (in LMCache) | WHY: it needs own-stack access to KV tensors, so it cannot run on a hosted API. Gains are 2.2–3.3× TTFT and 2.8–5× throughput, not ~10×. Recomputation is still ~15%. The "100% hit rate" in the LMCache blog is marketing, not a measured result. | [arXiv](https://arxiv.org/html/2405.16444v3), [LMCache](https://blog.lmcache.ai/2025-03-31-eurosys)

ATTEMPT 8: EPIC / LegoLink (position-independent caching that suppresses the attention-sink artefact at each chunk start) | ICML 2025 | niche | WHY: it still recomputes a few tokens per chunk and needs own-stack access. It claims up to 8× TTFT with negligible accuracy loss. The evidence is the authors' experiments only, with no independent replication that I found. | [PMLR](https://proceedings.mlr.press/v267/hu25j.html)

ATTEMPT 9: Cache-Craft (chunk caches with selective recompute and cache management) | 2025 | niche | WHY: it recomputes ~30% of tokens and keeps only ~90% of base ROUGE F1. It saved 51% of GPU compute vs prefix caching, not ~100%. | [arXiv](https://arxiv.org/pdf/2502.15734)

ATTEMPT 10: Block-Attention (independent blocks, re-encoded positions) | ICLR 2025 | niche | WHY: it needs fine-tuning, which the constraints exclude. At 32K tokens it cut TTFT by 98.7% and FLOPs by 99.8%. | [arXiv](https://arxiv.org/abs/2409.15355v5)

ATTEMPT 11: TurboRAG (precomputed chunk KV, independent attention, reordered RoPE) | EMNLP 2025 | niche | WHY: the arXiv abstract says it fine-tunes the model, but the EMNLP abstract does not say so. It reports TTFT down 8.6× on average and up to 9.4×. It is limited to RAG chunk stores on own infrastructure. | [arXiv](https://arxiv.org/abs/2410.07590)

ATTEMPT 12: Training-free reuse tested on reasoning tasks (KVShareArena 2026, Kamera 2026) | preprints | rejected as a general fix | WHY: quality depends on the model. Position alignment alone scores 0.41 on multi-hop with Llama-3.1-8B but 0.03 with Qwen3-8B. CacheBlend helps on Qwen3 but not Llama. Blind reuse took Kamera's multimodal reasoning from 0.59 to 0.41. A rank-16 patch recovered it to 0.64, which suggests a missing cross-chunk signal. These are non-peer-reviewed preprints. | [KVShareArena](https://arxiv.org/pdf/2609.10266), [Kamera](https://arxiv.org/pdf/2606.23581)

ATTEMPT 13: Trained encoder for position-independent caching (COMB) | 2026 preprint | rejected under these constraints | WHY: it argues existing training-free position-independent caching "often causes substantial accuracy loss" and so trains a component, which the no-training rule forbids. | [arXiv](https://www.arxiv.org/abs/2602.01519)

ATTEMPT 14: Semantic response caching (GPTCache, MeanCache, InstCache) | open source and academia, 2023–25 | niche, Thoughtworks "assess" | WHY: it caches the answer, not the KV, so it is wrong whenever context matters. In MeanCache's test, GPTCache gave 54 false hits on 250 queries that should have missed. InstCache measured 29.9% and 33.6% mismatch (LLM-judged) at thresholds 0.9 and 0.95. | [MeanCache](https://arxiv.org/pdf/2403.02694), [InstCache](https://arxiv.org/pdf/2411.13820)

ATTEMPT 15: Prompt compression (LLMLingua) | Microsoft, 2023 | niche | WHY: it makes the prompt shorter but changes its tokens, so the exact-prefix match breaks unless the compressed text is itself stable. It reached 20× with a 1.5-point drop on its own benchmarks (GSM8K, BBH, ShareGPT, Arxiv-March23). | [arXiv](https://arxiv.org/pdf/2310.05736)

ATTEMPT 16: Context editing, clearing old tool results (Anthropic) | 2025 | standard | WHY: each clear invalidates the cached prefix from that point and forces a new write. The docs' own mitigation is a `clear_at_least` threshold, which means it only pays off when a lot is cleared at once. | [Anthropic](https://platform.claude.com/docs/en/build-with-claude/context-editing)

LESSONS:
- Hosted APIs expose only exact-prefix matching and no KV handles, so the position-independent methods (attempts 6–11) cannot run client-side. They need your own serving stack, or the provider itself would have to adopt them.
- Every training-free position-independent method either recomputes a share of tokens (15–30%) or loses accuracy. The loss is worst on multi-hop reasoning and varies by model (attempt 12). Anything claiming ~100% hits needs a quality test per model.
- Methods that skip recomputation fully need fine-tuning or a trained component (attempts 10, 13). That is excluded here.
- Whatever hit rate is counted, the speedups reported are 2–9×, and the effective cost depends on the recompute share and the load bandwidth.
- Client-only options (attempts 2, 16) just reduce the damage from changes. Edits, insertions and reordering in the middle stay uncached, so about 100% is unreachable on a hosted API.
- Gaps: I did not verify official OpenAI or Anthropic pricing pages, per-token KV storage cost, or RAGCache's hit rates.