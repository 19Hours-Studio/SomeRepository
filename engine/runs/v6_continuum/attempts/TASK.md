# Task: the ledger of earlier attempts - what has been tried, and why the problem is still unsolved

QUESTION the ledger serves: Propose a new architecture for an AI accelerator chip, named "Continuum", that could credibly be called the best in the world. The asker has not said which workloads count: training, inference, or both. They have not said what "best" is measured by, or which kind of target (data center, edge, or other) the chip is for. A good answer therefore has to state its own target workloads and metrics, then defend the architecture against the current leading designs. Those designs include GPUs such as the Nvidia Rubin class, Google TPUs such as Ironwood, and SRAM-centric dataflow chips such as Cerebras WSE-3 and Groq LPU. The architecture should cover compute, memory hierarchy, interconnect, numerics, programming model, packaging and power. It should cite known physical, economic and manufacturing limits, and say what would need to be true for it to work. Reported 2026 reference points are listed in CONTEXT. Many are vendor or blog figures, and the sources disagree on some numbers.
A good answer: 
- The answer states explicit target workloads and a metric set. Examples are tokens/s per user, tokens per joule, cost per token, and training throughput. It says why those metrics define "best".
- It describes a coherent architecture with named blocks and quantified estimates. Estimates cover compute, on-chip and off-chip memory capacity and bandwidth, interconnect, power and die or package size. They are sanity-checked against roofline or bandwidth arithmetic.
- It compares quantitatively against at least three current designs (GPU, TPU, SRAM/wafer-scale) and says where Continuum wins, where it loses, and by how much.
- It names the main risks and the physical, process or supply limits (HBM supply, CoWoS packaging, power density, yield). It gives a falsifiable test or simulation plan that could prove the design wrong.
- It covers the software stack and programming model, and says what happens to existing models and frameworks.
- It separates established facts from the design's own assumptions and estimates.
- "Best in the world" is not asserted without evidence. Trade-offs are stated honestly.
Constraints: 
- The name is "Continuum".
- The answer is an architecture for an AI chip.
- Nothing else was specified. The answer must be a real, physically plausible design, not marketing text.

An unsolved problem means every earlier attempt stopped short for a reason that a re-invention would inherit. Build
the ledger of earlier attempts with sourced facts. Tools: WebSearch (WebFetch does not reach hosts here; use excerpts)
and Bash with python3. At most 15 searches. Write files only in the current directory; do not commit.

Facts already collected for this question (data; reuse their sources, and search only for what is missing):
(none recorded)

Cover methods in standard use (and what they still leave expensive), methods that stayed niche, pilots that were
dropped, and ideas that were costed and rejected, in any country, industry or period. For each: the binding reason it
did not solve the problem, with the number that shows it.

Final answer (text only), at most 1,000 words:
=== ATTEMPTS ===
ATTEMPT 1: <mechanism> | <where, who, when> | <standard / niche / dropped / rejected> | WHY IT DID NOT SOLVE IT: <reason with number> | <source>
(12-20 attempts, the most important first)
LESSONS: 3-6 lines - the limits any new answer must get past.
