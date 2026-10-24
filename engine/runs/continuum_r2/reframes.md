**ASSUMPTIONS:**
- One chip can be "best" across training, inference and edge at once. (contradicted: the archetypes have different dominant cost terms: margin and facility for A, hardware plus a staff floor for B, HBM movement for C, HBM and packaging for D)
- The right unit is the chip. (contradicted: cost and energy are set per served token or per run at rack and facility level, with network at 11–13% and facility at 20%)
- A better chip can make training several times cheaper. (contradicted: staff at about 33% does not shrink. Even with free hardware and networking, the remaining 43% caps the gain at about 2.3x. The ceiling block's "infinite ceiling, 0% untouchable" for B is a broken computation)
- Most inference cost can be reached through physical design. (contradicted: the largest term in A, the 28% vendor margin, is a pricing choice, not something architecture controls)
- HBM and CoWoS are available inputs to build on. (contradicted: HBM is reported sold out through 2026 and tight to 2028, and CoWoS is about 60% held by Nvidia)
- Decode is HBM-bandwidth-bound for all models. (partly contradicted: the 50% HBM share is an unsourced estimate, and absorbed-MLA decode is already compute-bound at FP8)
- Rubin and Ironwood specs are known well enough to compare against. (contradicted: the search gaps say they were not found)
- A capacity-limited SRAM design can scale to frontier models. (contradicted: Groq needed 576 chips for a 70B model, and Cerebras streams over about 150 GB/s off-wafer)
- Silicon is the hard part. (contradicted: Gaudi, Graphcore and PIM failed mainly on software)

**REFRAME 1:** What accelerator system minimizes joules per token and cost per token for long-context MoE decode? It must hold a stated tok/s/user floor and specify where the weights and KV cache live and the bytes/s each tier delivers. It is compared per rack against GB200/GB300 NVL72, an Ironwood pod and a Cerebras/Groq deployment at the same tok/s/user. | CHANGES: the unit becomes the served token at an SLO rather than the chip, and the scope narrows to the data-center decode archetype (A/C) | IMPORTANCE: high | POSSIBILITY: high | WHY: decode is where memory movement dominates and an architecture can act directly, and the metric is measurable against named baselines.

**REFRAME 2:** For each workload archetype, what is the largest cost or energy gain any chip design could deliver, given the terms it cannot touch (staff, the seller's margin, taxes)? Which archetypes leave room for a ≥2x "best" claim? | CHANGES: the bounding sub-question is answered before any design | IMPORTANCE: high | POSSIBILITY: high | WHY: it prevents claiming gains that are arithmetically impossible, such as 3x on training, and selects the target workload.

**REFRAME 3:** What is the highest delivered AI throughput per unit of the binding scarce inputs (per HBM stack, per CoWoS wafer, per facility kW) that can be built in volume in 2027–28? | CHANGES: "best" is redefined as best under supply and facility limits, not peak FLOPs | IMPORTANCE: high | POSSIBILITY: high | WHY: Attempts 1–2 show that supply and facility limits, not peak compute, cap what the leaders can deploy, so this is the measure on which a new design can credibly win.

**REFRAME 4:** What is the best training accelerator measured by hardware-plus-network cost per useful training FLOP at FP8/FP4? The claim must be backed by numerics evidence above 12B parameters, accept the ~2.3x total-cost ceiling, and target time-to-train. | CHANGES: the training metric moves from total run cost to the hardware share and wall-clock time | IMPORTANCE: medium | POSSIBILITY: medium | WHY: FP4 training beyond 12B is unproven, and staff cost caps the payoff.

**REFRAME 5:** Which architecture can run unmodified PyTorch, vLLM and JAX models through a compiler that does not lose to CUDA on the target workload? What is the minimal hardware departure that allows this? | CHANGES: software adoption becomes the primary constraint rather than a later section | IMPORTANCE: high | POSSIBILITY: medium | WHY: software is the most common cause of challenger failure, but compiler parity is hard to evidence before silicon exists.

**REFRAME 6:** Which roofline or simulation test, run on a known baseline such as measured H100 decode energy at 4K/16K context, would falsify a candidate's tokens-per-joule claim? | CHANGES: the falsification criterion is defined before the design | IMPORTANCE: medium | POSSIBILITY: high | WHY: the bandwidth model is already off by about 4x on H100 (27% of peak achieved), so the model must be calibrated before any claim.

**KEEP:** 1, 3 (they combine: decode cost per token at an SLO, measured per scarce input)
