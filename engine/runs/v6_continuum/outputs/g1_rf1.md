**Targets and metric.** The workload is batch-1 to batch-8 decode at 300 tok/s/user or more, on 70B-class dense and MoE models. The metric is $/Mtok at fixed tok/s/user. Silicon is about 60% of cost in this regime, and the ceiling is 16.7x.

**Deciding arithmetic.** A 70 GB FP8 model at 1,000 tok/s needs 70 TB/s per replica.
- Fabric cannot stream weights at that rate. 70 TB/s over 200 Gb/s optical lanes is 2,800 lanes.
- So weights stay where they live and the fabric carries only activations. That is about 8 KB per layer per token at d=8192, or 0.65 MB per token.
- The fabric's real limit is latency. At 1 ms per token and 80 layers, the budget is 12.5 µs per layer.

**Facts versus my estimates.**
- Fact: Rubin has 288 GB at about 22 TB/s, roughly 0.076 TB/s per GB (secondary source).
- Fact: GDDR7 runs at 32 Gb/s × 32 bits, or 128 GB/s per 3 GB device, roughly 0.04 TB/s per GB, with no CoWoS needed.
- Estimate, needs verifying: GDDR7 costs 3–5x less per GB than HBM. Optical hops add about 1 µs each.

**Honest cap.** Cutting the network share alone (18–23%) by 10x gives only about 1.25x. Reaching 3x also requires moving bandwidth-per-dollar off CoWoS/HBM, so each idea below targets both terms on the same decode path.

**Candidates**
1. CPO NVLink replacement | P 0.45
2. CXL memory pool for KV | P 0.35
3. Prefill/decode split over optics | P 0.30
4. Photonic interposer (Lightmatter-style) | P 0.15
5. OCS-reconfigured topology (TPU-style) for slices | P 0.12
6. Weight-stationary GDDR7 bricks, optical activation pipeline | P 0.06
7. Attention-at-KV-pool nodes; fabric ships only q/o | P 0.08
8. Per-batch OCS expert placement for MoE | P 0.07

**Versus incumbents (my estimates).**
- 70 TB/s from about 175 GDDR7 devices (525 GB) costs about $2–4k of DRAM, against about 3 Rubin packages.
- It loses on training, because the fabric is too thin for gradient all-reduce.
- It loses on prefill, so prefill stays on GPUs.
- Against Cerebras, the per-hop latency of 1 µs or more caps it near 2,000 tok/s on 70B.

**Falsification test.** Use a cycle-accurate model of an 80-layer pipeline with measured CPO hop latency and jitter. If p99 per-layer time exceeds 12.5 µs at 1,000 tok/s, or if CPO costs more than $1 per Gb/s, the design fails.

**Software.** The design is a PyTorch/vLLM backend that performs pipeline sharding at compile time. Models run without change.

=== IDEAS ===
IDEA 1
NAME: GDDR7 bricks, optical activation pipeline
MECHANISM: Weights are sharded layer-wise across many small non-CoWoS packages, each a modest compute die with GDDR7 at roughly 0.04 TB/s per GB, joined by co-packaged optics. Only activations of about 8 KB per layer per token cross the fabric. This design avoids the limit that stopped NVLink racks, which tied bandwidth to scarce HBM and CoWoS, because the fabric carries latency-bound traffic rather than bandwidth-bound traffic. The deciding quantity is the p99 per-hop latency against a 12.5 µs per-layer budget at 1,000 tok/s.
VALUE: It could deliver 70 TB/s per 70B replica at an estimated 3–5x lower memory cost than HBM, free of the CoWoS queue.

IDEA 2
NAME: Attention at the KV pool
MECHANISM: KV caches live in pooled DRAM nodes that hold small attention engines. Decode dies send queries of a few KB and receive outputs, so the roughly 20 GB per user of 128k-context KV never crosses the fabric. The closest earlier work, Lamina-style attention offload, ran over copper and PCIe, while this uses memory-semantic optics and bandwidth-matched DRAM. The deciding quantity is attention-node bandwidth per dollar against the HBM it replaces.
VALUE: Long-context, high-interactivity decode stops consuming HBM capacity, which removes stranded per-package memory.

IDEA 3
NAME: Per-batch optical expert placement
MECHANISM: MoE experts are stationary on memory nodes. An optical circuit switch is retuned every few hundred milliseconds to the observed routing histogram, so hot expert pairs get direct circuits and cold experts share links. Ironwood's OCS reconfigures only at the slice level, while this tracks token routing. The deciding quantity is the all-to-all latency per MoE layer after reconfiguration.
VALUE: MoE decode would need fewer switch tiers and less replication of hot experts, which cuts both the network share and memory over-provisioning.