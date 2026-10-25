**ASSUMPTIONS:**
- "Best" can be a single scalar, so one chip can top every metric at once. (Contradicted: SRAM parts win tok/s/user, while HBM racks win $/Mtok at about 50 tok/s/user and capacity. No design leads on both.)
- The chip is the right unit of comparison. (Contradicted: the accelerator package is only 38–60% of TCO. Rack, network and facility are 27–44%.)
- Energy efficiency (tokens per joule) drives cost. (Contradicted: energy is 9–11% of TCO and capex is about 85%.)
- One architecture should serve training, inference, data center and edge. (Contradicted: the four archetypes have different dominant terms and ceilings. Training is TIGHT and needs package and network cut together.)
- A new design can avoid HBM, CoWoS and power limits through better cores. (Contradicted: the lessons list HBM supply, CoWoS allocation and about 2.3 kW per package as binding, independent of core design.)
- Capacity and bandwidth must be traded off. (Partly contradicted: WSE-3 is 44 GB at 21 PB/s and Rubin is 288 GB at about 22 TB/s. These are points on a cost-per-byte curve, not a law.)
- A new software stack is acceptable. (Contradicted: Gaudi missed its $500M target on software, and Graphcore failed partly on software.)
- The 2026 reference numbers are reliable. (Contradicted: the sources conflict on CoWoS volume, Groq throughput, the terms of the Nvidia–Groq deal and Rubin bandwidth. Ironwood power is missing.)
- Fast SRAM serving failed commercially. (Contradicted: Nvidia's roughly $20B Groq deal prices low-latency decode highly.)

**REFRAME 1:** For LLM serving (dense and MoE, with stated context lengths), what system-level architecture moves the delivered $/Mtok-versus-tok/s/user Pareto frontier furthest beyond GB300 NVL72 ($0.06/Mtok at about 50 tok/s) and Cerebras/Groq (300–2,500 tok/s), and at which speed band? | CHANGES: metric from a chip scalar to a system cost-latency curve | IMPORTANCE: high | POSSIBILITY: high | WHY: it makes "best" checkable as a frontier dominated over a named band, and it uses the cost data actually in hand.

**REFRAME 2:** In high-interactivity decode (above 300 tok/s/user, 70B-class to MoE-class models), where silicon is about 60% of cost and the ceiling is 16.7x, how can the cost per GB of weight and KV capacity that sustains PB/s-class bandwidth per model replica fall 3–10x? The test is batch-1 roofline arithmetic: model bytes divided by aggregate bandwidth. | CHANGES: scope, narrowed to the one archetype the ceilings mark ROOM, and the target, set to the dominant cost term | IMPORTANCE: high | POSSIBILITY: high | WHY: only Archetype C lets a single term reach 3x, so the claim can be tested against one deciding number.

**REFRAME 3:** Using only the supply realistically allocable for 2027–28 (HBM bits, CoWoS wafers, at most about 2.3 kW per package, facility megawatts), which architecture maximises tokens per GW-year and per capex dollar? | CHANGES: the binding constraint, from peak performance to supply and power | IMPORTANCE: high | POSSIBILITY: medium | WHY: it addresses the lessons' "buildable on existing capacity" condition, but the supply numbers conflict and the facility share caps the gain.

**REFRAME 4:** For frontier training, with $ per useful training FLOP at cluster scale (MFU included) as the metric, can one design cut both the package cost and the scale-up and scale-out network cost on the same path? | CHANGES: workload split out, with two coupled terms targeted | IMPORTANCE: medium | POSSIBILITY: low | WHY: the ceiling is TIGHT and 3x needs three terms each cut 10x, so expect about 1.2–1.6x at most.

**REFRAME 5:** What architecture runs unmodified PyTorch, JAX and vLLM graphs at a stated fraction of roofline? Programming-model compatibility would be the first acceptance gate, ahead of peak specs. | CHANGES: software becomes a hard constraint, not a section of the answer | IMPORTANCE: medium | POSSIBILITY: medium | WHY: software is the most repeated cause of failure, but alone it does not make a chip best.

**KEEP:** 2, 1. Reframe 2 is the only route the ceilings leave open to a large, falsifiable gain. Reframe 1 places that gain on the overall cost-latency frontier, so it is not judged against a weak baseline.
