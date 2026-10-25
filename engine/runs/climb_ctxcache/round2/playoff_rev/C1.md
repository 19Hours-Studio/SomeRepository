I couldn't make cached context "much cheaper" by raising hit rates on non-identical prefixes, because that is a small slice of real traffic. I replayed 269,681 production requests (Alibaba Bailian: chat, API, coder and reasoning workloads) and the 200 SWE-agent sessions from the current answer:
- **Production sessions:** mid-prompt changes cost 0.00% of input. Chat edits show up as branches from an earlier turn, and those are still prefix hits.
- **Non-prefix reuse across requests:** it is 1.2% of chat input and 6.8% of API input. This is a lower bound, because only content that happens to align with the 16-token blocks is visible.
- **Agents:** the exact append-only hit rate is already 97.1%.

The real cost sits elsewhere. On your own stack, once prefix caching works, **49–69% of GPU time on agent sessions goes to decode re-reading the cached KV**. Lossless copy-speculation cuts that by **21–34% of GPU time** on GQA models (multi-head models with grouped KV heads), and the output does not change. Every mechanism below except Idea 5 keeps the prompt and KV exactly what a full recompute would use. Near-100% hit rate is impossible: the exact ceilings are 46–71% on production traffic and 97.9% on agents.

=== WHERE THE COST OF CACHED CONTEXT ACTUALLY IS ===

- **Production traffic (Bailian, 2 h window; Anthropic-style pricing; "∞" = an unbounded cache).**

| Workload | Hit at 5-min TTL | Hit at ∞ | Lost to mid-prompt edits in a session | Prior reply re-sent as new input | Output share of bill |
|---|---|---|---|---|---|
| Chat (A) | 46.2% | 57.8% | 0.00% | 8.8% | 56% |
| Coder | 57.3% | 66.4% | 0.00% | 5.2% | 54% |
| Reasoning | 43.1% | 46.2% | 0.00% | 2.6% | 83% |
| API (B, no sessions) | 51.2% | 53.4% | n/a | n/a | — |

- **Agents on your own stack.** I replayed the 200 SWE-agent sessions append-only, with exact prefix caching and the measured tool execution times (`agent_gpu.txt`). GPU time splits like this:

| Model | Prefill of new tokens | Prefill attention over cache | Decode weight reads | Decode re-reads of cached KV | KV idle during tool runs |
|---|---|---|---|---|---|
| Dense 72B GQA, BF16 KV | 14.5% | 7.9% | 22.2% | **52.1%** | 3.3% |
| Dense 72B GQA, FP8 KV | 20.0% | 10.9% | 30.7% | **36.0%** | 2.3% |
| DeepSeek-V3 MLA, FP8 KV | 18.5% | 37.5% | 14.2% | 27.9% | 1.8% |
| 30B-A3B MoE, BF16 KV | 3.1% | 10.9% | 9.4% | **72.0%** | 4.6% |

  - Misses (new tokens) are only 3–20% of GPU time. A perfect hit rate would remove at most that.
  - Offloading KV while tools run (the InferCept idea) is worth 2–5% at most.

=== IDEAS ===

**IDEA 1: Spread each read of the cached KV over several output tokens with lossless copy-speculation (own stack or provider)**

- **Mechanism.**
  - Look up the last 3 tokens in everything the model has seen: the prompt plus the text generated so far.
  - Propose the up to K tokens that followed the most recent match. One verify pass reads the KV once for all of them.
  - Greedy acceptance, or standard speculative rejection sampling when sampling, keeps the output identical to normal decoding.
- **Measured on the real agent outputs** (temperature 0, so acceptance means an exact match; `copyspec.txt`):
  - 1.82, 1.99 and 2.10 tokens per pass at K = 4, 8 and 16.
  - With a finer token split the figure is 2.3–3.0. Agents copy a lot: `old_str` arguments, file paths, identifiers.
