The answer supports one real gain over best practice: a small one. If an agent already keeps its prompt append-only, sending small diffs ("errata") instead of re-sending whole changed tool outputs cuts billed input by about 3–11%, and only in synthetic replays. It does not raise the hit rate, and nobody has tested what it does to output quality.

**How I checked.** All four scripts in `round1/` re-run and give byte-identical output. I added my own sensitivity runs and wrote the results to `gain_check.md` in this folder.

**Hit rate.** The "~100% hit rate" is already what current practice gets. The append-only baseline also hits 1.0000 on re-sent tokens, and its total hit rate is 96.27% against 96.30% for errata. The big figures, −35.8% and −52%, are measured against editing the prompt in place. The answer itself concedes that coding agents and Manus's published guidance already avoid that.

**Idea 1 (client-side errata).** Against the append-only baseline it saves 11.0% at 50 turns (−10.9% at OpenAI prices). All of that comes from appending 200-token diffs instead of 2,000-token re-reads. In long sessions it drops to 3–7%. Agents that already append diff-sized edit results get close to nothing from it. It also carries a published quality risk (PI-LLM): models get worse at finding the latest value as stale copies pile up.

**Idea 2 (provider-side span delete/replace).** The −25% depends on one setting the answer chose: compacting at 195k down to 140k. In my runs the gain shrinks as compaction clears deeper:

| Compaction target | Span delete vs append-only |
|---|---|
| 140k | −24.5% |
| 100k | −12.2% |
| 40k | −5.2% |

On a wider grid, every policy's cheapest setting is to clear down to 10k. There span delete saves only 1.0% and span replace 5.4%, which is no better than client errata at 5.6%. The cached state it reuses is also approximate, and its quality was not tested.

**Idea 4 (park the cache in CPU memory during tool calls).** The 1.4–9.5x comparison mixes pricing bases: GPU memory at rental price, CPU memory at hardware cost. On the same rental basis it is 1.28–3.57x. More importantly, the baseline it beats (keeping the cache pinned in GPU memory) is not best practice. Offloading to CPU memory is already standard (LMCache, vLLM's offloading connector, SGLang HiCache), and Continuum, the cited prior art, uses vLLM with LMCache CPU offload as one of its own baselines. Against that, the gain is none.

**Quality.** No result in the answer was measured on a real model.

Sources: [Continuum (arXiv 2511.02230)](https://arxiv.org/pdf/2511.02230), [llm-d KV offloader](https://llm-d.ai/docs/architecture/advanced/kv-management/kv-offloader), [NVIDIA Dynamo KV offloading](https://docs.nvidia.com/dynamo/v1.0.1/additional-resources/v-llm-details/kv-cache-offloading), [LMCache overview](https://jimmysong.io/en/ai/lmcache)

HONEST GAIN: about −3% to −11% billed input against append-only best practice (synthetic replays only; no gain in hit rate, which append-only already has at ~100% on re-sent tokens; quality untested)