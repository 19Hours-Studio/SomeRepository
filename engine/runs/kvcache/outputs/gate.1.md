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