=== IDEAS ===
IDEA 1
NAME: Hybrid-bonded DRAM-on-logic decode package
MECHANISM: Continuum targets one workload: decode for frontier sparse-MoE LLMs (1T total / 32B active parameters) at 8K–128K context. The main metric is tokens/s per kW at a per-user speed target (100, 400 or 1000 tok/s/user), with tokens per joule second. Peak FLOPS is not a metric. Serving revenue comes from throughput at an interactivity target, and running cost comes from joules. The package has four ~400 mm² N2-class logic chiplets. Each sits on top of a 4-high custom DRAM stack, bonded die to die at ≤9 µm pitch (hybrid bonding). That gives 160 GB at 64 TB/s per package, at about 0.8 pJ/bit. HBM is around 3 pJ/bit (my estimate), and a published 3D-DRAM estimate gives 0.66–0.88. Compute is 40 PF dense FP4 and 20 PF FP8, in a ~2.0 kW package. Stacked-DRAM power is 64 TB/s × 8 × 0.8 pJ = 410 W. FP8 at full rate would be about 1.6 kW, so the 2 kW budget is shared and the memory and FP8 cannot both run flat out. The package has no HBM. My model found that adding an HBM tier lowered tokens/s per kW, because each decode step reads all resident bytes and the slow tier sets the step time. On the same 4.5-bit weight and KV format, the roofline/energy model compares it with Rubin (288 GB, 22 TB/s, ~1.8 kW). For GQA models, Continuum gets 2.2–2.7× the tokens/s per kW and 2.3–2.5× the tokens/J, at both 8K and 128K. For dense-MLA models it gets only 1.08–1.29×, because MLA decode at 128K costs about 1.1 TFLOP per token in attention and is compute-bound.
VALUE: In my model, Continuum gives about 2.2–2.7× more decode tokens per kW than Rubin on GQA models (2.8–3.8× vs Ironwood, 4–18× vs Groq LP30 and WSE-3). That is a modeled result, not a measured one, and it hinges on the stacked DRAM really reaching ≤1 pJ/bit and 64 TB/s.

IDEA 2
NAME: Attention-balanced compute with sparse-KV gather
MECHANISM: Bandwidth alone does not win on MLA models. Their decode needs about 430 FLOP per byte, while Continuum's compute-to-bandwidth balance point is 20 PF / 64 TB/s = 312 FLOP/byte. Attention therefore needs FP4/FP8 matrix math with per-block scales. The chip also needs a hardware engine for DeepSeek-V3.2-style sparse attention (DSA): a top-k indexer plus a gather unit. This cuts the 128K attention cost from about 1.1 TFLOP to about 150 GFLOP per token (an FP8 indexer plus top-2048 attention). The KV rows it fetches are random ~324 B reads. Stacked DRAM with many banks suits those far better than HBM's long bursts, but this needs a cycle-level simulator to confirm. With DSA, the model shows 1.8–2.7× Rubin's tokens/s per kW at 128K and 1.8× its tokens/J, against 1.1–1.3× for dense MLA.
VALUE: This keeps the lead at 1.8–2.7× on new sparse-attention models instead of the 1.1× it falls to on dense MLA. Without it, Continuum is only marginally better than Rubin on DeepSeek/Kimi-class models.

IDEA 3
NAME: Decode-only part, disaggregated prefill/training
MECHANISM: I reject the premise that one chip should be best at training and inference. Prefill and training are compute-bound and need capacity: optimizer states, and prompts that use GDDR or HBM well, as Rubin CPX shows with 30 PF NVFP4 and 128 GB GDDR7. Continuum has 160 GB per package against Rubin's 288 GB, so it needs about 1.6–2× more packages for pools with very large KV caches. It also does not beat Rubin on training. The system therefore pairs Continuum decode racks with HBM or GDDR prefill/training parts, linked by KV transfer. Each package has 3.6 TB/s of NVLink-6-class scale-up, in 72-package copper racks. On maximum single-user speed it loses. Expert-parallel all-to-alls (120 per token × ~3 µs) cap it at about 2.8k tok/s/user, the same as Rubin. SRAM chips model at about 8k (Groq) and measure about 2.2k (Cerebras on gpt-oss-120B). Matching them would need about 1.5 µs collectives, which is unproven.
VALUE: Continuum is aimed at the bulk serving market, about 2× tokens per kW against Rubin + CPX-style disaggregation. It concedes ultra-low-latency single-user speed to Groq LPX and Cerebras, and training to Rubin and TPU.