- **GPU-hour effect** (`agent_gpu_spec.txt`; a conservative model that adds compute time and memory time without overlap):

| Model | K=4 | K=8 | K=16 |
|---|---|---|---|
| Dense 72B, BF16 KV | −26.6% | −27.1% | −23.6% |
| Dense 72B, FP8 KV | −21.0% | −20.1% | −14.5% |
| 30B-A3B, BF16 KV | −32.0% | −33.9% | −32.4% |
| DeepSeek-V3 MLA | −4.7% | +0.2% | +11.8% |

  - On MLA, verify passes become compute-bound, so use K ≤ 4 or turn it off.
- **Cases covered.** All four (middle edit, insertion, tool output, reordering). It does not care how the prefix changed, and the hit rate is unchanged: it lowers the cost of each hit.
  - It also composes with clearing, splicing and segment reuse. Shorter context from the current answer's clearing reduces the same re-reads.
- **Quality.** Output is identical by construction.
  - Test: bit-equality of greedy outputs with and without speculation on replayed prompts, using the same kernels. Batch-shape numerics can flip rare tokens, so compare against a baseline with matching batching.
- **Costs.**
  - An n-gram index on the CPU, a few bytes per context token.
  - Extra verify compute: ρ = 0.9–2.3 proposed tokens per output token.
  - Latency per output token goes down.
- **Prior art.** Prompt Lookup Decoding, LLMA, SuffixDecoding (up to 5.3× on SWE-bench), and MagicDec (speculation pays in the long-context, KV-bound regime).
- **What this adds.**
  - After prefix caching, this is the largest exact lever left on the cost of cached context for agents. The whole remaining hit-rate gap (97.1% → 100%) is worth less.
  - Per-model GPU-hour effects, including where it does not pay (MLA).
  - τ was measured with simple trigram lookup; SuffixDecoding reports more, so these numbers are a floor.
- **Plain API users** cannot apply this. A provider that does could price cached reads lower.

**IDEA 2: Keep the KV produced while decoding the reply, so the next turn hits it (provider or own stack; exact)**

- **Today.** The previous reply comes back as new input. Anthropic bills it as a 1.25× write, even though the server computed that KV moments earlier.
- **Measured** (`exact_ceiling.txt`, `carry_swe.txt`, `controller.txt`):

| Workload | Hit rate | Billed input | Provider prefill |
|---|---|---|---|
| Chat | 46.2% → 52.3% | −9.8% | −4.2% |
| Coder | | −6.3% | −3.5% |
| Reasoning | | −3.2% | −2.8% |
| Agents | 97.1% → 97.9% | −6.4% | — |

- **Cases covered.** None of the four. It removes a separate miss class: the reply re-sent as input.
- **Quality.** Exact, but only if the re-sent reply re-tokenises identically and the chat template neither strips nor inserts anything.
  - It breaks when previous reasoning is stripped. Bailian's FAQ says its app drops `<think>` tags, and Claude drops earlier thinking blocks outside tool loops.
  - Test: the rate of token-ID identity between the generated sequence and the re-rendered prompt.
- **Costs.** None, beyond keeping the reply's KV in the same tier as the prompt.
- **Prior art.** SGLang's radix cache and vLLM already cache generated blocks. What this adds is the measured value, plus the gap in API billing and in the token-identity contract.

**IDEA 3: Retention by cost, not by hit rate (provider or own stack; exact)**

- **When does keeping KV for an hour pay?** Compare storage cost with the prefill it saves (`keep_cost.txt`). A ratio above 1 means it costs more than it saves:

| Model | DRAM, keep everything | NVMe, keep everything | NVMe, oracle keeps only returning blocks |
|---|---|---|---|
| Dense 72B | 27–31× | 0.57–0.65× | 0.03–0.05× |
| 30B-A3B MoE | 176–201× | 3.7–4.3× | 0.22–0.30× |

  - Keeping everything stores about 17× more than the oracle, so predicting which sessions return is the real lever.
