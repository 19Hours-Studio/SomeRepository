=== GATE ===
IDEA 1: Reversible eviction with offload
KILLER | Share of the offloaded KV that can be fetched over PCIe each decode step without stalling. This applies when many users run long contexts at once, which is the "3× users" regime the idea claims. I took 30% resident and FP8 KV on Llama-3.1-8B (64 KB/token) | required ≈2.2% of offloaded pages per step: a 1.56% top-k budget, fetching K+V pages Quest-style, ÷0.7 offloaded (1.1% if only V is fetched, as ShadowKV does) | available 0.64% per step = (0.3/0.7)×(50 GB/s PCIe ÷ 3.35 TB/s HBM) (exact arithmetic; 1.56% budget from ShadowKV, arXiv 2410.21465) | MARGIN 0.29 (0.57 if only V is fetched; about 2.1 for a single 128K request, where the weight read hides the transfer)
CHAIN | FP8 KV + PagedAttention in vLLM, ledger archetype A | now 1.00 cost per 128K request | with idea ≈0.83, because only 30% of the 25% decode-KV-read share stays on the GPU | RATIO 1.21 (the 3× concurrency claim is not reachable while the PCIe budget is below what fetching needs)
VERDICT | DEAD | In the multi-user regime it is pitched for, the step stalls on PCIe by about 3.5×, and in the single-request regime where the bandwidth fits, it saves only about 1.2×.
NEW FACT | Modern offloading methods become lossy, or need much higher PCIe budgets, on context-intensive tasks (Text2JSON). The authors blame landmark-based token selection, which is the same kind of scoring Quest uses | https://arxiv.org/pdf/2604.08426
NEW FACT | KVzip stays near-lossless at a 30% cache ratio on Qwen2.5-7B/14B, Llama-3.1-8B and Gemma3-12B (global layers only). It fails on one retrieval variant | https://arxiv.org/pdf/2505.23416
NEW FACT | ShadowKV achieves 6× larger batches and 3.04× throughput on A100, tested on 6 models. It keeps low-rank pre-RoPE K on the GPU and fetches only V | https://arxiv.org/abs/2410.21465
IDEA 2: Exact-prefix tiered KV reuse
KILLER | Load time from the slowest tier compared with recomputing prefill, for 20K tokens on Llama-3.1-8B (2.62 GB KV in BF16, 425 TFLOP prefill) | required load < 0.85 s, the prefill time at 500 TFLOP/s effective | available 0.052 s from CPU over PCIe Gen5 (~50 GB/s), 0.37 s from one Gen4 NVMe (~7 GB/s) (exact arithmetic) | MARGIN 16 (CPU tier) / 2.3 (NVMe tier)
CHAIN | vLLM GPU-only automatic prefix caching; the GPU holds about 22 contexts of 20K, against about 380 per TB of DRAM | now 0.78 of no-reuse cost at a 34% hit rate | with idea 0.66 at 55%, using Mooncake's measured hit-rate rise with cache capacity | RATIO 1.20 (1.52 against no reuse; the ~2.4× claim needs a 94% hit rate; 1.0 if LMCache is already deployed, as in ledger D)
VERDICT | WOUNDED | The physics has 2–16× headroom and outputs are exact, but this is already current practice (vLLM + LMCache). On real traces, the gain over GPU-only prefix caching is about 1.2×, not 2.4×.
NEW FACT | In the Mooncake trace, prefix-cache hit ratio rises from 34% to 55% as capacity grows from 1K to 50K blocks, with minimal gains beyond that | https://arxiv.org/pdf/2407.00079
NEW FACT | LMCache + vLLM reports up to 15× throughput on multi-round QA and document analysis | https://arxiv.org/abs/2510.09665
IDEA 3: Gated per-model FP8 KV
KILLER | How small an accuracy change a 30-minute RULER-128K check can detect. At about 28 GPU-s per 128K sample, that budget gives about 32 samples per configuration | required ±2 points, which needs about 1,730 paired samples at p≈0.9 | available ±14.7 points at a 95% half-width (measured: I checked the formula against a simulation, sd 0.0137 vs 0.0134; 28 s per sample comes from the ledger) | MARGIN 0.14
CHAIN | Blanket FP8 KV where it is known to be safe, BF16 elsewhere | now 1.00 | with idea ≥1.00, because gating can only add BF16 layers (1.14× only against all-BF16, by the idea's own figure) | RATIO 1.0
VERDICT | DEAD | The 30-minute check can only catch the "major" R1-Distill case, not a "meaningful" Gemma-3 loss, and it adds no gain over the existing FP8 default.
NEW FACT | vLLM found that FP8 NIAH accuracy at 128K on Hopper fell from 91% to 13%. The cause was FP32 accumulation in the kernel, not the FP8 format, and a fix restores it to near BF16. vLLM also ships `--kv-cache-dtype-skip-layers` and recommends skipping sliding-window layers | https://vllm.ai/blog/2026-04-22-fp8-kvcache
IDEA 4: Probe-gated per-layer precision
KILLER | Whether the FP8 failure is confined to a few layers. Per-layer gating only pays off if the share f of layers kept in BF16 is small (f ≤ 0.5 for RATIO ≥ 1.1) and probe KL predicts the RULER loss | required f ≤ 0.5, plus a positive KL→RULER correlation | available: no published per-layer breakdown for R1-Distill-Qwen-7B or Gemma-3-1B. The one documented large FP8 long-context failure was in the kernel and affected every layer, which per-layer gating cannot fix (vLLM blog). This needs a run on a real model | MARGIN unmeasured (about 0.5 provisional)
CHAIN | All-BF16 KV on models where blanket FP8 fails; per-layer skipping already exists in vLLM | now 1.00 | with idea 0.85 at f=0.25 (KV ×1.6; archetype A with BF16 KV read ≈40% of cost) | RATIO 1.18 (≤1.0 on models where FP8 is already safe)
VERDICT | WOUNDED | It is cheap and can be falsified with stock vLLM flags, but it only helps on the few models where FP8 fails, and then by at most about 1.2×. If the failures come from the kernel rather than from particular layers, gating reverts to all-BF16.
NEW FACT | The FP8 RULER study on 10 models found near-lossless results on 8 dense GQA models. Degradation was major on DeepSeek-R1-Distill-Qwen-7B and meaningful on Gemma-3-1B-IT. No per-layer data was published | https://www.plushcap.com/content/huggingface/blog/huggingface-fp8-kv-cache-on-intel-arctm-pro-b70-2-capacity-with-strong-long-context-throughput-gains

Notes:
- **What was run:** no measurement on a real model was possible here, since Hugging Face is blocked. The only thing I ran was the statistics check for Idea 3. Everything else is exact arithmetic or published numbers.
- **Inputs I did not verify:** the bandwidths (H100 3.35 TB/s, PCIe 50 GB/s, NVMe 7 GB/s) and 500 TFLOP/s are standard or ledger assumptions. I took ShadowKV's 1.56% budget from memory; the search excerpts did not show it.
- **Biggest open question for Idea 1:** how much of each step's top-k set is already resident or was fetched in the previous step. If that overlap is high, the PCIe need falls below 0.64%. This would need a run, for example ShadowKV or Quest code on Llama-3.1-8B with SCBench.
- **Files:** the arithmetic is in `/home/user/SomeRepository/engine/runs/kvcache/gate/c1/gate_calc.py` and its output in `gate_calc.out`. Nothing was committed.

Sources:
- [vLLM FP8 KV-cache blog](https://vllm.ai/blog/2026-04-22-fp8-kvcache)
- [HF FP8 KV on Intel Arc Pro B70 (mirror)](https://www.plushcap.com/content/huggingface/blog/huggingface-fp8-kv-cache-on-intel-arctm-pro-b70-2-capacity-with-strong-long-context-throughput-gains)
- [ShadowKV](https://arxiv.org/abs/2410.21465)
- [KV Cache Offloading for Context-Intensive Tasks](https://arxiv.org/pdf/2604.08426)
- [KVzip](https://arxiv.org/pdf/2505.23416)
- [LMCache](https://arxiv.org/abs/2510.09665)
- [Mooncake](https://arxiv.org/pdf/2407.00079)
- [Mooncake trace analysis](https://arxiv.org/pdf/2505.21919v1)
IDEA 5: Tiered exact-prefix KV reuse
KILLER | token hit rate h on a real trace (the idea's own kill line is h < 0.4) | required 0.40 | available 0.374 at unlimited capacity, 0.342 with a 16M-token cache (public Mooncake conversation trace, third-party analysis: llmtrafficlens on PyPI) | MARGIN 0.86–0.94
CHAIN | vLLM prefix caching plus LMCache or the vLLM OffloadingConnector (GPU→CPU→disk, hashed chunks, layer-by-layer overlapped loads). This is already the ledger D baseline. | now 1.15 GPU-s/request | with idea 1.15 GPU-s/request (same mechanism). Against no reuse it would be 1.15→0.89 at h=0.342 (1.29×) | RATIO 1.0
VERDICT | DEAD | It is the tool a competent practitioner already runs, so it adds 1.0× over best practice, and even against no reuse it gives about 1.3× on a public trace, below its own 1.3× line.
NEW FACT | Bandwidth is not the problem. Hiding the load needs 3.08 GB/s for BF16 and 1.54 GB/s for FP8 (128 or 64 KiB/token ÷ 42.6 µs/token computed for 20K prefill at 500 TFLOPs). PCIe4 x16 at about 25 GB/s gives a margin of about 8× | gate_calc.py (exact arithmetic, checked against the known 128 KiB/token for 8B and 320 KiB/token for 70B)
NEW FACT | LMCache already does per-layer CUDA-stream pipelining, CPU, local-disk, remote and Redis tiers, and chunks larger than vLLM's 16-token pages, and reports up to 15× throughput on multi-round QA | https://arxiv.org/abs/2510.09665
NEW FACT | vLLM's OffloadingConnector natively supports HBM→CPU→filesystem with an LRU CPU pool | https://llm-d.ai/docs/guides/tiered-prefix-cache ; https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/kv_cache_cpu_offload.html
IDEA 6: Exact tiered prefix store
KILLER | end-to-end throughput gain at h=0.5 (its own kill line is <1.5×) | required 1.50× | available 1.49× with zero load cost, 1.40× with 0.105 s of BF16 PCIe4 load not overlapped (ledger D shares: 66% prefill, 1.15 GPU-s; gate_calc.py) | MARGIN 0.93
CHAIN | vLLM prefix caching plus LMCache or OffloadingConnector (FP8 blocks across GPU, CPU and SSD, hashed block chains, overlapped streaming) | now 1.15 GPU-s/request | with idea 1.15 GPU-s/request | RATIO 1.0
VERDICT | DEAD | It describes shipping LMCache/vLLM behaviour, and it fails its own 1.5× line by arithmetic: 66% prefill × 50% hits caps the gain at 1.49×.
NEW FACT | Real hit rates depend heavily on the workload: 3.3% at a 16K-token cache, 18.5% at 4M, 34.2% at 16M, with a 37.4% ceiling on the Mooncake conversation trace. There is also an unverified blog claim of >90% for Kimi coding workloads | https://pypi.org/project/llmtrafficlens/0.6.2/ ; https://apidog.com/de/blog/kimi-k3-pricing
IDEA 7: FP8 tiered exact-prefix store
KILLER | its stated falsifier: hit TTFT over NVMe must be ≥3× lower than vLLM's GPU-only prefix cache at a matched hit rate | required NVMe TTFT ≤ 0.33 × GPU-hit TTFT | available NVMe TTFT ≥ 1 × GPU-hit TTFT, because a GPU-resident hit loads nothing while NVMe Gen4 at about 7 GB/s adds 0.19 s per 20K FP8 prefix (gate_calc.py) | MARGIN ≤0.33. Its stated bandwidth quantity passes: 7 / 1.54 GB/s = 4.5×.
CHAIN | vLLM prefix caching plus LMCache local-disk backend (native KV bytes, no codec, layer-by-layer loads) | now 1.15 GPU-s/request | with idea 1.15 GPU-s/request | RATIO 1.0
VERDICT | DEAD | Its falsifier is impossible by construction, and the mechanism (native FP8 bytes, tiered, layer-pipelined) is LMCache's existing disk path.
NEW FACT | "Bit-identical" is not given for free. Cached and recomputed prefixes go through different batch shapes and kernels, so exact equality needs a batch-invariant kernel mode and would have to be checked on a real model. That check is not possible here because Hugging Face is blocked | needs a run, not sourced
IDEA 8: Recompute-cost-per-byte store eviction
KILLER | hit-weighted FLOPs gained over LRU when the working set is compared with tier capacity (its own kill line is <15%) | required +15% | available at most +9.4% token-hit headroom at a 16M-token cache, which is only 1.05 TB of FP8 for 8B and fits one NVMe drive (Mooncake ceiling 37.4% vs 34.2%). Published policies report +8.1–23.9% hit rate over LRU and LFU (Alibaba, via a secondary summary), and FLOP-aware eviction gave only a 19–46% P95 win on LMSys and ShareGPT even for hybrid models (Marconi) | MARGIN 0.6–1.0
CHAIN | vLLM, LMCache or SGLang with LRU over GPU, CPU and SSD tiers | now 0.878 relative cost at h_LRU=0.185 (4M-token cache) or 0.774 at 0.342 (16M) | with idea 0.860 or 0.740 at +15%. Even reaching the ceiling of 0.374 gives only 1.17× | RATIO 1.02–1.05
VERDICT | DEAD | A better eviction policy only helps when capacity is short, and SSD tiers make capacity cheap, so the system-level gain is about 2–5% even if the 15% target is met.
NEW FACT | Production traces show that reuse is skewed, that single-turn reuse matters as much as multi-turn, and that the cache size needed for an ideal hit ratio is moderate | https://arxiv.org/abs/2506.02634 (USENIX ATC '25)
NEW FACT | Marconi's FLOP-aware eviction gives up to 34.4× hit rate, but only on hybrid SSM models and against modified vLLM+/SGLang+ baselines. On LMSys and ShareGPT the P95 win is 45.6% and 19.0% | https://arxiv.org/abs/2411.19379

Notes:
- **Ideas 1–3 are one idea.** All three describe exact prefix reuse with offload to CPU and SSD, which already exists in LMCache and in vLLM's own offloading. They die on RATIO (about 1.0× against current practice), not on physics: bandwidth headroom is 4–8×. The real gain they would bring against no reuse, about 1.3× at measured hit rates, is already counted in the ledger D baseline.
- **Numbers not measured.** I could not measure anything on a real model. The 42.6 µs/token prefill cost, the "bit-identical" claim and the end-to-end throughput all need a real-model run, for example replaying the Mooncake trace through vLLM with and without LMCache.
- **Trace data quality.** The hit rates come from a third-party analysis of one public trace. The Alibaba +8–24% figure comes from a secondary summary I could not check against the paper.

The calculations are in `/home/user/SomeRepository/engine/runs/kvcache/gate/c2/gate_calc.py`; nothing was committed.

Sources: [LMCache paper](https://arxiv.org/abs/2510.09665) · [LMCache docs](https://docs.lmcache.ai/developer_guide/integration.html) · [Marconi](https://arxiv.org/abs/2411.19379) · [KVCache in the Wild](https://arxiv.org/abs/2506.02634) · [llmtrafficlens Mooncake trace analysis](https://pypi.org/project/llmtrafficlens/0.6.2/) · [llm-d tiered prefix cache](https://llm-d.ai/docs/guides/tiered-prefix-cache) · [vLLM CPU offload guide](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/kv_cache_cpu_offload.html) · [Kimi K3 pricing blog](https://apidog.com/de/blog/kimi-k3-pricing)