IDEA 4
NAME: 4.5-bit numerics, compiler-placed memory, kill gates
MECHANISM: Weights and KV are stored as NVFP4/MXFP4 at about 4.5 bits, activations are FP8, and accumulation is FP32. Existing checkpoints run after post-training quantization; they do not need retraining. The software stack is PyTorch/JAX → torch.export/StableHLO → MLIR, with Triton-style tile kernels and vLLM/SGLang backends. The compiler places experts statically in stacked DRAM and pages the KV cache. CUDA-only kernels need porting, which is the adoption cost. Five tests could kill the design:
1. Recalibrate the model against MLPerf and Artificial Analysis. Drop the design if the GQA-128K lead is below 1.5×.
2. Run 3D thermal and power simulation (3D-ICE/HotSpot plus a power-integrity tool). It fails if DRAM runs above 95 °C, or if IR drop exceeds 5% while delivering about 2,700 A at 0.75 V through the DRAM stack.
3. Model the DRAM in CACTI-3DD/Accelergy. It fails above 1.5 pJ/bit or below 40 TB/s per package.
4. Simulate in LLMCompass with real expert-routing traces.
5. Run RULER at 128K with NVFP4 KV. The numerics plan fails if it loses more than 1 point against BF16.
VALUE: Models and frameworks carry over with quantization only, and every headline ratio has a test that can prove it wrong before tape-out.

NOTES
- **Established facts (vendor or press figures):**
  - Rubin: 50 PF NVFP4, 288 GB HBM4, 22 TB/s, NVLink 3.6 TB/s. The ~1.8 kW power figure is only a press estimate, and the FP8 figure of 16 PF is my assumption.
  - Ironwood: 4,614 TFLOPS FP8, 192 GiB, 7.38 TB/s, 1.2 TB/s ICI, 9,216-chip pods. Its ~1 kW power is my assumption.
  - WSE-3: 44 GB SRAM, 21 PB/s, 125 PF sparse / 12.5 PF dense FP16, 23 kW system.
  - Groq: LPU-1 had 230 MB at 80 TB/s. LP30 has 500 MB and 1.2 PF FP8, and an LPX rack is 256 chips with 128 GB total. LP30's 150 TB/s and 0.5 kW are my assumptions.
  - Rubin CPX: 30 PF NVFP4, 128 GB GDDR7.
  - HBM4 (JESD270-4): 2048-bit, 8 Gb/s per pin, 2 TB/s per stack, up to 64 GB.
  - CoWoS capacity: about 95–130k wafers/month at end-2026 (analyst estimates).
  - Artificial Analysis, gpt-oss-120B: Cerebras about 1.85–2.19k tok/s, Groq about 475 tok/s.
- **My assumptions (not checked):** every Continuum block spec; 0.045/0.08 pJ per FP4/FP8 FLOP; 3 / 0.8 / 0.25 pJ/bit for HBM / stacked DRAM / SRAM; 70% compute efficiency; perfect load balance; uniform expert routing; 25% static power. Absolute numbers need a simulator or silicon; only the ratios are meaningful.
- **Main risks:** delivering power through the DRAM stack, and DRAM temperature under hot logic; a custom high-bank-count DRAM die that no vendor makes today; bonding yield (needs known-good-die, die-to-wafer bonding); hybrid-bonding capacity being smaller than CoWoS.
- **Files** (in `/home/user/SomeRepository/engine/runs/v6_continuum/baseline_1/`, nothing committed): the design note `CONTINUUM.md`; the model scripts `roofline.py`, `variants.py` and `final.py`; and their outputs `final_out.txt` and `variants_out.txt`.
- **Sources:**
  - [The Register: Rubin at CES](https://www.theregister.com/2026/01/05/ces_rubin_nvidia/)
  - [cyfuture: Rubin](https://cyfuture.ai/nvidia-vera-rubin-gpu)
  - [hyper.ai: Rubin power estimate](https://hyper.ai/en/stories/3422d6a72152beb34a564461208438ff)
  - [Google TPU7x docs](https://docs.cloud.google.com/tpu/docs/tpu7x?authuser=0)
  - [The Register: Ironwood](https://www.theregister.com/2025/11/06/googles_ironwood_tpus_ai/)
  - [DCD: WSE-3](https://www.datacenterdynamics.com/en/news/cerebras-unveils-four-trillion-transistor-giant-chip-targets-generative-ai)
  - [The Register: WSE-3 spec table](https://www.theregister.com/a/5289286)
  - [SemiAnalysis: Groq LPU 3](https://newsletter.semianalysis.com/p/nvidia-the-inference-kingdom-expands)
  - [SDxCentral: Groq 3 LPX](https://www.sdxcentral.com/news/nvidia-bets-big-on-bandwidth-with-groq-3-lpu-to-complement-gpus/)
  - [ServeTheHome: Groq 3 at Hot Chips 2026](https://servethehome.com/nvidias-groq-3-lpu-accelerators-for-heterogeneous-ai-compute-at-hot-chips-2026/)
  - [Futurum: Rubin CPX](https://futurumgroup.com/insights/nvidias-new-rubin-cpx-targets-future-of-large-scale-inference/)
  - [All About Circuits: HBM4 standard](https://www.allaboutcircuits.com/news/jedec-officially-releases-hbm4-memory-standard)
  - [TrendForce: CoWoS capacity](https://www.trendforce.com/news/?p=59316)
  - [arXiv 2604.08044: 3D-DRAM LLM accelerators](https://arxiv.org/pdf/2604.08044)
  - [Tom's Hardware: hybrid bonding in 2026](https://tomshardware.com/tech-industry/semiconductors/hybrid-bonding-roadmap-examined)
  - [Artificial Analysis: gpt-oss-120B providers](https://www.artificialanalysis.ai/models/gpt-oss-120b/providers)