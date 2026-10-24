=== BRIEF ===
TYPE: invent

QUESTION: Propose a new architecture for an AI accelerator chip, named "Continuum", that could credibly be called the best in the world. The asker has not said which workloads count: training, inference, or both. They have not said what "best" is measured by, or which kind of target (data center, edge, or other) the chip is for. A good answer therefore has to state its own target workloads and metrics, then defend the architecture against the current leading designs. Those designs include GPUs such as the Nvidia Rubin class, Google TPUs such as Ironwood, and SRAM-centric dataflow chips such as Cerebras WSE-3 and Groq LPU. The architecture should cover compute, memory hierarchy, interconnect, numerics, programming model, packaging and power. It should cite known physical, economic and manufacturing limits, and say what would need to be true for it to work. Reported 2026 reference points are listed in CONTEXT. Many are vendor or blog figures, and the sources disagree on some numbers.

SUCCESS:
- The answer states explicit target workloads and a metric set. Examples are tokens/s per user, tokens per joule, cost per token, and training throughput. It says why those metrics define "best".
- It describes a coherent architecture with named blocks and quantified estimates. Estimates cover compute, on-chip and off-chip memory capacity and bandwidth, interconnect, power and die or package size. They are sanity-checked against roofline or bandwidth arithmetic.
- It compares quantitatively against at least three current designs (GPU, TPU, SRAM/wafer-scale) and says where Continuum wins, where it loses, and by how much.
- It names the main risks and the physical, process or supply limits (HBM supply, CoWoS packaging, power density, yield). It gives a falsifiable test or simulation plan that could prove the design wrong.
- It covers the software stack and programming model, and says what happens to existing models and frameworks.
- It separates established facts from the design's own assumptions and estimates.
- "Best in the world" is not asserted without evidence. Trade-offs are stated honestly.

CONSTRAINTS:
- The name is "Continuum".
- The answer is an architecture for an AI chip.
- Nothing else was specified. The answer must be a real, physically plausible design, not marketing text.

CONTEXT:
- Nvidia Rubin: 288 GB HBM4, about 22 TB/s, 50 PFLOPS FP4 (35 dense), NVLink 6 at 3.6 TB/s per GPU. Per-GPU TDP is unconfirmed, with estimates of 1.8–2.3 kW. Source: https://blog.barrack.ai/nvidia-rubin-specs-architecture-2026/
- Google Ironwood TPU: 4,614 TFLOPS FP8, 192 GB HBM3e, about 7.37 TB/s, 9,216-chip pod, 2x perf/W over Trillium. Chip wattage is not published. Source: https://blog.google/products/google-cloud/ironwood-tpu-age-of-inference/
- Cerebras WSE-3 holds 44 GB of on-chip SRAM. Reported gpt-oss-120B speeds are about 3,000 tok/s on Cerebras and about 480–490 tok/s on Groq. These are vendor or aggregator figures at batch size 1. Source: https://www.cerebras.ai/blog/cerebras-cs-3-vs-groq-lpu
- Groq LPU keeps weights in hundreds of MB of on-chip SRAM, so large models need many chips. A chip draws about 375 W (a Cerebras claim). Source: https://www.spheron.network/blog/groq-lpu-vs-cerebras-wse-cheapest-inference-2026/
- Memory wall: one blog estimate has compute growing about 3x per 2 years against about 1.6x for bandwidth. A 70B FP16 model on an H100 (3.35 TB/s) needs at least about 42 ms per token for weight reads alone. Source: https://www.spheron.network/blog/ai-memory-wall-inference-latency-guide-2026/
- KV cache grows with context length and batch size, and is a growing inference bottleneck. Source: https://www.datacenterknowledge.com/data-center-hardware/scaling-the-memory-wall-hbm-cxl-and-the-new-gpu-playbook
- Supply: HBM is reported as sold out through 2026, and CoWoS is congested. HBM costs 5–10x more per GB than DRAM (secondary sources). Qualcomm has announced a near-memory design under LPDDR. HBM4 integrates logic dies. Source: the same datacenterknowledge article and https://www.wing.vc/content/the-ai-memory-stack

DATA:
- Vendor datasheets and whitepapers: Nvidia, Google Cloud TPU docs, Cerebras, Groq, AMD Instinct.
- MLPerf Inference and Training results (MLCommons).
- Artificial Analysis tokens/s benchmarks.
- Hot Chips and ISSCC papers.
- JEDEC HBM4 spec.
- Open model architecture parameters, such as Llama and gpt-oss sizes, for roofline calculations.
- Public simulators: Timeloop, Accelergy, gem5-based tools, LLMCompass.

ASSUMPTIONS:
- A single "best" architecture exists, independent of workload and metric.
- "AI chip" means a data-center accelerator, not edge or mobile.
- The chip can be designed at roughly current leading-edge process, packaging and memory availability.
- The answer is a conceptual design, and no tape-out or prototype is expected.
- Training and inference can both be served by one architecture.
- The name "Continuum" implies a specific design idea. That is unstated, and the design should not be bound to it.

CORRECTED:
- The superlative "best in the world" was turned into explicit, checkable metrics and a stated workload target, because it is undefined as written.
- Nothing was changed about the name.
- The question was in Russian, and the answer should be given in Russian.

UNCLEAR:
1. Is the target data-center training, data-center inference, both, or edge?
2. Which metric matters most: absolute speed, cost per token, energy, or something else? Is there a power, die-size or process budget?
3. How deep should the answer go: a conceptual pitch, or a detailed microarchitecture with numbers?

MODE: standard

Sources:
- [Nvidia Rubin at GTC 2026](https://blog.barrack.ai/nvidia-rubin-specs-architecture-2026/)
- [Google Ironwood](https://blog.google/products/google-cloud/ironwood-tpu-age-of-inference/)
- [Cerebras CS-3 vs Groq LPU](https://www.cerebras.ai/blog/cerebras-cs-3-vs-groq-lpu)
- [Spheron: Groq LPU vs Cerebras WSE](https://www.spheron.network/blog/groq-lpu-vs-cerebras-wse-cheapest-inference-2026/)
- [Spheron: AI memory wall](https://www.spheron.network/blog/ai-memory-wall-inference-latency-guide-2026/)
- [Data Center Knowledge: Scaling the Memory Wall](https://www.datacenterknowledge.com/data-center-hardware/scaling-the-memory-wall-hbm-cxl-and-the-new-gpu-playbook)
- [Wing VC: The AI Memory Stack](https://www.wing.vc/content/the-ai-memory-stack)