- **Controller.** Choose an NVMe keep time per (turn, type) category. It was trained on even-numbered sessions and scored on odd ones (`controller.txt`). Change in each workload's whole prefill bill, with carry-over included:

| Policy | Dense, chat | Dense, coder | MoE, chat | MoE, coder |
|---|---|---|---|---|
| Keep everything 1 h | −2.6% | +4.4% | **+55%** | **+107%** |
| Trained keep time | **−8.5%** | **−6.9%** | −4.3% | −3.6% |
| Oracle | −12.7% | −13.4% | −11.2% | −10.5% |

  - For the MoE model the controller learns to keep almost nothing beyond 5 minutes.
- **Cases covered.** None of the four: this is TTL misses. Quality is exact.
- **Prior art.** KVCache-in-the-Wild (ATC'25) proposed category-aware eviction, with hit ratio as the objective. Mooncake, LMCache and HiCache provide the storage tiers.
- **What this adds.** A dollar objective using each model's FLOPs per KV byte. For a model with few active parameters, the cost-optimal hit rate is far below 100%: chasing hit rate raises cost.

**IDEA 4: Client-only retention settings, measured (any API)**

- **OpenAI.** `prompt_cache_retention="24h"` costs the same as the default on the models that support it (`openai_retention.txt`). Billed input against the 5-minute default:
  - chat −17.8%, coder −16.9%, reasoning −4.6%, API −3.8%;
  - about half of that against a 10-minute default.
  - It is exact and free. GPT-5.6 and later changed this: a 30-minute minimum TTL, and cache writes are billed.
- **Anthropic: keep the defaults.** Billed input against the 5-minute default (`retain_fixed.txt`, `policy.txt`):
  - a 1-hour TTL on every write: +25% (chat, coder), +49% (reasoning);
  - Aider-style 2 keep-alive pings: +3% to +20%;
  - an online per-request choice between skip-write, 5 min and 1 h: −1.0% on chat, but +46% on coder, because skipping writes breaks prefixes that other sessions share;
  - an oracle on chat: −21.8%. The money is in knowing whether the user comes back, not in the TTL setting.

**IDEA 5: Position-independent segment reuse, only where the prize exists (provider or own stack; approximate)**

- **Measured prize** (`reuse.txt`, `taxonomy.txt`, `swe_crossreuse.txt`):
  - **Chat:** 1.2% of input (block-aligned runs of ≥2 blocks): 71% content from another request, 16% reordered, 13% insertion or edit of a known prompt.
  - **API:** 6.8%: 78% other-source, 20% insertion or edit, 1% reordered.
    - A typical API request diverges for only about 4 blocks (64 tokens, the median) and then resumes reused content. That points to a volatile field near the top of the prompt.
  - **Agents:** 8.3% of tool output was already seen in an earlier trajectory, and 9.6% earlier in the same one. That caps the value at a few percent of the agent bill.
- **Under-detection.** The 16-token block alignment hides misaligned reuse. Irminsul reports that fixed blocks find 3.8–4.8× less reuse than content-defined chunks. That puts a plausible range at about 1–6% for chat and 7–33% for API traffic.
- **Mechanism.** Content-defined chunk keys plus EPIC, CacheBlend or Irminsul, with a gate that falls back to recompute when deviation is too high. Enable it only for workloads whose measured non-prefix share justifies it.
- **Cases covered.** All four, but approximately.
- **Quality.** Not exact. FusionRAG reports that 7B with 15% recompute only reaches 3B-level quality. Test with KL divergence and top-1 agreement against full recompute, plus LongBench and 2WikiMQA. That needs a real model.

**What cannot reach about 100%:**
- **Exact KV after any change at position p.** Every later token's KV depends on all earlier tokens, so exact hit rate ≤ p/L. Only approximate reuse (Idea 5) gets past this, at unmeasured quality.
- **Production traffic.** Even an unbounded exact cache with carry-over tops out at 66.4% (chat), 71.2% (coder), 48.5% (reasoning) and 53.4% (API). The other 29–52% of tokens are new content.
- **Agents** top out at 97.9%.
- **Hit rate and cost trade off.** Keeping everything for 1 hour costs +55% to +178% for MoE models. A 1-hour TTL raises Anthropic bills by about 25%.
- **Output is 54–83% of the bill** on production traffic. Caching never touches it; only Idea 1 lowers its GPU cost.

=== NOTES ===
- **Calibration.**
  - Prices and hardware assumptions are listed in `README.md`.
  - The replay's token estimate (chars/3.5) gives bills 1.30× below the dollars SWE-agent actually recorded (`calibrate.txt`). Absolute values are about 30% low; ratios are unaffected.
  - τ uses GPT-2 pre-tokenizer pieces as tokens.
- **Limits of the data.**
  - The Bailian window is 2 hours, so gaps longer than about 1 hour are censored.
  - The replays share one cache across all users, while API caches are scoped per organisation.
  - The Bailian traces are a proxy for user behaviour; the prices are Anthropic's and OpenAI's.
- **Needs a real model** (no weights could be downloaded here):
  - τ for the target model's own outputs and tokenizer;
  - the bit-equality test for Idea 1;
  - token identity for Idea 2;
  - all quality numbers for Idea 5.
- **Compared with the current answer.** It saves money by showing the model less context. Everything here except Idea 5 keeps the context and KV exact, and Idea 1 stacks with its clearing.

Sources:
- [Qwen-Bailian traces](https://github.com/alibaba-edu/qwen-bailian-usagetraces-anon) · [KVCache in the Wild (ATC'25)](https://arxiv.org/pdf/2506.02634) · [Qwen-Bailian dataset overview](https://autoinf-qwen-bailian-trace-windows.static.hf.space/reports/detailed/index.html)
- [SuffixDecoding](https://arxiv.org/abs/2411.04975v2) · [MagicDec](https://arxiv.org/html/2408.11049v5)
- [Irminsul](https://arxiv.org/pdf/2605.05696) · [EPIC](https://arxiv.org/abs/2410.15332v3) · [CacheBlend](https://arxiv.org/html/2405.16444v3) · [FusionRAG](https://arxiv.org/pdf/2601.12904)
- [OpenAI prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) · [Azure prompt caching](https://learn.microsoft.com/en-my/Azure/foundry/openai/how-to/prompt-caching) · [Anthropic prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching) · [Helicone prompt caching](https://docs.helicone.ai/gateway/concepts/prompt-caching) · [OpenRouter prompt caching](https://openrouter.ai/docs/prompt-caching)
- [SWE-bench experiments](https://github.com/SWE-bench/experiments)

Everything is in `/home/user/SomeRepository/engine/runs/climb_ctxcache/round2/fresh/`. All outputs were re-run from scratch and reproduced identically. `README.md` lists the commands and assumptions:
- `scripts/fetch_data.sh`: fetches the data and checks it against `data/SHA256SUMS`
- `scripts/run_all.sh`: re-runs everything (about 35–40 minutes)
- `out/`: one output file per script

HONEST GAIN: These gains need no quality caveat:
- **Own stack, agents:** lossless copy-speculation cuts GPU time by 21–34% on GQA models (about 0 on MLA).
- **Provider:**
  - reply-KV carry-over cuts billed input by 6.4% (agents) and 9.8% (chat);
  - cost-based retention cuts the prefill bill by 8.5% (dense chat) and avoids the +55–107% that keeping everything costs on MoE.
- **OpenAI clients:** the free 24h retention flag cuts billed input by 17–18% on chat and coder.

The non-prefix prize that the question targets measures 0% inside sessions and 1–7% (block-aligned) across requests.