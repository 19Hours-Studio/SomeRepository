I've written a full design for Continuum and checked it with a decode roofline model against Rubin, Ironwood, Cerebras and Groq LPX. The result is a design that leads on cost per token for interactive LLM serving. It is roughly at parity, or slightly behind, on training. I can't honestly call it "best in the world" without simulator results, but there is a stated way to prove it wrong.

**Target and metrics (my choice).** Data-center LLM decode on a 1-trillion-parameter mixture-of-experts model (MoE) with compressed-KV attention (MLA), based on the public Kimi-K2 config, at 8K and 128K context. Weights are stored at about 4.25 bits and the KV cache at about 4.5 bits. "Best" means the most tokens/s per MW while each user still gets at least 100, 300 or 1,000 tokens/s. That captures both tokens per joule and cost per token. Training throughput is a secondary metric and I don't claim a win there.

Script: `/home/user/SomeRepository/engine/runs/v6_continuum/baseline_2/roofline.py`; output: `/home/user/SomeRepository/engine/runs/v6_continuum/baseline_2/roofline_out.txt`. Nothing was committed.

=== IDEAS ===
IDEA 1
NAME: Stacked-SRAM weights, HBM-only KV package
MECHANISM: Each package has two compute dies of about 800 mm² each on N2/N3, rated at about 30 PF dense FP4 and 15 PF FP8. Each compute die sits face-to-face on an 800 mm² SRAM base die. Older-node SRAM at about 30 Mb/mm² gives about 2.25 GB per die, so roughly 4 GB per package. At about 14k bonds/mm² across 40 mm² of signal area, each die gets about 210 TB/s, so about 300 TB/s per package at about 0.12 pJ/bit. Eight HBM4 stacks add 288 GB at 22 TB/s, which is about 3 pJ/bit. The model's 545 GB of weights are pinned across the SRAM of a 144-package domain (136 packages minimum). HBM then carries only KV cache, so weight reads and KV reads no longer compete for the same bandwidth. Earlier runs found weight reads take 23–36% of GPU HBM time. Power at full load is about 288 W (SRAM) + 528 W (HBM) + 900 W (compute at 0.12 pJ per FP8 multiply-accumulate) + about 250 W of I/O, roughly 2.0 kW, inside a 2.3 kW package. That is the same class as Rubin's reported 1.8–2.3 kW. The package needs CoWoS-L at about 4.5× reticle, like Rubin, plus TSMC's SoIC hybrid bonding. The model gives these per-MW results against the best incumbent:
- **8K context:** 18.6 vs 16.5 Mtok/s/MW at ≥100 tok/s/user (1.12×); 18.6 vs 13.2 at ≥300 (1.41×).
- **128K context:** 2.55 vs 2.23 at ≥100 (1.14×); 2.38 vs 1.51 at ≥300 (1.58×).
- **Losses:** prefill FLOPs per watt are about 0.91× Rubin, and capex is about 10–15% higher (my estimate) for the SRAM dies and bonding.
VALUE: Cost per token comes out about 1.1–1.6× lower than Rubin NVL72 at interactive speeds (an estimate). It needs about 8× fewer SRAM chips than Groq LP30 (136 vs 1,064) and, unlike Cerebras, it doesn't cap concurrency: the modelled CS-3 cluster fits only about 15 users at 128K context.

IDEA 2
NAME: Near-HBM sparse-KV gather attention engine
MECHANISM: Attention units sit beside each HBM4 controller. The KV cache is stored as 4.5-bit NVFP4 rows (324 B per token per layer for MLA) and read with a hardware top-k gather, in the style of DeepSeek's sparse attention (top 2,048 tokens plus a 128-dim FP4 index). At 128K context this cuts KV traffic per user-token from 2.59 GB to 0.62 GB. Dense MLA decode needs 1.18 TFLOP per user-token at 128K, about 450 FLOP per byte at FP4 KV. So the HBM-side attention units are sized at about 10 PF FP8 (≈22 TB/s × 450) rather than relying on the main arrays. With sparse attention, Continuum gets 9.39 Mtok/s/MW against Rubin's 5.74 (1.64×) and Ironwood's 7.04 (1.33×). The model assumes the gather sustains at least 80% of HBM peak at 324 B granularity; only a DRAM simulator or silicon can confirm that.
VALUE: Long-context throughput per MW rises about 3.7× over dense attention on the same hardware, and Continuum keeps a 1.3–1.6× lead over incumbents running the same sparse model.

