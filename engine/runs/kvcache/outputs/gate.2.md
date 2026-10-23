=== GATE ===
IDEA 1: Tiered exact-prefix KV reuse
KILLER | token hit rate h on a real trace (the idea's own kill line is h < 0.4) | required 0.40 | available 0.374 at unlimited capacity, 0.342 with a 16M-token cache (public Mooncake conversation trace, third-party analysis: llmtrafficlens on PyPI) | MARGIN 0.86–0.94
CHAIN | vLLM prefix caching plus LMCache or the vLLM OffloadingConnector (GPU→CPU→disk, hashed chunks, layer-by-layer overlapped loads). This is already the ledger D baseline. | now 1.15 GPU-s/request | with idea 1.15 GPU-s/request (same mechanism). Against no reuse it would be 1.15→0.89 at h=0.342 (1.29×) | RATIO 1.0
VERDICT | DEAD | It is the tool a competent practitioner already runs, so it adds 1.0× over best practice, and even against no reuse it gives about 1.3× on a public trace, below its own 1.3× line.
NEW FACT | Bandwidth is not the problem. Hiding the load needs 3.08 GB/s for BF16 and 1.54 GB/s for FP8 (128 or 64 KiB/token ÷ 42.6 µs/token computed for 20K prefill at 500 TFLOPs). PCIe4 x16 at about 25 GB/s gives a margin of about 8× | gate_calc.py (exact arithmetic, checked against the known 128 KiB/token for 8B and 320 KiB/token for 70B)
NEW FACT | LMCache already does per-layer CUDA-stream pipelining, CPU, local-disk, remote and Redis tiers, and chunks larger than vLLM's 16-token pages, and reports up to 15× throughput on multi-round QA | https://arxiv.org/abs/2510.09665
NEW FACT | vLLM's OffloadingConnector natively supports HBM→CPU→filesystem with an LRU CPU pool | https://llm-d.ai/docs/guides/tiered-prefix-cache ; https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/kv_cache_cpu_offload.html

IDEA 2: Exact tiered prefix store
KILLER | end-to-end throughput gain at h=0.5 (its own kill line is <1.5×) | required 1.50× | available 1.49× with zero load cost, 1.40× with 0.105 s of BF16 PCIe4 load not overlapped (ledger D shares: 66% prefill, 1.15 GPU-s; gate_calc.py) | MARGIN 0.93
CHAIN | vLLM prefix caching plus LMCache or OffloadingConnector (FP8 blocks across GPU, CPU and SSD, hashed block chains, overlapped streaming) | now 1.15 GPU-s/request | with idea 1.15 GPU-s/request | RATIO 1.0
VERDICT | DEAD | It describes shipping LMCache/vLLM behaviour, and it fails its own 1.5× line by arithmetic: 66% prefill × 50% hits caps the gain at 1.49×.
NEW FACT | Real hit rates depend heavily on the workload: 3.3% at a 16K-token cache, 18.5% at 4M, 34.2% at 16M, with a 37.4% ceiling on the Mooncake conversation trace. There is also an unverified blog claim of >90% for Kimi coding workloads | https://pypi.org/project/llmtrafficlens/0.6.2/ ; https://apidog.com/de/blog/kimi-k3-pricing

IDEA 3: FP8 tiered exact-prefix store
KILLER | its stated falsifier: hit TTFT over NVMe must be ≥3× lower than vLLM's GPU-only prefix cache at a matched hit rate | required NVMe TTFT ≤ 0.33 × GPU-hit TTFT | available NVMe TTFT ≥ 1 × GPU-hit TTFT, because a GPU-resident hit loads nothing while NVMe Gen4 at about 7 GB/s adds 0.19 s per 20K FP8 prefix (gate_calc.py) | MARGIN ≤0.33. Its stated bandwidth quantity passes: 7 / 1.54 GB/s = 4.5×.
CHAIN | vLLM prefix caching plus LMCache local-disk backend (native KV bytes, no codec, layer-by-layer loads) | now 1.15 GPU-s/request | with idea 1.15 GPU-s/request | RATIO 1.0
VERDICT | DEAD | Its falsifier is impossible by construction, and the mechanism (native FP8 bytes, tiered, layer-pipelined) is LMCache's existing disk path.
NEW FACT | "Bit-identical" is not given for free. Cached and recomputed prefixes go through different batch shapes and kernels, so exact equality needs a batch-invariant kernel mode and would have to be checked on a real model. That check is not possible here because Hugging Face is blocked | needs a run, not sourced

IDEA 4: Recompute-cost-per-byte store eviction
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