IDEA 3
NAME: Compiler-scheduled deterministic scale-up fabric
MECHANISM: The 144 packages are linked at 3.6 TB/s each in a statically scheduled network, Groq-style. The compiler fixes when every MoE dispatch and combine happens, so there are no software launch or handshake costs. The design target is 1.5 µs per all-to-all, against an assumed 8 µs for NVLink-class software collectives. At 61 layers × 2 collectives, one token's critical path drops from about 0.98 ms to 0.18 ms, giving 5,450 vs 1,010 tok/s/user at batch size 1. If latency is really 4 µs, single-user speed falls to 2,050 tok/s, but per-MW still beats Rubin, e.g. 2.08 vs 1.51 Mtok/s/MW at 128K and ≥300 tok/s/user. Software path: PyTorch/JAX export (torch.export / StableHLO) feeds a static dataflow compiler, and a vLLM/SGLang backend plugs in on top. MoE routing uses capacity-padded static schedules. Standard Transformer, MoE, MLA and GQA models run unchanged, but custom CUDA kernels don't port.
VALUE: At ≥1,000 tok/s/user it is the only design in the model with both high throughput and high per-user speed: 14.8 Mtok/s/MW at 8K, against about 0 for Rubin and Ironwood in this model. That 1,000 tok/s figure rests entirely on the latency assumption.

IDEA 4
NAME: One compute die, two phase-split SKUs
MECHANISM: Prefill and training are compute-bound, so the SRAM base die adds cost there without adding speed. A "C" SKU uses the same compute die on a plain interposer with HBM only, while the "D" SKU described above handles decode. They are mixed at a measured prefill-to-decode ratio, like Nvidia's CPX/Rubin pairing at 1:1. Training on the C SKU sits at about 0.86–1.0× Rubin per package (30 vs 35 PF FP4) because the compute die and HBM are the same class. I make no claim that it wins at training.
VALUE: It avoids the roughly 10–15% SRAM cost on compute-bound work and shares one tape-out between both SKUs. Training is at parity, not best.

NOTES
- **Facts (vendor or press figures):**
  - Rubin: 288 GB HBM4; 22 TB/s, though one source says 13; FP4 reported as 50 PF, which may be 35 PF dense plus sparsity; 17.5 PF FP8 dense; 1.8–2.3 kW per GPU; 190–230 kW per NVL72 rack; NVLink 6 at 3.6 TB/s.
  - Ironwood: 4,614 TFLOPS FP8, 192 GiB, 7.38 TB/s, 1.2 TB/s ICI, 9,216-chip pod, about 10 MW per pod (≈1.1 kW per chip).
  - Cerebras WSE-3: 44 GB SRAM, 21 PB/s, 125 PF is a sparse figure (about 12.5 PF dense FP16), 23 kW system.
  - Groq LP30: 512 MB and 150 TB/s per chip; an LPX rack is 256 chips with 128 GB, and power is not published.
  - HBM4 (JESD270-4): 2048-bit interface, 2 TB/s per stack, up to 16-high and 64 GB.
  - SoIC hybrid bonding: 6 µm pitch; about 14k face-to-face signals/mm² against about 1.5k face-to-back.
  - CoWoS supply: about 120–140k wafers per month by end-2026, with Nvidia booking more than half.
- **My assumptions (need a simulator or silicon):**
  - 0.12 pJ/bit for SRAM plus bonding, 3 pJ/bit for HBM4, 0.12 pJ per FP8 multiply-accumulate. The Rubin calibration is about 0.23 pJ all-in.
  - 1.5 µs all-to-all latency against 8 µs for GPUs.
  - 60% compute utilisation; 25% rack power overhead.
  - Groq LP30 at 0.8 kW all-in; this drives LPX's poor showing (0.4–3.8 Mtok/s/MW).
  - 10–15% higher package cost.
- **Main risks:**
  - Yield of an 800 mm² bonded die stack, and losses at the known-good-die and bonding steps.
  - Power delivered through the SRAM base die's TSVs, at a power density similar to Rubin.
  - HBM4 shipping at 13 rather than 22 TB/s: at 128K and ≥100 tok/s/user, Continuum falls to 1.64 Mtok/s/MW, below Rubin at 22 TB/s, though still 1.3× Rubin at 13.
  - Short HBM and CoWoS supply.
  - Models that outgrow about 576 GB at FP4, which would need a larger domain.
- **How to prove it wrong:**
  1. Simulate the fabric with a cycle-level network model (BookSim or a gem5 setup), using DeepSeek/Kimi MoE routing traces. If p99 all-to-all exceeds 4 µs, the per-user speed claims of Ideas 1 and 3 fail.
  2. Use LLMCompass or Timeloop+Accelergy to check the power split and the 0.12 pJ/bit SRAM figure. If SRAM energy exceeds 0.3 pJ/bit, the package goes over budget.
  3. Measure HBM4 efficiency for 324 B random gathers with Ramulator 2. Below 60%, Idea 2's advantage disappears.
  4. Test whether FP4 weights with an NVFP4 KV cache hold accuracy on long-context evals for open models; the evals can run once weights can be downloaded, which they can't here.
  5. Compare against the MLPerf Inference and Artificial Analysis numbers for Rubin and LPX once published. If Continuum shows less than 1.2× per MW at ≥300 tok/s/user, it should not be called "best".
- **Sources:**
  - [CUDO Rubin](https://www.cudocompute.com/products/nvidia-vera-rubin), [Spheron NVL72](https://www.spheron.network/blog/nvidia-vera-rubin-nvl72-guide/), [Hashrate Index NVL72](https://hashrateindex.com/blog/nvidia-vera-rubin-nvl72-specs-breakdown/), [Bizon GTC 2026](https://bizon-tech.com/blog/nvidia-gtc-2026-key-announcements), [VRLA NVLink6](https://vrlatech.com/nvidia-vera-rubin-architecture-explained/), [Naddod CPX](https://www.naddod.com/fr/blog/rubin-cpx-nvidia-dedicated-inference-gpu)
  - [Google TPU7x docs](https://docs.cloud.google.com/tpu/docs/tpu7x?authuser=0), [The Register Ironwood](https://www.theregister.com/2025/11/06/googles_ironwood_tpus_ai/), [Register Ironwood debut](https://www.theregister.com/2025/04/10/googles_7thgen_ironwood_tpus_debut/)
  - [Spheron Cerebras](https://www.spheron.network/blog/cerebras-vs-nvidia-h100-inference-2026/), [flopper WSE-3](https://flopper.io/gpu/cerebras-wse-3)
  - [StorageReview LPX](https://www.storagereview.com/news/nvidia-groq-3-lpx-everything-we-know), [MoreThanMoore LP30](https://morethanmoore.substack.com/p/nvidia-introduces-groq-lp30-and-lpx), [PCGH LPX](https://www.pcgameshardware.de/Kuenstliche-Intelligenz-Hardware-279517/News/Nvidia-Groq-3-LPX-Vera-Rubin-Vollproduktion-Token-1552188/)
  - [JEDEC HBM4 (BusinessWire)](https://businesswire.com/news/home/20250416843598/en/JEDEC-and-Industry-Leaders-Collaborate-to-Release-JESD270-4-HBM4-Standard-Advancing-Bandwidth-Efficiency-and-Capacity-for-AI-and-HPC), [Profesional Review HBM pJ/bit](https://www.profesionalreview.com/2025/11/02/hbm4e-vs-hbm3/)
  - [Tom's Hardware hybrid bonding](https://tomshardware.com/tech-industry/semiconductors/hybrid-bonding-roadmap-examined), [TrendForce hybrid-bond timeline](https://www.trendforce.com/news/2026/07/07/news-samsung-sk-hynix-reportedly-reconsider-hybrid-bonding-timeline-16-high-hbm4e-may-be-earliest-adoption/)
  - [TrendForce CoWoS](https://www.trendforce.com/news/2026/09/14/news-tsmc-reportedly-targets-22-2nm-16-3nm-capacity-boost-by-mid-2027-cowos-to-double-by-2028/), [Digitimes CoWoS](https://www.digitimes.com/news/a20251210PD218.html)